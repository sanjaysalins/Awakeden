#!/usr/bin/env python
"""Panel 05 FINAL — apply the two proven learnings (probe #1 wound recipe + probe #2 close-framing
sweet spot) to finally solve the panel that kept failing. Old PNG DELETED. ~1 cr.

Recipe: CLOSE shot (not macro, not a fiddly nail detail) of the face + one outstretched arm, the
open hand showing a WOUND (never the word 'nail'). This exact framing rendered cleanly in probe #2.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_05_final.py [--render]
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
    f"A CLOSE shot of the crucified Christ's face and one outstretched arm ({CHRIST}): his head is "
    "lifted toward heaven, and his open hand at the wooden crossbeam shows a dark ragged pierced hole "
    "in the centre of the palm with dark red blood running down toward the wrist. A dark storm sky "
    "behind, one shaft of warm light across his face and the wounded open hand. Reverent, merciful."
)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    rl.report(SUBJ, stage="still", context="INTERCESSION 26.8-32.4s: close face + wounded open hand (sweet spot + wound recipe)")
    if a.render:
        dest = NBP / "05_pierced_hand.png"
        ber.lint_canonical("05_pierced_hand", SUBJ)
        print("  ->", ber.render(SUBJ + ber.STYLE + ber.ONE, dest, refs=None))
    else:
        print("[lint-only] add --render to spend ~1 cr")


if __name__ == "__main__":
    main()
