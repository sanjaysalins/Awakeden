"""Fresh-takes proof pass -- composite the two ascent stills into the actual
split-screen demo frames ($0, local PIL work, no NBP spend). Produces:
  5_shadow_and_body.png  -- top half of image 2 + bottom half of image 3, thin seam
  6_written_twice.png    -- same composite, with "WOOD" straddling the seam

  .venv\\Scripts\\python.exe poc_living_sketchbook/_fresh_takes_test/_composite.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
TOP_SRC = HERE / "2_top_ascent.png"
BOTTOM_SRC = HERE / "3_bottom_ascent.png"

SEAM_COLOR = (43, 29, 20)  # scorched umber
SEAM_HEIGHT = 6


def build_composite(top_img, bottom_img):
    w, h = top_img.size
    top_half = top_img.crop((0, 0, w, h // 2))
    bottom_half = bottom_img.crop((0, h // 2, w, h))
    canvas = Image.new("RGB", (w, h), (245, 234, 211))
    canvas.paste(top_half, (0, 0))
    canvas.paste(bottom_half, (0, h // 2))
    draw = ImageDraw.Draw(canvas)
    seam_y = h // 2
    draw.rectangle([0, seam_y - SEAM_HEIGHT // 2, w, seam_y + SEAM_HEIGHT // 2], fill=SEAM_COLOR)
    return canvas


def add_bridging_word(canvas, word):
    canvas = canvas.copy()
    w, h = canvas.size
    seam_y = h // 2
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("georgiab.ttf", 46)
    except OSError:
        try:
            font = ImageFont.truetype("arialbd.ttf", 46)
        except OSError:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), word, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = seam_y - th // 2 - bbox[1]
    pad_x, pad_y = 22, 10
    draw.rectangle(
        [x - pad_x, y - pad_y, x + tw + pad_x, y + th + pad_y],
        fill=(245, 234, 211),
        outline=(154, 92, 44),
        width=3,
    )
    draw.text((x, y), word, font=font, fill=(43, 29, 20))
    return canvas


def main() -> None:
    if not TOP_SRC.exists() or not BOTTOM_SRC.exists():
        raise SystemExit(f"missing source(s): {TOP_SRC.exists()=} {BOTTOM_SRC.exists()=}")

    top_img = Image.open(TOP_SRC).convert("RGB")
    bottom_img = Image.open(BOTTOM_SRC).convert("RGB")
    if top_img.size != bottom_img.size:
        bottom_img = bottom_img.resize(top_img.size)

    composite = build_composite(top_img, bottom_img)
    out1 = HERE / "5_shadow_and_body.png"
    composite.save(out1)
    print(f"[ok] {out1}")

    with_word = add_bridging_word(composite, "WOOD")
    out2 = HERE / "6_written_twice.png"
    with_word.save(out2)
    print(f"[ok] {out2}")


if __name__ == "__main__":
    main()
