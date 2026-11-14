r"""Second Fire thumbs: the two LOCKED posters, used as-is (no redesign). 16x9 + 9x16 + tiktok = the locked images;
1x1 = the 9x16 poster scaled whole (title + tagline stay readable) and centred on its own teal ground.
.venv\Scripts\python.exe <this>"""
import json, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[4]; sys.path.insert(0, str(ROOT))
from pipeline import finality  # noqa: E402
HERE = Path(__file__).resolve().parent; OUT = HERE/"thumbs"; OUT.mkdir(exist_ok=True)
SRC = ROOT/"poc_folk_print_style"/"thumbs"
tall = Image.open(SRC/"SECOND_FIRE_thumb_shorts_9x16.jpg").convert("RGB")
wide = Image.open(SRC/"SECOND_FIRE_thumb_wide_16x9.jpg").convert("RGB")
wide.resize((1280, 720), Image.LANCZOS).save(OUT/"thumb_16x9.jpg", quality=92)   # YouTube wide: 1280x720, < 2 MB
tall.save(OUT/"thumb_9x16.jpg", quality=92)
tall.save(OUT/"thumb_tiktok.jpg", quality=92)
S = 1080; ground = tall.getpixel((8, tall.height - 8))      # the poster's own teal
im = Image.new("RGB", (S, S), ground); h = S; w = int(tall.width*h/tall.height)
im.paste(tall.resize((w, h), Image.LANCZOS), ((S - w)//2, 0)); im.save(OUT/"thumb_1x1.jpg", quality=92)
v = HERE.parent/"visual"/"second_fire_final.mp4"
(OUT/"_meta.json").write_text(json.dumps({"video": v.name, "final_sha": finality.content_sha(v), "t": None,
    "source": "locked posters poc_folk_print_style/thumbs/SECOND_FIRE_thumb_{shorts_9x16,wide_16x9}.jpg via make_thumbs.py (1x1 = pad, no redraw)"}, indent=2), encoding="utf-8")
print("ok")
