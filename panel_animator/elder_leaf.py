#!/usr/bin/env python
"""Elder Leaf -- the Old Testament, physically present: when an episode cites
its OT echo, the citation arrives as an OLDER leaf tipped into the sketchbook.
A smaller sheet of visibly older stock (darker, foxed, deckle-edged) settles
onto the spread with linen-tape corners, carrying the OT verse in an elder
register of the existing Scribed Ink hand (faded iron-gall brown), reference
in the same rubric red. The gold thread (the assembler's existing device) then
runs from the leaf to the Christ-element on the page -- that part is the
assembler's job, not this engine's.

Round 5 ("the book itself", 2026-07-30). Completes the chain round 3 started:
the Concordance Loom FINDS the echo, the panel JUDGES it, the Elder Leaf CITES
it. Reverence law: older paper must never read as LESSER paper -- the leaf is
aged but IMMACULATE (foxing, never filth; deckle, never damage), taped in with
visible care. The elder leaf is the root, not the relic.

$0 deterministic: the stock is generated (seeded numpy mottling + foxing +
deckled edge -- no metered render; bank a seedream texture later ONLY if the
user judges this one insufficient by eye). Lettering reuses the proven
render_scribed_ink pattern (per-glyph wobble, the KUNSTLER punctuation fix).

Usage:
    python elder_leaf.py --demo --still spread.png --out demo.mp4 \
        --verse "He maketh the storm a calm,|so that the waves|thereof are still." \
        --ref "PSALM 107:29" [--center 0.28,0.17] [--width-frac 0.58] \
        [--settle-at 0.8] [--duration 5]

    python elder_leaf.py --selftest
"""
from __future__ import annotations
import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from raking_light import scale_crop

FPS = 30
F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"

ELDER_INK = (94, 72, 50)      # faded iron-gall brown -- the elder register
ELDER_RUBRIC = (146, 44, 36)  # rubric red, slightly sunk into old paper
STOCK_BASE = (206, 186, 148)  # older, tanner than the book's own cream


