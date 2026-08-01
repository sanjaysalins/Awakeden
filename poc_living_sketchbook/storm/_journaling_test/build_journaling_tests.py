"""Journaler's-hand exploration round (2026-07-30) -- STILLS ONLY, $0.

The brief: everything the sketchbook does so far serves the NARRATION.
Nothing is the voice of the person KEEPING the book. These 7 test stills
composite a second, private, casual layer -- pencil reactions, margin
doodles, a highlighter swipe, arrows, a dated corner note, reaction marks --
over the already-approved Storm stills, so the user can SEE the language
before any motion is built.

Voices (kept deliberately distinct from the show's formal registers):
  - Scribed Ink (Kunstler, iron-gall INK, rubric-red refs)  = the scribe. UNTOUCHED.
  - Journaler   (Caveat, GRAPHITE pencil, looser jitter)    = the person. NEW.
  - Diary label (Ink Free, same graphite, smaller/printed)  = same person, printing.
  - Highlighter (ordinary marker YELLOW, never rubric-red)  = personal emphasis.
Rubric red stays reserved for Scripture citations/sacred marks -- hard rule.

Linework follows the house stroke grammar (annotators_circle): seeded
sum-of-sines wobble, TWO passes (full weight, then a lighter offset second
pass), round caps -- but in graphite weight/alpha, not ink.

Run:
  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_journaling_test/build_journaling_tests.py
"""
import importlib.util
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
STORM = HERE.parent
STILLS = STORM / "stills"

# import the real assembler as a module -- its scribed_ink_card() builds the
# byte-identical formal verse card (never re-implement the formal voice here)
spec = importlib.util.spec_from_file_location("storm_assemble", STORM / "_s4_assemble.py")
asm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(asm)

W, H = 1080, 1920
GRAPHITE = (82, 79, 76)           # neutral pencil gray -- NOT the show's warm iron-gall INK (35,30,26)
HIGHLIGHT = (252, 214, 50)        # ordinary marker yellow -- NEVER rubric-red (150,26,22)
F_CAVEAT = "C:/Windows/Fonts/Caveat-Regular.ttf"    # journaler's quick hand
F_INKFREE = "C:/Windows/Fonts/Inkfree.ttf"          # journaler's printed-label hand


def scale_crop(im, w=W, h=H):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def load_frame(name):
    return scale_crop(Image.open(STILLS / name).convert("RGB"))


# ---------------------------------------------------------------------------
# pencil primitives -- seeded hand-wobble, two-pass, graphite texture
# ---------------------------------------------------------------------------

def _smooth_noise(n, seed, sigma=4.0):
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(n + 24)
    kx = np.arange(-12, 13)
    k = np.exp(-(kx ** 2) / (2 * sigma ** 2))
    k /= k.sum()
    v = np.convolve(v, k, mode="same")[12:12 + n]
    m = np.max(np.abs(v)) or 1.0
    return v / m


def _resample(pts, step=3.5):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / step))
        for i in range(1, n + 1):
            out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
    return out


def wobble(pts, seed, amp=2.2):
    P = _resample(pts)
    if len(P) < 3:
        return P
    off = _smooth_noise(len(P), seed) * amp
    out = []
    for i, (x, y) in enumerate(P):
        a = P[max(0, i - 1)]
        b = P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        out.append((x + nx * off[i], y + ny * off[i]))
    return out


def _stroke(d, pts, color, width, alpha):
    d.line(pts, fill=(*color, alpha), width=width, joint="curve")
    r = width / 2.0
    for px, py in (pts[0], pts[-1]):
        d.ellipse((px - r, py - r, px + r, py + r), fill=(*color, alpha))


def pencil_texture(layer, seed, opacity=0.92):
    """Graphite grain: strokes are never solid ink -- modulate alpha by
    blurred noise + soften edges, so the marks read as pencil on tooth."""
    noise = Image.new("L", layer.size)
    rng = random.Random(seed)
    noise.putdata([rng.randint(150, 255) for _ in range(layer.width * layer.height)])
    noise = noise.filter(ImageFilter.GaussianBlur(0.6))
    a = np.array(layer)[:, :, 3].astype(np.float32)
    a = a * (np.array(noise, dtype=np.float32) / 255.0) * opacity
    a = np.array(Image.fromarray(a.astype("uint8")).filter(ImageFilter.GaussianBlur(0.4)))
    out = layer.copy()
    out.putalpha(Image.fromarray(a))
    return out


