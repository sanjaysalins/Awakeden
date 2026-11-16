r"""Nazareth thumbs ($0) from the LOCKED poster (owner pick 'A. The Unlit Line', 2026-11-16): packaging/THUMB_FINAL_9x16.jpg.
16x9 and 1x1 = the whole poster centred over a blurred, darkened copy of itself (no re-cropping the baked type).
.venv\Scripts\python.exe <this>"""
import json
from pathlib import Path
from PIL import Image, ImageFilter
HERE = Path(__file__).resolve().parent; OUT = HERE/"thumbs"; OUT.mkdir(exist_ok=True)
tall = Image.open(HERE.parent/"packaging/THUMB_FINAL_9x16.jpg").convert("RGB")
tall.save(OUT/"thumb_9x16.jpg", quality=92); tall.save(OUT/"thumb_tiktok.jpg", quality=92)
def cover(im, w, h):
    s = max(w/im.width, h/im.height); im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    x = (im.width-w)//2; y = (im.height-h)//2; return im.crop((x, y, x+w, y+h))
def frame(w, h):
    bg = cover(tall, w, h).filter(ImageFilter.GaussianBlur(24)); bg = Image.blend(bg, Image.new("RGB", (w, h), (20, 14, 10)), 0.45)
    p = tall.resize((round(tall.width*h/tall.height), h), Image.LANCZOS); bg.paste(p, ((w-p.width)//2, 0)); return bg
frame(1280, 720).save(OUT/"thumb_16x9.jpg", quality=92); frame(1080, 1080).save(OUT/"thumb_1x1.jpg", quality=92)
fin = json.loads((HERE.parent/"LOCKED.json").read_text())
(OUT/"_meta.json").write_text(json.dumps({"video": "nazareth_final.mp4", "final_sha": fin["final_sha256"], "t": None,
  "source": "LOCKED poster 'The Unlit Line' (owner pick 2026-11-16): prophecy/02_nazareth/packaging/THUMB_FINAL_9x16.jpg; this script"}, indent=2))
print("ok", tall.size)
