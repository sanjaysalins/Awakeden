#!/usr/bin/env python
"""Ribbon Marker -- the CTA in the book's own language: at the landing, after
the last spoken word, a narrow woven ribbon (rubric red, frayed tip) slips
down from the top edge and settles across the margin of the landing spread --
the way a reader marks the page they intend to return to. One soft cloth
settle, one contact shadow, then ABSOLUTE stillness: after settle the
composite is byte-identical every frame (asserted, not hoped).

Round 5 ("the book itself", 2026-07-30). Blue-line's ink-arrival opens every
episode; the ribbon closes it -- matching bookends, the pen and the ribbon.

Laws (SKILL.md): landing spread only, once per episode by definition; rubric
red ONLY (gold is His glory -- the ribbon is the READER'S object); a fixed
margin lane, series-constant, never crossing the torn hole / Christ figure /
lettering; the settle completes within ~0.6s of the last word, BEFORE the
INV-26 stillness clock runs; then zero motion. Timing vs. the sacred-stillness
law is a USER A/B decision -- this engine only makes the candidate.

$0 deterministic: the ribbon texture is generated (seeded weave + selvedge +
sheen + frayed tip); bank a photographed/rendered silk later ONLY if the user
judges this one insufficient by eye.

Usage:
    python ribbon_marker.py --demo --still landing.png --out demo.mp4 \
        [--x-frac 0.77] [--length-frac 0.33] [--settle-at 1.0] [--duration 5]

    python ribbon_marker.py --selftest
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
from PIL import Image, ImageFilter

from raking_light import scale_crop

FPS = 30
RIBBON_RED = (152, 28, 24)
SETTLE_DUR = 0.6          # drop 0.4s + bounce tail; byte-stable after this
BOUNCE_PX = 6.0           # micro-bounce amplitude -- an object with mass, not a tween


def make_ribbon_texture(width_px: int = 34, length_px: int = 700, seed: int = 3) -> Image.Image:
    """Woven silk ribbon RGBA, hanging vertically: fine warp/weft luminance
    weave, darker wobbled selvedge edges, a lengthwise sheen band that drifts
    (silk catching light), and a frayed tip -- individual thread strands past
    a ragged cut."""
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    w, h = width_px, length_px
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)

    base = np.zeros((h, w, 3), dtype=np.float32)
    base[..., 0], base[..., 1], base[..., 2] = RIBBON_RED

    # weave: warp threads (vertical) + weft picks (horizontal), both subtle
    warp = 0.06 * np.sin(2 * math.pi * xs / 3.4 + 0.7 * np.sin(ys / 90))
    weft = 0.045 * np.sin(2 * math.pi * ys / 5.2)
    base *= (1.0 + warp + weft)[..., None]

    # cylindrical shading: darker at the selvedges
    edge = np.sin(math.pi * (xs + 0.5) / w)
    base *= (0.78 + 0.22 * edge)[..., None]

    # sheen: a soft lengthwise highlight whose center drifts along the length
    sheen_c = w * (0.5 + 0.18 * np.sin(2 * math.pi * ys / (h * 0.9) + 1.1))
    sheen = np.exp(-0.5 * ((xs - sheen_c) / (w * 0.16)) ** 2)
    base += 46.0 * sheen[..., None] * np.array([1.0, 0.75, 0.7])[None, None, :]

    # slight lengthwise unevenness (dye + age)
    unev = np.asarray(Image.fromarray(
        np.clip(nrng.standard_normal((h // 24 + 2, 1)) * 30 + 128, 0, 255).astype(np.uint8)
    ).resize((1, h), Image.BICUBIC), dtype=np.float32).reshape(h, 1) / 255.0 - 0.5
    base *= (1.0 + 0.07 * unev)[..., None]

    alpha = np.full((h, w), 255.0, dtype=np.float32)

    # selvedge wobble: edges are woven, not die-cut
    for y in range(h):
        lw = 1.0 + 0.8 * math.sin(2 * math.pi * y / 37) + rng.uniform(-0.4, 0.4)
        rw = 1.0 + 0.8 * math.sin(2 * math.pi * y / 41 + 2.0) + rng.uniform(-0.4, 0.4)
        alpha[y, :max(0, int(lw))] = 0
        if int(rw) > 0:
            alpha[y, w - int(rw):] = 0

    # frayed tip: ragged cut line, then loose thread strands
    fray_top = h - int(width_px * 0.9)
    cut = np.array([fray_top + rng.uniform(0, width_px * 0.35) for _ in range(w)])
    cut = np.convolve(cut, np.ones(5) / 5, mode="same")
    for x in range(w):
        alpha[int(cut[x]):, x] = 0
    n_strands = max(4, w // 5)
    for _ in range(n_strands):
        sx = rng.randint(1, w - 2)
        s_len = rng.uniform(0.25, 1.0) * (h - cut[sx])
        y0, y1 = int(cut[sx]), min(h, int(cut[sx] + s_len))
        drift = rng.uniform(-2.5, 2.5)
        for yy in range(y0, y1):
            xx = int(sx + drift * (yy - y0) / max(1, y1 - y0))
            if 0 <= xx < w:
                alpha[yy, xx] = 235
                base[yy, xx] = [c * 0.92 for c in RIBBON_RED]

    out = np.dstack([np.clip(base, 0, 255), np.clip(alpha, 0, 255)]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def _settle_curve(tt: float) -> float:
    """0..1 drop progress: smootherstep over 0.4s, then a decaying micro-
    bounce (fixed BOUNCE_PX amplitude, NOT proportional to travel). Returns
    the vertical offset FROM final rest in pixels (>=0 above rest is negative
    ... we return offset_px where 0 = at rest, positive = still above)."""
    if tt <= 0:
        return 1e9  # fully parked off-frame before the cue
    if tt < 0.4:
        p = tt / 0.4
        s = p * p * p * (p * (p * 6 - 15) + 10)
        return (1.0 - s)  # fraction of travel remaining
    return 0.0


def _bounce_px(tt: float) -> float:
    """Micro-bounce below rest after touchdown at t=0.4, decayed by ~0.2s."""
    if tt < 0.4:
        return 0.0
    b = tt - 0.4
    return float(BOUNCE_PX * math.exp(-b / 0.055) * abs(math.sin(2 * math.pi * b / 0.11)))


def _sway_ribbon(ribbon: np.ndarray, t_rel: float) -> np.ndarray:
    """Lateral cloth sway while dropping: the lower part lags, decaying to
    zero by the end of the settle. cv2.remap horizontal shear per row."""
    if t_rel >= SETTLE_DUR:
        return ribbon
    h, w = ribbon.shape[:2]
    decay = max(0.0, 1.0 - t_rel / SETTLE_DUR)
    amp = 7.0 * decay
    rows = np.arange(h, dtype=np.float32) / max(1, h - 1)
    x_off = amp * np.sin(math.pi * rows) * math.sin(2 * math.pi * t_rel / 0.5)
    map_x = np.tile(np.arange(w, dtype=np.float32), (h, 1)) - x_off[:, None]
    map_y = np.tile(np.arange(h, dtype=np.float32)[:, None], (1, w))
    return cv2.remap(ribbon, map_x, map_y, cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def apply_ribbon(
    frame: Image.Image,
    t: float,
    settle_at: float,
    ribbon: Image.Image,
    x_frac: float = 0.77,
    top_overhang_px: int = 24,
) -> Image.Image:
    """Composite the ribbon at its lane. Before settle_at: no ribbon. During
    [settle_at, settle_at+0.6]: drop + sway + micro-bounce. After: BYTE-STABLE
    (the caller may cache; the function itself is deterministic in t and
    clamps all motion to zero)."""
    out = frame.convert("RGBA")
    W, H = out.size
    t_rel = t - settle_at
    if t_rel < 0:
        return out.convert("RGB")
    t_rel = min(t_rel, SETTLE_DUR)  # clamp: after settle everything is constant

    rib = np.asarray(ribbon, dtype=np.uint8).copy()
    rib = _sway_ribbon(rib, t_rel)
    rib_img = Image.fromarray(rib, "RGBA")
    rw, rh = rib_img.size

    travel = rh + top_overhang_px
    rest_y = -top_overhang_px
    frac_remaining = _settle_curve(t_rel)
    y = int(rest_y - min(frac_remaining, 1.0) * travel + _bounce_px(t_rel))
    x = int(x_frac * W - rw / 2)

    # contact shadow: tightens as the silk meets the page
    p = min(1.0, t_rel / 0.4)
    sh_blur = 9 - 4 * p
    sh_dx, sh_dy = int(6 - 3 * p), int(8 - 4 * p)
    sil = rib_img.split()[3].point(lambda a: min(a, 80))
    shadow = Image.new("RGBA", (rw, rh), (30, 20, 14, 0))
    shadow.putalpha(sil)
    shadow = shadow.filter(ImageFilter.GaussianBlur(sh_blur))
    out.alpha_composite(shadow, (x + sh_dx, y + sh_dy))
    out.alpha_composite(rib_img, (x, y))
    return out.convert("RGB")


def foley_cues(settle_at: float) -> list[dict]:
    """One soft fabric slip, the book's goodbye."""
    return [{"device": "fabric_slip", "start": settle_at, "duration": 0.5}]


