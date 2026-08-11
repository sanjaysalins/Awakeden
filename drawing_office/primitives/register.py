"""Register -- two-crops-from-one-plate primitive for a future "the_undivided"
-family correspondence device (registration_pull_reborn, considered but not
chosen for Two Goats -- see drawing_office/episodes/two_goats/commission.json
candidate_scoring). Two named regions of ONE plate are pulled out as their
own crops, meant to be animated into alignment downstream (a "these two
things match" proof-text device), never a second generation.

LOWER PRIORITY stub -- built on crop_study.crop_zoom, kept deliberately thin
until a real episode commission needs the correspondence device.
"""
from __future__ import annotations

from PIL import Image

from crop_study import crop_zoom


def register_crops(
    raw: Image.Image,
    box_a_frac: tuple[float, float, float, float],
    box_b_frac: tuple[float, float, float, float],
    out_size: tuple[int, int] | None = None,
) -> tuple[Image.Image, Image.Image]:
    """Pull two named-region crops (box_a_frac, box_b_frac -- each an
    (x0,y0,x1,y1) fraction box) from ONE plate, both resized to the same
    out_size (defaults to raw.size) so a downstream animator can pull them
    into registration against each other."""
    crop_a = crop_zoom(raw, box_a_frac, out_size=out_size)
    crop_b = crop_zoom(raw, box_b_frac, out_size=out_size)
    return crop_a, crop_b
