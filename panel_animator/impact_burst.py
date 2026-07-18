#!/usr/bin/env python
"""Hand-drawn ink "impact" burst, composited onto a real clip at an exact
SFX-hit timestamp (not a generic flash/shake -- an actual jagged ink-star
burst + radiating speed lines, drawn with the same rough-edge technique as
the caption band / brush arrow). $0, deterministic PIL + ffmpeg.

In production the hit timestamp comes from the episode's forced-aligned
SFX/caption timing (the same alignment already driving captions/SFX beds) --
here it's passed explicitly so this POC can be tested against any moment.

Usage:
    python impact_burst.py --clip clip.mp4 --at 1.20 --xy 0.62,0.68 \
        --out clip_with_impact.mp4 [--duration 0.32] [--color ink|blood]
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

INK = (20, 14, 10)
BLOOD = (94, 18, 14)


def draw_burst(size: int, progress: float, color: tuple, seed: int = 11) -> Image.Image:
    """progress 0..1 across the whole burst life (grow then fade)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size / 2, size / 2
    rng = random.Random(seed)

    grow = min(1.0, progress / 0.35)
    fade = 1.0 if progress < 0.45 else max(0.0, 1 - (progress - 0.45) / 0.55)
    scale = 0.35 + 0.65 * (1 - (1 - grow) ** 2)          # ease-out grow
    alpha = int(255 * fade)
    if alpha <= 2:
        return img

    # jagged ink-star burst: alternating long/short spikes around the center
    n_spikes = 14
    pts = []
    for i in range(n_spikes * 2):
        ang = (i / (n_spikes * 2)) * 2 * math.pi
        long_spike = (i % 2 == 0)
        base_r = (size * 0.42 if long_spike else size * 0.16) * scale
        r = base_r * (1 + rng.uniform(-0.12, 0.12))
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(*color, alpha))

    # a few radiating speed-line streaks beyond the star
    for i in range(8):
        ang = rng.uniform(0, 2 * math.pi)
        r0 = size * 0.40 * scale
        r1 = r0 + size * 0.22 * scale * rng.uniform(0.7, 1.15)
        x0, y0 = cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)
        x1, y1 = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)
        d.line([(x0, y0), (x1, y1)], fill=(*color, int(alpha * 0.8)), width=max(2, int(size * 0.012)))

    return img.filter(ImageFilter.GaussianBlur(0.6))


def _probe(clip: Path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-of", "csv=s=x:p=0", str(clip)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    w, h, fr = out.split("x")
    num, den = fr.split("/")
    fps = float(num) / float(den)
    return int(w), int(h), fps


def render(clip: Path, at: float, xy: tuple[float, float], out_mp4: Path,
           duration: float, color_name: str):
    color = BLOOD if color_name == "blood" else INK
    w, h, fps = _probe(clip)
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = max(2, int(duration * fps))
    win_start = at
    before, window, after = work / "before.mp4", work / "window.mp4", work / "after.mp4"

    subprocess.run(["ffmpeg", "-y", "-i", str(clip), "-t", f"{win_start:.3f}",
                    "-c", "copy", str(before)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{win_start:.3f}", "-i", str(clip),
                    "-t", f"{duration:.3f}", "-r", str(fps), str(work / "win_%04d.png")],
                   check=True, capture_output=True)

    burst_size = int(min(w, h) * 0.55)
    cx, cy = int(xy[0] * w), int(xy[1] * h)
    frame_files = sorted(work.glob("win_*.png"))
    for i, fp in enumerate(frame_files):
        progress = i / max(1, len(frame_files) - 1)
        burst = draw_burst(burst_size, progress, color)
        base = Image.open(fp).convert("RGBA")
        base.alpha_composite(burst, (cx - burst_size // 2, cy - burst_size // 2))
        base.convert("RGB").save(fp)

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "win_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(window)],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-ss", f"{win_start + duration:.3f}", "-i", str(clip),
                    "-c", "copy", str(after)], check=True, capture_output=True)

    concat_list = work / "concat.txt"
    concat_list.write_text(
        f"file '{before.resolve().as_posix()}'\n"
        f"file '{window.resolve().as_posix()}'\n"
        f"file '{after.resolve().as_posix()}'\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--at", type=float, required=True, help="hit timestamp, seconds")
    ap.add_argument("--xy", default="0.5,0.5", help="impact center, fraction of frame w,h")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=0.32)
    ap.add_argument("--color", choices=["ink", "blood"], default="ink")
    a = ap.parse_args()
    ox, oy = (float(v) for v in a.xy.split(","))
    render(Path(a.clip), a.at, (ox, oy), Path(a.out), a.duration, a.color)
