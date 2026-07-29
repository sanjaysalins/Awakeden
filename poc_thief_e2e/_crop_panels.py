"""Crop-and-recomposite test, step 1 (2026-07-25): crop the 4 panels out of
each Thief page (poc_thief_e2e/stills/_thief_poc/) into separate images.
Boundaries are estimated from the known wide/2-portrait/wide skeleton;
grid_choreography.py draws its own borders on recomposite, so generous
margins here are fine -- the goal is not cutting off faces, not pixel-exact
boundaries.

  .venv\\Scripts\\python.exe poc_thief_e2e/_crop_panels.py
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "stills" / "_thief_poc"
OUT = HERE / "stills" / "_crop_test" / "panels"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1536, 2752

# (x0, y0, x1, y1) as fractions of (W, H)
BOXES = {
    "panel1": (0.02, 0.015, 0.98, 0.335),
    "panel2": (0.02, 0.345, 0.485, 0.635),
    "panel3": (0.515, 0.345, 0.98, 0.635),
    "panel4": (0.02, 0.645, 0.98, 0.965),
}

for page in ["page1", "page2", "page3"]:
    img = Image.open(SRC / f"{page}.png")
    for name, (fx0, fy0, fx1, fy1) in BOXES.items():
        box = (int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H))
        crop = img.crop(box)
        out = OUT / f"{page}_{name}.png"
        crop.save(out)
        print(f"{out.name}  {crop.size}")
