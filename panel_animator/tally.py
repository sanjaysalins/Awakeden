#!/usr/bin/env python
"""Tally -- the exact-count device (Round 9 build,
`poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` sec. B2).

The gap this closes: round 8 proved, three separate times (14 tally strokes
rendered as ~15-16; 30 coins rendered as 50 until reframed as "three rows of
ten"; 7 seals rendered as 5, twice), that a generative image model cannot be
trusted to render a Scripture-stated DISCRETE count. `measuring_reed.py`
already enforces this same doctrine for CONTINUOUS magnitudes (a span, a
height) -- draw the line and ticks deterministically, let the model draw
only the page around it. This module is that same doctrine for COUNTED
OBJECTS.

DISCIPLINE (load-bearing, same as measuring_reed): this module does not know
or check Scripture -- the CALLER is responsible for only ever invoking it
with a verse-stated `n`, and for picking a `region` that is blank open paper
the still was prompted to leave empty (never drawn over the illustration
itself).

$0, deterministic PIL/numpy. Progressive draw-on reuses the same
staggered-front doctrine as `measuring_reed`'s ticks (each mark's own
position in a SEEDED draw order determines when it appears; an
already-drawn mark never moves or re-jitters between frames -- only the
frontier extends). The numeral+unit label is `measuring_reed`'s own
`_scribed_ink_label`, PORTED verbatim (copied, not imported, the same way
measuring_reed itself ported it from `poc_living_sketchbook/storm/
_s4_assemble.py` -- same punctuation-glyph fix, same sentence-case rule, so
this stays a standalone panel_animator module with no import coupling to
its cousin).

GOVERNOR (hard, not a suggestion): `layout="individual"` for `n > 7` is a
caller error this module refuses (raises `ValueError`), never silently
renders -- round 8's evidence is that ungrouped counts above single digits
are simply not reliable, full stop, regardless of prompt wording.

Layout tiers:
  - "individual" (n <= ~7): loose natural scatter, seeded jitter on
    position/size -- small counts survive ONLY when NOT forced into a grid.
  - "rows" (~8 <= n <= ~60): grouped into rows/bundles (e.g. 3 rows of 10) --
    the ONLY framing round 8 found actually works above a handful.
  - "representative" (n > ~60): draws a believable partial field (a few
    legible rows) plus an explicit hand-drawn "...and more" trailing mark,
    and REFUSES to literally emit n discrete marks past that ceiling -- not
    a workaround, the correct reading (round 8's Witness Roll: "too many to
    name" reading as overwhelming IS 1 Cor 15:6's own rhetorical point).

Usage (library):
    from tally import apply_tally
    frame = apply_tally(frame, region=(x0, y0, x1, y1), n=30, progress=0.7,
                         mark_kind="coin", layout="rows", seed=17,
                         label_text="thirty pieces of silver",
                         ref_text="ZECHARIAH 11:12")

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\tally.py --selftest
    .venv\\Scripts\\python.exe panel_animator\\tally.py --demo --still bg.png --out demo.mp4
        --x0 60 --y0 900 --x1 1020 --y1 1500 --n 30 --mark-kind coin --layout rows
        --label "thirty pieces of silver" --ref "ZECHARIAH 11:12"
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# ported verbatim from measuring_reed.py (which itself ported it from
# _s4_assemble.py's scribed_ink_card()) -- copy the working function, don't
# reinvent the punctuation-glyph fix or the sentence-case rule.
# ---------------------------------------------------------------------------
INK = (35, 30, 26)        # iron-gall ink -- matches measuring_reed.py / _s4_assemble.py
RUBRIC = (150, 26, 22)     # rubric-red reference caps -- matches RUBRIC there

F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"


def _scribed_ink_label(lines: list[str], ref: "str | None", width: int,
                        seed: int = 41) -> Image.Image:
    """Hand-lettered numeral+unit card -- ported verbatim from
    measuring_reed.py's _scribed_ink_label() (itself ported from
    poc_living_sketchbook/storm/_s4_assemble.py's scribed_ink_card()):
    letter-by-letter seeded baseline/rotation wobble, underline swash, small
    rubric-red reference caps, NO box, ever. Kunstler's comma/period glyphs
    are nearly invisible at body size -- drawn from a 1.7x larger stroked
    instance of the same font (same fix as the source, ported not
    rediscovered)."""
    font = ImageFont.truetype(F_KUNSTLER, 48)
    PUNCT = set(".,;:'\u2019\u201c\u201d?")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(48 * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)

    def char_w(ch, f=font):
        return td.textlength(ch, font=f)

    line_h = 62
    canvas = Image.new("RGBA", (width, line_h * len(lines) + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    rng = random.Random(seed)
    y = 10
    last_lw = last_x0 = 0
    for ln in lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (width - tw) / 2
        last_lw, last_x0 = tw, x
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.5, 2.5)
            jr = rng.uniform(-1.2, 1.2)
            draw_font = font_punct if ch in PUNCT else font
            layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.text((10, 10), ch, font=draw_font, fill=(*INK, 255),
                     stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*INK, 255))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + 32))
            canvas.alpha_composite(layer, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)
        y += line_h
    if ref:
        swash = [(last_x0, y - 6)]
        for i in range(1, 9):
            swash.append((last_x0 + last_lw * i / 8, y - 6 + rng.uniform(-3, 3)))
        d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
        rw = d.textlength(ref, font=ref_font)
        d.text(((width - rw) / 2, y + 16), ref, font=ref_font, fill=(*RUBRIC, 235))
        y += 60
    else:
        y += 16
    return canvas.crop((0, 0, width, y))


# ---------------------------------------------------------------------------
# layout constants
# ---------------------------------------------------------------------------
INDIVIDUAL_MAX = 7          # spec: layout="individual" hard-raises above this
REPRESENTATIVE_CAP = 30     # "a few legible rows" -- 3 rows of 10, matching the
                             # rows tier's own "three rows of ten" precedent
TARGET_ROWS = 3              # round 8's own found-good row count

MARKS_DRAW_END = 0.80        # marks finish drawing by this fraction of progress
LABEL_START = 0.90           # numeral+unit label starts fading in
LABEL_END = 1.00
POP_SPAN = 0.08               # fraction of the front's 0..1 domain a mark takes to fade in


def _ease(u: float) -> float:
    """Smoothstep, 0..1 -> 0..1 -- same recipe as measuring_reed.py / tide_mark.py."""
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


# ---------------------------------------------------------------------------
# row-split (the "three rows of ten" precedent, generalized)
# ---------------------------------------------------------------------------
def _rows_split(n: int, target_rows: int = TARGET_ROWS) -> list[int]:
    """Split n marks into target_rows rows, as even as possible, with any
    remainder landing in the LAST row as a partial. n=30 -> [10, 10, 10]
    (round 8's own "three rows of ten"); n=10 -> [4, 4, 2] (3 rows, the last
    one partial) -- the same fixed-row-count, variable-row-width rule for
    every n, not a special case."""
    if n <= 0:
        return []
    rows = max(1, min(target_rows, n))
    per = math.ceil(n / rows)
    counts = []
    remaining = n
    for i in range(rows):
        if i == rows - 1:
            counts.append(remaining)
        else:
            c = min(per, remaining)
            counts.append(c)
            remaining -= c
    return counts


# ---------------------------------------------------------------------------
# mark position builders
# ---------------------------------------------------------------------------
def _scatter_positions(x0: float, y0: float, x1: float, y1: float, n: int, seed: int):
    """Loose natural scatter for the 'individual' tier -- seeded jitter,
    rejection-sampled for breathing room between marks so nothing overlaps
    into an unreadable clump (round 8: small counts read fine ONLY when they
    don't collide)."""
    rng = random.Random(seed)
    w, h = x1 - x0, y1 - y0
    if n <= 0:
        return []
    min_dist = 0.30 * math.sqrt(max(1.0, (w * h) / max(1, n)))
    pts: list[tuple[float, float]] = []
    for _ in range(n):
        cx = cy = 0.0
        for _attempt in range(80):
            cx = x0 + rng.uniform(0.10, 0.90) * w
            cy = y0 + rng.uniform(0.15, 0.85) * h
            if all(math.hypot(cx - px, cy - py) >= min_dist for px, py in pts):
                break
        pts.append((cx, cy))
    return pts


def _grid_positions(x0: float, y0: float, x1: float, y1: float, n: int, seed: int):
    """Regular row/bundle grid for the 'rows' (and representative-cap) tier
    -- fairly REGULAR alignment on purpose (only a tiny jitter), unlike
    individual's loose scatter: round 8 found irregular arrangement was
    itself part of what made large counts misread."""
    rows = _rows_split(n)
    rng = random.Random(seed)
    w, h = x1 - x0, y1 - y0
    n_rows = len(rows)
    pts: list[tuple[float, float]] = []
    for ri, count in enumerate(rows):
        if count <= 0:
            continue
        row_cy = y0 + (ri + 0.5) / n_rows * h
        for ci in range(count):
            row_cx = x0 + (ci + 0.5) / count * w
            jx = rng.uniform(-0.012, 0.012) * w
            jy = rng.uniform(-0.02, 0.02) * h
            pts.append((row_cx + jx, row_cy + jy))
    return pts


def _tally_bundle_positions(x0: float, y0: float, x1: float, y1: float, n: int, seed: int):
    """Hand-tally strokes: bundles of 5 (4 verticals + a diagonal 5th strike
    across them), laid out row by row (same TARGET_ROWS convention as the
    grid tier) so a large count still stays legible; a bundle is always kept
    together on one row, never split across a row wrap. Returns mark dicts
    (not bare points) since strike marks need their bundle's x-span, not a
    single point."""
    if n <= 0:
        return []
    rng = random.Random(seed)
    w, h = x1 - x0, y1 - y0
    n_bundles = math.ceil(n / 5)
    rows_of_bundles = _rows_split(n_bundles)
    n_rows = len(rows_of_bundles)
    marks = []
    remaining = n
    for ri, b_count in enumerate(rows_of_bundles):
        if b_count <= 0:
            continue
        row_cy = y0 + (ri + 0.5) / n_rows * h
        bundle_w = w / b_count
        for bi in range(b_count):
            if remaining <= 0:
                break
            strokes_here = min(5, remaining)
            bx0 = x0 + bi * bundle_w + bundle_w * 0.14
            bx1 = x0 + bi * bundle_w + bundle_w * 0.86
            n_verts = min(4, strokes_here)
            vert_xs = [bx0 + (bx1 - bx0) * (vi / 3.0 if n_verts > 1 else 0.5)
                       for vi in range(n_verts)]
            for vx in vert_xs:
                jx = rng.uniform(-1, 1) * bundle_w * 0.01
                marks.append({"cx": vx + jx, "cy": row_cy, "glyph": "vert"})
            remaining -= n_verts
            if strokes_here == 5 and remaining > 0:
                marks.append({"cx": (bx0 + bx1) / 2, "cy": row_cy, "glyph": "strike",
                              "x0": bx0, "x1": bx1})
                remaining -= 1
    return marks


def _build_marks(region, n: int, layout: str, seed: int, mark_kind) -> list[dict]:
    """Build the full mark list (position + glyph) for one call's true `n`
    and layout tier -- the hard governor (individual, n>7 raises) lives
    here, checked BEFORE any drawing happens."""
    if layout == "individual" and n > INDIVIDUAL_MAX:
        raise ValueError(
            f"layout='individual' only supports n<=<{INDIVIDUAL_MAX + 1} "
            f"(round 8's own evidence: ungrouped counts above a handful are "
            f"not reliable, full stop); got n={n}. Use layout='rows' "
            f"(n<=~60) or layout='representative' (n>~60) instead."
        )
    if layout not in ("individual", "rows", "representative"):
        raise ValueError(f"unknown layout {layout!r}")

    x0, y0, x1, y1 = region
    represented_n = min(n, REPRESENTATIVE_CAP) if layout == "representative" else n

    if mark_kind == "tally":
        return _tally_bundle_positions(x0, y0, x1, y1, represented_n, seed)

    if layout == "individual":
        pts = _scatter_positions(x0, y0, x1, y1, represented_n, seed)
    else:
        pts = _grid_positions(x0, y0, x1, y1, represented_n, seed)
    return [{"cx": cx, "cy": cy, "glyph": mark_kind} for cx, cy in pts]


def _assign_reveal_fracs(marks: list[dict], seed: int, sequential: bool) -> list[dict]:
    """Assign each mark a `frac` (0..1) -- its position in the draw-front's
    domain. Tally strokes reveal SEQUENTIALLY (you count 1, 2, 3, 4,
    5-with-strike, 6... in real order; a shuffled tally is not a tally).
    Every other mark kind reveals in a SEEDED, non-raster order (never
    left-right/top-bottom) -- the doctrine this module inherits from
    measuring_reed's tick front, applied to discrete scattered/gridded
    objects instead of a continuous line."""
    n = len(marks)
    if n == 0:
        return marks
    order = list(range(n))
    if not sequential:
        random.Random(seed + 5000).shuffle(order)
    for reveal_i, mark_i in enumerate(order):
        marks[mark_i]["frac"] = (reveal_i + 1) / n
    return marks


def _mark_alpha(mark: dict, progress: float) -> int:
    """0..255 opacity for one mark at a given overall progress -- a pure
    function of (mark['frac'], progress): an already-drawn mark's alpha
    never decreases as progress increases (draw-front never regresses)."""
    front = _ease(min(1.0, progress / MARKS_DRAW_END)) if MARKS_DRAW_END > 0 else 1.0
    t = (front - (mark["frac"] - POP_SPAN)) / POP_SPAN
    return int(255 * _ease(max(0.0, min(1.0, t))))


# ---------------------------------------------------------------------------
# glyph rendering
# ---------------------------------------------------------------------------
def _draw_coin(d: "ImageDraw.ImageDraw", cx: float, cy: float, size: float, alpha: int) -> None:
    r = size
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*INK, alpha), width=max(2, int(r * 0.20)))
    d.arc([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], 200, 340,
          fill=(*INK, int(alpha * 0.7)), width=1)


