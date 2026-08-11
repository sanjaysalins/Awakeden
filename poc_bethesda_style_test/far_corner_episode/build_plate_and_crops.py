"""THROWAWAY EPISODE BUILD -- Bethesda / The Far Corner.

Step 1: composite the final "full plate + red survey path" image from
far_corner_01.png (a code-drawn hand-wobbled dashed red line, matching the
style already established in far_corner_02/03's AI-rendered lines).

Step 2: use the SAME crop math as panel_animator/insert_page_camera.py to cut
the two paid-insert source images at the EXACT frame the static camera
segments will end on, so the cut into each animated clip is seamless.
"""
from __future__ import annotations
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
STILLS = HERE.parent / "stills"
OUT = HERE
sys.path.insert(0, str(HERE.parent.parent / "panel_animator"))
from insert_page_camera import InsertPageCamera  # noqa: E402

random.seed(7)


def draw_survey_path(src_path: Path, out_path: Path,
                      start_frac: tuple[float, float],
                      end_frac: tuple[float, float],
                      color=(178, 42, 24)) -> None:
    """Hand-wobbled dashed line from start_frac to end_frac (image-fraction
    coords), matching the red survey-line device already used in
    far_corner_02/03. Drawn at 2x supersample then downsized for a clean
    anti-aliased line."""
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    ss = 2
    big = img.resize((w * ss, h * ss), Image.LANCZOS)
    draw = ImageDraw.Draw(big)

    x0, y0 = start_frac[0] * big.width, start_frac[1] * big.height
    x1, y1 = end_frac[0] * big.width, end_frac[1] * big.height

    n = 60
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
    dash_len = 5
    gap_len = 4
    i = 0
    while i < len(pts) - 1:
        j = min(len(pts) - 1, i + dash_len)
        draw.line(pts[i:j + 1], fill=color, width=int(2.4 * ss))
        i = j + gap_len

    # small tick marks every ~10 segments (measured-distance device, echoing far_corner_02)
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
    print(f"[ok] {out_path.name}  path {start_frac} -> {end_frac}")


def save_camera_crop(still_path: Path, cx: float, cy: float, zoom: float, out_path: Path) -> None:
    cam = InsertPageCamera(still_path, keyframes=[{"t": 0.0, "cx": cx, "cy": cy, "zoom": zoom, "hold_s": 0.0}],
                            duration_s=1.0)
    frame = cam.frame_at(0.0)
    frame.save(out_path)
    print(f"[ok] {out_path.name}  crop cx={cx} cy={cy} zoom={zoom}  size={frame.size}")


if __name__ == "__main__":
    # entrance notch near bottom-center of far_corner_01 -> far-corner position
    # (bottom-left quadrant, matching far_corner_02/03's "lone man alone" placement)
    draw_survey_path(
        STILLS / "far_corner_01.png",
        OUT / "final_plate.png",
        start_frac=(0.50, 0.86),
        end_frac=(0.27, 0.50),
    )

    # S1 (hook dive) ends here -> insert A (water stirs) starts here
    save_camera_crop(STILLS / "far_corner_01.png", cx=0.50, cy=0.46, zoom=1.65,
                      out_path=OUT / "inserts" / "insert_a_source.png")

    # S5 (close pair push) ends here -> insert B (rise) starts here
    save_camera_crop(STILLS / "far_corner_03.png", cx=0.50, cy=0.62, zoom=1.4,
                      out_path=OUT / "inserts" / "insert_b_source.png")
