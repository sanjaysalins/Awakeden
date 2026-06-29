r"""bible_gate.py — fail-closed Bible-check chokepoint for the pipeline.

Other stages call this BEFORE spending: animation must not render a still that
contradicts Scripture, and a piece must not LOCK without a green bible-check.

Exit 0  = GREEN (the check ran and passed for the rendered scenes).
Exit 3  = NOT GREEN (prints the reasons).
Exit 2  = usage error.

Usage (PowerShell):
  .venv\Scripts\python.exe bible_gate.py "<v1 folder>" --stage animate
  .venv\Scripts\python.exe bible_gate.py "<v1 folder>" --stage lock

Going-forward only: callers may set BIBLE_GATE=off (or pass --warn) to downgrade
to a warning for grandfathered back-catalogue pieces.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from pipeline import bible_kb


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("vfolder", help="episode v1 folder")
    ap.add_argument("--stage", default="lock", help="animate | lock (label only)")
    ap.add_argument("--warn", action="store_true",
                    help="downgrade a non-green result to a warning (grandfathered pieces)")
    ap.add_argument("--all-scenes", action="store_true",
                    help="require every planned scene (not only rendered) to be covered")
    args = ap.parse_args()

    v1 = Path(args.vfolder)
    if not v1.is_dir():
        print(f"[bible-gate] not a folder: {v1}", file=sys.stderr)
        return 2
    if args.warn:
        os.environ["BIBLE_GATE"] = "warn"

    try:
        st = bible_kb.gate(v1, stage=args.stage, rendered_only=not args.all_scenes)
    except RuntimeError as e:
        print(f"[bible-gate] *** NOT GREEN [{args.stage}] {v1} ***")
        print(str(e))
        print(f"   status -> {v1 / '_bible_check' / 'bible_check.status.json'}")
        return 3
    if st is None or st.ok:
        print(f"[bible-gate] OK [{args.stage}] {v1}.")
        return 0
    return 0  # warn mode: not green but downgraded


if __name__ == "__main__":
    sys.exit(main())
