#!/usr/bin/env python
"""Candle-Only Spread -- the light budget (Round 6 promotion, panel-revised
2026-07-30, `poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md` build card 5).
Promotes the radial grade (warm inside / cold-dark outside, soft 260px
falloff, flicker jitter on R) from
`poc_living_sketchbook/storm/_vault2_poc/_build_vault2.py::poc_candle`.

GOVERNORS (episode-design rules, not enforced by this module):
  - Anchor MUST be a drawn light source already present in the approved still
    (the lamp, a fire, a torch) -- the desk's lamp answering the page's lamp.
    This function has no idea what's actually lit in the art; it only knows
    where you tell it the light is. Candle anchors are AUTHORED per-spread
    pixel coordinates from the still-QC pass (the approved POC's
    `LAMP = (0.295W, 0.495H)` pattern), never auto-detected.
  - R(t) is energy-driven inverse: fear closes the light down, the turn opens
    it. This module only draws the radius it's given -- the caller authors
    the curve (see `radius_from_keyframes()` / `flicker_R()` helpers below).
  - <=1 spread per episode; never the landing spread (the torn page owns
    landing light); the light source must survive the still's own QC first.

WARM/COLD constants and the falloff shape are preserved EXACTLY from the
approved POC -- do not retune without a fresh taste gate.

API:
    from candle_only import apply_candle, radius_from_keyframes, flicker_R

    LAMP = (int(W * 0.295), int(H * 0.495))
    base_curve = lambda t: radius_from_keyframes(
        [(0.0, 3000.0), (2.4, 330.0), (5.2, 330.0), (6.8, 950.0)], t)
    R = flicker_R(base_curve, seed=51, amplitude=10.0)   # flicker only matters where base_curve is flat
    frame = apply_candle(frame, t, LAMP, R)

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\candle_only.py --demo --still <still.png> --anchor-frac 0.295,0.495 --out demo.mp4
    .venv\\Scripts\\python.exe panel_animator\\candle_only.py --selftest
"""
from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate

FPS = 30
W, H = 1080, 1920

FALLOFF_PX = 260.0                          # soft edge width, px -- preserved from the POC
WARM = np.array([1.08, 1.00, 0.88], np.float32)   # preserved exactly
COLD = np.array([0.82, 0.87, 1.00], np.float32)   # preserved exactly
COLD_GAIN = 0.16                            # preserved exactly
GLOW_GAIN = 0.10                            # preserved exactly


def _smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def radius_from_keyframes(keyframes: list[tuple[float, float]], t: float) -> float:
    """Piecewise smootherstep-eased R(t) from a sorted [(t0, R0), (t1, R1),
    ...] list -- generalizes the approved POC's hand-written 4-phase R_of()
    (hold / ease-down / flicker-flat / ease-up). Holds the first/last radius
    outside the given time range."""
    if not keyframes:
        raise ValueError("radius_from_keyframes needs at least one keyframe")
    if t <= keyframes[0][0]:
        return keyframes[0][1]
    if t >= keyframes[-1][0]:
        return keyframes[-1][1]
    for (ta, ra), (tb, rb) in zip(keyframes, keyframes[1:]):
        if ta <= t <= tb:
            u = _smootherstep((t - ta) / max(1e-6, tb - ta))
            return ra + (rb - ra) * u
    return keyframes[-1][1]


def flicker_R(base_curve, seed: int = 51, amplitude: float = 10.0, n_samples: int = 400):
    """Wrap a base R(t) curve with the approved POC's deterministic flicker:
    two interleaved seeded-random tables sampled at 12Hz/5Hz and averaged,
    scaled by `amplitude` (POC value: +-10px). Returns a callable R(t)."""
    rng = random.Random(seed)
    flick = [rng.uniform(-1, 1) for _ in range(n_samples)]

    def R(t):
        f = flick[int(t * 12) % n_samples] * 0.5 + flick[int(t * 5) % n_samples] * 0.5
        return base_curve(t) + amplitude * f

    return R


