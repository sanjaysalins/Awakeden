r"""Woman at the well thumbs ($0) from the LOCKED movie poster (owner 2026-11-14).
Art: poc_pop_halftone/woman_at_well/packaging/poster_r1/art/fix2.png.  .venv\Scripts\python.exe <this>"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[3]; OUT = HERE/"thumbs"
PK = ROOT/"poc_pop_halftone/woman_at_well/packaging"
ART = Image.open(PK/"poster_r1/art/fix2.png").convert("RGB")
F = "C:/Windows/Fonts/impact.ttf"; YEL, BLK, WHT = (255, 228, 0), (0, 0, 0), (255, 255, 255)
def font(s): return ImageFont.truetype(F, s)
def fit(d, t, s, mw):
    f = font(s)
    while d.textlength(t, font=f) > mw: s -= 3; f = font(s)
    return f, s
def title(d, cx, y, w, s1, s2, tag_s):
    for t, s in (("THE JAR", s1), ("STAYED", s2)):
        f, s = fit(d, t, s, w); x = cx - d.textlength(t, font=f)/2
        d.text((x+s*0.05, y+s*0.06), t, font=f, fill=BLK)
        d.text((x, y), t, font=f, fill=YEL, stroke_width=max(4, s//20), stroke_fill=BLK); y += int(s*1.03)
    ft = font(tag_s); tag = "SHE CAME FOR WATER."; tw = d.textlength(tag, font=ft); x = cx - tw/2; p = tag_s*0.45
    d.rounded_rectangle((x-p, y+tag_s*0.2, x+tw+p, y+tag_s*1.55), int(p/2), fill=BLK)
    d.text((x, y+tag_s*0.3), tag, font=ft, fill=WHT)
def cover(im, w, h, fy=0.5):
    s = max(w/im.width, h/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = (im.width-w)//2; y = int((im.height-h)*fy); return im.crop((x, y, x+w, y+h))
# 9x16 = the locked poster itself
tall = Image.open(PK/"THUMB_FINAL_9x16.jpg").convert("RGB"); tall.save(OUT/"thumb_9x16.jpg", quality=92)
tall.save(OUT/"thumb_tiktok.jpg", quality=92)
# 16x9: poster art left, blurred rays right with type
w, h = 1280, 720; bg = cover(ART.crop((0, 0, ART.width, int(ART.height*0.4))), w, h).filter(ImageFilter.GaussianBlur(3))
art = cover(ART, 405, 720, 0.5); bg.paste(art, (60, 0)); d = ImageDraw.Draw(bg)
d.rectangle((60, 0, 465, 719), outline=BLK, width=6)
title(d, 870, 120, 720, 170, 230, 44); bg.save(OUT/"thumb_16x9.jpg", quality=92)
# 1x1: art band y 0.20-0.90 on blurred rays, type over the rays at top (jar mouth + runner feet stay clear)
band = ART.crop((0, int(ART.height*0.20), ART.width, int(ART.height*0.90))); band = band.resize((round(band.width*1080/band.height), 1080), Image.LANCZOS)
sq = cover(ART.crop((0, 0, ART.width, int(ART.height*0.4))), 1080, 1080).filter(ImageFilter.GaussianBlur(3)); sq.paste(band, ((1080-band.width)//2, 0))
d = ImageDraw.Draw(sq); title(d, 540, 14, 900, 96, 132, 32); sq.save(OUT/"thumb_1x1.jpg", quality=92)
fin = (ROOT/"batches/cluster_04_encounters/woman_at_well_short/LOCKED.json")
(OUT/"_meta.json").write_text(json.dumps({"video": "woman_at_well_final.mp4", "final_sha": json.loads(fin.read_text())["final_sha256"], "t": None,
  "source": "LOCKED movie poster THE JAR STAYED (owner 'go with your pick' 2026-11-14): packaging/poster_r1/final/fix2.jpg; this script"}, indent=2))
print("ok")
