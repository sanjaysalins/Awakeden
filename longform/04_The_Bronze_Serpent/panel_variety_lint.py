"""Thin caller for the SHARED panel-variety + reuse-aspect gate
(`pipeline/panel_variety.py` — generalized from this file 2026-07-19; the full
defect-class history lives in that module's docstring + memory
`panel-variety-gate`). Kept so the documented per-episode invocation keeps
working:

Usage: python panel_variety_lint.py [--spec livingpage_full.spec.json]
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import panel_variety  # noqa: E402

POOL = HERE / "v1" / "visual_16x9_inked"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="livingpage_full.spec.json")
    ap.add_argument("--pool", default=str(POOL))
    a = ap.parse_args()
    pool = Path(a.pool)
    spec = json.loads((pool / a.spec).read_text(encoding="utf-8"))
    return panel_variety.check(pool, spec)


if __name__ == "__main__":
    sys.exit(main())
