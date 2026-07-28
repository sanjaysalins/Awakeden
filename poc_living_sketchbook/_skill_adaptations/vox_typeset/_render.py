"""Vox-Typeset adaptation: ArkAIology's /vox-type kinetic-word treatment
(letters set one by one like an old printing press's composing stick, small
blinking cursor) reworked into this project's visual language as a DELIBERATE
ALTERNATE register to Scribed Ink (see .claude/skills/living-sketchbook/SKILL.md
Sec.5). Scribed Ink = a scribe's HANDWRITTEN pen (script font, per-letter
baseline/rotation wobble, curved underline swash, rubric-red reference).
Typeset = a compositor's MECHANICALLY PRINTED page: a bold slab serif, letters
perfectly rigid on the baseline (real metal type is cast uniform -- it cannot
wobble), each glyph still gets its own stamped/pressed ink-density texture
(reusing the glyph-mask x blurred-noise technique from render_display_stamp()
in poc_living_sketchbook/_lettering_compare/_render_candidates.py) because a
real press deposits ink unevenly letter to letter even though the type itself
never moves. The "blinking cursor" becomes a small gold printer's fleuron
sitting in the next slot of the composing stick, right after the last letter
-- static here since this is the fully-set end-state reference frame; the
letter-by-letter reveal timing is the video assembler's job later.

This is a static PROOF-OF-GRAMMAR frame, not a production render: $0, pure
PIL, no new AI generation.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/vox_typeset/_render.py
"""
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
STILL = HERE.parents[1] / "jericho" / "stills" / "j12_line.png"
OUT = HERE
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
INK = (35, 30, 26)
FADED_INK = (70, 62, 54)
GOLD = (185, 146, 74)
GOLD_DARK = (120, 90, 38)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"

TEXT = "IN THE BEGINNING"
REF = "GENESIS 1:1  \u00b7  JOHN 1:1"


def base_canvas(path):
    """Same crop pattern as _lettering_compare/_render_candidates.py:
    scale-to-cover then center-crop to the 9:16 frame."""
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def stamp_glyph(ch, font, color, seed, size=(150, 160), origin=(24, 24)):
    """One letter as a rough-pressed ink stamp: glyph mask x blurred noise ->
    alpha. Same math as render_display_stamp(); called PER GLYPH with a unique
    seed so ink density varies letter to letter (uneven press impression)
    while the letterform itself (size, position, angle) stays perfectly rigid
    -- real cast type cannot wobble, only the ink deposit can."""
    mask = Image.new("L", size, 0)
    md = ImageDraw.Draw(mask)
    md.text(origin, ch, font=font, fill=255, stroke_width=2, stroke_fill=255)
    rng = random.Random(seed)
    noise = Image.new("L", size)
    noise.putdata([rng.randint(55, 255) for _ in range(size[0] * size[1])])
    noise = noise.filter(ImageFilter.GaussianBlur(1.1))
    a = (np.array(mask).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.6, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))
    inked = Image.new("RGBA", size, (*color, 0))
    inked.putalpha(alpha)
    return inked, origin


def draw_fleuron(canvas, cx, cy, r=17):
    """Gold diamond printer's fleuron standing in for the blinking cursor:
    the next slot in the compositor's stick, set and waiting. The one gold
    accent in an otherwise ink-black/faded-brown mechanical register."""
    pad = r * 3
    layer = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    lx, ly = pad, pad
    pts = [(lx, ly - r), (lx + r, ly), (lx, ly + r), (lx - r, ly)]
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon(pts, fill=(20, 15, 10, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    layer.alpha_composite(shadow, (2, 3))
    ld.polygon(pts, fill=(*GOLD, 255), outline=(*GOLD_DARK, 255), width=2)
    ld.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(*INK, 230))
    canvas.alpha_composite(layer, (int(cx - pad), int(cy - pad)))


def fit_font_size(text, tracking, max_w):
    size = 88
    tmp = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp)
    while size > 40:
        font = ImageFont.truetype(F_ZILLA, size)
        w = sum(d.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)
        if w <= max_w:
            return font, w
        size -= 2
    return ImageFont.truetype(F_ZILLA, size), sum(d.textlength(ch, font=font) for ch in text)


def render_typeset():
    canvas = base_canvas(STILL).convert("RGBA")
    tmp = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp)

    tracking = 6
    max_w = int(W * 0.86)
    font, text_w = fit_font_size(TEXT, tracking, max_w)

    y = int(H * 0.695)
    x = (W - text_w) / 2
    cx = x
    for i, ch in enumerate(TEXT):
        adv = d.textlength(ch, font=font)
        if ch != " ":
            stamp, origin = stamp_glyph(ch, font, INK, seed=1000 + i)
            canvas.alpha_composite(stamp, (int(cx) - origin[0], int(y) - origin[1]))
        cx += adv + tracking
    last_x = cx - tracking  # right edge of the set line

    # printer's fleuron: gold, next slot after the last letter, static cursor
    cap_h = font.size * 0.62
    fleuron_cy = y + cap_h * 0.5
    fleuron_cx = last_x + 28
    draw_fleuron(canvas, fleuron_cx, fleuron_cy, r=16)

    # dead-straight ruled baseline under the set line -- mechanical, no wobble
    # (the direct contrast to Scribed Ink's hand-drawn curved underline swash)
    d2 = ImageDraw.Draw(canvas)
    rule_y = y + cap_h + 34
    rule_x0, rule_x1 = x - 4, fleuron_cx + 44
    d2.line([(rule_x0, rule_y), (rule_x1, rule_y)], fill=(*FADED_INK, 150), width=2)

    # reference, small tracked caps, same mechanical ink -- gold stays the ONE accent
    ref_font = ImageFont.truetype(F_ZILLA, 25)
    ref_tracking = 3
    ref_w = sum(d.textlength(ch, font=ref_font) for ch in REF) + ref_tracking * (len(REF) - 1)
    rx = (W - ref_w) / 2
    ry = rule_y + 26
    for ch in REF:
        adv = d.textlength(ch, font=ref_font)
        if ch != " ":
            d2.text((rx, ry), ch, font=ref_font, fill=(*FADED_INK, 235))
        rx += adv + ref_tracking

    # dev-review footer label (matches the _lettering_compare candidate convention;
    # not part of the in-world lettering, purely for eye-checking this reference frame)
    label_font = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 24)
    d2.text((30, H - 90),
             "VOX-TYPESET: mechanical composing-stick type, gold fleuron cursor --\n"
             "alternate register to Scribed Ink (handwritten). Letters rigid, ink uneven.",
             font=label_font, fill=(*INK, 255))

    canvas.convert("RGB").save(OUT / "typeset_beginning.png")
    print("[ok] typeset_beginning.png ->", OUT / "typeset_beginning.png")


if __name__ == "__main__":
    render_typeset()
