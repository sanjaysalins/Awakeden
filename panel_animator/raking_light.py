#!/usr/bin/env python
"""Raking light -- makes the style's existing "soft raking museum light" MOVE:
a broad, slow directional grazing sweep across the sheet that catches the
paper tooth, deepens the shadow inside any torn edge, and -- on one beat
only -- passes across the gold-leaf strip so it flares, the way real leaf
does when the light finds it.

Technical approach ($0, deterministic):
  1. High-pass the still's own luminance (gray - gaussian_blur(gray)) to
     approximate paper tooth -- no normal map needed. The torn-edge shadows
     and ink-stroke ridges the artwork already has fall right out of this.
  2. Per frame, modulate brightness by 1 + k*tooth*falloff(sweep_progress),
     where falloff is a wide soft Gaussian band translating across the frame.
  3. Gold flare: isolate the leaf strip by hue/saturation/value, and when the
     sweep band overlaps it, add a short warm specular bump + a slight bloom.

Distinct from damp_cockle.py (a spatial WARP + gradient-shading) and from
line_boil.py (a whole-frame rigid jitter) -- this is a pure per-pixel
brightness relight, no geometry moves.

Usage:
    # demo straight from a still
    python raking_light.py --demo --still still.png --out demo.mp4 \
        --duration 8 [--flare] [--k 0.03]

    # apply to an already-rendered clip (recomputes nothing per-frame beyond
    # the brightness modulation; tooth/gold_mask are sampled once from the
    # first frame, tuned for this project's near-static "frozen tableau" clips)
    python raking_light.py --clip clip.mp4 --out clip_raking.mp4 [--flare]
"""
from __future__ import annotations
import argparse
import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

FPS = 30

# --- gold-leaf isolation thresholds -----------------------------------------
# Calibrated against this project's actual rendered gold-leaf strip (PIL HSV
# 0-255 scale): the leaf is a genuinely more saturated/brighter warm-gold than
# any sepia skin/cloth/wood tone the style otherwise uses, even though all of
# them share a similar hue. Verified zero false positives on skin/robe regions
# of the test still at these thresholds -- do not loosen without re-checking
# against a real still (a loose hue-only window pulls in half the artwork).
GOLD_HUE_MIN, GOLD_HUE_MAX = 5, 32
GOLD_SAT_MIN, GOLD_VAL_MIN = 160, 130


def paper_tooth_highpass(frame: Image.Image, blur_radius: int = 20) -> np.ndarray:
    """Approximate paper tooth/grain by high-pass filtering the still's own
    luminance: gray - gaussian_blur(gray, blur_radius). This also naturally
    picks up ink-stroke ridges and the shadow just inside a torn edge -- real
    texture already drawn into the artwork, not a synthetic normal map.

    Returns a float array (frame.height, frame.width) normalized to roughly
    -1..1 via the 99th percentile of |diff| (robust to a still's own overall
    contrast, so the same blur_radius works across different pieces).
    """
    gray_img = frame.convert("L")
    blurred_img = gray_img.filter(ImageFilter.GaussianBlur(blur_radius))
    gray = np.asarray(gray_img, dtype=np.float32)
    blurred = np.asarray(blurred_img, dtype=np.float32)
    diff = gray - blurred
    scale = float(np.percentile(np.abs(diff), 99.0))
    if scale < 1e-6:
        return np.zeros_like(diff)
    return np.clip(diff / scale, -1.0, 1.0)


