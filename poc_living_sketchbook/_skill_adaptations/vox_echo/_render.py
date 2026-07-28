"""
POC: adapt ArkAIology's /vox-type "echo" kinetic-word treatment into our own
living-sketchbook palette theology.

ArkAIology's echo = a REFRAIN word recurring through an episode, rendered as
a 3-color print-misregistration (their own palette). It's a natural fit here
because the device is already a PRINT artifact, not a screen-UI graphic -- the
only real adaptation is (a) our locked palette instead of theirs and (b) making
the misregistration read as genuinely old/analog, not a digital RGB-channel
glitch.

Technique: the word rendered 3x, each pass:
  - one solid color from OUR palette (RUBRIC / GOLD / FADED-INK)
  - offset a few px from the other two (a slightly out-of-alignment press)
  - partial opacity (~75-85%) so the passes overlap and misregister
  - a rough per-pixel "stamped" alpha (glyph mask x blurred noise) instead of
    a clean anti-aliased edge, per the living-sketchbook INK STAMP rule
      (.claude/skills/living-sketchbook/SKILL.md section 5)
Then one more very light paper-grain pass over the whole word so it reads as
printed-and-aged rather than a drop-shadow trick.

Test word: COME -- the series' own locked CTA verb ("So come", the In No Wise
Cast Out landing line) -- and echo's whole point is a word an episode DRUMS
repeatedly, so COME is the natural refrain candidate for a future episode.

Composite: the open-door glory beat -- thematically the natural home for an
invitation word.

    .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/vox_echo/_render.py
"""
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[3]
STILL = REPO / "poc_castbible_look" / "episode_door" / "stills" / "d10_opendoor.png"
OUT = HERE / "echo_come.png"

W, H = 1080, 1920

# living-sketchbook locked palette (matches poc_living_sketchbook/_lettering_compare
# and the task brief's hex refs: RUBRIC ~#961A16, GOLD ~#B9926A, FADED_INK ~#463E36)
RUBRIC = (150, 26, 22)       # blood-line / verse refs
GOLD = (185, 146, 74)        # His glory / sacred only
FADED_INK = (70, 62, 54)     # ink-black/faded-brown line work

FONT_PATH = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
WORD = "COME"
FONT_SIZE = 190
TEXT_CENTER_Y = int(H * 0.58)   # doorway/floor threshold -- clear of face, watermark zone, UI band

# 3-plate misregistration: (color, offset px, opacity)
PLATES = [
    (RUBRIC, (3, 2), 0.78),
    (GOLD, (-2, 3), 0.75),
    (FADED_INK, (0, -3), 0.85),
]


def base_canvas():
    im = Image.open(STILL).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def noise_field(size, lo, hi, seed, blur, tile):
    """Cheap paper-grain: small random tile upscaled + blurred."""
    rng = random.Random(seed)
    w, h = size
    small = Image.new("L", (max(2, w // tile), max(2, h // tile)))
    small.putdata([rng.randint(lo, hi) for _ in range(small.width * small.height)])
    return small.resize(size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))


def text_origin(draw, word, font):
    bbox = draw.textbbox((0, 0), word, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = W // 2 - tw // 2 - bbox[0]
    y = TEXT_CENTER_Y - th // 2 - bbox[1]
    return x, y, tw, th


def stamped_plate(word, font, base_xy, offset, color, opacity, seed):
    """One letterpress plate: glyph mask, softened + roughened, solid color, offset."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    x = base_xy[0] + offset[0]
    y = base_xy[1] + offset[1]
    d.text((x, y), word, font=font, fill=255)
    # ink-bleed soften, then a rough stamped edge (alpha = glyph mask x blurred noise)
    soft = mask.filter(ImageFilter.GaussianBlur(1.3))
    press_noise = noise_field((W, H), 195, 255, seed=seed, blur=1.6, tile=2)
    rough = ImageChops.multiply(soft, press_noise)
    alpha = rough.point(lambda v: int(v * opacity))
    layer = Image.new("RGBA", (W, H), (*color, 0))
    layer.putalpha(alpha)
    return layer


def add_print_grain(canvas_rgb, bbox, seed=99):
    """Very light paper-grain over just the word's region -- reused from
    the project's _paper_canvas grain technique (poc_comic_page /
    poc_living_sketchbook/_lettering_compare aged_paper_canvas)."""
    x0, y0, x1, y1 = bbox
    region = canvas_rgb.crop((x0, y0, x1, y1))
    w, h = region.size
    grain = noise_field((w, h), 118, 138, seed=seed, blur=0.9, tile=1)
    darker = ImageEnhance.Brightness(region).enhance(0.93)
    graded = Image.composite(darker, region, grain.point(lambda v: max(0, (v - 128) * 6)))
    canvas_rgb.paste(graded, (x0, y0))
    return canvas_rgb


def main():
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    canvas = base_canvas().convert("RGBA")
    tmp_draw = ImageDraw.Draw(canvas)
    base_xy = text_origin(tmp_draw, WORD, font)
    bx, by, tw, th = base_xy

    for i, (color, offset, opacity) in enumerate(PLATES):
        plate = stamped_plate(WORD, font, (bx, by), offset, color, opacity, seed=300 + i)
        canvas = Image.alpha_composite(canvas, plate)

    canvas_rgb = canvas.convert("RGB")

    pad = 60
    x0 = max(0, bx - pad)
    y0 = max(0, by - pad - 8)
    x1 = min(W, bx + tw + pad)
    y1 = min(H, by + th + pad + 8)
    canvas_rgb = add_print_grain(canvas_rgb, (x0, y0, x1, y1), seed=77)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas_rgb.save(OUT)
    print(f"[ok] wrote {OUT}")


if __name__ == "__main__":
    main()
