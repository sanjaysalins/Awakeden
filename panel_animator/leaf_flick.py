#!/usr/bin/env python
"""Leaf-Flick -- a fast, unmistakable page-turn transition. A blank strip of
paper (the verso of a leaf being turned) whips across the frame in ~0.3s.
Ahead of it, the outgoing scene; in its wake, the incoming scene is already
lying there. A soft drop-shadow rides just ahead of the strip's leading edge
-- that shadow is what sells it as a physical sheet passing over the desk,
not a video wipe.

Reuses elder_leaf.make_elder_stock()'s deckle-edged paper-stock generator
(cream tone override, not the aged/foxed one) for the strip texture -- same
$0 deterministic mottled-paper technique, no new texture engine.

Usage:
    python leaf_flick.py --a clipA.mp4 --b clipB.mp4 --out transition.mp4 [--duration 0.32]
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
import elder_leaf  # noqa: E402

W, H, FPS = 1920, 1080, 30
STRIP_FRAC = 0.22   # strip width as a fraction of frame width
CREAM_STOCK = (238, 229, 205)  # plain page-verso tone (not the aged/foxed elder register)


def _run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def _make_strip(strip_w: int, h: int) -> Image.Image:
    old_base = elder_leaf.STOCK_BASE
    elder_leaf.STOCK_BASE = CREAM_STOCK
    try:
        stock = elder_leaf.make_elder_stock(strip_w, h, seed=31)
    finally:
        elder_leaf.STOCK_BASE = old_base
    return stock


def _extract_single_frame(clip: Path, dest: Path, from_end: bool, w: int, h: int):
    cmd = ["ffmpeg", "-y"]
    if from_end:
        cmd += ["-sseof", "-0.1"]
    cmd += ["-i", str(clip), "-frames:v", "1",
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
            str(dest)]
    _run(cmd)


def render(a_clip: Path, b_clip: Path, out_mp4: Path, duration: float = 0.32,
           w: int = W, h: int = H, direction: str = "rtl"):
    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    a_png, b_png = work / "a.png", work / "b.png"
    _extract_single_frame(a_clip, a_png, True, w, h)
    _extract_single_frame(b_clip, b_png, False, w, h)
    a_arr = np.asarray(Image.open(a_png).convert("RGB"), dtype=np.float32)
    b_arr = np.asarray(Image.open(b_png).convert("RGB"), dtype=np.float32)

    strip_w = int(w * STRIP_FRAC)
    strip = _make_strip(strip_w, h)
    strip_rgb = np.asarray(strip.convert("RGB"), dtype=np.float32)
    strip_alpha = (np.asarray(strip.split()[-1], dtype=np.float32) / 255.0)[..., None]

    n = max(1, int(round(duration * FPS)))
    travel = w + strip_w  # strip fully off-screen at both ends of its travel
    xs = np.arange(w, dtype=np.float32)

    out_dir = work / "out"
    out_dir.mkdir()
    for i in range(n):
        frac = i / max(1, n - 1)
        if direction == "rtl":
            center = (w + strip_w / 2) - frac * travel   # right -> left
        else:
            center = -strip_w / 2 + frac * travel          # left -> right

        left_edge, right_edge = center - strip_w / 2, center + strip_w / 2
        # "ahead" = not yet reached by the strip = still shows A (the outgoing
        # scene); "behind" = already passed = B (incoming) already lying there.
        ahead_mask = (xs < left_edge) if direction == "rtl" else (xs > right_edge)
        frame = np.where(ahead_mask[None, :, None], a_arr, b_arr)

        # leading-edge shadow: soft dark band just ahead of travel direction
        lead_x = left_edge if direction == "rtl" else right_edge
        shadow_dist = (lead_x - xs) if direction == "rtl" else (xs - lead_x)
        shadow = np.clip(1.0 - np.abs(shadow_dist) / 60.0, 0.0, 1.0) ** 1.5
        shadow = np.where(shadow_dist > 0, shadow, 0.0)  # only on the "ahead" side
        frame = frame * (1.0 - 0.35 * shadow)[None, :, None]

        # composite the strip itself over [left_edge, right_edge]
        sx0, sx1 = int(np.clip(left_edge, 0, w)), int(np.clip(right_edge, 0, w))
        if sx1 > sx0:
            strip_sx0 = sx0 - int(left_edge)
            seg_rgb = strip_rgb[:, strip_sx0:strip_sx0 + (sx1 - sx0)]
            seg_a = strip_alpha[:, strip_sx0:strip_sx0 + (sx1 - sx0)]
            frame[:, sx0:sx1] = frame[:, sx0:sx1] * (1 - seg_a) + seg_rgb * seg_a

        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(out_dir / f"o{i:04d}.png")

    _run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(out_dir / "o%04d.png"),
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(out_mp4)])
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=0.32)
    ap.add_argument("--direction", choices=["rtl", "ltr"], default="rtl")
    a = ap.parse_args()
    render(Path(a.a), Path(a.b), Path(a.out), a.duration, direction=a.direction)
