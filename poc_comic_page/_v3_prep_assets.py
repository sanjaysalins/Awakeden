"""v3 elevation prep -- all $0:
  1. Pencil-sketch PNG per panel still (cv2 dodge-blend) -> stills_v2/_sketch/
     (the page reads fully PENCILLED from second one; panels ink in on their slam)
  2. rembg subject cutouts for the border-break panels -> stills_v2/_cutout/
     (pre-cropped to their compose cell so the compositor just scales + pastes)
  3. "THUD!" drawn SFX lettering PNG (Impact + jagged ink burst) -> _sketch/
  4. Line-boil the calm close-up extended clips -> clips_v2/extended_boil/

  .venv\\Scripts\\python.exe poc_comic_page/_v3_prep_assets.py
"""
import subprocess
import sys
import math
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STILLS = HERE / "_piece1" / "stills_v2"
SKETCH = STILLS / "_sketch"
CUTOUT = STILLS / "_cutout"
EXT = HERE / "_piece1" / "clips_v2" / "extended"
BOIL = HERE / "_piece1" / "clips_v2" / "extended_boil"
for d in (SKETCH, CUTOUT, BOIL):
    d.mkdir(parents=True, exist_ok=True)

PAPER = (208, 192, 156)

# every still that appears as a panel (name -> file)
PANEL_STILLS = {
    "p1a": "p1a_night_door.png", "p1b": "p1b_hesitant_hand.png",
    "p2a": "p2a_rehearsing.png", "p2b": "p2b_jesus_speaks.png",
    "p2c": "p2c_the_record.png",
    "panel_b": "panel_b_door.png", "panel_a": "panel_a_jesus.png",
    "panel_c": "panel_c_scroll.png", "panel_d": "panel_d_threshold.png",
    "p4a": "p4a_the_exception_fear.png", "p4b": "p4b_the_record_nailed.png",
    "p4c": "p4c_empty_threshold.png",
}

# border-break panels: (name, compose cell w/h at SS=1.18 canvas)
# page3 2x2 cell ~ (617, 1097)/2 -> computed exactly below from the same math
# as the compositor; we bake the scale-crop so compositor pastes 1:1.
SS = 1.18
W, H = 1080, 1920
MARGIN, GUTTER = 26, 12
LAYOUTS = {
    "2x2":        [(0.0, 0.0, 0.5, 0.5), (0.5, 0.0, 0.5, 0.5),
                   (0.0, 0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)],
    "3-big-left": [(0.0, 0.0, 0.62, 1.0), (0.62, 0.0, 0.38, 0.5), (0.62, 0.5, 0.38, 0.5)],
}


def cell_size(layout, idx):
    m = MARGIN * SS
    iw, ih = W * SS - 2 * m, H * SS - 2 * m
    fx, fy, fw, fh = LAYOUTS[layout][idx]
    x0, y0 = m + fx * iw, m + fy * ih
    x1, y1 = m + (fx + fw) * iw, m + (fy + fh) * ih
    g = GUTTER * SS / 2
    return (int(x1 - g) - int(x0 + g), int(y1 - g) - int(y0 + g))


BREAKS = [
    # (name, layout, panel_index)  -- panel_a bursts on the page3 splash pivot,
    # p4b's nailed scroll bursts on the THUD beat
    ("panel_a", "2x2", 1),
    ("p4b", "3-big-left", 1),
]


def pencil_sketch(src: Path, out: Path):
    img = cv2.imread(str(src))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (0, 0), 18)
    dodge = cv2.divide(gray, 255 - blur, scale=256)
    # boost line contrast a touch, then lay onto aged paper tone
    dodge = cv2.normalize(dodge, None, 0, 255, cv2.NORM_MINMAX)
    sk = cv2.cvtColor(dodge, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0
    paper = np.array(PAPER[::-1], dtype=np.float32) / 255.0  # BGR
    tinted = (sk * 0.30 + 0.70) * paper * 255.0  # lines darken the paper
    # keep the darkest strokes readable
    lines = (1.0 - sk) * 0.55
    outimg = tinted * (1.0 - lines) + np.array((60, 62, 70), np.float32) * lines
    cv2.imwrite(str(out), np.clip(outimg, 0, 255).astype(np.uint8))


def scale_crop(im: Image.Image, cw: int, ch: int) -> Image.Image:
    s = max(cw / im.width, ch / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - cw) // 2, (zh - ch) // 2,
                    (zw - cw) // 2 + cw, (zh - ch) // 2 + ch))


def make_cutouts():
    from rembg import remove
    for name, layout, idx in BREAKS:
        src = STILLS / PANEL_STILLS[name]
        cw, ch = cell_size(layout, idx)
        cell = scale_crop(Image.open(src).convert("RGB"), cw, ch)
        cut = remove(cell)  # RGBA
        # soften the alpha edge one step so the paste doesn't razor
        a = cut.split()[3].filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(1.2))
        cut.putalpha(a)
        out = CUTOUT / f"{name}_cell.png"
        cut.save(out)
        print(f"[cutout] {out.name} ({cw}x{ch})")


def make_thud():
    """Hand-lettered THUD! over a jagged ink burst star, transparent PNG."""
    Wp, Hp = 560, 400
    img = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = Wp // 2, Hp // 2
    rng = random.Random(41)
    # jagged burst: alternating long/short spikes
    pts = []
    n = 26
    for i in range(n):
        ang = i * 2 * math.pi / n + rng.uniform(-0.06, 0.06)
        r = (185 if i % 2 == 0 else 105) * rng.uniform(0.88, 1.12)
        pts.append((cx + r * math.cos(ang), cy + r * 0.72 * math.sin(ang)))
    d.polygon(pts, fill=(238, 226, 194, 255), outline=(35, 31, 32, 255))
    d.line(pts + [pts[0]], fill=(35, 31, 32, 255), width=7, joint="curve")
    font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 128)
    txt = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)
    bb = font.getbbox("THUD!")
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    ox, oy = (Wp - tw) // 2 - bb[0], (Hp - th) // 2 - bb[1]
    for dx in range(-7, 8, 2):
        for dy in range(-7, 8, 2):
            td.text((ox + dx, oy + dy), "THUD!", font=font, fill=(35, 31, 32, 255))
    td.text((ox, oy), "THUD!", font=font, fill=(142, 31, 31, 255))
    txt = txt.rotate(-7, resample=Image.BICUBIC, center=(cx, cy))
    img.alpha_composite(txt)
    out = SKETCH / "_thud.png"
    img.save(out)
    print(f"[thud] {out.name}")


BOIL_CLIPS = ["p2c", "panel_c", "p5b", "p4a"]


def main():
    for name, fn in PANEL_STILLS.items():
        out = SKETCH / f"{name}_sketch.png"
        pencil_sketch(STILLS / fn, out)
        print(f"[sketch] {out.name}")
    make_cutouts()
    make_thud()
    for stem in BOIL_CLIPS:
        src, out = EXT / f"{stem}.mp4", BOIL / f"{stem}.mp4"
        if not src.exists():
            print(f"[boil skip] {stem}")
            continue
        subprocess.run([sys.executable, str(ROOT / "panel_animator" / "line_boil.py"),
                        "--clip", str(src), "--out", str(out), "--amount", "0.8"],
                       check=True)
        print(f"[boil] {out.name}")
    print("[done]")


if __name__ == "__main__":
    main()
