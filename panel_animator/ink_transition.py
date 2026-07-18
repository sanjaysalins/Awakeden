#!/usr/bin/env python
"""Ink-bleed / brush-wipe transition between two clips (or stills).

Instead of a hard cut or a generic crossfade, clip A is revealed-through by
clip B along an organic ink-spread edge (mode="blot", like ink dropped on wet
paper) or a directional brush-stroke sweep (mode="wipe"). $0, deterministic:
a precomputed noise "reveal field" thresholded per frame -> ffmpeg maskedmerge.

Usage:
    python ink_transition.py --a clipA.mp4 --b clipB.mp4 --out transition.mp4
        [--duration 0.9] [--mode blot|wipe] [--origin 0.3,0.6] [--fps 30]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1920, 1080


def make_reveal_field(mode: str, origin: tuple[float, float], seed: int = 7) -> np.ndarray:
    """0..1 field: low values reveal first, high values reveal last."""
    rng = np.random.default_rng(seed)
    field = np.zeros((H, W), dtype=float)
    for scale, weight in [(6, 1.0), (3, 0.55), (1.5, 0.28)]:
        small = rng.random((int(H / 40 * scale) + 2, int(W / 40 * scale) + 2))
        img = Image.fromarray((small * 255).astype("uint8")).resize((W, H), Image.BICUBIC)
        field += np.asarray(img, dtype=float) * weight
    field = (field - field.min()) / (field.max() - field.min())

    yy, xx = np.mgrid[0:H, 0:W]
    if mode == "blot":
        cx, cy = origin[0] * W, origin[1] * H
        dist = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H) ** 2)
    else:  # directional brush wipe, angled slightly off-horizontal
        dist = (xx / W) * 0.92 + (yy / H) * 0.08
    dist = (dist - dist.min()) / (dist.max() - dist.min())

    combined = 0.32 * field + 0.68 * dist
    return (combined - combined.min()) / (combined.max() - combined.min())


def render_mask_frames(field: np.ndarray, n_frames: int, edge: float, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for i in range(n_frames):
        t = i / max(1, n_frames - 1)
        # pixel shows B (white) once field <= t, soft ramp of width `edge`
        mask = np.clip((t - (field - edge)) / (2 * edge), 0, 1)
        Image.fromarray((mask * 255).astype("uint8"), "L").save(out_dir / f"m{i:04d}.png")


def _run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def render(a_clip: Path, b_clip: Path, out_mp4: Path, duration: float,
           mode: str, origin: tuple[float, float], fps: int):
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    a_seg, b_seg = work / "a_seg.mp4", work / "b_seg.mp4"
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    _run(["ffmpeg", "-y", "-sseof", f"-{duration:.3f}", "-i", str(a_clip),
          "-t", f"{duration:.3f}", "-vf", scale, "-r", str(fps),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(a_seg)])
    _run(["ffmpeg", "-y", "-i", str(b_clip), "-t", f"{duration:.3f}", "-vf", scale,
          "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(b_seg)])

    n_frames = int(duration * fps)
    field = make_reveal_field(mode, origin)
    mask_dir = work / "mask_frames"
    render_mask_frames(field, n_frames, edge=0.09, out_dir=mask_dir)
    mask_mp4 = work / "mask.mp4"
    _run(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(mask_dir / "m%04d.png"),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(mask_mp4)])

    _run(["ffmpeg", "-y", "-i", str(a_seg), "-i", str(b_seg), "-i", str(mask_mp4),
          "-filter_complex", "[0:v][1:v][2:v]maskedmerge",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)])
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=0.9)
    ap.add_argument("--mode", choices=["blot", "wipe"], default="blot")
    ap.add_argument("--origin", default="0.5,0.55")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    ox, oy = (float(v) for v in a.origin.split(","))
    render(Path(a.a), Path(a.b), Path(a.out), a.duration, a.mode, (ox, oy), a.fps)
