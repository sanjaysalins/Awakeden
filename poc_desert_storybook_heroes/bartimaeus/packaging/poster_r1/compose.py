"""Poster r1: real type on the painted art, film fonts. $0. Usage: python compose.py <art_name> <top|bottom-y>"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import sys
H = Path(__file__).parent; A = H/"art"; O = H/"final"; O.mkdir(exist_ok=True)
PUB = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_remotion\public")
SHOUT, TELL, FELL = PUB/"ProtestRevolution-Regular.ttf", PUB/"CaveatBrush-Regular.ttf", PUB/"IMFeENrm28P.ttf"
W, HH = 1080, 1920
RED, BONE, INK = (178, 58, 34), (251, 241, 218), (43, 29, 20)
def cover(im):
    s = max(W/im.width, HH/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = (im.width-W)//2; y = (im.height-HH)//2; return im.crop((x, y, x+W, y+HH))
def fit(d, t, font, size, maxw):
    f = ImageFont.truetype(str(font), size)
    while d.textlength(t, font=f) > maxw: size -= 4; f = ImageFont.truetype(str(font), size)
    return f
def soft_band(im, y0, y1, a=110):
    ov = Image.new("L", im.size, 0); dd = ImageDraw.Draw(ov); dd.rectangle((0, y0, W, y1), fill=a)
    ov = ov.filter(ImageFilter.GaussianBlur(60)); dark = Image.new("RGB", im.size, INK)
    return Image.composite(dark, im, ov)
def poster(art, kind, y):
    im = cover(Image.open(A/f"{art}.png").convert("RGB"))
    im = soft_band(im, y - 30, y + 330)
    d = ImageDraw.Draw(im)
    if kind == "louder":
        f = fit(d, "LOUDER", SHOUT, 300, W - 120); t = "LOUDER"
        x = (W - d.textlength(t, font=f))/2
        d.text((x-5, y-6), t, font=f, fill=BONE, stroke_width=12, stroke_fill=BONE)
        d.text((x, y), t, font=f, fill=RED)
        tag, tf = "Everyone said hush.", ImageFont.truetype(str(TELL), 86)
    else:
        f = fit(d, "STOOD STILL", FELL, 230, W - 110); t = "STOOD STILL"
        x = (W - d.textlength(t, font=f))/2
        d.text((x+4, y+6), t, font=f, fill=INK, stroke_width=3, stroke_fill=INK)
        d.text((x, y), t, font=f, fill=BONE, stroke_width=2, stroke_fill=BONE)
        tag, tf = "for one blind man.", ImageFont.truetype(str(TELL), 92)
    bb = d.textbbox((0, 0), t, font=f); ty = y + bb[3] + 26
    tw = d.textlength(tag, font=tf); tx = (W - tw)/2
    d.text((tx+3, ty+4), tag, font=tf, fill=INK)
    d.text((tx, ty), tag, font=tf, fill=RED if kind == "stood" else BONE)
    out = O/f"{art}_{kind}.jpg"; im.save(out, quality=92); return out
if __name__ == "__main__":
    art, y = sys.argv[1], int(sys.argv[2])
    for k in ("louder", "stood"): print(poster(art, k, y))
