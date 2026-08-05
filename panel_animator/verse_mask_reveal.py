#!/usr/bin/env python
"""Verse-Mask Reveal -- "the Word becomes the scene." Adapted from
ArkAIology's `visual_bakeoff/iris_mask.py::text_mask_reveal()` (a sibling
project's own $0 deterministic primitive: grow a reveal outward from a
rendered glyph/word silhouette via a distance-field, so growth begins
exactly at the letterforms). Ported into this project's own letterpress-ink
verse vocabulary instead of ArkAIology's plain typeset word: the word is
PRESSED onto the page first (reusing _s3_thread_leaf_54_55.py's
make_line_mask/compose_pressed_tile, the same technique already proven on
spreads 54-55 and the round-4 text-combo POCs), held, and then the next
scene's art grows outward from inside its letterforms until it fills the
frame -- the pressed word becomes the aperture the next picture arrives
through.

No camera movement, no repaint of either still -- a pure distance-field
alpha mask + ffmpeg composite, deterministic.

Usage:
    python verse_mask_reveal.py --a stillA.png --b stillB.png --out clip.mp4 \\
        --word "BLOOD" --word-x 0.06 --word-y 0.06 [--hold 1.4] [--grow 1.8]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFont
from scipy.ndimage import distance_transform_edt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / "poc_living_sketchbook" / "day_of_atonement"))
import _s3_thread_leaf_54_55 as tl  # noqa: E402  -- reuse the proven letterpress-verse primitives

FPS = 30
W, H = 1920, 1080
WORD_SIZE = 96  # a single load-bearing word is rendered much larger than a verse line


def _ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render(still_a: Path, still_b: Path, out_mp4: Path, word: str,
           word_x: float, word_y: float, hold: float = 1.4, grow: float = 1.8,
           feather: int = 22, w: int = W, h: int = H):
    a = _scale_crop(Image.open(still_a).convert("RGB"), w, h)
    b = _scale_crop(Image.open(still_b).convert("RGB"), w, h)
    a_arr, b_arr = np.asarray(a), np.asarray(b)

    font = ImageFont.truetype(tl.F_BODY, WORD_SIZE)
    mask, mw, mh, pad, base_local = tl.make_line_mask([(word, WORD_SIZE)], {WORD_SIZE: font})
    tile_dark = tl.compose_pressed_tile(mask, tl.INK_DARK)
    tile_final = tl.compose_pressed_tile(mask, tl.INK_FINAL)

    block_x, block_y = int(word_x * w), int(word_y * h)

    # full-frame binary mask of the glyph silhouette, positioned EXACTLY
    # where paste_tile() will later place the tile (top-left = target_x-pad,
    # target_baseline_y-baseline_local = block_y since target_baseline_y is
    # block_y+base_local) -- the distance field is computed from THIS mask,
    # so the reveal begins exactly inside the pressed letterforms, never
    # offset from what the viewer sees.
    glyph_full = Image.new("L", (w, h), 0)
    glyph_full.paste(mask, (block_x - pad, block_y))
    glyph_arr = np.asarray(glyph_full) > 40
    dist = distance_transform_edt(~glyph_arr)
    max_dist = float(dist.max()) + feather

    press_dur = 0.10
    color_ease_dur = 0.5

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    total = hold + grow
    n = max(1, int(round(total * FPS)))
    for i in range(n):
        t = i / FPS

        # base frame: A, growing to B once the grow phase starts
        if t < hold:
            base_frame = a_arr
        else:
            gt = _ease(min(1.0, (t - hold) / grow))
            threshold = gt * max_dist
            soft = np.clip((threshold - dist) / max(1, feather) * 127 + 128, 0, 255)
            grow_mask = soft.astype(np.uint8)
            base_frame = np.asarray(Image.composite(b, a, Image.fromarray(grow_mask, "L")))

        img = Image.fromarray(base_frame).convert("RGBA")

        # the pressed word itself: pops in near t=0.15s, ink-dark then eases
        # to final tone, and holds visible even as the scene grows around it
        lt = t - 0.15
        if lt >= 0:
            if lt < press_dur:
                pop = lt / press_dur
                scale, alpha, color = 1.05 - 0.05 * pop, pop, tl.INK_DARK
            else:
                ce = min(1.0, (lt - press_dur) / color_ease_dur)
                scale, alpha, color = 1.0, 1.0, tl.lerp_color(tl.INK_DARK, tl.INK_FINAL, ce)
            tile = tl.compose_pressed_tile(mask, color)
            tl.paste_tile(img, tile, block_x, block_y + base_local, pad, base_local, scale, alpha)

        Image.fromarray(np.array(img.convert("RGB"))).save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--word", required=True)
    ap.add_argument("--word-x", type=float, default=0.06, dest="word_x")
    ap.add_argument("--word-y", type=float, default=0.06, dest="word_y")
    ap.add_argument("--hold", type=float, default=1.4)
    ap.add_argument("--grow", type=float, default=1.8)
    a = ap.parse_args()
    render(Path(a.a), Path(a.b), Path(a.out), a.word, a.word_x, a.word_y, a.hold, a.grow)
