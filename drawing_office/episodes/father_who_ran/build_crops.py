"""Drawing Office -- The Father Who Ran. Crop source images for slots that
reuse an existing plate at a tighter framing, all $0 via crop_study."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "primitives"))
from crop_study import camera_crop  # noqa: E402
from PIL import Image

HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
THIRD_LINE = HERE.parents[2] / "poc_bethesda_style_test" / "round3_devices" / "stills"
CROPS = HERE / "crops"
CROPS.mkdir(exist_ok=True)

JOBS = [
    # (source, out_name, cx, cy, zoom)
    (THIRD_LINE / "third_line_02.png", "run_flash_waist_up.png", 0.50, 0.35, 1.7),   # slot 2
    (THIRD_LINE / "third_line_03.png", "fists_on_back.png",      0.62, 0.55, 2.1),   # slot 9
    (THIRD_LINE / "third_line_02.png", "open_hand.png",          0.30, 0.55, 1.9),   # slot 10
    (PLATES / "father_watching.png",   "watcher_turn.png",       0.62, 0.55, 1.5),   # slot 11
    (PLATES / "christ_road.png",       "christ_close.png",       0.50, 0.55, 1.35),  # slot 13
]

if __name__ == "__main__":
    for src, out_name, cx, cy, zoom in JOBS:
        img = Image.open(src)
        crop = camera_crop(img, cx_frac=cx, cy_frac=cy, zoom=zoom)
        out_path = CROPS / out_name
        crop.save(out_path)
        print(f"[ok] {out_name}  from {src.name}  cx={cx} cy={cy} zoom={zoom}")
