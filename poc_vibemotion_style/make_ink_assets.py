#!/usr/bin/env python
"""Procedural ink-texture assets: a torn parchment caption band + a brush-stroke
arrow. Both used so overlay panels read as hand-inked comic elements, not flat
UI chrome (boxes/drop-shadows/rounded rects)."""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

INK = (42, 28, 16)
PAPER = (214, 193, 150)


def torn_band(w=1900, h=260, out="caption_band.png"):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rng = random.Random(3)

    def jitter_edge(y_base, amp, n):
        pts = []
        for i in range(n + 1):
            x = i * w / n
            y = y_base + rng.uniform(-amp, amp)
            pts.append((x, y))
        return pts

    top = jitter_edge(18, 9, 40)
    bot = jitter_edge(h - 18, 9, 40)[::-1]
    poly = top + bot
    d.polygon(poly, fill=(*PAPER, 235))
    # mottled ink stains
    for _ in range(60):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(4, 22)
        a = rng.randint(6, 22)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(90, 60, 30, a))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(out)
    print("wrote", out)


def brush_arrow(length=420, out="ink_arrow.png"):
    w, h = length + 40, 140
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cy = h / 2
    n = 60
    for i in range(n):
        t = i / n
        x = 20 + t * (length - 40)
        wobble = math.sin(t * math.pi * 3) * 2.2
        taper = (1 - t) * 0.7 + 0.3          # thick at tail, thin near head
        r = (10 * taper) + rng_jitter(i)
        d.ellipse([x - r, cy + wobble - r, x + r, cy + wobble + r], fill=(*INK, 235))
    # arrowhead (rough triangle, slightly irregular)
    hx = 20 + (length - 40)
    d.polygon([(hx - 6, cy - 2), (hx + 34, cy), (hx - 6, cy + 24)], fill=(*INK, 240))
    d.polygon([(hx - 10, cy - 20), (hx + 30, cy - 2), (hx - 10, cy + 4)], fill=(*INK, 200))
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    img.save(out)
    print("wrote", out)


def rng_jitter(i):
    random.seed(i)
    return random.uniform(-1.2, 1.2)


if __name__ == "__main__":
    torn_band()
    brush_arrow()
