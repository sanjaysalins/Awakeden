#!/usr/bin/env python
"""Hand-inked walking-caravan marker (deterministic, $0).

Draws a small ink-silhouette caravan — lead camel + rider, two walking
followers — with a walk cycle driven by DISTANCE travelled (so the legs only
move while the marker is actually advancing, and freeze on a dwell). A soft
cream halo keeps it legible over dark map hatching. Faces the travel direction.

draw_caravan(layer, x, y, facing, phase, scale) where (x, y) is the FRONT
ground point (the camel's leading foot) and `phase` is 2*pi * distance/stride.
"""
from __future__ import annotations
import math
from PIL import Image, ImageDraw, ImageFilter

INK = (48, 32, 20)
CREAM = (243, 231, 205)


def _leg(d, hip, foot, w, col):
    d.line([hip, foot], fill=col, width=w)


def _figure(d, bx, by, facing, phase, s, col, staff=False):
    """A small walking robed figure. (bx,by)=feet midpoint."""
    swing = math.sin(phase) * 5 * s
    bob = abs(math.sin(phase)) * 1.6 * s
    by -= bob
    hip = (bx, by - 15 * s)
    # legs
    _leg(d, hip, (bx - swing, by), max(1, int(3 * s)), col)
    _leg(d, hip, (bx + swing, by), max(1, int(3 * s)), col)
    # robe body (trapezoid)
    d.polygon([(bx - 6 * s, by - 32 * s), (bx + 6 * s, by - 32 * s),
               (bx + 8 * s, by - 12 * s), (bx - 8 * s, by - 12 * s)], fill=col)
    # head
    d.ellipse([bx - 5 * s, by - 44 * s, bx + 5 * s, by - 34 * s], fill=col)
    if staff:
        top = (bx + facing * 9 * s, by - 52 * s)
        bot = (bx + facing * 12 * s, by - 1 * s)
        d.line([top, bot], fill=col, width=max(1, int(2 * s)))


def _camel(d, fx, fy, facing, phase, s, col):
    """Lead camel with a rider. (fx,fy)=front leading foot ground point."""
    f = facing
    swing = math.sin(phase) * 6 * s
    swing2 = math.sin(phase + math.pi) * 6 * s
    bob = abs(math.sin(phase * 2)) * 1.3 * s
    g = fy - bob
    cx = fx - f * 18 * s              # body centre behind the front foot
    belly = g - 18 * s
    lw = max(2, int(2.6 * s))
    front_x = cx + f * 13 * s
    rear_x = cx - f * 15 * s
    # legs first, so the barrel body covers their tops (front + rear pairs, gait)
    _leg(d, (front_x, belly), (front_x + swing, fy), lw, col)
    _leg(d, (front_x, belly), (front_x - swing * 0.6, fy), lw, col)
    _leg(d, (rear_x, belly), (rear_x + swing2, fy), lw, col)
    _leg(d, (rear_x, belly), (rear_x - swing2 * 0.6, fy), lw, col)
    # barrel body
    d.ellipse([cx - 24 * s, belly - 14 * s, cx + 20 * s, belly + 4 * s], fill=col)
    # single rounded hump
    d.ellipse([cx - 9 * s, belly - 26 * s, cx + 9 * s, belly - 4 * s], fill=col)
    # neck: tapered polygon rising up-forward from the shoulder
    d.polygon([(cx + f * 12 * s, belly - 8 * s), (cx + f * 19 * s, belly - 5 * s),
               (cx + f * 27 * s, belly - 28 * s), (cx + f * 23 * s, belly - 31 * s)], fill=col)
    # head + snout + ear at the top of the neck
    hx, hy = cx + f * 25 * s, belly - 31 * s
    d.ellipse([hx - 4 * s, hy - 4 * s, hx + 4 * s, hy + 4 * s], fill=col)
    d.polygon([(hx + f * 2 * s, hy - 2 * s), (hx + f * 11 * s, hy + 2 * s),
               (hx + f * 2 * s, hy + 5 * s)], fill=col)                      # snout
    d.polygon([(hx - f * 1 * s, hy - 3 * s), (hx - f * 2 * s, hy - 9 * s),
               (hx + f * 2 * s, hy - 3 * s)], fill=col)                      # ear
    # tail
    d.line([(cx - f * 22 * s, belly - 10 * s), (cx - f * 27 * s, belly + 6 * s)],
           fill=col, width=max(1, int(2 * s)))
    # rider seated just behind the hump
    rx, ry = cx - f * 3 * s, belly - 22 * s
    d.polygon([(rx - 4 * s, ry), (rx + 4 * s, ry),
               (rx + 3 * s, ry - 14 * s), (rx - 3 * s, ry - 14 * s)], fill=col)
    d.ellipse([rx - 4 * s, ry - 24 * s, rx + 4 * s, ry - 16 * s], fill=col)


