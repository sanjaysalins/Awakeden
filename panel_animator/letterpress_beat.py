#!/usr/bin/env python
"""Letterpress Beat -- the page pressed in rhythm with the voice. Only the
INK pixels (a luminance mask -- the linework/shading, not the paper) darken
a few percent for a couple of frames on each real speech beat, then relax.
Paper tone never changes, so it can never read as a light pulse (that's the
spotlight family's language) -- it reads as the lines THEMSELVES responding,
kinetic-typography's core idea (a visual hit locked to speech timing)
applied to linework instead of type.

Beats are derived from this episode's own real forced-alignment word starts
(not a guessed metronome): consecutive word starts closer together than
`min_spacing` collapse into one beat, so the rhythm follows actual phrase
onsets rather than firing on every syllable.

No camera movement, no repaint -- a per-pixel luminance-masked darken +
tiny emboss offset, deterministic.

Usage:
    python letterpress_beat.py --still still.png --out clip.mp4 \\
        --duration 7.9 --align _alignment.json --window-start 269.4
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FPS = 30
DARKEN_K = 0.10       # peak ink-darkening fraction at a beat
PULSE_DUR = 0.16      # seconds for a beat to decay away
MIN_SPACING = 0.6     # seconds -- collapse word starts closer than this into one beat


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def beats_in_window(words: list[dict], win_start: float, win_end: float, min_spacing: float) -> list[float]:
    starts = sorted(w["start"] for w in words if win_start <= w["start"] < win_end)
    beats = []
    for s in starts:
        if not beats or (s - beats[-1]) >= min_spacing:
            beats.append(s)
    return [b - win_start for b in beats]  # local time within the hold


def render(still: Path, out_mp4: Path, duration: float, beats_local: list[float],
           w: int = 1920, h: int = 1080):
    base = _scale_crop(Image.open(still).convert("RGB"), w, h)
    src = np.asarray(base, dtype=np.float32)
    gray = np.asarray(base.convert("L"), dtype=np.float32) / 255.0
    ink_mask = np.clip(1.0 - gray, 0.0, 1.0) ** 1.3  # darker pixels = more "ink"

    n = max(1, int(round(duration * FPS)))
    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i in range(n):
        t = i / FPS
        pulse = 0.0
        for b in beats_local:
            dt = t - b
            if 0 <= dt < PULSE_DUR:
                pulse = max(pulse, (1.0 - dt / PULSE_DUR))
        darken = DARKEN_K * pulse
        frame = src * (1.0 - darken * ink_mask[..., None])
        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}  ({len(beats_local)} beats)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--align", required=True)
    ap.add_argument("--window-start", type=float, required=True, dest="window_start")
    a = ap.parse_args()
    words = json.loads(Path(a.align).read_text(encoding="utf-8"))
    beats = beats_in_window(words, a.window_start, a.window_start + a.duration, MIN_SPACING)
    render(Path(a.still), Path(a.out), a.duration, beats)
