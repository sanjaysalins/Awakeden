"""CHRONO SWEEP -- adapted from ArkAIology's /vox-map skill (a horizontal
era-timeline rail with a sweeping highlight + event pings, synced to
verified chronology data) into our own living-sketchbook hand-drawn style.

Honesty constraint (this project's locked no-invented-precision rule): no
precise BC year is asserted anywhere on this image. The three stops are
named EVENTS/PERIODS only (THE EXODUS / 40 YEARS -- THE WILDERNESS /
JERICHO FALLS), each grounded in a real KJV reference, and the whole
diagram carries a small visible "(illustrative order, not to scale)" note.
The "sweep" itself is rendered as the rail's own ink firming up (thin +
pale at the start, thicker + darker by the end) plus a gold glow at the
climactic stop -- not as a highlighter bar (that reads as a UI chip, the
thing this whole lettering system was rebuilt to get away from).

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/map_chrono/_render.py
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
LETTERING_DIR = HERE.parents[1] / "_lettering_compare"
sys.path.insert(0, str(LETTERING_DIR))
from _render_new_finds import aged_paper_canvas, W, H, INK, RUBRIC, GOLD, FADED_INK  # noqa: E402

OUT = HERE / "chrono_sweep.png"

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_CORMORANT_I = "C:/Windows/Fonts/CormorantInfant-Italic.ttf"

RAIL_Y = 1180
RAIL_X0 = 130
X1, X2, X3 = 240, 545, 840  # THE EXODUS / 40 YEARS WILDERNESS / JERICHO FALLS
TAIL_END = X3 + 70


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c0, c1, t):
    return tuple(int(round(lerp(a, b, t))) for a, b in zip(c0, c1))


def wobble_points(x0, y0, x1, y1, seed, n=48, amp=1.4):
    rng = random.Random(seed)
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + rng.uniform(-amp, amp)
        pts.append((x, y))
    return pts


def centered_text(draw, cx, y, text, font, fill, stroke_width=0, stroke_fill=None, clip_margin=40, canvas_w=W):
    tw = draw.textlength(text, font=font) + 2 * stroke_width
    x = cx - tw / 2
    x = max(clip_margin, min(canvas_w - clip_margin - tw, x))
    kwargs = {}
    if stroke_width:
        kwargs = dict(stroke_width=stroke_width, stroke_fill=stroke_fill)
    draw.text((x + stroke_width, y), text, font=font, fill=fill, **kwargs)
    return x, tw


def draw_tick(draw, x, y_center, seed, tall=False):
    rng = random.Random(seed)
    half = 8 if tall else 5
    jx = rng.uniform(-1.0, 1.0)
    draw.line([(x + jx, y_center - half), (x + jx, y_center + half)],
              fill=(*FADED_INK, 190), width=2 if tall else 1)


def draw_ruled_rail(draw):
    """The rail itself carries the 'sweep' -- pale/thin at the start,
    firming to full ink-black/thicker by Jericho. This IS the sweeping
    highlight, ported without a highlighter-bar UI chip."""
    pts = wobble_points(RAIL_X0, RAIL_Y, X3, RAIL_Y, seed=3, n=70, amp=1.2)
    n = len(pts) - 1
    for i in range(n):
        t = i / (n - 1)
        color = lerp_color(FADED_INK, INK, t)
        width = int(round(lerp(2, 4, t)))
        draw.line([pts[i], pts[i + 1]], fill=(*color, 255), width=width)
    # a faint second rule below the main line -- the ledger-sheet double rule
    pts2 = wobble_points(RAIL_X0, RAIL_Y + 9, X3, RAIL_Y + 9, seed=17, n=60, amp=1.0)
    draw.line(pts2, fill=(*FADED_INK, 130), width=1, joint="curve")
    # a short fading tail past Jericho -- the story keeps going past this frame
    tail = wobble_points(X3, RAIL_Y, TAIL_END, RAIL_Y, seed=23, n=10, amp=1.0)
    for i in range(len(tail) - 1):
        a = int(round(lerp(170, 0, i / (len(tail) - 2))))
        draw.line([tail[i], tail[i + 1]], fill=(*INK, a), width=2)


def draw_ticks(draw):
    x = RAIL_X0
    i = 0
    stops = (X1, X2, X3)
    while x <= X3:
        if not any(abs(x - s) < 18 for s in stops):
            draw_tick(draw, x, RAIL_Y, seed=1000 + i, tall=(i % 5 == 0))
        x += 26
        i += 1


def leader_tick(draw, x, y0, y1, seed, color=FADED_INK, alpha=200):
    pts = wobble_points(x, y0, x, y1, seed=seed, n=6, amp=1.0)
    draw.line(pts, fill=(*color, alpha), width=2)


def motion_hatches(draw, cx, cy, seed, color=FADED_INK, alpha=110):
    """Small trailing ink strokes -- the sweep having just passed through."""
    rng = random.Random(seed)
    for i in range(3):
        ang = math.radians(198 + rng.uniform(-12, 12))
        length = rng.uniform(14, 22)
        dist = 20 + i * 7
        x0 = cx + math.cos(ang) * dist
        y0v = cy + math.sin(ang) * dist
        x1 = x0 + math.cos(ang) * length
        y1v = y0v + math.sin(ang) * length
        draw.line([(x0, y0v), (x1, y1v)], fill=(*color, alpha), width=2)


def draw_ping_ink(draw, cx, cy, r=14, seed=1):
    pts = []
    rng = random.Random(seed)
    for i in range(28):
        a = i / 27 * 2 * math.pi
        rr = r + rng.uniform(-1.2, 1.2)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    pts.append(pts[0])
    draw.line(pts, fill=(*INK, 255), width=3, joint="curve")


def draw_ping_gold(canvas, draw, cx, cy, r=16, seed=2):
    # soft gold glow halo behind the marker -- gold leaf "burning" on the page
    glow = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([110 - 62, 110 - 62, 110 + 62, 110 + 62], fill=(*GOLD, 95))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    canvas.alpha_composite(glow, (int(cx - 110), int(cy - 110)))
    draw = ImageDraw.Draw(canvas)
    pts = []
    rng = random.Random(seed)
    for i in range(28):
        a = i / 27 * 2 * math.pi
        rr = r + rng.uniform(-1.0, 1.0)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=(*GOLD, 255))
    pts.append(pts[0])
    draw.line(pts, fill=(*INK, 255), width=2, joint="curve")
    return draw


def render():
    canvas = aged_paper_canvas().convert("RGBA")
    d = ImageDraw.Draw(canvas)

    kicker_font = ImageFont.truetype(F_ZILLA, 36)
    label_font = ImageFont.truetype(F_ZILLA, 28)
    ref_font = ImageFont.truetype(F_ZILLA, 20)
    disclaimer_font = ImageFont.truetype(F_CORMORANT_I, 27)
    footer_font = ImageFont.truetype(F_ZILLA, 22)

    # -------- kicker + hairline (ties into the engineering-grid page style)
    centered_text(d, W / 2, 600, "THE JOURNEY TO CANAAN", kicker_font, (*INK, 255))
    hairline = wobble_points(RAIL_X0, 660, X3, 660, seed=5, n=40, amp=0.8)
    d.line(hairline, fill=(*FADED_INK, 120), width=1)

    # -------- the rail: hand-ruled ledger line + ticks
    draw_ruled_rail(d)
    draw_ticks(d)

    # -------- STOP 1: THE EXODUS (above rail, ink-black)
    centered_text(d, X1, 1020, "THE EXODUS", label_font, (*INK, 255))
    centered_text(d, X1, 1060, "EXODUS 12:41", ref_font, (*RUBRIC, 230))
    leader_tick(d, X1, 1086, RAIL_Y - 14 - 4, seed=101)
    draw_ping_ink(d, X1, RAIL_Y, r=14, seed=201)

    # -------- STOP 2: 40 YEARS -- THE WILDERNESS (below rail, ink-black)
    leader_tick(d, X2, RAIL_Y + 14 + 4, RAIL_Y + 130 - 6, seed=102)
    centered_text(d, X2, RAIL_Y + 130, "40 YEARS \u2014 THE WILDERNESS", label_font, (*INK, 255))
    centered_text(d, X2, RAIL_Y + 170, "NUMBERS 14:33\u201334", ref_font, (*RUBRIC, 230))
    draw_ping_ink(d, X2, RAIL_Y, r=14, seed=202)
    motion_hatches(d, X2, RAIL_Y, seed=302)

    # -------- STOP 3: JERICHO FALLS (above rail, GOLD -- the sacred arrival)
    d = draw_ping_gold(canvas, d, X3, RAIL_Y, r=16, seed=203)
    centered_text(d, X3, 1020, "JERICHO FALLS", label_font, (*GOLD, 255),
                  stroke_width=2, stroke_fill=(*INK, 255))
    centered_text(d, X3, 1060, "JOSHUA 6:20", ref_font, (*RUBRIC, 230))
    leader_tick(d, X3, 1086, RAIL_Y - 16 - 4, seed=103, color=GOLD, alpha=230)
    motion_hatches(d, X3, RAIL_Y, seed=303, color=GOLD, alpha=120)

    # -------- honesty note: small, legible, attached to the diagram itself
    centered_text(d, W / 2, RAIL_Y + 280, "(illustrative order, not to scale)",
                  disclaimer_font, (*FADED_INK, 235))

    # -------- provenance footer (matches this repo's POC-labeling convention)
    d.text((70, H - 90),
           "CHRONO SWEEP \u2014 adapted from ArkAIology /vox-map (era rail + event\n"
           "pings, hand-drawn) \u00b7 named periods only, no invented dates",
           font=footer_font, fill=(*FADED_INK, 220))

    canvas.convert("RGB").save(OUT)
    print(f"[ok] wrote {OUT}")


if __name__ == "__main__":
    render()
