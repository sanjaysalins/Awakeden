#!/usr/bin/env python
"""Redo 05 + 06 (user 2026-07-01) — old PNGs already DELETED (redo rule: never keep/index them).

  05_pierced_hand -> the wounded hand read as a lone hand pierced to the cross. Reframe so the
                     arm clearly CONNECTS back to Christ's shoulder/torso (not a detached hand).
  06_cross_over_us -> the cross was floating (its foot dissolved into a light shaft). Plant the
                     upright FIRMLY into the rocky hilltop earth; kneeling figure on the same ground.

~2 credits (~$0.30). seedream_v4_5 inked, no-ref consistent-descriptor.
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/redo_05_06.py
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

JOBS = [
    ("05_pierced_hand",
     "A tight reverent view along the crucified Christ's OUTSTRETCHED ARM laid against the dark "
     f"grained wood of the cross beam ({CHRIST}): his bare forearm and open hand reach out along "
     "the timber, the palm turned open with a single small round dark wound at its very centre, one "
     "shaft of warm light across the open wounded palm. The arm continues unbroken back to his "
     "shoulder and the edge of his robed torso at the side of the frame, so the hand plainly belongs "
     "to the living man on the cross — a whole connected arm, never a detached hand. Reverent, merciful."),
    ("06_cross_over_us",
     "The cross seen from a low angle against a breaking storm sky, the crucified Christ high upon it "
     f"({CHRIST}, robed at the waist); the tall wooden upright of the cross runs unbroken all the way "
     "DOWN and is driven firmly into the rocky earth of the hilltop, its foot set solidly in a heap of "
     "stones and packed dust — the cross planted deep in the ground, standing solid, never floating. In "
     "the near shadowed foreground one ordinary figure kneels on that same rocky ground at the foot of "
     "the cross, seen from behind, small beneath it, a pale shaft of light falling from the sky between "
     "them. Reverent, humble, grounded."),
]


def main():
    for slug, subj in JOBS:
        dest = NBP / f"{slug}.png"
        ber.lint_canonical(slug, subj)
        status = ber.render(subj + ber.STYLE + ber.ONE, dest, refs=None)
        print(f"  -> {slug}: {status}")


if __name__ == "__main__":
    main()
