"""Test 1 (Fable's plan, 2026-08-20) -- $0 deterministic "always alive" pass
over an already-rendered raw clip: whole-page line_boil (paper-life) +
raking_light (one slow lamp sweep) + ink_bloom breathing pulses at 2
calibrated points in the swirl threads. No new AI generation, no risk of
re-triggering the shot-6 escalation (nothing here can grow past its own
coded radius/strength cap) or the panel-lock seam (nothing is replaced with
static pixels -- every layer modulates the clip's own live pixels).

Calibration points picked by eye on the_cross_kling.mp4's own first frame
(_calib_frame0.jpg) -- the two visible clusters of blue swirl thread, left
and right of Jesus's torso, well clear of his face/robe/wound marks.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\build_deterministic_pass.py
"""
from __future__ import annotations

import math
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "panel_animator"))
sys.path.insert(0, str(HERE.parent / "northstar_shortform"))

import line_boil       # noqa: E402
import raking_light    # noqa: E402
import ink_bloom       # noqa: E402

from PIL import Image  # noqa: E402

SRC = HERE / "the_cross_kling.mp4"
BOILED = HERE / "_dpass_1_boiled.mp4"
LIT = HERE / "_dpass_2_lit.mp4"
FINAL = HERE / "the_cross_kling_alive.mp4"

# Two calibrated swirl-thread points (cx_frac, cy_frac), eyeballed on
# _calib_frame0.jpg -- left cluster below/left of his torso, right cluster
# below his right arm, both well clear of face/wounds/robe.
POINTS = [
    {"cx": 0.14, "cy": 0.68, "radius": 0.09, "period": 3.1, "phase": 0.0},
    {"cx": 0.84, "cy": 0.66, "radius": 0.11, "period": 2.6, "phase": 1.4},
]
MAX_STRENGTH = 0.25   # Fable's Stage-3 recommendation
BREATH_FLOOR = 0.35   # never fully off -- a floor, not a flicker


def _probe(clip: Path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-of", "csv=s=x:p=0", str(clip)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    w, h, fr = out.split("x")
    num, den = fr.split("/")
    return int(w), int(h), float(num) / float(den)


def apply_ink_breathing(clip: Path, out_mp4: Path) -> None:
    w, h, fps = _probe(clip)
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    subprocess.run(["ffmpeg", "-y", "-i", str(clip), str(work / "f%05d.png")],
                    check=True, capture_output=True)
    frames = sorted(work.glob("f*.png"))
    n = len(frames)

    for i, fp in enumerate(frames):
        t = i / fps
        frame = Image.open(fp).convert("RGB")
        for p in POINTS:
            breath = BREATH_FLOOR + (1.0 - BREATH_FLOOR) * (
                0.5 + 0.5 * math.sin(2 * math.pi * t / p["period"] + p["phase"]))
            strength = MAX_STRENGTH * breath
            frame = ink_bloom.apply_ink_bloom(frame, p["cx"], p["cy"], p["radius"], strength)
        frame.save(fp)

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
                    "-i", str(clip), "-map", "0:v", "-map", "1:a?",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
                    "-shortest", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    print("[1/3] line_boil (whole-page paper life)...")
    line_boil.render(SRC, BOILED, amount=0.7)

    print("[2/3] raking_light (one slow lamp sweep)...")
    w, h, _ = _probe(BOILED)
    raking_light.render_clip(BOILED, LIT, flare=False, k=0.025, intensity=1.0,
                              band_width_px=max(w, h) * 0.5, angle_deg=15.0)

    print("[3/3] ink_bloom breathing (2 calibrated swirl points)...")
    apply_ink_breathing(LIT, FINAL)

    print(f"\nDone -> {FINAL}")