def draw_caravan(layer, x, y, facing=1, phase=0.0, scale=1.0):
    """Composite a walking caravan onto RGBA `layer` at front-foot (x, y)."""
    s = scale
    f = 1 if facing >= 0 else -1
    # draw silhouette on its own layer so we can halo it
    sil = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    _camel(d, x, y, f, phase, s, (*INK, 255))
    # two followers trailing behind the camel, staggered
    _figure(d, x - f * 40 * s, y + 1 * s, f, phase + 1.1, 0.6 * s, (*INK, 255), staff=True)
    _figure(d, x - f * 55 * s, y + 2 * s, f, phase + 2.3, 0.55 * s, (*INK, 255))
    _halo_and_composite(layer, sil)


def draw_boat(layer, x, y, facing=1, phase=0.0, scale=1.0):
    """Composite a small ink fishing-boat marker onto RGBA `layer`; (x, y) is the
    waterline point at the boat's centre. A gentle bob (driven by the same
    distance-cadenced `phase` the caravan's walk cycle uses) stands in for a
    walk cycle — there are no legs to animate crossing open water. For a sea
    crossing (mapengine route.json config `"marker": "boat"`), used instead of
    draw_caravan so the marker doesn't read as a camel walking on the lake."""
    s, f = scale, (1 if facing >= 0 else -1)
    bob = math.sin(phase) * 3 * s
    y = y + bob
    sil = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sil)
    col = (*INK, 255)
    # hull: a shallow ink crescent, bow toward the travel direction
    d.polygon([(x - f * 34 * s, y), (x - f * 20 * s, y + 10 * s), (x + f * 20 * s, y + 10 * s),
               (x + f * 34 * s, y), (x + f * 20 * s, y - 4 * s), (x - f * 20 * s, y - 4 * s)], fill=col)
    # mast + single billowed sail
    d.line([(x, y - 4 * s), (x, y - 46 * s)], fill=col, width=max(1, int(2.4 * s)))
    d.polygon([(x, y - 44 * s), (x + f * 24 * s, y - 30 * s), (x, y - 12 * s)], fill=col)
    # two small seated figures amidships
    for dx in (-10, 8):
        fx = x + dx * s
        d.ellipse([fx - 4 * s, y - 20 * s, fx + 4 * s, y - 12 * s], fill=col)
        d.polygon([(fx - 5 * s, y - 12 * s), (fx + 5 * s, y - 12 * s),
                   (fx + 3 * s, y - 2 * s), (fx - 3 * s, y - 2 * s)], fill=col)
    _halo_and_composite(layer, sil)


def _halo_and_composite(layer, sil):
    """Soft cream halo for legibility over dark hatching, then composite the
    silhouette on top. Shared by draw_caravan and draw_boat."""
    halo = sil.filter(ImageFilter.MaxFilter(5))
    halo = halo.point(lambda a: 255 if a > 8 else 0).convert("L")
    halo_rgba = Image.new("RGBA", layer.size, (*CREAM, 0))
    halo_rgba.putalpha(Image.eval(halo, lambda a: int(a * 0.85)))
    halo_rgba = halo_rgba.filter(ImageFilter.GaussianBlur(2))
    layer.alpha_composite(halo_rgba)
    layer.alpha_composite(sil)
