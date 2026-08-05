#!/usr/bin/env python
"""Unseen Hand -- a near-invisible page-turn transition. A soft shadow (as if
someone were turning a page just above the lamp, out of frame) sweeps across
the spread; the paper gives a faint shiver as it's handled; the hard cut from
clip A to clip B happens hidden inside the darkest instant of the shadow, so
the viewer never consciously registers a transition device at all -- just a
brief dimming and a shiver, then the new page is there.

Distinct from ink_transition.py (a visible ink-bleed reveal edge): this is
meant to be the workhorse default for ordinary cuts, not a moment that draws
attention to itself.

$0, deterministic: reuses raking_light._sweep_band() for the shadow's shape
(inverted -- darkens instead of brightens) and damp_cockle.apply_damp_cockle()
for the paper shiver, both already-approved modules. No new visual language,
just a new combination.

Usage:
    python unseen_hand.py --a clipA.mp4 --b clipB.mp4 --out transition.mp4 [--duration 0.7]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from raking_light import _sweep_band  # noqa: E402
from damp_cockle import apply_damp_cockle  # noqa: E402

W, H, FPS = 1920, 1080, 30
SHADOW_K = 0.55       # peak darkening (1.0 - SHADOW_K = darkest brightness multiplier)
COCKLE_AMP = 0.6      # peak damp-cockle amplitude during the shiver
BAND_WIDTH_PX = 1400.0  # wide/soft -- reads as an even shadow, not a visible edge
ANGLE_DEG = 12.0


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def _extract_frames(clip: Path, out_dir: Path, seek_from_end: float | None, dur: float, w: int, h: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y"]
    if seek_from_end is not None:
        cmd += ["-sseof", f"-{seek_from_end:.3f}"]
    cmd += ["-i", str(clip), "-t", f"{dur:.3f}",
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
            "-r", str(FPS), str(out_dir / "f%04d.png")]
    _run(cmd)
    return sorted(out_dir.glob("f*.png"))


def render(a_clip: Path, b_clip: Path, out_mp4: Path, duration: float = 0.7,
           w: int = W, h: int = H, shadow_k: float = SHADOW_K, cockle_amp: float = COCKLE_AMP):
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    half = duration / 2.0
    a_frames = _extract_frames(a_clip, work / "a", half, half, w, h)
    b_frames = _extract_frames(b_clip, work / "b", None, half, w, h)
    n = len(a_frames) + len(b_frames)

    out_dir = work / "out"
    out_dir.mkdir()
    for i in range(n):
        t = i / FPS
        e = max(0.0, np.sin(np.pi * min(t, duration) / duration))  # 0 -> 1 -> 0
        src_frames, idx = (a_frames, i) if i < len(a_frames) else (b_frames, i - len(a_frames))
        frame = Image.open(src_frames[idx]).convert("RGB")
        frame = apply_damp_cockle(frame, t, amplitude=cockle_amp * e)
        band = _sweep_band(w, h, t / duration, BAND_WIDTH_PX, ANGLE_DEG)
        modulation = 1.0 - shadow_k * e * (0.55 + 0.45 * band)  # mostly-uniform dim + a soft directional bias
        arr = np.asarray(frame, dtype=np.float32) * modulation[..., None]
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(out_dir / f"o{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_dir / "o%04d.png"),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)])
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=0.7)
    a = ap.parse_args()
    render(Path(a.a), Path(a.b), Path(a.out), a.duration)
