"""Her Seed -- s03 "The Lamp Finds It Finished" motion graphic, full build.
Production version of the concept Fable designed and the user approved from
the preview (`_MOTION_CONCEPTS_s03_s05.html`).

Layer 1 (reused device, no new code): `panel_animator/raking_light.py`'s
plain sweep -- already rendered to clips/s03_already_written_page.mp4 by a
separate `raking_light.py --demo` call. Diff-checked against its own first
frame: the effect is real but genuinely too subtle on THIS still (mean
pixel change ~0.1/255, ~2000 of 2,073,600 pixels changed) to read as
"alive" on its own -- this still has little of the high-tooth/edge texture
the device's luminance-modulation approach needs to be visible. That
matches the skill's own honest warning (k=0.03 is tuned to be barely
perceptible) but isn't enough alone for what was approved.

Layer 2 (this script): flame flicker + drifting dust motes + a late,
gentle warm-grade fade, composited on top of the raking-light base --
completes Fable's actual concept (only the sweep half was built by the
reused device). Flame position (0.43, 0.11) measured directly off the
real still, not guessed.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s03_lamp_finds_it.py
"""
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
BASE_CLIP = HERE / "clips" / "s03_already_written_page.mp4"     # raking-light sweep, already rendered
OUT = HERE / "clips" / "s03_already_written_page.mp4"
WORK = HERE / "_s03_work"

W, H, FPS = 1080, 1920, 30
FLAME_X, FLAME_Y = 0.43 * W, 0.11 * H     # measured off the real still

MOTES = [
    # (x_frac, y_frac, start_frac, dx_px, dy_px)
    (0.47, 0.16, 0.55, -8, -75),
    (0.39, 0.18, 0.62, 10, -62),
    (0.51, 0.13, 0.48, -4, -85),
]


def extract_base_frames():
    WORK.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(BASE_CLIP),
                     str(WORK / "b%04d.png")], check=True)
    return sorted(WORK.glob("b*.png"))


def main():
    frames = extract_base_frames()
    n = len(frames)
    duration = n / FPS

    for i, fpath in enumerate(frames):
        t = i / FPS
        frac = t / duration
        frame = Image.open(fpath).convert("RGB")
        arr = np.array(frame).astype(float)

        # --- flame flicker: small radial glow, trembling scale/opacity ---
        flick = 1.0 + 0.12 * math.sin(t * 2 * math.pi * 5.4) + 0.06 * math.sin(t * 2 * math.pi * 13.1)
        radius = 26 * max(0.7, flick)
        yy, xx = np.mgrid[0:H, 0:W]
        dist2 = (xx - FLAME_X) ** 2 + (yy - FLAME_Y) ** 2
        glow = np.exp(-dist2 / (2 * radius ** 2)) * 70.0 * max(0.6, flick)
        arr[..., 0] += glow          # warm: boost R most
        arr[..., 1] += glow * 0.75
        arr[..., 2] += glow * 0.35

        # --- dust motes: drift up + slight horizontal parallax after the sweep passes ---
        for mx_f, my_f, start_f, dx, dy in MOTES:
            if frac < start_f:
                continue
            p = min(1.0, (frac - start_f) / max(1e-6, (1.0 - start_f)))
            fade = math.sin(min(1.0, p * 1.6) * math.pi)  # fade in then out
            mx = mx_f * W + dx * p
            my = my_f * H + dy * p
            mr = 2.2
            d2 = (xx - mx) ** 2 + (yy - my) ** 2
            mote_glow = np.exp(-d2 / (2 * (mr * 2.2) ** 2)) * 90.0 * fade
            arr[..., 0] += mote_glow
            arr[..., 1] += mote_glow * 0.9
            arr[..., 2] += mote_glow * 0.72

        # --- late gentle warm-grade fade (settles in after the sweep exits) ---
        if frac > 0.55:
            grade_p = min(1.0, (frac - 0.55) / 0.30)
            grade_dist2 = (xx - 0.6 * W) ** 2 + (yy - 0.2 * H) ** 2
            grade = np.exp(-grade_dist2 / (2 * (700) ** 2)) * 18.0 * grade_p
            arr[..., 0] += grade
            arr[..., 1] += grade * 0.72
            arr[..., 2] += grade * 0.30

        out_frame = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
        out_frame.save(fpath)

    tmp_out = WORK / "_s03_final.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(WORK / "b%04d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp_out)], check=True)

    for f in WORK.glob("b*.png"):
        f.unlink()
    tmp_out.replace(OUT)
    WORK.rmdir()
    print(f"[ok] -> {OUT}")


if __name__ == "__main__":
    main()
