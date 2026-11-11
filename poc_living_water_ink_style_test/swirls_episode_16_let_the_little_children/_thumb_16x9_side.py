"""Ep16 only: side-by-side 16:9 thumbnail. The shared compose_centered() shrinks a 9:16 cover
to a stamp on 16:9 when the title runs to 2 lines; here the words sit left and the owner's
still sits right at full height, so the smiling-Jesus vs "Angry" contrast survives.
Same fonts/colours/wordmark as the shared engine. Overwrites publish/thumbs/thumb_16x9.jpg."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402
from pipeline.thumbnails import cover_crop, _font, GEORGIA, _default_title  # noqa: E402
from pipeline.channel_dress import draw_wordmark, wordmark_width  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location("ep16", HERE / "episode.py")
ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
W, H = 1280, 720
frame = Image.open(HERE / "front_cover.png").convert("RGB")
im = cover_crop(frame, W, H).filter(ImageFilter.GaussianBlur(28))
im = Image.eval(im, lambda px: int(px * 0.42))
dr = ImageDraw.Draw(im, "RGBA")

# picture: right side, full safe height
ph = int(H * 0.88)
pw = int(frame.width * ph / frame.height)
art = frame.resize((pw, ph), Image.LANCZOS)
px, py = W - pw - 70, (H - ph) // 2
dr.rectangle([px - 4, py - 4, px + pw + 3, py + ph + 3], outline=(200, 190, 160, 255), width=3)
im.paste(art, (px, py))

# words: left column
lines = _default_title(ep.FRONT_COVER.title)
colw = px - 70 - 60
size = 120
while True:
    f = _font(GEORGIA.replace("georgia.ttf", "georgiab.ttf") if "georgia.ttf" in GEORGIA else GEORGIA, size)
    if max(dr.textlength(l, font=f) for l in lines) <= colw or size < 40:
        break
    size -= 4
lh = int(size * 1.08)
block = lh * len(lines)
ty = (H - block) // 2 - 40
for i, l in enumerate(lines):
    tw = dr.textlength(l, font=f)
    x, y = 70 + (colw - tw) / 2, ty + i * lh
    dr.text((x + 4, y + 5), l, font=f, fill=(0, 0, 0, 200))
    dr.text((x, y), l, font=f, fill=(246, 238, 210, 255))
fr = _font(GEORGIA, int(size * 0.36))
ref = ep.FRONT_COVER.subtitle
rw = dr.textlength(ref, font=fr)
ry = ty + block + 24
dr.text((70 + (colw - rw) / 2, ry), ref, font=fr, fill=(246, 238, 210, 255))
bs = 34
draw_wordmark(im, 70 + (colw - wordmark_width(bs)) / 2, ry + int(size * 0.36) + 40, bs, glow=False, shadow=True)
out = HERE / "publish" / "thumbs" / "thumb_16x9.jpg"
im.convert("RGB").save(out, quality=92)
print(out, size)
