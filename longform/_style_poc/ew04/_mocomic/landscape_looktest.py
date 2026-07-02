#!/usr/bin/env python
"""EW04 LANDSCAPE look-test — wide 16:9 graphic-novel pages from the EXISTING stills.

$0: no new renders. Re-lays the EW04 portrait AI art into wide comic PAGES that
only work in landscape (splash+strip, polyptych row, 2x3 grid, wide-bleed hero) to
prove the long-form comic format. Same furniture vocabulary as comic_engine.py
(parchment caption box + red-letter Scripture bar + inked borders), re-geometried
for 2560x1440.

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/landscape_looktest.py
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
STILLS = HERE.parent / "stills"
OUT = HERE / "_landscape"
OUT.mkdir(exist_ok=True)

PAGE_W, PAGE_H = 2560, 1440
M, G, BORDER = 56, 30, 12
PAPER = (252, 249, 241)
INK = (18, 14, 8, 255)
PARCH = (245, 234, 208, 255)
WHITE = (250, 248, 244, 255)
RED = (150, 28, 24, 255)
FONT = r"C:\Windows\Fonts\comicbd.ttf"

_SLOP = {"—": "-", "–": "-", "‒": "-", "―": "-",
         "‘": "'", "’": "'", "“": '"', "”": '"', "…": "..."}


def sanitize(s):
    for k, v in _SLOP.items():
        s = s.replace(k, v)
    return s


# ---------------- crop ----------------
def fill_bias(im, w, h, bx=0.5, by=0.5):
    iw, ih = im.size
    s = max(w / iw, h / ih)
    sw, sh = max(math.ceil(iw * s), w), max(math.ceil(ih * s), h)
    im2 = im.resize((sw, sh), Image.LANCZOS)
    x = min(max(round((sw - w) * bx), 0), sw - w)
    y = min(max(round((sh - h) * by), 0), sh - h)
    return im2.crop((x, y, x + w, y + h))


# ---------------- landscape layouts ----------------
def _cols(area, n):
    x, y, w, h = area
    pw = (w - (n - 1) * G) / n
    return [(round(x + i * (pw + G)), y, round(pw), h) for i in range(n)]


def _rows(area, n):
    x, y, w, h = area
    ph = (h - (n - 1) * G) / n
    return [(x, round(y + i * (ph + G)), w, round(ph)) for i in range(n)]


def lay_splash_strip(area):
    """big hero (wide) on top + a bottom row of 3 story panels."""
    x, y, w, h = area
    strip_h = round(h * 0.30)
    hero_h = h - strip_h - G
    rects = [(x, y, w, hero_h)]
    rects += _cols((x, y + hero_h + G, w, strip_h), 3)
    return rects


def lay_poly3(area):
    return _cols(area, 3)


def lay_grid_2x3(area):
    out = []
    for r in _rows(area, 2):
        out += _cols(r, 3)
    return out


def lay_bleed(area):
    return [(0, 0, PAGE_W, PAGE_H)]


# ---------------- furniture ----------------
def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _box(d, x0, y0, x1, text, font_sz, fill, txt_fill, pad=26, radius=16):
    font = ImageFont.truetype(FONT, font_sz)
    lines = _wrap(d, sanitize(text).upper(), font, x1 - x0 - 2 * pad)
    lh = font_sz + 14
    h = len(lines) * lh + 2 * pad
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=radius, fill=fill, outline=INK, width=8)
    y = y0 + pad
    for ln in lines:
        d.text((x0 + pad + 4, y), ln, font=font, fill=txt_fill); y += lh
    return y0 + h


def draw_caption(d, slot, spec):
    typ = spec.get("type", "caption")
    text = sanitize(spec["text"])
    if typ == "redletter":
        font = ImageFont.truetype(FONT, 58); tagf = ImageFont.truetype(FONT, 40)
        mx, pad = 64, 30
        lines = _wrap(d, text, font, PAGE_W - 2 * mx - 2 * pad)
        lh = 72; bh = len(lines) * lh + 2 * pad; top = PAGE_H - bh - 70
        tag = f"{spec.get('speaker', 'JESUS')}  -  {spec.get('ref', '')}"
        tw = d.textlength(tag, font=tagf)
        d.rounded_rectangle([mx, top - 64, mx + tw + 56, top + 6], radius=10, fill=RED, outline=INK, width=4)
        d.text((mx + 28, top - 56), tag, font=tagf, fill=(255, 248, 240, 255))
        d.rounded_rectangle([mx, top, PAGE_W - mx, top + bh], radius=18, fill=WHITE, outline=INK, width=8)
        y = top + pad
        for ln in lines:
            d.text((mx + pad, y), ln, font=font, fill=RED); y += lh
    elif slot == "corner":
        _box(d, M + 10, M + 10, M + 920, text, 50, PARCH, INK)
    elif slot == "top_band":
        _box(d, M, M, PAGE_W - M, text, 52, PARCH, INK)
    else:  # overlay top
        _box(d, M, M, PAGE_W - M, text, 54, PARCH, INK)


# ---------------- page builder ----------------
def content_area(slot):
    top = M + (110 if slot == "top_band" else 0)
    return (M, top, PAGE_W - 2 * M, PAGE_H - 2 * M - (110 if slot == "top_band" else 0))


def build_page(name, mode, layout_fn, slot, panels, cap):
    """panels: list of (still, bias) for fill_each/bleed, OR single (still,bias) for poly (sliced)."""
    if mode == "bleed":
        still, bias = panels[0]
        im = Image.open(STILLS / still).convert("RGB")
        page = fill_bias(im, PAGE_W, PAGE_H, *bias).convert("RGBA")
        rects = []
    else:
        page = Image.new("RGBA", (PAGE_W, PAGE_H), PAPER)
        rects = layout_fn(content_area(slot))
        if mode == "poly":  # one image sliced across the columns (continuous broken page)
            still, bias = panels[0]
            full = fill_bias(Image.open(STILLS / still).convert("RGB"),
                             PAGE_W - 2 * M, content_area(slot)[3], *bias)
            ox, oy = M, content_area(slot)[1]
            for (x, y, w, h) in rects:
                page.paste(full.crop((x - ox, y - oy, x - ox + w, y - oy + h)), (x, y))
        else:  # fill_each
            for k, (x, y, w, h) in enumerate(rects):
                still, bias = panels[k % len(panels)]
                page.paste(fill_bias(Image.open(STILLS / still).convert("RGB"), w, h, *bias), (x, y))

    d = ImageDraw.Draw(page)
    for (x, y, w, h) in rects:
        d.rectangle([x, y, x + w, y + h], outline=INK, width=BORDER)
    draw_caption(d, slot, cap)
    dest = OUT / f"{name}.png"
    page.convert("RGB").save(dest)
    print(f"[page] {name}")
    return dest


PAGES = [
    dict(name="01_splash_strip", mode="fill_each", layout_fn=lay_splash_strip, slot="overlay",
         panels=[("01b_moses_close.png", (0.30, 0.40)),
                 ("02_judgment_plague.png", (0.42, 0.74)),
                 ("02b_serpents_spread.png", (0.5, 0.60)),
                 ("03_bronze_lifted.png", (0.5, 0.30))],
         cap={"type": "caption", "text": "My people were dying of snakebite -- the venom our sin had earned."}),

    dict(name="02_polyptych", mode="poly", layout_fn=lay_poly3, slot="top_band",
         panels=[("08_bitten_multitude.png", (0.5, 0.5))],
         cap={"type": "caption", "text": "You who are bitten -- that is every one of us."}),

    dict(name="03_grid_2x3", mode="fill_each", layout_fn=lay_grid_2x3, slot="corner",
         panels=[("05_night_teacher.png", (0.5, 0.45)),
                 ("05b_jesus_speaks.png", (0.5, 0.40)),
                 ("03b_serpent_atop_sky.png", (0.5, 0.30)),
                 ("06_cross_lifted.png", (0.5, 0.35)),
                 ("04b_face_to_life.png", (0.5, 0.35)),
                 ("01_hook_moses.png", (0.5, 0.45))],
         cap={"type": "caption", "text": "From the pole in the wilderness to the cross."}),

    dict(name="04_wide_hero", mode="bleed", layout_fn=lay_bleed, slot="overlay",
         panels=[("07_risen_christ.png", (0.5, 0.32))],
         cap={"type": "redletter", "speaker": "JESUS", "ref": "JOHN 3",
              "text": "As Moses lifted up the serpent in the wilderness, even so must the Son of man be lifted up."}),
]


def main():
    dests = [build_page(**p) for p in PAGES]
    # vertical contact sheet (half-res) for one-click review
    half = [(Image.open(d).resize((PAGE_W // 2, PAGE_H // 2), Image.LANCZOS)) for d in dests]
    gap = 24
    sheet = Image.new("RGB", (PAGE_W // 2, len(half) * (PAGE_H // 2) + (len(half) - 1) * gap), (20, 18, 14))
    y = 0
    for im in half:
        sheet.paste(im, (0, y)); y += PAGE_H // 2 + gap
    sheet.save(OUT / "_CONTACT_SHEET.png")
    print(f"\npages + sheet -> {OUT}")


if __name__ == "__main__":
    main()
