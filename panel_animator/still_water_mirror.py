#!/usr/bin/env python
"""Still-Water Mirror -- on a calm-water still, gives the flat water a
reflection it never had: whatever stands near the waterline (mast, hull, a
gunwale) mirrored below it in pale, horizontally rippled ink, with the
ripple decaying to near-glass across the shot so you watch the water go
still while you look at it. "There was a great calm" is a positive
statement (the sea gives the world back), not just an absence of storm.

$0, deterministic: numpy hue-band water mask + cv2 Sobel (horizon find) +
cv2.remap (ripple) + PIL compositing + ffmpeg encode for the --demo mode.

CRITICAL GUARDRAIL -- READ BEFORE USE:
This project has a hard-won, previously-caught defect class: a reflected
cross/Christ figure rendered UPSIDE DOWN reads as a real doctrinal/visual
error (memory: feedback-cross-in-water-inverted). This module is FAIL-CLOSED
by default: `include_figure_region=False` (the default) only ever mirrors a
narrow band immediately above the horizon line -- waves, a hull, a mast --
never the taller region where a standing figure's head and torso would be.
Setting `include_figure_region=True` opts into a taller source band that
COULD include a standing figure and MUST be eye-checked, frame by frame,
before it ships. There is no segmentation here (no person-detector) -- the
narrow-band default is the actual safety mechanism, not a formality on top
of a smarter check. See the Guardrails section in
`.claude/skills/still-water-mirror/SKILL.md` before changing the defaults.

Usage:
    python still_water_mirror.py --demo --still still.png --out demo.mp4
        [--duration 8] [--horizon-y 950] [--decay-tau 4.0] [--alpha 0.25]
        [--include-figure-region]
"""
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import warnings
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

FPS = 30

# Source band (above the horizon) as a fraction of frame height.
# Default is intentionally NARROW -- see the module docstring guardrail.
# This narrow band is what keeps a standing figure out of the reflection
# by construction, not a separate smarter check.
BAND_FRAC_WATER_ONLY = 0.20      # include_figure_region=False (default)
BAND_FRAC_WITH_FIGURE = 0.45     # include_figure_region=True (opt-in only)

SQUASH_FRAC = 0.45               # mirrored band squashed to this fraction of its own height
TINT_STRENGTH = 0.35             # blend toward sampled water colour
AMP0_FRAC = 0.010                # ripple amplitude at t=0, as a fraction of frame width
WAVELENGTH_FRAC = 0.037          # ripple wavelength, as a fraction of frame width
PHASE_HZ = 0.6                   # ripple undulation speed


