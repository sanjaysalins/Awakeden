#!/usr/bin/env python
"""Papermaker's Mark -- a watermark IN the paper: a wire-form line device (the
ichthys) that is INVISIBLE at rest and appears only while raking-light's sweep
crosses it -- the paper thins where the wire pressed, the lamp finds it, the
strokes glow faintly lighter, the sweep moves on. The mark was in the paper
before anything was drawn on it.

Round 5 ("the book itself", 2026-07-30). Deliberately has NO reveal mechanism
of its own: visibility is the raking-light sweep band evaluated at the mark's
pixels -- no sweep, no mark, mathematically zero at rest. Call it every frame
in the SAME pass as apply_raking_light with the SAME sweep/band/angle values
so there is exactly one lamp.

Technical approach ($0, deterministic):
  1. make_ichthys_mask() draws the two-arc wire fish (two quadratic beziers
     crossing at the tail, extended to the fin tips) with the house seeded
     hand-wobble, then Gaussian-softens it -- even the wire is hand-bent.
  2. place_mark() embeds that mask into a full-frame float map at a chosen
     blank-margin position.
  3. apply_papermakers_mark() lightens frame pixels by
     1 + strength * mark_mask * sweep_band(sweep_progress) -- the identical
     _sweep_band as raking_light, imported, never re-implemented.

Governors (SKILL.md): <=1 reveal per episode; blank margin only; never during
the KJV verse hold; strength capped ~0.12; the symbol is series-constant and
a USER decision (ichthys default, plain cross alternative).

Usage:
    # demo: raking light + mark together on one still
    python papermakers_mark.py --demo --still still.png --out demo.mp4 \
        --duration 8 [--center 0.42,0.93] [--mark-width-frac 0.20] [--strength 0.10]

    # self-test (no files written)
    python papermakers_mark.py --selftest --still still.png
"""
from __future__ import annotations
import argparse
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from raking_light import _sweep_band, apply_raking_light, paper_tooth_highpass, scale_crop

FPS = 30
STRENGTH_CAP = 0.12  # governor: a whisper, not an effect
ENV_FLOOR = 0.10     # band values below this contribute EXACTLY zero -- a wide
                     # Gaussian's tail never truly leaves a 1080px frame, and
                     # "invisible at rest" must be mathematically true, not
                     # approximately true (found on the s04 re-placement)


def _wobble_polyline(points: list[tuple[float, float]], rng, amp: float = 1.6) -> list[tuple[float, float]]:
    """Smooth seeded hand-wobble: cumulative small jitter, low-pass filtered,
    so the wire bends like a hand bent it -- never per-point static."""
    n = len(points)
    jx = np.cumsum(np.array([rng.uniform(-1, 1) for _ in range(n)])) * 0.35
    jy = np.cumsum(np.array([rng.uniform(-1, 1) for _ in range(n)])) * 0.35
    # low-pass by simple box smoothing, keep amplitude bounded
    k = 5
    jx = np.convolve(jx, np.ones(k) / k, mode="same")
    jy = np.convolve(jy, np.ones(k) / k, mode="same")
    jx = np.clip(jx - jx.mean(), -amp, amp)
    jy = np.clip(jy - jy.mean(), -amp, amp)
    return [(x + float(dx), y + float(dy)) for (x, y), dx, dy in zip(points, jx, jy)]


def _bezier_stroke(n0: tuple[float, float], c: tuple[float, float], t1: tuple[float, float],
                    u_max: float, n_pts: int = 60) -> list[tuple[float, float]]:
    """Quadratic bezier N->T with control C, sampled on u in [0, u_max]
    (u_max > 1 extends past the tail crossing to the fin tip)."""
    pts = []
    for i in range(n_pts):
        u = u_max * i / (n_pts - 1)
        x = (1 - u) ** 2 * n0[0] + 2 * u * (1 - u) * c[0] + u ** 2 * t1[0]
        y = (1 - u) ** 2 * n0[1] + 2 * u * (1 - u) * c[1] + u ** 2 * t1[1]
        pts.append((x, y))
    return pts


