#!/usr/bin/env python
"""Spread 53 (the cross) -- replaces the generative Kling/Seedance attempt
with a $0 deterministic camera arc (panel_animator/dynamic_cam3d.py). Three
prompt-tightening rounds on Seedance still animated the robe (billowing/
swinging, user: "Jesus is dancing"); rather than a 4th generative attempt
fighting the same invention risk, this treats the still as a rigid plane
and moves a virtual camera over it -- nothing is ever regenerated, so the
robe literally cannot move, while still giving a real orbit-around-Christ
camera feel (the user's own request).

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s53_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s53_the_cross.png"
DEST = HERE / "clips" / "s53_the_cross.mp4"
FOCUS = (0.51, 0.30)  # Christ's face/chest, eye-checked against the still

if __name__ == "__main__":
    out = render_move(STILL, "arc", duration=4.5, focus=FOCUS, dest=DEST, amp=0.8)
    print(f"[ok] {out}")
