#!/usr/bin/env python
"""Spread 5 (walking to the veil) -- the embroidered cherub wings on the
veil kept animating (flapping/distorting) across 2 generative attempts
(Seedance), the same failure class as s53's robe. $0 deterministic push
via dynamic_cam3d instead of a 3rd generative attempt.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s05_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s05_walking_to_veil.png"
DEST = HERE / "clips" / "s05_walking_to_veil.mp4"
FOCUS = (0.38, 0.42)  # Aaron's face, eye-checked against the still

if __name__ == "__main__":
    out = render_move(STILL, "push", duration=4.0, focus=FOCUS, dest=DEST, amp=0.7)
    print(f"[ok] {out}")