def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def detect_horizon(frame: Image.Image) -> int:
    """Best-effort horizon-row finder.

    Sobel-y row-energy profile (strongest long horizontal edge), searched
    ONLY in the lower half of the frame -- this project's calm-water spreads
    put the sea/sky line there, not in the top half of a 9:16 composition.

    This is a heuristic over a painted/inked still, not a real horizon
    detector -- TESTED on this project's own s11_exactly.png and confirmed
    UNRELIABLE: the strongest lower-half edge is often the boat hull/its own
    painted reflection (higher-contrast ink line) rather than the soft
    watercolor sea/sky line, and a torn-paper deckle edge near the very
    bottom of the frame can out-score both. The bottom margin is excluded
    below for exactly that reason, but this does not fix the hull/reflection
    confusion. ALWAYS eye-check the returned row against the actual still
    (does it sit on the sea line, not floating in cloud, not cutting through
    a boat hull or its reflection?) before trusting it -- pass `--horizon-y`
    explicitly once you've confirmed the right row instead of relying on
    this every time. See the Locked lessons in
    `.claude/skills/still-water-mirror/SKILL.md`.
    """
    gray = np.array(frame.convert("L")).astype(np.float32)
    h, _w = gray.shape
    sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
    row_energy = np.mean(np.abs(sobel_y), axis=1)
    bottom_margin = int(0.08 * h)  # exclude the torn-paper/deckle zone near the page edge
    row_energy[: h // 2] = -1.0
    row_energy[h - bottom_margin :] = -1.0
    return int(np.argmax(row_energy))


def _sample_water_color(arr: np.ndarray, horizon_y: int, sample_h: int = 40) -> np.ndarray:
    h = arr.shape[0]
    sample_h = max(1, min(sample_h, h - horizon_y - 1))
    if sample_h <= 0:
        return np.array([150.0, 160.0, 170.0])
    patch = arr[horizon_y : horizon_y + sample_h, :, :]
    return patch.reshape(-1, 3).mean(axis=0)


def _water_hue_mask(dest_region_rgb: np.ndarray, water_color: np.ndarray) -> np.ndarray:
    """Per-pixel mask of how 'water-like' each destination pixel already is,
    via an HSV hue-band around the sampled water colour. Keeps the
    reflection clipped to the actual painted water and off the kraft-paper
    deckle border that runs down the sides of these stills."""
    hsv = cv2.cvtColor(dest_region_rgb.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    water_hsv = cv2.cvtColor(np.uint8([[np.clip(water_color, 0, 255)]]), cv2.COLOR_RGB2HSV)[0, 0].astype(np.float32)
    hue_diff = np.abs(hsv[..., 0] - water_hsv[0])
    hue_diff = np.minimum(hue_diff, 180.0 - hue_diff)
    mask = ((hue_diff < 30.0) & (hsv[..., 1] > 12.0)).astype(np.float32)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    return mask


def _warn_if_figure_like(region_rgb: np.ndarray) -> None:
    """Advisory-only heuristic: flags likely skin-tone content inside the
    default (water-only) source band. Does NOT block the render -- the
    narrow band is the real guardrail -- this just makes sure a human looks
    at this specific still's reflection before it ships, since a boat gunwale
    can still have a rower's hand/forearm dip into the band."""
    if region_rgb.size == 0:
        return
    hsv = cv2.cvtColor(region_rgb.astype(np.uint8), cv2.COLOR_RGB2HSV)
    lower = np.array([0, 20, 70])
    upper = np.array([25, 150, 255])
    mask = cv2.inRange(hsv, lower, upper)
    frac = float(mask.mean()) / 255.0
    if frac > 0.06:
        warnings.warn(
            "[still_water_mirror] possible figure/skin-tone content detected in the "
            f"reflected band ({frac:.0%} of band pixels) even with include_figure_region=False. "
            "EYE-CHECK this still's rendered reflection before shipping -- a reflected human "
            "figure must render UPRIGHT, never inverted (feedback-cross-in-water-inverted)."
        )


def apply_still_water_mirror(
    frame: Image.Image,
    horizon_y: int,
    t: float,
    decay_tau: float = 4.0,
    alpha: float = 0.25,
    include_figure_region: bool = False,
) -> Image.Image:
    """Composite a decaying, rippled reflection below `horizon_y` onto `frame`.

    Fail-closed by construction: `include_figure_region=False` (default)
    only ever samples a narrow band immediately above the horizon (waves,
    hull, mast). Passing `include_figure_region=True` widens that band to
    where a standing figure could be -- every use of that flag MUST be
    eye-checked frame-by-frame before shipping. See the module docstring.
    """
    orig_mode = frame.mode
    rgb = frame.convert("RGB")
    arr = np.array(rgb).astype(np.float32)
    h, w = arr.shape[:2]
    horizon_y = int(np.clip(horizon_y, 0, h - 1))

    if include_figure_region:
        warnings.warn(
            "[still_water_mirror] include_figure_region=True: sampling a TALL region above "
            "the horizon that may include a standing figure. This is an explicit opt-in, not "
            "the default -- you MUST eye-check every frame of the rendered reflection before "
            "this ships. A standing Christ/human figure must reflect UPRIGHT, never inverted "
            "(feedback-cross-in-water-inverted). If in doubt, do not use this flag."
        )
        band_frac = BAND_FRAC_WITH_FIGURE
    else:
        band_frac = BAND_FRAC_WATER_ONLY

    band_h = max(4, int(round(band_frac * h)))
    src_top = max(0, horizon_y - band_h)
    source = arr[src_top:horizon_y, :, :]

    if source.shape[0] < 4 or horizon_y >= h - 2:
        # Nothing sensible to reflect (horizon at the very top/bottom edge) --
        # degrade gracefully to the untouched frame rather than guess.
        return frame.copy()

    if not include_figure_region:
        _warn_if_figure_like(source)

    # 1. Mirror vertically (flip the band so what was nearest the horizon
    #    stays nearest the horizon in the reflection -- keeps any upright
    #    element, e.g. a mast, upright-in-mirror rather than inverted-twice).
    mirrored = source[::-1, :, :]

    # 2. Squash vertically -- a reflection is compressed by the water's
    #    surface geometry, never a 1:1 mirror.
    squash_h = max(3, int(round(mirrored.shape[0] * SQUASH_FRAC)))
    mirrored_img = Image.fromarray(np.clip(mirrored, 0, 255).astype(np.uint8)).resize((w, squash_h), Image.LANCZOS)
    mirrored_arr = np.array(mirrored_img).astype(np.float32)

    # 3. Tint toward the water's own sampled colour.
    water_color = _sample_water_color(arr, horizon_y)
    mirrored_arr = mirrored_arr * (1 - TINT_STRENGTH) + water_color * TINT_STRENGTH

    # 4. Horizontal sinusoidal ripple via cv2.remap; amplitude decays
    #    exponentially over the spread -- this is the "watch it go still"
    #    beat. Wavelength/amplitude scale with frame width so the same
    #    call reads consistently at any still resolution.
    mh, mw = mirrored_arr.shape[:2]
    amp0 = AMP0_FRAC * w
    amp = amp0 * math.exp(-t / max(decay_tau, 1e-6))
    wavelength_px = max(4.0, WAVELENGTH_FRAC * w)
    phase = t * 2 * math.pi * PHASE_HZ

    map_x, map_y = np.meshgrid(np.arange(mw, dtype=np.float32), np.arange(mh, dtype=np.float32))
    disp = amp * np.sin(2 * math.pi * (map_y / wavelength_px) + phase)
    map_x_r = map_x + disp
    rippled = cv2.remap(
        mirrored_arr.astype(np.float32), map_x_r, map_y,
        interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT,
    )

    # 5. Alpha: base alpha, gently higher (more visible/agitated) early and
    #    settling toward a calmer floor as the ripple itself decays, then
    #    feathered per-pixel: fade IN sharply right at the horizon line so
    #    there's no hard seam, fade OUT toward the bottom of the reflected
    #    band (i.e. toward the bottom of the frame direction), and clipped
    #    to a hue-band water mask so it never paints over the paper border.
    alpha_now = alpha * (0.6 + 0.4 * math.exp(-t / max(decay_tau, 1e-6)))

    dest_top = horizon_y
    dest_bottom = min(h, horizon_y + mh)
    region_h = dest_bottom - dest_top
    if region_h <= 0:
        return frame.copy()

    ys = np.arange(region_h, dtype=np.float32)
    feather_in = np.clip(ys / 6.0, 0.0, 1.0)                       # 0 -> 1 over ~6px at the horizon
    feather_out = 0.30 + 0.70 * np.clip(1.0 - ys / max(region_h, 1), 0.0, 1.0)  # fades toward band bottom
    row_profile = (alpha_now * feather_in * feather_out)[:, None]

    dest_region = arr[dest_top:dest_bottom, :, :]
    water_mask = _water_hue_mask(dest_region, water_color)          # (region_h, w)

    alpha_map = row_profile * water_mask                             # (region_h, w)
    alpha_map = alpha_map[:, :, None]

    comp_src = rippled[:region_h]

    out = arr.copy()
    out[dest_top:dest_bottom] = dest_region * (1 - alpha_map) + comp_src * alpha_map
    out = np.clip(out, 0, 255).astype(np.uint8)
    result = Image.fromarray(out, "RGB")

    if orig_mode == "RGBA":
        result = result.convert("RGBA")
        result.putalpha(frame.split()[-1])
    elif orig_mode != "RGB":
        result = result.convert(orig_mode)

    return result


def render_demo(still: Path, out_mp4: Path, duration: float, horizon_y, decay_tau: float,
                 alpha: float, include_figure_region: bool):
    im = Image.open(still).convert("RGB")
    im = scale_crop(im, 1080, 1920)

    if horizon_y is None:
        horizon_y = detect_horizon(im)
        print(f"[detect_horizon] no --horizon-y given; heuristic picked row {horizon_y} "
              f"of {im.height} -- EYE-CHECK this against the still before trusting it.")
    else:
        print(f"[still_water_mirror] using explicit horizon_y={horizon_y}")

    work = out_mp4.parent / (out_mp4.stem + "_frames")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(duration * FPS)
    for i in range(n_frames):
        t = i / FPS
        frame = apply_still_water_mirror(
            im, horizon_y, t,
            decay_tau=decay_tau, alpha=alpha, include_figure_region=include_figure_region,
        )
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
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=8.0)
    ap.add_argument("--horizon-y", type=int, default=None, dest="horizon_y",
                     help="known/verified horizon row; falls back to detect_horizon() if omitted")
    ap.add_argument("--decay-tau", type=float, default=4.0, dest="decay_tau")
    ap.add_argument("--alpha", type=float, default=0.25)
    ap.add_argument("--include-figure-region", action="store_true", dest="include_figure_region",
                     help="opt-in: reflect a taller band that may include a standing figure -- "
                          "MUST be eye-checked before shipping, see module docstring")
    args = ap.parse_args()

    if args.demo:
        if not args.still or not args.out:
            ap.error("--demo requires --still and --out")
        render_demo(Path(args.still), Path(args.out), args.duration, args.horizon_y,
                    args.decay_tau, args.alpha, args.include_figure_region)
    else:
        ap.error("no mode selected -- currently only --demo is implemented")
