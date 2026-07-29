#!/usr/bin/env python
"""Blue-Line -- a spread opens as underdrawing (non-photo-blue construction
lines over a pale, desaturated wash) and the ink arrives once, resolving the
drawing along a soft hand-wobbled diagonal front, ~0.9s. Then it is a
finished drawing like every other spread -- the pleasure is in the ARRIVAL,
not a lingering effect.

$0, deterministic: cv2.adaptiveThreshold + Sobel on the dark channel extract
the underdrawing's linework from the one finished still (no second render);
the wipe front reuses the hand-wobbled jittered-polyline mask pattern from
poc_living_sketchbook/storm/_s4_assemble.py's transition_mask().

Usage (standalone preview/tuning):
    python blue_line.py --demo --still still.png --out demo.mp4 [--duration 3.0]
        [--feather 75] [--seed 11]

Library use (the real production path -- import into an episode's assemble
script, see .claude/skills/blue-line/SKILL.md):
    from panel_animator.blue_line import make_underdrawing_plate, apply_blue_line_reveal
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

INK_BLUE = (90, 140, 200)   # non-photo-blue
PAPER = (248, 245, 235)     # warm off-white to blend toward, not clinical pure white


def make_underdrawing_plate(still: Image.Image) -> Image.Image:
    """From a finished still, produce a plausible underdrawing: luminance
    lifted + desaturated + flattened base (the "blocked-in pale wash"), with
    dark-channel linework extracted (adaptiveThreshold + Sobel) and re-tinted
    toward non-photo-blue at low opacity (the "construction lines")."""
    rgb = still.convert("RGB")
    w, h = rgb.size
    arr = np.array(rgb)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    # smooth first so fine paint texture doesn't get picked up as false line noise
    gray_blur = cv2.GaussianBlur(gray, (0, 0), sigmaX=1.3)

    # adaptiveThreshold on the dark channel: locally-dark pixels (contours,
    # fold shadows, silhouette edges) -> the bulk of the "construction lines"
    block = 35  # must be odd
    adaptive = cv2.adaptiveThreshold(
        gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, block, 9,
    )

    # Sobel magnitude: catches soft large-scale silhouette edges (e.g. a wave
    # crest against sky) that a small adaptiveThreshold block misses
    sx = cv2.Sobel(gray_blur, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(gray_blur, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(sx, sy)
    mag = np.clip(mag / (np.percentile(mag, 99.0) + 1e-6) * 255, 0, 255).astype("uint8")
    _, sobel_mask = cv2.threshold(mag, 45, 255, cv2.THRESH_BINARY)

    linework = np.maximum(adaptive, sobel_mask)
    linework = cv2.medianBlur(linework, 3)   # drop single-pixel speckle noise

    # pale, flattened base: lift luminance toward paper, desaturate ~65%,
    # flatten contrast so washes read as blocked-in color, not rendered form
    lifted = Image.blend(rgb, Image.new("RGB", (w, h), PAPER), 0.38)
    desat = ImageEnhance.Color(lifted).enhance(0.35)
    base = ImageEnhance.Contrast(desat).enhance(0.62)

    # re-tint the extracted linework toward ink-blue at low opacity over the base
    line_alpha = Image.fromarray(linework).convert("L")
    ink_layer = Image.new("RGBA", (w, h), (*INK_BLUE, 0))
    ink_layer.putalpha(line_alpha.point(lambda v: int(v * 0.50)))
    result = Image.alpha_composite(base.convert("RGBA"), ink_layer)
    return result.convert("RGB")


def _ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def _wobbled_diagonal_mask(w: int, h: int, progress: float, seed: int, feather_px: float) -> Image.Image:
    """0/255 mask (blurred to feather): 255 = show finished, 0 = show
    underdrawing. A hand-wobbled front along lines of constant x+y, so it
    sweeps diagonally top-left -> bottom-right as progress goes 0 -> 1.
    Adapts the jittered-polyline pattern from _s4_assemble.py's
    transition_mask() -- same trick (polygon of jittered edge points, then
    Gaussian-blur the hard edge into a feather), rotated 45 degrees."""
    rng = random.Random(seed)
    diag = w + h
    margin = feather_px * 3.0   # front starts/ends fully off-canvas either side
    center = -margin + max(0.0, min(1.0, progress)) * (diag + 2 * margin)

    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    step = 40
    jitter = feather_px * 0.55
    pts = [(-margin * 2, -margin * 2)]
    y = -step
    while y <= h + step:
        edge_x = center - y + rng.uniform(-jitter, jitter)
        pts.append((edge_x, y))
        y += step
    pts.append((-margin * 2, h + margin * 2))
    d.polygon(pts, fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather_px * 0.42))


def apply_blue_line_reveal(underdrawing: Image.Image, finished: Image.Image,
                            progress: float, seed: int = 11, feather_px: float = 75.0) -> Image.Image:
    """Composite underdrawing -> finished through a hand-wobbled diagonal
    wipe. progress=0.0 -> pure underdrawing, progress=1.0 -> pure finished."""
    w, h = finished.size
    assert underdrawing.size == (w, h), "plates must be the same size"
    mask = _wobbled_diagonal_mask(w, h, progress, seed, feather_px)
    return Image.composite(finished.convert("RGB"), underdrawing.convert("RGB"), mask)


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render_demo(still_path: Path, out_mp4: Path, duration: float, feather_px: float, seed: int):
    W, H, FPS = 1080, 1920, 30
    HOLD_UNDER = 0.3     # brief: page sits as underdrawing first
    SWEEP = 0.9           # brief: "about 0.9s, once"

    finished = scale_crop(Image.open(still_path).convert("RGB"), W, H)
    underdrawing = make_underdrawing_plate(finished)

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(duration * FPS)
    for i in range(n_frames):
        t = i / FPS
        if t < HOLD_UNDER:
            frame = underdrawing
        elif t < HOLD_UNDER + SWEEP:
            progress = _ease((t - HOLD_UNDER) / SWEEP)
            frame = apply_blue_line_reveal(underdrawing, finished, progress, seed=seed, feather_px=feather_px)
        else:
            frame = finished
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a standalone preview mp4 from one still")
    ap.add_argument("--still", help="source still (demo mode)")
    ap.add_argument("--out", help="output mp4 (demo mode)")
    ap.add_argument("--duration", type=float, default=3.0, help="demo clip length, seconds")
    ap.add_argument("--feather", type=float, default=75.0, help="wipe front feather width, px (60-90)")
    ap.add_argument("--seed", type=int, default=11, help="hand-wobble jitter seed")
    a = ap.parse_args()
    if a.demo:
        if not a.still or not a.out:
            raise SystemExit("--demo requires --still and --out")
        render_demo(Path(a.still), Path(a.out), a.duration, a.feather, a.seed)
    else:
        raise SystemExit("no CLI mode selected -- pass --demo, or import make_underdrawing_plate / "
                          "apply_blue_line_reveal directly (see .claude/skills/blue-line/SKILL.md)")
