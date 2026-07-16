#!/usr/bin/env python
"""caption_render16.py — caption furniture for the 16:9 dynamic comic, placed by caption_layout.

Replaces the locked comic_engine's full-width bottom furniture (SPEC v2 §4B). Three looks:

  kinetic box / scrim   compact parchment box (Tier 1) or translucent soft-top scrim (Tier 2)
                        at the SOLVED box — cumulative word-cascade states, payload keyword in
                        red (same cascade language as the locked short's kinetic_caption.py)
  redletter plaque      compact white plaque + red speaker/ref tag chip, red KJV text (Tier 1)
  redletter band        designed translucent parchment band, soft gradient top edge, red KJV
                        text + tag chip — art shows through (never the old opaque slab)

Text contract: caption_layout.solve() sanitizes + cases the text ONCE and returns the wrapped
lines; these renderers draw sol["lines"] VERBATIM so measured == drawn (red-letter Scripture
stays mixed case, kinetic is upper). All PNGs are full-page transparent overlays; the driver
composites them with ffmpeg.
"""
from PIL import Image, ImageDraw, ImageFont

import caption_layout as cl

PARCH = (245, 234, 208)
WHITE = (250, 248, 244)
INK = (18, 14, 8, 255)
RED = (150, 28, 24, 255)
RED_KIN = (170, 30, 26, 255)
TAG_TXT = (255, 248, 240, 255)


def _font(sz):
    return ImageFont.truetype(cl.FONT, sz)


def _soft_top(layer, x, y, bw, soft):
    """Fade the top `soft` px of a drawn band/scrim to transparent (soft gradient edge)."""
    a = layer.getchannel("A")
    d = ImageDraw.Draw(a)
    full = a.crop((x, y, x + bw, y + soft))
    for i in range(soft):
        f = (i + 1) / soft
        row = full.crop((0, i, bw, i + 1)).point(lambda v, f=f: int(v * f))
        a.paste(row, (x, y + i))
    layer.putalpha(a)


# ---------------- kinetic word cascade ----------------
def render_kinetic_states(kw, sol, page, out_dir, stem):
    """Cumulative reveal PNGs (word 1, words 1-2, ...) at the SOLVED box. -> [paths]
    Words come from sol['lines'] verbatim (already sanitized/upper-cased by the solver)."""
    pw, ph = page
    sc = ph / cl.BASE_H
    x, y, bw, bh = sol["box"]
    fsz, pad, lh = sol["fsz"], sol["pad"], sol["lh"]
    font = _font(fsz)
    kwset = {w.strip(".,;:!?") for w in cl.san(kw).upper().split()} if kw else set()
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

    layout, yy = [], y + pad
    for ln in sol["lines"]:
        xx = x + pad
        for w in ln.split():
            color = RED_KIN if w.strip(".,;:!?") in kwset else INK
            layout.append((xx, yy, w, color))
            xx += d0.textlength(w + " ", font=font)
        yy += lh
    scrim = sol["style"] == "scrim"
    # the box layer is drawn once (scrim gets a soft gradient top edge, R1 language)
    box_layer = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    bd = ImageDraw.Draw(box_layer)
    if scrim:
        bd.rounded_rectangle([x, y, x + bw, y + bh], radius=round(10 * sc), fill=PARCH + (205,))
        _soft_top(box_layer, x, y, bw + 1, round(22 * sc))
    else:
        bd.rounded_rectangle([x, y, x + bw, y + bh], radius=round(12 * sc),
                             fill=PARCH + (244,), outline=INK, width=round(6 * sc))
    paths = []
    for k in range(1, len(layout) + 1):
        img = box_layer.copy()
        d = ImageDraw.Draw(img)
        for (xx, yy, w, color) in layout[:k]:
            d.text((xx, yy), w, font=font, fill=color)
        p = out_dir / f"_kc16_{stem}_{k:02d}.png"
        img.save(p)
        paths.append(p)
    return paths


# ---------------- red-letter Scripture ----------------
def render_redletter(cap, sol, page, out_path):
    """Static full-page PNG: plaque (Tier 1) or translucent parchment band (Tier 2/3).
    Body text = sol['lines'] verbatim (mixed-case KJV, sanitized by the solver)."""
    pw, ph = page
    sc = ph / cl.BASE_H
    x, y, bw, bh = sol["box"]
    fsz, pad, lh, chip_h = sol["fsz"], sol["pad"], sol["lh"], sol["chip_h"]
    font, tagf = _font(fsz), _font(round(cl.R_TAG * sc))
    tag = cl.san(f"{cap.get('speaker', 'JESUS')} - {cap.get('ref', '')}".strip(" -"))
    text_top = y + chip_h + pad

    img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if sol["style"] == "plaque":
        d.rounded_rectangle([x, y + chip_h, x + bw, y + bh], radius=round(14 * sc),
                            fill=WHITE + (240,), outline=INK, width=round(6 * sc))
    else:                               # band — translucent parchment, soft top edge
        band_top = y + chip_h
        d.rectangle([x, band_top, x + bw, y + bh], fill=PARCH + (205,))
        _soft_top(img, x, band_top, bw + 1, round(26 * sc))
    # tag chip
    tw = d.textlength(tag, font=tagf)
    chip_y1 = y + chip_h + round(4 * sc)
    d.rounded_rectangle([x, y, x + tw + round(44 * sc), chip_y1], radius=round(9 * sc),
                        fill=RED, outline=INK, width=round(3 * sc))
    d.text((x + round(22 * sc), y + round(6 * sc)), tag, font=tagf, fill=TAG_TXT)
    # body text (red letter, mixed case)
    yy = text_top
    for ln in sol["lines"]:
        d.text((x + pad, yy), ln, font=font, fill=RED)
        yy += lh
    img.save(out_path)
    return out_path