def apply_candle(frame: Image.Image, t: float, anchor_xy, R_of_t,
                  falloff_px: float = FALLOFF_PX) -> Image.Image:
    """Radial light budget: warm gain within radius R(t) of `anchor_xy`,
    cold-dark falloff outside it, soft `falloff_px` edge, a glow bump right
    at the anchor. Unchanged math from the approved POC
    (`_vault2_poc/_build_vault2.py::poc_candle`), generalized off a caller-
    supplied anchor + radius function instead of a hardcoded still/curve.

    R_of_t: either a plain callable `R(t) -> float` (px), or a
        `[(t0, R0), (t1, R1), ...]` keyframe list (passed straight to
        `radius_from_keyframes`).
    """
    R = float(R_of_t(t)) if callable(R_of_t) else radius_from_keyframes(R_of_t, t)
    frame_rgb = frame.convert("RGB")
    w, h = frame_rgb.size
    arr = np.asarray(frame_rgb, np.float32)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    ax, ay = anchor_xy
    dist = np.sqrt((xs - ax) ** 2 + (ys - ay) ** 2)
    lit = np.clip((R - dist) / falloff_px + 0.5, 0, 1)
    glow = np.clip(1.0 - dist / max(R, 1.0), 0, 1) ** 2
    gain = (COLD[None, None, :] * COLD_GAIN) * (1 - lit[..., None]) \
        + (WARM[None, None, :] * (1.0 + GLOW_GAIN * glow[..., None])) * lit[..., None]
    out = np.clip(arr * gain, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


# ---------------------------------------------------------------------- demo


def _render(name: str, frame_fn, dur: float, outdir: Path):
    work = outdir / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = outdir / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def render_demo(still: Path, out_mp4: Path, anchor_frac: tuple[float, float], duration: float):
    base = scale_crop(Image.open(still).convert("RGB"), W, H)
    anchor = (W * anchor_frac[0], H * anchor_frac[1])
    base_curve = lambda t: radius_from_keyframes(
        [(0.0, 3000.0), (2.4, 330.0), (5.2, 330.0), (6.8, 950.0)], t)
    R = flicker_R(base_curve, seed=51, amplitude=10.0)
    _render(out_mp4.stem, lambda t: apply_candle(base, t, anchor, R), duration, out_mp4.parent)


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    # 1. constants preserved exactly
    check(FALLOFF_PX == 260.0, f"FALLOFF_PX preserved at 260px, got {FALLOFF_PX}")
    check(np.allclose(WARM, [1.08, 1.00, 0.88]), f"WARM preserved: {WARM}")
    check(np.allclose(COLD, [0.82, 0.87, 1.00]), f"COLD preserved: {COLD}")

    # 2. radius_from_keyframes holds outside range, interpolates inside
    kf = [(0.0, 100.0), (2.0, 300.0)]
    check(radius_from_keyframes(kf, -5.0) == 100.0, "R(t) holds first keyframe before range")
    check(radius_from_keyframes(kf, 50.0) == 300.0, "R(t) holds last keyframe after range")
    mid = radius_from_keyframes(kf, 1.0)
    check(100.0 < mid < 300.0, f"R(1.0) interpolates between keyframes: {mid}")

    # 3. apply_candle: the anchor is lit (bright, warm-toned: R>B); far away is
    # dark and cold-toned (B>R) -- the whole point of the light BUDGET
    base = Image.new("RGB", (W, H), (150, 150, 150))
    anchor = (int(W * 0.3), int(H * 0.5))
    near = apply_candle(base, 0.0, anchor, lambda t: 50.0)
    arr = np.asarray(near, np.float32)
    at_anchor = arr[anchor[1], anchor[0]]
    far_pt = arr[50, 50]
    check(at_anchor.sum() > far_pt.sum(),
          f"anchor is much brighter than far away: at_anchor={at_anchor} (sum {at_anchor.sum():.0f}), "
          f"far={far_pt} (sum {far_pt.sum():.0f})")
    check(at_anchor[0] > at_anchor[2] and far_pt[2] > far_pt[0],
          f"anchor reads warm (R>B), far away reads cold (B>R): at_anchor={at_anchor}, far={far_pt}")

    # 4. flicker_R is deterministic (same seed -> same samples) and stays near the base curve
    base_curve = lambda t: 300.0
    R1 = flicker_R(base_curve, seed=51, amplitude=10.0)
    R2 = flicker_R(base_curve, seed=51, amplitude=10.0)
    samples_equal = all(abs(R1(t) - R2(t)) < 1e-9 for t in [0.1, 1.3, 4.7])
    check(samples_equal, "flicker_R is deterministic for a fixed seed")
    check(all(abs(R1(t) - 300.0) <= 10.0 + 1e-6 for t in [0.1, 1.3, 4.7]),
          "flicker stays within +-amplitude of the base curve")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip from a still")
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--anchor-frac", default="0.295,0.495",
                     help="anchor as W_frac,H_frac (--demo mode), default matches the approved POC's lamp")
    ap.add_argument("--duration", type=float, default=7.5, help="--demo clip length, seconds")
    ap.add_argument("--selftest", action="store_true", help="run the engine self-tests")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        fx, fy = (float(v) for v in a.anchor_frac.split(","))
        render_demo(Path(a.still), Path(a.out), (fx, fy), a.duration)
    else:
        ap.print_help()
