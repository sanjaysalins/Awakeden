"""Agent-mode LLM bridge — answer the engine's LLM calls from the in-chat agent
(Claude Code on the Max subscription) instead of the metered Anthropic API.

How it works
------------
When `LLM_PROVIDER=agent`, every LLM call in the engine (text + Vision) is turned
into a pair of files instead of an API request:

    .agent_bridge/requests/<id>.request.md   <- the engine writes the full prompt
    .agent_bridge/responses/<id>.txt          <- the AGENT writes the raw reply

The engine writes the request, prints a loud banner, then BLOCKS, polling for the
response file. The in-chat agent watches the requests dir, reads each `.request.md`
(and, for Vision calls, the referenced image with the Read tool), reasons, and
writes the matching `<id>.txt`. The engine reads it and continues — zero API spend.

Operational pattern: run the engine with `run_in_background`, then service the
requests from chat until the background process exits.

This module is intentionally dependency-light (only the stdlib) so the SAME file
can be imported by the sibling PythonProject1 tools (e.g. image_to_kling.py),
which run under a different venv. It reads its directory + knobs from env vars so
it does NOT need this project's `config` module:

    LLM_PROVIDER        agent | api          (default: agent)
    AGENT_BRIDGE_DIR    path                 (default: <this repo>/.agent_bridge)
    AGENT_BRIDGE_TIMEOUT seconds per call    (default: 3600)
    AGENT_BRIDGE_POLL   poll interval, sec   (default: 1.5)
"""
from __future__ import annotations

import os
import threading
import time
import uuid
from pathlib import Path


# ----------------------------------------------------------------------------
# Configuration (env-driven so both projects share one bridge with no imports)
# ----------------------------------------------------------------------------
def provider() -> str:
    return os.getenv("LLM_PROVIDER", "agent").strip().lower()


def enabled() -> bool:
    return provider() == "agent"


def _bridge_dir() -> Path:
    override = os.getenv("AGENT_BRIDGE_DIR")
    if override:
        return Path(override)
    # Default: a `.agent_bridge` next to this file's project root (JesusInTheBible).
    return Path(__file__).resolve().parent.parent / ".agent_bridge"


def _timeout() -> float:
    return float(os.getenv("AGENT_BRIDGE_TIMEOUT", "3600"))


def _poll() -> float:
    return float(os.getenv("AGENT_BRIDGE_POLL", "1.5"))


# ----------------------------------------------------------------------------
# Id allocation — readable ordinal + uuid suffix, unique across threads/procs
# ----------------------------------------------------------------------------
_ord_lock = threading.Lock()
_ordinal = 0


def _next_id() -> str:
    global _ordinal
    with _ord_lock:
        _ordinal += 1
        n = _ordinal
    return f"{n:04d}_{uuid.uuid4().hex[:6]}"


def _dirs() -> tuple[Path, Path, Path]:
    base = _bridge_dir()
    req = base / "requests"
    resp = base / "responses"
    img = base / "images"
    for d in (req, resp, img):
        d.mkdir(parents=True, exist_ok=True)
    return req, resp, img


def print_startup_banner() -> None:
    """Loud one-time notice at CLI start so agent-mode is never a surprise."""
    if not enabled():
        return
    base = _bridge_dir()
    line = "#" * 72
    print(f"\n{line}")
    print("#  LLM_PROVIDER=agent  — engine LLM calls route to the in-chat agent")
    print("#  (Claude Code / Max subscription) via the file bridge. NO metered API.")
    print(f"#  bridge dir : {base}")
    print("#  RUN ME IN THE BACKGROUND and service requests from chat:")
    print(f"#    new requests appear in   {base / 'requests'}")
    print(f"#    write each reply to      {base / 'responses'}/<id>.txt")
    print("#  For an unattended run with the metered API instead: set LLM_PROVIDER=api")
    print(f"{line}\n", flush=True)


_shared_written = False
_shared_lock = threading.Lock()


def _write_shared_context(text: str) -> str:
    """Write the big cached prefix (constitution + series library) ONCE per run
    so individual requests can reference it instead of repeating ~10KB each."""
    global _shared_written
    base = _bridge_dir()
    base.mkdir(parents=True, exist_ok=True)
    path = base / "shared_context.md"
    with _shared_lock:
        if not _shared_written or not path.exists():
            path.write_text(text, encoding="utf-8")
            _shared_written = True
    return str(path)


