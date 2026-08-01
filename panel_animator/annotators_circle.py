#!/usr/bin/env python
"""Annotator's Circle -- the hand that marks the Word. When the narration
speaks one word already lettered on the page (a Scribed Ink verse card, or
any other hand-lettered raster), a hand-drawn ink ellipse draws itself
around that word: a full first pass, then a second, lighter, slightly
offset pass -- because a real hand circling something important goes
around twice (`_FABLE_ROUND4_REMOTION_SKILLS.md` sec. 2, "Annotator's
Circle"). Rubric-red by default; gold only for a glory-beat word (Scribe's
Tally's color law, reused -- this module does not decide that, it only
exposes `color` so the caller can pass GOLD).

$0, deterministic PIL: the ellipse path is precomputed once per pass from a
seeded sum of sines perturbing the radius (same family of math as
tide_mark's boundary / wash_creep's front / impact_burst's jagged spikes --
a wobbled-but-fixed shape, seeded, never re-randomized frame to frame), then
progressively revealed by taking a longer prefix of the same point list as
`progress` advances -- the classic two-pass dash-offset draw-on the brief
names, without needing an SVG stack.

Governors (load-bearing, see .claude/skills/annotators-circle/SKILL.md):
at most ONE circle per episode; only on a word already approved verbatim on
the page (KJV or a map label) -- this device can only MARK existing
lettering, never add text; never on the landing spread's set-off (that
register stays quiet by law).

Usage (library, inside an assembly script's per-frame loop):
    from annotators_circle import apply_annotators_circle, RUBRIC, GOLD
    frame = apply_annotators_circle(frame, bbox=(578, 244, 662, 283),
                                     progress=progress, color=RUBRIC)

Usage (demo CLI -- preview the circle animating over a plain still):
    python annotators_circle.py --demo --still still.png --out demo.mp4 \
        --bbox 578,244,662,283 --t0 0.0 --duration 1.4
"""
from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

RUBRIC = (150, 26, 22)   # matches poc_living_sketchbook/storm/_s4_assemble.py's RUBRIC
GOLD = (185, 146, 74)    # matches that file's GOLD -- pass color=GOLD on a glory-beat word

# Two-pass timing: the first, full-weight sweep owns the first PASS1_END of
# the progress window; the second, lighter, offset pass owns the rest --
# "a real hand circling something important goes around twice."
PASS1_END = 0.6
PASS2_START = 0.6

N_POINTS = 181           # samples around one full loop (0..2*pi) -- plenty
                          # smooth for a stroke this size, cheap to slice


def _ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)  # smoothstep


def _wobbled_ellipse_points(cx: float, cy: float, rx: float, ry: float,
                             seed: int, start_angle_deg: float = -100.0,
                             wobble_amp_frac: float = 0.055,
                             n_points: int = N_POINTS) -> list[tuple[float, float]]:
    """One full loop (n_points samples, 0..2*pi) of an ellipse whose radius
    is perturbed by a seeded sum of 3-4 sines (tide_mark's boundary trick,
    ported to an angle instead of an x-position) -- a real hand never draws
    a geometric ellipse, but the WOBBLE ITSELF must be fixed for the whole
    gesture, not re-rolled every frame, or the ink would visibly crawl.
    """
    rng = random.Random(seed)
    n_terms = rng.randint(3, 4)
    freqs = [rng.uniform(1.6, 4.3) for _ in range(n_terms)]
    phases = [rng.uniform(0.0, 2 * math.pi) for _ in range(n_terms)]
    rel_amps = [1.0, 0.55, 0.3, 0.18][:n_terms]
    weights = [ra * rng.uniform(0.8, 1.2) for ra in rel_amps]
    wsum = sum(weights) or 1.0
    weights = [w_ / wsum for w_ in weights]  # bounded roughly to +-1 overall

    start = math.radians(start_angle_deg)
    pts = []
    for i in range(n_points):
        frac = i / (n_points - 1)
        theta = start + frac * 2 * math.pi
        wob = sum(w_ * math.sin(f_ * frac * 2 * math.pi + p_)
                  for w_, f_, p_ in zip(weights, freqs, phases))
        mult = 1.0 + wobble_amp_frac * wob
        pts.append((cx + rx * mult * math.cos(theta),
                    cy + ry * mult * math.sin(theta)))
    return pts


def _draw_stroke(layer: Image.Image, points: list[tuple[float, float]],
                  color: tuple, width: int, alpha: int) -> None:
    if len(points) < 2:
        return
    d = ImageDraw.Draw(layer)
    d.line(points, fill=(*color, alpha), width=width, joint="curve")
    # round off the two visible ends -- a pen stroke doesn't have square tips
    r = width / 2.0
    for (px, py) in (points[0], points[-1]):
        d.ellipse((px - r, py - r, px + r, py + r), fill=(*color, alpha))


