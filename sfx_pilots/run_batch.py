"""Build SFX/ambience-enhanced versions of the finished shorts (Level A, no music, $0).

  python sfx_pilots/run_batch.py --plan          # show all maps (free)
  python sfx_pilots/run_batch.py                 # build all -> sfx_pilots/out/<safe>_sfx.mp4
  python sfx_pilots/run_batch.py 16 35           # build only the named episodes
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sfxlib
from plans import PLANS, NARR

OUT = HERE / "out"


def main():
    args = [a for a in sys.argv[1:] if a != "--plan"]
    plan_only = "--plan" in sys.argv
    OUT.mkdir(exist_ok=True)

    for name, (dur, layers) in PLANS.items():
        if args and not any(a in name for a in args):
            continue
        safe = name.replace(" ", "_")
        sfxlib.show_plan(name, layers)
        if plan_only:
            continue
        src = Path(NARR) / name / "v1" / "assembly" / "viral_cut.mp4"
        out = OUT / f"{safe}_sfx.mp4"
        sfxlib.build(src, out, layers)
        print(f"[ok] {out}")
        sfxlib.measure(out)


if __name__ == "__main__":
    main()
