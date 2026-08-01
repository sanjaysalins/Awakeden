#!/usr/bin/env python
"""Frottage (the Rubbing) -- evidence taken by hand: when an episode turns on
an OBJECT (a coin, a seal, an inscription, a nail), the spread's object-insert
arrives as a graphite rubbing. Diagonal graphite strokes accumulate in hand
order (band by band, the way a wrist actually works) and the image emerges
UNDER them -- graphite-gray on paper, edges strong where the relief is, the
paper breathing through every stroke.

Round 5 ("the book itself", 2026-07-30). The reveal IS a documentary claim:
this was pressed against the real thing.

HARD GOVERNOR (stated before anything else): objects and inscriptions ONLY.
Never a figure, never a face, and absolutely never the Face -- a rubbing of
Christ's countenance is Veronica-relic territory. The device documents THINGS;
persons stay drawn. Also: <=1 rubbing per episode; the plate derives from an
already-approved still, never a fresh unaudited render; strokes never fully
opaque (cap 0.92).

$0 deterministic: plate = desaturate + graphite tone curve + Sobel edge boost
of an approved still; strokes = seeded soft bands in wrist order.

Usage:
    python frottage.py --demo --object obj.png --out demo.mp4 \
        [--duration 4] [--reveal-dur 2.2] [--angle-deg 38] [--seed 9]

    python frottage.py --selftest --object obj.png
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

FPS = 30
PAPER = np.array([230, 220, 194], dtype=np.float32)
GRAPHITE = np.array([58, 56, 58], dtype=np.float32)
OPACITY_CAP = 0.92  # paper always breathes through


def make_rubbing_plate(im: Image.Image) -> np.ndarray:
    """Graphite plate of an approved object still: luminance -> graphite tone
    curve (paper where light, graphite where dark), Sobel edge boost ~0.35 so
    relief edges catch the way a real rubbing catches them. Returns float
    (h, w, 3)."""
    gray = np.asarray(im.convert("L"), dtype=np.float32)
    lo, hi = np.percentile(gray, 2.0), np.percentile(gray, 98.0)
    g = np.clip((gray - lo) / max(1e-6, hi - lo), 0, 1)
    w = g ** 0.85  # 1 = paper, 0 = graphite

    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    edge = np.clip((gx + gy) / 80.0, 0, 1)
    edge = np.asarray(Image.fromarray((edge * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0
    w = np.clip(w - 0.35 * edge, 0, 1)

    return PAPER[None, None, :] * w[..., None] + GRAPHITE[None, None, :] * (1 - w[..., None])


def build_strokes(region: tuple[int, int, int, int], seed: int = 9,
                   angle_deg: float = 38.0) -> list[tuple[tuple[int, int, int, int], np.ndarray]]:
    """Seeded stroke bands in WRIST ORDER: rows top-to-bottom, each row swept
    left-to-right, every stroke jittered in angle/length/width so the order
    reads as a hand's progress, never a wipe. Returns [(bbox, soft mask)]."""
    x0, y0, x1, y1 = region
    rw = x1 - x0
    rng = random.Random(seed)
    strokes = []
    stroke_w = max(26, rw // 24)
    row_h = int(stroke_w * 1.35)
    s_len = max(120, int(rw * 0.34))

    y = y0 + row_h // 2
    row_i = 0
    while y < y1 + row_h // 2:
        x = x0 + int(rng.uniform(-0.06, 0.02) * rw)
        while x < x1:
            ang = math.radians(angle_deg + rng.uniform(-4, 4))
            ln = s_len * rng.uniform(0.8, 1.15)
            wd = stroke_w * rng.uniform(0.85, 1.2)
            cx = x + ln * 0.4
            cy = y + rng.uniform(-0.25, 0.25) * row_h
            dx, dy = math.cos(ang) * ln / 2, -math.sin(ang) * ln / 2

            pad = int(wd * 2)
            bx0 = int(min(cx - dx, cx + dx) - pad)
            by0 = int(min(cy - dy, cy + dy) - pad)
            bx1 = int(max(cx - dx, cx + dx) + pad)
            by1 = int(max(cy - dy, cy + dy) + pad)
            layer = Image.new("L", (bx1 - bx0, by1 - by0), 0)
            d = ImageDraw.Draw(layer)
            d.line([(cx - dx - bx0, cy - dy - by0), (cx + dx - bx0, cy + dy - by0)],
                   fill=255, width=int(wd))
            layer = layer.filter(ImageFilter.GaussianBlur(wd * 0.22))
            mask = np.asarray(layer, dtype=np.float32) / 255.0
            # per-stroke pressure unevenness (graphite is never flat)
            press = rng.uniform(0.75, 1.0)
            strokes.append(((bx0, by0, bx1, by1), mask * press))
            x += int(ln * rng.uniform(0.42, 0.6))
        row_i += 1
        y += row_h
    return strokes


class FrottageReveal:
    """Precomputed reveal: frame_at(t) composites base + plate through the
    accumulated stroke mask. Monotonic-t rendering keeps one running accum
    array (memory-light); call with strictly non-decreasing t."""

    def __init__(self, base: Image.Image, plate: np.ndarray,
                 region: tuple[int, int, int, int], t0: float, reveal_dur: float,
                 seed: int = 9, angle_deg: float = 38.0):
        self.base = np.asarray(base.convert("RGB"), dtype=np.float32)
        h, w = self.base.shape[:2]
        if plate.shape[:2] != (h, w):
            raise ValueError("plate must be pre-placed at frame size")
        self.plate = plate
        self.t0, self.dur = t0, reveal_dur
        self.strokes = build_strokes(region, seed, angle_deg)
        self.accum = np.zeros((h, w), dtype=np.float32)
        self._k_done = 0
        self._final = None

    def _advance(self, k: int):
        for i in range(self._k_done, k):
            (bx0, by0, bx1, by1), m = self.strokes[i]
            sl = self.accum[max(0, by0):by1, max(0, bx0):bx1]
            mm = m[max(0, by0) - by0:, max(0, bx0) - bx0:][:sl.shape[0], :sl.shape[1]]
            np.maximum(sl, mm, out=sl)
        self._k_done = max(self._k_done, k)

    def frame_at(self, t: float) -> Image.Image:
        n = len(self.strokes)
        p = (t - self.t0) / self.dur
        if p <= 0:
            return Image.fromarray(self.base.astype(np.uint8))
        if p >= 1.0 and self._final is not None:
            return self._final
        k_f = min(n, int(p * n) if p < 1.0 else n)
        self._advance(k_f)
        mask = self.accum
        if k_f < n:  # current stroke fading in
            frac = p * n - k_f
            (bx0, by0, bx1, by1), m = self.strokes[k_f]
            mask = self.accum.copy()
            sl = mask[max(0, by0):by1, max(0, bx0):bx1]
            mm = m[max(0, by0) - by0:, max(0, bx0) - bx0:][:sl.shape[0], :sl.shape[1]]
            np.maximum(sl, mm * frac, out=sl)
        m3 = (mask * OPACITY_CAP)[..., None]
        out = Image.fromarray(np.clip(self.base * (1 - m3) + self.plate * m3, 0, 255).astype(np.uint8))
        if p >= 1.0:
            self._final = out
        return out

    def coverage(self) -> float:
        """Fraction of the region currently under graphite (>0.3 mask)."""
        return float((self.accum > 0.3).mean())


def foley_cues(t0: float, reveal_dur: float) -> list[dict]:
    """Soft graphite scratch under the stroke window -- the desk's most
    tactile cue."""
    return [{"device": "graphite_scratch", "start": t0, "duration": reveal_dur}]


def make_paper_base(w: int = 1080, h: int = 1920, seed: int = 4) -> Image.Image:
    """The book's own cream page with a whisper of grain -- demo base."""
    nrng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), dtype=np.float32)
    base[..., 0], base[..., 1], base[..., 2] = (238, 226, 194)
    grain = nrng.standard_normal((h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 40 + 128, 0, 255).astype(np.uint8))
                        .filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float32) / 255.0 - 0.5
    base *= (1.0 + 0.05 * grain)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def place_plate(obj: Image.Image, frame_w: int, frame_h: int,
                 region: tuple[int, int, int, int]) -> np.ndarray:
    """Fit the object still into the region, plate it, embed at frame size
    (paper color elsewhere)."""
    x0, y0, x1, y1 = region
    rw, rh = x1 - x0, y1 - y0
    s = max(rw / obj.width, rh / obj.height)
    zw, zh = int(obj.width * s + 0.5), int(obj.height * s + 0.5)
    fit = obj.resize((zw, zh), Image.LANCZOS).crop(
        ((zw - rw) // 2, (zh - rh) // 2, (zw - rw) // 2 + rw, (zh - rh) // 2 + rh))
    plate_full = np.zeros((frame_h, frame_w, 3), dtype=np.float32)
    plate_full[..., :] = PAPER[None, None, :]
    plate_full[y0:y1, x0:x1] = make_rubbing_plate(fit)
    return plate_full


# ---------------------------------------------------------------- self-test

def selftest(obj_path: Path):
    obj = Image.open(obj_path).convert("RGB")
    region = (140, 620, 940, 1220)
    base = make_paper_base()
    plate = place_plate(obj, 1080, 1920, region)
    rev = FrottageReveal(base, plate, region, t0=0.5, reveal_dur=2.2, seed=9)

    f_pre = rev.frame_at(0.2)
    assert np.array_equal(np.asarray(f_pre), np.asarray(base)), "graphite on the page before the hand moved"

    covs, cents = [], []
    for p in (0.25, 0.5, 0.75, 1.0):
        rev.frame_at(0.5 + p * 2.2)
        covs.append(rev.coverage())
        ys, xs = np.where(rev.accum > 0.3)
        if len(ys):
            cents.append(float(ys.mean()))
    assert all(b >= a for a, b in zip(covs, covs[1:])), f"coverage not monotonic: {covs}"
    region_area = (region[3] - region[1]) * (region[2] - region[0]) / (1080 * 1920)
    assert covs[-1] > region_area * 0.92, f"final coverage too low: {covs[-1]:.3f} vs region {region_area:.3f}"
    assert cents[0] < cents[-1] - 50, f"no top-to-bottom hand order: centroids {cents}"
    mx = rev.accum.max() * OPACITY_CAP
    assert mx <= OPACITY_CAP + 1e-6, "opacity cap breached -- paper must breathe"
    print(f"[selftest] PASS -- monotonic {['%.2f' % c for c in covs]}, hand order top->bottom, cap {mx:.2f}")


# ---------------------------------------------------------------- demo

def render_demo(obj_path: Path, out_mp4: Path, duration: float, reveal_dur: float,
                angle_deg: float, seed: int, t0: float = 0.6):
    obj = Image.open(obj_path).convert("RGB")
    region = (140, 620, 940, 1220)
    base = make_paper_base()
    plate = place_plate(obj, 1080, 1920, region)
    rev = FrottageReveal(base, plate, region, t0=t0, reveal_dur=reveal_dur,
                          seed=seed, angle_deg=angle_deg)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(duration * FPS))
    for i in range(n):
        rev.frame_at(i / FPS).save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")
    print(f"[foley] cues: {foley_cues(t0, reveal_dur)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--object", required=True, help="approved OBJECT still (never a figure/face)")
    ap.add_argument("--out")
    ap.add_argument("--duration", type=float, default=4.0)
    ap.add_argument("--reveal-dur", type=float, default=2.2, dest="reveal_dur")
    ap.add_argument("--angle-deg", type=float, default=38.0, dest="angle_deg")
    ap.add_argument("--seed", type=int, default=9)
    a = ap.parse_args()

    if a.selftest:
        selftest(Path(a.object))
    elif a.demo:
        if not a.out:
            ap.error("--demo requires --out")
        render_demo(Path(a.object), Path(a.out), a.duration, a.reveal_dur, a.angle_deg, a.seed)
    else:
        ap.error("specify --demo or --selftest")
