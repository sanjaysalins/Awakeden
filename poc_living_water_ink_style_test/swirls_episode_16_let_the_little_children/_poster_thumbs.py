"""Ep16 poster thumbs (2026-11-14): owner picked poster D2 (NBP, Jesus upset holding the curly-haired girl).
Title on the art: NOT NOW (pairs with the YouTube title 'Why Jesus Was Angry'). Writes publish/thumbs/thumb_{9x16,16x9,1x1}.jpg.
Old thumbs kept in publish/thumbs/_old_v1/."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
from pipeline.thumbnails import cover_crop, _font  # noqa: E402
from pipeline.channel_dress import draw_wordmark, wordmark_width  # noqa: E402

ART = Image.open(HERE / "_packaging/poster_r1/art/D2_girl_nbp.png").convert("RGB")
BOLD = r"C:\Windows\Fonts\georgiab.ttf"
REG = r"C:\Windows\Fonts\georgia.ttf"
TITLE, REF = "NOT NOW", "Mark 10:13-16"
CREAM = (246, 238, 210, 255)


def shade(im, top_frac, bot_frac, top_a=200, bot_a=210):
    """dark gradients top + bottom so type reads; middle (faces) untouched"""
    W, H = im.size
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    th, bh = int(H * top_frac), int(H * bot_frac)
    for y in range(th):
        d.line([(0, y), (W, y)], fill=(12, 8, 4, int(top_a * (1 - y / th) ** 1.3)))
    for y in range(bh):
        d.line([(0, H - 1 - y), (W, H - 1 - y)], fill=(12, 8, 4, int(bot_a * (1 - y / bh) ** 1.3)))
    return Image.alpha_composite(im.convert("RGBA"), ov)


def text_c(dr, cx, y, s, f, fill=CREAM, sh=6):
    w = dr.textlength(s, font=f)
    dr.text((cx - w / 2 + sh * .6, y + sh), s, font=f, fill=(0, 0, 0, 210))
    dr.text((cx - w / 2, y), s, font=f, fill=fill)


def fit(dr, s, maxw, start):
    size = start
    while dr.textlength(s, font=_font(BOLD, size)) > maxw and size > 30:
        size -= 4
    return _font(BOLD, size), size


def vertical(W, H, out, title_y=0.055, crop_y=0.0):
    im = cover_crop(ART, W, H) if crop_y == 0 else ART
    if crop_y:
        sc = W / ART.width
        r = ART.resize((W, int(ART.height * sc)), Image.LANCZOS)
        y0 = int((r.height - H) * crop_y)
        im = r.crop((0, y0, W, y0 + H))
    im = shade(im, 0.30, 0.20)
    dr = ImageDraw.Draw(im)
    f, size = fit(dr, TITLE, W * 0.86, int(W * 0.20))
    text_c(dr, W / 2, int(H * title_y), TITLE, f)
    bs = int(W * 0.034)
    fr = _font(REG, int(bs * 1.15))
    text_c(dr, W / 2, H - int(bs * 4.6), REF, fr, sh=3)
    draw_wordmark(im, (W - wordmark_width(bs)) / 2, H - int(bs * 2.4), bs, glow=False, shadow=True)
    im.convert("RGB").save(out, quality=92)
    print(out, size)


T = HERE / "publish" / "thumbs"
vertical(1080, 1920, T / "thumb_9x16.jpg")
vertical(1080, 1080, T / "thumb_1x1.jpg", crop_y=0.18)

# 16:9: blurred bg, poster right at full height, words left
W, H = 1280, 720
bg = cover_crop(ART, W, H).filter(ImageFilter.GaussianBlur(28))
bg = Image.eval(bg, lambda p: int(p * 0.40))
dr = ImageDraw.Draw(bg, "RGBA")
ph = int(H * 0.90); pw = int(ART.width * ph / ART.height)
px, py = W - pw - 60, (H - ph) // 2
dr.rectangle([px - 4, py - 4, px + pw + 3, py + ph + 3], outline=(200, 190, 160, 255), width=3)
bg.paste(ART.resize((pw, ph), Image.LANCZOS), (px, py))
colw = px - 60 - 50
cx = 60 + colw / 2
f1, s1 = fit(dr, "NOT", colw, 200)
lh = int(s1 * 1.0)
ty = H // 2 - lh - 50
text_c(dr, cx, ty, "NOT", f1)
text_c(dr, cx, ty + lh, "NOW", f1)
fr = _font(REG, int(s1 * 0.22))
ry = ty + 2 * lh + 30
text_c(dr, cx, ry, REF, fr, sh=3)
bs = 32
draw_wordmark(bg, cx - wordmark_width(bs) / 2, ry + int(s1 * 0.22) + 36, bs, glow=False, shadow=True)
bg.convert("RGB").save(T / "thumb_16x9.jpg", quality=92)
print(T / "thumb_16x9.jpg", s1)
