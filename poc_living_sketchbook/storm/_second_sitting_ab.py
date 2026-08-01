"""Second Sitting A/B prototype (round 5) -- the book in time: late in the
episode, cut BACK to s03 (the terrified disciples, "carest thou not that we
perish?") for ~2.5s: the same plate, unchanged but for one new margin line in
elder-faded ink -- "...and there was a great calm." -- the page that panicked,
annotated by the calm it couldn't see coming.

Renders BOTH arms of the A/B:
  _round5_demos/second_sitting_B_annotated.mp4  (the revisit, annotated)
  _round5_demos/second_sitting_A_straight.mp4   (same plate, no annotation)
The A/B question is the round-5 doc's governor: does the annotated revisit
read as PAYOFF (build it) or padding (kill it)? User judges by eye.

$0 deterministic. The addition is overlay ink only -- the plate is never
re-rendered (drift-proof by construction). Placement: top cream margin,
centered (x 0.29-0.71 -- clear of the AWAKEDEN zone x<0.22 and of the wave
art below y~0.075).

  ..\\..\\.venv\\Scripts\\python.exe _second_sitting_ab.py
"""
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "panel_animator"))
from raking_light import scale_crop  # noqa: E402

OUT_DIR = HERE / "_round5_demos"
OUT_DIR.mkdir(exist_ok=True)
FPS = 30
W, H = 1080, 1920
DUR = 2.5

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
ELDER_INK = (94, 72, 50)
ELDER_RUBRIC = (146, 44, 36)

LINE = "\u2026and there was a great calm."   # KJV fragment, ellipsis marks it honestly
REF = "MATTHEW 8:26"
WRITE_AT, WRITE_DUR = 0.4, 1.3
FONT_SIZE = 42
BASELINE_Y = 66   # glyph TOP y -- the line lives in the top cream margin
PUNCT = set(".,;:'\u2019\u201c\u201d")


def glyph_layers(draw_probe):
    """Pre-render each glyph (elder Scribed Ink register: per-glyph wobble +
    the KUNSTLER punctuation fix) with its x-advance and reveal index."""
    font = ImageFont.truetype(F_KUNSTLER, FONT_SIZE)
    font_punct = ImageFont.truetype(F_KUNSTLER, int(FONT_SIZE * 1.7))
    rng = random.Random(17)
    widths = [draw_probe.textlength(ch, font=font) for ch in LINE]
    total = sum(widths)
    x = (W - total) / 2
    glyphs = []
    for ch, cw in zip(LINE, widths):
        jy, jr = rng.uniform(-2.2, 2.2), rng.uniform(-1.2, 1.2)
        gf = font_punct if ch in PUNCT else font
        layer = Image.new("RGBA", (int(FONT_SIZE * 2.6), int(FONT_SIZE * 2.8)), (0, 0, 0, 0))
        gd = ImageDraw.Draw(layer)
        gd.text((10, 10), ch, font=gf, fill=(*ELDER_INK, 235),
                stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*ELDER_INK, 235))
        layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + FONT_SIZE * 0.6))
        glyphs.append((layer, int(x) - 10, int(BASELINE_Y + jy) - 10))
        x += cw
    return glyphs


def annotated_frame(plate, glyphs, ref_font, t):
    """Plate + however much of the margin line time t has earned."""
    out = plate.convert("RGBA")
    n = len(glyphs)
    k = 0 if t < WRITE_AT else min(n, int((t - WRITE_AT) / WRITE_DUR * n) + 1)
    for layer, gx, gy in glyphs[:k]:
        out.alpha_composite(layer, (gx, gy))
    if t >= WRITE_AT + WRITE_DUR + 0.15:
        d = ImageDraw.Draw(out)
        rb = d.textbbox((0, 0), REF, font=ref_font)
        d.text(((W - (rb[2] - rb[0])) // 2, BASELINE_Y + int(FONT_SIZE * 1.15)),
               REF, font=ref_font, fill=(*ELDER_RUBRIC, 210))
    return out.convert("RGB")


def render(name, frame_fn):
    work = OUT_DIR / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    n = int(DUR * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = OUT_DIR / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def main():
    plate = scale_crop(Image.open(HERE / "stills" / "s03_screaming.png").convert("RGB"), W, H)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    glyphs = glyph_layers(probe)
    ref_font = ImageFont.truetype(F_ZILLA, 22)

    render("second_sitting_B_annotated", lambda t: annotated_frame(plate, glyphs, ref_font, t))
    render("second_sitting_A_straight", lambda t: plate)
    print("[a/b] B = revisit annotated by the calm; A = same plate straight. User judges.")


if __name__ == "__main__":
    main()
