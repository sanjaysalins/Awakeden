"""Shared panel-variety + reuse-aspect lint for comic-grid pieces (any pool).

Generalized 2026-07-19 from `longform/04_The_Bronze_Serpent/panel_variety_lint.py`
(which stays as a thin caller) so the gate is one implementation, callable from
any episode AND wired into the livingpage build itself instead of relying on
someone remembering to run a per-episode script (memory `panel-variety-gate`:
it caught 6 of 9 real grid collisions when introduced — but only when run).

Two defect classes:
1. Panel redundancy — 2+ panels in one multi-panel grid sharing a
   `visual_tags.json` category tag (same subject/pose/framing twice).
2. Reuse-aspect — a `reuse_*` 9:16-native asset used full-bleed or zoomed
   past 1.05x (stretches past native resolution, softness shows).

GRANDFATHERING: a pool with no `visual_tags.json` skips the gate entirely
(WARN) — legacy pieces (father_forgive_them, Psalm 22) predate the tagging
discipline and must keep rebuilding; a NEW comic-grid piece should create
`visual_tags.json` with its first multi-panel grid. Once the file exists,
untagged slugs in grids are BLOCKING (tag before it enters a grid).

The deterministic tag check is a FLOOR, not the ceiling — 3 of the 9 original
collisions needed a human eye on the composited frame (see `panel-variety-gate`
memory). This gate never replaces that look.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ZOOM_CEILING = 1.05


def lint(pool: Path, spec: dict) -> dict:
    """Pure check. Returns {'skipped': bool, 'fails': [...], 'aspect_fails': [...],
    'untagged': [...], 'motion': Counter}. `skipped` means no visual_tags.json
    (grandfathered pool) — nothing else is populated in that case."""
    tags_path = pool / "visual_tags.json"
    if not tags_path.is_file():
        return {"skipped": True, "fails": [], "aspect_fails": [], "untagged": [],
                "motion": Counter()}
    tags = json.loads(tags_path.read_text(encoding="utf-8"))

    fails: list[str] = []
    aspect_fails: list[str] = []
    untagged: set[str] = set()
    motion: Counter = Counter()

    for i, b in enumerate(spec["beats"], 1):
        clips = b.get("clips", [])
        n_panels = len(clips)
        if n_panels > 1:
            seen: dict[str, str] = {}
            for c in clips:
                slug = c["slug"]
                tag = tags.get(slug)
                if tag is None:
                    untagged.add(slug)
                    continue
                if tag in seen:
                    fails.append(f"beat {i:2d} [{b['tpl']:10s}] panel redundancy: "
                                 f"'{seen[tag]}' and '{slug}' share tag '{tag}'")
                else:
                    seen[tag] = slug
        for c in clips:
            slug = c["slug"]
            motion[c.get("motion", "pushin" if "cam" not in c else c["cam"])] += 1
            if slug.startswith("reuse_"):
                if n_panels == 1:
                    aspect_fails.append(
                        f"beat {i:2d} [{b['tpl']:10s}] '{slug}' is a 9:16-native reuse asset "
                        f"used as a full-bleed hero panel -- forbidden, render a native 16:9 still instead.")
                zoom = c.get("zoom", 1.0)
                if zoom > ZOOM_CEILING:
                    aspect_fails.append(
                        f"beat {i:2d} [{b['tpl']:10s}] '{slug}' zoomed to {zoom} (> {ZOOM_CEILING}) -- "
                        f"9:16 reuse assets must not be pushed past native scale, softness will show.")

    return {"skipped": False, "fails": fails, "aspect_fails": aspect_fails,
            "untagged": sorted(untagged), "motion": motion}


def check(pool: Path, spec: dict, *, log=print) -> int:
    """Print a report; return 0 clean / 1 violations / 0 with a WARN when the
    pool is grandfathered (no visual_tags.json)."""
    r = lint(pool, spec)
    if r["skipped"]:
        log(f"[panel-variety] no visual_tags.json in {pool.name} — grandfathered legacy "
            f"pool, gate SKIPPED (new comic-grid pieces should tag their stills)")
        return 0
    log(f"[panel-variety] {len(spec['beats'])} beats scanned")
    if r["untagged"]:
        log("[panel-variety] UNTAGGED slugs (add to visual_tags.json before they enter a grid):")
        for s in r["untagged"]:
            log(f"    {s}")
    if r["fails"]:
        log(f"[panel-variety] {len(r['fails'])} REDUNDANCY FAIL(s):")
        for f in r["fails"]:
            log(f"  FAIL  {f}")
    else:
        log("[panel-variety] 0 redundant grids -- every multi-panel grid shows distinct content.")
    if r["aspect_fails"]:
        log(f"[panel-variety] {len(r['aspect_fails'])} REUSE-ASPECT FAIL(s):")
        for f in r["aspect_fails"]:
            log(f"  FAIL  {f}")
    else:
        log("[panel-variety] 0 reuse-aspect violations -- no 9:16 asset full-bleed or over-zoomed.")

    total = sum(r["motion"].values())
    if total:
        top_motion, top_n = r["motion"].most_common(1)[0]
        top_pct = round(100 * top_n / total)
        log(f"[panel-variety] motion mix: {dict(r['motion'])}  (top: {top_motion} at {top_pct}%)")
        if top_pct > 60:
            log(f"  WARN  '{top_motion}' dominates {top_pct}% of panels -- mix in other camera "
                f"directions (hold/pull/drift) per the camera-variety standard.")

    return 1 if (r["fails"] or r["untagged"] or r["aspect_fails"]) else 0
