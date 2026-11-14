r"""Bartimaeus thumbs ($0) from the LOCKED movie poster (owner pick 2026-11-14: STOOD STILL / for one blind man).
Art: poc_desert_storybook_heroes/bartimaeus/packaging/poster_r1/art/frozen.png.  .venv\Scripts\python.exe <this>"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[3]; OUT = HERE/"thumbs"
PK = ROOT/"poc_desert_storybook_heroes/bartimaeus/packaging"; PUB = ROOT/"_remotion/public"
ART = Image.open(PK/"poster_r1/art/frozen.png").convert("RGB")
FELL, TELL = str(PUB/"IMFeENrm28P.ttf"), str(PUB/"CaveatBrush-Regular.ttf")
RED, BONE, INK = (178, 58, 34), (251, 241, 218), (43, 29, 20)
def fit(d, t, path, s, mw):
    f = ImageFont.truetype(path, s)
    while d.textlength(t, font=f) > mw: s -= 3; f = ImageFont.truetype(path, s)
    return f, s
def title(d, cx, y, w, s1, s2):
    f, s = fit(d, "STOOD STILL", FELL, s1, w); x = cx - d.textlength("STOOD STILL", font=f)/2
    d.text((x+4, y+6), "STOOD STILL", font=f, fill=INK, stroke_width=3, stroke_fill=INK); d.text((x, y), "STOOD STILL", font=f, fill=BONE, stroke_width=2, stroke_fill=BONE)
    y += int(s*1.05); g, _ = fit(d, "for one blind man.", TELL, s2, w); x = cx - d.textlength("for one blind man.", font=g)/2
    d.text((x, y), "for one blind man.", font=g, fill=BONE, stroke_width=max(6, s2//12), stroke_fill=BONE); d.text((x, y), "for one blind man.", font=g, fill=RED)
def cover(im, w, h, fy=0.5):
    s = max(w/im.width, h/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = (im.width-w)//2; y = int((im.height-h)*fy); return im.crop((x, y, x+w, y+h))
def darken(im, a=0.35): return Image.blend(im, Image.new("RGB", im.size, INK), a)
tall = Image.open(PK/"THUMB_FINAL_9x16.jpg").convert("RGB"); tall.save(OUT/"thumb_9x16.jpg", quality=92); tall.save(OUT/"thumb_tiktok.jpg", quality=92)
# 16x9: poster art (beggar + still Jesus) left, soft sky right with type
w, h = 1280, 720
bg = darken(cover(ART.crop((0, 0, ART.width, int(ART.height*0.18))), w, h).filter(ImageFilter.GaussianBlur(6)))
art = cover(ART, 470, 720, 0.75); bg.paste(art, (40, 0)); d = ImageDraw.Draw(bg)
d.rectangle((40, 0, 509, 719), outline=INK, width=6); title(d, 890, 200, 700, 150, 110); bg.save(OUT/"thumb_16x9.jpg", quality=92)
# 1x1: art band y 0.14-1.0 (sky + still Jesus + beggar) on a darkened sky ground, type over the band's sky
band = ART.crop((0, int(ART.height*0.14), ART.width, ART.height)); band = band.resize((round(band.width*880/band.height), 880), Image.LANCZOS)
sq = darken(cover(ART.crop((0, 0, ART.width, int(ART.height*0.18))), 1080, 1080).filter(ImageFilter.GaussianBlur(6)), 0.3); sq.paste(band, ((1080-band.width)//2, 200))
d = ImageDraw.Draw(sq); title(d, 540, 20, 960, 120, 84); sq.save(OUT/"thumb_1x1.jpg", quality=92)
fin = HERE.parent/"LOCKED.json"
(OUT/"_meta.json").write_text(json.dumps({"video": "bartimaeus_final.mp4", "final_sha": json.loads(fin.read_text())["final_sha256"], "t": None,
  "source": "LOCKED movie poster STOOD STILL (owner pick 2026-11-14): poc_desert_storybook_heroes/bartimaeus/packaging/THUMB_FINAL_9x16.jpg; this script"}, indent=2))
im = [Image.open(OUT/n) for n in ("thumb_9x16.jpg", "thumb_16x9.jpg", "thumb_1x1.jpg")]
sh = Image.new("RGB", (270+480+270+40, 480), "white"); sh.paste(im[0].resize((270, 480)), (0, 0)); sh.paste(im[1].resize((480, 270)), (290, 0)); sh.paste(im[2].resize((270, 270)), (790, 0)); sh.save(OUT/"_sheet.jpg", quality=88)
print("ok")
