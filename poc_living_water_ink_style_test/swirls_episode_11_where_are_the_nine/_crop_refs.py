from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "swirls_episode_11_where_are_the_nine_f02_9x16.png"
REFS = HERE / "refs"
im = Image.open(SRC)
W, H = im.size
print(f"source size: {W}x{H}")

BOXES = {
    "village_edge_ref.png": (0, 1080, 250, 1440),
    "ten_ref.png": (520, 930, 1510, 2240),
    "samaritan_ref.png": (930, 1180, 1220, 2240),
}

for name, box in BOXES.items():
    crop = im.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
