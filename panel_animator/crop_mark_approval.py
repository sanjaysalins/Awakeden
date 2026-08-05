#!/usr/bin/env python
"""Crop-Mark Approval -- the motion lives entirely in the negative space, the
art itself stays untouched at full legibility. Four pale graphite corner
crop-marks (the kind a paste-up carries when it's ready for the press) draw
themselves in, one at a time, staggered like a hand marking up a layout --
then, on the hold's closing beat, a single thin rule draws in under the
frame, as if the page has just been passed for print. Real editorial-motion-
design vocabulary (graphic accents entering with intention), not simulated
light or paper physics, and it never touches the drawn art at all -- the
purest "no-dimming" answer for verse cards where legibility must not drop.

No camera movement, no crop/zoom/pan, no repaint of the art -- a pure
overlay compositing pass, deterministic PIL draw calls with a hand-wobbled
stroke (small per-segment jitter, same discipline as this project's other
hand-drawn overlay devices).

Usage:
    python crop_mark_approval.py --still still.png --out clip.mp4 --duration 3.75
"""
from __future__ import annotations
import argparse
import random
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

FPS = 30
MARK_LEN = 46          # px, each crop-mark arm length
MARK_INSET = 34        # px inset from the true frame corner
MARK_COLOR = (90, 86, 74, 165)   # pale graphite, semi-transparent
RULE_COLOR = (90, 86, 74, 140)
STROKE_W = 2


def _ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _wobbled_line(d: ImageDraw.ImageDraw, p0, p1, frac: float, color, rng: random.Random):
    """Draw the segment from p0 toward p1, only up to `frac` of the way, with
    a couple of small hand-jitter waypoints so it doesn't read as a vector
    ruler line."""
    if frac <= 0:
        return
    x0, y0 = p0
    x1, y1 = p0[0] + (p1[0] - p0[0]) * frac, p0[1] + (p1[1] - p0[1]) * frac
    mx, my = (x0 + x1) / 2 + rng.uniform(-0.6, 0.6), (y0 + y1) / 2 + rng.uniform(-0.6, 0.6)
    d.line([(x0, y0), (mx, my), (x1, y1)], fill=color, width=STROKE_W, joint="curve")


def _corner_marks(corner: str, w: int, h: int) -> list[tuple]:
    """Two short perpendicular arms forming an L, offset inward from the
    true corner (real print crop-marks never touch the trim edge)."""
    if corner == "tl":
        ox, oy = MARK_INSET, MARK_INSET
        return [((ox - MARK_LEN, oy), (ox, oy)), ((ox, oy - MARK_LEN), (ox, oy))]
    if corner == "tr":
        ox, oy = w - MARK_INSET, MARK_INSET
        return [((ox + MARK_LEN, oy), (ox, oy)), ((ox, oy - MARK_LEN), (ox, oy))]
    if corner == "bl":
        ox, oy = MARK_INSET, h - MARK_INSET
        return [((ox - MARK_LEN, oy), (ox, oy)), ((ox, oy + MARK_LEN), (ox, oy))]
    ox, oy = w - MARK_INSET, h - MARK_INSET  # br
    return [((ox + MARK_LEN, oy), (ox, oy)), ((ox, oy + MARK_LEN), (ox, oy))]


def render(still: Path, out_mp4: Path, duration: float, w: int = 1920, h: int = 1080, seed: int = 17):
    base = _scale_crop(Image.open(still).convert("RGB"), w, h)
    rng = random.Random(seed)

    corners = ["tl", "tr", "bl", "br"]
    stagger = min(0.55, duration * 0.09)  # gap between each corner's start
    mark_draw_dur = 0.32
    marks_span = stagger * (len(corners) - 1) + mark_draw_dur
    rule_start = max(marks_span + 0.3, duration - 0.9)
    rule_dur = 0.5

    n = max(1, int(round(duration * FPS)))
    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i in range(n):
        t = i / FPS
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        for ci, corner in enumerate(corners):
            start_t = ci * stagger
            frac = _ease((t - start_t) / mark_draw_dur) if t > start_t else 0.0
            for p0, p1 in _corner_marks(corner, w, h):
                _wobbled_line(d, p0, p1, frac, MARK_COLOR, rng)

        if t > rule_start:
            rf = _ease((t - rule_start) / rule_dur)
            ry = h - 64
            x0, x1 = w * 0.30, w * 0.30 + (w * 0.40) * rf
            _wobbled_line(d, (x0, ry), (x0 + (x1 - x0), ry), 1.0 if rf > 0 else 0.0, RULE_COLOR, rng)

        frame = base.convert("RGBA")
        frame.alpha_composite(overlay)
        frame.convert("RGB").save(work / f"f{i:04d}.png")

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
    a = ap.parse_args()
    render(Path(a.still), Path(a.out), a.duration)
