"""Lettering redesign POC: 4 real candidates replacing the "alien" ArkAIology-
style caption chip (translucent card + Arial Black + yellow highlighter),
composited onto ACTUAL Jericho art -- not mockups. Also renders our current
(hated) treatment on the same frame for a fair three-way comparison, plus a
display-type ("13 LAPS" style) redesign pass.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_lettering_compare/_render_candidates.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
JERICHO = HERE.parents[0] / "jericho"
OUT = HERE / "candidates"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)
CREAM = (238, 226, 194)
FADED_INK = (70, 62, 54)

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_OLDENGL = "C:/Windows/Fonts/OLDENGL.TTF"
F_VLADIMIR = "C:/Windows/Fonts/VLADIMIR.TTF"
F_GEORGIA = "C:/Windows/Fonts/georgia.ttf"
F_GEORGIA_I = "C:/Windows/Fonts/georgiai.ttf"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_ZILLA_I = "C:/Windows/Fonts/ZillaSlab-Italic.ttf"
F_CORMORANT_I = "C:/Windows/Fonts/CormorantInfant-Italic.ttf"
F_ARIBLK = "C:/Windows/Fonts/ariblk.ttf"


def base_canvas(still_name):
    im = Image.open(JERICHO / "stills" / f"{still_name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def wrap(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def label(img, text, xy, size=26, color=INK, font=F_GEORGIA):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(font, size)
    d.text(xy, text, font=f, fill=color)


# ============================================================ 0. THE CURRENT (hated) TREATMENT
def render_current_hated():
    canvas = base_canvas("j06_thread").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    text = "Bind this line of scarlet thread in the window."
    font = ImageFont.truetype(F_GEORGIA_I, 47)
    pad = 30
    lines = wrap(text, font, int(W * 0.86) - 2 * pad, d)
    line_h = 47 + 14
    bw = int(W * 0.86)
    bh = line_h * len(lines) + 2 * pad
    box = Image.new("RGBA", (bw, bh), (232, 217, 181, 235))
    bd = ImageDraw.Draw(box)
    rng = random.Random(3)
    pts = []
    corners = [(0, 0), (bw, 0), (bw, bh), (0, bh), (0, 0)]
    for (x0, y0), (x1, y1) in zip(corners, corners[1:]):
        for i in range(9):
            t = i / 9
            pts.append((x0 + (x1 - x0) * t + rng.uniform(-2.5, 2.5),
                        y0 + (y1 - y0) * t + rng.uniform(-2.5, 2.5)))
    pts.append(pts[0])
    bd.line(pts, fill=(*INK, 255), width=5, joint="curve")
    for i, ln in enumerate(lines):
        bd.text((pad, pad + i * line_h), ln, font=font, fill=(*RUBRIC, 255))
    canvas.paste(box, (int((W - bw) / 2), int(H * 0.70)), box)
    label(canvas, "0 -- CURRENT (the hated one): translucent chip + italic serif\n"
                   "structurally identical to ArkAIology's VerseQuoteCard, just recolored",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "0_current_hated.png")
    print("[ok] 0_current_hated")


# ============================================================ 1. SCRIBED INK (page writes itself)
def render_scribed_ink():
    canvas = base_canvas("j06_thread").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    # KUNSTLER's textbbox side-bearings confuse the generic wrap() helper --
    # this verse is short enough to hand-break into 2 balanced lines instead.
    lines = ["Bind this line of scarlet thread", "in the window."]
    font = ImageFont.truetype(F_KUNSTLER, 54)
    # KUNSTLER's comma/period glyphs are nearly invisible at body size (~16x7px
    # ink bbox) -- verbatim KJV punctuation was silently disappearing. Found
    # during the thread_v2 skill-adaptation POC (2026-07-28); fix backported
    # here: draw punctuation from a larger stroked instance of the SAME font
    # (advance width from the body-size font, so spacing/centering don't shift).
    PUNCT = set(".,;:'’“”")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(54 * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 26)
    y = int(H * 0.665)
    rng = random.Random(11)

    def char_w(ch):
        return d.textlength(ch, font=font)

    last_lw = 0
    last_x0 = 0
    for ln in lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (W - tw) / 2
        last_lw, last_x0 = tw, x
        # hand-inked wobble: draw letter by letter with tiny baseline jitter
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.5, 2.5)
            jr = rng.uniform(-1.2, 1.2)
            draw_font = font_punct if ch in PUNCT else font
            layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.text((10, 10), ch, font=draw_font, fill=(*INK, 255), stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*INK, 255))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + 32))
            canvas.alpha_composite(layer, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)  # advance from body-size font -- spacing unaffected
        y += 70
    # a thin hand-drawn underline swash beneath the last line, then the reference
    d = ImageDraw.Draw(canvas)
    lw, lx0 = last_lw, last_x0
    swash = [(lx0, y - 10)]
    for i in range(1, 9):
        swash.append((lx0 + lw * i / 8, y - 10 + rng.uniform(-3, 3)))
    d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
    ref = "JOSHUA 2:18"
    rb = d.textbbox((0, 0), ref, font=ref_font)
    d.text(((W - (rb[2] - rb[0])) // 2, y + 14), ref, font=ref_font, fill=(*RUBRIC, 235))
    label(canvas, "1 -- SCRIBED INK: hand-written script, no box, ties into the\n"
                   "'page draws itself' ink-in device already in the comic pipeline",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "1_scribed_ink.png")
    print("[ok] 1_scribed_ink")


# ============================================================ 2. ILLUMINATED RUBRIC
def render_illuminated_rubric():
    canvas = base_canvas("j06_thread").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    text = "ind this line of scarlet thread in the window."
    dropcap_font = ImageFont.truetype(F_OLDENGL, 130)
    body_font = ImageFont.truetype(F_ZILLA_I, 44)
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    y0 = int(H * 0.665)
    # dropped gold-leaf capital "B"
    cap = "B"
    cap_bb = d.textbbox((0, 0), cap, font=dropcap_font)
    cap_w = cap_bb[2] - cap_bb[0]
    # thin hairline rules top/bottom like a real page
    margin = 90
    d.line([(margin, y0 - 22), (W - margin, y0 - 22)], fill=(*FADED_INK, 130), width=2)
    # gold cap with a thin ink outline
    cx = margin
    d.text((cx - cap_bb[0], y0), cap, font=dropcap_font, fill=(*GOLD, 255),
          stroke_width=2, stroke_fill=(*INK, 255))
    body_x0 = cx + cap_w + 18
    max_w = W - margin - body_x0
    lines = wrap(text, body_font, max_w, d)
    ly = y0 + 14
    for i, ln in enumerate(lines):
        x0 = body_x0 if i == 0 else margin
        d.text((x0, ly), ln, font=body_font, fill=(*INK, 255))
        ly += 54
    d.line([(margin, ly + 6), (W - margin, ly + 6)], fill=(*FADED_INK, 130), width=2)
    ref = "JOSHUA  2 : 18"
    rb = d.textbbox((0, 0), ref, font=ref_font)
    d.text(((W - (rb[2] - rb[0])) // 2, ly + 24), ref, font=ref_font, fill=(*RUBRIC, 235))
    label(canvas, "2 -- ILLUMINATED RUBRIC: gold-leaf dropped capital + printed-\n"
                   "Bible serif body + hairline rules, red rubric reference",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "2_illuminated_rubric.png")
    print("[ok] 2_illuminated_rubric")


# ============================================================ 3. PINNED SCRAP
def render_pinned_scrap():
    canvas = base_canvas("j06_thread").convert("RGBA")
    text = "Bind this line of scarlet thread in the window."
    font = ImageFont.truetype(F_GEORGIA_I, 42)
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    pad = 44
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    max_w = int(W * 0.72)
    lines = wrap(text, font, max_w, td)
    line_h = 42 + 16
    bw = max(td.textbbox((0, 0), ln, font=font)[2] for ln in lines) + 2 * pad
    bh = line_h * len(lines) + 2 * pad + 40
    scrap = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrap)
    # torn parchment shape, slightly darker/warmer than the page (a real object laid on it)
    rng = random.Random(19)
    pts = []
    corners = [(20, 20), (bw + 20, 20), (bw + 20, bh + 20), (20, bh + 20), (20, 20)]
    for (x0, y0), (x1, y1) in zip(corners, corners[1:]):
        n = 8
        for i in range(n):
            t = i / n
            jig = 6 if i not in (0,) else 0
            pts.append((x0 + (x1 - x0) * t + rng.uniform(-jig, jig),
                        y0 + (y1 - y0) * t + rng.uniform(-jig, jig)))
    sd.polygon(pts, fill=(222, 202, 160, 255))
    sd.line(pts + [pts[0]], fill=(120, 96, 64, 200), width=2, joint="curve")
    for i, ln in enumerate(lines):
        sd.text((40 + pad - 20, 40 + pad - 20 + i * line_h), ln, font=font, fill=(*INK, 255))
    ref = "Joshua 2:18"
    rb = sd.textbbox((0, 0), ref, font=ref_font)
    sd.text((40 + bw - (rb[2] - rb[0]), 40 + bh - 26), ref, font=ref_font, fill=(*RUBRIC, 230))
    # small red wax-seal dot
    sd.ellipse([40 + 6, 40 + bh - 34, 40 + 30, 40 + bh - 10], fill=(*RUBRIC, 230))
    scrap = scrap.filter(ImageFilter.GaussianBlur(0))
    # drop shadow
    shadow = Image.new("RGBA", scrap.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon(pts, fill=(15, 12, 10, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    scrap_r = scrap.rotate(-2.4, expand=True, resample=Image.BICUBIC)
    shadow_r = shadow.rotate(-2.4, expand=True, resample=Image.BICUBIC)
    ox = (W - scrap_r.width) // 2
    oy = int(H * 0.66)
    canvas.alpha_composite(shadow_r, (ox + 10, oy + 14))
    canvas.alpha_composite(scrap_r, (ox, oy))
    label(canvas, "3 -- PINNED SCRAP: a separate torn parchment note laid onto\n"
                   "the page, rotated, wax-sealed -- a physical object, not a UI card",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "3_pinned_scrap.png")
    print("[ok] 3_pinned_scrap")


# ============================================================ 4. MARGINALIA
def render_marginalia():
    canvas = base_canvas("j06_thread").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    text = "\u201cBind this line of scarlet thread\nin the window.\u201d"
    font = ImageFont.truetype(F_CORMORANT_I, 46)
    ref_font = ImageFont.truetype(F_CORMORANT_I, 32)
    x0, y0 = 100, int(H * 0.70)
    lines = text.split("\n")
    y = y0
    for ln in lines:
        d.text((x0, y), ln, font=font, fill=(*FADED_INK, 255))
        y += 56
    ref = "\u2014 Joshua 2:18"
    d.text((x0 + 30, y + 4), ref, font=ref_font, fill=(*RUBRIC, 220))
    # hand-drawn leader curling up-right toward the thread motif above
    rng = random.Random(5)
    start = (x0 + 40, y0 - 6)
    target = (560, 985)  # the thread swash's midpoint on this still
    leader = [start]
    for i in range(1, 7):
        t = i / 6
        bow = 60 * math.sin(t * math.pi)
        px = start[0] + (target[0] - start[0]) * t - bow * 0.3
        py = start[1] + (target[1] - start[1]) * t + rng.uniform(-4, 4)
        leader.append((px, py))
    d.line(leader, fill=(*FADED_INK, 200), width=2, joint="curve")
    d.ellipse([leader[-1][0] - 5, leader[-1][1] - 5, leader[-1][0] + 5, leader[-1][1] + 5],
              fill=(*RUBRIC, 220))
    label(canvas, "4 -- MARGINALIA: neat annotation in the page's own margin,\n"
                   "no box at all, a hand-drawn leader pointing at the detail",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "4_marginalia.png")
    print("[ok] 4_marginalia")


# ============================================================ 5. DISPLAY-TYPE: current (hated)
def render_display_current():
    canvas = base_canvas("j04_wallface").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(F_ARIBLK, 58)
    text = "THE WALL FELL DOWN FLAT."
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x = (W - tw) // 2
    y = int(H * 0.22)
    pad = 18
    d.rectangle([x - pad, y + int(58 * 0.10), x + tw + pad, y + int(58 * 1.0)],
                fill=(250, 230, 90, 215))
    d.text((x + 4, y + 5), text, font=font, fill=(0, 0, 0, 70))
    d.text((x, y), text, font=font, fill=(*INK, 255))
    label(canvas, "5 -- CURRENT display-type: Arial Black + yellow highlighter\n"
                   "(the internet-explainer grammar, lifted directly)",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "5_display_current.png")
    print("[ok] 5_display_current")


# ============================================================ 6. DISPLAY-TYPE: INK STAMP
def render_display_stamp():
    canvas = base_canvas("j04_wallface").convert("RGBA")
    text = "THE WALL FELL DOWN FLAT"
    font = ImageFont.truetype(F_ZILLA, 70)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 24
    stamp = Image.new("L", (tw + 2 * pad, th + 2 * pad), 0)
    sd = ImageDraw.Draw(stamp)
    sd.text((pad - bb[0], pad - bb[1]), text, font=font, fill=255, stroke_width=2, stroke_fill=255)
    # rough stamped texture: multiply with noise so ink looks unevenly pressed
    rng = random.Random(31)
    noise = Image.new("L", stamp.size)
    noise.putdata([rng.randint(60, 255) for _ in range(stamp.width * stamp.height)])
    noise = noise.filter(ImageFilter.GaussianBlur(1.1))
    import numpy as np
    a = (np.array(stamp).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.6, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))
    inked = Image.new("RGBA", stamp.size, (*RUBRIC, 0))
    inked.putalpha(alpha)
    rot = inked.rotate(-1.4, expand=True, resample=Image.BICUBIC)
    ox = (W - rot.width) // 2
    oy = int(H * 0.20)
    canvas.alpha_composite(rot, (ox, oy))
    label(canvas, "6 -- INK STAMP: rough-pressed rubric-red serif caps, no box,\n"
                   "no highlighter -- reads as pressed onto the page, not typed",
          (30, H - 90), 24, INK)
    canvas.convert("RGB").save(OUT / "6_display_stamp.png")
    print("[ok] 6_display_stamp")


def main():
    render_current_hated()
    render_scribed_ink()
    render_illuminated_rubric()
    render_pinned_scrap()
    render_marginalia()
    render_display_current()
    render_display_stamp()


if __name__ == "__main__":
    main()
