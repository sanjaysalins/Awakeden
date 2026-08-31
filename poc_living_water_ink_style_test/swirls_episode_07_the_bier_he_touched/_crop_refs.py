from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "swirls_episode_07_the_bier_he_touched_f01_9x16.png"
REFS = HERE / "refs"
im = Image.open(SRC)
W, H = im.size
print(f"source size: {W}x{H}")

# Boxes eyeballed from the 1:1 F01 render (2nd, corrected render -- composition
# changed from the wood-desk reroll). Native 1536x2752.
BOXES = {
    "widow_ref.png": (840, 1440, 1240, 2280),
    "widow_face_ref.png": (910, 1495, 1110, 1690),
}

for name, box in BOXES.items():
    crop = im.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