# ---------------------------------------------------------------- self-test

def selftest():
    ribbon = make_ribbon_texture(34, 700, seed=3)
    assert ribbon.mode == "RGBA" and ribbon.size == (34, 700)
    a = np.asarray(ribbon.split()[3])
    assert (a[:500] > 200).mean() > 0.75, "ribbon body should be mostly solid"
    assert (a[-20:] > 200).mean() < 0.35, "tip should be frayed, not solid"

    base = Image.new("RGB", (1080, 1920), (238, 226, 194))
    pre = apply_ribbon(base, 0.5, 1.0, ribbon)
    assert np.array_equal(np.asarray(pre), np.asarray(base)), "ribbon visible before its cue"
    f_a = apply_ribbon(base, 1.7, 1.0, ribbon)
    f_b = apply_ribbon(base, 4.9, 1.0, ribbon)
    assert np.array_equal(np.asarray(f_a), np.asarray(f_b)), "NOT byte-stable after settle -- stillness law broken"
    assert not np.array_equal(np.asarray(f_a), np.asarray(base)), "ribbon never arrived"
    # overshoot bounded: never travels more than BOUNCE_PX below rest
    assert max(_bounce_px(0.4 + i * 0.01) for i in range(30)) <= BOUNCE_PX + 0.01
    assert foley_cues(1.0) == [{"device": "fabric_slip", "start": 1.0, "duration": 0.5}]
    print("[selftest] PASS -- frayed, punctual, byte-still after the settle")


