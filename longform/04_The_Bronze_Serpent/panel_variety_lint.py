"""Deterministic $0 guards against two defect classes found in this piece:

1. (2026-07-17) A multi-panel comic grid where 2+ panels show visually-redundant
   content (same subject/pose/framing from different files -- e.g. two near-
   identical crucifixion face close-ups side by side). A full-film eye survey
   found 9 such grids in this piece.

2. (2026-07-18) A `reuse_*` slug (a 9:16-native asset pulled from the shorts
   library, per memory `vertical-panels-cross-aspect-reuse`) used as a
   full-bleed hero panel or zoomed in beyond 1.0. That memory already said
   "full-bleed reuse stays forbidden" -- Bronze Serpent violated it in 5 hero
   beats anyway, plus 2 over-zoomed grid panels, all found by the user's own
   eye ("some clips are sharp, some are really poor... you're zooming into
   9:16"). 9:16 assets are native-res in a narrow VERTICAL grid column; a
   16:9 full-bleed or a push past 1.0 zoom stretches them past their real
   resolution and the softness becomes visible.

Reads visual_tags.json (a slug -> short category tag map, hand-assigned once
per still) and livingpage_full.spec.json.

Usage: python panel_variety_lint.py [--spec livingpage_full.spec.json]
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = HERE / "v1" / "visual_16x9_inked"
ZOOM_CEILING = 1.05


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="livingpage_full.spec.json")
    ap.add_argument("--pool", default=str(POOL))
    a = ap.parse_args()
    pool = Path(a.pool)
    spec = json.loads((pool / a.spec).read_text(encoding="utf-8"))
    tags = json.loads((pool / "visual_tags.json").read_text(encoding="utf-8"))

    fails = []
    aspect_fails = []
    untagged = set()
    motion_counter = Counter()

    for i, b in enumerate(spec["beats"], 1):
        clips = b.get("clips", [])
        n_panels = len(clips)
        if n_panels > 1:
            seen = {}
            for c in clips:
                slug = c["slug"]
                tag = tags.get(slug)
                if tag is None:
                    untagged.add(slug)
                    continue
                if tag in seen:
                    fails.append(
                        f"beat {i:2d} [{b['tpl']:10s}] panel redundancy: "
                        f"'{seen[tag]}' and '{slug}' share tag '{tag}'"
                    )
                else:
                    seen[tag] = slug
        for c in clips:
            slug = c["slug"]
            motion_counter[c.get("motion", "pushin" if "cam" not in c else c["cam"])] += 1
            if slug.startswith("reuse_"):
                if n_panels == 1:
                    aspect_fails.append(
                        f"beat {i:2d} [{b['tpl']:10s}] '{slug}' is a 9:16-native reuse asset "
                        f"used as a full-bleed hero panel -- forbidden, render a native 16:9 still instead."
                    )
                zoom = c.get("zoom", 1.0)
                if zoom > ZOOM_CEILING:
                    aspect_fails.append(
                        f"beat {i:2d} [{b['tpl']:10s}] '{slug}' zoomed to {zoom} (> {ZOOM_CEILING}) -- "
                        f"9:16 reuse assets must not be pushed past native scale, softness will show."
                    )

    print(f"[panel-variety] {len(spec['beats'])} beats scanned")
    if untagged:
        print(f"[panel-variety] UNTAGGED slugs (add to visual_tags.json before they enter a grid):")
        for s in sorted(untagged):
            print(f"    {s}")
    if fails:
        print(f"[panel-variety] {len(fails)} REDUNDANCY FAIL(s):")
        for f in fails:
            print(f"  FAIL  {f}")
    else:
        print("[panel-variety] 0 redundant grids -- every multi-panel grid shows distinct content.")
    if aspect_fails:
        print(f"[panel-variety] {len(aspect_fails)} REUSE-ASPECT FAIL(s):")
        for f in aspect_fails:
            print(f"  FAIL  {f}")
    else:
        print("[panel-variety] 0 reuse-aspect violations -- no 9:16 asset full-bleed or over-zoomed.")

    total = sum(motion_counter.values())
    if total:
        top_motion, top_n = motion_counter.most_common(1)[0]
        top_pct = round(100 * top_n / total)
        print(f"[panel-variety] motion mix: {dict(motion_counter)}  (top: {top_motion} at {top_pct}%)")
        if top_pct > 60:
            print(f"  WARN  '{top_motion}' dominates {top_pct}% of panels -- mix in other camera "
                  f"directions (hold/pull/drift) per the camera-variety standard.")

    return 1 if (fails or untagged or aspect_fails) else 0


if __name__ == "__main__":
    sys.exit(main())
