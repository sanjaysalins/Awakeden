#!/usr/bin/env python
"""Thread Device -- the gold thread connecting an OT type to its NT
fulfillment. Promoted here (Fable Round 10, Concept C) from
poc_living_sketchbook/day_of_atonement/_s3_thread_leaf_54_55.py, where it
was proven on spreads 54-55 (the goat-laying-on vignette -> Christ). That
script's own thread call sites now import from here instead of defining
their own copies -- this is a PROMOTION, not a rewrite; `make_thread_layer`'s
drawing logic is unchanged. `thread_opacity`/`thread_swell` are generalized
off caller-supplied timing (start/fade/swell_time) instead of that file's
own hardcoded per-spread module constants (THREAD_START/THREAD_FADE/
REF_TIME), so a second use (e.g. a reprise elsewhere in the same episode)
doesn't need to duplicate the drawing code -- only pass its own timing.

Regression contract: spread 54/55's own render, re-run after this promotion,
must produce byte-identical frames to before (same math, just relocated).

$0, deterministic PIL.
"""
from __future__ import annotations
import math
import random
from PIL import Image, ImageDraw

GOLD = (185, 146, 74)
GOLD_BRIGHT = (226, 193, 118)   # thread's luminance-swell tone


def smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def make_thread_layer(w: int, h: int, p0_frac, p1_frac, color, seed=9, n=16, bow=70, width=4) -> Image.Image:
    """Static gold-stitched-thread RGBA layer, full frame size, transparent bg."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = p0_frac[0] * w, p0_frac[1] * h
    x1, y1 = p1_frac[0] * w, p1_frac[1] * h
    rng = random.Random(seed)
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + dx * t
        y = y0 + dy * t
        off = bow * math.sin(t * math.pi) + rng.uniform(-3, 3)
        pts.append((x + nx * off, y + ny * off))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(*color, 255), width=width)
    r = width + 2
    d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=(*color, 255))
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=(*color, 255))
    return layer


def thread_opacity(t: float, start: float, fade: float) -> float:
    """0 before `start`, eases to 1 over `fade` seconds, holds at 1 after."""
    if t < start:
        return 0.0
    return smootherstep((t - start) / fade)


def thread_swell(t: float, swell_time: float, rise: float = 0.6, decay: float = 0.8) -> float:
    """One luminance swell centered on `swell_time`: rises over `rise`s,
    decays over `decay`s, 0 elsewhere -- for the moment a reference/thesis
    word actually lands."""
    lt = t - swell_time
    if lt < 0:
        return 0.0
    if lt < rise:
        return smootherstep(lt / rise)
    lt2 = lt - rise
    if lt2 < decay:
        return 1.0 - smootherstep(lt2 / decay)
    return 0.0
