"""Rung 2 Phase A -- character-sheet crop builder. Crops face/detail regions
from the rung1 canon + rung2 panels into poc_comic_page/rung2/stills/_charsheet/
for the drift-check section of _STILLS_REVIEW.html. Each crop is resized to a
fixed height (keeps aspect ratio) for a clean horizontal strip layout.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_build_charsheet_crops.py
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
R1 = HERE.parent / "rung1" / "stills"
R2 = HERE / "stills"
OUT = R2 / "_charsheet"
OUT.mkdir(parents=True, exist_ok=True)

TARGET_H = 420

# (label, src_path, box) -- box = (x0,y0,x1,y1) in the SOURCE image's own pixels
CROPS = [
    # ---- JESUS ----
    ("jesus_01_rung1_panel_a", R1 / "panel_a_jesus.png", (100, 150, 1150, 1250)),
    ("jesus_02_p2b_speaks",    R2 / "p2b_jesus_speaks.png", (0, 150, 1100, 1250)),
    ("jesus_03_rung1_panel_d", R1 / "panel_d_threshold.png", (950, 480, 1536, 1050)),
    ("jesus_04_p5a_welcome",   R2 / "p5a_the_welcome.png", (1200, 400, 1850, 1000)),

    # ---- SEEKER ----
    ("seeker_01_rung1_panel_d", R1 / "panel_d_threshold.png", (250, 600, 900, 1300)),
    ("seeker_02_p2a_rehearsing", R2 / "p2a_rehearsing.png", (400, 550, 1100, 1250)),
    ("seeker_03_p5a_welcome",    R2 / "p5a_the_welcome.png", (400, 500, 1050, 1150)),

    # ---- DOOR ----
    ("door_01_rung1_panel_b", R1 / "panel_b_door.png", (30, 150, 900, 1700)),
    ("door_02_rung1_panel_d", R1 / "panel_d_threshold.png", (30, 150, 650, 1750)),
    ("door_03_p4c_empty",     R2 / "p4c_empty_doorway.png", (0, 300, 900, 2200)),
    ("door_04_p5c_latch",     R2 / "p5c_never_locked.png", (0, 400, 1200, 1750)),

    # ---- LEDGER (bonus drift-check) ----
    ("ledger_01_rung1_panel_c", R1 / "panel_c_ledger.png", (150, 300, 1000, 1200)),
    ("ledger_02_p1b_hand",      R2 / "p1b_hesitant_hand.png", (1000, 700, 1750, 1350)),
    ("ledger_03_p5b_received",  R2 / "p5b_record_received.png", (300, 700, 1300, 1500)),
]


def main():
    for label, src, box in CROPS:
        if not src.exists():
            print(f"[skip] {label}: source missing ({src})")
            continue
        im = Image.open(src).convert("RGB")
        w, h = im.size
        x0, y0, x1, y1 = box
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(w, x1), min(h, y1)
        crop = im.crop((x0, y0, x1, y1))
        cw, ch = crop.size
        scale = TARGET_H / ch
        crop = crop.resize((max(1, int(cw * scale)), TARGET_H))
        out = OUT / f"{label}.png"
        crop.save(out)
        print(f"[ok] {label} -> {out.name} ({crop.size[0]}x{crop.size[1]})")


if __name__ == "__main__":
    main()
