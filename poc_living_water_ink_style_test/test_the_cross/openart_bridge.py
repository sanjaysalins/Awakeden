"""openart_bridge.py -- file-bridge client for OpenArt image/video generation.

OpenArt has no REST API or API key (MCP-only, OAuth: "no keys to create,
rotate, or leak"). A standalone script (episode.py) cannot call it directly
the way it calls hf.exe. This writes a request file and BLOCKS, polling for
a reply -- same shape as AGENT_BRIDGE.md's LLM bridge, on its own channel
(gen_requests/ gen_responses/) so it can't collide with the text servicer.

A live Claude Code session (holding the OpenArt MCP connection) must be
watching .agent_bridge/gen_requests/ and servicing each file: upload any
local refs, call the matching mcp__openart__generate_image/video tool, wait
for completion, download the result to the request's out_path, and write
the response JSON. See AGENT_BRIDGE.md's "Image/video generation" section
for the exact servicing steps.

Policy (locked 2026-08-27, user instruction): on any failure or timeout this
raises -- callers must NOT silently fall back to Higgsfield. Falling back
requires an explicit human decision (re-run with SWIRLS_GEN_PROVIDER=hf).

SWIRLS SHORT GUARDED PROTOCOL (design v3.2 section 5.1): a request whose
`out_path` sits under a folder holding a `.swirls_short` marker is GUARDED.
It never goes through the legacy folder: it needs a guard context
(swirls_guard.guard_context), goes through swirls_guard.before() first, and is written to
`gen_requests_guarded/` (only a servicer that read POC\\SWIRLS_SHORT_SERVICER.md watches it).
The client keeps a heartbeat file fresh, and on ANY stop (timeout, error, Ctrl-C) tries to
RENAME the request into `gen_requests_guarded/cancelled/`: rename wins = never claimed
(CANCELLED_UNCLAIMED); rename fails = a servicer claimed it (LATE_PENDING, settled only by
`fetch`). Requests outside a marked folder behave exactly as before.
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any

MARKER = ".swirls_short"
BRIDGE_DIR = Path(os.environ.get("AGENT_BRIDGE_DIR", Path(__file__).resolve().parents[2] / ".agent_bridge"))
REQUESTS_DIR = BRIDGE_DIR / "gen_requests"
RESPONSES_DIR = BRIDGE_DIR / "gen_responses"
ARCHIVE_DIR = BRIDGE_DIR / "gen_archive"
GUARDED_DIR = BRIDGE_DIR / "gen_requests_guarded"
CANCELLED_DIR = GUARDED_DIR / "cancelled"
CLAIMED_DIR = BRIDGE_DIR / "gen_claimed"
STAGING_DIR = BRIDGE_DIR / "gen_staging"
RECEIPTS_DIR = BRIDGE_DIR / "gen_receipts"
TIMEOUT_SECONDS = float(os.environ.get("OPENART_BRIDGE_TIMEOUT", "3600"))
POLL_SECONDS = float(os.environ.get("OPENART_BRIDGE_POLL", "3"))
HEARTBEAT_SECONDS = 10.0
HEARTBEAT_STALE_SECONDS = 60.0
SERVICER_RULES = "poc_living_water_ink_style_test/SWIRLS_SHORT_SERVICER.md"


def configure(bridge_dir: Path) -> None:
    """Point every bridge folder at `bridge_dir` (tests use a temp dir; production never calls this)."""
    global BRIDGE_DIR, REQUESTS_DIR, RESPONSES_DIR, ARCHIVE_DIR, GUARDED_DIR, CANCELLED_DIR
    global CLAIMED_DIR, STAGING_DIR, RECEIPTS_DIR
    BRIDGE_DIR = Path(bridge_dir)
    REQUESTS_DIR = BRIDGE_DIR / "gen_requests"
    RESPONSES_DIR = BRIDGE_DIR / "gen_responses"
    ARCHIVE_DIR = BRIDGE_DIR / "gen_archive"
    GUARDED_DIR = BRIDGE_DIR / "gen_requests_guarded"
    CANCELLED_DIR = GUARDED_DIR / "cancelled"
    CLAIMED_DIR = BRIDGE_DIR / "gen_claimed"
    STAGING_DIR = BRIDGE_DIR / "gen_staging"
    RECEIPTS_DIR = BRIDGE_DIR / "gen_receipts"


class OpenArtBridgeError(RuntimeError):
    pass


class OpenArtBridgeTimeout(OpenArtBridgeError):
    pass


def find_marker(path) -> tuple[Path, dict] | None:
    """(episode_dir, marker dict) if `path` (or a parent) holds a `.swirls_short` marker."""
    p = Path(path).resolve()
    for parent in [p, *p.parents]:
        m = parent / MARKER
        if m.is_file():
            try:
                return parent, json.loads(m.read_text(encoding="utf-8"))
            except Exception:
                return parent, {}
    return None


def _guard():
    here = str(Path(__file__).resolve().parents[1])   # POC dir holds swirls_guard.py
    if here not in sys.path:
        sys.path.insert(0, here)
    import swirls_guard
    return swirls_guard


def submit(payload: dict[str, Any]) -> dict[str, Any]:
    """Write a gen request, block polling for the matching response, return it.

    Raises OpenArtBridgeError/OpenArtBridgeTimeout on failure. Does NOT fall
    back to another provider -- that is a human decision, not this module's.
    """
    out = payload.get("out_path")
    hit = find_marker(out) if out else None
    if hit is not None:
        return _submit_guarded(payload, hit)
    return _submit_legacy(payload)


def _submit_legacy(payload: dict[str, Any]) -> dict[str, Any]:
    REQUESTS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    req_id = uuid.uuid4().hex[:12]
    payload = {"id": req_id, **payload}
    req_path = REQUESTS_DIR / f"{req_id}.request.json"
    resp_path = RESPONSES_DIR / f"{req_id}.response.json"
    req_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"  [openart-bridge] wrote {req_path.name} -- waiting for a live Claude "
          f"session to service it (timeout {int(TIMEOUT_SECONDS)}s)...")
    waited = 0.0
    while not resp_path.exists():
        time.sleep(POLL_SECONDS)
        waited += POLL_SECONDS
        if waited >= TIMEOUT_SECONDS:
            raise OpenArtBridgeTimeout(
                f"no response for {req_path.name} after {int(waited)}s -- is a Claude "
                f"Code session watching {REQUESTS_DIR}? Not falling back to HF "
                f"automatically -- re-run with SWIRLS_GEN_PROVIDER=hf to confirm that "
                f"fallback."
            )
    resp = json.loads(resp_path.read_text(encoding="utf-8"))
    req_path.replace(ARCHIVE_DIR / req_path.name)
    resp_path.replace(ARCHIVE_DIR / resp_path.name)
    if resp.get("status") != "ok":
        raise OpenArtBridgeError(
            f"{req_id} failed: {resp.get('error', 'unknown error')} -- not falling "
            f"back to HF automatically -- re-run with SWIRLS_GEN_PROVIDER=hf to "
            f"confirm that fallback."
        )
    return resp


# ------------------------------------------------------------- guarded protocol ---
def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def cancel_request(rid: str) -> str:
    """Try to RENAME the request into cancelled/. Rename wins -> 'CANCELLED_UNCLAIMED' (never
    claimed). Rename fails -> 'LATE_PENDING' (a servicer already claimed it)."""
    req = GUARDED_DIR / f"{rid}.request.json"
    CANCELLED_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.replace(req, CANCELLED_DIR / req.name)
        return "CANCELLED_UNCLAIMED"
    except OSError:
        return "LATE_PENDING"


def _submit_guarded(payload: dict[str, Any], hit: tuple[Path, dict]) -> dict[str, Any]:
    g = _guard()
    ep_dir, marker = hit
    ctx = g.current_context()
    if ctx is None:
        raise OpenArtBridgeError("REFUSED by SWS-G0: no guard context (a marked episode can only "
                                 "spend through swirls_episode.py); nothing was written")
    try:
        row = g.before(ctx, payload, provider=os.environ.get("SWIRLS_GEN_PROVIDER", "openart"))
    except g.SpendRefused as e:
        raise OpenArtBridgeError(f"REFUSED by SWS-G0: {e}") from e
    rid = row["id"]
    GUARDED_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    req_path = GUARDED_DIR / f"{rid}.request.json"
    hb_path = GUARDED_DIR / f"{rid}.heartbeat"
    resp_path = RESPONSES_DIR / f"{rid}.response.json"
    req = {"id": rid, "rid": rid, "episode_id": marker.get("episode_id"),
           "not_after": time.time() + TIMEOUT_SECONDS, "heartbeat": str(hb_path),
           "priced": g.priced_fields(payload), "sha256": g.payload_hashes(payload),
           "servicer_rules": SERVICER_RULES, "payload": payload, **payload}
    req["id"] = rid
    hb_path.write_text(str(time.time()), encoding="utf-8")
    _atomic_write(req_path, json.dumps(req, indent=2, ensure_ascii=False))
    print(f"  [openart-bridge/guarded] wrote {req_path.name} (price {row['price']} {row['unit']}) -- "
          f"waiting for a servicer that read {SERVICER_RULES}")
    done = False
    try:
        waited, last_hb = 0.0, time.time()
        while not resp_path.exists():
            time.sleep(POLL_SECONDS)
            waited += POLL_SECONDS
            if time.time() - last_hb >= HEARTBEAT_SECONDS:
                hb_path.write_text(str(time.time()), encoding="utf-8")
                last_hb = time.time()
            if waited >= TIMEOUT_SECONDS:
                raise OpenArtBridgeTimeout(f"no response for {req_path.name} after {int(waited)}s")
        for _ in range(40):            # Windows can briefly refuse a read while the reply is being swapped in
            try:
                resp = json.loads(resp_path.read_text(encoding="utf-8"))
                break
            except (OSError, ValueError):
                time.sleep(0.05)
        else:
            raise OpenArtBridgeError(f"reply {resp_path.name} is unreadable")
        done = True
    finally:
        if not done:
            status = cancel_request(rid)
            g.mark(ep_dir, rid, status)
            print(f"  [openart-bridge/guarded] stopped: {rid} -> {status}")
    try:
        ok = g.after(ctx, rid, resp)
    except g.SpendRefused as e:
        raise OpenArtBridgeError(f"{rid}: {e}") from e
    if resp.get("status") != "ok" or not ok:
        raise OpenArtBridgeError(
            f"{rid} not settled: {resp.get('error') or 'receipt did not verify'} -- row is open "
            f"(UNRESOLVED); settle it with `fetch {rid}` / `confirm {rid}`; nothing was charged to a new request")
    return resp