def _draw_dot(d: "ImageDraw.ImageDraw", cx: float, cy: float, size: float, alpha: int) -> None:
    r = size * 0.62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*INK, alpha))


def _draw_head_mark(d: "ImageDraw.ImageDraw", cx: float, cy: float, size: float, alpha: int) -> None:
    r = size
    d.ellipse([cx - r * 0.55, cy - r * 0.9, cx + r * 0.55, cy + r * 0.15], fill=(*INK, alpha))
    d.pieslice([cx - r, cy - r * 0.05, cx + r, cy + r * 1.6], 180, 360, fill=(*INK, alpha))


def _draw_tally(d: "ImageDraw.ImageDraw", mark: dict, size: float, alpha: int) -> None:
    w_ = max(2, int(size * 0.24))
    if mark["glyph"] == "strike":
        y = mark["cy"]
        d.line([(mark["x0"], y - size * 0.85), (mark["x1"], y + size * 0.85)],
               fill=(*INK, alpha), width=w_)
    else:
        cx = mark["cx"]
        d.line([(cx, mark["cy"] - size), (cx, mark["cy"] + size)], fill=(*INK, alpha), width=w_)


def _draw_mark(d: "ImageDraw.ImageDraw", mark: dict, size: float, alpha: int,
               mark_kind) -> None:
    if callable(mark_kind):
        mark_kind(d, mark["cx"], mark["cy"], size, alpha)
        return
    if mark_kind == "coin":
        _draw_coin(d, mark["cx"], mark["cy"], size, alpha)
    elif mark_kind == "dot":
        _draw_dot(d, mark["cx"], mark["cy"], size, alpha)
    elif mark_kind == "head_mark":
        _draw_head_mark(d, mark["cx"], mark["cy"], size, alpha)
    elif mark_kind == "tally":
        _draw_tally(d, mark, size, alpha)
    else:
        raise ValueError(f"unknown mark_kind {mark_kind!r}")