def draw_doodle(paths, seed, color=GRAPHITE, width=3, amp=2.2, pad=18):
    """paths: list of (pts, double). Returns a tight RGBA layer.
    House grammar: pass 1 full weight; double paths get a lighter, re-wobbled,
    slightly offset second pass (a hand going over its own line)."""
    xs = [p[0] for pts, _ in paths for p in pts]
    ys = [p[1] for pts, _ in paths for p in pts]
    x0, y0 = min(xs) - pad, min(ys) - pad
    lw = int(max(xs) - x0 + pad)
    lh = int(max(ys) - y0 + pad)
    layer = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, (pts, double) in enumerate(paths):
        loc = [(x - x0, y - y0) for x, y in pts]
        _stroke(d, wobble(loc, seed + i * 7, amp), color, width, 225)
        if double:
            loc2 = [(x + 1.6, y + 1.1) for x, y in loc]
            _stroke(d, wobble(loc2, seed + i * 7 + 101, amp * 1.2), color,
                    max(2, width - 1), 110)
    return pencil_texture(layer, seed + 500)


def pencil_text(text, size, seed, tilt=-2.0, font_path=F_CAVEAT, color=GRAPHITE):
    """The journaler's hand: per-char baseline/rotation jitter LOOSER than
    Scribed Ink's (+-3px/+-2.4deg vs +-2.5px/+-1.2deg), graphite texture,
    whole-note tilt. A quick private note, not calligraphy."""
    font = ImageFont.truetype(font_path, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    adv = [tmp.textlength(ch, font=font) + 0.8 for ch in text]
    lw = int(sum(adv)) + 60
    lh = int(size * 2.4)
    layer = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    rng = random.Random(seed)
    cx, y = 28.0, size * 0.5
    for ch, a in zip(text, adv):
        jy = rng.uniform(-3.0, 3.0)
        jr = rng.uniform(-2.4, 2.4)
        g = Image.new("RGBA", (int(size * 2.6), int(size * 2.6)), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.text((size * 0.6, size * 0.4), ch, font=font, fill=(*color, 235))
        g = g.rotate(jr, resample=Image.BICUBIC, center=(size * 0.6, size * 0.4 + size * 0.6))
        layer.alpha_composite(g, (int(cx - size * 0.6), int(y + jy - size * 0.4)))
        cx += a
    layer = pencil_texture(layer, seed + 31)
    if tilt:
        layer = layer.rotate(tilt, resample=Image.BICUBIC, expand=True)
    return layer


def paste(frame, layer, xy):
    fr = frame.convert("RGBA")
    fr.alpha_composite(layer, xy)
    return fr.convert("RGB")


# ---------------------------------------------------------------------------
# doodle shape vocab (local coords; small, idle, absent-minded)
# ---------------------------------------------------------------------------

def sun_paths(r=24):
    c = [(r + r * math.cos(t), r + r * math.sin(t))
         for t in np.linspace(-0.4, 2 * math.pi - 0.35, 46)]  # not-quite-closed circle
    paths = [(c, True)]
    rng = random.Random(9)
    for k in range(8):
        a = k * math.pi / 4 + rng.uniform(-0.12, 0.12)
        r0, r1 = r + 6, r + 15 + rng.uniform(-2, 3)
        paths.append(([(r + r0 * math.cos(a), r + r0 * math.sin(a)),
                       (r + r1 * math.cos(a), r + r1 * math.sin(a))], False))
    return paths


def wave_paths(w=110):
    rows = []
    for row, (n, y0, ww) in enumerate([(3, 0, w), (2, 18, w * 0.62)]):
        pts = []
        for i in range(int(n * 12) + 1):
            x = (w - ww) / 2 + ww * i / (n * 12)
            pts.append((x, y0 + 15 - 14 * abs(math.sin(i / 12 * math.pi))))
        rows.append((pts, row == 0))
    return rows


def boat_paths(w=110):
    hull = [(0, 30), (w * 0.12, 44), (w * 0.5, 50), (w * 0.88, 44), (w, 26)]
    deck = [(w * 0.06, 32), (w * 0.94, 30)]
    mast = [(w * 0.5, 30), (w * 0.52, -28)]
    sail = [(w * 0.52, -26), (w * 0.80, 24), (w * 0.53, 24)]
    water = [(w * 0.1, 58), (w * 0.35, 54), (w * 0.6, 58), (w * 0.9, 54)]
    return [(hull, True), (deck, False), (mast, False), (sail, False), (water, False)]


def cross_paths(h=54):
    return [([(h * 0.33, 0), (h * 0.35, h)], True),
            ([(h * 0.02, h * 0.30), (h * 0.66, h * 0.28)], True)]


def spiral_paths(r=20):
    pts = [(r + r * (t / (5 * math.pi)) * math.cos(t),
            r + r * (t / (5 * math.pi)) * math.sin(t))
           for t in np.linspace(0.3, 5 * math.pi, 70)]
    return [(pts, False)]


def heart_paths(s=17):
    pts = []
    for t in np.linspace(0, 2 * math.pi, 44):
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((s + x * s / 16, s - y * s / 16))
    return [(pts, False)]


def burst_paths(r=17):
    rng = random.Random(4)
    paths = []
    for k in range(8):
        a = k * math.pi / 4 + rng.uniform(-0.15, 0.15)
        r0 = r * rng.uniform(0.35, 0.5)
        r1 = r * rng.uniform(0.9, 1.15)
        paths.append(([(r * 1.2 + r0 * math.cos(a), r * 1.2 + r0 * math.sin(a)),
                       (r * 1.2 + r1 * math.cos(a), r * 1.2 + r1 * math.sin(a))], False))
    return paths


def arrow_layer(p0, p1, seed, bend=0.18, width=3):
    """Hand-drawn connecting arrow p0 -> p1 in FRAME coords with a gentle
    curve + open-chevron head (the house arrowhead -- never a filled
    triangle). Returns (layer, paste_xy)."""
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    cx, cy = mx - dy / L * L * bend, my + dx / L * L * bend
    curve = [(
        (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t ** 2 * p1[0],
        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t ** 2 * p1[1],
    ) for t in np.linspace(0, 1, 24)]
    tx, ty = curve[-1][0] - curve[-2][0], curve[-1][1] - curve[-2][1]
    tl = math.hypot(tx, ty) or 1.0
    tx, ty = tx / tl, ty / tl
    head = []
    for sgn in (1, -1):
        a = math.radians(152) * sgn
        hx = tx * math.cos(a) - ty * math.sin(a)
        hy = tx * math.sin(a) + ty * math.cos(a)
        head.append(([(p1[0], p1[1]), (p1[0] + hx * 16, p1[1] + hy * 16)], False))
    paths = [(curve, True)] + head
    xs = [p[0] for pts, _ in paths for p in pts]
    ys = [p[1] for pts, _ in paths for p in pts]
    x0, y0 = int(min(xs) - 18), int(min(ys) - 18)
    shifted = [([(x - x0, y - y0) for x, y in pts], dbl) for pts, dbl in paths]
    return draw_doodle(shifted, seed, width=width, amp=2.6), (x0, y0)


# ---------------------------------------------------------------------------
# highlighter swipe (ordinary marker yellow -- never rubric-red)
# ---------------------------------------------------------------------------

def highlighter_swipe(frame, rect, seed=23, color=HIGHLIGHT, ink_resist=None):
    """A hand-swiped marker band: wavering top/bottom edges (tide_mark's
    sum-of-sines trick), slight downhill angle, soft caps, faint pigment
    pooling at the trailing end. Semi-opaque (real fluorescent marker), and
    where `ink_resist` (an alpha map of lettering) is dark the swipe thins so
    the letters stay crisp."""
    x0, y0, x1, y1 = rect
    fw, fh = frame.size
    bw = x1 - x0
    xs = np.arange(fw, dtype=np.float32)
    rng = np.random.default_rng(seed)
    yy = np.arange(fh, dtype=np.float32)[:, None]

    def edge(base_y, s):
        e = np.full(fw, base_y, dtype=np.float32)
        for f, ph, a in zip((1.3, 2.9, 5.1), rng.uniform(0, 6.3, 3), (3.0, 1.6, 0.9)):
            e += a * np.sin(2 * np.pi * f * (xs - x0) / bw + ph)
        return e + (xs - x0) / bw * 5.0  # slight downhill: a wrist, not a ruler

    top = edge(y0, seed)
    bot = edge(y1, seed + 3)
    band = np.clip((yy - top[None, :]) / 2.5, 0, 1) * np.clip((bot[None, :] - yy) / 2.5, 0, 1)
    ramp_in = np.clip((xs - (x0 - 4)) / 12.0, 0, 1)
    ramp_out = np.clip(((x1 + 6) - xs) / 18.0, 0, 1)
    band *= (ramp_in * ramp_out)[None, :]
    pool = np.exp(-((xs - (x1 - 4)) ** 2) / (2 * 7.0 ** 2)) * 0.35 + 1.0  # trailing-end pooling
    band *= pool[None, :]
    band = np.clip(band, 0, 1.18)
    a = np.array(Image.fromarray((np.clip(band, 0, 1) * 255).astype("uint8")).filter(
        ImageFilter.GaussianBlur(1.1)), dtype=np.float32) / 255.0 * 0.70
    a *= 1.0 + 0.18 * (band > 1.0)  # keep the pooled cap a touch heavier post-blur
    if ink_resist is not None:
        a *= 1.0 - 0.68 * ink_resist  # lettering resists the marker -- stays crisp
    base = np.asarray(frame, dtype=np.float32)
    col = np.array(color, dtype=np.float32)
    out = base * (1 - a[..., None]) + a[..., None] * (0.25 * base + 0.75 * col[None, None, :])
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"))


def verse_card_assembled(frame):
    """Composite the REAL Scribed Ink card exactly as the assembler's settled
    state does (ox centered -> 0, oy = max(WM_TOP, ...) -> 160), and return
    (frame, card, (ox, oy))."""
    card = asm.scribed_ink_card(["Why are ye fearful,", "O ye of little faith?"], "MATTHEW 8:26")
    ox = int(W * 0.5 - card.width / 2)
    oy = max(asm.WM_TOP, int(H * 0.134 - card.height / 2))
    out = frame.convert("RGBA")
    out.paste(card, (ox, oy), card)
    return out.convert("RGB"), card, (ox, oy)


def word_rect_on_card(card, line1, word, card_xy):
    """Frame-coords rect of `word` inside line 1 of the card, computed by
    replicating scribed_ink_card's own char-width cursor math (the FAITH_BBOX
    method -- never eyeballed), tight y from the card's own alpha."""
    font = ImageFont.truetype(asm.F_KUNSTLER, 48)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))

    def cw(ch):
        return tmp.textlength(ch, font=font)

    tw = sum(cw(ch) for ch in line1)
    xs = (W - tw) / 2
    i = line1.index(word)
    x0 = xs + sum(cw(ch) for ch in line1[:i])
    x1 = x0 + sum(cw(ch) for ch in word)
    alpha = np.array(card)[:, :, 3]
    colslice = alpha[0:76, int(x0):int(x1)]  # line 1 band only
    rows = np.where(colslice.max(axis=1) > 8)[0]
    y0, y1 = int(rows.min()), int(rows.max())
    # a real swipe covers the x-height body; ascenders stick out above it --
    # bias the band top DOWN past the ascender zone (first cut sat too high)
    y0 = int(y0 + 0.42 * (y1 - y0))
    ox, oy = card_xy
    # Kunstler leans right: glyph ink sits left of the advance cursor --
    # shift the band left so the swipe owns the word, not its right shoulder
    return (int(x0) - 18 + ox, y0 - 6 + oy, int(x1) + 2 + ox, y1 + 9 + oy)


# ---------------------------------------------------------------------------
# the 7 test stills
# ---------------------------------------------------------------------------

def s01_doodles():
    f = load_frame("s04_asleep.png")
    f = paste(f, draw_doodle(boat_paths(110), 11), (150, 1712))
    f = paste(f, draw_doodle(wave_paths(110), 12), (345, 1745))
    f = paste(f, draw_doodle(sun_paths(22), 13), (520, 1690))
    f = paste(f, draw_doodle(cross_paths(54), 14, width=3), (26, 880))
    f = paste(f, draw_doodle(spiral_paths(19), 15, width=2), (700, 1795))
    f.save(HERE / "01_doodles_only.png")


def s02_reaction():
    f = load_frame("s04_asleep.png")
    note = pencil_text("why does He sleep?", 46, seed=21, tilt=-2.5)
    f = paste(f, note, (455, 42))
    f.save(HERE / "02_handwritten_reaction.png")


def s03_highlighter():
    f = load_frame("s08_verse.png")
    f, card, card_xy = verse_card_assembled(f)
    rect = word_rect_on_card(card, "Why are ye fearful,", "fearful", card_xy)
    # ink-resist map: the card's own lettering alpha, placed at frame coords
    resist = np.zeros((H, W), dtype=np.float32)
    ca = np.array(card)[:, :, 3].astype(np.float32) / 255.0
    ox, oy = card_xy
    resist[oy:oy + card.height, ox:ox + card.width] = ca[:H - oy, :W - ox]
    f = highlighter_swipe(f, rect, seed=23, ink_resist=resist)
    f.save(HERE / "03_highlighter_swipe.png")


def diary_note_layer():
    l1 = pencil_text("Sea of Galilee,", 34, seed=41, tilt=0, font_path=F_INKFREE)
    l2 = pencil_text("night.", 34, seed=42, tilt=0, font_path=F_INKFREE)
    lay = Image.new("RGBA", (max(l1.width, l2.width), l1.height + l2.height - 30), (0, 0, 0, 0))
    lay.alpha_composite(l1, (lay.width - l1.width, 0))
    lay.alpha_composite(l2, (lay.width - l2.width, l1.height - 30))
    return lay.rotate(-1.4, resample=Image.BICUBIC, expand=True)


def s04_diary():
    f = load_frame("s08_verse.png")
    d = diary_note_layer()
    f = paste(f, d, (1040 - d.width, 34))
    f.save(HERE / "04_diary_corner.png")


def s05_restrained():
    f = load_frame("s04_asleep.png")
    d = diary_note_layer()
    f = paste(f, d, (1040 - d.width, 34))
    note = pencil_text("why does He sleep?", 46, seed=21, tilt=-1.8)
    f = paste(f, note, (120, 1735))
    f.save(HERE / "05_restrained_combo.png")


def s06_fuller():
    f = load_frame("s04_asleep.png")
    d = diary_note_layer()
    f = paste(f, d, (1040 - d.width, 34))
    note = pencil_text("why does He sleep?", 46, seed=21, tilt=-1.8)
    note_xy = (120, 1748)
    f = paste(f, note, note_xy)
    # doodle-to-note arrow, kept entirely ON PAPER (first cut routed it over
    # the painted hull and graphite simply died on dark paint -- journal
    # marks live in the margins, never over the art)
    f = paste(f, draw_doodle(boat_paths(96), 11), (585, 1690))
    arr, axy = arrow_layer((580, 1760), (490, 1790), seed=61, bend=0.22)
    f = paste(f, arr, axy)
    f = paste(f, draw_doodle(sun_paths(21), 13), (285, 55))
    f = paste(f, draw_doodle(wave_paths(100), 12), (718, 1712))
    f = paste(f, draw_doodle(spiral_paths(18), 15, width=2), (955, 1800))
    q = pencil_text("?", 62, seed=71, tilt=3.0)
    f = paste(f, q, (6, 890))
    f = paste(f, draw_doodle(heart_paths(16), 16, width=3), (30, 1062))
    f.save(HERE / "06_fuller_combo.png")


def s07_landing():
    # the sacred-stillness test: ONE small, quiet, wordless mark, on clean
    # cream, far from the torn hole and the gold (first cut landed on a
    # torn-edge tan zone and vanished entirely)
    f = load_frame("s13_landing.png")
    f = paste(f, draw_doodle(cross_paths(46), 14, width=3), (140, 1500))
    f.save(HERE / "07_landing_touch.png")


if __name__ == "__main__":
    for fn in (s01_doodles, s02_reaction, s03_highlighter, s04_diary,
               s05_restrained, s06_fuller, s07_landing):
        fn()
        print("[ok]", fn.__name__)
    print("done ->", HERE)
