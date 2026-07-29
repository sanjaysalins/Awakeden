#!/usr/bin/env python
"""Damp cockle -- paper that has been wet cockles: it waves and buckles, and
under a raking light the crests catch and the troughs shadow. This is a
spatially-varying per-pixel warp (a low-frequency 2-D displacement field,
cv2.remap'd through the frame) plus a shading term derived from the field's
own gradient, so crests brighten and troughs darken slightly. This is what
sells it as damp PAPER rather than a wobbly video.

Distinct from line_boil.py: line-boil is a WHOLE-FRAME rigid affine jitter
(every pixel moves together, like a hand-held camera on stable art). Damp
cockle moves different parts of the frame by different amounts at different
times -- the top-left can crest while the bottom-right troughs.

$0, deterministic numpy + cv2.remap (falls back to nothing else needed --
cv2 is already a project dependency) + ffmpeg encode.

Usage:
    # apply to an already-rendered clip
    python damp_cockle.py --clip clip.mp4 --out clip_cockle.mp4 [--amplitude 1.0]

    # render a demo clip straight from a still (constant full amplitude)
    python damp_cockle.py --demo --still still.png --out demo.mp4 --duration 8
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

FPS = 30

# --- displacement field tuning ---------------------------------------------
AMP_PX = 5.0        # base full-strength warp amplitude in px (brief: +/-3-6px)
FX = 2.0            # cycles of the x-displacement sine across the frame width
FY = 1.7            # cycles of the y-displacement sine across the frame height
DRIFT_HZ = 0.15     # base drift speed of the field (~0.15Hz per the brief)
PHASE_X = 0.4
PHASE_Y = 2.1
SHADE_K = 0.03      # shading strength -> ~2-4% brightness swing at crests/troughs


def apply_damp_cockle(frame: Image.Image, t: float, amplitude: float = 1.0) -> Image.Image:
    """Warp one already-composited RGB frame through a slow, spatially-varying
    paper-cockle displacement field, then re-light it so crests/troughs read
    as raised, damp paper rather than a geometric wobble.

    frame: PIL Image, any size (designed for 1080x1920 composited frames)
    t: seconds -- drives the phase of the drifting sine fields
    amplitude: 0.0 = no effect (frame returned unchanged), 1.0 = full
        +/-3-6px warp. Use this to taper a per-episode curve (full during a
        storm, tapering out toward a calm landing).
    """
    if amplitude <= 0.0:
        return frame

    arr = np.asarray(frame.convert("RGB"), dtype=np.float32)
    h, w = arr.shape[:2]

    amp_px = AMP_PX * amplitude

    xs = np.arange(w, dtype=np.float32)
    ys = np.arange(h, dtype=np.float32)

    # dx varies along x only, dy varies along y only -- summed through remap
    # they still produce a genuine 2-D cockle (a wave crest can sit anywhere
    # on the sheet, not just move the whole frame together).
    dx_row = amp_px * np.sin(2 * np.pi * (xs / w * FX + t * DRIFT_HZ) + PHASE_X)              # (w,)
    dy_col = amp_px * np.sin(2 * np.pi * (ys / h * FY + t * DRIFT_HZ * 1.3) + PHASE_Y)         # (h,)

    map_x = np.tile((xs + dx_row)[np.newaxis, :], (h, 1)).astype(np.float32)
    map_y = np.tile((ys + dy_col)[:, np.newaxis], (1, w)).astype(np.float32)

    warped = cv2.remap(arr, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    # Shading: crests (steepest part of the field) catch raking light, troughs
    # shadow. Use the derivative of each 1-D sine w.r.t. its own axis,
    # normalized to [-1, 1] so SHADE_K directly controls the brightness swing
    # -- the raw pixel-space derivative is far too small (scales with 1/w) to
    # be visible on its own.
    grad_x = np.gradient(dx_row)
    grad_x = grad_x / (np.max(np.abs(grad_x)) + 1e-9)
    grad_y = np.gradient(dy_col)
    grad_y = grad_y / (np.max(np.abs(grad_y)) + 1e-9)

    # Each axis contributes at half weight so the combined x+y shading lands
    # in the target 2-4% swing (SHADE_K), not 2x that from simply summing
    # two independently-normalized [-1, 1] terms.
    shade = 1.0 + 0.5 * SHADE_K * amplitude * (grad_x[np.newaxis, :] + grad_y[:, np.newaxis])
    shade = np.clip(shade, 1.0 - SHADE_K, 1.0 + SHADE_K)[:, :, np.newaxis]

    warped = np.clip(warped * shade, 0, 255).astype(np.uint8)
    return Image.fromarray(warped)


def scale_crop(im, w, h):
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


def render_demo(still: Path, out_mp4: Path, duration: float):
    im = Image.open(still).convert("RGB")
    im = scale_crop(im, 1080, 1920)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(duration * FPS)
    for i in range(n_frames):
        t = i / FPS
        frame = apply_damp_cockle(im, t=t, amplitude=1.0)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


def render_clip(clip: Path, out_mp4: Path, amplitude: float):
    w, h, fps = _probe(clip)
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    subprocess.run(["ffmpeg", "-y", "-i", str(clip), str(work / "f%05d.png")],
                    check=True, capture_output=True)
    frames = sorted(work.glob("f*.png"))

    for i, fp in enumerate(frames):
        t = i / fps
        im = Image.open(fp).convert("RGB")
        warped = apply_damp_cockle(im, t=t, amplitude=amplitude)
        warped.save(fp)

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
    ap.add_argument("--amplitude", type=float, default=1.0,
                     help="warp strength multiplier, 0=off 1=full +/-3-6px (--clip mode)")
    a = ap.parse_args()

    if a.demo:
        if not a.still:
            ap.error("--demo requires --still")
        render_demo(Path(a.still), Path(a.out), a.duration)
    elif a.clip:
        render_clip(Path(a.clip), Path(a.out), a.amplitude)
    else:
        ap.error("specify --demo --still <png> or --clip <mp4>")
