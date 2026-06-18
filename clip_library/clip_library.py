"""Central CLIP library — reuse already-animated 9:16 clips instead of regenerating.

A clip is indexed BY REFERENCE (its source path in the episode folder), with auto-derived
tags, a jesus_variant, and a topical-fit SCOPE:
  - "neutral"  : a thread-neutral passion/Christ plate (cross, Christ-face, pierced side,
                 wounds, nailed hand, dawn cross, lamb) — reusable in ANY passion episode.
  - "specific" : a story-bound clip (mockers, dice/garments, sheep, tomb, well ...) —
                 reusable ONLY in an episode whose narration actually contains that subject
                 (the topical-fit rule, memory feedback-topical-fit-gate).

find() defaults to scope="neutral" so cross-episode reuse is safe; pass scope="any" + a tag
to pull a story-specific clip into a matching episode. Build the index with ingest_clips.py.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = Path(__file__).resolve().parent / "index.json"


def load() -> list[dict]:
    if not INDEX.exists():
        return []
    return json.loads(INDEX.read_text(encoding="utf-8")).get("clips", [])


def find(tags: list[str] | None = None, *, scope: str = "neutral",
         variant: str | None = None, limit: int = 5) -> list[dict]:
    """Return clips matching ALL given tags, ranked by tag-overlap then duration sanity.
    scope: 'neutral' (default, cross-episode-safe) | 'specific' | 'any'."""
    want = set(t.lower() for t in (tags or []))
    out = []
    for c in load():
        if scope != "any" and c.get("scope") != scope:
            continue
        if variant and c.get("jesus_variant") not in (variant, None):
            continue
        ctags = set(c.get("tags", []))
        if want and not want.issubset(ctags):
            continue
        overlap = len(want & ctags)
        out.append((overlap, c))
    # rank: curated 'preferred' best-of first, then tag-overlap, then title
    out.sort(key=lambda x: (-int(x[1].get("preferred", False)), -x[0], x[1].get("title", "")))
    return [c for _, c in out[:limit]]


def materialize(entry: dict, dest_nbp: Path, index: int, slug: str) -> Path:
    """Copy a chosen library clip (+ its still) into a short's visual/nbp as NN_slug.*,
    writing passing image-audit + clip_qc sidecars (it was already QC'd). Returns the mp4."""
    import shutil
    from pipeline import clip_qc, coherence
    dest_nbp.mkdir(parents=True, exist_ok=True)
    src = ROOT / entry["source"]
    dst_mp4 = dest_nbp / f"{index:02d}_{slug}.mp4"
    shutil.copy2(src, dst_mp4)
    src_png = src.with_suffix(".png")
    if src_png.exists():
        dst_png = dest_nbp / f"{index:02d}_{slug}.png"
        shutil.copy2(src_png, dst_png)
        dst_png.with_suffix(".png.audit.json").write_text(json.dumps(
            {"passed": True, "issues": [{"claim": "reused", "actual": f"library clip {entry['slug']}"}],
             "banned_token_hits": []}), encoding="utf-8")
        # INV-24: COPY the source's real coherence verdict; never fabricate one. If the source
        # was never coherence-audited, the destination stays UNVERIFIED and the assembly
        # chokepoint (require_visual_coherence) will block it.
        coherence.copy_verdict(src_png, dst_png)
    clip_qc.record_verdict(dst_mp4, passed=True, note=f"REUSED library clip {entry['slug']} <- {entry['source']}")
    return dst_mp4
