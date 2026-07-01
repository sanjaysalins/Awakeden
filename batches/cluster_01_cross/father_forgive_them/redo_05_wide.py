#!/usr/bin/env python
"""Redo 05_pierced_hand (user 2026-07-01, chose 'pull back to a clear pose'). Old PNG DELETED.

Close nailed-hand framing kept fighting the crucifixion geometry. Fix = pull back to a medium
waist-up view so the WHOLE cross is visible: both arms out along the crossbeam, hands nailed to
that beam, warm light drawing the eye to the nearer pierced hand. Geometry unambiguous.

  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_05_wide.py [--render]
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
    f"A reverent medium view of the crucified Christ from the waist up ({CHRIST}, robed at the "
    "waist), seen straight on in the classic crucifixion pose: he has exactly two arms, extended "
    "straight out to the left and to the right along the horizontal wooden crossbeam, and each open "
    "palm is nailed to that beam by a single old dark iron nail whose plain rounded head sits flush "
    "against the skin, dark blood around each wound running down the forearms. His head is lifted, his "
    "face calm. A dark storm sky behind him "
    "with one shaft of warm light. Exactly two arms and two hands, one nail through each hand, palms "
    "facing forward. Reverent, merciful."
)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    rl.report(SUBJ, stage="still", context="INTERCESSION 26.8-32.4s: nailed hands out along the crossbeam (waist-up)")
    if a.render:
        dest = NBP / "05_pierced_hand.png"
        ber.lint_canonical("05_pierced_hand", SUBJ)
        print("  ->", ber.render(SUBJ + ber.STYLE + ber.ONE, dest, refs=None))
    else:
        print("[lint-only] add --render to spend ~1 cr")


if __name__ == "__main__":
    main()
