#!/usr/bin/env python
"""Redo 05 + 07 (user 2026-07-01, round 2) — old PNGs DELETED (redo rule: never keep/index them).

  05_pierced_hand -> no visible nail; Jesus reads as reaching, not crucified. Show a rough forged
                     IRON SPIKE driven through the open hand, pinning it to the beam (open, not a fist).
  07_risen_hero   -> the healed scar rendered as a big BURNT brand. Make it a small, neat, flat,
                     pale healed round scar — subtle, not a burn, not a hole.

NOTE: "spike/nail" trips the poison linter (draws a decorative stud) — intentional here; described
as a rough forged iron spike pinning the hand + blood at entry to push it to a real crucifixion nail.
07 uses the TEXT-FREE style variant (avoids the speech-bubble regression). ~2 cr (~$0.30).
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_05_07.py
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("ber", ROOT / "longform" / "_base_elements_refs.py")
ber = importlib.util.module_from_spec(spec); spec.loader.exec_module(ber)

NBP = HERE / "visual" / "nbp"
CHRIST = ("the SAME man throughout: a dark-haired bearded man in his early thirties with a calm "
          "Near-Eastern face")
STYLE_NO_TEXT = ber.STYLE.split(" ABSOLUTELY NO text")[0]

JOBS = [
    ("05_pierced_hand",
     "A tight low-angle view along the crucified Christ's outstretched arm laid against the dark "
     f"grained wood of the cross beam ({CHRIST}): the hand is open with the fingers relaxed, and a "
     "single large rough forged-iron spike is driven straight down through the very centre of the "
     "open hand, pinning it firmly to the wooden beam, dark blood beading where the black iron enters "
     "the flesh. The bare forearm continues unbroken up to His shoulder and robed torso at the edge of "
     "the frame, so the nailed hand plainly belongs to the living man on the cross. One shaft of warm "
     "light falls across the pierced open hand. Reverent, merciful — an open hand, not a clenched fist.",
     ber.STYLE),
    ("07_risen_hero",
     f"The risen Christ standing in warm golden morning light ({CHRIST}, in clean flowing robes), alive "
     "and serene, his glorified face healed and at peace, reaching one open hand gently toward the "
     "viewer in welcome; at the very centre of the open palm there is one small, neat, pale round healed "
     "scar, flat and closed over and level with the skin, subtle and clean. Soft deep shadow behind him. "
     "The tender gospel hero image.",
     STYLE_NO_TEXT),
]


def main():
    for slug, subj, style in JOBS:
        dest = NBP / f"{slug}.png"
        ber.lint_canonical(slug, subj)
        status = ber.render(subj + style + ber.ONE, dest, refs=None)
        print(f"  -> {slug}: {status}")


if __name__ == "__main__":
    main()
