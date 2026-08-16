"""Thin caller for the SHARED spread-variety gates (`pipeline/spread_variety.py`
-- adapted 2026-07-31 from `panel_variety.py`'s tagging philosophy for linear
living-sketchbook spread sequences instead of comic-grid panels). Kept at the
repo level (not episode-local) so any living-sketchbook episode can call it
the same way -- same shape as `longform/04_The_Bronze_Serpent/
panel_variety_lint.py`'s thin-caller pattern.

Runs BOTH checks in one invocation:
  1. `lint()`/`check()` -- exact subject+pose+framing collision between any
     two spreads (the original 2026-07-31 gate).
  2. `census()`/`check_census()` -- WARNs (non-blocking) when one object/prop
     anchors more than `--threshold` spreads, added 2026-08-16 after
     Serpent-Crusher Promised shipped 4 zero-collision serpent framings that
     still read as "loads of feet and snake stills" on real playback --
     see memory `living-sketchbook-subject-variety-gap`.

Usage:
    python spread_variety_lint.py <episode_dir> [--slugs s01_wide,s02_grief,...] [--threshold 2]

If --slugs is omitted, the spread order is read from the episode's own
visual_tags.json insertion order (Python dicts preserve insertion order,
and this repo's tags files are always authored in page order), so a caller
doesn't have to duplicate the spread list. Author `visual_tags.json` at
PLANNING time, from the `_PLAN.md` spread table's own content descriptions
-- this is a textual judgment call, not derived from pixels, so it costs $0
and can run before the first still is ever rendered.

Example (Bronze Serpent):
    .venv\\Scripts\\python.exe poc_living_sketchbook/spread_variety_lint.py ^
        poc_living_sketchbook/bronze_serpent
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from pipeline import spread_variety  # noqa: E402


def _slugs_from_tags(pool: Path) -> list[str] | None:
    tags_path = pool / "visual_tags.json"
    if not tags_path.is_file():
        return None
    keys = json.loads(tags_path.read_text(encoding="utf-8")).keys()
    return [k for k in keys if not k.startswith("_")]  # skip _mandated, etc.


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode_dir")
    ap.add_argument("--slugs", default=None,
                     help="comma-separated spread slugs in page order; "
                          "defaults to visual_tags.json's own key order")
    ap.add_argument("--threshold", type=int, default=spread_variety.DEFAULT_OBJECT_THRESHOLD,
                     help="max spreads an object may center in before the census WARNs (default 2)")
    a = ap.parse_args()
    pool = Path(a.episode_dir)
    if a.slugs:
        slugs = a.slugs.split(",")
    else:
        slugs = _slugs_from_tags(pool)
        if slugs is None:
            print(f"[spread-variety] no visual_tags.json in {pool} -- pass --slugs "
                  f"explicitly or tag the pool first")
            return 0

    composition_result = spread_variety.check(pool, slugs)
    print()
    census_result = spread_variety.check_census(pool, slugs, threshold=a.threshold)
    return 1 if (composition_result or census_result) else 0


if __name__ == "__main__":
    sys.exit(main())