# ---------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------
def apply_tally(frame: Image.Image, region, n: int, progress: float,
                 mark_kind="dot", layout: str = "rows", seed: int = 17,
                 label_text=None, ref_text: "str | None" = None,
                 label_side: str = "below") -> Image.Image:
    """Apply Tally to an already-composited RGB(A) frame.

    region: x0,y0,x1,y1 pixel box of the blank-paper reservation the STILL
        was prompted to leave open. Never draws over existing linework --
        pick a region that is clear open paper, same discipline as
        measuring_reed.
    n: the verbatim Scripture-stated count. This module does not know or
        check Scripture -- the caller is responsible for only ever passing a
        verse-stated n.
    progress: 0..1, drives the whole reveal -- 0 = untouched frame, ~0.80 =
        every mark fully drawn, 0.90-1.00 = the label fades in.
    mark_kind: "tally" (bundled hand-tally strokes, 4 verticals + a diagonal
        5th strike), "coin", "dot", "head_mark", or a caller-supplied
        callable(draw, cx, cy, size, alpha) -> None.
    layout: "individual" (n<=7, loose scatter -- RAISES ValueError above 7),
        "rows" (~8<=n<=~60, grouped rows/bundles), "representative" (n>~60,
        draws a capped representative field + an "...and more" trailing
        mark, never n literal marks).
    seed: draw-order + jitter seed. Same seed -> byte-identical marks.
    label_text/ref_text: the numeral+unit line(s) (e.g. "thirty pieces of
        silver") and an optional citation caps line (e.g. "ZECHARIAH
        11:12"), in Scribed Ink -- reuses measuring_reed's own
        _scribed_ink_label. Omit label_text for no label.
    label_side: "above" or "below" the region -- pick whichever side has
        clear paper for the card to land on.
    """
    progress = max(0.0, min(1.0, progress))
    marks = _build_marks(region, n, layout, seed, mark_kind)
    sequential = mark_kind == "tally"
    marks = _assign_reveal_fracs(marks, seed, sequential)

    x0, y0, x1, y1 = region
    W_, H_ = frame.size
    scale = W_ / 1080.0
    src_mode = frame.mode
    out = frame.convert("RGBA")
    overlay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    mark_size = max(6.0, min(x1 - x0, y1 - y0) / 22.0) * (1.0 if scale <= 0 else scale)
    for m in marks:
        alpha = _mark_alpha(m, progress)
        if alpha <= 0:
            continue
        _draw_mark(d, m, mark_size, alpha, mark_kind)

    out = Image.alpha_composite(out, overlay)

    # -- the numeral+unit label, Scribed Ink, fading in once the field
    # finishes drawing (same 0.90-1.00 window as measuring_reed)
    if label_text and progress >= LABEL_START:
        label_fade = _ease((progress - LABEL_START) / max(1e-6, LABEL_END - LABEL_START))
        if label_fade > 0.0:
            lines = [label_text] if isinstance(label_text, str) else list(label_text)
            card = _scribed_ink_label(lines, ref_text, width=W_, seed=seed + 900)
            if label_fade < 1.0:
                a = card.split()[3].point(lambda v: int(v * label_fade))
                card.putalpha(a)
            cx = int((x0 + x1) / 2 - card.width / 2)
            cx = max(10, min(W_ - card.width - 10, cx))
            margin = int(40 * scale)
            top_y = (max(y0, y1) + margin) if label_side == "below" else (min(y0, y1) - card.height - margin)
            cy = max(10, min(H_ - card.height - 10, int(top_y)))
            layer = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            layer.alpha_composite(card, (cx, cy))
            out = Image.alpha_composite(out, layer)

    # -- representative tier only: the honest "...and more" trailing mark,
    # never a silent truncation
    if layout == "representative" and progress >= LABEL_START:
        more_fade = _ease((progress - LABEL_START) / max(1e-6, LABEL_END - LABEL_START))
        if more_fade > 0.0:
            more_card = _scribed_ink_label(["...and more"], None, width=W_, seed=seed + 950)
            if more_fade < 1.0:
                a = more_card.split()[3].point(lambda v: int(v * more_fade))
                more_card.putalpha(a)
            mcx = int((x0 + x1) / 2 - more_card.width / 2)
            mcx = max(10, min(W_ - more_card.width - 10, mcx))
            mcy = int(max(y0, y1) + 6 * scale)
            mcy = max(10, min(H_ - more_card.height - 10, mcy))
            layer = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            layer.alpha_composite(more_card, (mcx, mcy))
            out = Image.alpha_composite(out, layer)

    return out if src_mode == "RGBA" else out.convert(src_mode)