# ----------------------------------------------------------------------------
# Core submit/poll
# ----------------------------------------------------------------------------
def _banner(req_id: str, kind: str, label: str, req_path: Path, resp_path: Path,
            image_path: Path | None) -> None:
    line = "=" * 72
    print(f"\n{line}", flush=True)
    print(f"  AGENT-BRIDGE REQUEST {req_id}  [{kind}]  {label}", flush=True)
    print(f"  prompt : {req_path}", flush=True)
    if image_path is not None:
        print(f"  image  : {image_path}", flush=True)
    print(f"  REPLY  -> write the raw model output to: {resp_path}", flush=True)
    print(f"  (engine is blocked, polling every {_poll():.1f}s up to {_timeout():.0f}s)", flush=True)
    print(f"{line}\n", flush=True)


def _await_response(req_id: str, resp_path: Path, label: str) -> str:
    deadline = time.time() + _timeout()
    waited = 0.0
    while time.time() < deadline:
        if resp_path.exists():
            # Guard against a half-written file: require it to be non-empty and
            # stable across one poll interval.
            size1 = resp_path.stat().st_size
            time.sleep(min(0.4, _poll()))
            if resp_path.exists() and resp_path.stat().st_size == size1 and size1 > 0:
                return resp_path.read_text(encoding="utf-8").strip()
        time.sleep(_poll())
        waited += _poll()
        if waited % 30 < _poll():
            print(f"  …still waiting on agent reply for {req_id} ({label})", flush=True)
    raise RuntimeError(
        f"agent-bridge timed out after {_timeout():.0f}s waiting for {resp_path}. "
        f"Either service the request (write the reply file) or set LLM_PROVIDER=api."
    )


def call_text(role: str, user: str, model: str, shared: str | None = None,
              label: str = "text") -> str:
    """Submit a text LLM call to the in-chat agent and block for the reply."""
    req_dir, resp_dir, _ = _dirs()
    req_id = _next_id()
    req_path = req_dir / f"{req_id}.request.md"
    resp_path = resp_dir / f"{req_id}.txt"

    shared_ref = ""
    if shared:
        sp = _write_shared_context(shared)
        shared_ref = (
            "## SHARED CONTEXT (constitution + series library — binding)\n"
            f"The stable system prefix is in: `{sp}`\n"
            "(It is identical on every call; read it once per session.)\n\n"
        )

    body = (
        f"<!-- agent-bridge id={req_id} kind=text model={model} -->\n"
        f"# AGENT-BRIDGE REQUEST {req_id} — text ({label})\n\n"
        f"**Model the API would use:** `{model}`\n\n"
        "Answer as that model would: produce ONLY the raw reply the engine expects "
        "(usually a single JSON object, optionally in a ```json fence — no extra prose). "
        f"Write it to `{resp_path}`.\n\n"
        "## SYSTEM / ROLE INSTRUCTIONS\n"
        f"{role}\n\n"
        f"{shared_ref}"
        "## USER MESSAGE\n"
        f"{user}\n"
    )
    tmp = req_path.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.replace(req_path)

    _banner(req_id, "text", label, req_path, resp_path, None)
    reply = _await_response(req_id, resp_path, label)
    _archive(req_id, req_path, resp_path)
    return reply


def call_vision(role: str, user: str, image_bytes: bytes, media: str, model: str,
                label: str = "vision") -> str:
    """Submit a Vision call. Writes the image to disk so the agent can view it
    with the Read tool (better than the SDK audit — CLAUDE.md guidance)."""
    req_dir, resp_dir, img_dir = _dirs()
    req_id = _next_id()
    ext = ".jpg" if "jpeg" in media else ".png"
    img_path = img_dir / f"{req_id}{ext}"
    img_path.write_bytes(image_bytes)
    req_path = req_dir / f"{req_id}.request.md"
    resp_path = resp_dir / f"{req_id}.txt"

    body = (
        f"<!-- agent-bridge id={req_id} kind=vision model={model} -->\n"
        f"# AGENT-BRIDGE REQUEST {req_id} — vision ({label})\n\n"
        f"**LOOK AT THE IMAGE FIRST** with the Read tool: `{img_path}`\n\n"
        "Then answer as the auditor described below. Produce ONLY the raw reply "
        f"(a single JSON object, optionally fenced — no extra prose) and write it to `{resp_path}`.\n\n"
        "## AUDITOR ROLE\n"
        f"{role}\n\n"
        "## USER MESSAGE\n"
        f"{user}\n"
    )
    tmp = req_path.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.replace(req_path)

    _banner(req_id, "vision", label, req_path, resp_path, img_path)
    reply = _await_response(req_id, resp_path, label)
    _archive(req_id, req_path, resp_path)
    return reply


def _archive(req_id: str, req_path: Path, resp_path: Path) -> None:
    """Move the serviced request+response into archive/ so the live dirs stay
    clean and the agent's 'unanswered request' scan is unambiguous."""
    base = _bridge_dir()
    arc = base / "archive"
    arc.mkdir(parents=True, exist_ok=True)
    for p in (req_path, resp_path):
        try:
            if p.exists():
                p.replace(arc / p.name)
        except OSError:
            pass
