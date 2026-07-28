"""vox-lowerThird adaptation POC: ArkAIology's documentary chapter/act title card
(kicker + title + flat gold rule, `six_10.png`) rebuilt in this series' hand-made
sketchbook grammar -- NO card/box behind anything, a real gold-LEAF texture
(cropped from this episode's own art) instead of a flat vector rule, and thin
ink hairline rules bracketing the block like a printed page's chapter heading
(same technique as render_illuminated_rubric() in
poc_living_sketchbook/_lettering_compare/_render_candidates.py).

Renders TWO candidates for the gold rule (real cropped gold-leaf texture vs. a
procedurally drawn+noised gold rectangle) so the choice is a real comparison,
not a guess, then ships the winner as lowerthird_act2.png.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/vox_lowerthird/_render.py
"""
import random

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
JERICHO = HERE.parents[1] / "jericho"
OUT = HERE

W, H = 1080, 1920
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)
FADED_INK = (70, 62, 54)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_ZILLA_I = "C:/Windows/Fonts/ZillaSlab-Italic.ttf"

KICKER = "ACT TWO"
TITLE = "THE FALL OF THE WALL"


# ---------------------------------------------------------------- helpers
def base_canvas(still_name):
    """Same scale+center-crop-to-1080x1920 pattern used across this POC set."""
    im = Image.open(JERICHO / "stills" / f"{still_name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def wrap(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked_width(d, text, font, tracking):
    return sum(d.textlength(ch, font=font) for ch in text) + tracking * max(0, len(text) - 1)


def draw_tracked_centered(d, text, font, cy, tracking, fill, cx=W / 2):
    tw = tracked_width(d, text, font, tracking)
    x = cx - tw / 2
    for ch in text:
        d.text((x, cy), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return tw


def hairline(d, y, margin=90, color=(*FADED_INK, 130), width=2):
    d.line([(margin, y), (W - margin, y)], fill=color, width=width)


# ---------------------------------------------------------------- gold rule, candidate A: real texture
def gold_rule_texture(width, thickness, seed=7):
    """Crop the real vertical gold-leaf strip visible on the right edge of
    j06_thread.png (confirmed by pixel scan: strip runs x~1420-1485 of a
    1536-wide source, full column, genuine textured gold-leaf grain -- not a
    flat fill), rotate it to run horizontal, then mask it with a wobbled
    (irregular, deckle-ish) top/bottom edge so it reads as a pressed leaf
    strip, not a ruled vector line."""
    src = Image.open(JERICHO / "stills" / "j06_thread.png").convert("RGB")
    strip = src.crop((1405, 260, 1495, 2440))  # tall narrow real gold-leaf column
    strip = strip.transpose(Image.ROTATE_90)  # now runs horizontal (wide x thin)
    scale = thickness / strip.height
    new_w = max(width, int(strip.width * scale))
    strip = strip.resize((new_w, thickness), Image.LANCZOS)
    x0 = (new_w - width) // 2
    band = strip.crop((x0, 0, x0 + width, thickness))
    band = ImageEnhance.Color(band).enhance(1.25)
    band = ImageEnhance.Contrast(band).enhance(1.12)
    band = ImageEnhance.Brightness(band).enhance(1.05)
    band = band.convert("RGBA")

    mask = Image.new("L", (width, thickness), 0)
    md = ImageDraw.Draw(mask)
    rng = random.Random(seed)
    n = 16
    top_pts = [(t * width / n, rng.uniform(0, 3.5)) for t in range(n + 1)]
    bot_pts = [(t * width / n, thickness - rng.uniform(0, 3.5)) for t in range(n + 1)]
    md.polygon(top_pts + bot_pts[::-1], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))
    band.putalpha(mask)
    return band


# ---------------------------------------------------------------- gold rule, candidate B: drawn + noised
def gold_rule_drawn(width, thickness, seed=7):
    """Procedural alternative: a wobbled-edge rectangle filled flat GOLD, then
    multiplied by blurred noise so it isn't a clean vector fill -- the same
    stamped-texture trick as render_display_stamp()'s ink, tinted gold."""
    import numpy as np

    rng = random.Random(seed)
    mask = Image.new("L", (width, thickness), 0)
    md = ImageDraw.Draw(mask)
    n = 16
    top_pts = [(t * width / n, rng.uniform(0, 3.5)) for t in range(n + 1)]
    bot_pts = [(t * width / n, thickness - rng.uniform(0, 3.5)) for t in range(n + 1)]
    md.polygon(top_pts + bot_pts[::-1], fill=255)

    noise = Image.new("L", (width, thickness))
    noise.putdata([rng.randint(140, 255) for _ in range(width * thickness)])
    noise = noise.filter(ImageFilter.GaussianBlur(1.4))
    a = (np.array(mask).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.3, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))

    band = Image.new("RGBA", (width, thickness), (*GOLD, 0))
    band.putalpha(alpha)
    return band


# ---------------------------------------------------------------- the card itself
def render_lowerthird(gold_rule_fn, out_name, tag):
    canvas = base_canvas("j04_wallface").convert("RGBA")
    d = ImageDraw.Draw(canvas)

    kicker_font = ImageFont.truetype(F_ZILLA, 30)
    title_font = ImageFont.truetype(F_ZILLA_I, 82)

    y = 980
    hairline(d, y)
    y += 46
    draw_tracked_centered(d, KICKER, kicker_font, y, tracking=9, fill=(*RUBRIC, 255))
    y += 58

    rule_w, rule_h = 560, 26
    rule = gold_rule_fn(rule_w, rule_h)
    canvas.alpha_composite(rule, (int((W - rule_w) / 2), y))
    y += rule_h + 44

    lines = wrap(TITLE, title_font, W - 2 * 90, d)
    line_h = 96
    for ln in lines:
        bb = d.textbbox((0, 0), ln, font=title_font)
        lw = bb[2] - bb[0]
        d.text(((W - lw) / 2 - bb[0], y), ln, font=title_font, fill=(*INK, 255))
        y += line_h
    y += 4
    hairline(d, y)

    out_path = OUT / out_name
    canvas.convert("RGB").save(out_path)
    print(f"[ok] {tag} -> {out_path}")
    return out_path


def main():
    render_lowerthird(gold_rule_texture, "lowerthird_act2_candidate_texture.png", "candidate A (cropped gold-leaf texture)")
    render_lowerthird(gold_rule_drawn, "lowerthird_act2_candidate_drawn.png", "candidate B (drawn + noised rectangle)")
    # SHIPPED: candidate A -- see report for why (real leaf grain beats a
    # procedural fill at this scale/thickness; texture-map decisions are eye
    # calls we get to make once, not something to leave to chance).
    winner = render_lowerthird(gold_rule_texture, "lowerthird_act2.png", "SHIPPED (candidate A)")
    print(f"[shipped] {winner}")


if __name__ == "__main__":
    main()
