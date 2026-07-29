#!/usr/bin/env python
"""Wash-Creep -- the paint has not dried yet. Isolates a dark blue-grey
watercolour wash (a storm sky/sea) by HSV band, then advances or retreats its
edge a few px along the paper fibre: a feathered, slightly fingered front,
the way ink spreads on damp cold-press paper. Reverse it (negative
advance_px) and the wash dries back, cream paper reclaiming what the ink had
taken -- the safest possible way to render "and there was a great calm": the
*paint* obeys, not a generated frame.

$0, deterministic numpy/cv2/PIL + ffmpeg encode for the demo. Engine only --
callers own compositing this onto a spread inside their own assembler
(e.g. `poc_living_sketchbook/storm/_s4_assemble.py`); this module never reads
an alignment file or a scene plan.

Family: related to `ink_transition.py`'s noise-field reveal, but that one
wipes BETWEEN two clips -- this one deforms a colour region INSIDE one.

Usage (library):
    from wash_creep import isolate_storm_wash, apply_wash_creep
    mask = isolate_storm_wash(still)          # compute ONCE per still
    frame = apply_wash_creep(still, advance_px=9.0, mask=mask)
    frame = apply_wash_creep(still, advance_px=-6.0, mask=mask, backrun=True)

Usage (demo CLI):
    python wash_creep.py --demo --still still.png --out demo.mp4
        [--duration 8] [--direction advance|retreat|both]
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# isolate_storm_wash -- HSV band tuned on the storm episode's dark navy/
# charcoal washes (calibrated against s01_waves.png / s04_asleep.png).
# ---------------------------------------------------------------------------
HUE_LO, HUE_HI = 95, 140      # OpenCV 0-179 hue scale: blue-grey band
SAT_LO = 25                   # excludes near-achromatic ink linework/kraft/cream
VAL_LO, VAL_HI = 10, 195      # excludes near-black ink and bright paper/highlights
MIN_AREA_FRAC = 0.0015        # drop connected components smaller than this fraction of the frame


def isolate_storm_wash(frame: Image.Image) -> np.ndarray:
    """Return a uint8 0/255 mask of the dark blue-grey storm wash region.

    HSV band on the blue-grey hues + low-mid value -> morphological close to
    knit the watercolour's mottled interior into one region -> keep only the
    largest connected components (drops stray blue-grey noise elsewhere in
    the frame, e.g. a shadow or a fold line).
    """
    arr = np.array(frame.convert("RGB"))
    h, w = arr.shape[:2]
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
    hue, sat, val = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    band = (
        (hue >= HUE_LO) & (hue <= HUE_HI)
        & (sat >= SAT_LO)
        & (val >= VAL_LO) & (val <= VAL_HI)
    )
    raw = (band * 255).astype(np.uint8)

    k = max(5, int(round(min(h, w) * 0.006)) | 1)  # odd, proportional to frame size
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    closed = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, kernel)

    n, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    min_area = MIN_AREA_FRAC * h * w
    keep = np.zeros_like(closed)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep[labels == i] = 255
    return keep


# ---------------------------------------------------------------------------
# apply_wash_creep
# ---------------------------------------------------------------------------
NOISE_CELL = 46            # px per noise grid cell (pre-upsample) -- controls "finger" scale
NOISE_AMP_PX = 5.0         # +/- perturbation applied to the distance-field radius
FEATHER_PX = 2.5           # soft edge width at the new front
SAFE_MARGIN_FRAC = 0.05    # never claim pixels this close to the raw canvas edge -- the
                            # illustration's ruled border / torn kraft backing lives out there
HIGHLIGHT_GUARD_V = 236    # never claim a near-white/gold specular highlight outright
BARRIER_VAL = 65           # near-black ink linework is a reserve the wash can't creep through
                            # (a hand-inked outline around a foreground object works exactly
                            # like a frisket in real watercolour -- the wash stops at the line)
PAPER_HUE_LO, PAPER_HUE_HI = 0, 55   # warm hue range of blank kraft/cream paper
PAPER_VAL_MIN = 120                  # paper is bright; a dark warm pixel is a shadow/object, not paper
PAPER_REACH_MIN = 0.14                # retreat needs >=14% real paper in its sampling window
                                      # or it leaves that stretch of edge frozen (see _paper_reach)


def _low_freq_noise(h: int, w: int, seed: int, cell: int = NOISE_CELL, amp: float = NOISE_AMP_PX) -> np.ndarray:
    """A smooth, seeded, low-frequency field (roughly +/-amp), same trick as
    ink_transition.make_reveal_field: a small random grid, upsampled with
    BICUBIC so it stays low-frequency instead of per-pixel noise."""
    rng = np.random.default_rng(seed)
    sh, sw = max(2, h // cell), max(2, w // cell)
    small = rng.random((sh, sw)).astype(np.float32)
    big = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    field = np.asarray(big, dtype=np.float32) / 255.0
    return (field - float(field.mean())) * (2.0 * amp)


def _safe_zone(h: int, w: int, margin_frac: float = SAFE_MARGIN_FRAC) -> np.ndarray:
    """True everywhere except a thin margin at the raw canvas edge."""
    my, mx = int(h * margin_frac), int(w * margin_frac)
    zone = np.zeros((h, w), dtype=bool)
    zone[my:h - my, mx:w - mx] = True
    return zone


def _paper_like(hsv: np.ndarray) -> np.ndarray:
    """True where a pixel's own colour reads as blank kraft/cream paper (warm
    hue, bright) rather than another inked object (this style's mast/ropes/
    hull are painted in the same cool palette as the wash, just lighter --
    hue is what actually separates them, not brightness alone)."""
    hue, val = hsv[..., 0], hsv[..., 2]
    return (hue >= PAPER_HUE_LO) & (hue <= PAPER_HUE_HI) & (val >= PAPER_VAL_MIN)


def _geodesic_advance(wash: np.ndarray, barrier: np.ndarray, max_radius: int) -> np.ndarray:
    """Grassfire-grow `wash` outward up to `max_radius` px, one px per step,
    never crossing a `barrier` pixel. Returns a float 'arrival step' field
    (px at which each pixel was first reached; untouched pixels stay inf).
    This is a geodesic/obstacle-respecting alternative to
    cv2.distanceTransform's straight-line distance -- a hand-inked outline
    around a foreground object (the mast, a rope, the hull) is a real
    barrier the wash can't tunnel through to reach paper on the far side."""
    current = wash.copy()
    arrival = np.full(wash.shape, np.inf, dtype=np.float32)
    kernel = np.ones((3, 3), np.uint8)
    steps = max(1, int(np.ceil(max_radius)))
    for step in range(1, steps + 1):
        dilated = cv2.dilate(current.astype(np.uint8), kernel) > 0
        newly = dilated & ~current & ~barrier
        if not newly.any():
            break
        arrival[newly] = step
        current = current | newly
    return arrival


