"""Focal Tour -- light (not camera) sweeps a soft halo through a still's own
named elements in sequence, dimming everything else, so the eye is drawn to
each one in turn without ever cropping/zooming the frame. Ported from a
sibling project (edenradios' pipeline/utils/motion_styles.py, its
"dramatic_spotlight" family) -- ~13 render-quality bake-off variants tested
there before landing on this technique. Adapted here as a project-agnostic,
$0 deterministic PIL/numpy + ffmpeg module (no LLM dependency in the core;
focal regions are supplied explicitly).

Use this instead of a flat uniform push-in whenever a single still has 2-4
distinct named elements (a vignette, a main figure, a caption/verse area,
...) that should each get a moment of attention in a fixed narration window
-- a "camera tour" without ever physically cropping the page, which also
sidesteps the crop-vs-content-bounds bookkeeping a real push-in needs.

Two ways to use it:

1. Standalone clip from a bare still:
     render_clip(image_path, focal_regions, motion_style, duration_sec,
                 output_w, output_h, out_path)
   Motion styles: dramatic_spotlight, caravaggio_pulse (breathing halo),
   desat_focus (colour halo on a desaturated base), chiaroscuro_reveal
   (focals ignite cumulatively), slow_breath (sleep-paced), cross_fade,
   dipblack (crop-shot slideshows with dissolves, no halo).

2. Interleaved with other per-frame compositing (e.g. a device like the
   gold Thread or a letterpressed verse already drawn on top of the base
   art each frame) -- build a schedule once, then multiply your own
   composited RGB frame by the halo field at each frame's global time:

     from focal_tour import build_tour_schedule, halo_field, center_at
     schedule = build_tour_schedule(focal_regions, duration_sec, w, h)
     ...
     for t in frame_times:
         frame = my_own_compose(t)                       # your art + overlays
         cx, cy, r = center_at(schedule, t)
         frame = apply_halo(frame, cx, cy, r, dim_floor=0.30)

focal_regions: list of {"bbox": [x,y,w,h] percent of frame (0-100, top-left
origin), "zoom": float (only used by cross_fade/dipblack's crop shots)}.
Order = narration order (the tour visits them in the order given).
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FPS = 30

MOTION_STYLES: tuple[str, ...] = (
    "cross_fade", "dipblack", "dramatic_spotlight", "caravaggio_pulse",
    "desat_focus", "chiaroscuro_reveal", "slow_breath",
)
DEFAULT_STYLE = "dramatic_spotlight"

_DIM_FLOOR_DRAMATIC = 0.30
_WARM_SEPIA_TINT = np.array([0.95, 0.85, 0.65], dtype=np.float32)
_DESAT_DIM = 0.65
_CHIARO_BASE_DIM = 0.20


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


# --------------------------------------------------------------- geometry

def focal_to_px(bbox_pct: tuple[float, float, float, float], output_w: int, output_h: int
                 ) -> tuple[float, float, float]:
    """(cx_px, cy_px, halo_radius_px) for a focal bbox (x,y,w,h in percent)."""
    bx, by, bw, bh = bbox_pct
    cx = (bx + bw / 2.0) / 100.0 * output_w
    cy = (by + bh / 2.0) / 100.0 * output_h
    bbox_w_px = bw / 100.0 * output_w
    bbox_h_px = bh / 100.0 * output_h
    diag = math.sqrt(bbox_w_px ** 2 + bbox_h_px ** 2)
    halo_radius = max(diag * 0.55, output_w * 0.16)
    return cx, cy, halo_radius


def halo_brightness(x_grid: np.ndarray, y_grid: np.ndarray, cx: float, cy: float,
                     radius: float, dim_floor: float) -> np.ndarray:
    sigma = max(radius * 0.55, 1.0)
    dist_sq = (x_grid - cx) ** 2 + (y_grid - cy) ** 2
    mask = np.exp(-dist_sq / (2.0 * sigma ** 2))
    return dim_floor + (1.0 - dim_floor) * mask


def apply_halo(frame_rgb: np.ndarray | Image.Image, cx: float, cy: float, radius: float,
                dim_floor: float = _DIM_FLOOR_DRAMATIC) -> np.ndarray:
    """Multiply an already-composited frame by the halo field. Accepts/returns
    a float32 0..1 HxWx3 array (matches this module's own frame convention) --
    pass `arr = np.asarray(pil_img, dtype=np.float32)/255.0` in, and
    `Image.fromarray((out*255).astype('uint8'))` out, if working in PIL."""
    if isinstance(frame_rgb, Image.Image):
        arr = np.asarray(frame_rgb.convert("RGB"), dtype=np.float32) / 255.0
    else:
        arr = frame_rgb
    h, w = arr.shape[:2]
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
    bright = halo_brightness(x_grid, y_grid, cx, cy, radius, dim_floor)[..., None]
    return arr * bright


# ------------------------------------------------------------- tour schedule

class TourSchedule:
    """Waypoint list [full, focal1, ..., focalN, full] + the timing to move
    through them: initial_hold, then (move, hold) per focal, then a final
    move back to full + final_hold. `center_at(t)` interpolates."""

    def __init__(self, waypoints, seg_starts, seg_kinds, total_dur):
        self.waypoints = waypoints          # list of (cx, cy, radius)
        self.seg_starts = seg_starts        # cumulative start time of each segment
        self.seg_kinds = seg_kinds          # "hold" or ("move", wp_a_idx, wp_b_idx)
        self.total_dur = total_dur


def build_tour_schedule(focal_regions: list[dict], duration_sec: float, output_w: int, output_h: int,
                         initial_hold_sec: float = 0.8, move_sec: float = 1.2,
                         final_hold_sec: float = 2.0) -> TourSchedule:
    """Full -> focal_1 -> focal_2 -> ... -> focal_N -> full, in the order
    given. Remaining time after the fixed holds/moves splits evenly across
    the N focal holds (minimum 1s each, extending final_hold if that floor
    can't be met -- a tour is not allowed to silently rush past an element)."""
    full_center = (output_w / 2.0, output_h / 2.0, output_w * 2.5)
    focal_centers = [focal_to_px(tuple(r["bbox"]), output_w, output_h) for r in focal_regions]
    n = len(focal_centers)
    n_moves = n + 1
    remaining = duration_sec - initial_hold_sec - final_hold_sec - n_moves * move_sec
    focal_hold_sec = max(1.0, remaining / max(n, 1)) if n else 0.0

    waypoints = [full_center] + focal_centers + [full_center]
    seg_starts = [0.0]
    seg_kinds = []
    t = initial_hold_sec
    seg_kinds.append(("hold", 0))
    seg_starts.append(t)
    for i in range(len(waypoints) - 1):
        seg_kinds.append(("move", i, i + 1))
        t += move_sec
        seg_starts.append(t)
        if i < len(waypoints) - 2:
            seg_kinds.append(("hold", i + 1))
            t += focal_hold_sec
            seg_starts.append(t)
    seg_kinds.append(("hold", len(waypoints) - 1))
    t += final_hold_sec
    seg_starts.append(t)
    return TourSchedule(waypoints, seg_starts, seg_kinds, t)


def center_at(schedule: TourSchedule, t: float) -> tuple[float, float, float]:
    """Current (cx, cy, radius) at global time t, clamped to the schedule."""
    t = max(0.0, min(schedule.total_dur, t))
    for i, kind in enumerate(schedule.seg_kinds):
        seg_t0, seg_t1 = schedule.seg_starts[i], schedule.seg_starts[i + 1]
        if t > seg_t1 and i < len(schedule.seg_kinds) - 1:
            continue
        if kind[0] == "hold":
            return schedule.waypoints[kind[1]]
        _, ia, ib = kind
        dur = seg_t1 - seg_t0
        frac = smoothstep((t - seg_t0) / dur) if dur > 0 else 1.0
        a, b = schedule.waypoints[ia], schedule.waypoints[ib]
        return tuple(a[k] + (b[k] - a[k]) * frac for k in range(3))
    return schedule.waypoints[-1]


# --------------------------------------------------------------- ffmpeg io

def _open_ffmpeg(out_path: Path, output_w: int, output_h: int) -> subprocess.Popen:
    return subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{output_w}x{output_h}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "fast", str(out_path)],
        stdin=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def _write_frame(proc: subprocess.Popen, arr: np.ndarray) -> None:
    proc.stdin.write((np.clip(arr, 0.0, 1.0) * 255.0).astype(np.uint8).tobytes())


def _finalize(proc: subprocess.Popen) -> None:
    proc.stdin.close()
    _, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg encode failed:\n{err.decode(errors='replace')[-2000:]}")


def _static_full(src: Image.Image, w: int, h: int) -> np.ndarray:
    return np.asarray(src.resize((w, h), Image.LANCZOS), dtype=np.float32) / 255.0


def _static_crop(src: Image.Image, bbox_pct, zoom: float, w: int, h: int) -> np.ndarray:
    sw, sh = src.size
    bx, by, bw, bh = bbox_pct
    cx, cy = (bx + bw / 2.0) / 100.0, (by + bh / 2.0) / 100.0
    aspect = w / h
    crop_w_px = sw / zoom
    crop_h_px = crop_w_px / aspect
    if crop_h_px > sh:
        crop_h_px = sh
        crop_w_px = crop_h_px * aspect
    cx_px = max(crop_w_px / 2, min(sw - crop_w_px / 2, cx * sw))
    cy_px = max(crop_h_px / 2, min(sh - crop_h_px / 2, cy * sh))
    left, top = int(round(cx_px - crop_w_px / 2)), int(round(cy_px - crop_h_px / 2))
    crop = src.crop((left, top, left + int(crop_w_px), top + int(crop_h_px))).resize((w, h), Image.LANCZOS)
    return np.asarray(crop, dtype=np.float32) / 255.0


# ------------------------------------------------------------- style renderers

def _render_slideshow(src, focal_regions, duration_sec, w, h, out_path, *, xfade_sec, dip_black):
    chosen = focal_regions[:3]
    shots = [_static_full(src, w, h)] + [_static_crop(src, tuple(r["bbox"]), float(r.get("zoom", 2.0)), w, h)
                                          for r in chosen] + [_static_full(src, w, h)]
    total_frames = int(round(duration_sec * FPS))
    n = len(shots)
    xfade_frames = max(2 if dip_black else 1, int(round(xfade_sec * FPS)))
    hold_frames = max(1, (total_frames - (n - 1) * xfade_frames) // n)
    proc = _open_ffmpeg(out_path, w, h)
    try:
        for i in range(n):
            for _ in range(hold_frames):
                _write_frame(proc, shots[i])
            if i < n - 1:
                if dip_black:
                    half = xfade_frames // 2
                    for f in range(half):
                        _write_frame(proc, shots[i] * (1.0 - smoothstep((f + 1) / half)))
                    for f in range(xfade_frames - half):
                        _write_frame(proc, shots[i + 1] * smoothstep((f + 1) / (xfade_frames - half)))
                else:
                    for f in range(xfade_frames):
                        a = smoothstep((f + 1) / xfade_frames)
                        _write_frame(proc, (1.0 - a) * shots[i] + a * shots[i + 1])
    finally:
        _finalize(proc)


def _render_spotlight(src, focal_regions, duration_sec, w, h, out_path, *,
                       dim_floor, pulse_amplitude=0.0,
                       initial_hold_sec=2.5, move_sec=1.0, final_hold_sec=2.5):
    src_arr = _static_full(src, w, h)
    hh, ww = src_arr.shape[:2]
    y_grid, x_grid = np.mgrid[0:hh, 0:ww].astype(np.float32)
    schedule = build_tour_schedule(focal_regions, duration_sec, w, h,
                                    initial_hold_sec, move_sec, final_hold_sec)
    n_frames = int(round(duration_sec * FPS))
    proc = _open_ffmpeg(out_path, w, h)
    try:
        for f in range(n_frames):
            t = f / FPS
            cx, cy, r = center_at(schedule, t)
            if pulse_amplitude > 0:
                r *= 1.0 + pulse_amplitude * math.sin(2 * math.pi * (t % 3.0) / 3.0)
            bright = halo_brightness(x_grid, y_grid, cx, cy, r, dim_floor)
            _write_frame(proc, src_arr * bright[..., None])
    finally:
        _finalize(proc)


def _render_desat_focus(src, focal_regions, duration_sec, w, h, out_path):
    src_arr = _static_full(src, w, h)
    hh, ww = src_arr.shape[:2]
    y_grid, x_grid = np.mgrid[0:hh, 0:ww].astype(np.float32)
    gray = 0.299 * src_arr[..., 0] + 0.587 * src_arr[..., 1] + 0.114 * src_arr[..., 2]
    desat_baseline = np.stack([gray] * 3, axis=-1) * _WARM_SEPIA_TINT[None, None, :] * _DESAT_DIM
    schedule = build_tour_schedule(focal_regions, duration_sec, w, h)
    n_frames = int(round(duration_sec * FPS))
    proc = _open_ffmpeg(out_path, w, h)
    try:
        for f in range(n_frames):
            t = f / FPS
            cx, cy, r = center_at(schedule, t)
            sigma = max(r * 0.55, 1.0)
            halo = np.exp(-((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / (2.0 * sigma ** 2))[..., None]
            _write_frame(proc, halo * src_arr + (1.0 - halo) * desat_baseline)
    finally:
        _finalize(proc)


def _render_chiaroscuro_reveal(src, focal_regions, duration_sec, w, h, out_path):
    src_arr = _static_full(src, w, h)
    hh, ww = src_arr.shape[:2]
    y_grid, x_grid = np.mgrid[0:hh, 0:ww].astype(np.float32)
    focal_centers = [focal_to_px(tuple(r["bbox"]), w, h) for r in focal_regions]
    total_frames = int(round(duration_sec * FPS))
    n = len(focal_centers)
    ignition_frames = [int(total_frames * (0.10 + 0.75 * i / max(n - 1, 1))) for i in range(n)]
    ramp_frames = max(1, int(total_frames * 0.12))
    masks = []
    for cx, cy, r in focal_centers:
        sigma = max(r * 0.55, 1.0)
        masks.append(np.exp(-((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / (2.0 * sigma ** 2)))
    proc = _open_ffmpeg(out_path, w, h)
    try:
        for f in range(total_frames):
            lit = np.zeros((hh, ww), dtype=np.float32)
            for i in range(n):
                if f < ignition_frames[i]:
                    continue
                amt = smoothstep((f - ignition_frames[i]) / ramp_frames)
                lit = np.maximum(lit, masks[i] * amt)
            bright = _CHIARO_BASE_DIM + (1.0 - _CHIARO_BASE_DIM) * lit
            _write_frame(proc, src_arr * bright[..., None])
    finally:
        _finalize(proc)


_RENDERERS = {
    "cross_fade": lambda *a, **k: _render_slideshow(*a, xfade_sec=1.5, dip_black=False, **k),
    "dipblack": lambda *a, **k: _render_slideshow(*a, xfade_sec=2.0, dip_black=True, **k),
    "dramatic_spotlight": lambda *a, **k: _render_spotlight(*a, dim_floor=_DIM_FLOOR_DRAMATIC, **k),
    "caravaggio_pulse": lambda *a, **k: _render_spotlight(*a, dim_floor=_DIM_FLOOR_DRAMATIC,
                                                            pulse_amplitude=0.20, **k),
    "slow_breath": lambda *a, **k: _render_spotlight(*a, dim_floor=0.40, pulse_amplitude=0.05,
                                                       initial_hold_sec=5.0, move_sec=3.0,
                                                       final_hold_sec=5.0, **k),
    "desat_focus": _render_desat_focus,
    "chiaroscuro_reveal": _render_chiaroscuro_reveal,
}


def render_clip(image_path: Path, focal_regions: list[dict], motion_style: str, duration_sec: float,
                 output_w: int, output_h: int, out_path: Path) -> None:
    """Dispatch to the named renderer for a STANDALONE clip (no custom
    overlays). For interleaved use with your own per-frame compositing, use
    build_tour_schedule() + center_at() + apply_halo() directly instead."""
    if motion_style not in _RENDERERS:
        raise ValueError(f"unknown motion_style {motion_style!r}. Known: {', '.join(MOTION_STYLES)}")
    src = Image.open(image_path).convert("RGB")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _RENDERERS[motion_style](src, focal_regions, duration_sec, output_w, output_h, out_path)
