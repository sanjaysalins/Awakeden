r"""Mary and Martha thumbs from CLEAN stills (no baked captions), crops chosen so faces sit above the title scrim.
Reuses pipeline/thumbnails.compose / compose_tiktok.  .venv\Scripts\python.exe <this>"""
import json, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[4]; sys.path.insert(0, str(ROOT))
from pipeline import thumbnails as T, finality  # noqa: E402
HERE = Path(__file__).resolve().parent; OUT = HERE/"thumbs"; ST = ROOT/"poc_warm_storybook_style"/"stills"
TITLE, REF = ["DOES ANYONE", "EVEN CARE?"], "MARTHA  ·  LUKE 10"
s05 = Image.open(ST/"s05.png").convert("RGB"); s01 = Image.open(ST/"s01.png").convert("RGB")
W = s05.width
crops = {"16x9": (s05, 560, int(W*9/16)), "1x1": (s05, 380, W)}
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
tall(s05).save(OUT/"thumb_9x16.jpg", quality=92)
T.compose_tiktok(s05, TITLE, REF).save(OUT/"thumb_tiktok.jpg", quality=92)
v = HERE.parent/"visual"/"mary_martha_final.mp4"
(OUT/"_meta.json").write_text(json.dumps({"video": v.name, "final_sha": finality.content_sha(v), "t": None,
    "source": "clean still s05 (Martha asks, Jesus seated, Mary at His feet) for all sizes via make_thumbs.py"}, indent=2), encoding="utf-8")
print("ok")

# 16x9 side-by-side (ep16 _thumb_16x9_side.py pattern): the scrim layout covered both faces on 16x9,
# so words sit left and the still sits right at full height.
from PIL import ImageDraw, ImageFilter
from pipeline.channel_dress import draw_wordmark, wordmark_width
W16, H16 = 1280, 720
frame = s05.crop((0, 350, s05.width, 350 + 1920))
im = T.cover_crop(frame, W16, H16).filter(ImageFilter.GaussianBlur(28))
im = Image.eval(im, lambda px: int(px * 0.42)); dr = ImageDraw.Draw(im, "RGBA")
ph = int(H16 * 0.88); pw = int(frame.width * ph / frame.height); art = frame.resize((pw, ph), Image.LANCZOS)
px, py = W16 - pw - 70, (H16 - ph) // 2
dr.rectangle([px - 4, py - 4, px + pw + 3, py + ph + 3], outline=(200, 190, 160, 255), width=3); im.paste(art, (px, py))
colw = px - 70 - 60; size = 120
while True:
    f = T._font(T.GEORGIA_B, size)
    if max(dr.textlength(l, font=f) for l in TITLE) <= colw or size < 40: break
    size -= 4
lh = int(size * 1.08); block = lh * len(TITLE); ty = (H16 - block) // 2 - 40
for i, l in enumerate(TITLE):
    tw = dr.textlength(l, font=f); x, y = 70 + (colw - tw) / 2, ty + i * lh
    dr.text((x + 4, y + 5), l, font=f, fill=(0, 0, 0, 200)); dr.text((x, y), l, font=f, fill=(246, 238, 210, 255))
fr = T._font(T.GEORGIA, int(size * 0.36)); rw = dr.textlength(REF, font=fr); ry = ty + block + 24
dr.text((70 + (colw - rw) / 2, ry), REF, font=fr, fill=(246, 238, 210, 255))
bs = 34; draw_wordmark(im, 70 + (colw - wordmark_width(bs)) / 2, ry + int(size * 0.36) + 40, bs, glow=False, shadow=True)
im.convert("RGB").save(OUT / "thumb_16x9.jpg", quality=92)
print("16x9 side-by-side", size)

# red team r1 (Fable + Opus 2/2): the see-through band on 9x16 + 1x1 covered Mary's face (ghost face).
# 9x16 -> the clean TikTok layout; 1x1 -> words on top, framed art below, no band over any face.
T.compose_tiktok(s05, TITLE, REF).save(OUT / "thumb_9x16.jpg", quality=92)
S = 1080
art_src = s05.crop((0, 600, s05.width, 2200))
im = T.cover_crop(art_src, S, S).filter(ImageFilter.GaussianBlur(26)); im = Image.eval(im, lambda px: int(px * 0.42))
dr = ImageDraw.Draw(im, "RGBA"); f = T._fit_title_font(dr, TITLE, int(S * 0.095), S * 0.88); ts = f.size
ty = int(S * 0.04)
for l in TITLE:
    tw = dr.textlength(l, font=f); x = (S - tw) / 2
    dr.text((x + 4, ty + 4), l, font=f, fill=(0, 0, 0, 210)); dr.text((x, ty), l, font=f, fill=T.IVORY); ty += int(ts * 1.08)
fr = T._font(T.GEORGIA, int(ts * 0.36)); ref_h = int(ts * 0.36) + 30
ay = ty + 18; ah = S - ay - ref_h - 30; aw = int(art_src.width * ah / art_src.height)
art = art_src.resize((aw, ah), Image.LANCZOS); ax = (S - aw) // 2
dr.rectangle([ax - 3, ay - 3, ax + aw + 2, ay + ah + 2], outline=T.IVORY + (160,), width=3); im.paste(art, (ax, ay))
rw = dr.textlength(REF, font=fr); dr.text(((S - rw) / 2, ay + ah + 16), REF, font=fr, fill=T.IVORY)
im.convert("RGB").save(OUT / "thumb_1x1.jpg", quality=92)
print("9x16 = tiktok layout; 1x1 framed")