def make_ichthys_mask(mark_w: int, seed: int = 5, stroke_frac: float = 0.022,
                       blur_frac: float = 0.012) -> np.ndarray:
    """The two-stroke wire fish, nose left, tail-cross right, fins past the
    cross. Returns a float mask (h, w) in 0..1, Gaussian-softened. Height is
    ~0.46 of width (the classic proportion)."""
    import random
    rng = random.Random(seed)
    mark_h = int(mark_w * 0.46)
    pad = int(mark_w * 0.10)
    W, H = mark_w + 2 * pad, mark_h + 2 * pad
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)

    L = mark_w * 0.82          # nose -> tail-cross distance
    A = mark_h * 0.78          # arc bow amplitude
    nose = (pad, pad + mark_h / 2)
    tail = (pad + L, pad + mark_h / 2)
    stroke_w = max(2, int(mark_w * stroke_frac))

    for sign in (-1, +1):      # upper wire, lower wire
        ctrl = (pad + L * 0.5, pad + mark_h / 2 + sign * A)
        pts = _bezier_stroke(nose, ctrl, tail, u_max=1.28)
        pts = _wobble_polyline(pts, rng, amp=max(1.2, mark_w * 0.006))
        d.line(pts, fill=255, width=stroke_w, joint="curve")

    blur = max(1.0, mark_w * blur_frac)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(layer, dtype=np.float32) / 255.0


def make_cross_mask(mark_w: int, seed: int = 5, stroke_frac: float = 0.028,
                     blur_frac: float = 0.012) -> np.ndarray:
    """The plain-cross alternative (user decides the series symbol once).
    Latin cross proportions, same hand-bent wire treatment."""
    import random
    rng = random.Random(seed)
    mark_h = int(mark_w * 1.45)
    pad = int(mark_w * 0.12)
    W, H = mark_w + 2 * pad, mark_h + 2 * pad
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    stroke_w = max(2, int(mark_w * stroke_frac))

    cx = pad + mark_w / 2
    beam_y = pad + mark_h * 0.32
    vert = [(cx, pad), (cx, pad + mark_h)]
    horiz = [(pad, beam_y), (pad + mark_w, beam_y)]
    for seg in (vert, horiz):
        n = 40
        pts = [(seg[0][0] + (seg[1][0] - seg[0][0]) * i / (n - 1),
                seg[0][1] + (seg[1][1] - seg[0][1]) * i / (n - 1)) for i in range(n)]
        pts = _wobble_polyline(pts, rng, amp=max(1.2, mark_w * 0.007))
        d.line(pts, fill=255, width=stroke_w, joint="curve")

    blur = max(1.0, mark_w * blur_frac)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(layer, dtype=np.float32) / 255.0