# ---------------------------------------------------------------- demo

def render_demo(still: Path, out_mp4: Path, x_frac: float, length_frac: float,
                settle_at: float, duration: float, seed: int):
    im = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    ribbon = make_ribbon_texture(34, int(1920 * length_frac), seed=seed)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(duration * FPS))
    stable = None
    for i in range(n):
        t = i / FPS
        if t >= settle_at + SETTLE_DUR and stable is not None:
            frame = stable
        else:
            frame = apply_ribbon(im, t, settle_at, ribbon, x_frac=x_frac)
            if t >= settle_at + SETTLE_DUR:
                stable = frame
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")
    print(f"[foley] cues: {foley_cues(settle_at)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--still")
    ap.add_argument("--out")
    ap.add_argument("--x-frac", type=float, default=0.77, dest="x_frac",
                     help="lane center; series-constant, never over hole/figure/lettering")
    ap.add_argument("--length-frac", type=float, default=0.33, dest="length_frac")
    ap.add_argument("--settle-at", type=float, default=1.0, dest="settle_at")
    ap.add_argument("--duration", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=3)
    a = ap.parse_args()

    if a.selftest:
        selftest()
    elif a.demo:
        if not (a.still and a.out):
            ap.error("--demo requires --still and --out")
        render_demo(Path(a.still), Path(a.out), a.x_frac, a.length_frac,
                    a.settle_at, a.duration, a.seed)
    else:
        ap.error("specify --demo or --selftest")
