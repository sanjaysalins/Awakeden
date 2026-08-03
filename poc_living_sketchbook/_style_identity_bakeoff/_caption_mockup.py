"""Quick mockup: composite real, chosen hand-script captions + a wobbled
leader line onto the clean (text-free) sl20 v2 renders -- proves out
"controlled text" the RIGHT way (deterministic overlay, same font family
this project's Scribed Ink already uses), not by asking the image model
to spell. Positions are rough/eyeballed for review purposes -- nudge
after the user picks final words/spots, not meant to be pixel-perfect yet.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_PATH = Path("C:/Windows/Fonts/KUNSTLER.TTF")
INK = (40, 32, 24, 255)

# (label, anchor_xy in ORIGINAL 1536x2752 px, text_offset_xy)
MOSES_LABELS = [
    ("profile study", (385, 344), (-40, -70)),
    ("grip", (1294, 317), (60, -30)),
    ("boot", (317, 2518), (-90, 40)),
    ("thumbprint", (1314, 1142), (90, -10)),
]
JESUS_LABELS = [
    ("profile study", (385, 358), (-40, -70)),
    ("sandal", (1238, 2573), (70, 30)),
    ("hand", (812, 2271), (-100, 30)),
    ("thumbprint", (1390, 1541), (-160, -10)),
]


def wobbled_line(draw, p0, p1, seed):
    rnd = random.Random(seed)
    steps = 12
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = p0[0] + (p1[0] - p0[0]) * t + rnd.uniform(-3, 3)
        y = p0[1] + (p1[1] - p0[1]) * t + rnd.uniform(-3, 3)
        pts.append((x, y))
    draw.line(pts, fill=INK, width=3)


def composite(src_path: Path, labels: list, out_path: Path, font_size=42, margin=24):
    img = Image.open(src_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    for i, (text, anchor, offset) in enumerate(labels):
        text_xy = [anchor[0] + offset[0], anchor[1] + offset[1]]
        # clamp so the label text can never run off the page, regardless
        # of how the offset was eyeballed -- the one real bug this mockup
        # round caught (Jesus's "thumbprint" ran off the right edge)
        l, t, r, b = draw.textbbox(tuple(text_xy), text, font=font)
        if r > img.width - margin:
            text_xy[0] -= (r - (img.width - margin))
        if l < margin:
            text_xy[0] += (margin - l)
        if b > img.height - margin:
            text_xy[1] -= (b - (img.height - margin))
        if t < margin:
            text_xy[1] += (margin - t)
        text_xy = tuple(text_xy)
        wobbled_line(draw, anchor, text_xy, seed=i)
        # small dot at the studied detail
        r_dot = 6
        draw.ellipse([anchor[0] - r_dot, anchor[1] - r_dot, anchor[0] + r_dot, anchor[1] + r_dot], fill=INK)
        draw.text(text_xy, text, font=font, fill=INK)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(out_path)
    print(f"[out] {out_path}")


def main():
    composite(HERE / "stills" / "sl20_sketchbook_spread_v2.png", MOSES_LABELS,
              HERE / "stills" / "sl20_sketchbook_spread_v2_captioned_MOCKUP.png")
    composite(HERE / "stills_jesus" / "sl20_sketchbook_spread_v2.png", JESUS_LABELS,
              HERE / "stills_jesus" / "sl20_sketchbook_spread_v2_captioned_MOCKUP.png")


if __name__ == "__main__":
    main()
