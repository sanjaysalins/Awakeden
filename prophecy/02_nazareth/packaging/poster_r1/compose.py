"""Nazareth poster r1: real type (the film's Bangers comic font) on the painted art. $0.
Usage: python compose.py <art_name> [y]   (y = top of the 2-line block, default 70)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import sys
H = Path(__file__).parent; A = H / "art"; O = H / "final"; O.mkdir(exist_ok=True)
BANG = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_remotion\public\Bangers.ttf")
W, HH = 1080, 1920
INK, CREAM, GOLD, NIGHT = (18, 16, 20), (255, 244, 214), (246, 185, 35), (12, 18, 44)


def cover(im):
    s = max(W / im.width, HH / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - HH) // 2
    return im.crop((x, y, x + W, y + HH))


def fit(d, t, size, maxw):
    f = ImageFont.truetype(str(BANG), size)
    while d.textlength(t, font=f) > maxw:
        size -= 4; f = ImageFont.truetype(str(BANG), size)
    return f


def band(im, y0, y1, a=150):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rectangle((0, y0, W, y1), fill=a)
    m = m.filter(ImageFilter.GaussianBlur(55))
    return Image.composite(Image.new("RGB", im.size, NIGHT), im, m)


def comic(d, x, y, t, f, fill, sw=10):
    d.text((x + sw, y + sw), t, font=f, fill=INK, stroke_width=sw, stroke_fill=INK)   # drop shadow
    d.text((x, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=INK)


def poster(art, y=70):
    im = cover(Image.open(A / f"{art}.png").convert("RGB"))
    im = band(im, y - 40, y + 400)
    d = ImageDraw.Draw(im)
    f1 = fit(d, "THE LINE", 170, W - 140)
    f2 = fit(d, "HE LEFT UNREAD", 215, W - 100)
    t1, t2 = "THE LINE", "HE LEFT UNREAD"
    comic(d, (W - d.textlength(t1, font=f1)) / 2, y, t1, f1, CREAM, 9)
    y2 = y + d.textbbox((0, 0), t1, font=f1)[3] + 22
    comic(d, (W - d.textlength(t2, font=f2)) / 2, y2, t2, f2, GOLD, 11)
    out = O / f"{art}.jpg"; im.save(out, quality=92); return out



if __name__ == "__main__":
    print(poster(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 70))
