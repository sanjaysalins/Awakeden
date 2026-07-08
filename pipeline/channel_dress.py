"""pipeline/channel_dress.py — $0 YouTube channel banner + avatar.

Banner: 2560x1440 from the inked crane_cross_soldiers still (Psalm-22 rebuild),
composed so the face + outstretched arms sit inside the 1546x423 all-device safe
strip, with the red AWAKEDEN wordmark + tagline on the sand at the left of the strip.
Avatar: 800x800 ivory disc, red ring, Georgia 'A' - matches the watermark identity.

  .venv\\Scripts\\python.exe pipeline/channel_dress.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1"
       / "visual_16x9_inked" / "crane_cross_soldiers.png")
OUT = ROOT / "_brand"

RED = (168, 35, 29)
IVORY = (245, 240, 208)
INK = (18, 14, 10)
GEORGIA_B = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA_I = r"C:\Windows\Fonts\georgiai.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(ARIAL_B, size)


def banner():
    W, H = 2560, 1440
    sx0, sy0, sx1, sy1 = 507, 508, 2053, 931          # all-device safe strip
    img = Image.open(SRC).convert("RGB")

    # cover-crop; bias so the face (upper-middle of source) sits mid-safe-strip
    sw, sh = img.size
    scale = max(W / sw, H / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    sw, sh = img.size
    # shift the subject right-of-center so the wordmark owns the left of the strip
    x = max(0, (sw - W) // 2 - 520)
    y = max(0, min(round(sh * 0.10), sh - H))          # keep the dark sky + face high
    im = img.crop((x, y, x + W, y + H))
    dr = ImageDraw.Draw(im, "RGBA")

    # comic caption box at the strip's left, ending BEFORE the face (never over it)
    f_word = font(ARIAL_B, 88)
    f_tag = font(GEORGIA_I, 40)
    word = "AWAKEDEN"
    tag1 = "Finding Jesus in the"
    tag2 = "whole Bible · one panel"
    tag3 = "at a time"
    pad = 26
    pw = max(dr.textlength(word, font=f_word),
             dr.textlength(tag2, font=f_tag)) + pad * 2
    px0, py0 = sx0 + 20, sy0 + 62
    dr.rounded_rectangle([px0, py0, px0 + pw, py0 + 300], radius=16,
                         fill=INK + (205,), outline=IVORY + (235,), width=3)
    ty = py0 + 20
    dr.text((px0 + pad + 2, ty + 2), word, font=f_word, fill=(0, 0, 0, 220))
    dr.text((px0 + pad, ty), word, font=f_word, fill=RED)
    ty += 106
    for tg in (tag1, tag2, tag3):
        dr.text((px0 + pad, ty), tg, font=f_tag, fill=IVORY)
        ty += 54

    OUT.mkdir(exist_ok=True)
    p = OUT / "channel_banner.png"
    im.save(p)
    # safe-strip preview so the user can check what phones/desktop show
    im.crop((sx0, sy0, sx1, sy1)).save(OUT / "channel_banner_SAFE_PREVIEW.png")
    print(f"banner  -> {p}")


def avatar():
    px = 800
    im = Image.new("RGB", (px, px), IVORY)
    dr = ImageDraw.Draw(im)
    ring = 26
    dr.ellipse([ring, ring, px - ring, px - ring], outline=RED, width=ring)
    f = font(GEORGIA_B, 470)
    w = dr.textlength("A", font=f)
    dr.text(((px - w) / 2, px * 0.115), "A", font=f, fill=RED)
    # small ink tagline dot-rule under the A
    dr.rectangle([px * 0.34, px * 0.80, px * 0.66, px * 0.815], fill=INK)
    p = OUT / "channel_avatar.png"
    im.save(p)
    print(f"avatar  -> {p}")


if __name__ == "__main__":
    banner()
    avatar()
