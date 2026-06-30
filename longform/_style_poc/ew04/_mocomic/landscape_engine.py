#!/usr/bin/env python
"""Awakeden LANDSCAPE motion-comic engine — the 16:9 long-form template library.

Sibling of the locked 9:16 shorts comic_engine.py. A landscape PAGE is a grid of
typed cells; each cell is filled by ONE of three fidelities:
    hero  (16:9)  = the ONE paid veo animation        [VEO]
    col   (9:16)  = an existing shorts clip dropped WHOLE, zero crop [REUSE]
    kb            = a still + Ken Burns ($0 cheat)     [KEN BURNS]
Governing rule: at most ONE 'hero' (veo) per page; several templates are veo=0
(pure reuse / Ken Burns) so a long-form alternates paid pages with free pages and
the per-episode veo budget stays flat.

Templates are pure geometry off PAGE_W/PAGE_H (same as the shorts engine), so the
static preview here and the motion builder (landscape_motion_page.py) share them.

This module:
  * defines the 10 built templates (Core 6 + Extended 4)  [11-12 catalogued, not built]
  * renders a $0 STATIC preview PNG per template + a contact sheet, filled from the
    existing EW04 stills, with a fidelity BADGE per cell so the economics is visible.

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/landscape_engine.py
"""
import importlib.util
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lt", HERE / "landscape_looktest.py")
lt = importlib.util.module_from_spec(spec); spec.loader.exec_module(lt)

STILLS = HERE.parent / "stills"
WIDE = HERE / "_landscape" / "hero_serpent_wide.png"   # a real 16:9 still for hero cells
OUT = HERE / "_templates"; OUT.mkdir(exist_ok=True)