def apply_annotators_circle(frame: Image.Image, bbox: tuple[int, int, int, int],
                             progress: float, color: tuple = RUBRIC, seed: int = 17,
                             pad_x_frac: float = 0.32, pad_y_frac: float = 1.05,
                             stroke_width: int = 5, start_angle_deg: float = -100.0
                             ) -> Image.Image:
    """Draw the Annotator's Circle around `bbox` on an already-composited
    frame (e.g. one that already has a Scribed Ink verse card pasted on it).

    bbox: (x0, y0, x1, y1) pixel rectangle of the word, in the SAME pixel
        space as `frame` (i.e. already translated to the frame's own
        coordinates if the lettering lives on a pasted overlay).
    progress: 0.0-1.0 across the whole two-pass gesture. 0 -> untouched
        frame. Pass 1 (full weight) draws over progress 0..PASS1_END; pass 2
        (lighter, slightly offset) draws over PASS1_END..1.0.
    color: RUBRIC (default) or GOLD for a glory-beat word (Scribe's Tally's
        color law decides which -- this function just takes the result).
    pad_x_frac / pad_y_frac: how far the ellipse's half-axes extend past the
        bbox's own half-width/height (a word's ink bbox is letter-tight; an
        annotator's circle needs real air around it to read as a circling
        gesture and not a bounding box).
    """
    progress = max(0.0, min(1.0, progress))
    if progress <= 0.0:
        return frame

    x0, y0, x1, y1 = bbox
    bw, bh = max(1.0, x1 - x0), max(1.0, y1 - y0)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    rx = (bw / 2.0) * (1.0 + pad_x_frac)
    ry = (bh / 2.0) * (1.0 + pad_y_frac)

    frame_rgba = frame.convert("RGBA")
    layer = Image.new("RGBA", frame_rgba.size, (0, 0, 0, 0))

    # pass 1 -- the full sweep, full ink weight
    p1 = min(1.0, progress / PASS1_END)
    if p1 > 0:
        pts = _wobbled_ellipse_points(cx, cy, rx, ry, seed=seed,
                                       start_angle_deg=start_angle_deg)
        n_take = max(2, int(round(_ease(p1) * (len(pts) - 1))) + 1)
        _draw_stroke(layer, pts[:n_take], color, width=stroke_width, alpha=232)

    # pass 2 -- lighter, slightly offset second loop: "a real hand circling
    # something important goes around twice." Different seed -> a visibly
    # different wobble path, not a traced duplicate of pass 1.
    if progress > PASS2_START:
        p2 = min(1.0, (progress - PASS2_START) / (1.0 - PASS2_START))
        off = max(2.0, min(rx, ry) * 0.09)
        pts2 = _wobbled_ellipse_points(cx + off * 0.4, cy - off * 0.5,
                                        rx * 1.05, ry * 1.06, seed=seed + 101,
                                        start_angle_deg=start_angle_deg + 24)
        n_take2 = max(2, int(round(_ease(p2) * (len(pts2) - 1))) + 1)
        _draw_stroke(layer, pts2[:n_take2], color,
                      width=max(2, stroke_width - 2), alpha=140)

    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    out = Image.alpha_composite(frame_rgba, layer)
    return out.convert("RGB")


# ---------------------------------------------------------------------------
# demo CLI
# ---------------------------------------------------------------------------

def scale_crop(im, w, h):
    s = max(w / im.width, h / im.height)
    zw, zh = int(im.width * s + 0.5), int(im.height * s + 0.5)
    im = im.resize((zw, zh), Image.LANCZOS)
    return im.crop(((zw - w) // 2, (zh - h) // 2, (zw - w) // 2 + w, (zh - h) // 2 + h))


def render_demo(still: Path, out_mp4: Path, bbox: tuple, t0: float, duration: float,
                 color_name: str, seed: int):
    W, H, FPS = 1080, 1920, 30
    color = GOLD if color_name == "gold" else RUBRIC
    im = scale_crop(Image.open(still).convert("RGB"), W, H)

    work = out_mp4.parent / (out_mp4.stem + "_work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    n_frames = int(round(duration * FPS))
    for i in range(n_frames):
        t = i / FPS
        progress = max(0.0, min(1.0, t / max(1e-6, duration)))
        frame = apply_annotators_circle(im, bbox, progress, color=color, seed=seed)
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
    ap.add_argument("--demo", action="store_true", help="render a standalone preview clip over a still")
    ap.add_argument("--still", help="source still (any resolution)")
    ap.add_argument("--out", help="output mp4")
    ap.add_argument("--bbox", required=False, default="440,860,640,910",
                     help="x0,y0,x1,y1 pixel rect to circle, in the 1080x1920 frame")
    ap.add_argument("--t0", type=float, default=0.0, help="unused placeholder, kept for symmetry with sibling demos")
    ap.add_argument("--duration", type=float, default=1.4, help="whole two-pass gesture length, seconds")
    ap.add_argument("--color", choices=["rubric", "gold"], default="rubric")
    ap.add_argument("--seed", type=int, default=17)
    a = ap.parse_args()
    if a.demo:
        if not a.still or not a.out:
            ap.error("--demo requires --still and --out")
        bbox = tuple(int(v) for v in a.bbox.split(","))
        render_demo(Path(a.still), Path(a.out), bbox, a.t0, a.duration, a.color, a.seed)
    else:
        ap.error("only --demo is implemented from the CLI -- import apply_annotators_circle for pipeline use")
