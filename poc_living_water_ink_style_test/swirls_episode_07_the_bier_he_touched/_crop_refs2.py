from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = HERE / "refs"

f05 = Image.open(HERE / "swirls_episode_07_the_bier_he_touched_f05_9x16.png")
f03 = Image.open(HERE / "swirls_episode_07_the_bier_he_touched_f03_9x16.png")
print("f05 size:", f05.size, "f03 size:", f03.size)

BOXES_F05 = {
    "son_ref.png": (440, 1101, 770, 1486),
}
BOXES_F03 = {
    "empty_bier_ref.png": (523, 165, 991, 716),
}

for name, box in BOXES_F05.items():
    crop = f05.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")

for name, box in BOXES_F03.items():
    crop = f03.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
