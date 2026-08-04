#!/usr/bin/env python
"""The 6 remaining Christ-iconography spreads (excluded from _s4_animate.py's
JOBS after s53's failure -- see that file's comments) -- $0 deterministic
camera moves via panel_animator/dynamic_cam3d.py instead of a generative
attempt. s53's prompt already had explicit "robe holds its exact folds"
language and still animated the robe; prompt-tightening is not trusted for
Christ/robe content anymore, so nothing here is regenerated at all.

Varied moves for richness (not the same "arc" on every spread) -- see each
entry's own note.

Run (sequential, gentle, $0):
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s_christ_spreads_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"

# (name, move, duration, focus, amp)
SPREADS = [
    # Identity anchor -- the film's first Christ render, longest hold (13.8s
    # per the plan). Most restrained treatment: a slow reverent push, no yaw.
    ("s51_jesus_pivot", "push", 8.0, (0.50, 0.28), 0.7),
    # "Entering" -- a gentle arc suits the forward motion already implied.
    ("s52_jesus_entering_formal", "arc", 4.5, (0.50, 0.40), 0.7),
    # THE ANSWER -- the film's thesis image (both goats small either side,
    # Christ central/radiant). Centered push keeps the symmetry intact.
    ("s56_the_answer", "push", 4.5, (0.50, 0.35), 0.7),
    # Two-panel spread (Christ through the gate / the goat's body at the
    # fire) -- an arc sweeps across both halves in sequence.
    ("s57_without_the_gate", "arc", 5.0, (0.50, 0.55), 0.9),
    # Seated, dignified -- a slow push, not a sweep.
    ("s60_seated_glory", "push", 4.5, (0.50, 0.45), 0.6),
    # Close face -- a gentle arc adds life to a portrait-hold without
    # overdoing it.
    ("s66_high_priests_face", "arc", 4.5, (0.50, 0.30), 0.5),
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
