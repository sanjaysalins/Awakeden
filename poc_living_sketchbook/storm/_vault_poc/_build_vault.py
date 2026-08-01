"""VAULT POC (pre-lock taste test) -- four devices from _IDEA_VAULT.md, $0:

  1  vault_1_word_whole.mp4   s09: the Keeper writes shakily ("we woke him.
     someone scre--") and is INTERRUPTED mid-word -- because between one frame
     and the next, "Peace, be still." is simply THERE, complete, formal
     Scribed Ink, no reveal animation of any kind. Human words take strokes;
     His word doesn't take time. The nothing IS the device.
  2  vault_2_negative_space.mp4   blank page: ink-blue night floods in from
     every edge and closes toward the center -- and a cross of untouched
     paper remains. The darkness arrives last where the light is, and never
     touches it. "The light shineth in darkness; and the darkness
     comprehended it not."
  3  vault_3_two_days.mp4   plain paper: a weary hand writes "the end." --
     then, in a later steadier hand and fresher ink, "the end." is struck
     through and "the third day." written beneath, earning the frame's only
     gold. The strike-through as gospel.
  4  vault_4_inkwell.mp4   s02: "we bailed and bailed and the" -- the ink
     starves to a dry scratch mid-word, stops; a re-dip blot; "water kept
     coming." resumes darker. Human frailty inside the act of writing.

  ..\\..\\..\\.venv\\Scripts\\python.exe _build_vault.py
"""
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
STORM = HERE.parent
sys.path.insert(0, str(STORM.parents[1] / "panel_animator"))
sys.path.insert(0, str(STORM / "_keeper_poc"))
from raking_light import scale_crop  # noqa: E402
import _build_poc as K  # noqa: E402  (entry_events, compose_at, KEEPER_INK)

FPS = 30
W, H = 1080, 1920
F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)
PAPER = (238, 226, 194)