# ---------------------------------------------------------------------------
# demo CLI
# ---------------------------------------------------------------------------
def scale_crop(im: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render_demo(still: "Path | None", out_mp4: Path, duration: float, fps: int, seed: int,
                 x0: float, y0: float, x1: float, y1: float, n: int, mark_kind: str,
                 layout: str, label: "str | None", ref: "str | None"):
    if still is not None:
        im = scale_crop(Image.open(still).convert("RGB"), 1080, 1920)
    else:
        im = Image.new("RGB", (1080, 1920), (232, 221, 194))

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(round(duration * fps))
    pre_hold = int(0.3 * fps)
    post_hold = int(0.6 * fps)
    reveal_frames = max(1, n_frames - pre_hold - post_hold)
    for i in range(n_frames):
        if i < pre_hold:
            progress = 0.0
        elif i >= pre_hold + reveal_frames:
            progress = 1.0
        else:
            progress = (i - pre_hold) / (reveal_frames - 1) if reveal_frames > 1 else 1.0
        frame = apply_tally(im, (x0, y0, x1, y1), n, progress, mark_kind=mark_kind,
                             layout=layout, seed=seed, label_text=label, ref_text=ref)
        frame.convert("RGB").save(work / f"f{i:05d}.png")

    subprocess.run(
        ["ffmpeg", "-y", "-framerate", str(fps), "-i", str(work / "f%05d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out_mp4)],
        check=True, capture_output=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {out_mp4}")


# ------------------------------------------------------------------ selftest
def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    region = (60.0, 900.0, 1020.0, 1500.0)
    frame0 = Image.new("RGB", (1080, 1920), (232, 221, 194))

    # 1. drawn-mark count at progress=1.0 == n, for individual and rows
    for layout, n in [("individual", 7), ("rows", 30), ("rows", 10)]:
        marks = _assign_reveal_fracs(_build_marks(region, n, layout, 5, "dot"), 5, False)
        drawn = sum(1 for m in marks if _mark_alpha(m, 1.0) == 255)
        check(drawn == n, f"layout={layout!r} n={n}: {drawn} marks fully drawn at progress=1.0 (want {n})")

    # 2. draw-front never regresses (per-mark alpha is non-decreasing in progress)
    marks = _assign_reveal_fracs(_build_marks(region, 30, "rows", 9, "coin"), 9, False)
    steps = [i / 40 for i in range(41)]
    regressed = False
    for m in marks:
        prev = -1
        for p in steps:
            a = _mark_alpha(m, p)
            if a < prev:
                regressed = True
            prev = a
    check(not regressed, "draw-front never regresses (per-mark alpha non-decreasing across progress)")

    # 3. same seed -> byte-identical marks
    f1 = apply_tally(frame0, region, 20, 0.6, mark_kind="dot", layout="rows", seed=17)
    f2 = apply_tally(frame0, region, 20, 0.6, mark_kind="dot", layout="rows", seed=17)
    check(np.array_equal(np.asarray(f1), np.asarray(f2)), "same seed -> byte-identical render")

    # 4. layout="individual" with n=8 raises
    try:
        _build_marks(region, 8, "individual", 5, "dot")
        check(False, "layout='individual' with n=8 raises ValueError")
    except ValueError:
        check(True, "layout='individual' with n=8 raises ValueError")

    # 5. layout="rows" picks a sane split for n=10 and n=30 (three-rows-of-ten precedent)
    split10 = _rows_split(10)
    split30 = _rows_split(30)
    check(len(split10) == 3 and sum(split10) == 10 and split10[-1] < split10[0],
          f"n=10 -> 3 rows incl. a partial: {split10}")
    check(split30 == [10, 10, 10], f"n=30 -> three rows of ten: {split30}")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a progress 0->1 demo clip")
    ap.add_argument("--still", default=None, help="optional background still (else blank cream)")
    ap.add_argument("--out", help="output mp4")
    ap.add_argument("--duration", type=float, default=5.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--x0", type=float, default=60.0)
    ap.add_argument("--y0", type=float, default=900.0)
    ap.add_argument("--x1", type=float, default=1020.0)
    ap.add_argument("--y1", type=float, default=1500.0)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--mark-kind", default="coin", dest="mark_kind",
                     choices=["coin", "dot", "head_mark", "tally"])
    ap.add_argument("--layout", default="rows", choices=["individual", "rows", "representative"])
    ap.add_argument("--label", default=None)
    ap.add_argument("--ref", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.out:
            ap.error("--demo requires --out")
        render_demo(Path(a.still) if a.still else None, Path(a.out), a.duration, a.fps, a.seed,
                    a.x0, a.y0, a.x1, a.y1, a.n, a.mark_kind, a.layout, a.label, a.ref)
    else:
        ap.error("only --demo/--selftest are implemented from the CLI -- import apply_tally for pipeline use")
