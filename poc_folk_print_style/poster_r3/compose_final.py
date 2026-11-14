"""Bake-off B finalists: title type + 16:9 version. $0."""
import sys
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "poster_r1"))
import poster as P  # noqa: E402
OUT = H / "final"; OUT.mkdir(exist_ok=True)
FIN = {"burnB_nbp2": "He fed him first.", "burnB_gpt2": "He fed him first.",
       "doubleB_nbp3": "He carried that night.", "doubleB_gpt1": "He carried that night."}
for n, tag in FIN.items():
    v, h = P.make(Image.open(H / "art" / f"{n}.png").convert("RGB"), 0.5, "The Second Fire", tag, "bottom")
    v.convert("RGB").save(OUT / f"{n}_9x16.jpg", quality=93)
    h.convert("RGB").save(OUT / f"{n}_16x9.jpg", quality=93)
print("ok")
