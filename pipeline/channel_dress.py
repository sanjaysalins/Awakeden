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
# website identity (assets/css/site.css): AWAK bone + EDEN red-bright w/ glow,
# Archivo Black — Arial Black (ariblk) is the closest installed face
BONE = (236, 234, 228)      # --bone
RED_BRIGHT = (229, 48, 61)  # --red-bright
SITE_INK = (12, 14, 18)     # --ink
GEORGIA_B = r"C:\Windows\Fonts\georgiab.ttf"
GEORGIA_I = r"C:\Windows\Fonts\georgiai.ttf"
ARIAL_B = r"C:\Windows\Fonts\arialbd.ttf"
ARIAL_BLK = r"C:\Windows\Fonts\ariblk.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(ARIAL_B, size)


def wordmark_width(size: int, tracking: float = 0.14) -> float:
    f = font(ARIAL_BLK, size)
    tmp = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return sum(tmp.textlength(ch, font=f) + size * tracking for ch in "AWAKEDEN")


def draw_split_char(im: Image.Image, xy: tuple, ch: str, f: ImageFont.FreeTypeFont,
                    size: int, c1: tuple, c2: tuple) -> None:
    """Draw one glyph split diagonally: top-left half c1 (bone), bottom-right half c2
    (red) — the shared E where AWAKE becomes EDEN."""
    pad = size // 3
    tile_w, tile_h = size * 2 + pad, size * 2 + pad
    t1 = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    ImageDraw.Draw(t1).text((pad, pad), ch, font=f, fill=c1 + (255,))
    t2 = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    ImageDraw.Draw(t2).text((pad, pad), ch, font=f, fill=c2 + (255,))
    bbox = t1.getbbox()
    if not bbox:
        return
    x0, y0, x1, y1 = bbox
    mask = Image.new("L", (tile_w, tile_h), 0)
    # red = right of the diagonal running from glyph top-right to bottom-left
    ImageDraw.Draw(mask).polygon([(x1, y0), (x1, y1), (x0, y1)], fill=255)
    t1.paste(t2, (0, 0), Image.composite(t2.split()[3], Image.new("L", mask.size, 0), mask))
    im.paste(t1, (int(xy[0]) - pad, int(xy[1]) - pad), t1)


def draw_wordmark(im: Image.Image, x: float, y: float, size: int,
                  tracking: float = 0.14, glow: bool = True, shadow: bool = False) -> float:
    """Site wordmark: AWAK bone + shared split-E + DEN red-bright (glow),
    letterspaced Arial Black — reads as AWAKE and EDEN sharing the E."""
    f = font(ARIAL_BLK, size)
    if glow:
        from PIL import ImageFilter
        gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        cx = x
        for i, ch in enumerate("AWAKEDEN"):
            if i >= 5:
                gd.text((cx, y), ch, font=f, fill=RED_BRIGHT + (160,))
            cx += gd.textlength(ch, font=f) + size * tracking
        gl = gl.filter(ImageFilter.GaussianBlur(size * 0.09))
        im.paste(Image.alpha_composite(im.convert("RGBA"), gl).convert("RGB"), (0, 0))
    dr = ImageDraw.Draw(im, "RGBA")
    cx = x
    for i, ch in enumerate("AWAKEDEN"):
        if shadow:
            dr.text((cx + max(2, size // 30), y + max(2, size // 30)), ch,
                    font=f, fill=(0, 0, 0, 210))
        if i == 4:                       # the shared E: half bone, half red
            draw_split_char(im, (cx, y), ch, f, size, BONE, RED_BRIGHT)
            dr = ImageDraw.Draw(im, "RGBA")
        else:
            dr.text((cx, y), ch, font=f, fill=BONE if i < 4 else RED_BRIGHT)
        cx += dr.textlength(ch, font=f) + size * tracking
    return cx


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

    # site-identity panel at the strip's left, ending BEFORE the face (never over it)
    size = 74
    f_tag = font(GEORGIA_I, 40)
    tag1 = "Finding Jesus in the"
    tag2 = "whole Bible · one panel"
    tag3 = "at a time"
    pad = 30
    pw = max(wordmark_width(size), dr.textlength(tag2, font=f_tag)) + pad * 2
    px0, py0 = sx0 + 20, sy0 + 58
    dr.rounded_rectangle([px0, py0, px0 + pw, py0 + 306], radius=14,
                         fill=SITE_INK + (222,), outline=BONE + (235,), width=3)
    draw_wordmark(im, px0 + pad, py0 + 24, size)
    dr = ImageDraw.Draw(im, "RGBA")
    ty = py0 + 24 + 106
    for tg in (tag1, tag2, tag3):
        dr.text((px0 + pad, ty), tg, font=f_tag, fill=BONE)
        ty += 56

    OUT.mkdir(exist_ok=True)
    p = OUT / "channel_banner.png"
    im.save(p)
    # safe-strip preview so the user can check what phones/desktop show
    im.crop((sx0, sy0, sx1, sy1)).save(OUT / "channel_banner_SAFE_PREVIEW.png")
    print(f"banner  -> {p}")


def fit_word_size(max_w: float, tracking: float = 0.08) -> int:
    """Largest font size whose AWAKEDEN width fits max_w (grows from tiny)."""
    size = 8
    while wordmark_width(size + 2, tracking) <= max_w:
        size += 2
    return size


def word_bbox(size: int, tracking: float = 0.08) -> tuple:
    """(w, cap_top, cap_bottom) of the drawn word, measured, for true centering."""
    w = int(wordmark_width(size, tracking)) + size
    tmp = Image.new("RGBA", (w, size * 3), (0, 0, 0, 0))
    dr = ImageDraw.Draw(tmp)
    f = font(ARIAL_BLK, size)
    cx = 0.0
    for ch in "AWAKEDEN":
        dr.text((cx, size), ch, font=f, fill=(255, 255, 255, 255))
        cx += dr.textlength(ch, font=f) + size * tracking
    bb = tmp.getbbox()
    return (bb[2] - bb[0]), bb[1] - size, bb[3] - size   # width, top-off, bottom-off


def draw_word_centered(im: Image.Image, box: tuple, tracking: float = 0.08,
                       glow: bool = False) -> None:
    """Draw the one-word mark optically centered inside box=(x0,y0,x1,y1)."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    size = fit_word_size(bw, tracking)
    w, top_off, bot_off = word_bbox(size, tracking)
    glyph_h = bot_off - top_off
    x = box[0] + (bw - w) / 2
    y = box[1] + (bh - glyph_h) / 2 - top_off
    draw_wordmark(im, x, y, size, tracking=tracking, glow=glow)


def avatar():
    """ONE word — AWAKEDEN — centered inside the CIRCLE YouTube crops to:
    the word box is the inscribed-safe 72% band, so the round mask never clips it."""
    px = 800
    im = Image.new("RGB", (px, px), SITE_INK)
    m = px * 0.14                                   # circle-safe margin
    draw_word_centered(im, (m, px * 0.40, px - m, px * 0.56), glow=True)
    dr = ImageDraw.Draw(im)
    dr.rectangle([px * 0.36, px * 0.60, px * 0.64, px * 0.607], fill=BONE)
    p = OUT / "channel_avatar.png"
    im.save(p)
    # round preview — exactly what the circular crop shows
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, px, px], fill=255)
    prev = Image.new("RGB", (px, px), (255, 255, 255))
    prev.paste(im, (0, 0), mask)
    prev.save(OUT / "channel_avatar_ROUND_PREVIEW.png")
    print(f"avatar  -> {p}")


if __name__ == "__main__":
    banner()
    avatar()
