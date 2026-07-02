#!/usr/bin/env python
"""Kinetic word-cascade captions (Tier-2) — decoupled from the LOCKED shared comic engine.

Renders, for one caption, a sequence of cumulative reveal-state PNGs (word 1, words 1-2, ...): a
fixed-geometry parchment comic box at the bottom third, the words appearing one at a time, with the
payload KEYWORD drawn in red. build_mocomic_v2 overlays these states with per-word enable windows +
a quick snap-in, so the caption cascades in synced to the beat instead of sitting static. The
Scripture red-letter bars stay static (the engine still draws those — sacred anchors, not TikTok text).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1080, 1920
FONT = r"C:\Windows\Fonts\comicbd.ttf"
PARCH = (245, 234, 208, 255)
INK = (18, 14, 8, 255)
RED = (170, 30, 26, 255)
FSZ, PAD, MARGIN = 48, 26, 40
_SLOP = {"—": "-", "–": "-", "―": "-", "‘": "'", "’": "'", "“": '"', "”": '"', "…": "..."}


def _san(s):
    for k, v in _SLOP.items():
        s = s.replace(k, v)
    return s


def _wrap(draw, words, font, maxw):
    lines, cur = [], []
    for w in words:
        trial = " ".join(cur + [w])
        if not cur or draw.textlength(trial, font=font) <= maxw:
            cur.append(w)
        else:
            lines.append(cur); cur = [w]
    if cur:
        lines.append(cur)
    return lines


def render_states(text, kw, out_dir, stem, page=(PAGE_W, PAGE_H)):
    """Return (paths, box_top, box_h). paths[k] shows the first k+1 words (cumulative).
    page=(W,H): 9:16 (1080x1920, default) or 16:9 landscape (1920x1080). Font/box scale by width."""
    pw, ph = page
    # Scale furniture by canvas HEIGHT (9:16 baseline 1920) — height governs how tall the box
    # reads. Scaling by WIDTH ballooned the box on 16:9 (1920 wide / 1080 tall). 9:16 -> 1.0 (unchanged).
    sc = ph / 1920.0
    fsz, pad, margin = round(FSZ * sc), round(PAD * sc), round(MARGIN * sc)
    text = _san(text).upper()
    kwset = {w.strip(".,;:!?") for w in _san(kw).upper().split()} if kw else set()
    font = ImageFont.truetype(FONT, fsz)
    dummy = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    words = text.split()
    maxw = pw - 2 * margin - 2 * pad
    lines = _wrap(dummy, words, font, maxw)
    lh = fsz + round(14 * sc)
    box_h = len(lines) * lh + 2 * pad
    top = ph - box_h - round(56 * sc)
    left, right = margin, pw - margin

    # precompute a fixed layout: (x, y, word, color) for every word
    layout, y = [], top + pad
    for ln in lines:
        x = left + pad + round(4 * sc)
        for w in ln:
            color = RED if w.strip(".,;:!?") in kwset else INK
            layout.append((x, y, w, color))
            x += dummy.textlength(w + " ", font=font)
        y += lh

    paths = []
    for k in range(1, len(layout) + 1):
        img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([left, top, right, top + box_h], radius=round(16 * sc),
                            fill=PARCH, outline=INK, width=round(8 * sc))
        for (x, y, w, color) in layout[:k]:
            d.text((x, y), w, font=font, fill=color)
        p = out_dir / f"_kc_{stem}_{k:02d}.png"
        img.save(p)
        paths.append(p)
    return paths, top, box_h
