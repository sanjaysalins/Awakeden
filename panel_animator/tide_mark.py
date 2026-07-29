#!/usr/bin/env python
"""Tide-Mark -- a real damp tide-line across the bottom of the SHEET (not the
drawing): a wavering, never-straight boundary with a slightly darker feathered
ridge exactly at the edge and faintly warmer/heavier paper below it, the way a
page stains after sitting in a puddle. It rises as fear rises, holds through
the crisis, then dries back to a faint PERMANENT ghost line -- paper never
fully forgets a soaking. On one later beat it can snap back to its old
high-water height.

$0, deterministic numpy: the boundary is a 1-D height field (3-4 seeded sines
+ light smoothing, never a straight line, never a gauge); each frame is
multiply-darkened + warm-tinted below that line with a 4-8px feathered ridge
at the boundary itself.

Usage (library):
    from tide_mark import apply_tide_mark, tide_height_curve
    frame = apply_tide_mark(frame, height_frac=0.18, seed=7)

Usage (demo CLI -- simple rise-and-recede over a still, NOT the authored
Storm curve, just to see the effect move):
    python tide_mark.py --demo --still still.png --out demo.mp4 --duration 8
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image


# ---------------------------------------------------------------------------
# boundary + effect (generic -- works for any episode, any still)
# ---------------------------------------------------------------------------

def _tide_boundary(w: int, h: int, height_frac: float, seed: int) -> np.ndarray:
    """1-D height field y(x) in pixels-from-top across the frame width: the
    wavering tide boundary. Sum of 3-4 seeded sines at different
    frequencies/phases + light gaussian smoothing -- never a straight line,
    never a gauge. Amplitude is modest (a stain edge, not an ocean wave)."""
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 1.0, w)
    base_y = h * (1.0 - max(0.0, min(1.0, height_frac)))

    n = int(rng.integers(3, 5))  # 3 or 4 components
    base_freqs = np.array([0.8, 1.9, 3.3, 4.7])[:n]
    freqs = base_freqs * rng.uniform(0.85, 1.15, size=n)
    phases = rng.uniform(0.0, 2 * np.pi, size=n)
    rel_amps = np.array([1.0, 0.55, 0.3, 0.18])[:n] * rng.uniform(0.8, 1.2, size=n)
    amps = rel_amps * (h * 0.009)  # tallest single component ~0.9% of frame height

    y = np.full(w, base_y, dtype=np.float64)
    for f, p, a in zip(freqs, phases, amps):
        y += a * np.sin(2 * np.pi * f * x + p)

    # light smoothing so the sum of sines reads as one soft undulating line,
    # not a visibly composited wave pattern
    sigma = max(3, w // 120)
    radius = sigma * 3
    kx = np.arange(-radius, radius + 1)
    kernel = np.exp(-(kx ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    y = np.convolve(y, kernel, mode="same")
    return y


def apply_tide_mark(frame: Image.Image, height_frac: float, seed: int = 7,
                     paper_mask: "np.ndarray | None" = None) -> Image.Image:
    """Apply the tide-mark to an already-composited RGB frame.

    height_frac: 0.0-1.0, fraction of the frame height the tide currently
    occupies, measured up from the bottom. 0.0 = dry page (frame returned
    unchanged).

    paper_mask: optional float array (H, W) in 0..1, 1 = paper/margin (safe
    to darken), 0 = drawn illustration (never darken). LIMITATION: without a
    real segmentation mask, the default (None) applies the effect wherever
    the boundary math says to, with no knowledge of what's paper vs drawing
    -- it is the CALLER's job to keep height_frac low enough (the Storm
    example curve below tops out at 0.18) that the boundary stays inside the
    still's own bottom paper margin. Pass a real paper_mask when a still's
    illustration bleeds all the way to the bottom edge (no safe margin) and
    the tide still needs to run.
    """
    w, h = frame.size
    height_frac = max(0.0, min(1.0, height_frac))
    if height_frac <= 0.0:
        return frame

    arr = np.asarray(frame.convert("RGB"), dtype=np.float32)
    y_boundary = _tide_boundary(w, h, height_frac, seed)          # (w,)
    yy = np.arange(h, dtype=np.float32)[:, None]                  # (h,1)
    dist = yy - y_boundary[None, :]                                # (h,w), +ve = below/wet

    # soak: smoothstep into the wet region over ~2px (the boundary itself
    # isn't a razor edge), flat multiply below it
    soak = np.clip(dist / 2.0, 0.0, 1.0)

    # ridge: the darkest line, feathered 4-8px, centered right at the
    # boundary -- classic stain physics, darkest exactly where the water
    # sat, not just a gradient fading from full-dark
    ridge_sigma = 2.6
    ridge = np.exp(-(dist ** 2) / (2 * ridge_sigma ** 2))

    BASE_MULT = 0.955      # 0.94-0.97 warm-brown multiply below the line
    RIDGE_STRENGTH = 0.10  # extra darkening right at the boundary

    mult = 1.0 - soak * (1.0 - BASE_MULT) - ridge * RIDGE_STRENGTH
    mult = np.clip(mult, 0.75, 1.0)

    if paper_mask is not None:
        pm = np.asarray(paper_mask, dtype=np.float32)
        if pm.shape != (h, w):
            pm = np.asarray(
                Image.fromarray((np.clip(pm, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.NEAREST),
                dtype=np.float32,
            ) / 255.0
        mult = 1.0 - (1.0 - mult) * pm
        soak = soak * pm

    # warm brown channel tint -- less blue/green than red, so soaked paper
    # reads warmer/heavier, not just darker. Scaled by `soak` (0 above the
    # boundary, ramping to 1 in the wet region) so dry paper above the tide
    # line is returned byte-identical -- this is a bottom-band-only effect,
    # never a global colour cast on the whole frame.
    tint = np.array([1.0, 0.965, 0.88], dtype=np.float32)
    channel_tint = 1.0 - soak[..., None] * (1.0 - tint[None, None, :])
    out = arr * (mult[..., None] * channel_tint)
    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


# ---------------------------------------------------------------------------
# example authored curve (Storm episode) -- NOT used by apply_tide_mark;
# this is reference for an assembly script to copy/adapt per episode
# ---------------------------------------------------------------------------

def _ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)  # smoothstep


def tide_height_curve(t: float) -> float:
    """Example keyframe curve for the Storm episode (Mark 4:35-41, calming of
    the storm), authored off the alignment word times. This is a REFERENCE
    an assembly script copies/adapts per episode -- apply_tide_mark() itself
    stays generic and only takes a plain height_frac.

    Beats (seconds, word-aligned):
      0.0   -> 6.7   rise: dry paper -> full-fear high-water (~0.18)
      6.7   -> 29.8  hold at 0.18 through "asleep" / "carest thou not" -- the
                      verse itself sits at ~23.55-27.43s inside this hold and
                      is DELIBERATELY not varied: the tide never editorialises
                      under Scripture, it just holds still and lets the words work
      29.8  -> 40.0  recede: 0.18 -> a faint PERMANENT ghost level (~0.02) --
                      paper that has been soaked never fully dries flat again
      40.0  -> 43.16 hold at the ghost level (~0.02)
      43.16 -> 44.36 SNAP back to the old high-water mark (~0.18) for ~1.2s --
                      the word "knees" recalls the fear at its highest, fast
                      not eased, because a memory returns all at once
      44.36 -> 49.0  fade out to 0 by the landing -- the mark itself resolves,
                      nothing rides under the closing image
      >= 49.0        0.0
    """
    GHOST = 0.02
    PEAK = 0.18
    if t <= 0.0:
        return 0.0
    if t < 6.7:
        return PEAK * _ease(t / 6.7)
    if t < 29.8:
        return PEAK
    if t < 40.0:
        u = (t - 29.8) / (40.0 - 29.8)
        return PEAK + (GHOST - PEAK) * _ease(u)
    if t < 43.16:
        return GHOST
    if t < 44.36:
        # fast snap up (not eased) over the first ~0.12s of this window, then hold
        u = (t - 43.16) / 0.12
        return GHOST + (PEAK - GHOST) * min(1.0, u)
    if t < 49.0:
        u = (t - 44.36) / (49.0 - 44.36)
        return PEAK * (1.0 - _ease(u))
    return 0.0


# ---------------------------------------------------------------------------
# demo CLI
# ---------------------------------------------------------------------------

def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _demo_curve(t: float, duration: float) -> float:
    """Simple demo rise-and-recede (0.0 -> 0.25 -> 0.03), NOT the Storm curve
    above -- just enough motion to see the effect animate."""
    half = duration / 2.0
    if t <= half:
        return 0.25 * _ease(t / half)
    u = (t - half) / (duration - half)
    return 0.25 + (0.03 - 0.25) * _ease(u)


def render_demo(still: Path, out_mp4: Path, duration: float, seed: int):
    im = Image.open(still).convert("RGB")
    im = scale_crop(im, 1080, 1920)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(round(duration * 30))
    for i in range(n_frames):
        t = i / 30.0
        hf = _demo_curve(t, duration)
        frame = apply_tide_mark(im, hf, seed=seed)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-framerate", "30", "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
        check=True, capture_output=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a rise-and-recede demo clip from one still")
    ap.add_argument("--still", help="source still (any resolution)")
    ap.add_argument("--out", help="output mp4")
    ap.add_argument("--duration", type=float, default=8.0, help="demo clip length, seconds")
    ap.add_argument("--seed", type=int, default=7, help="boundary seed")
    a = ap.parse_args()
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        render_demo(Path(a.still), Path(a.out), a.duration, a.seed)
    else:
        ap.error("only --demo is implemented from the CLI -- import apply_tide_mark/tide_height_curve for pipeline use")
