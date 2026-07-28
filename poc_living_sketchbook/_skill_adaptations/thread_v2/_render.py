"""Thread Device v2 -- two refined variants fixing the v1 POC's "UI chip"
problem (two wobbled-rectangle verse cards = the exact box shape the
rebuilt lettering system (SKILL.md Sec.5) now forbids for single verse
reveals) and its wrong font (plain italic Georgia instead of the house
Scribed-Ink hand-lettering, Kunstler Script).

  A. NO BOX      -- both verses hand-written directly on the open page,
                     no rectangle anywhere; a gold stitched thread (dash
                     technique from render_thread_device) is the only
                     device signalling the two verses are linked.
  B. UNIFIED CARD -- ONE torn-parchment scrap (torn-edge polygon + drop
                     shadow + rotation, technique from render_pinned_scrap)
                     holding BOTH verses stacked inside it, so "these two
                     verses are linked" is tested as a single physical
                     object instead of two boxes.

Composited onto real episode art (jericho/stills/j06_thread.png) so both
can be judged in a realistic context, not on blank paper.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/thread_v2/_render.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
STILL = HERE.parents[1] / "jericho" / "stills" / "j06_thread.png"
OUT = HERE
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"

# ---- verses (KJV verbatim, pre-verified against pipeline.scripture tonight) ----
GEN_REF = "GENESIS 1:1"
GEN_LINES = ["In the beginning God created", "the heaven and the earth."]
JOHN_REF = "JOHN 1:1"
JOHN_LINES = ["In the beginning was the Word,", "and the Word was with God,",
              "and the Word was God."]
SHARED_PHRASE = "In the beginning"

# Safe-zone guide rails (SKILL.md Sec.5 letterer laws):
# watermark top-left x~40-240/y~70-160; bottom ~18% UI band = y > H*0.82.
# The still's gold-leaf spine sits at roughly x=985-1055 -- keep clear of it too.
TOP_SAFE_Y = 175
BOTTOM_SAFE_Y = int(H * 0.82) - 15  # 1561, a little inside the 18% line
SAFE_CX = 478  # visual center of the WRITABLE page (page is 0..~985, spine beyond)


def base_canvas():
    im = Image.open(STILL).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def torn_polygon(rng, x0, y0, x1, y1, n=8, jig=6):
    """Torn-parchment edge, technique lifted from render_pinned_scrap()."""
    pts = []
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    for (ax, ay), (bx, by) in zip(corners, corners[1:]):
        for i in range(n):
            t = i / n
            pts.append((ax + (bx - ax) * t + rng.uniform(-jig, jig),
                        ay + (by - ay) * t + rng.uniform(-jig, jig)))
    return pts


def char_widths(draw, text, font):
    # Kunstler's textbbox() side-bearings are unreliable for centering --
    # sum per-character textlength() instead (render_scribed_ink() gotcha).
    return [draw.textlength(ch, font=font) for ch in text]


PUNCT = ",.;:"


def draw_scribed_line(canvas, draw, text, font, cx_center, y, seed=0, jitter=2.2, ink=INK):
    """Hand-inked script line, centered at cx_center, top-of-glyph at y.
    Returns per-char x positions/widths so callers can find a phrase anchor.

    Kunstler's comma/period glyphs measure only a few px of ink at these
    sizes (verified: bbox ~16x7px at 80pt) -- effectively invisible against
    the paper texture, which would silently drop verbatim KJV punctuation.
    Punctuation is drawn from a ~1.7x, lightly stroked font so it stays
    legible; it does NOT affect the advance width, so letter spacing/
    centering math (and the proven cursive rhythm) is untouched.
    """
    rng = random.Random(seed)
    widths = char_widths(draw, text, font)
    tw = sum(widths)
    x0 = cx_center - tw / 2
    xs = []
    cx = x0
    punct_font = ImageFont.truetype(font.path, int(font.size * 1.7))
    for ch, wch in zip(text, widths):
        xs.append(cx)
        jy = rng.uniform(-jitter, jitter)
        jr = rng.uniform(-1.1, 1.1)
        layer = Image.new("RGBA", (110, 120), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        if ch in PUNCT:
            ld.text((12, 12), ch, font=punct_font, fill=(*ink, 255), stroke_width=1, stroke_fill=(*ink, 255))
        else:
            ld.text((12, 12), ch, font=font, fill=(*ink, 255))
        layer = layer.rotate(jr, resample=Image.BICUBIC, center=(12, 12 + 34))
        canvas.alpha_composite(layer, (int(cx) - 12, int(y + jy) - 12))
        cx += wch
    return {"text": text, "x0": x0, "tw": tw, "xs": xs, "widths": widths, "y": y}


def phrase_anchor(line_info, phrase, y_offset):
    """x-center of `phrase`, y placed in the WHITESPACE beside the line (not
    on top of the ink) -- a positive y_offset lands the anchor dot below this
    line (the gap before the next line); a negative one lands it above."""
    idx = line_info["text"].index(phrase)
    end = idx + len(phrase)
    x_start = line_info["xs"][idx]
    x_end = line_info["xs"][end - 1] + line_info["widths"][end - 1]
    return ((x_start + x_end) / 2, line_info["y"] + y_offset)


def draw_ref_stamp(draw, text, font, cx_center, y, color=RUBRIC):
    tw = draw.textlength(text, font=font)
    draw.text((cx_center - tw / 2, y), text, font=font, fill=(*color, 235))
    return tw


def draw_gold_thread(draw, p0, p1, seed=9, n=16, bow=90, width=4):
    """Gold stitched thread: a single gentle bow (not a UI connector line),
    dashed via the same 'draw every other segment of pts' technique as the
    original render_thread_device -- swung to one side so it clears any
    reference-stamp text sitting between the two anchors."""
    rng = random.Random(seed)
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + dx * t
        y = y0 + dy * t
        off = bow * math.sin(t * math.pi) + rng.uniform(-3, 3)
        pts.append((x + nx * off, y + ny * off))
    for i in range(0, len(pts) - 1, 2):
        draw.line([pts[i], pts[i + 1]], fill=(*GOLD, 255), width=width)
    r = width + 2
    draw.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=(*GOLD, 255))
    draw.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=(*GOLD, 255))


# ============================================================ VARIANT A -- NO BOX
def render_variant_a():
    canvas = base_canvas().convert("RGBA")
    d = ImageDraw.Draw(canvas)
    verse_font = ImageFont.truetype(F_KUNSTLER, 50)
    ref_font = ImageFont.truetype(F_ZILLA, 26)
    line_h = 80

    # Genesis block -- upper page, above the still's own ribbon motif
    y = 300
    gen_infos = []
    for i, line in enumerate(GEN_LINES):
        info = draw_scribed_line(canvas, d, line, verse_font, SAFE_CX, y, seed=101 + i)
        gen_infos.append(info)
        y += line_h
    d = ImageDraw.Draw(canvas)
    draw_ref_stamp(d, GEN_REF, ref_font, SAFE_CX, y + 8)
    gen_block_bottom = y + 8 + 34

    # John block -- lower page, below the ribbon motif
    y2 = 1140
    john_infos = []
    for i, line in enumerate(JOHN_LINES):
        info = draw_scribed_line(canvas, d, line, verse_font, SAFE_CX, y2, seed=201 + i)
        john_infos.append(info)
        y2 += line_h
    d = ImageDraw.Draw(canvas)
    draw_ref_stamp(d, JOHN_REF, ref_font, SAFE_CX, y2 + 8)
    john_block_bottom = y2 + 8 + 34

    # gold stitched thread: shared phrase (verse 1) -> shared phrase (verse 2).
    # Anchors sit in the whitespace beside each phrase (below Genesis's line 1,
    # above John's line 1) so the dot never lands on top of a letter.
    p0 = phrase_anchor(gen_infos[0], SHARED_PHRASE, y_offset=line_h - 12)
    p1 = phrase_anchor(john_infos[0], SHARED_PHRASE, y_offset=-16)
    d = ImageDraw.Draw(canvas)
    draw_gold_thread(d, p0, p1, bow=130, width=4)

    print(f"[A] genesis block: 300..{gen_block_bottom}  john block: 1140..{john_block_bottom}")
    print(f"[A] safe window: {TOP_SAFE_Y}..{BOTTOM_SAFE_Y}  thread anchors: {p0} -> {p1}")

    out = OUT / "variant_a_nobox.png"
    canvas.convert("RGB").save(out)
    print(f"[ok] {out}")


# ============================================================ VARIANT B -- ONE UNIFIED CARD
def render_variant_b():
    verse_size = 40
    ref_size = 22
    line_h = 64
    pad = 64
    block_gap = 50
    rot_angle = -2.2

    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    verse_font = ImageFont.truetype(F_KUNSTLER, verse_size)
    ref_font = ImageFont.truetype(F_ZILLA, ref_size)

    def line_w(text):
        return sum(td.textlength(ch, font=verse_font) for ch in text)

    content_w = max([line_w(l) for l in GEN_LINES] + [line_w(l) for l in JOHN_LINES] +
                     [td.textlength(GEN_REF, font=ref_font), td.textlength(JOHN_REF, font=ref_font)])
    bw = int(content_w) + 2 * pad
    gen_block_h = line_h * len(GEN_LINES) + 14 + ref_size
    john_block_h = line_h * len(JOHN_LINES) + 14 + ref_size
    bh = gen_block_h + block_gap + john_block_h + 2 * pad

    margin = 22  # extra room around the polygon for the torn jag + wax seal
    scrap = Image.new("RGBA", (bw + 2 * margin, bh + 2 * margin), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrap)
    rng = random.Random(19)
    pts = torn_polygon(rng, margin, margin, margin + bw, margin + bh)
    sd.polygon(pts, fill=(224, 204, 163, 255))
    sd.line(pts + [pts[0]], fill=(120, 96, 64, 200), width=2, joint="curve")

    cx_local = (bw + 2 * margin) / 2
    y = margin + pad
    gen_infos = []
    for i, line in enumerate(GEN_LINES):
        info = draw_scribed_line(scrap, sd, line, verse_font, cx_local, y, seed=101 + i, jitter=1.5)
        gen_infos.append(info)
        y += line_h
    sd = ImageDraw.Draw(scrap)
    draw_ref_stamp(sd, GEN_REF, ref_font, cx_local, y + 8)
    y += 8 + ref_size + block_gap

    john_infos = []
    for i, line in enumerate(JOHN_LINES):
        info = draw_scribed_line(scrap, sd, line, verse_font, cx_local, y, seed=201 + i, jitter=1.5)
        john_infos.append(info)
        y += line_h
    sd = ImageDraw.Draw(scrap)
    draw_ref_stamp(sd, JOHN_REF, ref_font, cx_local, y + 8)
    content_bottom = y + 8 + ref_size

    # gold stitch entirely inside the one scrap -- anchors sit in the gap
    # below Genesis's line 1 and above John's line 1, never on top of a letter
    p0 = phrase_anchor(gen_infos[0], SHARED_PHRASE, y_offset=line_h - 12)
    p1 = phrase_anchor(john_infos[0], SHARED_PHRASE, y_offset=-14)
    sd = ImageDraw.Draw(scrap)
    draw_gold_thread(sd, p0, p1, bow=60, width=3)

    # small wax seal, bottom-left corner of the scrap (pinned-scrap register)
    sd.ellipse([margin + 8, margin + bh - 34, margin + 32, margin + bh - 10], fill=(*RUBRIC, 230))

    print(f"[B] scrap content: {bw}x{bh}  content_bottom={content_bottom}  bh={bh}")

    # drop shadow (same polygon, blurred, offset) + slight rotation -- render_pinned_scrap technique
    shadow = Image.new("RGBA", scrap.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon(pts, fill=(15, 12, 10, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    scrap_r = scrap.rotate(rot_angle, expand=True, resample=Image.BICUBIC)
    shadow_r = shadow.rotate(rot_angle, expand=True, resample=Image.BICUBIC)

    canvas = base_canvas().convert("RGBA")
    ox = int(SAFE_CX - scrap_r.width / 2)
    oy = TOP_SAFE_Y + 40
    if oy + scrap_r.height > BOTTOM_SAFE_Y:
        oy = max(TOP_SAFE_Y + 40, BOTTOM_SAFE_Y - scrap_r.height)
    canvas.alpha_composite(shadow_r, (ox + 10, oy + 14))
    canvas.alpha_composite(scrap_r, (ox, oy))

    print(f"[B] scrap_r size: {scrap_r.size}  placed at ({ox},{oy})  "
          f"right_edge={ox + scrap_r.width}  bottom_edge={oy + scrap_r.height}  "
          f"safe window: {TOP_SAFE_Y}..{BOTTOM_SAFE_Y}")

    out = OUT / "variant_b_unified_card.png"
    canvas.convert("RGB").save(out)
    print(f"[ok] {out}")


def main():
    render_variant_a()
    render_variant_b()


if __name__ == "__main__":
    main()
