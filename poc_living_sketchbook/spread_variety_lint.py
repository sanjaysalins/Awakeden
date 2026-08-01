"""Thin caller for the SHARED spread-variety gate (`pipeline/spread_variety.py`
-- adapted 2026-07-31 from `panel_variety.py`'s tagging philosophy for linear
living-sketchbook spread sequences instead of comic-grid panels). Kept at the
repo level (not episode-local) so any living-sketchbook episode can call it
the same way -- same shape as `longform/04_The_Bronze_Serpent/
panel_variety_lint.py`'s thin-caller pattern.

Usage:
    python spread_variety_lint.py <episode_dir> [--slugs s01_wide,s02_grief,...]

If --slugs is omitted, the spread order is read from the episode's own
visual_tags.json insertion order (Python dicts preserve insertion order,
and this repo's tags files are always authored in page order), so a caller
doesn't have to duplicate the spread list.

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode_dir")
    ap.add_argument("--slugs", default=None,
                     help="comma-separated spread slugs in page order; "
                          "defaults to visual_tags.json's own key order")
    a = ap.parse_args()
    pool = Path(a.episode_dir)
    if a.slugs:
        slugs = a.slugs.split(",")
    else:
        tags_path = pool / "visual_tags.json"
        if not tags_path.is_file():
            print(f"[spread-variety] no visual_tags.json in {pool} -- pass --slugs "
                  f"explicitly or tag the pool first")
            return 0
        slugs = list(json.loads(tags_path.read_text(encoding="utf-8")).keys())
    return spread_variety.check(pool, slugs)


if __name__ == "__main__":
    sys.exit(main())
