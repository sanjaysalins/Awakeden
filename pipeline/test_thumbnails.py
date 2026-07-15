"""Tests for pipeline/thumbnails.py — deterministic thumbnail-quality logic.

Regressions caught by a 2026-07-15 deep-dive audit (looked at real generated
thumbnails, not just ran the script): migrated hero-frame timestamps landed on
unpainted panel-grid voids after the wave rebuild moved timing (blank_fraction +
grab_frame's auto-avoidance), and long titles ran off the canvas at the fixed
font size (_fit_title_font)."""
from __future__ import annotations

from PIL import Image, ImageDraw

from pipeline.thumbnails import _fit_title_font, blank_fraction


def _flat(w, h, rgb) -> Image.Image:
    return Image.new("RGB", (w, h), rgb)


def _split(w, h, left_rgb, right_rgb, split_frac) -> Image.Image:
    im = Image.new("RGB", (w, h), left_rgb)
    im.paste(Image.new("RGB", (w - int(w * split_frac), h), right_rgb), (int(w * split_frac), 0))
    return im


# ---- blank_fraction -----------------------------------------------------------
def test_fully_flat_bright_frame_is_all_blank():
    # calibrated on a confirmed-bad panel-grid void: bright + zero-variance
    assert blank_fraction(_flat(400, 300, (228, 228, 228))) == 1.0


def test_fully_flat_dark_frame_is_not_blank():
    # a dramatic flat-black backdrop is LEGITIMATE content, not an unpainted void
    assert blank_fraction(_flat(400, 300, (10, 10, 10))) == 0.0


def test_partial_void_scores_partial():
    # right 40% unpainted (light), left 60% "painted" (dark) -> roughly matches
    im = _split(400, 300, (60, 60, 60), (228, 228, 228), 0.6)
    frac = blank_fraction(im)
    assert 0.30 < frac < 0.50


def test_textured_bright_region_is_not_flagged():
    # real linework/shading has local variance even when bright overall
    im = Image.new("RGB", (400, 300), (220, 220, 220))
    dr = ImageDraw.Draw(im)
    for x in range(0, 400, 8):
        dr.line([(x, 0), (x, 300)], fill=(40, 40, 40), width=2)
    assert blank_fraction(im) < 0.12


# ---- _fit_title_font ------------------------------------------------------------
def test_short_title_keeps_start_size():
    im = Image.new("RGB", (1280, 720))
    dr = ImageDraw.Draw(im)
    f = _fit_title_font(dr, ["HI"], 120, max_w=1000)
    assert f.size == 120


def test_long_title_shrinks_to_fit():
    im = Image.new("RGB", (1280, 720))
    dr = ImageDraw.Draw(im)
    long_title = ["THEY SHALL LOOK", "ON HIM"]  # the confirmed-overflowing case
    max_w = 1280 - 2 * int(1280 * 0.055) - int(1280 * 0.16)
    f = _fit_title_font(dr, long_title, 134, max_w)
    assert all(dr.textlength(line, font=f) <= max_w for line in long_title)
    assert f.size < 134


def test_never_shrinks_below_floor():
    im = Image.new("RGB", (1280, 720))
    dr = ImageDraw.Draw(im)
    f = _fit_title_font(dr, ["AN ABSURDLY LONG TITLE THAT COULD NEVER FIT"], 60, max_w=10, min_size=24)
    assert f.size == 24


if __name__ == "__main__":
    import sys

    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
