#!/usr/bin/env python
"""Registration Snap -- a motion-design (not paper-physics) hold treatment.
The page sits slightly "out of register" the way an early print pull does
(red/blue channels a couple px apart, a faint halftone screen sitting over
the art), then at one keyed moment in the hold the channels ease into
perfect register (with a tiny overshoot) and the halftone thins toward
nothing -- the print becomes quietly sharper. A discrete rhythmic EVENT,
not a continuous effect, which is what distinguishes this from the
light/paper-physics family already built.

No camera movement, no crop/zoom/pan -- purely a per-pixel channel-shift +
halftone-opacity animation, full frame throughout. Reuses print_grade.py's
halftone screen generator (its own dot-density alpha channel, not a color
value) so the "print" vocabulary matches what print_grade already applies as
a static finishing pass elsewhere in the project.

Usage:
    python registration_snap.py --still still.png --out clip.mp4 --duration 7.3 [--snap-frac 0.55]
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
from print_grade import make_halftone_screen  # noqa: E402

FPS = 30


def _ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _shift_channel(chan: np.ndarray, dx: float) -> np.ndarray:
    """Sub-pixel-ish horizontal shift via nearest-int roll (amplitude is only
    a few px, so a plain roll reads as a clean fringe without needing
    interpolation); wrap-around is imperceptible at this amplitude on a
    full-bleed illustration."""
    d = int(round(dx))
    if d == 0:
        return chan
    return np.roll(chan, d, axis=1)


def render(still: Path, out_mp4: Path, duration: float, w: int = 1920, h: int = 1080,
           snap_frac: float = 0.55, baseline_px: float = 2.4, overshoot_px: float = 0.7,
           ease_dur: float = 0.6, halftone_baseline: float = 0.11, halftone_settled: float = 0.02):
    base = _scale_crop(Image.open(still).convert("RGB"), w, h)
    arr = np.asarray(base, dtype=np.float32)
    screen = make_halftone_screen(w, h)
    dot_alpha = np.asarray(screen.split()[-1], dtype=np.float32) / 255.0  # dot-density map

    snap_t = duration * snap_frac
    n = max(1, int(round(duration * FPS)))
    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i in range(n):
        t = i / FPS
        if t < snap_t - ease_dur:
            dx, screen_op, pop = baseline_px, halftone_baseline, 0.0
        elif t < snap_t:
            p = _ease((t - (snap_t - ease_dur)) / ease_dur)
            dx = baseline_px * (1.0 - p)
            screen_op = halftone_baseline + (halftone_settled - halftone_baseline) * p
            pop = 0.0
        else:
            p2 = min(1.0, (t - snap_t) / 0.35)
            dx = -overshoot_px * np.sin(np.pi * p2) * np.exp(-3.5 * p2)
            screen_op = halftone_settled
            pop = 0.06 * np.exp(-8.0 * p2)  # brief contrast/brightness pop right at the snap

        frame = arr.copy()
        frame[..., 0] = _shift_channel(arr[..., 0], dx)
        frame[..., 2] = _shift_channel(arr[..., 2], -dx)
        frame *= (1.0 - screen_op * dot_alpha * 0.9)[..., None]
        if pop > 0:
            frame = frame * (1.0 + pop) - 127.5 * pop  # tiny contrast pop, centered

        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}  (snap at {snap_t:.2f}s of {duration:.2f}s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--snap-frac", type=float, default=0.55, dest="snap_frac")
    a = ap.parse_args()
    render(Path(a.still), Path(a.out), a.duration, snap_frac=a.snap_frac)
