#!/usr/bin/env python
"""User's clip-review punch-list (2026-08-05, 6 spreads flagged) -- every one
of these is the SAME failure class already proven twice this episode (s05,
s07, s25, s53): a generative animator invents motion/content a frozen-tableau
still must not have. $0 deterministic camera move via panel_animator/
dynamic_cam3d.py instead of a re-prompt -- nothing is regenerated, so nothing
can be invented. Stills themselves are untouched and fine; only the clips
were bad.

User's notes, verbatim, and what they map to on frame-by-frame inspection
(_review_frames/*_contact.png, 32-frame contact sheets):
  s26_through_veil_stage2 -- "the curtain[']s the angle is flapping his
      wings" -- the veil's woven cherub (Exodus 26:31) animates its wings
      as a living figure. Same defect as s05/s45.
  s27_sprinkling -- "there is some ghost like figure imerging and loads of
      blood flowing from this hands" -- confirmed: the glory-cloud behind
      the ark morphs into a humanoid figure over the clip, blood escalates
      from Lev 16:14's single controlled drop into a large pool/streak, and
      the ark's gold cherubim spread their wings further than the still.
      Highest doctrinal stakes after s63.
  s34_riddle_recap -- "some abnormal page turn animation" -- confirmed: the
      left vignette card is animated as a physical page being lifted/turned
      in the priest's hand, then a whole open book appears -- invented
      content with no basis in the still at all.
  s45_sign_before_veil -- "the curtain wings are flapping" -- same defect
      class as s26 (this spread has 3 woven cherub figures across the veil).
  s50_the_shadow -- "some weird birds fly in the middle" -- confirmed: small
      bird silhouettes invented over the desert dunes, not in the still.
  s63_torn_veil_card -- "when the curtain tear, some naked woman in wings
      come out" -- confirmed, SEVERE: the two woven cherub heads (a static
      close-up of the veil's own embroidery, per s45) are animated into two
      fully-realised nude winged humanoid figures holding hands, rendered in
      an unrelated anime style -- a total style/content break. Do not retry
      generatively on this one under any circumstances.

Run (sequential, gentle, $0):
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s_fix_batch2_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"

# (name, move, duration, focus, amp) -- focus eye-checked per still
SPREADS = [
    # Aaron's face, away from the veil's cherub on the left -- gentle push.
    ("s26_through_veil_stage2", "push", 4.0, (0.62, 0.28), 0.6),
    # Push toward Aaron + the sprinkling hand/bowl, away from the ark
    # cherubim and glory-cloud that were inventing a figure.
    ("s27_sprinkling", "push", 4.0, (0.60, 0.60), 0.7),
    # Calm portrait push on the priest's face -- no pretense of a "page."
    ("s34_riddle_recap", "push", 4.0, (0.68, 0.45), 0.5),
    # Whole-veil push toward the small witnessing priest figure at the
    # bottom -- all 3 cherub figures stay motionless regardless of focus.
    ("s45_sign_before_veil", "push", 4.0, (0.50, 0.55), 0.6),
    # Wide desert landscape -- slow arc drift along the shadow's line.
    ("s50_the_shadow", "arc", 4.0, (0.55, 0.55), 0.6),
    # Reverent push into the light between the two cherub heads -- the
    # veil-torn beat (Matt 27:51), restrained on purpose.
    ("s63_torn_veil_card", "push", 4.0, (0.50, 0.42), 0.6),
]

if __name__ == "__main__":
    for name, move, dur, focus, amp in SPREADS:
        still = STILLS / f"{name}.png"
        dest = CLIPS / f"{name}.mp4"
        if not still.exists():
            print(f"[HOLD] {name}: still missing")
            continue
        out = render_move(still, move, dur, focus, dest, amp=amp)
        print(f"[ok] {name} ({move}) -> {out}")