def place_mark(frame_w: int, frame_h: int, mark: np.ndarray,
                center_frac: tuple[float, float]) -> np.ndarray:
    """Embed a mark mask into a full-frame float map at center_frac (x, y)."""
    full = np.zeros((frame_h, frame_w), dtype=np.float32)
    mh, mw = mark.shape
    cx, cy = int(center_frac[0] * frame_w), int(center_frac[1] * frame_h)
    x0, y0 = cx - mw // 2, cy - mh // 2
    xs0, ys0 = max(0, x0), max(0, y0)
    xs1, ys1 = min(frame_w, x0 + mw), min(frame_h, y0 + mh)
    if xs1 <= xs0 or ys1 <= ys0:
        raise ValueError("mark placed entirely outside the frame")
    full[ys0:ys1, xs0:xs1] = mark[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    return full


def apply_papermakers_mark(
    frame: Image.Image,
    sweep_progress: float,
    mark_full: np.ndarray,
    strength: float = 0.10,
    band_width_px: float = 550.0,
    angle_deg: float = 15.0,
) -> Image.Image:
    """Lighten the paper along the wire strokes, scaled by the SAME sweep band
    raking_light uses -- pass identical band_width_px/angle_deg so the mark is
    found by the one lamp, not lit by a second. Zero effect when the sweep is
    elsewhere; call it every frame without gating."""
    strength = min(strength, STRENGTH_CAP)
    frame_rgb = frame.convert("RGB")
    w, h = frame_rgb.size
    if mark_full.shape != (h, w):
        raise ValueError(f"mark_full shape {mark_full.shape} != frame {(h, w)}")
    band = _sweep_band(w, h, sweep_progress, band_width_px, angle_deg)
    env = np.clip((band - ENV_FLOOR) / (1.0 - ENV_FLOOR), 0.0, 1.0)
    modulation = 1.0 + strength * mark_full * env
    arr = np.asarray(frame_rgb, dtype=np.float32)
    out = np.clip(arr * modulation[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


# ---------------------------------------------------------------- self-test

def selftest(still: Path, center=(0.42, 0.93), mark_width_frac=0.20, strength=0.10):
    """Three frames: sweep far before / sweep on the mark / sweep far past.
    The mark region must be untouched in 1 and 3, visibly lightened in 2."""
    im = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    mark = make_ichthys_mask(int(1080 * mark_width_frac))
    full = place_mark(1080, 1920, mark, center)

    # sweep progress that centers the band on the mark (project the mark
    # center onto the sweep axis, same math as _sweep_band)
    angle = math.radians(15.0)
    dx, dy = math.cos(angle), math.sin(angle)
    ys, xs = np.mgrid[0:1920, 0:1080]
    proj = xs * dx + ys * dy
    cx, cy = center[0] * 1080, center[1] * 1920
    on_mark = float((cx * dx + cy * dy - proj.min()) / (proj.max() - proj.min()))

    base = np.asarray(im, dtype=np.float32)
    ysld, xsld = np.where(full > 0.05)
    bbox = (ysld.min(), ysld.max(), xsld.min(), xsld.max())

    def mark_delta(p):
        out = np.asarray(apply_papermakers_mark(im, p, full, strength=strength), dtype=np.float32)
        return float(np.abs(out - base)[bbox[0]:bbox[1], bbox[2]:bbox[3]].mean())

    # probe "elsewhere" at >=3.2 sigma from the mark IN PROJECTION SPACE --
    # a hardcoded p=0.02/0.98 can sit inside the band's Gaussian tail when the
    # mark lies far along the sweep axis (found on the s04 re-placement).
    sigma_frac = (550.0 / 2.3548) / float(proj.max() - proj.min())
    p_before = max(0.0, on_mark - 3.2 * sigma_frac)
    p_after = min(1.0, on_mark + 3.2 * sigma_frac)
    d_before, d_on, d_after = mark_delta(p_before), mark_delta(on_mark), mark_delta(p_after)
    print(f"[selftest] mark-region mean |delta|: before={d_before:.3f} on={d_on:.3f} after={d_after:.3f}")
    assert d_before < 0.05, f"mark visible before the sweep arrives ({d_before:.3f})"
    assert d_after < 0.05, f"mark visible after the sweep passed ({d_after:.3f})"
    assert d_on > 1.0, f"mark not visible at sweep peak ({d_on:.3f})"
    print("[selftest] PASS -- invisible at rest, found by the lamp, released")


# ---------------------------------------------------------------- demo

def render_demo(still: Path, out_mp4: Path, duration: float, center, mark_width_frac,
                strength, k, band_width_px, angle_deg, symbol: str):
    im = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    tooth = paper_tooth_highpass(im)
    maker = make_cross_mask if symbol == "cross" else make_ichthys_mask
    mark = maker(int(1080 * mark_width_frac))
    full = place_mark(1080, 1920, mark, center)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(duration * FPS))
    for i in range(n):
        p = i / max(1, n - 1)
        frame = apply_raking_light(im, p, tooth=tooth, k=k,
                                    band_width_px=band_width_px, angle_deg=angle_deg)
        frame = apply_papermakers_mark(frame, p, full, strength=strength,
                                        band_width_px=band_width_px, angle_deg=angle_deg)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--still", required=True)
    ap.add_argument("--out")
    ap.add_argument("--duration", type=float, default=8.0)
    ap.add_argument("--center", default="0.42,0.93", help="mark center as x_frac,y_frac (blank margin!)")
    ap.add_argument("--mark-width-frac", type=float, default=0.20, dest="mark_width_frac")
    ap.add_argument("--strength", type=float, default=0.10, help=f"lighten strength, capped {STRENGTH_CAP}")
    ap.add_argument("--k", type=float, default=0.03, help="raking-light strength for the demo pass")
    ap.add_argument("--band-width-px", type=float, default=550.0, dest="band_width_px")
    ap.add_argument("--angle-deg", type=float, default=15.0, dest="angle_deg")
    ap.add_argument("--symbol", choices=["ichthys", "cross"], default="ichthys")
    a = ap.parse_args()
    center = tuple(float(v) for v in a.center.split(","))

    if a.selftest:
        selftest(Path(a.still), center=center, mark_width_frac=a.mark_width_frac, strength=a.strength)
    elif a.demo:
        if not a.out:
            ap.error("--demo requires --out")
        render_demo(Path(a.still), Path(a.out), a.duration, center, a.mark_width_frac,
                    a.strength, a.k, a.band_width_px, a.angle_deg, a.symbol)
    else:
        ap.error("specify --demo or --selftest")
