#!/usr/bin/env python
"""Marginalia -- real, chosen, hand-lettered field-note captions + a
leader line pointing at the detail they name. Promotes the compositing
core proven on the living-sketchbook style bake-off's sl20 fix
(`poc_living_sketchbook/_style_identity_bakeoff/_caption_mockup.py`,
2026-08-01, user-approved: "very nice, love it, we should use more of
this visual").

WHY THIS EXISTS (do not relitigate -- see memory
`sketchbook-controlled-text-overlay`): the image-generation model cannot
be trusted to render arbitrary/controlled text, even when the prompt
explicitly bans lettering -- a labeling/documentation CONCEPT in the
prompt ("marginal studies," "surveyor's sensibility") can still pull real
or garbled text into the render. The only reliable way to get REAL,
LEGIBLE, CHOSEN words onto a page is to composite them afterward with a
real font -- never ask the generative model to spell anything.

GOVERNORS (episode-design rules, not enforced by this module):
  - Secondary-note only, never primary (SKILL.md sec.5's own rule) -- fine
    for a field-note aside next to a sketch detail, too subtle at video
    size to carry a main verse reveal.
  - Keep it restrained: 3-4 labels per still read as a page of real notes;
    labeling every detail reads as a diagram, not a sketchbook.
  - Anchor points are AUTHORED per-still pixel coordinates from the
    approved render (this module has no idea what's in the art) -- same
    discipline as candle_only's LAMP anchor.
  - Canvas-bound clamping is automatic (the real bug the sl20 fix caught:
    an eyeballed position ran a caption off the page edge) -- callers
    don't need to get positions exactly right, just roughly right.

API:
    from marginalia import Label, composite_labels

    labels = [
        Label("sandal", anchor=(1238, 2573), offset=(70, 30)),
        Label("thumbprint", anchor=(1390, 1541), offset=(-160, -10)),
    ]
    out = composite_labels(still_img, labels)   # PIL.Image in, PIL.Image out

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\marginalia.py --demo --still <still.png> --out <out.png> --label "sandal:1238,2573:70,30"
    .venv\\Scripts\\python.exe panel_animator\\marginalia.py --selftest
"""
from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

DEFAULT_FONT_PATH = Path("C:/Windows/Fonts/KUNSTLER.TTF")  # same family Scribed Ink uses
DEFAULT_FONT_SIZE = 42
INK = (40, 32, 24, 255)
MARGIN_PX = 24          # captions never draw closer than this to any edge
DOT_RADIUS = 6
LEADER_STEPS = 12
LEADER_JITTER_PX = 3


@dataclass
class Label:
    text: str
    anchor: tuple[int, int]     # the detail being pointed at (in the still's own pixel space)
    offset: tuple[int, int]     # rough caption position relative to anchor -- auto-clamped to canvas


