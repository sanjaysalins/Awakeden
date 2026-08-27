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
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

BRIDGE_DIR = Path(os.environ.get("AGENT_BRIDGE_DIR", Path(__file__).resolve().parents[2] / ".agent_bridge"))
REQUESTS_DIR = BRIDGE_DIR / "gen_requests"
RESPONSES_DIR = BRIDGE_DIR / "gen_responses"
ARCHIVE_DIR = BRIDGE_DIR / "gen_archive"
TIMEOUT_SECONDS = float(os.environ.get("OPENART_BRIDGE_TIMEOUT", "3600"))
POLL_SECONDS = float(os.environ.get("OPENART_BRIDGE_POLL", "3"))


class OpenArtBridgeError(RuntimeError):
    pass


class OpenArtBridgeTimeout(OpenArtBridgeError):
    pass


def submit(payload: dict[str, Any]) -> dict[str, Any]:
    """Write a gen request, block polling for the matching response, return it.

    Raises OpenArtBridgeError/OpenArtBridgeTimeout on failure. Does NOT fall
    back to another provider -- that is a human decision, not this module's.
    """
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
