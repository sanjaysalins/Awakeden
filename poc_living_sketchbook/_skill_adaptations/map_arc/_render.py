"""POC: adapt ArkAIology's /vox-map "ARC + counter" move (a curved arc between
two points with a distance/count readout) into our living-sketchbook hand-
drawn cartography style. Composited over the Jericho siege-map still, which
already carries a dashed circular march-path -- this adds a SEPARATE small
measurement note (curved dashed arc + a hand-lettered "13 LAPS" readout) in
open paper space, pointing at that existing path, without overlapping it.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_skill_adaptations/map_arc/_render.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
JERICHO = HERE.parents[1] / "jericho"
OUT = HERE

W, H = 1080, 1920
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"


def base_canvas(still_name):
    im = Image.open(JERICHO / "stills" / f"{still_name}.png").convert("RGB")
    s = max(W / im.width, H / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))


def bezier(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def bezier_tangent(p0, p1, p2, t):
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    n = math.hypot(dx, dy) or 1.0
    return dx / n, dy / n


def draw_dashed_arc(draw, p0, ctrl, p1, rng, color=INK, width=4):
    """Hand-drawn dashed arc matching j03_laps.png's route-line vocabulary:
    short irregular ink strokes with a small per-dash perpendicular wobble,
    following a smooth curve -- no colour wash (this is an annotation, not
    the walked route itself, so it stays ink-only per palette theology)."""
    samples = [bezier(p0, ctrl, p1, t / 800) for t in range(801)]
    # cumulative arc length per sample
    cum = [0.0]
    for i in range(1, len(samples)):
        ax, ay = samples[i - 1]
        bx, by = samples[i]
        cum.append(cum[-1] + math.hypot(bx - ax, by - ay))
    total = cum[-1]

    def point_at(dist):
        # binary search would be overkill for a POC; linear scan is fine (801 samples)
        for i in range(1, len(cum)):
            if cum[i] >= dist:
                t0, t1 = cum[i - 1], cum[i]
                frac = 0 if t1 == t0 else (dist - t0) / (t1 - t0)
                ax, ay = samples[i - 1]
                bx, by = samples[i]
                return ax + (bx - ax) * frac, ay + (by - ay) * frac
        return samples[-1]

    d = 0.0
    while d < total:
        dash_len = rng.uniform(13, 21)
        gap_len = rng.uniform(9, 15)
        d_end = min(d + dash_len, total)
        a = point_at(d)
        b = point_at(d_end)
        # small hand-wobble perpendicular to the local tangent, same jitter
        # magnitude as the existing dashed path on this still
        t_local = d / total
        tx, ty = bezier_tangent(p0, ctrl, p1, t_local)
        nx, ny = -ty, tx
        wob = rng.uniform(-1.6, 1.6)
        a = (a[0] + nx * wob, a[1] + ny * wob)
        b = (b[0] + nx * wob, b[1] + ny * wob)
        draw.line([a, b], fill=color, width=width, joint="curve")
        d = d_end + gap_len


def draw_hand_arrowhead(draw, tip, angle, rng, size=24, color=INK, width=5):
    """Open hand-drawn chevron (two brush strokes meeting at the tip) --
    matching a close-up of the still's OWN arrowheads, which are two quick
    asymmetric pen strokes, not a filled CAD triangle."""
    back = angle + math.pi
    a1 = back - math.radians(22 + rng.uniform(-4, 4))
    a2 = back + math.radians(34 + rng.uniform(-4, 4))
    len1 = size * rng.uniform(0.95, 1.1)
    len2 = size * rng.uniform(0.55, 0.7)
    p1 = (tip[0] + math.cos(a1) * len1, tip[1] + math.sin(a1) * len1)
    p2 = (tip[0] + math.cos(a2) * len2, tip[1] + math.sin(a2) * len2)
    draw.line([p1, tip], fill=color, width=width, joint="curve")
    draw.line([tip, p2], fill=color, width=width, joint="curve")
    for pt in (p1, p2, tip):
        r = width / 2
        draw.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill=color)


def draw_end_tick(draw, point, angle, rng, length=15, color=INK, width=3):
    """A small perpendicular baseline tick -- the surveyor's 'far end' mark
    that closes off the measured span (the arrowhead marks the near end)."""
    perp = angle + math.pi / 2
    jig = rng.uniform(-1.5, 1.5)
    a = (point[0] + math.cos(perp) * (length / 2 + jig), point[1] + math.sin(perp) * (length / 2 + jig))
    b = (point[0] - math.cos(perp) * (length / 2 - jig), point[1] - math.sin(perp) * (length / 2 - jig))
    draw.line([a, b], fill=color, width=width)


def hand_lettered(canvas, text, center_xy, font, color, rng, size_hint=32):
    """Small hand-inked readout: per-glyph baseline/rotation wobble, no box
    -- the same 'written directly on the page' grammar as the Scribed Ink
    verse treatment, just at marginal-note scale."""
    d = ImageDraw.Draw(canvas)
    tw = sum(d.textlength(ch, font=font) for ch in text)
    x = center_xy[0] - tw / 2
    y = center_xy[1] - size_hint / 2
    cx = x
    for ch in text:
        jy = rng.uniform(-1.6, 1.6)
        jr = rng.uniform(-2.0, 2.0)
        cw = d.textlength(ch, font=font)
        layer = Image.new("RGBA", (int(cw) + 26, size_hint + 26), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((13, 13), ch, font=font, fill=(*color, 255))
        layer = layer.rotate(jr, resample=Image.BICUBIC, center=(13, 13 + size_hint // 2))
        canvas.alpha_composite(layer, (int(cx) - 13, int(y + jy) - 13))
        cx += cw


def main():
    canvas = base_canvas("j03_laps").convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    rng = random.Random(42)

    # Open paper zone confirmed by probe crop: canvas x 780-1010, y 180-520 --
    # clear of the city/wall art, clear of the existing dashed path's top
    # arrowhead (~x760,y595), clear of the watermark zone (x40-240/y70-160)
    # and the gold-leaf edge (only appears below y~1200 on the right border).
    p_near = (812, 505)   # near end -- arrowhead points down-left at the existing route
    p_ctrl = (1000, 455)  # bow the curve outward, away from the city
    p_far = (975, 285)    # far end -- baseline tick closes the span

    draw_dashed_arc(draw, p_near, p_ctrl, p_far, rng, color=INK, width=5)

    tangent_near = bezier_tangent(p_near, p_ctrl, p_far, 0.0)
    angle_near = math.atan2(tangent_near[1], tangent_near[0])
    draw_hand_arrowhead(draw, p_near, angle_near, rng, size=22)

    tangent_far = bezier_tangent(p_near, p_ctrl, p_far, 1.0)
    angle_far = math.atan2(tangent_far[1], tangent_far[0])
    draw_end_tick(draw, p_far, angle_far, rng)

    # readout at the arc's midpoint, nudged outward (away from the city) into
    # the open paper so it never sits on top of the dashes themselves
    mid = bezier(p_near, p_ctrl, p_far, 0.5)
    tmx, tmy = bezier_tangent(p_near, p_ctrl, p_far, 0.5)
    nx, ny = -tmy, tmx
    # outward = away from city centre (~x480,y1000) -> pick the normal sign
    # that increases distance from the city
    city_c = (480, 1000)
    if (mid[0] + nx * 10 - city_c[0]) ** 2 + (mid[1] + ny * 10 - city_c[1]) ** 2 < \
       (mid[0] - nx * 10 - city_c[0]) ** 2 + (mid[1] - ny * 10 - city_c[1]) ** 2:
        nx, ny = -nx, -ny
    readout_xy = (mid[0] + nx * 34, mid[1] + ny * 34)

    font = ImageFont.truetype(F_ZILLA, 32)
    hand_lettered(canvas, "13 LAPS", readout_xy, font, INK, rng, size_hint=32)

    canvas.convert("RGB").save(OUT / "arc_counter.png")
    print("[ok] wrote", OUT / "arc_counter.png")

    # a tight crop of just the new device, for eye-QC against the source style
    zx0, zy0, zx1, zy1 = 720, 200, 1080, 620
    canvas.convert("RGB").crop((zx0, zy0, zx1, zy1)).save(OUT / "_zoom_device.png")
    print("[ok] wrote", OUT / "_zoom_device.png")


if __name__ == "__main__":
    main()
