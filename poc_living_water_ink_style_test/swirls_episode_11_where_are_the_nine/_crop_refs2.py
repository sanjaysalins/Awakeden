from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "swirls_episode_11_where_are_the_nine_f05_9x16.png"
REFS = HERE / "refs"
im = Image.open(SRC)
W, H = im.size
print(f"source size: {W}x{H}")

BOXES = {
    "samaritan_face_ref.png": (440, 1220, 660, 1460),
    "road_ref.png": (60, 2350, 700, 2650),
}

for name, box in BOXES.items():
    crop = im.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
