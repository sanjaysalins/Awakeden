#!/usr/bin/env python
"""Ink-Up Build -- attention by FINISH, not by light. For a multi-element
spread, the element currently being named sits at full ink density; the
others rest partway back toward an underdrawn state (a deterministic pixel
curve toward the paper tone, line ghosts still visible) -- the classic
motion-graphics "build" (elements revealed at staged completion) translated
into this project's own sketchbook vocabulary instead of a generic wipe/
fade. The page's overall lighting never changes -- this is categorically
different from the focal_tour spotlight family (light guides the eye here;
DRAWN COMPLETENESS guides it there).

No repaint risk: the "underdrawn" look is a pure per-pixel curve of the
ALREADY-RENDERED art (L -> paper_tone + (L-paper_tone)*k), never new
generated content -- it can only ever look like a lighter/ghostlier version
of exactly what's already drawn.

Reuses focal_tour.py's build_tour_schedule/center_at for the region-visit
timing (same proven per-element narration-order schedule already used for
the spotlight family) -- only the per-region RENDER differs (ink density
blend instead of a brightness halo).

Usage:
    python ink_up_build.py --still still.png --out clip.mp4 --duration 12.6 \\
        --regions "38,8,24,30;8,60,20,28;72,60,20,28"
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from focal_tour import build_tour_schedule, center_at, halo_brightness  # noqa: E402

FPS = 30
PAPER_TONE = np.array([222, 208, 178], dtype=np.float32)  # this project's cream paper base
RESTING_K = 0.42   # how "ghosted back" an unfocused region gets (0=invisible, 1=full ink)
FOCUSED_K = 1.0


def _scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render(still: Path, regions: list[dict], out_mp4: Path, duration: float,
           w: int = 1920, h: int = 1080):
    base = _scale_crop(Image.open(still).convert("RGB"), w, h)
    src = np.asarray(base, dtype=np.float32)
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)

    schedule = build_tour_schedule(regions, duration, w, h,
                                    initial_hold_sec=max(0.6, duration * 0.10),
                                    move_sec=max(0.5, duration * 0.06),
                                    final_hold_sec=max(0.6, duration * 0.10))

    # one soft region-membership field per focal element -- reuses
    # halo_brightness's own Gaussian falloff so "attention" and "ink" share
    # the exact same spatial shape, just applied to different things.
    region_fields = []
    for r in regions:
        cx, cy, radius = None, None, None
        from focal_tour import focal_to_px
        cx, cy, radius = focal_to_px(tuple(r["bbox"]), w, h)
        field = halo_brightness(x_grid, y_grid, cx, cy, radius, dim_floor=0.0)  # 0..1 membership
        region_fields.append(field)

    n = max(1, int(round(duration * FPS)))
    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i in range(n):
        t = i / FPS
        cx, cy, _ = center_at(schedule, t)

        # k(x,y): RESTING_K everywhere, rising toward FOCUSED_K in whichever
        # region currently holds the tour's attention (nearest region center
        # to the schedule's current point governs which field dominates).
        # Distances from schedule's current focus to each region's own
        # center pick the "active" region smoothly via a soft nearest-wins.
        dists = [((cx - fx) ** 2 + (cy - fy) ** 2) for fx, fy in
                 [tuple(__import__("focal_tour").focal_to_px(tuple(r["bbox"]), w, h)[:2]) for r in regions]]
        active = int(np.argmin(dists)) if regions else -1

        k = np.full((h, w), RESTING_K, dtype=np.float32)
        if active >= 0:
            field = region_fields[active]
            k = RESTING_K + (FOCUSED_K - RESTING_K) * field

        frame = PAPER_TONE[None, None, :] + (src - PAPER_TONE[None, None, :]) * k[..., None]
        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(work / f"f{i:04d}.png")

    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%04d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out_mp4)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--regions", required=True, help="semicolon-separated x,y,w,h percent bboxes")
    a = ap.parse_args()
    regions = [{"bbox": [float(v) for v in grp.split(",")]} for grp in a.regions.split(";")]
    render(Path(a.still), regions, Path(a.out), a.duration)
