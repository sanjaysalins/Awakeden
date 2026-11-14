"""Round 3: add title type to the no-lettering key art (reuses poster_r1/poster.py), copy lettered ones as-is. $0."""
import sys
from pathlib import Path
from PIL import Image
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "poster_r1"))
import poster as P  # noqa: E402

OUT = H / "out"; OUT.mkdir(exist_ok=True)
TYPED = {  # art name -> (tagline, where)
    "flame_gpt2": ("He said no. Three times.", "bottom"), "flame_nbp2": ("He said no. Three times.", "bottom"),
    "fold_gpt1": ("One night. One sunrise.", "bottom"), "fold_nbp1": ("One night. One sunrise.", "bottom"),
    "double_nbp1": ("He carried that night.", "bottom"), "double_gpt2": ("He carried that night.", "bottom"),
    "burn_nbp1": ("He fed him first.", "bottom"), "burn_gpt1": ("He fed him first.", "bottom"),
}
LETTERED = ["coals_gpt2", "coals_nbp1", "foot_gpt1", "foot_nbp1"]
for n, (tag, where) in TYPED.items():
    v, h = P.make(Image.open(H / "art" / f"{n}.png").convert("RGB"), 0.5, "The Second Fire", tag, where)
    v.convert("RGB").save(OUT / f"{n}_9x16.jpg", quality=92)
for n in LETTERED:
    P.cover(Image.open(H / "art" / f"{n}.png").convert("RGB"), 1080, 1920).save(OUT / f"{n}_9x16.jpg", quality=92)
print("ok", len(TYPED) + len(LETTERED))
