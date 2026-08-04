#!/usr/bin/env python
"""Spread 76 (the landing, "already inside") -- $0 deterministic gentle push,
same dynamic_cam3d treatment as the other Christ spreads.

The plan calls the full `tear_hole` reveal (the page physically tearing open
AS the veil, gold light spilling from beneath) this landing's "mandatory"
device. Checked the whole repo for an existing implementation -- there isn't
one. It's referenced in several files' comments as "the landing's own
device," but the only real precedent (Bronze Serpent's own landing, s68)
explicitly deferred it as a "polish-pass device... here it's just a plain
held frame" and shipped without it. Same call here: a reverent held/pushed
frame now (real, finished, $0), tear_hole as a future polish layer if
wanted later -- not a half-built compositing device pretending to be done.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s76_landing.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s76_already_inside.png"
DEST = HERE / "clips" / "s76_already_inside.mp4"
FOCUS = (0.50, 0.35)  # Christ's face, eye-checked against the still

if __name__ == "__main__":
    out = render_move(STILL, "push", duration=5.3, focus=FOCUS, dest=DEST, amp=0.5)
    print(f"[ok] {out}")
