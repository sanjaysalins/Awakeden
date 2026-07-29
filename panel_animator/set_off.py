#!/usr/bin/env python
"""Set-Off — a faint mirrored impression of an earlier hand-scribed verse,
absorbed into the blank page instead of sitting on top of it.

Heavy ink pressed against a facing page leaves a "set-off": a mirrored, pale
ghost of what was written opposite, soaked into the paper's own fibre. At a
landing, an earlier spread's Scribed Ink verse card reappears on the blank
upper half of the final page — mirrored, brown-ink faint, blurred, and
absorbed unevenly (never a flat clean watermark). No caption, no card, no
repetition: the words have simply come through from an earlier page.

$0, deterministic: reuses the EXACT raster `scribed_ink_card()` already
produces elsewhere in the episode (copied verbatim below), so the
"handwriting" is guaranteed identical to what's on screen elsewhere. This is
a deterministic overlay of an already-rendered raster — it never generates
new writing, so it never touches the never-animate-writing rule.

Usage (as a library, inside an assembly script's per-frame loop):
    from set_off import scribed_ink_card, apply_set_off
    card = scribed_ink_card(["Why are ye fearful,", "O ye of little faith?"],
                             "MATTHEW 8:26")
    frame = apply_set_off(frame, card, progress)   # progress: 0.0 -> 1.0

Usage (CLI demo, renders a standalone test clip over a still):
    python set_off.py --demo --still <landing_still.png> --out <demo.mp4> --duration 6
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30

# Colour constants + font paths, copied from poc_living_sketchbook/storm/
# _s4_assemble.py so scribed_ink_card() below renders byte-identical
# handwriting to the verse cards already used elsewhere in an episode.
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)          # unused directly here, kept for source fidelity
FADED_INK = (75, 62, 48)       # the "faded ink" tone the set-off tints toward

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"

# Set-off tuning. max alpha is the brief's "12-18% max alpha" band, mid-point;
# the fibre-noise field then modulates each pixel further down within that.
SET_OFF_MAX_ALPHA = 0.16
SET_OFF_BLUR = 1.2
SET_OFF_NOISE_SEED = 71
SET_OFF_NOISE_BLUR = 14
SET_OFF_NOISE_LO, SET_OFF_NOISE_HI = 0.6, 1.0


def scribed_ink_card(lines, ref):
    """SCRIBED INK grammar (SKILL.md sec.5, poc_living_sketchbook/
    _lettering_compare/_render_candidates.py's render_scribed_ink -- the
    device this episode exists to prove in motion): hand-written script,
    letter-by-letter seeded baseline/rotation wobble, underline swash, small
    rubric-red reference caps. NO box, ever. Kunstler's comma/period glyphs
    are nearly invisible at body size -- draw punctuation from a larger
    stroked instance of the same font (fixed bug, backported per SKILL.md).

    Copied VERBATIM from poc_living_sketchbook/storm/_s4_assemble.py so the
    set-off's source raster is guaranteed to be the same handwriting as any
    verse card already rendered elsewhere in the episode."""
    font = ImageFont.truetype(F_KUNSTLER, 48)
    PUNCT = set(".,;:'\u2019\u201c\u201d?")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(48 * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)

    def char_w(ch, f=font):
        return td.textlength(ch, font=f)

    line_h = 62
    canvas = Image.new("RGBA", (W, line_h * len(lines) + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    rng = random.Random(26)
    y = 10
    last_lw = last_x0 = 0
    for ln in lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (W - tw) / 2
        last_lw, last_x0 = tw, x
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.5, 2.5)
            jr = rng.uniform(-1.2, 1.2)
            draw_font = font_punct if ch in PUNCT else font
            layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.text((10, 10), ch, font=draw_font, fill=(*INK, 255),
                     stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*INK, 255))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + 32))
            canvas.alpha_composite(layer, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)
        y += line_h
    swash = [(last_x0, y - 6)]
    for i in range(1, 9):
        swash.append((last_x0 + last_lw * i / 8, y - 6 + rng.uniform(-3, 3)))
    d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
    rw = d.textlength(ref, font=ref_font)
    d.text(((W - rw) / 2, y + 16), ref, font=ref_font, fill=(*RUBRIC, 235))
    return canvas.crop((0, 0, W, y + 60))


def ease(t: float) -> float:
    """Cosine ease-in-out, 0..1 -> 0..1. Matches _s4_assemble.py's ease()."""
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


