"""pipeline/art_style.py — detect whether a piece was rendered in the LEGACY
Baroque oil-painting look or the current graphic-novel/inked standard.

🔒 HARDENED (user, 2026-07-15, memory `graphic-novel-style-migration`):
"everything from the oil-painting era is LEGACY and will NEVER BE UPLOADED...
don't count legacy finals as upload-ready on any board or plan." No per-piece
style field is persisted anywhere today, so this is the deterministic stopgap
signal the memory calls for.

Two passes:
1. Classify the LANE the piece actually SHIPS from (`pipeline.finality.
   final_video`), not just directory presence. A `*_inked` directory is the
   graphic-novel rebuild pool by established project convention (see
   `longform/_add_score_lf.py`'s own "inked-rebuild pool wins when present"
   precedence) — this alone correctly classifies livingpage-format rebuilds
   (per-still PNGs + audits, no `scene_plan.json`) that pass #2's text-scan
   right by, e.g. Isaiah 53.
2. Text-scan fallback over whatever artifacts exist (`scene_plan.json`
   style_base, the self-review `_panel_scene_plan.md`, a batches-format
   `piece.json`'s still-job prompts) for an explicit style marker.

Fail-SAFE, not fail-closed: only a POSITIVE "baroque" text match blocks a
piece. Anything the scanner can't read returns "unknown" and is left alone —
retroactively failing every already-shipped piece this heuristic doesn't
recognise would be its own regression. Tighten this (persist a real
`art_style` field at render time; treat "unknown" as baroque) as a follow-up
once the whole catalogue has been swept and confirmed clean under the loose
version.
"""
from __future__ import annotations

import json
from pathlib import Path

BAROQUE = "baroque"
GRAPHIC_NOVEL = "graphic_novel"
UNKNOWN = "unknown"

# Baroque markers first: a piece can mention "graphic novel" in passing notes
# while still being a Baroque render, but never the reverse in this corpus —
# so Baroque wins ties. Checked BEFORE that: an explicitly NEGATED Baroque
# mention ("STYLE = inked graphic-novel (NOT Baroque oil)" — the migration's
# own doc-comment phrasing in rebuilt pieces) must not trip the Baroque
# marker at all; a naive substring scan misreads the negation as a hit.
_BAROQUE_MARKERS = ("baroque oil", "baroque-oil", "oil-painting era", "old-master oil")
_GN_MARKERS = ("graphic-novel", "graphic novel", "inked biblical")
_BAROQUE_NEGATION_MARKERS = ("not baroque", "no longer baroque", "never baroque")


def _classify(text: str) -> str | None:
    t = text.lower()
    if any(m in t for m in _BAROQUE_NEGATION_MARKERS):
        return GRAPHIC_NOVEL
    if any(m in t for m in _BAROQUE_MARKERS):
        return BAROQUE
    if any(m in t for m in _GN_MARKERS):
        return GRAPHIC_NOVEL
    return None


def _classify_json_file(p: Path) -> str | None:
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return _classify(json.dumps(data))


def detect_art_style(piece_dir: Path | str) -> str:
    """Best-effort art-style classification for one piece folder."""
    d = Path(piece_dir)

    # Pass 1: the lane the piece actually ships from. A directory literally
    # named *_inked, or a final whose filename carries the `LivingPage_`
    # prefix (the project's naming convention for a migrated long-form
    # rebuild — see Isaiah 53 and Psalm 22, both `LivingPage_<Title>_16x9...`
    # sitting in a plain, non-"_inked" visual_16x9/ alongside a STALE
    # pre-migration scene_plan.json), is the graphic-novel pool — no
    # text-scan needed. This is what makes livingpage-format rebuilds
    # classify correctly instead of falling through to that stale sibling.
    try:
        from pipeline import finality
        _status, video = finality.final_video(d)
    except Exception:
        video = None
    if video is not None:
        if "inked" in video.parent.name.lower() or video.name.lower().startswith("livingpage"):
            return GRAPHIC_NOVEL

    # Pass 2: text-scan whatever artifacts exist, preferring the shipping
    # lane's own directory when known.
    search_dirs: list[Path] = []
    if video is not None and video.parent not in search_dirs:
        search_dirs.append(video.parent)
    for sub in ("visual_16x9_inked", "visual_16x9", "visual"):
        p = d / sub
        if p.is_dir() and p not in search_dirs:
            search_dirs.append(p)
    # Archived-visual pieces (2026-07-16 Baroque-episode archival) keep a
    # preserved scene_plan.json copy at the piece root once visual_16x9/ is
    # moved to archive/ — scan the root too so those still classify.
    if d not in search_dirs:
        search_dirs.append(d)

    for sd in search_dirs:
        hit = _classify_json_file(sd / "scene_plan.json")
        if hit:
            return hit

    panel = d / "_panel_scene_plan.md"
    if panel.is_file():
        hit = _classify(panel.read_text(encoding="utf-8", errors="ignore"))
        if hit:
            return hit

    hit = _classify_json_file(d / "piece.json")
    if hit:
        return hit

    return UNKNOWN
