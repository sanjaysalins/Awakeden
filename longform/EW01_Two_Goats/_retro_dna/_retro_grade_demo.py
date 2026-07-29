"""Retro print-grade demo (2026-07-23): turn an INK base into TRUE retro comic.
Applies a luminance-driven Ben-Day halftone + limited-palette posterize + cream
newsprint + CMYK misregistration to show the "base + treatment" the DNA needs.
$0 (PIL only). Builds before/after strips.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_retro_grade_demo.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageChops, ImageEnhance

HERE = Path(__file__).resolve().parent
EW = HERE.parent  # longform/EW01_Two_Goats
OUT = HERE / "_retro_grade"
OUT.mkdir(exist_ok=True)

SRCS = {
    "splash_cross": HERE / "splash_cross.png",
    "christ_painted": EW / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png",
}
PAPER = (232, 217, 181)   # #E8D9B5 newsprint


def halftone(gray: Image.Image, pitch: int = 6, angle: int = 15) -> Image.Image:
    """Luminance-driven dot screen: darker cell -> bigger black dot. White ground."""
    g = gray.rotate(angle, expand=1, fillcolor=255)
    W, H = g.size
    dots = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(dots)
    px = g.load()
    for y in range(0, H, pitch):
        for x in range(0, W, pitch):
            # average luminance of the cell
            s = n = 0
            for yy in range(y, min(y + pitch, H), 2):
                for xx in range(x, min(x + pitch, W), 2):
                    s += px[xx, yy]; n += 1
            lum = s / max(n, 1)
            r = (1 - lum / 255) * (pitch * 0.72)   # dark -> big dot
            if r > 0.4:
                cx, cy = x + pitch / 2, y + pitch / 2
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    return dots.rotate(-angle, expand=0).crop((
        (dots.width - gray.width) // 2, (dots.height - gray.height) // 2,
        (dots.width - gray.width) // 2 + gray.width,
        (dots.height - gray.height) // 2 + gray.height))


def misregister(img: Image.Image, shift: int = 2) -> Image.Image:
    r, g, b = img.split()
    r = ImageChops.offset(r, shift, 0)
    b = ImageChops.offset(b, -shift, 1)
    return Image.merge("RGB", (r, g, b))


def retro(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    W, H = img.size
    # 1. limited palette + a touch less saturation (printed, not glossy)
    base = ImageOps.posterize(img, 3)
    base = ImageEnhance.Color(base).enhance(0.9)
    base = ImageEnhance.Contrast(base).enhance(0.95)
    # 2. newsprint: multiply toward cream + let paper warm it
    paper = Image.new("RGB", (W, H), PAPER)
    base = ImageChops.multiply(base, Image.blend(Image.new("RGB", (W, H), (255, 255, 255)), paper, 0.35))
    # 3. Ben-Day dots from luminance, multiplied in (dots in the mid/shadows)
    dots = halftone(ImageOps.grayscale(img), pitch=6).convert("RGB")
    dots = Image.blend(Image.new("RGB", (W, H), (255, 255, 255)), dots, 0.55)  # soften dot strength
    base = ImageChops.multiply(base, dots)
    # 4. CMYK misregistration fringe
    base = misregister(base, 2)
    return base


def main():
    for name, src in SRCS.items():
        if not src.exists():
            print(f"[skip] missing {src}"); continue
        im = Image.open(src).convert("RGB")
        # work at half res for speed
        im2 = im.resize((im.width // 2, im.height // 2))
        graded = retro(im2)
        # before/after side by side
        strip = Image.new("RGB", (im2.width * 2 + 12, im2.height), (20, 17, 9))
        strip.paste(im2, (0, 0)); strip.paste(graded, (im2.width + 12, 0))
        strip.save(OUT / f"{name}_beforeafter.png")
        graded.save(OUT / f"{name}_retro.png")
        print(f"[ok] {name} -> {OUT / (name + '_beforeafter.png')}")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
