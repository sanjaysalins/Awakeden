#!/usr/bin/env python
"""Re-roll the 2 flagged inked stills for 'Father, forgive them' (2026-07-01).

  05_pierced_hand -> TIGHT on the wounded hand only (v1 was face-dominant + a near-dup of 07).
  07_risen_hero   -> TEXT-FREE style (v1 grew a gibberish speech bubble because the locked
                     STYLE literally NAMES "NO speech bubbles" and seedream has no negative
                     channel, so naming a thing DRAWS it — memory: seedream-no-negative-channel).

Old PNGs already moved to visual/nbp/_rejected/. ~2 credits (~$0.30). Idempotent (skip if exists).
  .venv\\Scripts\\python.exe batches/cluster_01_cross/father_forgive_them/reroll_stills.py
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

# TEXT-FREE style = the locked inked STYLE with the "ABSOLUTELY NO text..." clause removed, so
# seedream is never PROMPTED with the word "speech bubbles" (which it otherwise draws as gibberish).
STYLE_NO_TEXT = ber.STYLE.split(" ABSOLUTELY NO text")[0]

JOBS = [
    # 05 — tight wounded hand only, no face. Positive end-state for the wound (never "nail").
    ("05_pierced_hand",
     "An intimate tight study filling the whole frame of one open human hand fixed against the "
     "dark grained wood of a cross beam, the palm turned open with fingers gently spread in a "
     "gesture of mercy, a single small round dark wound at the very centre of the open palm, one "
     "shaft of warm light falling across the open palm and the wood. Only the hand and wrist and "
     "the wooden beam are visible — no face, no head, no other figure. Clean, reverent, merciful.",
     ber.STYLE),
    # 07 — same hero concept, TEXT-FREE style so no speech bubble is drawn.
    ("07_risen_hero",
     f"The risen Christ standing in warm golden morning light ({CHRIST}, in clean flowing robes), "
     "alive and serene, his glorified face healed and at peace, reaching one open hand with a "
     "round healed scar in the palm gently toward the viewer in welcome, soft deep shadow behind "
     "him. The tender gospel hero image.",
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
