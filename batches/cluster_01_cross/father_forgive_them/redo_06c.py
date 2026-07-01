#!/usr/bin/env python
"""Panel 06c FINAL — living Christ interceding. Old PNG DELETED. Applies the learnings: ONE dominant
lifted scarred hand (the two-hands-both-scars case is unreliable), healed-scar wording (no 'nail',
no 'puckered', one centre-palm scar), TEXT-FREE style. ~1 cr.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_06c.py [--render]
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
STYLE_NO_TEXT = ber.STYLE.split(" ABSOLUTELY NO text")[0]
SUBJ = (
    f"A close reverent view of the living risen Christ ({CHRIST}, in clean flowing white robes) "
    "standing in warm golden light, calm and at peace; he lifts ONE open hand toward the viewer in "
    "intercession, and at the very centre of that open palm is one single round healed scar — a small "
    "patch of smooth, closed, pale skin, flat and level. His other hand rests low at his side. Soft "
    "deep shadow behind him. Reverent, alive."
)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    rl.report(SUBJ, stage="still", context="CONVICTION 39.4-42.8s: living Christ interceding, one lifted scarred hand")
    if a.render:
        dest = NBP / "06c_intercession_lives.png"
        ber.lint_canonical("06c_intercession_lives", SUBJ)
        print("  ->", ber.render(SUBJ + STYLE_NO_TEXT + ber.ONE, dest, refs=None))
    else:
        print("[lint-only] add --render to spend ~1 cr")


if __name__ == "__main__":
    main()
