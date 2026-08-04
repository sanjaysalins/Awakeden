#!/usr/bin/env python
"""Spread 25 (slaying stage 1) -- Kling invented blood on the goat's face/
neck by the end of the clip despite explicit "no wound, no blood, no red
mark appears anywhere at any point" language -- exactly the pre-flagged
elevated risk for this spread (a knife-adjacent staged tableau). $0
deterministic push via dynamic_cam3d instead of a 2nd generative attempt --
this project's own "no gore" doctrine is non-negotiable, not worth a retry
gamble.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s25_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s25_slaying_stage1.png"
DEST = HERE / "clips" / "s25_slaying_stage1.mp4"
FOCUS = (0.38, 0.42)  # between the raised knife and the goat's head

if __name__ == "__main__":
    out = render_move(STILL, "push", duration=5.0, focus=FOCUS, dest=DEST, amp=0.6)
    print(f"[ok] {out}")
