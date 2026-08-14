"""Her Seed -- s03 "The Lamp Finds It Finished" motion graphic, full build.
Production version of the concept Fable designed and the user approved from
the preview (`_MOTION_CONCEPTS_s03_s05.html`).

v2: the first build layered a flickering flame + dust motes on top of
`panel_animator/raking_light.py`'s stock sweep -- but that device's tuned
default (k=0.03, deliberately subtle per its own locked lesson) diff-
checked as ~0.1/255 mean change on this still, and the user correctly
couldn't see any motion at all in playback. This version builds the
sweep itself directly and visibly -- a warm diagonal band of light
travels from the lamp (top-right) down across the page, clearly brighter
than raking-light's photometric-realism approach, matching what the
approved mockup actually showed -- plus the flame flicker, dust motes,
and late warm-grade settle from the first pass.

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s03_lamp_finds_it.py
"""
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from blue_line import scale_crop  # noqa: E402 -- reuse, don't duplicate

HERE = Path(__file__).resolve().parent
STILL = HERE / "stills" / "s03_already_written_page.png"
OUT = HERE / "clips" / "s03_already_written_page.mp4"
WORK = HERE / "_s03_work"

W, H, FPS = 1080, 1920, 30
DURATION = 4.5
FLAME_X, FLAME_Y = 0.43 * W, 0.11 * H     # measured off the real still

# diagonal sweep: lines of constant (x - y); top-right (high x-y) -> bottom-left (low x-y)
SWEEP_START, SWEEP_END = 0.10, 0.62       # fraction of DURATION the band travels
SWEEP_SIGMA = 340.0
SWEEP_PEAK = (125.0, 92.0, 34.0)          # warm gold, R>G>B

MOTES = [
    (0.47, 0.16, 0.55, -8, -75),
    (0.39, 0.18, 0.62, 10, -62),
    (0.51, 0.13, 0.48, -4, -85),
]


def main():
    WORK.mkdir(exist_ok=True)
    finished = scale_crop(Image.open(STILL).convert("RGB"), W, H)
    base = np.array(finished).astype(float)

    yy, xx = np.mgrid[0:H, 0:W]
    u = xx - yy                              # top-right ~ +W, bottom-left ~ -H
    u_start, u_end = W + 300, -H - 300

    n = int(DURATION * FPS)
    for i in range(n):
        t = i / FPS
        frac = t / DURATION
        arr = base.copy()

        # --- the sweep itself: a visible warm diagonal band travels top-right -> bottom-left ---
        sweep_p = (frac - SWEEP_START) / max(1e-6, (SWEEP_END - SWEEP_START))
        sweep_p = max(0.0, min(1.0, sweep_p))
        if SWEEP_START <= frac <= SWEEP_END + 0.06:
            u_center = u_start + sweep_p * (u_end - u_start)
            band = np.exp(-((u - u_center) ** 2) / (2 * SWEEP_SIGMA ** 2))
            arr[..., 0] += band * SWEEP_PEAK[0]
            arr[..., 1] += band * SWEEP_PEAK[1]
            arr[..., 2] += band * SWEEP_PEAK[2]

        # --- flame flicker: small radial glow, trembling scale/opacity ---
        flick = 1.0 + 0.12 * math.sin(t * 2 * math.pi * 5.4) + 0.06 * math.sin(t * 2 * math.pi * 13.1)
        radius = 26 * max(0.7, flick)
        dist2 = (xx - FLAME_X) ** 2 + (yy - FLAME_Y) ** 2
        glow = np.exp(-dist2 / (2 * radius ** 2)) * 70.0 * max(0.6, flick)
        arr[..., 0] += glow
        arr[..., 1] += glow * 0.75
        arr[..., 2] += glow * 0.35

        # --- dust motes: drift up + slight horizontal parallax after the sweep passes ---
        for mx_f, my_f, start_f, dx, dy in MOTES:
            if frac < start_f:
                continue
            p = min(1.0, (frac - start_f) / max(1e-6, (1.0 - start_f)))
            fade = math.sin(min(1.0, p * 1.6) * math.pi)
            mx = mx_f * W + dx * p
            my = my_f * H + dy * p
            mr = 2.2
            d2 = (xx - mx) ** 2 + (yy - my) ** 2
            mote_glow = np.exp(-d2 / (2 * (mr * 2.2) ** 2)) * 90.0 * fade
            arr[..., 0] += mote_glow
            arr[..., 1] += mote_glow * 0.9
            arr[..., 2] += mote_glow * 0.72

        # --- late gentle warm-grade fade (settles in after the sweep exits) ---
        if frac > 0.62:
            grade_p = min(1.0, (frac - 0.62) / 0.30)
            grade_dist2 = (xx - 0.6 * W) ** 2 + (yy - 0.2 * H) ** 2
            grade = np.exp(-grade_dist2 / (2 * (700) ** 2)) * 20.0 * grade_p
            arr[..., 0] += grade
            arr[..., 1] += grade * 0.72
            arr[..., 2] += grade * 0.30

        out_frame = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
        out_frame.save(WORK / f"f{i:04d}.png")

    tmp_out = WORK / "_s03_final.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(WORK / "f%04d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp_out)], check=True)

    for f in WORK.glob("f*.png"):
        f.unlink()
    tmp_out.replace(OUT)
    WORK.rmdir()
    print(f"[ok] -> {OUT}")


if __name__ == "__main__":
    main()
