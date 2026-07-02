#!/usr/bin/env python
"""Redo 05_pierced_hand (user 2026-07-01): 'wrong cross and angle'. Old PNG DELETED.

The low-angle 'along the arm' framing produced wrong crucifixion geometry — the arm angled DOWN
and the hand was nailed to a beam that didn't line up. Fix (now rule crucifixion-arm-geometry):
lay the arm straight OUT along the horizontal crossbeam, nail the hand to THAT beam, ONE clear beam.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_05_geom.py [--render]
"""
import argparse, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

def _load(n, rel):
    s = importlib.util.spec_from_file_location(n, ROOT / rel); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

ber = _load("ber", "longform/_base_elements_refs.py")
rl = _load("rll", "render_lint/lint.py")

NBP = HERE / "visual" / "nbp"
CHRIST = ("the SAME man throughout: a dark-haired bearded man in his early thirties with a calm "
          "Near-Eastern face")
SUBJ = (
    f"A close reverent view of the crucified Christ's arm and open hand ({CHRIST}) laid straight out "
    "along the top of the single rough wooden crossbeam: the bare arm extends horizontally OUT to the "
    "side, resting flat along the beam, and the open hand at its end is nailed to that same timber by "
    "one thick plain dark iron nail with a flat square head hammered flush through the centre of the "
    "palm, dark blood running down onto the wood. The forearm leads back toward his shoulder and the "
    "edge of his robed torso at the frame edge, so the hand plainly belongs to the man on the cross. "
    "One shaft of warm light falls across the open pierced hand. The arm is outstretched along the "
    "crossbeam in the true crucifixion pose. Reverent, merciful."
)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    rl.report(SUBJ, stage="still", context="INTERCESSION 26.8-32.4s: nailed hand along the crossbeam")
    if a.render:
        dest = NBP / "05_pierced_hand.png"
        ber.lint_canonical("05_pierced_hand", SUBJ)
        print("  ->", ber.render(SUBJ + ber.STYLE + ber.ONE, dest, refs=None))
    else:
        print("[lint-only] add --render to spend ~1 cr")


if __name__ == "__main__":
    main()
