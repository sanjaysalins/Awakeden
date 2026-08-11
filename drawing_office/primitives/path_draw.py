"""Path Draw -- hand-wobbled dashed line composited onto a plate.

Promotes `draw_survey_path()` from
`poc_bethesda_style_test/far_corner_episode/build_plate_and_crops.py`
near-verbatim: a low-frequency sine wobble (not per-point noise -- reads as
a hand tracing a line, not jitter), drawn dashed with tick marks and an
endpoint dot, at 2x supersample then downsized for anti-aliasing.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw


def draw_wobbled_path(
    img_path: Path,
    out_path: Path,
    start_frac: tuple[float, float],
    end_frac: tuple[float, float],
    color=(178, 42, 24),
    n_points: int = 60,
    dash_len: int = 5,
    gap_len: int = 4,
) -> None:
    """Hand-wobbled dashed line from start_frac to end_frac (image-fraction
    coords), matching the red survey-line device from build_plate_and_crops.py."""
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    ss = 2
    big = img.resize((w * ss, h * ss), Image.LANCZOS)
    draw = ImageDraw.Draw(big)

    x0, y0 = start_frac[0] * big.width, start_frac[1] * big.height
    x1, y1 = end_frac[0] * big.width, end_frac[1] * big.height

    n = n_points
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        # gentle hand-wobble: low-frequency sine jitter, not per-point noise
        wobble = math.sin(t * 5.3 + 1.7) * 6 * ss + math.sin(t * 11.0) * 2 * ss
        # perpendicular offset
        dx, dy = x1 - x0, y1 - y0
        length = max(1e-6, math.hypot(dx, dy))
        nx, ny = -dy / length, dx / length
        pts.append((x + nx * wobble, y + ny * wobble))

    # dashed: draw short segments with gaps
    i = 0
    while i < len(pts) - 1:
        j = min(len(pts) - 1, i + dash_len)
        draw.line(pts[i:j + 1], fill=color, width=int(2.4 * ss))
        i = j + gap_len

    # small tick marks every ~10 segments (measured-distance device)
    for k in range(0, len(pts), 10):
        x, y = pts[k]
        dx, dy = x1 - x0, y1 - y0
        length = max(1e-6, math.hypot(dx, dy))
        nx, ny = -dy / length, dx / length
        tick = 5 * ss
        draw.line([(x - nx * tick, y - ny * tick), (x + nx * tick, y + ny * tick)],
                   fill=color, width=int(1.4 * ss))

    # endpoint dot at the far corner
    r = 3.2 * ss
    draw.ellipse((x1 - r, y1 - r, x1 + r, y1 + r), fill=color)

    out = big.resize((w, h), Image.LANCZOS)
    out.save(out_path)