def _local_fill(arr_f: np.ndarray, weight: np.ndarray, radius: int) -> np.ndarray:
    """The wash's (or paper's) own locally-sampled colour: a normalized
    box-filter average of arr_f restricted to wherever `weight` is truthy.
    cv2.boxFilter is a running-sum filter, so this is cheap even at a
    generous radius -- no per-pixel nearest-neighbour search needed. Only
    meaningful where `_paper_reach` (below) says the window has real
    coverage -- callers must gate on that separately, this does no fallback."""
    k = max(3, 2 * radius + 1)
    w3 = weight.astype(np.float32)
    wsum = cv2.boxFilter(w3, ddepth=-1, ksize=(k, k), normalize=False)
    csum = cv2.boxFilter(arr_f * w3[..., None], ddepth=-1, ksize=(k, k), normalize=False)
    return csum / np.clip(wsum, 1e-3, None)[..., None]


def _paper_reach(paper_like: np.ndarray, radius: int) -> np.ndarray:
    """0..1 fraction of an rxr window around each pixel that is genuine
    paper. Retreat only reveals paper where this is high enough -- a wash
    edge that borders the mast/a rope/the hull, not open page, has nothing
    to retreat INTO, so that stretch of edge is left frozen rather than
    filled with a guess (avoids both object-colour bleed and a smoothed
    fallback tone that reads as a flat halo instead of real paper)."""
    k = max(3, 2 * radius + 1)
    return cv2.boxFilter(paper_like.astype(np.float32), ddepth=-1, ksize=(k, k), normalize=True)


def _feather(mask_bool: np.ndarray, px: float = FEATHER_PX) -> np.ndarray:
    k = max(3, int(round(px)) * 2 + 1)
    alpha = cv2.GaussianBlur(mask_bool.astype(np.float32), (k, k), px / 2.0)
    return np.clip(alpha, 0.0, 1.0)


