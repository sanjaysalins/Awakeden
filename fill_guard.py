"""Fail-closed guard for FILL (owner rule, 2026-11-21).

The owner forbids filling a slot that is longer than its clip by reversing / boomeranging /
ping-ponging / freezing / slow-motion-stretching (> 1.15x) the clip, or by a Ken Burns push on a
still. Each clip must be >= its slot; trim only.

Every builder that can fill calls one of the checks below BEFORE it fills. The default is to raise
`ClipShorterThanSlot`. The old behaviour stays reachable ONLY through an explicit, loudly named
opt-in, so an already-locked film can still be re-rendered byte-identically:

    allow_fill=True              (argument, where a helper takes it)
    ALLOW_FILL_OWNER_OK=1        (environment)

Do not set either for new work.
"""
from __future__ import annotations

import os

MAX_STRETCH = 1.15      # slow-motion stretch above this counts as fill
SLOT_TOL = 0.05         # seconds of slack before a clip counts as shorter than its slot
ENV_FLAG = "ALLOW_FILL_OWNER_OK"


class ClipShorterThanSlot(RuntimeError):
    """A clip is shorter than its slot and the builder would have to fill it."""


def fill_allowed(allow_fill: bool | None = None) -> bool:
    if allow_fill is not None:
        return bool(allow_fill)
    return os.environ.get(ENV_FLAG, "").strip() == "1"


def _msg(slot_name, clip_len, slot_len, what):
    return (f"clip shorter than slot: {what} - slot '{slot_name}' needs {slot_len:.2f}s but the clip is "
            f"{clip_len:.2f}s. Re-time trim-only or render a longer clip. (Fill is forbidden; the "
            f"locked-film re-render opt-in is allow_fill=True or {ENV_FLAG}=1.)")


def require_clip_covers_slot(slot_name: str, clip_len: float, slot_len: float,
                             allow_fill: bool | None = None, what: str = "no fill allowed") -> None:
    """Raise unless clip_len >= slot_len (within SLOT_TOL) or fill is explicitly allowed."""
    if clip_len + SLOT_TOL >= slot_len or fill_allowed(allow_fill):
        return
    raise ClipShorterThanSlot(_msg(slot_name, clip_len, slot_len, what))


def require_stretch_ok(slot_name: str, clip_len: float, slot_len: float,
                       allow_fill: bool | None = None, max_stretch: float = MAX_STRETCH) -> None:
    """Slow-motion stretch (slot/clip) above max_stretch counts as fill; a clip that is longer than
    its slot is fine (trim)."""
    if clip_len <= 0:
        raise ClipShorterThanSlot(_msg(slot_name, clip_len, slot_len, "empty clip"))
    if slot_len / clip_len <= max_stretch or fill_allowed(allow_fill):
        return
    raise ClipShorterThanSlot(_msg(slot_name, clip_len, slot_len,
                                   f"would need a {slot_len / clip_len:.2f}x slow-motion stretch (> {max_stretch}x)"))


def forbid_still_kenburns(slot_name: str, allow_fill: bool | None = None) -> None:
    """A still with no animated clip would be given a Ken Burns push: forbidden."""
    if fill_allowed(allow_fill):
        return
    raise ClipShorterThanSlot(
        f"no animated clip for slot '{slot_name}': a Ken Burns push on a still is forbidden. Render a real "
        f"clip. (Locked-film re-render opt-in: allow_fill=True or {ENV_FLAG}=1.)")


def require_fill_opt_in(what: str) -> None:
    """For helpers that cannot see slot/clip lengths (frame-index loops): raise unless opted in."""
    if fill_allowed(None):
        return
    raise ClipShorterThanSlot(
        f"clip shorter than slot: {what}. Re-time trim-only or render a longer clip. (Fill is forbidden; "
        f"locked-film re-render opt-in: {ENV_FLAG}=1.)")
