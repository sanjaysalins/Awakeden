"""Crop Study -- code-only crops/zooms of ONE AI plate.

`crop_zoom()` promotes `crop_study()` from
`poc_bethesda_style_test/round3_devices/build_stills.py` (the Blemish Hunt
device: one plate, magnified crops derived by code, never a second
generation of "the same lamb").

`camera_crop()` promotes `save_camera_crop()`'s crop math from
`poc_bethesda_style_test/far_corner_episode/build_plate_and_crops.py`. This
is the SEAM function: it replicates InsertPageCamera's own single-keyframe
`frame_at(0.0)` call exactly, so a paid animated insert's start-image is
pixel-identical to what a static camera segment would show at that same
cx/cy/zoom -- the cut into animation is invisible.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

_PANEL_ANIMATOR_DIR = Path(__file__).resolve().parents[2] / "panel_animator"
if str(_PANEL_ANIMATOR_DIR) not in sys.path:
    sys.path.insert(0, str(_PANEL_ANIMATOR_DIR))

from insert_page_camera import InsertPageCamera  # noqa: E402


def crop_zoom(
    raw: Image.Image,
    box_frac: tuple[float, float, float, float],
    out_size: tuple[int, int] | None = None,
) -> Image.Image:
    """Crop `raw` to the fractional box (x0,y0,x1,y1) and resize back up to
    `out_size` (defaults to raw.size -- a magnified "zoom" of that region)."""
    img = raw.convert("RGB")
    w, h = img.size
    x0, y0, x1, y1 = box_frac
    crop = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    target = out_size if out_size is not None else img.size
    return crop.resize(target, Image.LANCZOS)


def camera_crop(
    raw: Image.Image,
    cx_frac: float,
    cy_frac: float,
    zoom: float,
    out_w: int = 1080,
    out_h: int = 1920,
) -> Image.Image:
    """The exact pixel crop InsertPageCamera would show at (cx_frac, cy_frac,
    zoom) -- a single-keyframe camera, frame_at(0.0). Used to produce a paid
    insert's source image that seamlessly matches a static segment's ending
    frame.

    `raw` is written to a temp file because InsertPageCamera's constructor
    takes a still_path, not an in-memory Image (matching the source script's
    own `save_camera_crop(still_path, ...)` call pattern)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp) / "raw_for_camera_crop.png"
        raw.convert("RGB").save(tmp_path)
        cam = InsertPageCamera(
            tmp_path,
            keyframes=[{"t": 0.0, "cx": cx_frac, "cy": cy_frac, "zoom": zoom, "hold_s": 0.0}],
            duration_s=1.0,
            out_w=out_w,
            out_h=out_h,
        )
        return cam.frame_at(0.0)
