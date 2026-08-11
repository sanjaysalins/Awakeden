"""Relight -- code-only regrading of ONE AI plate into multiple lightings.

Promoted from `poc_bethesda_style_test/round3_devices/build_stills.py`'s
`_radial_vignette()` + `relight_fire()` (proven by eye on real output: the
Same Fire device, one plate -> night/dawn regrade, zero alignment risk).

`relight_radial()` generalizes `relight_fire()`'s two hardcoded branches
(night/dawn) into one function selected by `mode`, reusable for any subject,
not just fire. `relight_split()` is new: a linear left/right split-grade for
stories where two halves of ONE plate carry two different fates (built for
the Two Goats episode, `drawing_office/episodes/two_goats/commission.json`,
device "the_undivided").

No image generation here -- PIL only. $0.
"""
from __future__ import annotations

from PIL import Image, ImageEnhance


# --------------------------------------------------------------------------
# mask generators
# --------------------------------------------------------------------------
def radial_vignette(
    img: Image.Image,
    cx_frac: float,
    cy_frac: float,
    inner_frac: float,
    outer_frac: float,
    dark_to: float = 0.15,
) -> Image.Image:
    """Multiplicative radial mask: 255 (full) near (cx,cy), fading to
    int(255*dark_to) at outer_frac. Same math as build_stills.py's
    `_radial_vignette()`, promoted almost verbatim."""
    w, h = img.size
    cx, cy = w * cx_frac, h * cy_frac
    max_r = (w ** 2 + h ** 2) ** 0.5 / 2
    inner, outer = inner_frac * max_r, outer_frac * max_r
    mask = Image.new("L", (w, h), 0)
    dr = mask.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= inner:
                v = 255
            elif d >= outer:
                v = int(255 * dark_to)
            else:
                t = (d - inner) / max(1e-6, outer - inner)
                v = int(255 * (1 - t * (1 - dark_to)))
            dr[x, y] = v
            if x + 1 < w:
                dr[x + 1, y] = v
            if y + 1 < h:
                dr[x, y + 1] = v
            if x + 1 < w and y + 1 < h:
                dr[x + 1, y + 1] = v
    return mask


def _linear_mask(
    w: int,
    h: int,
    split_x_frac: float,
    feather_px: int,
) -> Image.Image:
    """255 on the left of split_x, 0 on the right, feathered over
    `feather_px` centered on the split line (soft, not a hard cut)."""
    split_x = w * split_x_frac
    mask = Image.new("L", (w, h), 0)
    dr = mask.load()
    half = max(1, feather_px) / 2.0
    for x in range(w):
        if x < split_x - half:
            v = 255
        elif x > split_x + half:
            v = 0
        else:
            t = (x - (split_x - half)) / max(1e-6, 2 * half)
            v = int(255 * (1 - t))
        for y in range(h):
            dr[x, y] = v
    return mask


# --------------------------------------------------------------------------
# color-grade profiles -- the exact shift numbers proven in relight_fire()
# --------------------------------------------------------------------------
def _grade_night(base: Image.Image) -> Image.Image:
    """Cool, desaturated, darkened -- fear closes it down."""
    night = ImageEnhance.Color(base).enhance(0.55)
    night = ImageEnhance.Brightness(night).enhance(0.62)
    night = ImageEnhance.Contrast(night).enhance(1.08)
    r, g, b = night.split()
    b = ImageEnhance.Brightness(b).enhance(1.18)
    r = ImageEnhance.Brightness(r).enhance(0.92)
    return Image.merge("RGB", (r, g, b))


def _grade_dawn(base: Image.Image) -> Image.Image:
    """Warm, saturated, brightened -- grace arrives, opens up."""
    dawn = ImageEnhance.Color(base).enhance(1.12)
    dawn = ImageEnhance.Brightness(dawn).enhance(1.15)
    dawn = ImageEnhance.Contrast(dawn).enhance(1.05)
    r, g, b = dawn.split()
    r = ImageEnhance.Brightness(r).enhance(1.16)
    g = ImageEnhance.Brightness(g).enhance(1.05)
    b = ImageEnhance.Brightness(b).enhance(0.88)
    return Image.merge("RGB", (r, g, b))


# aliases for relight_split's left/right profile names (commission.json
# names these "cool_still" / "warm_departing" -- same underlying grades as
# night/dawn, reused rather than reimplemented).
_GRADE_PROFILES = {
    "night": _grade_night,
    "cool_still": _grade_night,
    "dawn": _grade_dawn,
    "warm_departing": _grade_dawn,
}


def _resolve_grade(mode: str):
    try:
        return _GRADE_PROFILES[mode]
    except KeyError:
        raise ValueError(
            f"unknown relight mode {mode!r} -- valid modes: {sorted(_GRADE_PROFILES)}"
        )


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------
def relight_radial(
    raw: Image.Image,
    mode: str,
    cx_frac: float = 0.5,
    cy_frac: float = 0.5,
) -> Image.Image:
    """Generalized relight_fire(): ONE plate, ONE code-only lighting,
    selected by `mode` ("night" or "dawn" -- same color-shift numbers proven
    on the Same Fire plate, now reusable for any subject, not just fire)."""
    base = raw.convert("RGB")
    grade_fn = _resolve_grade(mode)
    graded = grade_fn(base)

    if mode in ("night", "cool_still"):
        mask = radial_vignette(base, cx_frac, cy_frac, inner_frac=0.10, outer_frac=0.42, dark_to=0.22)
        dark = ImageEnhance.Brightness(graded).enhance(0.35)
    else:  # dawn / warm_departing
        mask = radial_vignette(base, cx_frac, cy_frac, inner_frac=0.35, outer_frac=0.95, dark_to=0.72)
        dark = ImageEnhance.Brightness(graded).enhance(0.8)

    return Image.composite(graded, dark, mask)


def relight_split(
    raw: Image.Image,
    split_x_frac: float,
    left_mode: str,
    right_mode: str,
    blend: float = 0.0,
    feather_px: int = 40,
) -> Image.Image:
    """Linear left/right split-grade of ONE plate: `left_mode`'s color
    profile on the left region, `right_mode`'s on the right, composited
    through a feathered linear mask centered at `split_x_frac * width`.

    `blend` interpolates the WHOLE image from fully-split (blend=0.0, each
    side keeps its own grade) to fully-unified (blend=1.0, one neutral warm
    grade applied everywhere, the mask has no visible effect) -- this is the
    "no single creature could hold both halves" -> unification beat from the
    Two Goats commission (drawing_office/episodes/two_goats/commission.json).
    """
    base = raw.convert("RGB")
    w, h = base.size
    blend = min(1.0, max(0.0, blend))

    left_fn = _resolve_grade(left_mode)
    right_fn = _resolve_grade(right_mode)
    left_graded = left_fn(base)
    right_graded = right_fn(base)

    mask = _linear_mask(w, h, split_x_frac, feather_px)
    split_composite = Image.composite(left_graded, right_graded, mask)

    if blend <= 0.0:
        return split_composite

    # unified grade: warm/dawn profile applied everywhere, no mask.
    unified = _grade_dawn(base)

    if blend >= 1.0:
        return unified

    return Image.blend(split_composite, unified, blend)
