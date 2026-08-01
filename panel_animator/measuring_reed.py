#!/usr/bin/env python
"""Measuring Reed -- a hand-ruled measured span draws itself across the open
paper when Scripture states an actual physical MAGNITUDE verbatim (a length,
height, or measurement -- never an invented or estimated one). The line
extends to its final length via a progressive draw-on (wobbled iron-gall
ink, matching this show's other hand-drawn devices), tick marks for each
unit arrive one by one, staggered, as the draw-front passes them, and
finally the numeral + unit label arrives in Scribed Ink once the span
completes. Brief: poc_living_sketchbook/_FABLE_ROUND4_REMOTION_SKILLS.md
sec. 3 "Measuring Reed". Skill doc: .claude/skills/measuring-reed/SKILL.md.

DISCIPLINE (load-bearing -- see the skill doc for the full rule): only draw
a magnitude the text states VERBATIM. This module does not know or check
Scripture -- the CALLER is responsible for only ever invoking it with a
verse-stated n_units, and for the >=1 reed sequence per episode governor.

$0, deterministic PIL/numpy -- the same progressive-draw machinery as
Tally and the map route (draw-front wobble = tide_mark's seeded sum-of-
sines recipe; the wobble is a pure function of arc-length position s, not
of time, so an already-drawn stretch of line never jitters between frames,
only the frontier extends). The final label reuses this show's real
SCRIBED INK lettering grammar (letter-by-letter seeded jitter, no box,
ever) -- replicated from poc_living_sketchbook/storm/_s4_assemble.py's
scribed_ink_card() rather than imported, so this stays a standalone
panel_animator module with no dependency on the Storm episode's assembler.

Usage (library):
    from measuring_reed import apply_measuring_reed
    frame = apply_measuring_reed(frame, x0=68, y0=1194, x1=1014, y1=1120,
                                  n_units=300, progress=0.6,
                                  label_text="300 cubits", ref_text="GENESIS 6:15")

Usage (demo CLI -- render a progress 0->1 test clip over one still):
    python measuring_reed.py --demo --still ark.png --out demo.mp4 --duration 5
        --x0 68 --y0 1194 --x1 1014 --y1 1120 --n-units 300
        --label "300 cubits" --ref "GENESIS 6:15"
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

INK = (35, 30, 26)        # iron-gall ink -- matches _s4_assemble.py's INK
RUBRIC = (150, 26, 22)     # rubric-red reference caps -- matches RUBRIC there

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"

# progress phase boundaries (brief: line draws first, then ticks populate as
# the front passes them, then the label fades in once progress reaches ~0.9-1.0)
LINE_DRAW_END = 0.80
LABEL_START = 0.90
LABEL_END = 1.00
TICK_POP_SPAN = 0.06       # fraction of the front's 0..1 domain a tick takes to fade in

_NICE_STEPS = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000]


def _ease(u: float) -> float:
    """Smoothstep, 0..1 -> 0..1 -- same recipe as tide_mark.py / held_breath.py."""
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _default_tick_steps(n_units: float) -> tuple[float, float]:
    """Pick a major/minor tick interval the way a real hand-ruled reed would
    be marked -- aim for ~5-7 major divisions across the span (never one
    tick per unit for a large magnitude; never so coarse the span reads
    unmarked), then a minor subdivision every 1/5th (or 1/2, if the major
    step isn't divisible by 5) of the major step. A small magnitude
    (Ezekiel's 6-cubit reed, Goliath's 6-cubit height) gets majors every
    1 unit with no minor subdivision -- there's nothing left to subdivide."""
    target_majors = 6
    raw = max(1.0, n_units / target_majors)
    major = min(_NICE_STEPS, key=lambda s: abs(s - raw))
    if major % 5 == 0:
        minor = major / 5
    elif major % 2 == 0:
        minor = major / 2
    else:
        minor = major
    return major, minor


def _path_wobble(n_samples: int, seed: int, amp_px: float) -> np.ndarray:
    """Perpendicular offset (px) as a function of arc-length fraction s in
    [0,1] along the reed's path -- a seeded sum of 3-4 sines + light
    smoothing, the same recipe as tide_mark._tide_boundary, so a "wobbled"
    hand-ruled line reads the same hand as this show's other ink devices.
    Offset is a pure function of s (not of time/progress): an already-drawn
    stretch of the line never jitters between frames, only the frontier
    extends as progress advances."""
    rng = np.random.default_rng(seed)
    s = np.linspace(0.0, 1.0, n_samples)
    n = int(rng.integers(3, 5))
    base_freqs = np.array([1.1, 2.6, 4.3, 6.1])[:n]
    freqs = base_freqs * rng.uniform(0.85, 1.15, size=n)
    phases = rng.uniform(0.0, 2 * np.pi, size=n)
    rel_amps = np.array([1.0, 0.5, 0.28, 0.15])[:n] * rng.uniform(0.8, 1.2, size=n)
    amps = rel_amps * amp_px
    y = np.zeros(n_samples)
    for f, p, a in zip(freqs, phases, amps):
        y += a * np.sin(2 * np.pi * f * s + p)
    sigma = max(2, n_samples // 100)
    radius = sigma * 3
    kx = np.arange(-radius, radius + 1)
    kernel = np.exp(-(kx ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    y = np.convolve(y, kernel, mode="same")
    return y


def _scribed_ink_label(lines: list[str], ref: "str | None", width: int,
                        seed: int = 41) -> Image.Image:
    """Hand-lettered numeral+unit card -- ported verbatim from
    poc_living_sketchbook/storm/_s4_assemble.py's scribed_ink_card()
    (SKILL.md sec.5 SCRIBED INK grammar): letter-by-letter seeded
    baseline/rotation wobble, underline swash, small rubric-red reference
    caps, NO box, ever. Kunstler's comma/period glyphs are nearly invisible
    at body size -- drawn from a 1.7x larger stroked instance of the same
    font (same fix as the source, ported not rediscovered). Replicated
    (not imported) so this stays a standalone panel_animator module -- the
    source file pulls in the whole Storm episode's sibling devices
    (wash_creep, tide_mark, damp_cockle, ...) this module has no need of.
    Only the canvas WIDTH is generalized (the source hardcodes W=1080);
    the reference-caps line is optional here (ref=None skips it)."""
    font = ImageFont.truetype(F_KUNSTLER, 48)
    PUNCT = set(".,;:'\u2019\u201c\u201d?")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(48 * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)

    def char_w(ch, f=font):
        return td.textlength(ch, font=f)

    line_h = 62
    canvas = Image.new("RGBA", (width, line_h * len(lines) + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    rng = random.Random(seed)
    y = 10
    last_lw = last_x0 = 0
    for ln in lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (width - tw) / 2
        last_lw, last_x0 = tw, x
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.5, 2.5)
            jr = rng.uniform(-1.2, 1.2)
            draw_font = font_punct if ch in PUNCT else font
            layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.text((10, 10), ch, font=draw_font, fill=(*INK, 255),
                     stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*INK, 255))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + 32))
            canvas.alpha_composite(layer, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)
        y += line_h
    if ref:
        swash = [(last_x0, y - 6)]
        for i in range(1, 9):
            swash.append((last_x0 + last_lw * i / 8, y - 6 + rng.uniform(-3, 3)))
        d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
        rw = d.textlength(ref, font=ref_font)
        d.text(((width - rw) / 2, y + 16), ref, font=ref_font, fill=(*RUBRIC, 235))
        y += 60
    else:
        y += 16
    return canvas.crop((0, 0, width, y))


def apply_measuring_reed(frame: Image.Image, x0: float, y0: float, x1: float, y1: float,
                          n_units: float, progress: float, label_text,
                          ref_text: "str | None" = None, seed: int = 11,
                          major_step: "float | None" = None,
                          minor_step: "float | None" = None,
                          tick_side: int = 1,
                          label_side: str = "above") -> Image.Image:
    """Apply the Measuring Reed to an already-composited RGB(A) frame.

    x0,y0 -> x1,y1: pixel endpoints of the span on THIS frame. Per the
    brief, the reed draws on the OPEN PAPER (a blank/background margin --
    sand, sky, floor), never smeared across the drawn illustration itself:
    dark-on-dark iron-gall ink over a dark painted subject has no contrast
    and reads as nothing (found live in this module's own test render --
    see the skill doc). Pick two points along a clear paper stretch that
    RUNS PARALLEL to the magnitude being measured (e.g. the sand just below
    a hull's keel line), not the hull edge itself.
    n_units: the verbatim count of units the text states (e.g. 300 for
    Genesis 6:15's "three hundred cubits").
    progress: 0..1, drives the whole reveal -- 0 = untouched frame,
    ~0.80 = line + every tick fully drawn, 0.90-1.00 = label fades in.
    label_text: str or list[str], the numeral+unit line(s) -- write it
    SENTENCE CASE (e.g. "300 cubits"), not ALL CAPS. Found live in this
    module's own test render: Kunstler Script's capital letterforms are
    ornate swash caps built for the occasional dropped/leading capital in
    a normal sentence, not a whole word -- "300 CUBITS" rendered nearly
    illegible while "300 cubits" (the font's plainer cursive lowercase)
    read cleanly at the same size. ref_text: optional citation caps line
    (e.g. "GENESIS 6:15", rendered in ZillaSlab not Kunstler -- unaffected
    by this); omit for no reference line.
    major_step/minor_step: override the tick spacing; default is a
    hand-ruled-reasonable auto pick (see _default_tick_steps).
    tick_side: +1 or -1, which side of the line the tick strokes drop to --
    pick whichever side stays on open paper (away from the subject).
    label_side: "above" or "below" the line -- pick whichever side has
    clear paper for the card to land on.
    """
    progress = max(0.0, min(1.0, progress))
    if progress <= 0.0:
        return frame

    W, H = frame.size
    scale = W / 1080.0
    src_mode = frame.mode
    out = frame.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    length = math.hypot(x1 - x0, y1 - y0)
    amp = max(1.5 * scale, min(6.0 * scale, length * 0.006))
    n_samples = 400
    s = np.linspace(0.0, 1.0, n_samples)
    wob = _path_wobble(n_samples, seed, amp)
    dx, dy = x1 - x0, y1 - y0
    L = max(1e-6, length)
    ux, uy = dx / L, dy / L
    perp = (-uy, ux)
    xs = x0 + s * dx + wob * perp[0]
    ys = y0 + s * dy + wob * perp[1]

    # -- the line itself: a progressive draw-on, front position eased so the
    # reveal isn't linear-mechanical (matches this show's other devices)
    front = _ease(min(1.0, progress / LINE_DRAW_END))
    line_w = max(2, round(3 * scale))
    if front > 0.0:
        idx = max(2, int(round(front * (n_samples - 1))) + 1)
        pts = list(zip(xs[:idx].tolist(), ys[:idx].tolist()))
        d.line(pts, fill=(*INK, 255), width=line_w, joint="curve")

    # -- tick marks: majors + minors, each fading in exactly as the draw-
    # front reaches its position along the span (staggered by construction,
    # never simultaneous, never individually hand-timed)
    auto_major, auto_minor = _default_tick_steps(n_units)
    m_major = major_step if major_step is not None else auto_major
    m_minor = minor_step if minor_step is not None else auto_minor

    ticks = []
    u = 0.0
    if m_minor > 0:
        while u < n_units - 1e-9:
            ticks.append(round(u, 6))
            u += m_minor
    ticks.append(round(n_units, 6))
    ticks = sorted(set(ticks))

    tick_major_len = 20 * scale
    tick_minor_len = 10 * scale
    trng = random.Random(seed * 1000 + 7)
    for u in ticks:
        p = (u / n_units) if n_units else 0.0
        is_major = u in (0, n_units) or (m_major > 0 and abs((u / m_major) - round(u / m_major)) < 1e-6)
        jr = trng.uniform(-6.0, 6.0)
        jlen = trng.uniform(0.85, 1.15)
        # ramps 0->1 over the last TICK_POP_SPAN of the front's approach to
        # p, reaching 1.0 exactly as the front passes it -- never requires
        # front to exceed 1.0, so the terminal tick (p==1.0) still pops
        tick_prog = _ease(max(0.0, min(1.0, (front - (p - TICK_POP_SPAN)) / TICK_POP_SPAN)))
        if tick_prog <= 0.0:
            continue
        px = float(np.interp(p, s, xs))
        py = float(np.interp(p, s, ys))
        base_len = (tick_major_len if is_major else tick_minor_len) * jlen * tick_prog
        rad = math.radians(jr)
        rpx = perp[0] * math.cos(rad) - perp[1] * math.sin(rad)
        rpy = perp[0] * math.sin(rad) + perp[1] * math.cos(rad)
        ex = px + tick_side * rpx * base_len
        ey = py + tick_side * rpy * base_len
        alpha = int(255 * tick_prog)
        tw_ = max(2, round((3 if is_major else 2) * scale))
        d.line([(px, py), (ex, ey)], fill=(*INK, alpha), width=tw_)

    out = Image.alpha_composite(out, overlay)

    # -- the numeral + unit label, in Scribed Ink, fading in once the span
    # has completed (brief: ~0.9-1.0)
    if progress >= LABEL_START:
        label_fade = _ease((progress - LABEL_START) / max(1e-6, LABEL_END - LABEL_START))
        if label_fade > 0.0:
            lines = [label_text] if isinstance(label_text, str) else list(label_text)
            card = _scribed_ink_label(lines, ref_text, width=W, seed=seed + 900)
            if label_fade < 1.0:
                a = card.split()[3].point(lambda v: int(v * label_fade))
                card.putalpha(a)
            cx = int((x0 + x1) / 2 - card.width / 2)
            cx = max(10, min(W - card.width - 10, cx))
            margin = int(40 * scale)
            if label_side == "below":
                top_y = max(y0, y1) + margin
            else:
                top_y = min(y0, y1) - card.height - margin
            cy = max(10, min(H - card.height - 10, int(top_y)))
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            layer.alpha_composite(card, (cx, cy))
            out = Image.alpha_composite(out, layer)

    return out if src_mode == "RGBA" else out.convert(src_mode)


# ---------------------------------------------------------------------------
# demo CLI
# ---------------------------------------------------------------------------

def scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render_demo(still: Path, out_mp4: Path, duration: float, fps: int, seed: int,
                 x0: float, y0: float, x1: float, y1: float, n_units: float,
                 label: str, ref: "str | None", major_step, minor_step, tick_side: int,
                 label_side: str):
    im = Image.open(still).convert("RGB")
    im = scale_crop(im, 1080, 1920)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    # hold ~0.4s on the bare still, draw+label across the remaining duration,
    # then hold ~0.6s on the finished reed -- so a scrub of the clip shows a
    # clean before/during/after, not the reveal eating the whole runway
    n_frames = int(round(duration * fps))
    pre_hold = int(0.4 * fps)
    post_hold = int(0.6 * fps)
    reveal_frames = max(1, n_frames - pre_hold - post_hold)
    for i in range(n_frames):
        if i < pre_hold:
            progress = 0.0
        elif i >= pre_hold + reveal_frames:
            progress = 1.0
        else:
            progress = (i - pre_hold) / (reveal_frames - 1) if reveal_frames > 1 else 1.0
        frame = apply_measuring_reed(im, x0, y0, x1, y1, n_units, progress, label,
                                      ref_text=ref, seed=seed, major_step=major_step,
                                      minor_step=minor_step, tick_side=tick_side,
                                      label_side=label_side)
        frame.convert("RGB").save(work / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
        check=True, capture_output=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a progress 0->1 demo clip over one still")
    ap.add_argument("--still", help="source still (any resolution, scaled/cropped to 1080x1920)")
    ap.add_argument("--out", help="output mp4")
    ap.add_argument("--duration", type=float, default=5.0, help="demo clip length, seconds")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--seed", type=int, default=11, help="wobble/jitter seed")
    ap.add_argument("--x0", type=float, required=False)
    ap.add_argument("--y0", type=float, required=False)
    ap.add_argument("--x1", type=float, required=False)
    ap.add_argument("--y1", type=float, required=False)
    ap.add_argument("--n-units", type=float, default=300.0)
    ap.add_argument("--label", default="300 cubits")
    ap.add_argument("--ref", default=None)
    ap.add_argument("--major-step", type=float, default=None)
    ap.add_argument("--minor-step", type=float, default=None)
    ap.add_argument("--tick-side", type=int, default=1, choices=[-1, 1])
    ap.add_argument("--label-side", default="above", choices=["above", "below"])
    a = ap.parse_args()
    if a.demo:
        if not a.still or not a.out or None in (a.x0, a.y0, a.x1, a.y1):
            ap.error("--demo requires --still --out --x0 --y0 --x1 --y1")
        render_demo(Path(a.still), Path(a.out), a.duration, a.fps, a.seed,
                    a.x0, a.y0, a.x1, a.y1, a.n_units, a.label, a.ref,
                    a.major_step, a.minor_step, a.tick_side, a.label_side)
    else:
        ap.error("only --demo is implemented from the CLI -- import apply_measuring_reed for pipeline use")
