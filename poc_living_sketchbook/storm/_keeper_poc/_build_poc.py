"""KEEPER POC (pre-lock taste test, round 6 candidate) -- the sketchbook gets
a PERSON. Four clips on real Storm spreads, all $0 deterministic:

  A  keeper_A_panic_entry.mp4   s01: a two-line journal entry in the Keeper's
     Hand at storm energy -- jagged, rushed, baseline heaving; the word search
     (storm / wind struck through, "fear." left standing); the final dash
     SKIDS off as a wave hits. Handwriting as acting.
  B  keeper_B_calm_line.mp4     s10: one dead-calm steady line after the
     rebuke -- same hand, same ink, zero shake. The calm you can READ.
  C  keeper_C_lamp_studies.mp4  s04: two quick pencil margin STUDIES of the
     lamp (derived from the spread's own art -- the keeper drawing what they
     can't stop looking at), leader line up to the lamp, tiny caption.
  D  keeper_D_field_header.mp4  s01: the episode as an ENTRY -- "Galilee --
     evening. crossing over." ("when the even was come", Mark 4:35 -- no
     invented dates, honesty rule.)

The Keeper's words here are PLACEHOLDER VOICE for taste only -- panel review
before anything ships (human voice, questions/observations, never doctrine
claims, never competing with the KJV's formal register).

  ..\\..\\..\\.venv\\Scripts\\python.exe _build_poc.py
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
from raking_light import scale_crop  # noqa: E402

FPS = 30
W, H = 1080, 1920
F_KEEPER = "C:/Windows/Fonts/Inkfree.ttf"   # quick pencil hand -- NOT Kunstler (the Word's register)
KEEPER_INK = (72, 64, 54)                   # graphite-iron, a working pencil-pen
BOLD = 1                                     # standing art direction (user, 2026-07-30):
                                             # keeper text BIGGER AND BOLDER -- extra stroke width

# ---------------------------------------------------------------- the hand


def _energy_params(e: float) -> dict:
    """ONE mapping from story energy (0 calm .. 1 panic) to how the hand
    behaves. This is the whole device: the same hand, differently afraid."""
    return dict(
        jit_y=0.6 + 5.0 * e,          # per-glyph baseline jitter, px
        jit_rot=0.8 + 4.5 * e,        # per-glyph rotation, deg
        drift_amp=2.0 + 15.0 * e,     # slow baseline heave across the line, px
        rot_bias=-2.2 * e,            # rushed forward lean
        gap_sigma=0.15 + 0.85 * e,    # reveal-burstiness (lognormal sigma)
        pressure=1 if e > 0.55 else 0,  # stroke width bump -- pressing too hard
    )


def keeper_line(text: str, size: int, energy: float, seed: int):
    """Layout one line of the Keeper's Hand. `~~word~~` marks a struck word.
    Returns (glyphs, strikes, width):
      glyphs  [(layer, dx, dy)]              in draw order
      strikes [(after_glyph_idx, x0, x1, y)] wobbly strike segments
    Coordinates are relative to the line's left/baseline-top origin."""
    p = _energy_params(energy)
    rng = random.Random(seed)
    font = ImageFont.truetype(F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    tokens = []  # (word, struck)
    for raw in text.split():
        if raw.startswith("~~") and raw.endswith("~~") and len(raw) > 4:
            tokens.append((raw[2:-2], True))
        else:
            tokens.append((raw, False))

    glyphs, strikes = [], []
    x = 0.0
    drift_phase = rng.uniform(0, 2 * math.pi)
    space_w = probe.textlength(" ", font=font)
    total_w = sum(probe.textlength(w, font=font) for w, _ in tokens) \
        + space_w * (len(tokens) - 1)

    for word, struck in tokens:
        wx0 = x
        for ch in word:
            cw = probe.textlength(ch, font=font)
            frac = x / max(1.0, total_w)
            drift = p["drift_amp"] * math.sin(2 * math.pi * 1.3 * frac + drift_phase)
            jy = drift + rng.uniform(-p["jit_y"], p["jit_y"])
            jr = p["rot_bias"] + rng.uniform(-p["jit_rot"], p["jit_rot"])
            layer = Image.new("RGBA", (int(size * 2.2), int(size * 2.4)), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            d.text((12, 12), ch, font=font, fill=(*KEEPER_INK, 225),
                   stroke_width=p["pressure"] + BOLD, stroke_fill=(*KEEPER_INK, 225))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(12, 12 + size * 0.55))
            glyphs.append((layer, int(x) - 12, int(jy) - 12))
            x += cw
        if struck:
            ymid = size * 0.55 + p["drift_amp"] * math.sin(
                2 * math.pi * 1.3 * (wx0 / max(1.0, total_w)) + drift_phase)
            strikes.append((len(glyphs) - 1, wx0 - 2, x + 2, ymid))
        x += space_w
    return glyphs, strikes, x - space_w


def strike_layer(x0: float, x1: float, y: float, seed: int, width: int = 3):
    """A wobbly hand strike across [x0,x1] at height y (line-local coords)."""
    rng = random.Random(seed)
    pad = 8
    lw = int(x1 - x0) + 2 * pad
    layer = Image.new("RGBA", (lw, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    n = max(6, lw // 14)
    for i in range(n):
        t = i / (n - 1)
        pts.append((pad + t * (x1 - x0),
                    20 + rng.uniform(-2.5, 2.5) + 3.0 * math.sin(math.pi * t)))
    d.line(pts, fill=(*KEEPER_INK, 235), width=width, joint="curve")
    return layer, int(x0) - pad, int(y) - 20


def skid_layer(size: int, seed: int):
    """The interrupted stroke: ink skidding away as something hits the desk --
    an accelerating, thinning tail."""
    rng = random.Random(seed)
    layer = Image.new("RGBA", (240, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = 10.0, 30.0
    vx, vy = 6.0, 1.5
    pts = [(x, y)]
    for i in range(16):
        vx *= 1.13
        vy += rng.uniform(0.4, 1.3)
        x += vx
        y += vy + rng.uniform(-1.5, 1.5)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        wdt = max(1, int(4 * (1 - i / len(pts))))
        d.line([pts[i], pts[i + 1]], fill=(*KEEPER_INK, 210), width=wdt)
    return layer


def entry_events(lines, origin, size, energy, seed, t0, dur, skid=False):
    """Timing: one event per glyph/strike (+ optional final skid), bursty at
    high energy, even when calm. lines = [(text, dx, dy)] offsets from origin.
    Returns (events, layers): events [(t, idx)] into layers [(layer, X, Y)]."""
    rng = random.Random(seed + 99)
    p = _energy_params(energy)
    layers, order = [], []
    ox, oy = origin
    for li, (text, dx, dy) in enumerate(lines):
        glyphs, strikes, _w = keeper_line(text, size, energy, seed + li)
        smap = {}
        for si, (after, x0, x1, y) in enumerate(strikes):
            smap.setdefault(after, []).append((x0, x1, y, si))
        for gi, (layer, gx, gy) in enumerate(glyphs):
            layers.append((layer, ox + dx + gx, oy + dy + gy))
            order.append(len(layers) - 1)
            for (x0, x1, y, si) in smap.get(gi, []):
                sl, sx, sy = strike_layer(x0, x1, y, seed + 31 * li + si)
                layers.append((sl, ox + dx + sx, oy + dy + sy))
                order.append(len(layers) - 1)
    if skid:
        last_layer, lx, ly = layers[-1]
        sk = skid_layer(size, seed + 7)
        layers.append((sk, lx + last_layer.width - 20, ly + int(size * 0.35)))
        order.append(len(layers) - 1)

    gaps = [rng.lognormvariate(0, p["gap_sigma"]) for _ in order]
    total = sum(gaps)
    events, t = [], t0
    for idx, g in zip(order, gaps):
        events.append((t, idx))
        t += dur * g / total
    return events, layers


def compose_at(base: Image.Image, events, layers, t: float) -> Image.Image:
    out = base.convert("RGBA")
    for et, idx in events:
        if t >= et:
            layer, x, y = layers[idx]
            out.alpha_composite(layer, (x, y))
    return out.convert("RGB")


# ---------------------------------------------------------------- studies


def pencil_study(src: Image.Image, out_w: int, seed: int, contrast: float = 1.0):
    """A quick graphite STUDY derived from the spread's own art: gray ->
    invert-blur-dodge (classic pencil conversion) -> soft irregular border.
    Slightly different params per attempt so two studies read as two tries."""
    rng = random.Random(seed)
    im = src.convert("L")
    s = out_w / im.width
    im = im.resize((out_w, int(im.height * s)), Image.LANCZOS)
    g = np.asarray(im, dtype=np.float32)
    inv = 255.0 - g
    blur = np.asarray(Image.fromarray(inv.astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(6 + 4 * rng.random())), dtype=np.float32)
    dodge = np.clip(g * 255.0 / np.clip(255.0 - blur, 12, 255), 0, 255)
    pencil = 255.0 - np.clip((255.0 - dodge) * (1.5 * contrast), 0, 255)  # keep only strong strokes

    h, w = pencil.shape
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    r = np.maximum(np.abs(xs - cx) / (w * 0.52), np.abs(ys - cy) / (h * 0.52))
    edge = np.clip((1.05 - r) * 6.0, 0, 1)  # soft irregular-ish vignette border
    noise = np.asarray(Image.fromarray(
        (np.random.default_rng(seed).random((h // 8 + 1, w // 8 + 1)) * 255).astype(np.uint8)
    ).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0
    edge = np.clip(edge - 0.35 * noise * (r > 0.7), 0, 1)

    alpha = (1.0 - pencil / 255.0) * edge  # ink where strokes are, transparent elsewhere
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = (66, 60, 54)
    rgba[..., 3] = np.clip(alpha * 235, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA").rotate(rng.uniform(-4, 4), expand=True,
                                                 resample=Image.BICUBIC)


def sweep_reveal(layer: Image.Image, frac: float, angle_deg: float = 38.0):
    """Reveal a study along a diagonal front -- quick hatching, not a fade."""
    if frac >= 1.0:
        return layer
    w, h = layer.size
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    proj = xs * math.cos(math.radians(angle_deg)) + ys * math.sin(math.radians(angle_deg))
    pr = (proj - proj.min()) / max(1e-6, proj.max() - proj.min())
    m = np.clip((frac - pr) * 12.0, 0, 1)
    a = np.asarray(layer.split()[3], dtype=np.float32) * m
    out = layer.copy()
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    return out


def leader_layer(p0, p1, seed: int):
    """Wobbly leader line from a study toward the detail it studies."""
    rng = random.Random(seed)
    x0, y0 = p0
    x1, y1 = p1
    pad = 12
    lw, lh = abs(x1 - x0) + 2 * pad, abs(y1 - y0) + 2 * pad
    layer = Image.new("RGBA", (max(lw, 4), max(lh, 4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = min(x0, x1), min(y0, y1)
    n = 14
    pts = []
    for i in range(n):
        t = i / (n - 1)
        px = x0 + (x1 - x0) * t
        py = y0 + (y1 - y0) * t + 10 * math.sin(math.pi * t) + rng.uniform(-1.5, 1.5)
        pts.append((px - ox + pad, py - oy + pad))
    d.line(pts, fill=(*KEEPER_INK, 200), width=2, joint="curve")
    return layer, ox - pad, oy - pad, pts


# ---------------------------------------------------------------- render


def render(name, frame_fn, dur):
    work = HERE / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    n = int(dur * FPS)
    last_t_done = None
    cache = None
    for i in range(n):
        t = i / FPS
        frame_fn(t).save(work / f"f{i:05d}.png")
    out = HERE / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def poc_A():
    base = scale_crop(Image.open(STORM / "stills" / "s01_waves.png").convert("RGB"), W, H)
    events, layers = entry_events(
        [("~~storm~~ ~~wind~~ fear.", 0, 0),
         ("water at our knees", 40, 100)],
        origin=(int(W * 0.36), int(H * 0.878)), size=64, energy=0.85,
        seed=41, t0=0.6, dur=2.6, skid=True)
    render("keeper_A_panic_entry", lambda t: compose_at(base, events, layers, t), 5.0)


def poc_B():
    base = scale_crop(Image.open(STORM / "stills" / "s10_calm.png").convert("RGB"), W, H)
    events, layers = entry_events(
        [("not a breath of wind. not one.", 0, 0)],
        origin=(int(W * 0.09), int(H * 0.050)), size=64, energy=0.08,
        seed=42, t0=0.8, dur=2.4)
    render("keeper_B_calm_line", lambda t: compose_at(base, events, layers, t), 5.0)


def poc_C():
    src = Image.open(STORM / "stills" / "s04_asleep.png").convert("RGB")
    base = scale_crop(src, W, H)
    # the lamp on s04 sits ~ (0.30, 0.50); crop it from the SCALED plate so
    # study + leader-line coordinates share one space
    lamp_box = (int(W * 0.185), int(H * 0.435), int(W * 0.415), int(H * 0.565))
    lamp = base.crop(lamp_box)
    st1 = pencil_study(lamp, 240, seed=7, contrast=1.9)
    st2 = pencil_study(lamp, 210, seed=8, contrast=2.3)
    s1_pos = (int(W * 0.10), int(H * 0.878))
    s2_pos = (int(W * 0.34), int(H * 0.892))
    lead, lx, ly, _ = leader_layer(
        (s2_pos[0] + st2.width // 2, s2_pos[1] + 6),
        (int(W * 0.315), int(H * 0.56)), seed=9)
    cap_events, cap_layers = entry_events(
        [("still burning.", 0, 0)],
        origin=(int(W * 0.55), int(H * 0.908)), size=56, energy=0.25,
        seed=43, t0=3.1, dur=0.9)

    def frame(t):
        out = base.convert("RGBA")
        f1 = np.clip((t - 0.5) / 0.7, 0, 1)
        f2 = np.clip((t - 1.6) / 0.7, 0, 1)
        if f1 > 0:
            out.alpha_composite(sweep_reveal(st1, float(f1)), s1_pos)
        if f2 > 0:
            out.alpha_composite(sweep_reveal(st2, float(f2)), s2_pos)
        if t >= 2.6:
            fl = np.clip((t - 2.6) / 0.4, 0, 1)
            l = lead.copy()
            if fl < 1.0:
                a = np.asarray(l.split()[3], dtype=np.float32)
                h = a.shape[0]
                cut = int(h * (1 - fl))
                a[:cut, :] = 0  # draws upward toward the lamp
                l.putalpha(Image.fromarray(a.astype(np.uint8)))
            out.alpha_composite(l, (lx, ly))
        return compose_at(out.convert("RGB"), cap_events, cap_layers, t)

    render("keeper_C_lamp_studies", frame, 5.0)


def poc_D():
    base = scale_crop(Image.open(STORM / "stills" / "s01_waves.png").convert("RGB"), W, H)
    events, layers = entry_events(
        [("Galilee. evening. crossing over.", 0, 0)],
        origin=(int(W * 0.15), int(H * 0.014)), size=60, energy=0.18,
        seed=44, t0=0.6, dur=1.8)
    render("keeper_D_field_header", lambda t: compose_at(base, events, layers, t), 4.0)


if __name__ == "__main__":
    poc_A()
    poc_B()
    poc_C()
    poc_D()
    print("KEEPER_POC_DONE")
