"""Two more real POCs, on the second-pass ArkAIology audit:
  7. THREAD device -- two verse cards (Gen 1:1 / John 1:1, verified verbatim)
     stitched by a real gold thread. Adapted from ArkAIology's /threads
     ThreadCard, using OUR Scribed-Ink hand lettering instead of theirs.
  8. CIRCLED WORD -- a single word hand-circled in gold ink on our
     Illuminated Rubric block. Adapted from ArkAIology's /vox-type
     `circled` treatment (their own "v1 felt alien -> rebuilt as house
     artifact" lesson independently confirms today's caption diagnosis).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_lettering_compare/_render_new_finds.py
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
FADED_INK = (70, 62, 54)

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_OLDENGL = "C:/Windows/Fonts/OLDENGL.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_ZILLA_I = "C:/Windows/Fonts/ZillaSlab-Italic.ttf"


def base_canvas(still_name):
    im = Image.open(JERICHO / "stills" / f"{still_name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def aged_paper_canvas(seed=41):
    rng = random.Random(seed)
    base = Image.new("RGB", (W, H), (238, 226, 194))
    grain = Image.new("L", (W // 3, H // 3))
    grain.putdata([rng.randint(118, 138) for _ in range(grain.width * grain.height)])
    grain = grain.resize((W, H), Image.BICUBIC)
    from PIL import ImageEnhance
    base = Image.composite(ImageEnhance.Brightness(base).enhance(0.94), base,
                           grain.point(lambda v: max(0, (v - 128) * 6)))
    return base


def label(img, text, xy, size=24, color=INK):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(F_ZILLA, size)
    d.text(xy, text, font=f, fill=color)


def wobbled_rect(draw, box, seed, width=3):
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    pts = []
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    for (a, b), (c, d_) in zip(corners, corners[1:]):
        for i in range(7):
            t = i / 7
            pts.append((a + (c - a) * t + rng.uniform(-2.5, 2.5),
                        b + (d_ - b) * t + rng.uniform(-2.5, 2.5)))
    pts.append(pts[0])
    draw.line(pts, fill=(*FADED_INK, 160), width=width, joint="curve")


# ============================================================ 7. THREAD DEVICE
def render_thread_device():
    canvas = aged_paper_canvas().convert("RGBA")
    d = ImageDraw.Draw(canvas)
    body_font = ImageFont.truetype(F_ZILLA_I, 40)
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    kicker_font = ImageFont.truetype(F_ZILLA, 22)

    card1 = dict(kicker="GENESIS 1:1", text="In the beginning God created\nthe heaven and the earth.",
                y=int(H * 0.18))
    card2 = dict(kicker="JOHN 1:1", text="In the beginning was the Word,\nand the Word was with God.",
                y=int(H * 0.52))
    anchors = []
    for card in (card1, card2):
        margin = 110
        d.text((margin, card["y"] - 34), card["kicker"], font=kicker_font, fill=(*RUBRIC, 230))
        wobbled_rect(d, (margin - 20, card["y"] - 4, W - margin + 20, card["y"] + 150), seed=hash(card["kicker"]))
        y = card["y"] + 14
        first_line_x0 = margin
        for ln in card["text"].split("\n"):
            d.text((margin, y), ln, font=body_font, fill=(*INK, 255))
            y += 52
        d.text((W - margin - ref_font.getbbox(card['kicker'])[2], card["y"] + 150 + 10),
              "", font=ref_font, fill=(*RUBRIC, 200))
        # anchor point = end of "In the beginning" on line 1 (approx x for stitch attach)
        anchor_w = d.textlength("In the beginning", font=body_font)
        anchors.append((margin + anchor_w, card["y"] + 14 + 20))

    # gold stitched thread connecting the shared phrase between the two cards
    x0, y0 = anchors[0]
    x1, y1 = anchors[1]
    rng = random.Random(9)
    n = 14
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + 26 * math.sin(t * math.pi * 2.4)
        pts.append((x, y))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(*GOLD, 255), width=4)
    d.ellipse([x0 - 6, y0 - 6, x0 + 6, y0 + 6], fill=(*GOLD, 255))
    d.ellipse([x1 - 6, y1 - 6, x1 + 6, y1 + 6], fill=(*GOLD, 255))

    tag_font = ImageFont.truetype(F_ZILLA, 26)
    tag = "THREAD \u2116 1  \u00b7  KJV VERBATIM \u00b7 GENESIS \u2192 JOHN"
    tw = d.textlength(tag, font=tag_font)
    d.text(((W - tw) / 2, int(H * 0.80)), tag, font=tag_font, fill=(*FADED_INK, 220))

    label(canvas, "7 -- THREAD DEVICE (adapted from /threads): two Scribed-Ink\n"
                   "verse cards stitched by a real gold thread -- the whole-Bible-\n"
                   "through-Jesus doctrine, made a literal on-screen object",
          (30, H - 130), 24, INK)
    canvas.convert("RGB").save(OUT / "7_thread_device.png")
    print("[ok] 7_thread_device")


# ============================================================ 8. CIRCLED WORD
def render_circled_word():
    canvas = base_canvas("j06_thread").convert("RGBA")
    d = ImageDraw.Draw(canvas)
    dropcap_font = ImageFont.truetype(F_OLDENGL, 130)
    body_font = ImageFont.truetype(F_ZILLA_I, 44)
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    y0 = int(H * 0.665)
    margin = 90
    d.line([(margin, y0 - 22), (W - margin, y0 - 22)], fill=(*FADED_INK, 130), width=2)
    cap = "B"
    cap_bb = d.textbbox((0, 0), cap, font=dropcap_font)
    cap_w = cap_bb[2] - cap_bb[0]
    d.text((margin - cap_bb[0], y0), cap, font=dropcap_font, fill=(*GOLD, 255),
          stroke_width=2, stroke_fill=(*INK, 255))
    body_x0 = margin + cap_w + 18
    words = ["ind", "this", "line", "of", "scarlet", "thread", "in", "the", "window."]
    x = body_x0
    scarlet_box = None
    for w_ in words:
        d.text((x, y0 + 14), w_, font=body_font, fill=(*INK, 255))
        ww = d.textlength(w_ + " ", font=body_font)
        if w_ == "scarlet":
            wb = d.textlength(w_, font=body_font)
            scarlet_box = (x, y0 + 14, x + wb, y0 + 14 + 50)
        x += ww
    d.line([(margin, y0 + 68), (W - margin, y0 + 68)], fill=(*FADED_INK, 130), width=2)
    ref = "JOSHUA  2 : 18"
    rb = d.textlength(ref, font=ref_font)
    d.text(((W - rb) / 2, y0 + 86), ref, font=ref_font, fill=(*RUBRIC, 235))

    # hand-circled in gold around the word "scarlet" -- forensic pointing
    if scarlet_box:
        bx0, by0, bx1, by1 = scarlet_box
        cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2 + 4
        rx, ry = (bx1 - bx0) / 2 + 18, (by1 - by0) / 2 + 16
        rng = random.Random(21)
        pts = []
        for i in range(38):
            a = -math.pi / 2 + i / 36 * 2 * math.pi * 1.06
            pts.append((cx + (rx + rng.uniform(-3, 3)) * math.cos(a),
                        cy + (ry + rng.uniform(-3, 3)) * math.sin(a)))
        d.line(pts, fill=(*GOLD, 255), width=5, joint="curve")

    label(canvas, "8 -- CIRCLED WORD (adapted from /vox-type 'circled'):\n"
                   "forensic gold-ink circle on ONE word -- their own house lesson\n"
                   "was 'v1 felt alien -> rebuilt as a diegetic page artifact'",
          (30, H - 100), 24, INK)
    canvas.convert("RGB").save(OUT / "8_circled_word.png")
    print("[ok] 8_circled_word")


def main():
    render_thread_device()
    render_circled_word()


if __name__ == "__main__":
    main()
