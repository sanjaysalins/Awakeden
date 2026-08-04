#!/usr/bin/env python
"""Spread 7 (the nation outside, bird's-eye) -- an aerial courtyard shot is
exactly the composition a real drone move reads best on (user's own call).
$0 deterministic camera arc (panel_animator/dynamic_cam3d.py) instead of/in
addition to the generative Kling clip -- treats the still as a plane and
sweeps a virtual camera across it, giving genuine drone-orbit motion with
zero risk of inventing a figure (nothing is regenerated).

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s07_orbit.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s07_nation_outside.png"
DEST = HERE / "clips" / "s07_nation_outside_orbit.mp4"  # separate file -- compare against the Kling version
FOCUS = (0.5, 0.45)  # tabernacle courtyard center

if __name__ == "__main__":
    out = render_move(STILL, "arc", duration=5.0, focus=FOCUS, dest=DEST, amp=1.0)
    print(f"[ok] {out}")
