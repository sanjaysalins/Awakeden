"""THROWAWAY EPISODE BUILD -- the 6 $0 camera segments over the 3 static
plates, timed to the real word-alignment boundaries of the narration.

Timeline (from pipeline.assembly_align on the real narration.mp3):
  S1  far_corner_01   [0.00, 4.18]    hook dive, whole complex -> pool
  A   insert (paid)   [4.18, 9.18]    water stirs, crowd surges  (fixed 5.0s)
  S3  far_corner_02   [9.18, 16.80]   track down the porch to the far corner
  S4  far_corner_03   [16.80, 26.04]  Jesus present, push in, "wilt thou..."
  S5  far_corner_03   [26.04, 33.36]  continue push, "the old answer..."
  B   insert (paid)   [33.36, 38.36]  "Rise..." -- the man stands  (fixed 5.0s)
  S7  final_plate     [38.36, 47.64]  pull back, the turn
  S8  final_plate     [47.64, 61.88]  landing hold (58.88 last word + 3.0s)
"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STILLS = HERE.parent / "stills"
SEG = HERE / "segments"
sys.path.insert(0, str(HERE.parent.parent / "panel_animator"))
from insert_page_camera import InsertPageCamera  # noqa: E402

SEGMENTS = [
    dict(name="s1", still=STILLS / "far_corner_01.png", duration=4.18, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.42, "zoom": 1.02, "hold_s": 0.3},
        {"t": 1.00, "cx": 0.50, "cy": 0.46, "zoom": 1.65, "hold_s": 0.0},
    ]),
    dict(name="s3", still=STILLS / "far_corner_02.png", duration=7.62, keyframes=[
        {"t": 0.00, "cx": 0.42, "cy": 0.12, "zoom": 1.35, "hold_s": 0.4},
        {"t": 1.00, "cx": 0.28, "cy": 0.80, "zoom": 1.30, "hold_s": 0.3},
    ]),
    dict(name="s4", still=STILLS / "far_corner_03.png", duration=9.24, keyframes=[
        {"t": 0.00, "cx": 0.55, "cy": 0.55, "zoom": 1.00, "hold_s": 1.0},
        {"t": 1.00, "cx": 0.55, "cy": 0.60, "zoom": 1.25, "hold_s": 0.0},
    ]),
    dict(name="s5", still=STILLS / "far_corner_03.png", duration=7.32, keyframes=[
        {"t": 0.00, "cx": 0.55, "cy": 0.60, "zoom": 1.25, "hold_s": 0.5},
        {"t": 1.00, "cx": 0.50, "cy": 0.62, "zoom": 1.40, "hold_s": 0.0},
    ]),
    dict(name="s7", still=HERE / "final_plate.png", duration=9.28, keyframes=[
        {"t": 0.00, "cx": 0.27, "cy": 0.50, "zoom": 1.80, "hold_s": 0.3},
        {"t": 1.00, "cx": 0.50, "cy": 0.46, "zoom": 1.02, "hold_s": 0.5},
    ]),
    dict(name="s8", still=HERE / "final_plate.png", duration=14.24, keyframes=[
        {"t": 0.00, "cx": 0.50, "cy": 0.46, "zoom": 1.02, "hold_s": 12.0},
        {"t": 1.00, "cx": 0.50, "cy": 0.44, "zoom": 1.08, "hold_s": 0.0},
    ]),
]

if __name__ == "__main__":
    SEG.mkdir(exist_ok=True)
    for spec in SEGMENTS:
        out = SEG / f"{spec['name']}.mp4"
        cam = InsertPageCamera(spec["still"], keyframes=spec["keyframes"], duration_s=spec["duration"])
        cam.render_clip(out)
        print(f"  duration target={spec['duration']:.2f}s")
