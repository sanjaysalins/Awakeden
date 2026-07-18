#!/usr/bin/env python
"""2.5D parallax depth on a single still -- rembg extracts the nearest salient
subject as its own layer (with alpha), the full still stays as the base plate;
the two layers drift at different rates/directions, giving real depth instead
of a flat push-in. A cheaper, and on calm panels arguably more alive,
alternative to a generic generated push-in clip.

$0 after the one-time rembg model fetch: PIL compositing + ffmpeg encode.

Usage:
    python parallax_25d.py --still still.png --out parallax.mp4
        [--duration 4.0] [--fg-amp 14] [--bg-amp 5]
"""
from __future__ import annotations
import argparse
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image
from rembg import remove, new_session

FPS = 30


def render(still: Path, out_mp4: Path, duration: float, fg_amp: float, bg_amp: float):
    base = Image.open(still).convert("RGB")
    w, h = base.size

    session = new_session("u2net")
    fg = remove(base, session=session)          # RGBA cutout of the nearest subject

    # oversample the base plate so it can pan without exposing empty edges
    margin = 1.06
    bw, bh = int(w * margin), int(h * margin)
    base_big = base.resize((bw, bh), Image.LANCZOS)
    bx0, by0 = (bw - w) // 2, (bh - h) // 2

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(duration * FPS)
    for i in range(n_frames):
        t = i / FPS
        bgx = bg_amp * math.sin(2 * math.pi * 0.09 * t)
        bgy = bg_amp * 0.5 * math.sin(2 * math.pi * 0.07 * t + 0.8)
        fgx = fg_amp * math.sin(2 * math.pi * 0.09 * t + 3.14159)   # opposite phase = depth
        fgy = fg_amp * 0.5 * math.sin(2 * math.pi * 0.07 * t + 0.8 + 3.14159)

        frame = base_big.crop((int(bx0 + bgx), int(by0 + bgy),
                                int(bx0 + bgx) + w, int(by0 + bgy) + h)).convert("RGBA")
        frame.alpha_composite(fg, (int(fgx - bgx), int(fgy - bgy)))
        frame.convert("RGB").save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=4.0)
    ap.add_argument("--fg-amp", type=float, default=14.0, dest="fg_amp")
    ap.add_argument("--bg-amp", type=float, default=5.0, dest="bg_amp")
    a = ap.parse_args()
    render(Path(a.still), Path(a.out), a.duration, a.fg_amp, a.bg_amp)