def _fbm_noise(h: int, w: int, rng: np.random.Generator, octaves=((16, 1.0), (64, 0.5), (180, 0.25))) -> np.ndarray:
    """Low-frequency mottling: sum of upscaled coarse noise fields, 0-centered."""
    acc = np.zeros((h, w), dtype=np.float32)
    for cell, amp in octaves:
        gh, gw = max(2, h // cell), max(2, w // cell)
        coarse = rng.standard_normal((gh, gw)).astype(np.float32)
        img = Image.fromarray(((coarse - coarse.min()) / (np.ptp(coarse) + 1e-6) * 255).astype(np.uint8))
        up = np.asarray(img.resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0 - 0.5
        acc += amp * up
    return acc / sum(a for _, a in octaves)


def _deckle_mask(w: int, h: int, rng_seed: int, rough_px: float = 7.0) -> Image.Image:
    """Deckled (wavy, fibrous) edge alpha for the whole leaf: summed-sine
    wobble per edge (tide-mark's law: never a straight line) + fine fray."""
    rng = random.Random(rng_seed)
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)

    def edge_offsets(n, span):
        phases = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
        freqs = [rng.uniform(2.0, 5.0) for _ in range(3)]
        amps = [rough_px * a for a in (1.0, 0.55, 0.3)]
        return [sum(a * math.sin(2 * math.pi * f * t / span + p)
                    for a, f, p in zip(amps, freqs, phases)) + rng.uniform(-1.5, 1.5)
                for t in range(n)]

    top = edge_offsets(w, w)
    bot = edge_offsets(w, w)
    lef = edge_offsets(h, h)
    rig = edge_offsets(h, h)
    inset = rough_px * 2.8  # deeper than the summed wobble amplitude can reach
    poly = []
    poly += [(x, inset + top[x]) for x in range(0, w, 3)]
    poly += [(w - inset + rig[y], y) for y in range(0, h, 3)]
    poly += [(x, h - inset + bot[x]) for x in range(w - 1, -1, -3)]
    poly += [(inset + lef[y], y) for y in range(h - 1, -1, -3)]
    d.polygon(poly, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(0.8))


def make_elder_stock(w: int, h: int, seed: int = 21) -> Image.Image:
    """Deterministic elder stock: warm tan sheet, low-freq mottling, fibrous
    grain, a few soft foxing blooms, edge-darkened, deckle-edged RGBA.
    Aged, never dirty -- foxing stays sparse and soft (reverence law)."""
    nrng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), dtype=np.float32)
    base[..., 0], base[..., 1], base[..., 2] = STOCK_BASE

    mottle = _fbm_noise(h, w, nrng)
    base *= (1.0 + 0.10 * mottle)[..., None]

    grain = nrng.standard_normal((h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 40 + 128, 0, 255).astype(np.uint8))
                        .filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0 - 0.5
    base *= (1.0 + 0.05 * grain)[..., None]

    # foxing: few, soft, rust-toned blooms -- treasured age, not neglect
    rng = random.Random(seed)
    fox = np.zeros((h, w), dtype=np.float32)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    for _ in range(max(3, (w * h) // 220000)):
        fx, fy = rng.uniform(0.08, 0.92) * w, rng.uniform(0.08, 0.92) * h
        fr = rng.uniform(0.02, 0.05) * max(w, h)
        fall = np.exp(-0.5 * (((xs - fx) ** 2 + (ys - fy) ** 2) / fr ** 2))
        fox += rng.uniform(0.35, 0.7) * fall
    fox = np.clip(fox, 0, 1) * 0.16
    rust = np.array([160, 118, 74], dtype=np.float32)
    base = base * (1 - fox[..., None]) + rust[None, None, :] * fox[..., None]

    # edge darkening (a sheet handled for centuries)
    edge = np.minimum(np.minimum(xs, w - 1 - xs) / (0.18 * w),
                       np.minimum(ys, h - 1 - ys) / (0.18 * h))
    edge = np.clip(edge, 0, 1)
    base *= (0.90 + 0.10 * edge)[..., None]

    out = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    out.putalpha(_deckle_mask(w, h, seed))
    return out


def _tape_strip(length: int, width: int, seed: int) -> Image.Image:
    """One linen-tape strip: pale translucent warm cream, ragged cut ends,
    faint fibre streaks, slightly darker edges."""
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    arr = np.zeros((width, length, 4), dtype=np.float32)
    arr[..., 0], arr[..., 1], arr[..., 2] = (229, 219, 192)
    fib = _fbm_noise(width, length, nrng, octaves=((6, 1.0), (24, 0.5)))
    for c in range(3):
        arr[..., c] *= (1.0 + 0.07 * fib)
    alpha = np.full((width, length), 150.0, dtype=np.float32)
    yy = np.mgrid[0:width, 0:length][0].astype(np.float32)
    edge_dark = np.exp(-yy / 3.0) + np.exp(-(width - 1 - yy) / 3.0)
    for c in range(3):
        arr[..., c] *= (1.0 - 0.12 * edge_dark)
    # ragged cut ends
    for end in (0, 1):
        for y in range(width):
            cut = rng.uniform(0, 6)
            if end == 0:
                alpha[y, :int(cut)] = 0
            else:
                alpha[y, length - int(cut):] = 0
    arr[..., 3] = alpha
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def compose_elder_leaf(verse_lines: list[str], ref: str, leaf_w: int,
                        seed: int = 21, font_size: int | None = None) -> Image.Image:
    """The finished leaf RGBA: elder stock + verse in the elder Scribed Ink
    register (per-glyph wobble, KUNSTLER punctuation fix -- copied from the
    proven render_scribed_ink pattern, ink recolored to faded iron-gall) +
    rubric reference + two linen-tape corners (top-left, bottom-right)."""
    if font_size is None:
        font_size = max(30, int(leaf_w * 0.072))
    font = ImageFont.truetype(F_KUNSTLER, font_size)
    PUNCT = set(".,;:'\u2019\u201c\u201d")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(font_size * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, max(18, int(leaf_w * 0.034)))

    line_h = int(font_size * 1.30)
    pad_y = int(leaf_w * 0.11)
    leaf_h = pad_y * 2 + line_h * len(verse_lines) + int(leaf_w * 0.10)
    leaf = make_elder_stock(leaf_w, leaf_h, seed)
    d = ImageDraw.Draw(leaf)
    rng = random.Random(seed + 7)

    def char_w(ch):
        return d.textlength(ch, font=font)

    # align punctuation BASELINES with the body font -- top-aligned 1.7x punct
    # glyphs land ~0.4em low (comma drifts onto the line below; found on the
    # vault POC's "Peace, be still." card, latent here since the first leaf)
    punct_dy = font.getmetrics()[0] - font_punct.getmetrics()[0]
    y = pad_y
    last_lw, last_x0 = 0, 0
    for ln in verse_lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (leaf_w - tw) / 2
        last_lw, last_x0 = tw, x
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.2, 2.2)
            jr = rng.uniform(-1.2, 1.2)
            draw_font = font_punct if ch in PUNCT else font
            glyph = Image.new("RGBA", (int(font_size * 2.4), int(font_size * 2.6)), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glyph)
            gd.text((10, 10 + (punct_dy if ch in PUNCT else 0)), ch, font=draw_font,
                    fill=(*ELDER_INK, 235),
                    stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*ELDER_INK, 235))
            glyph = glyph.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + font_size * 0.6))
            leaf.alpha_composite(glyph, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)
        y += line_h

    # emphasis underline swash beneath the LAST line, faded rubric
    swash = [(last_x0, y - int(font_size * 0.16))]
    for i in range(1, 9):
        swash.append((last_x0 + last_lw * i / 8,
                      y - int(font_size * 0.16) + rng.uniform(-2.5, 2.5)))
    d.line(swash, fill=(*ELDER_RUBRIC, 200), width=3, joint="curve")

    rb = d.textbbox((0, 0), ref, font=ref_font)
    d.text(((leaf_w - (rb[2] - rb[0])) // 2, y + int(font_size * 0.22)), ref,
           font=ref_font, fill=(*ELDER_RUBRIC, 220))

    # linen tape, two opposite corners, laid over the leaf edge at ~45 deg
    tape_len, tape_wid = int(leaf_w * 0.30), int(leaf_w * 0.075)
    for corner, (cx_, cy_), ang in (("tl", (0, 0), -45), ("br", (leaf_w, leaf_h), -45)):
        strip = _tape_strip(tape_len, tape_wid, seed + (11 if corner == "tl" else 13))
        strip = strip.rotate(ang, expand=True, resample=Image.BICUBIC)
        leaf.alpha_composite(strip, (int(cx_ - strip.width / 2), int(cy_ - strip.height / 2)))
    return leaf


def smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def apply_elder_leaf(
    frame: Image.Image,
    leaf: Image.Image,
    center_frac: tuple[float, float],
    t: float,
    settle_at: float,
    settle_dur: float = 0.5,
    angle_deg: float = -2.5,
) -> Image.Image:
    """Composite the leaf with its lay-down: before settle_at, no leaf; during
    the settle, scale 1.035->1.0 (smootherstep) with the contact shadow
    tightening; after, byte-stable. Shadow = the leaf's own silhouette,
    blurred, warm-black, offset shrinking as the sheet meets the page."""
    out = frame.convert("RGBA")
    if t < settle_at:
        return out.convert("RGB")
    p = smootherstep((t - settle_at) / settle_dur) if settle_dur > 0 else 1.0

    scale = 1.035 - 0.035 * p
    rot = leaf.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
    sw, sh = int(rot.width * scale), int(rot.height * scale)
    sc = rot.resize((sw, sh), Image.LANCZOS)

    W, H = out.size
    cx, cy = int(center_frac[0] * W), int(center_frac[1] * H)
    x0, y0 = cx - sw // 2, cy - sh // 2

    sh_blur = 18 - 12 * p
    sh_dx, sh_dy = int(10 - 6 * p), int(14 - 8 * p)
    sh_alpha = int(80 + 20 * p)
    sil = sc.split()[3].point(lambda a: min(a, sh_alpha))
    shadow = Image.new("RGBA", (sw, sh), (30, 22, 14, 0))
    shadow.putalpha(sil)
    shadow = shadow.filter(ImageFilter.GaussianBlur(sh_blur))
    out.alpha_composite(shadow, (x0 + sh_dx, y0 + sh_dy))
    out.alpha_composite(sc, (x0, y0))
    return out.convert("RGB")


def foley_cues(settle_at: float, settle_dur: float = 0.5) -> list[dict]:
    """The cue window scriptorium_foley consumes: one soft paper lay-down."""
    return [{"device": "paper_lay", "start": settle_at, "duration": settle_dur}]


# ---------------------------------------------------------------- self-test

def selftest():
    leaf = compose_elder_leaf(
        ["He maketh the storm a calm,", "so that the waves", "thereof are still."],
        "PSALM 107:29", leaf_w=640, seed=21)
    assert leaf.mode == "RGBA" and leaf.width == 640
    a = np.asarray(leaf.split()[3])
    frac = (a > 128).mean()
    assert 0.75 < frac < 0.995, f"deckle alpha coverage off: {frac:.3f}"
    # deckle inset: the outermost pixel at each mid-edge sits outside the
    # sheet (corners are exempt -- linen tape legitimately crosses them)
    assert a[0, a.shape[1] // 2] < 128 and a[-1, a.shape[1] // 3] < 128, "deckle edge missing (top/bottom)"
    assert a[a.shape[0] // 2, 0] < 128 and a[a.shape[0] // 3, -1] < 128, "deckle edge missing (left/right)"

    base = Image.new("RGB", (1080, 1920), (238, 226, 194))
    f_pre = apply_elder_leaf(base, leaf, (0.30, 0.20), t=0.5, settle_at=0.8)
    assert np.array_equal(np.asarray(f_pre), np.asarray(base)), "leaf visible before settle"
    f_a = apply_elder_leaf(base, leaf, (0.30, 0.20), t=1.6, settle_at=0.8)
    f_b = apply_elder_leaf(base, leaf, (0.30, 0.20), t=3.0, settle_at=0.8)
    assert np.array_equal(np.asarray(f_a), np.asarray(f_b)), "leaf not byte-stable after settle"
    assert not np.array_equal(np.asarray(f_a), np.asarray(base)), "leaf never landed"
    assert foley_cues(0.8) == [{"device": "paper_lay", "start": 0.8, "duration": 0.5}]
    print("[selftest] PASS -- deckled, invisible before, settled byte-stable after")


# ---------------------------------------------------------------- demo

def render_demo(still: Path, out_mp4: Path, verse_lines, ref, center, width_frac,
                settle_at, duration, seed, angle_deg):
    im = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    leaf = compose_elder_leaf(verse_lines, ref, int(1080 * width_frac), seed=seed)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n = max(1, int(duration * FPS))
    stable = None
    for i in range(n):
        t = i / FPS
        if t >= settle_at + 0.5 and stable is not None:
            frame = stable  # byte-stable hold, render once
        else:
            frame = apply_elder_leaf(im, leaf, center, t, settle_at, angle_deg=angle_deg)
            if t >= settle_at + 0.5:
                stable = frame
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")
    print(f"[foley] cues: {foley_cues(settle_at)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--still")
    ap.add_argument("--out")
    ap.add_argument("--verse", help="verse lines separated by | (hand-broken, KJV verbatim)")
    ap.add_argument("--ref", default="")
    ap.add_argument("--center", default="0.28,0.17")
    ap.add_argument("--width-frac", type=float, default=0.58, dest="width_frac")
    ap.add_argument("--settle-at", type=float, default=0.8, dest="settle_at")
    ap.add_argument("--duration", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=21)
    ap.add_argument("--angle-deg", type=float, default=-2.5, dest="angle_deg")
    a = ap.parse_args()

    if a.selftest:
        selftest()
    elif a.demo:
        if not (a.still and a.out and a.verse):
            ap.error("--demo requires --still, --out, --verse")
        center = tuple(float(v) for v in a.center.split(","))
        render_demo(Path(a.still), Path(a.out), a.verse.split("|"), a.ref, center,
                    a.width_frac, a.settle_at, a.duration, a.seed, a.angle_deg)
    else:
        ap.error("specify --demo or --selftest")
