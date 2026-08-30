from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "swirls_episode_05_barrel_that_did_not_waste_f01_9x16.png"
REFS = HERE / "refs"
im = Image.open(SRC)
W, H = im.size

BOXES = {
    "widow_ref.png": (170, 1270, 720, 2470),
    "widow_face_ref.png": (450, 1280, 670, 1540),
    "elijah_ref.png": (860, 1030, 1450, 2480),
    "elijah_face_ref.png": (910, 1040, 1220, 1340),
    "gate_ref.png": (30, 950, 900, 1600),
}

for name, box in BOXES.items():
    crop = im.crop(box)
    out = REFS / name
    crop.save(out)
    print(f"{name}: box={box} size={crop.size} -> {out}")
