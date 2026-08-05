#!/usr/bin/env python
"""Tipped-In Plate -- the incoming scene arrives as a physical sheet being
laid onto the desk over the outgoing page: clip B's own opening frames, cut
with a deckle edge, drop in at ~103.5% scale and a slight rotation with a
loose blurred shadow beneath, and settle over ~0.6s (scale to 100%, rotation
to 0, shadow tightening to nothing) until they exactly fill the frame and B's
live motion just continues. Reads as "here is the next drawing" -- suits
cuts that introduce a new location or subject.

Generalizes elder_leaf.py's proven settle mechanics (apply_elder_leaf: scale
1.035->1.0, tightening contact shadow, smootherstep easing) from a small
tipped-in leaf to a full-frame plate. Same $0 deterministic technique, no new
visual language.

Usage:
    python tipped_in_plate.py --a clipA.mp4 --b clipB.mp4 --out transition.mp4 [--duration 0.6]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elder_leaf import _deckle_mask, smootherstep  # noqa: E402

W, H, FPS = 1920, 1080, 30
# NOTE: elder_leaf's own settle uses 1.035 (a SMALL leaf shrinking slightly
# onto a big page -- barely perceptible is correct there). Generalized to a
# FULL-FRAME plate, a 3.5% oversize is imperceptible (it's already covering
# ~97% of frame from t=0) and reads as a hard cut, not an arrival -- caught
# by eye-check, not assumed. Starting visibly SMALLER (backdrop showing at
# the edges) and growing to exactly fill the frame gives a real, legible
# "the sheet drops onto the desk" read.
START_SCALE = 0.90
START_ANGLE = 1.6


def _run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def _extract_frames(clip: Path, out_dir: Path, n: int, w: int, h: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    _run(["ffmpeg", "-y", "-i", str(clip), "-frames:v", str(n),
          "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
          "-r", str(FPS), str(out_dir / "f%04d.png")])
    return sorted(out_dir.glob("f*.png"))


def _extract_last_frame(clip: Path, dest: Path, w: int, h: int):
    _run(["ffmpeg", "-y", "-sseof", "-0.1", "-i", str(clip), "-frames:v", "1",
          "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", str(dest)])


def render(a_clip: Path, b_clip: Path, out_mp4: Path, duration: float = 0.6,
           w: int = W, h: int = H):
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(round(duration * FPS)))
    b_frames = _extract_frames(b_clip, work / "b", n, w, h)
    a_last_png = work / "a_last.png"
    _extract_last_frame(a_clip, a_last_png, w, h)
    backdrop = np.asarray(Image.open(a_last_png).convert("RGB"), dtype=np.float32)

    deckle = _deckle_mask(w, h, rng_seed=41, rough_px=9.0)  # full-frame deckle alpha

    out_dir = work / "out"
    out_dir.mkdir()
    for i in range(n):
        t = i / FPS
        p = smootherstep(t / duration)
        scale = START_SCALE - (START_SCALE - 1.0) * p
        angle = START_ANGLE * (1.0 - p)

        plate = Image.open(b_frames[i]).convert("RGBA")
        plate.putalpha(deckle)
        sw, sh = int(w * scale), int(h * scale)
        plate = plate.resize((sw, sh), Image.LANCZOS).rotate(angle, expand=True, resample=Image.BICUBIC)

        canvas = Image.fromarray(np.clip(backdrop, 0, 255).astype(np.uint8)).convert("RGBA")
        cx, cy = w // 2, h // 2
        x0, y0 = cx - plate.width // 2, cy - plate.height // 2

        sh_blur = 22 - 16 * p
        sh_dx, sh_dy = int(12 - 9 * p), int(16 - 11 * p)
        sh_alpha = int(75 + 25 * p)
        sil = plate.split()[3].point(lambda a: min(a, sh_alpha))
        shadow = Image.new("RGBA", plate.size, (25, 18, 12, 0))
        shadow.putalpha(sil)
        shadow = shadow.filter(ImageFilter.GaussianBlur(sh_blur))
        canvas.alpha_composite(shadow, (x0 + sh_dx, y0 + sh_dy))
        canvas.alpha_composite(plate, (x0, y0))

        canvas.convert("RGB").save(out_dir / f"o{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_dir / "o%04d.png"),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)])
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=0.6)
    a = ap.parse_args()
    render(Path(a.a), Path(a.b), Path(a.out), a.duration)
