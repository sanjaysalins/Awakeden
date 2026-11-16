r"""Zacchaeus POSTER thumbs ($0): flat mustard yellow, two big cut-out faces (Jesus s13 + Zacchaeus s12), movie-poster type.
Cut-outs made once with rembg -> thumbs_poster/_s13_cut.png, _s12_cut.png.  .venv\Scripts\python.exe <this>"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).resolve().parent; OUT = HERE/"thumbs_poster"
YEL, BLK, RED = (232, 178, 34), (16, 12, 8), (150, 32, 26)
F = lambda n, s: ImageFont.truetype(rf"C:\Windows\Fonts\{n}", s)
JES = Image.open(OUT/"_s13_cut.png"); ZAC = Image.open(OUT/"_s12_cut.png")
JES = JES.crop(JES.getbbox()); ZAC = ZAC.crop(ZAC.getbbox())

def ground(w, h, seed=7):
    im = Image.new("RGB", (w, h), YEL); dr = ImageDraw.Draw(im); r = random.Random(seed)
    for _ in range(int(w*h/2500)):                      # ink spatter, like the stills
        x, y, s = r.randrange(w), r.randrange(h), r.choice([1, 1, 2, 2, 3, 5])
        dr.ellipse([x, y, x+s, y+s], fill=BLK)
    return im

def head(cut, height, top_frac):
    """scale so the head+shoulders top part fills `height`; top_frac = how much of the figure to keep."""
    c = cut.crop((0, 0, cut.width, int(cut.height*top_frac)))
    s = height/c.height; return c.resize((int(c.width*s), height), Image.LANCZOS)

def paste_shadow(bg, fig, xy):
    a = fig.split()[-1]; sh = Image.new("RGBA", fig.size, BLK+(0,)); sh.putalpha(a.point(lambda v: v*0.55))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); bg.paste(sh, (xy[0]+10, xy[1]+8), sh); bg.paste(fig, xy, fig)

def text_c(dr, cx, y, s, f, fill, stroke=0, sfill=None):
    w = dr.textlength(s, font=f); dr.text((cx-w/2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)

def wide():
    w, h = 1280, 720; im = ground(w, h).convert("RGBA")
    z = head(ZAC, 560, 0.55); paste_shadow(im, z, (w-z.width+40, h-z.height))       # Zacchaeus right, looking left
    j = head(JES, 760, 0.60); paste_shadow(im, j, (-60, h-j.height+40))              # Jesus big, left
    dr = ImageDraw.Draw(im)
    f1, f2, f3 = F("BebasNeue-Regular.ttf", 132), F("BebasNeue-Regular.ttf", 132), F("bahnschrift.ttf", 30)
    cx = 760
    text_c(dr, cx, 22, "HE CLIMBED A TREE.", f1, BLK, 6, YEL)
    text_c(dr, cx, 140, "JESUS FOUND HIM.", f2, RED, 6, YEL)
    text_c(dr, cx, 278, "ZACCHAEUS  ·  LUKE 19", f3, BLK, 3, YEL)
    return im.convert("RGB")

def tall():
    w, h = 1080, 1920; im = ground(w, h, 9).convert("RGBA")
    j = head(JES, 1850, 1.0); paste_shadow(im, j, ((w-j.width)//2 - 40, 330))
    z = head(ZAC, 820, 0.55); paste_shadow(im, z, (w-z.width+120, h-z.height))
    dr = ImageDraw.Draw(im); f1 = F("BebasNeue-Regular.ttf", 165)
    text_c(dr, w//2, 60, "HE CLIMBED A TREE.", f1, BLK, 7, YEL)
    text_c(dr, w//2, 210, "JESUS FOUND HIM.", f1, RED, 7, YEL)
    text_c(dr, 300, h-110, "ZACCHAEUS · LUKE 19", F("bahnschrift.ttf", 44), BLK, 4, YEL)
    return im.convert("RGB")

wide().save(OUT/"poster_16x9.jpg", quality=92); tall().save(OUT/"poster_9x16.jpg", quality=92); print("ok")