def render(name, frame_fn, dur):
    work = HERE / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for i in range(int(dur * FPS)):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = HERE / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def smootherstep(t):
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def paper_base(seed=4, tint=PAPER):
    nrng = np.random.default_rng(seed)
    base = np.zeros((H, W, 3), np.float32)
    base[..., 0], base[..., 1], base[..., 2] = tint
    grain = np.asarray(Image.fromarray(np.clip(nrng.standard_normal((H, W)) * 40 + 128, 0, 255)
                                        .astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
                        np.float32) / 255.0 - 0.5
    base *= (1.0 + 0.05 * grain)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


def scribed_verse_layer(text, ref, size=56, seed=11, bold=False):
    """The Word's own register: formal Scribed Ink (Kunstler + punctuation
    fix + seeded wobble), ref stamped in rubric. Returns a full-width RGBA
    strip to composite wherever the verse lives."""
    font = ImageFont.truetype(F_KUNSTLER, size)
    font_punct = ImageFont.truetype(F_KUNSTLER, int(size * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    PUNCT = set(".,;:'\u2019\u201c\u201d")
    layer = Image.new("RGBA", (W, int(size * 2.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(seed)
    tw = sum(d.textlength(ch, font=font) for ch in text)
    x = (W - tw) / 2
    cx = x
    # punctuation glyphs are drawn from a 1.7x font -- align BASELINES, not
    # glyph tops, or the comma/period land ~28px low (caught on "Peace, be
    # still." rendering as "Peace be still" with the comma on the ref line)
    punct_dy = font.getmetrics()[0] - font_punct.getmetrics()[0]
    for ch in text:
        jy, jr = rng.uniform(-2.0, 2.0), rng.uniform(-1.0, 1.0)
        gf = font_punct if ch in PUNCT else font
        g = Image.new("RGBA", (int(size * 2.4), int(size * 2.6)), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.text((10, 10 + (punct_dy if ch in PUNCT else 0)), ch, font=gf, fill=(*INK, 255),
                stroke_width=1 if (bold or ch in PUNCT) else 0, stroke_fill=(*INK, 255))
        g = g.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + size * 0.6))
        layer.alpha_composite(g, (int(cx) - 10, int(10 + jy)))
        cx += d.textlength(ch, font=font)
    rb = d.textbbox((0, 0), ref, font=ref_font)
    d.text(((W - (rb[2] - rb[0])) // 2, int(size * 1.55)), ref, font=ref_font, fill=(*RUBRIC, 235))
    return layer


# ------------------------------------------------- 1 THE WORD ARRIVES WHOLE


def poc_1():
    base = scale_crop(Image.open(STORM / "stills" / "s09_rebuke.png").convert("RGB"), W, H)
    T_WORD = 3.0
    events, layers = K.entry_events(
        [("we woke him. someone screamed", 0, 0)],
        origin=(int(W * 0.08), int(H * 0.930)), size=60, energy=0.8,
        seed=71, t0=0.7, dur=3.4)
    events = [(t, i) for (t, i) in events if t < T_WORD]  # interrupted forever
    verse = scribed_verse_layer("Peace, be still.", "MARK 4:39", size=62, seed=12, bold=True)

    def frame(t):
        out = K.compose_at(base, events, layers, t).convert("RGBA")
        if t >= T_WORD:  # no reveal, no fade, no sound of arrival. simply there.
            out.alpha_composite(verse, (0, int(H * 0.006)))
        return out.convert("RGB")

    render("vault_1_word_whole", frame, 5.5)


# ------------------------------------------------- 2 NEGATIVE-SPACE LIGHT


def _cross_mask(seed=17):
    """Reserved light: a Latin cross of untouched paper, hand-wobbled edges,
    soft feather so the wash bleeds toward it but never in."""
    rng = random.Random(seed)
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    cx, beam_y = W // 2, int(H * 0.40)
    vw, vh = 96, 820
    bw, bh = 560, 96

    def wobble_rect(x0, y0, x1, y1):
        pts = []
        for (xa, ya), (xb, yb) in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                                    ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
            for i in range(12):
                t = i / 12
                pts.append((xa + (xb - xa) * t + rng.uniform(-3.5, 3.5),
                            ya + (yb - ya) * t + rng.uniform(-3.5, 3.5)))
        d.polygon(pts, fill=255)

    wobble_rect(cx - vw // 2, beam_y - int(vh * 0.28), cx + vw // 2, beam_y - int(vh * 0.28) + vh)
    wobble_rect(cx - bw // 2, beam_y - bh // 2, cx + bw // 2, beam_y + bh // 2)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255.0


def poc_2():
    base = paper_base(seed=8)
    base_a = np.asarray(base, np.float32)
    cross = _cross_mask()

    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.minimum(np.minimum(xs, W - 1 - xs) / (W / 2),
                       np.minimum(ys, H - 1 - ys) / (H / 2))  # 0 edge .. 1 center
    nrng = np.random.default_rng(9)
    rough = np.asarray(Image.fromarray((nrng.random((H // 40 + 1, W // 40 + 1)) * 255)
                                        .astype(np.uint8)).resize((W, H), Image.BICUBIC),
                        np.float32) / 255.0
    blotch = np.asarray(Image.fromarray((nrng.random((H // 90 + 1, W // 90 + 1)) * 255)
                                         .astype(np.uint8)).resize((W, H), Image.BICUBIC),
                         np.float32) / 255.0
    ink_col = np.array([56, 66, 88], np.float32)   # ink-blue night (judgment palette)

    T0, DUR = 0.6, 2.6

    def frame(t):
        p = smootherstep((t - T0) / DUR)
        front = np.clip((p * 1.15 - (dist + 0.10 * (rough - 0.5))) * 9.0, 0, 1)
        alpha = front * (0.78 + 0.18 * blotch) * (1.0 - cross)
        # feathered darker ridge at the advancing edge (wash-creep's law)
        ridge = np.clip(front * (1 - front) * 4.0, 0, 1) * (1.0 - cross)
        arr = base_a * (1 - alpha[..., None]) + ink_col[None, None, :] * alpha[..., None]
        arr *= (1.0 - 0.10 * ridge)[..., None]
        # after the flood: the reserved paper warms, barely (glow breathes only)
        if p >= 1.0:
            b = 0.05 + 0.02 * math.sin(2 * math.pi * (t - T0 - DUR) / 2.4)
            warm = np.array([255, 236, 190], np.float32)
            arr = arr * (1 - (cross * b)[..., None]) + warm[None, None, :] * (cross * b)[..., None]
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    render("vault_2_negative_space", frame, 6.0)


# ------------------------------------------------- 3 ENTRIES ACROSS DAYS


def poc_3():
    base = paper_base(seed=15, tint=(234, 222, 190))
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    ORIGIN1 = (int(W * 0.36), int(H * 0.42))
    ORIGIN2 = (int(W * 0.30), int(H * 0.50))

    old_ink = (98, 78, 56)     # the first day: iron-gall, tired
    new_ink = (52, 46, 42)     # the third day: fresh carbon, steady
    saved = K.KEEPER_INK
    K.KEEPER_INK = old_ink
    ev1, ly1 = K.entry_events([("the end.", 0, 0)], origin=ORIGIN1, size=60,
                               energy=0.35, seed=81, t0=0.7, dur=1.2)
    K.KEEPER_INK = new_ink
    ev2, ly2 = K.entry_events([("the third day.", 0, 0)], origin=ORIGIN2, size=60,
                               energy=0.06, seed=82, t0=3.4, dur=1.4)
    K.KEEPER_INK = saved

    font = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 60)
    w1 = probe.textlength("the end.", font=font)
    T_STRIKE = 2.9
    rng = random.Random(83)
    strike_pts = []
    for i in range(14):
        t = i / 13
        strike_pts.append((ORIGIN1[0] - 6 + (w1 + 12) * t,
                           ORIGIN1[1] + 34 + rng.uniform(-3, 3) + 4 * math.sin(math.pi * t)))
    T_GOLD = 5.3
    w2 = probe.textlength("the third day.", font=font)
    gold_pts = []
    for i in range(12):
        t = i / 11
        gold_pts.append((ORIGIN2[0] + w2 * t, ORIGIN2[1] + 78 + rng.uniform(-2.5, 2.5)))

    def frame(t):
        out = K.compose_at(base, ev1, ly1, t)
        out = K.compose_at(out, ev2, ly2, t)
        d = ImageDraw.Draw(out, "RGBA")
        if t >= T_STRIKE:
            p = smootherstep((t - T_STRIKE) / 0.35)
            n = max(2, int(len(strike_pts) * p))
            d.line(strike_pts[:n], fill=(*new_ink, 235), width=4, joint="curve")
        if t >= T_GOLD:
            p = smootherstep((t - T_GOLD) / 0.5)
            n = max(2, int(len(gold_pts) * p))
            d.line(gold_pts[:n], fill=(*GOLD, 255), width=5, joint="curve")
        return out

    render("vault_3_two_days", frame, 7.0)


# ------------------------------------------------- 4 THE INKWELL RUNS DRY


def poc_4():
    base = scale_crop(Image.open(STORM / "stills" / "s02_water.png").convert("RGB"), W, H)
    STARVE_N = 5   # the last N glyphs of line 1 starve
    ev1, ly1 = K.entry_events([("we bailed and bailed and the", 0, 0)],
                               origin=(int(W * 0.06), int(H * 0.008)), size=54,
                               energy=0.6, seed=91, t0=0.5, dur=1.9)
    # starve: fade + thin the dying glyphs (dry nib -- alpha falls off a cliff)
    for k, a in enumerate([200, 150, 105, 65, 38]):
        layer, x, y = ly1[-STARVE_N + k]
        ly1[-STARVE_N + k] = (layer.point(lambda v, aa=a: min(v, aa) if v else 0), x, y)

    ev2, ly2 = K.entry_events([("water kept coming.", 0, 0)],
                               origin=(int(W * 0.13), int(H * 0.044)), size=54,
                               energy=0.6, seed=92, t0=3.3, dur=1.3)
    T_BLOT = 3.0
    bx, by = int(W * 0.115), int(H * 0.049)

    def frame(t):
        out = K.compose_at(base, ev1, ly1, t)
        if t >= T_BLOT:
            p = smootherstep((t - T_BLOT) / 0.4)
            d = ImageDraw.Draw(out, "RGBA")
            r = 4 + 6 * p
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=(48, 40, 34, 205))
            d.ellipse([bx - r * 1.7, by - r * 1.7, bx + r * 1.7, by + r * 1.7],
                      outline=None, fill=(48, 40, 34, int(35 * p)))
        return K.compose_at(out, ev2, ly2, t)

    render("vault_4_inkwell", frame, 6.0)
    print("[sfx] dry-nib scratch 1.9-2.4, dip+blot at 3.0")


if __name__ == "__main__":
    poc_1()
    poc_2()
    poc_3()
    poc_4()
    print("VAULT_POC_DONE")