@lru_cache(maxsize=16)
def _fibre_noise(w: int, h: int, seed: int = SET_OFF_NOISE_SEED):
    """Smoothed random field renormalized into the ~0.6-1.0 band -- the ink
    is absorbed unevenly into the paper's fibre rather than sitting as a
    flat, clean wash. Cached per (w, h, seed) since the same card renders
    the same footprint every frame of a hold."""
    rng = random.Random(seed)
    noise = Image.new("L", (max(1, w), max(1, h)))
    noise.putdata([rng.randint(0, 255) for _ in range(w * h)])
    noise = noise.filter(ImageFilter.GaussianBlur(SET_OFF_NOISE_BLUR))
    arr = np.asarray(noise, dtype=np.float32) / 255.0
    lo, hi = float(arr.min()), float(arr.max())
    arr = (arr - lo) / (hi - lo) if hi - lo > 1e-6 else np.full_like(arr, 0.5)
    return SET_OFF_NOISE_LO + (SET_OFF_NOISE_HI - SET_OFF_NOISE_LO) * arr


def apply_set_off(frame: Image.Image, card: Image.Image, progress: float,
                   cx_frac: float = 0.5, cy_frac: float = 0.22) -> Image.Image:
    """Composite a mirrored, faded, absorbed set-off impression of `card`
    onto `frame`. `progress` (0.0-1.0) is the ease-in fade -- 0 renders
    nothing, 1 renders the mark at its full (still faint) strength.

    frame: an already-composited 1080x1920 RGB frame.
    card: an RGBA raster from scribed_ink_card() (or any hand-lettered
        raster produced the same way elsewhere in the episode).
    """
    if progress <= 0.0:
        return frame

    # 1. mirror -- a set-off is the impression of the FACING page, backwards.
    mirrored = card.transpose(Image.FLIP_LEFT_RIGHT)
    cw, ch = mirrored.size

    # 2. desaturate/tint toward the paper's own faded-ink brown, at a max
    #    12-18% alpha scaled by progress. Recolour fully to FADED_INK --
    #    the original glyph shape survives entirely in the alpha channel.
    src_alpha = np.asarray(mirrored.split()[3], dtype=np.float32) / 255.0
    scaled_alpha = np.clip(src_alpha * SET_OFF_MAX_ALPHA * progress, 0.0, 1.0)
    tinted = Image.new("RGBA", (cw, ch), (*FADED_INK, 0))
    tinted.putalpha(Image.fromarray((scaled_alpha * 255).astype(np.uint8)))

    # 3. blur ~1.2px -- softens the pen-stroke edges into a soaked-in look.
    tinted = tinted.filter(ImageFilter.GaussianBlur(SET_OFF_BLUR))

    # 4. multiply alpha by the fibre-noise field -- uneven absorption, not a
    #    flat clean watermark.
    noise = _fibre_noise(cw, ch)
    a2 = np.asarray(tinted.split()[3], dtype=np.float32) / 255.0
    a2 = np.clip(a2 * noise, 0.0, 1.0)
    tinted.putalpha(Image.fromarray((a2 * 255).astype(np.uint8)))

    # 5. composite onto the frame at the given position, via true alpha
    #    blending (not a simple opaque paste).
    out = frame.convert("RGBA")
    fw, fh = out.size
    px = int(fw * cx_frac - cw / 2)
    py = int(fh * cy_frac - ch / 2)
    out.paste(tinted, (px, py), tinted)
    return out.convert("RGB")


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _demo(a):
    still = Path(a.still)
    out_mp4 = Path(a.out)
    frame_base = scale_crop(Image.open(still).convert("RGB"), W, H)
    card = scribed_ink_card(
        ["Why are ye fearful,", "O ye of little faith?"], "MATTHEW 8:26")

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(a.duration * FPS)
    for i in range(n_frames):
        t = i / FPS
        progress = ease(min(1.0, t / a.fade)) if a.fade > 0 else 1.0
        frame = apply_set_off(frame_base, card, progress, a.cx_frac, a.cy_frac)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true",
                     help="render a standalone demo clip over a test still")
    ap.add_argument("--still", help="1080x1920 (or larger) landing-style still")
    ap.add_argument("--out", help="output mp4 path")
    ap.add_argument("--duration", type=float, default=6.0, help="demo clip length, seconds")
    ap.add_argument("--fade", type=float, default=2.5,
                     help="ease-in seconds before the mark holds at full strength")
    ap.add_argument("--cx-frac", type=float, default=0.5, dest="cx_frac")
    ap.add_argument("--cy-frac", type=float, default=0.22, dest="cy_frac")
    a = ap.parse_args()
    if not a.demo:
        ap.error("set_off.py is a library module -- run with --demo to render a test clip")
    if not a.still or not a.out:
        ap.error("--demo requires --still and --out")
    _demo(a)


if __name__ == "__main__":
    main()