def _sweep_band(w: int, h: int, sweep_progress: float, band_width_px: float, angle_deg: float) -> np.ndarray:
    """A wide soft Gaussian band, several hundred px wide, translating across
    the frame as sweep_progress goes 0->1. angle_deg tilts the direction of
    travel slightly off pure horizontal so it reads as a real light raking
    across a page rather than a video wipe."""
    ys, xs = np.mgrid[0:h, 0:w]
    xs = xs.astype(np.float32)
    ys = ys.astype(np.float32)
    angle = math.radians(angle_deg)
    dx, dy = math.cos(angle), math.sin(angle)
    proj = xs * dx + ys * dy
    proj_min, proj_max = float(proj.min()), float(proj.max())
    center = proj_min + sweep_progress * (proj_max - proj_min)
    sigma = max(band_width_px / 2.3548, 1.0)  # band_width_px = FWHM
    return np.exp(-0.5 * ((proj - center) / sigma) ** 2)


def apply_raking_light(
    frame: Image.Image,
    sweep_progress: float,
    tooth: np.ndarray | None = None,
    k: float = 0.03,
    band_width_px: float = 550.0,
    angle_deg: float = 15.0,
) -> Image.Image:
    """Modulate brightness by 1 + k*tooth*falloff(sweep_progress, pixel_pos)
    so only a moving band of the frame brightens/deepens at any moment.

    sweep_progress: 0.0-1.0, position of the light sweep across the frame.
    tooth: reuse a precomputed paper_tooth_highpass() map (recommended when
        calling this every frame on the SAME still) -- computed fresh if None.
    k: modulation strength. Keep small (0.02-0.05) -- see the skill's locked
        lessons; this is a lamp finding texture, not a video filter.
    """
    frame_rgb = frame.convert("RGB")
    w, h = frame_rgb.size
    if tooth is None:
        tooth = paper_tooth_highpass(frame_rgb)
    band = _sweep_band(w, h, sweep_progress, band_width_px, angle_deg)
    modulation = 1.0 + k * tooth * band
    arr = np.asarray(frame_rgb, dtype=np.float32)
    out = np.clip(arr * modulation[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


def isolate_gold_leaf(frame: Image.Image) -> np.ndarray:
    """HSV hue/saturation/value band mask isolating the warm gold-leaf strip
    this style always paints along one edge. Returns a boolean array
    (frame.height, frame.width)."""
    hsv = np.asarray(frame.convert("HSV"), dtype=np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return (h >= GOLD_HUE_MIN) & (h <= GOLD_HUE_MAX) & (s >= GOLD_SAT_MIN) & (v >= GOLD_VAL_MIN)


def apply_gold_flare(
    frame: Image.Image,
    sweep_progress: float,
    gold_mask: np.ndarray | None = None,
    intensity: float = 1.0,
    band_width_px: float = 550.0,
    angle_deg: float = 15.0,
    boost: float = 0.55,
    bloom_radius: int = 24,
) -> Image.Image:
    """When the sweep overlaps the gold-leaf mask, add a short warm specular
    bump + slight bloom, scaled by how centered the sweep currently is on the
    strip and by intensity. Outside that overlap window this is a no-op --
    call it every frame, it only ever fires once per sweep pass.

    Pass the SAME band_width_px/angle_deg used for apply_raking_light so the
    flare travels with the same sweep, not a second independent light.
    """
    frame_rgb = frame.convert("RGB")
    w, h = frame_rgb.size
    if gold_mask is None:
        gold_mask = isolate_gold_leaf(frame_rgb)
    mask_f = gold_mask.astype(np.float32)
    mask_sum = float(mask_f.sum())
    if mask_sum < 1.0:
        return frame_rgb  # no gold strip found in this still -- no-op

    band = _sweep_band(w, h, sweep_progress, band_width_px, angle_deg)
    overlap = float((band * mask_f).sum() / mask_sum)  # mean band value AT the gold pixels, 0..1
    if overlap < 0.05:
        return frame_rgb  # sweep nowhere near the strip this frame -- no effect at all

    arr = np.asarray(frame_rgb, dtype=np.float32)
    warm = np.array([255, 235, 170], dtype=np.float32)  # warm gold-white specular color

    # localized specular bump: strongest where the band is brightest AND the
    # pixel is gold -- this makes the highlight slide along the strip's own
    # length as the sweep crosses it, not flash the whole strip at once.
    bump = boost * intensity * overlap * band * mask_f
    specular = bump[..., None] * warm[None, None, :]

    # slight bloom: blur the bump map and add a soft warm glow around it
    bloom_src = Image.fromarray(np.clip(bump * 255.0, 0, 255).astype(np.uint8))
    bloom = np.asarray(bloom_src.filter(ImageFilter.GaussianBlur(bloom_radius)), dtype=np.float32) / 255.0
    glow = bloom[..., None] * warm[None, None, :] * 0.5

    out = np.clip(arr + specular + glow, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")


def scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


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


def render_demo(still: Path, out_mp4: Path, duration: float, flare: bool, k: float, intensity: float,
                 band_width_px: float, angle_deg: float):
    im = Image.open(still).convert("RGB")
    frame0 = scale_crop(im, 1080, 1920)
    tooth = paper_tooth_highpass(frame0)
    gold_mask = isolate_gold_leaf(frame0) if flare else None

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = max(1, int(duration * FPS))
    for i in range(n_frames):
        progress = i / max(1, n_frames - 1)
        frame = apply_raking_light(frame0, progress, tooth=tooth, k=k,
                                    band_width_px=band_width_px, angle_deg=angle_deg)
        if flare:
            frame = apply_gold_flare(frame, progress, gold_mask=gold_mask, intensity=intensity,
                                      band_width_px=band_width_px, angle_deg=angle_deg)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


def render_clip(clip: Path, out_mp4: Path, flare: bool, k: float, intensity: float,
                 band_width_px: float, angle_deg: float):
    w, h, fps = _probe(clip)
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    subprocess.run(["ffmpeg", "-y", "-i", str(clip), str(work / "f%05d.png")],
                    check=True, capture_output=True)
    frames = sorted(work.glob("f*.png"))
    n = len(frames)

    tooth = None
    gold_mask = None
    for i, fp in enumerate(frames):
        progress = i / max(1, n - 1)
        im = Image.open(fp).convert("RGB")
        if tooth is None:
            tooth = paper_tooth_highpass(im)
            if flare:
                gold_mask = isolate_gold_leaf(im)
        frame = apply_raking_light(im, progress, tooth=tooth, k=k,
                                    band_width_px=band_width_px, angle_deg=angle_deg)
        if flare:
            frame = apply_gold_flare(frame, progress, gold_mask=gold_mask, intensity=intensity,
                                      band_width_px=band_width_px, angle_deg=angle_deg)
        frame.save(fp)

    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
                    "-i", str(clip), "-map", "0:v", "-map", "1:a?",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
                    "-shortest", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip from a single still")
    ap.add_argument("--clip", help="apply to an already-rendered clip")
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=8.0, help="--demo mode clip length in seconds")
    ap.add_argument("--flare", action="store_true", help="also render the gold-leaf flare beat")
    ap.add_argument("--k", type=float, default=0.03, help="raking-light modulation strength (0.02-0.05)")
    ap.add_argument("--intensity", type=float, default=1.0, help="gold-flare intensity multiplier")
    ap.add_argument("--band-width-px", type=float, default=550.0, dest="band_width_px",
                     help="FWHM of the sweep band in px")
    ap.add_argument("--angle-deg", type=float, default=15.0, dest="angle_deg",
                     help="sweep travel direction, degrees off horizontal")
    a = ap.parse_args()

    if a.demo:
        if not a.still:
            ap.error("--demo requires --still")
        render_demo(Path(a.still), Path(a.out), a.duration, a.flare, a.k, a.intensity,
                    a.band_width_px, a.angle_deg)
    elif a.clip:
        render_clip(Path(a.clip), Path(a.out), a.flare, a.k, a.intensity,
                    a.band_width_px, a.angle_deg)
    else:
        ap.error("specify --demo --still <png> or --clip <mp4>")