def apply_wash_creep(frame: Image.Image, advance_px: float, mask: np.ndarray | None = None,
                      backrun: bool = False, seed: int = 7) -> Image.Image:
    """Advance (advance_px > 0) or retreat (advance_px < 0) the storm wash's
    edge by that many px along a fibrous, noise-perturbed front. `frame` is
    the ORIGINAL already-composited still every time -- this is not
    cumulative, callers animate by varying advance_px call to call, not by
    feeding a prior call's output back in.

    If `mask` is None, `isolate_storm_wash` is called internally (pass the
    mask explicitly when animating a sequence so it's computed once and the
    fibrous pattern stays temporally consistent).

    If `backrun=True`, also blend a pale "cauliflower bloom" patch near the
    new edge -- wet pigment pushed back into a drying wash.
    """
    rgb = frame.convert("RGB")
    arr = np.array(rgb)
    h, w = arr.shape[:2]
    arr_f = arr.astype(np.float32)

    if mask is None:
        mask = isolate_storm_wash(rgb)
    wash = np.asarray(mask) > 0

    if abs(advance_px) < 0.05 and not backrun:
        return rgb

    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
    paper_like = _paper_like(hsv)      # blank kraft/cream paper, by its own colour
    noise = _low_freq_noise(h, w, seed)

    if advance_px >= 0:
        barrier = (hsv[..., 2] < BARRIER_VAL) & ~wash   # near-black ink outline = a reserve
        radius = max(1, int(round(advance_px)) + 2)
        arrival = _geodesic_advance(wash, barrier, radius)
        front = arrival + noise

        highlight_guard = hsv[..., 2] >= HIGHLIGHT_GUARD_V
        safe = _safe_zone(h, w)

        claimed = (~wash) & safe & (~highlight_guard) & (front <= advance_px)
        fill = _local_fill(arr_f, wash, max(4, radius))
        alpha = _feather(claimed)
        out = arr_f * (1 - alpha[..., None]) + fill * alpha[..., None]
        edge_zone = claimed
    else:
        radius_px = -advance_px
        wash_u8 = wash.astype(np.uint8) * 255
        dist_in = cv2.distanceTransform(wash_u8, cv2.DIST_L2, 5)
        front = dist_in + noise

        # a wash edge bordering the mast/a rope/the hull has no paper to retreat INTO --
        # only reveal paper where the sampling window actually has real paper reach;
        # elsewhere that stretch of edge is left frozen (see _paper_reach's docstring)
        reach_radius = max(12, int(round(radius_px)) + 10)
        reach = _paper_reach(paper_like, reach_radius)
        vacated = wash & (front <= radius_px) & (reach >= PAPER_REACH_MIN)
        fill = _local_fill(arr_f, (~wash) & paper_like, reach_radius)
        alpha = _feather(vacated)
        out = arr_f * (1 - alpha[..., None]) + fill * alpha[..., None]
        edge_zone = wash & ~vacated  # just inside the surviving edge

    if backrun:
        bloom_noise = _low_freq_noise(h, w, seed + 101, cell=max(18, NOISE_CELL // 2), amp=1.0)
        thresh = float(np.quantile(bloom_noise, 0.82))  # top ~18% -> blobby "cauliflower" patches
        reach = _paper_reach(paper_like, 22)
        bloom_mask = edge_zone & (bloom_noise >= thresh) & (reach >= PAPER_REACH_MIN)
        bloom_alpha = _feather(bloom_mask, px=3.0) * 0.55
        paper_tint = _local_fill(arr_f, (~wash) & paper_like, 22)
        pale = out * 0.55 + paper_tint * 0.45
        out = out * (1 - bloom_alpha[..., None]) + pale * bloom_alpha[..., None]

    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGB")


# ---------------------------------------------------------------------------
# --demo CLI
# ---------------------------------------------------------------------------
FPS = 30
ADVANCE_MAX = 15.0


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def _ease(t: float) -> float:
    """Smoothstep -- watercolour absorption doesn't move at constant rate."""
    return t * t * (3 - 2 * t)


def _build_frame_plan(direction: str, n_frames: int) -> list[tuple[float, bool]]:
    """Return [(advance_px, backrun_on), ...] for each output frame."""
    plan: list[tuple[float, bool]] = []
    if direction == "advance":
        for i in range(n_frames):
            t = _ease(i / max(1, n_frames - 1))
            plan.append((t * ADVANCE_MAX, t > 0.62))
    elif direction == "retreat":
        for i in range(n_frames):
            t = _ease(i / max(1, n_frames - 1))
            plan.append((ADVANCE_MAX - t * (2 * ADVANCE_MAX), False))
    else:  # "both" -- advance, hold with a backrun bloom, then dry back past the original edge
        n_adv = int(n_frames * 0.42)
        n_hold = int(n_frames * 0.12)
        n_ret = n_frames - n_adv - n_hold
        for i in range(n_adv):
            t = _ease(i / max(1, n_adv - 1))
            plan.append((t * ADVANCE_MAX, False))
        for _ in range(n_hold):
            plan.append((ADVANCE_MAX, True))
        for i in range(n_ret):
            t = _ease(i / max(1, n_ret - 1))
            plan.append((ADVANCE_MAX - t * (2 * ADVANCE_MAX), False))
    return plan


def render_demo(still: Path, out_mp4: Path, duration: float, direction: str):
    base = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    mask = isolate_storm_wash(base)  # computed ONCE, reused every frame

    n_frames = max(1, int(round(duration * FPS)))
    plan = _build_frame_plan(direction, n_frames)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    for i, (advance_px, backrun) in enumerate(plan):
        frame = apply_wash_creep(base, advance_px, mask=mask, backrun=backrun)
        frame.save(work / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
        check=True, capture_output=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip from a single still")
    ap.add_argument("--still", help="source still (any resolution)")
    ap.add_argument("--out", help="output mp4")
    ap.add_argument("--duration", type=float, default=8.0)
    ap.add_argument("--direction", choices=["advance", "retreat", "both"], default="both")
    a = ap.parse_args()
    if not a.demo:
        raise SystemExit("wash_creep.py is a library; run with --demo --still <png> --out <mp4> to preview")
    if not a.still or not a.out:
        raise SystemExit("--demo requires --still and --out")
    render_demo(Path(a.still), Path(a.out), a.duration, a.direction)
