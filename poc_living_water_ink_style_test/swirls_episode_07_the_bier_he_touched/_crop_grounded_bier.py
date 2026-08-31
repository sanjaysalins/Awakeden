from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = HERE / "refs"

f03 = Image.open(HERE / "swirls_episode_07_the_bier_he_touched_f03_9x16.png")
print("f03 size:", f03.size)

BOXES = {
    "bier_grounded_ref.png": (530, 1540, 1400, 2160),
}

for name, box in BOXES.items():
    crop = f03.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
