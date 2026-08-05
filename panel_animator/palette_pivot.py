#!/usr/bin/env python
"""East/West Palette Pivot -- colour choreography, not spatial light. The
whole frame's palette balance travels across the hold, keyed to the
composition's own halves: near-uniform at the start, then the two sides
are pushed chromatically APART over the hold -- one half warms, the other
cools -- following a soft split down the frame (not a hard graphic edge).
The separation is a scripted colour ARC with a beginning and an end
(title-sequence grade-arc thinking), unlike round 2's desat_focus (which
was spatial: colour lives wherever the light currently sits).

No camera movement, no crop/zoom/pan -- a pure per-pixel colour-temperature
blend, full frame throughout, deterministic.

Usage:
    python palette_pivot.py --still still.png --out clip.mp4 --duration 5.3 [--split-x 0.5]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FPS = 30
WARM_TINT = np.array([26, 8, -22], dtype=np.float32)   # push toward warm (west/sunset side)
COOL_TINT = np.array([-16, -4, 22], dtype=np.float32)  # push toward cool (east/dusk side)


def _ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render(still: Path, out_mp4: Path, duration: float, w: int = 1920, h: int = 1080,
           split_x: float = 0.5, softness: float = 0.22, max_strength: float = 1.0):
    base = _scale_crop(Image.open(still).convert("RGB"), w, h)
    src = np.asarray(base, dtype=np.float32)

    xs = np.linspace(0, 1, w, dtype=np.float32)
    # soft sigmoid split -- west (left) mask near 1, east (right) mask near 0
    west_mask = 1.0 / (1.0 + np.exp((xs - split_x) / softness))
    east_mask = 1.0 - west_mask
    west_mask = np.tile(west_mask[None, :], (h, 1))
    east_mask = np.tile(east_mask[None, :], (h, 1))

    n = max(1, int(round(duration * FPS)))
    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i in range(n):
        t = i / FPS
        strength = max_strength * _ease(t / duration)
        tint = (west_mask[..., None] * WARM_TINT[None, None, :] +
                east_mask[..., None] * COOL_TINT[None, None, :]) * strength
        frame = src + tint
        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--split-x", type=float, default=0.5, dest="split_x")
    a = ap.parse_args()
    render(Path(a.still), Path(a.out), a.duration, split_x=a.split_x)
