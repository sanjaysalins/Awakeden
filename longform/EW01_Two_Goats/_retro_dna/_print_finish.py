"""Clean LIGHT retro print-finish (2026-07-23). Preserves a render's native
Ben-Day dots and just adds: gentle cream newsprint, a light limited-palette
posterize, a faint dot reinforcement, and a SUBTLE (not muddy) CMYK
misregistration fringe. $0 PIL. Reusable pass for finished frames.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_print_finish.py <img> [<img>...]
  (no args = finish the _true_retro/*.png set + build before/after strips)
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageChops, ImageEnhance

HERE = Path(__file__).resolve().parent
PAPER = (240, 229, 200)


def halftone(gray, pitch=5, angle=15):
    g = gray.rotate(angle, expand=1, fillcolor=255)
    W, H = g.size
    dots = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(dots)
    px = g.load()
    for y in range(0, H, pitch):
        for x in range(0, W, pitch):
            s = n = 0
            for yy in range(y, min(y + pitch, H), 2):
                for xx in range(x, min(x + pitch, W), 2):
                    s += px[xx, yy]; n += 1
            r = (1 - (s / max(n, 1)) / 255) * (pitch * 0.66)
            if r > 0.4:
                cx, cy = x + pitch / 2, y + pitch / 2
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
    o = dots.rotate(-angle, expand=0)
    L = (o.width - gray.width) // 2, (o.height - gray.height) // 2
    return o.crop((L[0], L[1], L[0] + gray.width, L[1] + gray.height))


def finish(img, dot=0.13, misreg=1, shadow_floor=125):
    """LIGHT balanced finish: keep native colour + clean solids; add cream paper,
    dots ONLY in the dark areas (solids/faces stay flat), a subtle misreg fringe."""
    img = img.convert("RGB"); W, H = img.size
    white = Image.new("RGB", (W, H), (255, 255, 255))
    base = ImageEnhance.Color(img).enhance(0.96)             # keep native palette, faint desat
    base = ImageChops.multiply(base, Image.blend(white, Image.new("RGB", (W, H), PAPER), 0.20))  # light cream
    # dots sized by darkness, then MASK to the dark areas only (solids/faces stay clean)
    gray = ImageOps.grayscale(img)
    d = halftone(gray, 5).convert("RGB")
    dotted = ImageChops.multiply(base, Image.blend(white, d, dot))
    mask = gray.point(lambda v: 255 if v < shadow_floor else 0)  # allow dots only where dark
    base = Image.composite(dotted, base, mask)
    # very subtle misregistration fringe
    r, g, b = base.split()
    r = ImageChops.offset(r, misreg, 0); b = ImageChops.offset(b, -misreg, 0)
    base = Image.blend(base, Image.merge("RGB", (r, g, b)), 0.18)
    return base


def main():
    args = sys.argv[1:]
    if args:
        for a in args:
            p = Path(a); finish(Image.open(p)).save(p.with_name(p.stem + "_finished.png"))
            print("ok", p.with_name(p.stem + "_finished.png"))
        return
    src = HERE / "_true_retro"
    out = HERE / "_true_retro_finished"; out.mkdir(exist_ok=True)
    for p in sorted(src.glob("*.png")):
        im = Image.open(p).convert("RGB")
        im2 = im.resize((im.width // 2, im.height // 2))
        fin = finish(im2)
        strip = Image.new("RGB", (im2.width * 2 + 12, im2.height), (20, 17, 9))
        strip.paste(im2, (0, 0)); strip.paste(fin, (im2.width + 12, 0))
        strip.save(out / f"{p.stem}_beforeafter.png")
        fin.save(out / f"{p.stem}_finished.png")
        print("ok", p.stem)
    print("[out]", out)


if __name__ == "__main__":
    main()