PAGE_W, PAGE_H = 2560, 1440
M, G, BORDER = 56, 30, 12
PAPER, INK, PARCH = lt.PAPER, lt.INK, lt.PARCH
FONT = lt.FONT
RAIL_W = int(((PAGE_H - 2 * M) * 9 / 16) // 2 * 2)     # true 9:16 column width (even)

# fidelity badge styling
BADGE = {"hero": ("VEO", (150, 28, 24)),
         "col":  ("9:16 REUSE", (34, 64, 112)),
         "kb":   ("KEN BURNS", (84, 84, 84))}


# ---------------- geometry helpers (even-snapped for downstream video) ----------------
def _even(n):
    return int(n) - int(n) % 2


def cols(area, n, g=G):
    x, y, w, h = area
    pw = (w - (n - 1) * g) / n
    return [(round(x + i * (pw + g)), y, _even(round(pw)), h) for i in range(n)]


def rows(area, n, g=G):
    x, y, w, h = area
    ph = (h - (n - 1) * g) / n
    return [(x, round(y + i * (ph + g)), w, _even(round(ph))) for i in range(n)]


def split_v(area, lw, g=G):
    x, y, w, h = area
    lw = _even(lw)
    return (x, y, lw, h), (x + lw + g, y, _even(w - lw - g), h)


def split_h(area, th, g=G):
    x, y, w, h = area
    th = _even(th)
    return (x, y, w, th), (x, y + th + g, w, _even(h - th - g))


def C(rect, fid):
    return {"rect": rect, "fid": fid}


def content():
    return (M, M, PAGE_W - 2 * M, PAGE_H - 2 * M)


# ---------------- THE TEMPLATES (name -> dict(veo, cap, cells, sliced?)) ----------------
def t_full_bleed():
    return dict(veo=1, cap="overlay", cells=[C((0, 0, PAGE_W, PAGE_H), "hero")])


def t_hero_rail():
    left, rail = split_v(content(), content()[2] - RAIL_W - G)
    hero, band = split_h(left, left[2] * 9 / 16)
    return dict(veo=1, cap="corner", cells=[C(hero, "hero"), C(rail, "col"), C(band, "kb")])


def t_splash_strip():
    hero, strip = split_h(content(), (PAGE_H - 2 * M) * 0.66)
    return dict(veo=1, cap="overlay",
                cells=[C(hero, "hero")] + [C(r, "kb") for r in cols(strip, 3)])


def t_triptych_cols():
    return dict(veo=0, cap="top_band", cells=[C(r, "col") for r in cols(content(), 3)])


def t_polyptych():
    return dict(veo=0, cap="top_band", sliced=True,
                cells=[C(r, "kb") for r in cols(content(), 3)])


def t_grid_2x3():
    """Montage: two full-height 9:16 clip RAILS book-end a hero+3-still centre, so the reuse
    clips drop in NATIVE (true 9:16, zero crop) instead of a landscape grid cell with cream gaps."""
    x0, y0, w, h = content()
    lrail = (x0, y0, RAIL_W, h)
    rrail = (x0 + w - RAIL_W, y0, RAIL_W, h)
    cx = x0 + RAIL_W + G
    cw = w - 2 * (RAIL_W + G)                      # centre column width
    hero = (cx, y0, cw, _even(round(cw * 9 / 16)))  # 16:9 hero on top
    sub = (cx, hero[1] + hero[3] + G, cw, y0 + h - (hero[1] + hero[3] + G))
    top, bot = split_h(sub, (sub[3] - G) / 2)       # 2 small kb + 1 wide kb below
    kbL, kbR = cols(top, 2)
    cells = [C(lrail, "col"), C(hero, "hero"), C(kbL, "kb"),
             C(kbR, "kb"), C(bot, "kb"), C(rrail, "col")]
    return dict(veo=1, cap="corner", cells=cells)


def t_big_inset():
    hero = C((0, 0, PAGE_W, PAGE_H), "hero")
    iw, ih = 600, 380
    in1 = C((M + 30, PAGE_H - M - 30 - ih, iw, ih), "kb")
    in2 = C((PAGE_W - M - 30 - iw, PAGE_H - M - 30 - ih, iw, ih), "kb")
    return dict(veo=1, cap="overlay", cells=[hero, in1, in2])


def t_band_of_three():
    a, b, c = rows(content(), 3)
    return dict(veo=1, cap="overlay",
                cells=[C(a, "kb"), C(b, "hero"), C(c, "col")])


def t_big_left_L():
    left, right = split_v(content(), content()[2] - RAIL_W - G)
    hero, band = split_h(left, left[2] * 9 / 16)
    rtop, rbot = rows(right, 2)
    return dict(veo=1, cap="corner",
                cells=[C(hero, "hero"), C(rtop, "kb"), C(rbot, "kb"), C(band, "col")])


def t_rail_duo():
    rail, right = split_v(content(), RAIL_W)
    rtop, rbot = rows(right, 2)
    return dict(veo=0, cap="top_band",
                cells=[C(rail, "col"), C(rtop, "kb"), C(rbot, "kb")])


TEMPLATES = {
    # --- Core 6 ---
    "01_full_bleed":    t_full_bleed,
    "02_hero_rail":     t_hero_rail,
    "03_splash_strip":  t_splash_strip,
    "04_triptych_cols": t_triptych_cols,
    "05_polyptych":     t_polyptych,
    "06_grid_2x3":      t_grid_2x3,
    # --- Extended 4 ---
    "07_big_inset":     t_big_inset,
    "08_band_of_three": t_band_of_three,
    "09_big_left_L":    t_big_left_L,
    "10_rail_duo":      t_rail_duo,
}
# Catalogued, NOT built (phase 2, harder geometry):
#   11_diagonal_canted  — angled gutters
#   12_breaking_border  — a figure overlaps panel edges


# ---------------- preview rendering ($0, stills only) ----------------
POOL = ["01b_moses_close", "02_judgment_plague", "02b_serpents_spread", "03_bronze_lifted",
        "03b_serpent_atop_sky", "04b_face_to_life", "05_night_teacher", "05b_jesus_speaks",
        "06_cross_lifted", "08_bitten_multitude", "01_hook_moses", "07_risen_christ"]


def _still(name):
    return Image.open(STILLS / f"{name}.png").convert("RGB")


def badge(d, rect, fid):
    txt, col = BADGE[fid]
    x, y, w, h = rect
    f = ImageFont.truetype(FONT, 30)
    tw = d.textlength(txt, font=f)
    bx, by = x + 16, y + h - 56
    d.rounded_rectangle([bx, by, bx + tw + 28, by + 44], radius=8,
                        fill=col + (255,), outline=(250, 248, 244, 255), width=3)
    d.text((bx + 14, by + 6), txt, font=f, fill=(250, 248, 244, 255))


def caption_box(d, slot, text):
    if slot == "top_band":
        lt._box(d, M, M, PAGE_W - M, text, 48, PARCH, INK)
    elif slot == "corner":
        lt._box(d, M + 12, M + 12, M + 12 + 760, text, 44, PARCH, INK)
    else:  # overlay top-left
        lt._box(d, M + 12, M + 12, M + 12 + 900, text, 46, PARCH, INK)


def render_preview(name, tpl, caption):
    page = Image.new("RGBA", (PAGE_W, PAGE_H), PAPER)
    cells = tpl["cells"]
    pi = 0
    if tpl.get("sliced"):                      # one wide image broken across the columns
        full = lt.fill_bias(_still("08_bitten_multitude") if not WIDE.exists()
                            else Image.open(WIDE).convert("RGB"),
                            PAGE_W - 2 * M, cells[0]["rect"][3], 0.5, 0.5)
        ox = M
        for c in cells:
            x, y, w, h = c["rect"]
            page.paste(full.crop((x - ox, 0, x - ox + w, h)), (x, y))
    else:
        for c in cells:
            x, y, w, h = c["rect"]
            if c["fid"] == "hero" and WIDE.exists():
                src = Image.open(WIDE).convert("RGB")          # real 16:9 art for hero
            else:
                src = _still(POOL[pi % len(POOL)]); pi += 1
            page.paste(lt.fill_bias(src, w, h, 0.5, 0.40), (x, y))

    d = ImageDraw.Draw(page)
    for c in cells:                            # inked borders + fidelity badges
        x, y, w, h = c["rect"]
        d.rectangle([x, y, x + w, y + h], outline=INK, width=BORDER)
        badge(d, c["rect"], c["fid"])
    caption_box(d, tpl["cap"], caption)
    dest = OUT / f"{name}.png"
    page.convert("RGB").save(dest)
    return dest


CAPS = {
    "01_full_bleed":    "Hook / gospel pivot / the landing on Christ.",
    "02_hero_rail":     "A main moment + a witness reaction.",
    "03_splash_strip":  "Establishing vista + three supporting beats.",
    "04_triptych_cols": "Three witnesses -- all reused, zero veo.",
    "05_polyptych":     "One sweeping vista sliced across the page.",
    "06_grid_2x3":      "Montage / survey / passage of time.",
    "07_big_inset":     "A scene with a telling detail inset.",
    "08_band_of_three": "Three stacked moments, sequential.",
    "09_big_left_L":    "Dynamic asymmetry -- big hero, wrapping L.",
    "10_rail_duo":      "A witness column + two beats, near-free.",
}


def main():
    dests = []
    for name, fn in TEMPLATES.items():
        tpl = fn()
        dests.append((name, tpl["veo"], render_preview(name, tpl, CAPS[name])))
        print(f"[tpl] {name:18s} veo={tpl['veo']}  cells={len(tpl['cells'])}")

    # contact sheet: 2 columns, labelled band over each page
    tw, th = PAGE_W // 2, PAGE_H // 2
    lab = 64
    ncol, nrow = 2, (len(dests) + 1) // 2
    sheet = Image.new("RGB", (ncol * tw + 30, nrow * (th + lab) + 30), (22, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 34)
    for i, (name, veo, dp) in enumerate(dests):
        cx, cy = (i % ncol) * tw + 10, (i // ncol) * (th + lab) + 10
        d.text((cx + 8, cy + 8), f"{name}   (veo/page = {veo})", font=f, fill=(245, 240, 230))
        sheet.paste(Image.open(dp).resize((tw - 20, th - 20), Image.LANCZOS), (cx, cy + lab))
    sheet.save(OUT / "_TEMPLATE_SHEET.png")
    n0 = sum(1 for _, v, _ in dests if v == 0)
    print(f"\n{len(dests)} templates ({n0} zero-veo) -> {OUT}\\_TEMPLATE_SHEET.png")


if __name__ == "__main__":
    main()
