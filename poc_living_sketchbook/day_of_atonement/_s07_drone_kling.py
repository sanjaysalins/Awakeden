#!/usr/bin/env python
"""Spread 7 (the nation outside) -- a THIRD variant, alongside the static
Kling version (crowd frozen, ambient dust only) and the $0 deterministic
orbit-arc (dynamic_cam3d): asks Kling itself for a genuine drone flyover
camera move, keeping the same anti-invention safeguards that fixed the
original invented-figure defect (the empty courtyard named explicitly, ink-
on-paper reframe) but DROPPING the LOCK camera-stillness line on purpose --
this run is specifically testing whether Kling can hold "everyone frozen"
while ALSO doing real camera motion, rather than everything being frozen
including the camera.

Writes to clips/s07_nation_outside_dronekling.mp4 -- does not touch the
existing s07_nation_outside.mp4 (static Kling, fixed) or
s07_nation_outside_orbit.mp4 (deterministic orbit).

Run (real spend, ~$1.30, Kling):
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s07_drone_kling.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("_anim", ROOT / "poc_comic_page" / "_animate_piece1_v2.py")
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
A.EPISODE = "LS_DayOfAtonementLong"
A.OUT = HERE / "clips"
A.OUT.mkdir(exist_ok=True)

NAME = "s07_nation_outside_dronekling"
STILL = HERE / "stills" / "s07_nation_outside.png"
ASPECT = "16:9"

PROMPT = (
    "This is a finished ink-and-watercolor drawing on an aged page, an aerial "
    "bird's-eye view of the whole nation gathered in a great ring around the "
    "tabernacle courtyard on the Day of Atonement. The camera performs a slow, "
    "smooth drone flyover: it drifts gently forward and downward across the "
    "courtyard, as if a low-flying aerial camera were gliding over the scene. "
    "Every one of the hundreds of tiny figures in the crowd is ink on paper "
    "and stays exactly as drawn -- frozen, no one steps, turns, gestures, or "
    "walks. The empty courtyard between the gate and the tabernacle stays "
    "completely empty from the first frame to the last -- no figure enters "
    "it, nothing crosses it. INVENT NOTHING new anywhere in the frame -- no "
    "new figures, objects, or marks appear anywhere. Only: faint dust drifts "
    "across the outer ground, the tabernacle's linen hangings stir very "
    "slightly in the wind. Nothing else changes."
)

if __name__ == "__main__":
    ok = A.run_job(NAME, "kling", STILL, ASPECT, PROMPT, duration=5)
    print("done, clean" if ok else "FAILED")
