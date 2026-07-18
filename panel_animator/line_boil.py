#!/usr/bin/env python
"""Line-boil -- a subtle per-frame wobble (micro translate/rotate/scale,
smooth low-frequency sine jitter, NOT random per-frame flicker) that makes a
clip read as hand-inked frame-by-frame animation rather than a computer-
locked render. Real traditionally-animated comics are never perfectly
stable frame to frame; this adds that imperfection back in.

$0, deterministic PIL (frame-by-frame affine) + ffmpeg re-encode.

Usage:
    python line_boil.py --clip clip.mp4 --out clip_boil.mp4 [--amount 1.0]
"""
from __future__ import annotations
import argparse
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image


def boil_params(t: float, amount: float):
    dx = amount * (1.6 * math.sin(2 * math.pi * 0.7 * t + 0.3) + 0.6 * math.sin(2 * math.pi * 1.9 * t))
    dy = amount * (1.3 * math.sin(2 * math.pi * 0.5 * t + 1.1) + 0.5 * math.sin(2 * math.pi * 2.3 * t + 0.6))
    rot = amount * 0.16 * math.sin(2 * math.pi * 0.6 * t + 2.0)
    return dx, dy, rot


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


def render(clip: Path, out_mp4: Path, amount: float):
    w, h, fps = _probe(clip)
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    subprocess.run(["ffmpeg", "-y", "-i", str(clip), str(work / "f%05d.png")],
                    check=True, capture_output=True)
    frames = sorted(work.glob("f*.png"))

    margin = 1.03   # oversample so rotation/translate never exposes empty edges
    bw, bh = int(w * margin), int(h * margin)
    ox, oy = (bw - w) // 2, (bh - h) // 2

    for i, fp in enumerate(frames):
        t = i / fps
        dx, dy, rot = boil_params(t, amount)
        im = Image.open(fp).convert("RGB").resize((bw, bh), Image.LANCZOS)
        im = im.rotate(rot, resample=Image.BICUBIC, center=(bw / 2, bh / 2))
        left, top = ox - dx, oy - dy
        cropped = im.crop((int(left), int(top), int(left) + w, int(top) + h))
        cropped.save(fp)

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
                    "-i", str(clip), "-map", "0:v", "-map", "1:a?",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
                    "-shortest", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--amount", type=float, default=1.0, help="jitter strength multiplier")
    a = ap.parse_args()
    render(Path(a.clip), Path(a.out), a.amount)
