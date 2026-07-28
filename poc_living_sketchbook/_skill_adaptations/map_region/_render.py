"""ArkAIology "ANCIENT REGION" map move, re-skinned into the living-sketchbook
hand-drawn style: a hand-inked DASHED ring marking an approximate ancient
territory, with a MANDATORY sourcing/honesty tag beneath it.

This is fundamentally an HONESTY device, carried over exactly from
ArkAIology's /vox-map rule: precise historical borders for Bible-era
territories are NOT verifiable the way modern borders are, so a Bible-era
entity may only ever go on a map via this stylized (never solid/precise)
treatment. The ring must always be a wobbled hand-drawn dashed line, never a
clean vector dash and never a filled/solid shape -- and the honesty tag below
it may never be dropped.

Composited over the real Jericho siege-map still (bird's-eye view + the
existing march-loop artwork), scaled/center-cropped to 1080x1920 with the
same base_canvas() pattern used across tonight's POCs. Ring placement was
picked by an edge-density scan of the actual pixels (not eyeballing a
thumbnail) -- the openest paper in the whole frame is the band above the
existing dashed march-loop and clear of the city linework.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/map_region/_render.py
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
JERICHO = HERE.parents[1] / "jericho"
OUT_PATH = HERE / "ancient_region.png"

W, H = 1080, 1920
INK = (35, 30, 26)
FADED_INK = (75, 62, 48)      # ink-brown -- the hand-drawn ring + label
FADED_ITALIC = (100, 85, 68)  # lighter faded ink -- the honesty tag (quiet, not a warning label)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_ZILLA_I = "C:/Windows/Fonts/ZillaSlab-Italic.ttf"


def wrap_text(text, font_path, size, max_w):
    font = ImageFont.truetype(font_path, size)
    tmp = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp)
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def base_canvas(still_name):
    im = Image.open(JERICHO / "stills" / f"{still_name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def hand_dashed_ellipse(canvas, center, rx, ry, color, seed=7, base_width=4):
    """A cartographer's rough-sketched territory ring: an organically
    wobbled boundary curve (built from a few random-phase sine harmonics, so
    it gently bulges/pinches instead of tracing a perfect ellipse), walked by
    irregular hand-drawn dashes -- randomized dash/gap lengths, per-dash
    perpendicular jitter, per-dash width and ink-alpha variance, and the
    occasional pen-lift ink blot at a dash end. Never a clean vector dash.
    """
    rng = random.Random(seed)
    cx, cy = center
    n = 720
    wobble_terms = [
        (rng.uniform(2, 3), rng.uniform(7, 13), rng.uniform(0, math.tau)),
        (rng.uniform(4, 6), rng.uniform(4, 7), rng.uniform(0, math.tau)),
        (rng.uniform(7, 9), rng.uniform(2, 3.5), rng.uniform(0, math.tau)),
    ]
    pts = []
    for i in range(n + 1):
        t = i / n * math.tau
        wob = sum(amp * math.sin(freq * t + ph) for freq, amp, ph in wobble_terms)
        x = cx + (rx + wob) * math.cos(t)
        y = cy + (ry + wob * ry / rx) * math.sin(t)
        pts.append((x, y))

    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    i = 0
    on = True
    while i < len(pts) - 2:
        run = rng.randint(9, 22) if on else rng.randint(6, 17)
        j = min(i + run, len(pts) - 1)
        if on and j > i:
            seg = pts[i:j + 1]
            jit = rng.uniform(-1.8, 1.8)
            dx, dy = seg[-1][0] - seg[0][0], seg[-1][1] - seg[0][1]
            ln = math.hypot(dx, dy) or 1
            nx, ny = -dy / ln, dx / ln
            seg = [(px + nx * jit, py + ny * jit) for px, py in seg]
            w = max(2, int(round(base_width + rng.uniform(-1.4, 1.4))))
            a = rng.randint(170, 255)
            ld.line(seg, fill=(*color, a), width=w, joint="curve")
            if rng.random() < 0.13:
                ex, ey = seg[-1]
                r = w * 0.9
                ld.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(*color, a))
        i = j
        on = not on

    canvas.alpha_composite(layer)


def stamped_text(canvas, text, center, font_path, size, color, rotate=0.0, seed=1,
                  letter_spacing=0):
    """Locked INK STAMP grammar (living-sketchbook SKILL.md sec.5): rough
    per-pixel pressed-ink texture -- alpha = glyph mask x blurred noise, no
    clean vector edges, no rectangle behind it. Used for both the hand-
    lettered map label and the honesty tag so everything reads as pressed
    onto the page, never a floating screen element."""
    font = ImageFont.truetype(font_path, size)
    tmp = Image.new("L", (10, 10))
    td = ImageDraw.Draw(tmp)
    bb = td.textbbox((0, 0), text, font=font)
    th = bb[3] - bb[1]
    if letter_spacing:
        widths = [td.textlength(ch, font=font) for ch in text]
        tw = sum(widths) + letter_spacing * (len(text) - 1)
    else:
        widths = None
        tw = bb[2] - bb[0]
    pad = 20
    stamp = Image.new("L", (int(tw) + 2 * pad, int(th) + 2 * pad), 0)
    sd = ImageDraw.Draw(stamp)
    if letter_spacing:
        x = pad
        for ch, wch in zip(text, widths):
            sd.text((x, pad - bb[1]), ch, font=font, fill=255)
            x += wch + letter_spacing
    else:
        sd.text((pad - bb[0], pad - bb[1]), text, font=font, fill=255)

    rng = random.Random(seed)
    noise = Image.new("L", stamp.size)
    noise.putdata([rng.randint(70, 255) for _ in range(stamp.width * stamp.height)])
    noise = noise.filter(ImageFilter.GaussianBlur(1.0))
    a = (np.array(stamp).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.5, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))
    inked = Image.new("RGBA", stamp.size, (*color, 0))
    inked.putalpha(alpha)
    if rotate:
        inked = inked.rotate(rotate, expand=True, resample=Image.BICUBIC)
    ox = int(center[0] - inked.width / 2)
    oy = int(center[1] - inked.height / 2)
    canvas.alpha_composite(inked, (ox, oy))


def render():
    canvas = base_canvas("j03_laps").convert("RGBA")

    # PLACEMENT FIX (2026-07-28, user catch): the first pass put the region
    # in a narrow vertical corridor beside the city, forcing "THE LAND OF
    # CANAAN" to stack into 3 cramped lines -- a territory ring should read
    # HORIZONTAL (wide, short), like a real hand-drawn region on a map, not
    # a tall narrow bubble. Re-scanned the true-black-ink mask (threshold
    # <105) across the WHOLE frame: y0-200 is ink-free across nearly the
    # full width (one single stray pixel at x764-765, negligible) -- clear
    # above both the city and the existing march-loop's topmost dash
    # (which starts ~y230). That top band is wide enough for a genuinely
    # horizontal ring with the label on ONE line.
    ring_center = (545, 110)
    rx, ry = 320, 62
    label_max_w = 620

    hand_dashed_ellipse(canvas, ring_center, rx, ry, FADED_INK, seed=42, base_width=4)

    label_lines = wrap_text("THE LAND OF CANAAN", F_ZILLA, 40, label_max_w)
    line_h = 50
    y0 = ring_center[1] - (len(label_lines) - 1) * line_h / 2
    for i, ln in enumerate(label_lines):
        stamped_text(canvas, ln, (ring_center[0], y0 + i * line_h),
                     F_ZILLA, 40, INK, rotate=(-0.4 if i % 2 == 0 else 0.3),
                     seed=5 + i, letter_spacing=4)

    # MANDATORY honesty tag -- never optional, never dropped. Quiet and
    # legible: a scholar's marginal caveat, not a warning label. Sits below
    # the wide ring, still one line, still comfortably inside the clear
    # top band (ring bottom ~172, tag baseline ~200, loop starts ~230).
    tag_lines = wrap_text("APPROXIMATE EXTENT · BOUNDARIES NOT PRECISELY KNOWN",
                           F_ZILLA_I, 24, 560)
    tag_line_h = 32
    tag_y0 = ring_center[1] + ry + 30
    for i, ln in enumerate(tag_lines):
        stamped_text(canvas, ln, (ring_center[0], tag_y0 + i * tag_line_h),
                     F_ZILLA_I, 24, FADED_ITALIC, rotate=(-0.3 if i % 2 == 0 else 0.2),
                     seed=9 + i, letter_spacing=1)

    canvas.convert("RGB").save(OUT_PATH)
    print(f"[ok] {OUT_PATH}")


if __name__ == "__main__":
    render()
