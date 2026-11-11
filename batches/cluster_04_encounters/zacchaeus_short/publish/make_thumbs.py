"""Zacchaeus thumbs from CLEAN stills (no baked captions), crops chosen so faces sit above the title scrim.
Reuses pipeline/thumbnails.compose / compose_tiktok.  .venv\Scripts\python.exe <this>"""
import json, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[4]; sys.path.insert(0, str(ROOT))
from pipeline import thumbnails as T, finality  # noqa: E402
HERE = Path(__file__).resolve().parent; OUT = HERE/"thumbs"; ST = ROOT/"poc_scratchy_ink"/"zacchaeus"/"stills"
TITLE, REF = ["HE CLIMBED A TREE.", "JESUS FOUND HIM."], "ZACCHAEUS  ·  LUKE 19"
s11 = Image.open(ST/"s11.png").convert("RGB"); s09b = Image.open(ST/"s09b.png").convert("RGB"); s13 = Image.open(ST/"s13.png").convert("RGB")
W = s11.width
crops = {"16x9": (s09b, 1010, int(W*9/16)), "1x1": (s11, 600, W)}
for key, (im, y0, h) in crops.items():
    T.compose(im.crop((0, y0, W, y0+h)), key, TITLE, REF).save(OUT/f"thumb_{key}.jpg", quality=92)
def tall(img):
    """9x16 with the title band LOW (55-78%) so both faces stay clear (red team r1: top band covered Jesus's eyes)."""
    from PIL import ImageDraw
    from pipeline.channel_dress import draw_wordmark, wordmark_width
    w, h = T.SIZES["9x16"]; im = T.cover_crop(img, w, h); dr = ImageDraw.Draw(im, "RGBA")
    margin = int(w*0.055); f = T._fit_title_font(dr, TITLE, int(w*0.10), w-2*margin); ts = f.size
    fr = T._font(T.GEORGIA_B, int(ts*0.42))
    top = int(h*0.56); bot = top + len(TITLE)*int(ts*1.08) + int(ts*1.0)
    dr.rectangle([0, top-int(ts*0.35), w, bot], fill=T.INK+(225,))
    y = top
    for line in TITLE:
        tw = dr.textlength(line, font=f); x = (w-tw)//2
        dr.text((x+4, y+4), line, font=f, fill=(0,0,0,210)); dr.text((x, y), line, font=f, fill=T.IVORY); y += int(ts*1.08)
    rw = dr.textlength(REF, font=fr); dr.text(((w-rw)//2, y+int(ts*0.1)), REF, font=fr, fill=T.IVORY)
    bs = int(ts*0.26); draw_wordmark(im, (w-wordmark_width(bs))//2, int(h*0.045), bs, glow=False, shadow=True)
    return im
tall(s11).save(OUT/"thumb_9x16.jpg", quality=92)
T.compose_tiktok(s11, TITLE, REF).save(OUT/"thumb_tiktok.jpg", quality=92)
v = HERE.parent/"visual"/"zacchaeus_final.mp4"
(OUT/"_meta.json").write_text(json.dumps({"video": v.name, "final_sha": finality.content_sha(v), "t": None,
    "source": "clean stills s09b (16x9), s11 (1x1, tiktok) (9x16 low band) via make_thumbs.py"}, indent=2), encoding="utf-8")
print("ok")
