"""POC (2026-08-05, round 2): 4 more no-camera hold options the user picked
from the design panel's menu -- Breath-Synced Halo, Chiaroscuro Reveal,
Raking light (repositioned for cards/objects, no wobble/no flare this time),
Desat Focus. All still zero camera movement (no crop/zoom/pan).

Breath-Synced Halo is the one genuinely new combination: the approved
caravaggio_pulse halo, but its breathing damps toward stillness during this
episode's OWN real narration silences (from the already-existing
_alignment.json) instead of a fixed 3s sine cycle. New driver here (~40
lines), reusing focal_tour's own interleaved API (build_tour_schedule,
center_at, halo_brightness) + held_breath.energy_envelope -- both already-
built modules, no new visual language.

Chiaroscuro Reveal and Desat Focus are untried EXISTING focal_tour.py
styles -- zero new code, just render_clip() with a style name not tried yet.

Raking light gets a second look, minus the line-boil wobble AND minus the
gold-flare (both of which were part of the earlier rejected/misdiagnosed
POC) -- just the plain lamp sweep across a fully-lit, fully-legible page,
tested specifically on the scene TYPE the panel flagged the spotlight family
can't serve: a verse card (dimming would hurt lettering) and an object
close-up.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_holds_round2.py
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import focal_tour  # noqa: E402
from held_breath import energy_envelope  # noqa: E402
from raking_light import apply_raking_light, paper_tooth_highpass, scale_crop as rl_scale_crop  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "_poc_holds2"
OUT.mkdir(exist_ok=True)
WINDOWS = json.loads((HERE / "_spread_windows.json").read_text(encoding="utf-8"))
ALIGNMENT = json.loads((HERE / "_alignment.json").read_text(encoding="utf-8"))

W, H, FPS = 1920, 1080, 30
LAST_WORD_END = max(w["end"] for w in ALIGNMENT)


def window_of(name: str):
    row = next(r for r in WINDOWS if r["name"] == name)
    return row["start"], row["dur"]


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


# ------------------------------------------------------- 1. Breath-Synced Halo

def build_breath_synced_halo(name: str, bbox: list, dest: Path):
    start, dur = window_of(name)
    energy = energy_envelope(ALIGNMENT, LAST_WORD_END, floor=0.25, ramp=0.15)
    src = Image.open(STILLS / f"{name}.png").convert("RGB")
    src_arr = np.asarray(src.resize((W, H), Image.LANCZOS), dtype=np.float32) / 255.0
    y_grid, x_grid = np.mgrid[0:H, 0:W].astype(np.float32)

    regions = [{"bbox": bbox}]
    init_hold = max(0.8, min(2.5, dur * 0.18))
    move = max(0.5, min(1.0, dur * 0.08))
    final_hold = init_hold
    schedule = focal_tour.build_tour_schedule(regions, dur, W, H, init_hold, move, final_hold)

    n = max(1, int(round(dur * FPS)))
    frames_dir = OUT / f"{dest.stem}_frames"
    frames_dir.mkdir(exist_ok=True)
    for i in range(n):
        t_local = i / FPS
        e = energy(start + t_local)  # this episode's OWN real narration silences
        cx, cy, r = focal_tour.center_at(schedule, t_local)
        r_pulsed = r * (1.0 + 0.20 * e * np.sin(2 * np.pi * (t_local % 3.0) / 3.0))
        dim_floor = 0.30 - 0.04 * (1.0 - e)  # floor deepens slightly in real silences
        bright = focal_tour.halo_brightness(x_grid, y_grid, cx, cy, r_pulsed, dim_floor)
        frame = np.clip(src_arr * bright[..., None] * 255.0, 0, 255).astype(np.uint8)
        Image.fromarray(frame).save(frames_dir / f"f{i:04d}.png")
    run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "f%04d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    print(f"[ok] breath_synced_halo {name} -> {dest}")


# ------------------------------------------------------- 2/3. existing focal_tour styles

def build_focal_style(name: str, bboxes: list, style: str, dest: Path):
    _, dur = window_of(name)
    still = STILLS / f"{name}.png"
    regions = [{"bbox": b} for b in bboxes]
    focal_tour.render_clip(still, regions, style, dur, W, H, dest)
    print(f"[ok] {style} {name} -> {dest}")


# ------------------------------------------------------- 4. Raking light (cards/objects)

def build_raking_only(name: str, dest: Path):
    _, dur = window_of(name)
    still = STILLS / f"{name}.png"
    base = rl_scale_crop(Image.open(still).convert("RGB"), W, H)
    tooth = paper_tooth_highpass(base)
    n = max(1, int(round(dur * FPS)))
    frames_dir = OUT / f"{dest.stem}_frames"
    frames_dir.mkdir(exist_ok=True)
    for i in range(n):
        progress = i / max(1, n - 1)
        frame = apply_raking_light(base, progress, tooth=tooth, k=0.03)
        frame.save(frames_dir / f"f{i:04d}.png")
    run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "f%04d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(dest)])
    print(f"[ok] raking_only {name} -> {dest}")


if __name__ == "__main__":
    # 1. Breath-Synced Halo -- same 2 spreads as the approved spotlight POC
    build_breath_synced_halo("s51_jesus_pivot", [38, 6, 24, 32], OUT / "s51_jesus_pivot_breath_synced.mp4")
    build_breath_synced_halo("s60_seated_glory", [40, 4, 20, 30], OUT / "s60_seated_glory_breath_synced.mp4")

    # 2. Chiaroscuro Reveal -- a real multi-figure "argument" spread
    build_focal_style("s56_the_answer",
                       [[38, 8, 24, 30], [8, 60, 20, 28], [72, 60, 20, 28]],
                       "chiaroscuro_reveal", OUT / "s56_the_answer_chiaroscuro.mp4")

    # 3. Desat Focus -- a daylight wide landscape
    build_focal_style("s68_east_west_horizon", [[40, 30, 25, 35]],
                       "desat_focus", OUT / "s68_east_west_horizon_desat.mp4")

    # 4. Raking light, no wobble/no flare -- a verse card and an object close-up
    build_raking_only("s16_lords_charge_card", OUT / "s16_lords_charge_card_raking.mp4")
    build_raking_only("s42_basin_linen_ready", OUT / "s42_basin_linen_ready_raking.mp4")