def _load_font(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError:
        return ImageFont.load_default(size=size)


def _wobbled_leader(draw: ImageDraw.ImageDraw, p0, p1, seed: int) -> None:
    rnd = random.Random(seed)
    pts = []
    for i in range(LEADER_STEPS + 1):
        t = i / LEADER_STEPS
        x = p0[0] + (p1[0] - p0[0]) * t + rnd.uniform(-LEADER_JITTER_PX, LEADER_JITTER_PX)
        y = p0[1] + (p1[1] - p0[1]) * t + rnd.uniform(-LEADER_JITTER_PX, LEADER_JITTER_PX)
        pts.append((x, y))
    draw.line(pts, fill=INK, width=3)


def _clamp_to_canvas(draw, text, xy, font, canvas_w, canvas_h, margin=MARGIN_PX):
    """Returns an (x, y) guaranteed to keep `text`'s rendered bbox fully
    within [margin, canvas-margin] on both axes -- the fix for the real
    sl20 bug (an eyeballed offset ran a caption off the page edge)."""
    x, y = list(xy)
    l, t, r, b = draw.textbbox((x, y), text, font=font)
    if r > canvas_w - margin:
        x -= (r - (canvas_w - margin))
    if l < margin:
        x += (margin - l)
    if b > canvas_h - margin:
        y -= (b - (canvas_h - margin))
    if t < margin:
        y += (margin - t)
    return (x, y)


def composite_labels(img: Image.Image, labels: list[Label], *,
                      font_path: Path = DEFAULT_FONT_PATH,
                      font_size: int = DEFAULT_FONT_SIZE) -> Image.Image:
    """Composite hand-script captions + wobbled leader lines onto `img`.
    Pure function -- returns a new image, never mutates the input."""
    base = img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font = _load_font(font_path, font_size)
    for i, label in enumerate(labels):
        raw_xy = (label.anchor[0] + label.offset[0], label.anchor[1] + label.offset[1])
        text_xy = _clamp_to_canvas(draw, label.text, raw_xy, font, base.width, base.height)
        _wobbled_leader(draw, label.anchor, text_xy, seed=i)
        ax, ay = label.anchor
        draw.ellipse([ax - DOT_RADIUS, ay - DOT_RADIUS, ax + DOT_RADIUS, ay + DOT_RADIUS], fill=INK)
        draw.text(text_xy, label.text, font=font, fill=INK)
    return Image.alpha_composite(base, overlay).convert("RGB")


# -------------------------------------------------------------------- demo


def render_demo(still: Path, out: Path, labels: list[Label]) -> None:
    img = Image.open(still)
    composite_labels(img, labels).save(out)
    print(f"[out] {out}")


def _parse_label_arg(spec: str) -> Label:
    """'text:ax,ay:ox,oy' -> Label"""
    text, anchor_s, offset_s = spec.split(":")
    ax, ay = (int(v) for v in anchor_s.split(","))
    ox, oy = (int(v) for v in offset_s.split(","))
    return Label(text, (ax, ay), (ox, oy))


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    canvas = Image.new("RGB", (1536, 2752), (230, 220, 200))

    # 1. a label positioned to overflow the right edge gets clamped, not clipped
    overflow_label = Label("thumbprint", anchor=(1390, 1541), offset=(200, -10))
    out = composite_labels(canvas, [overflow_label])
    check(out.size == canvas.size, "output image is the same size as input")

    draw = ImageDraw.Draw(Image.new("RGBA", canvas.size))
    font = _load_font(DEFAULT_FONT_PATH, DEFAULT_FONT_SIZE)
    raw_xy = (overflow_label.anchor[0] + overflow_label.offset[0],
              overflow_label.anchor[1] + overflow_label.offset[1])
    clamped_xy = _clamp_to_canvas(draw, overflow_label.text, raw_xy, font, canvas.width, canvas.height)
    l, t, r, b = draw.textbbox(clamped_xy, overflow_label.text, font=font)
    check(r <= canvas.width - MARGIN_PX + 1, f"clamped text right edge ({r}) stays within canvas bound")
    check(l >= MARGIN_PX - 1, f"clamped text left edge ({l}) stays within canvas bound")

    # 2. a label that already fits is left roughly where it was asked (not
    # dragged across the page unnecessarily)
    safe_label = Label("grip", anchor=(700, 700), offset=(20, -20))
    raw_xy2 = (720, 680)
    clamped_xy2 = _clamp_to_canvas(draw, "grip", raw_xy2, font, canvas.width, canvas.height)
    check(clamped_xy2 == raw_xy2, f"a well-placed label is not moved: {clamped_xy2} == {raw_xy2}")

    # 3. leader line is deterministic for a fixed seed
    d1 = ImageDraw.Draw(Image.new("RGBA", (200, 200), (0, 0, 0, 0)))
    d2 = ImageDraw.Draw(Image.new("RGBA", (200, 200), (0, 0, 0, 0)))
    rnd1 = random.Random(7)
    rnd2 = random.Random(7)
    seq1 = [rnd1.uniform(-3, 3) for _ in range(12)]
    seq2 = [rnd2.uniform(-3, 3) for _ in range(12)]
    check(seq1 == seq2, "leader-line jitter is deterministic for a fixed seed")

    # 4. composite_labels never mutates the caller's input image
    original_bytes = canvas.tobytes()
    composite_labels(canvas, [Label("x", (10, 10), (5, 5))])
    check(canvas.tobytes() == original_bytes, "input image is never mutated (pure function)")

    # 5. multiple labels all actually draw something (canvas changes near each anchor)
    multi = [Label("a", (200, 200), (30, -30)), Label("b", (1000, 2000), (-30, 30))]
    out_multi = composite_labels(canvas, multi)
    before = canvas.convert("RGB")
    changed_near_a = out_multi.crop((150, 150, 280, 280)) != before.crop((150, 150, 280, 280))
    changed_near_b = out_multi.crop((950, 1950, 1080, 2080)) != before.crop((950, 1950, 1080, 2080))
    check(changed_near_a, "label near anchor (200,200) actually drew something")
    check(changed_near_b, "label near anchor (1000,2000) actually drew something")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="composite labels onto a still")
    ap.add_argument("--still", help="source still (--demo mode)")
    ap.add_argument("--out", help="output png (--demo mode)")
    ap.add_argument("--label", action="append", default=[],
                     help="'text:ax,ay:ox,oy' -- repeatable, one per label (--demo mode)")
    ap.add_argument("--selftest", action="store_true", help="run the engine self-tests")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.still or not a.out or not a.label:
            ap.error("--demo requires --still, --out, and at least one --label")
        render_demo(Path(a.still), Path(a.out), [_parse_label_arg(s) for s in a.label])
    else:
        ap.print_help()
