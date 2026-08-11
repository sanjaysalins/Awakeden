"""Shared vision-call adapter for the drawing_office guard modules.

Reuses `pipeline.visual_render`'s image-encoding helpers
(`_encode_image_for_vision`, which itself calls `_detect_media_type`) and
`pipeline.engine`'s JSON extraction + client, and mirrors
`pipeline.visual_render._vision_call`'s agent-mode-vs-metered-API branching
EXACTLY -- WITHOUT depending on the `Scene` dataclass that `_vision_call` is
tightly coupled to (it builds its prompt from `scene.subject_block`,
`scene.vignettes`, etc., which none of these guards have). This is a minimal
local adapter, not a reimplementation of the vision-call plumbing itself.

Not a public module of its own — imported only by the sibling guard modules
in this folder (drift_check.py, text_check.py, fact_check.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # drawing_office/guards -> JesusInTheBible
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import config
from pipeline import engine as text_engine
from pipeline.visual_render import _encode_image_for_vision


def vision_call(role: str, user_text: str, png_bytes: bytes, label: str) -> dict:
    """One vision call, agent-mode (file bridge, $0) or metered API depending
    on `config.agent_mode()` — same branch pipeline.visual_render._vision_call
    uses. Returns the parsed JSON reply. Raises on any failure; callers are
    responsible for failing closed (never silently pass on an error)."""
    b64, media = _encode_image_for_vision(png_bytes)

    if config.agent_mode():
        from pipeline import agent_bridge
        text = agent_bridge.call_vision(
            role=role, user=user_text, image_bytes=png_bytes, media=media,
            model=config.MODEL, label=label,
        )
        return text_engine._extract_json(text)

    client = text_engine._client()
    resp = client.messages.create(
        model=config.MODEL,
        max_tokens=1500,
        thinking={"type": "adaptive"},
        system=role,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
                {"type": "text", "text": user_text},
            ],
        }],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    return text_engine._extract_json(text)
