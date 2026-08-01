#!/usr/bin/env python
"""Page Transitions -- the family the user asked for (Round 6 promotion,
panel-revised 2026-07-30, `poc_living_sketchbook/_FABLE_ROUND6_THE_KEEPER.md`
build card 3). REVISED BY PANEL: v1 ships `torn_out_page` ONLY -- the one
device the user's verdict actually approved (grab -> lift+shadow -> rip away,
deckle flash, rip cue at release). Promotes
`poc_living_sketchbook/storm/_bold_poc/_build_bold.py` poc_2, generalized to
any above/below frame pair + timing params.

NAMING (grok's fix, accepted): this device is `torn_out_page` -- the
landing's torn-hole device is a *different* thing, the `tear_hole`. Never the
same words for both.

NOT BUILT IN v1 -- do not add without a POC + the user's taste gate:
  - `slide_under` -- a candidate the user's "we can have more such transition
    effects" note OPENS AS A LANE, not a spec. Needs its own $0 POC and the
    same taste gate that killed 13 of 22 devices this round.
  - `lift_away` -- same status: named candidate, no production code until it
    earns a KEEP verdict on its own POC.
  Every future candidate in this family must be a two-hand PAPER action --
  wipes, dissolves, and CG curls die at the pitch (Round 6 doc).

Relationship to the existing transition stack (cursor's note in the round
doc): this EXTENDS it. `paperRip`/`inkSwipe`/`halftone` (wherever the
episode assembler already wires them) stay; `torn_out_page` is a new option
in the same family, not a parallel path.

GOVERNORS: NEVER tear out a page carrying the Word (LAW 1 -- caller's
responsibility, this class has no idea what a frame contains); hard physical
transitions at ACT TURNS only; never two inside 10 seconds. Foley: a single
`paper_tear` cue at the release (rip) instant.

API:
    from page_transitions import TornOutPage

    tr = TornOutPage(above=screaming_still, below=asleep_still,
                      grab_t=0.9, rip_t=1.5, gone_t=1.95, seed=13)
    frame = tr.compose(t)          # t = seconds since the transition's own t=0
    cues = tr.foley_cues()

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\page_transitions.py --demo --above <a.png> --below <b.png> --out demo.mp4
    .venv\\Scripts\\python.exe panel_animator\\page_transitions.py --selftest
"""
from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate

FPS = 30
W, H = 1080, 1920
DECKLE_W = 46           # torn-remnant strip width, px -- matches the approved POC


def _smootherstep(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


def _deckle_layer(h: int, seed: int) -> Image.Image:
    """White torn deckle down the flying page's left edge (the tear
    remnant). Unchanged geometry from the approved POC, generalized to any
    frame height `h`."""
    rng = random.Random(seed)
    deckle = Image.new("RGBA", (DECKLE_W, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deckle)
    pts = [(DECKLE_W, 0)]
    for y in range(0, h, 14):
        pts.append((14 + rng.uniform(-9, 9), y))
    pts += [(DECKLE_W, h)]
    dd.polygon(pts, fill=(247, 242, 228, 255))
    return deckle


class TornOutPage:
    """The Torn-Out Page transition: the Keeper RIPS the `above` page out of
    the book on camera -- grab, lift, tear away right (white deckle flash on
    the flying page), `below` already waiting beneath. Deterministic, $0.
    Unchanged mechanics from the approved POC
    (`_bold_poc/_build_bold.py::poc_2`), generalized to any two frames + any
    timing."""

    def __init__(self, above: Image.Image, below: Image.Image,
                 grab_t: float = 0.9, rip_t: float = 1.5, gone_t: float = 1.95,
                 seed: int = 13):
        """
        above: the page being torn away (the panic/rejected spread).
        below: the page revealed beneath (already composited full-frame --
            this class never generates it).
        grab_t: the hand settles on the page, no motion yet before this.
        rip_t: the release instant -- deckle flashes just before this, the
            page accelerates away starting here. Foley `paper_tear` fires at
            this time.
        gone_t: `above` has fully left frame; `compose()` returns `below`
            unchanged for any t >= gone_t.
        seed: deckle wobble seed.
        """
        self.above = above.convert("RGBA")
        self.below = below.convert("RGB")
        if self.above.size != self.below.size:
            raise ValueError(f"above/below size mismatch: {self.above.size} vs {self.below.size}")
        self.grab_t, self.rip_t, self.gone_t = grab_t, rip_t, gone_t
        self._deckle = _deckle_layer(self.above.size[1], seed)

    def compose(self, t: float) -> Image.Image:
        out = self.below.convert("RGBA")
        if t >= self.gone_t:
            return out.convert("RGB")
        w, h = self.above.size
        page = self.above.copy()
        if t >= self.rip_t - 0.35:   # deckle shows as the page starts to give
            page.alpha_composite(self._deckle, (0, 0))
        if t < self.grab_t:
            ang, dx, dy, lift = 0.0, 0, 0, 0.0
        elif t < self.rip_t:
            p = _smootherstep((t - self.grab_t) / (self.rip_t - self.grab_t))
            ang, dx, dy, lift = -2.2 * p, int(8 * p), int(-6 * p), p
        else:
            p = ((t - self.rip_t) / (self.gone_t - self.rip_t)) ** 1.8   # accelerates away
            ang = -2.2 - 16 * p
            dx = int(8 + (w * 1.45) * p)
            dy = int(-6 - (h * 0.22) * p)
            lift = 1.0
        page = page.rotate(ang, center=(60, int(h * 0.6)), resample=Image.BICUBIC)
        if lift > 0:
            sil = page.split()[3].point(lambda a: min(a, int(70 * lift)))
            shadow = Image.new("RGBA", page.size, (25, 18, 12, 0))
            shadow.putalpha(sil)
            shadow = shadow.filter(ImageFilter.GaussianBlur(6 + 10 * lift))
            out.alpha_composite(shadow, (dx + int(10 * lift), dy + int(14 * lift)))
        out.alpha_composite(page, (dx, dy))
        return out.convert("RGB")

    def foley_cues(self):
        """A single `paper_tear` cue at the release, spanning the rip-away
        phase only (the grab/lift itself is silent -- matches the v6 score's
        own convention, `scriptorium_foley.storm_cue_list`'s Torn-Out Page cue)."""
        return [("paper_tear", self.rip_t, self.gone_t - self.rip_t)]


# ---------------------------------------------------------------------- demo


def _render(name: str, frame_fn, dur: float, outdir: Path):
    work = outdir / f"_{name}_work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    n = int(dur * FPS)
    for i in range(n):
        frame_fn(i / FPS).save(work / f"f{i:05d}.png")
    out = outdir / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(work / "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)],
                   check=True, capture_output=True)
    shutil.rmtree(work)
    print(f"[ok] {out}")


def render_demo(above: Path, below: Path, out_mp4: Path, duration: float):
    a = scale_crop(Image.open(above).convert("RGB"), W, H)
    b = scale_crop(Image.open(below).convert("RGB"), W, H)
    tr = TornOutPage(a, b)
    _render(out_mp4.stem, lambda t: tr.compose(t), duration, out_mp4.parent)


# ------------------------------------------------------------------ selftest


def run_selftests() -> int:
    ok = True

    def check(cond, label):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {label}")
        ok = ok and cond

    above = Image.new("RGB", (200, 300), (200, 50, 50))
    below = Image.new("RGB", (200, 300), (50, 200, 50))
    tr = TornOutPage(above, below, grab_t=0.9, rip_t=1.5, gone_t=1.95, seed=13)

    # 1. before grab, above fills the frame (no motion)
    f0 = np.asarray(tr.compose(0.0))
    check(np.array_equal(f0, np.asarray(above.convert("RGB"))),
          "before grab_t, frame is the untouched `above` page")

    # 2. at/after gone_t, below fills the frame, byte-stable forever after
    f_gone = np.asarray(tr.compose(1.95))
    f_later = np.asarray(tr.compose(50.0))
    check(np.array_equal(f_gone, np.asarray(below)), "at gone_t, `below` is fully revealed")
    check(np.array_equal(f_gone, f_later), "compose() is byte-stable for any t beyond gone_t")

    # 3. mid-transition, neither page alone explains the frame (page is moving/rotated)
    f_mid = np.asarray(tr.compose(1.7))
    check(not np.array_equal(f_mid, np.asarray(above.convert("RGB"))) and
          not np.array_equal(f_mid, np.asarray(below)),
          "mid-rip frame differs from both the pure above and pure below pages")

    # 4. foley cue is exactly the rip-away window
    cues = tr.foley_cues()
    cue_ok = len(cues) == 1 and cues[0][0] == "paper_tear" and cues[0][1] == 1.5 \
        and abs(cues[0][2] - 0.45) < 1e-6
    check(cue_ok, f"foley_cues() is the rip-away window: {cues}")

    # 5. size mismatch raises
    try:
        TornOutPage(Image.new("RGB", (10, 10)), Image.new("RGB", (20, 20)))
        check(False, "size mismatch raises ValueError")
    except ValueError:
        check(True, "size mismatch raises ValueError")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip")
    ap.add_argument("--above", help="page being torn away (--demo mode)")
    ap.add_argument("--below", help="page revealed beneath (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=4.5, help="--demo clip length, seconds")
    ap.add_argument("--selftest", action="store_true", help="run the engine self-tests")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(run_selftests())
    if a.demo:
        if not a.above or not a.below or not a.out:
            ap.error("--demo requires --above, --below, and --out")
        render_demo(Path(a.above), Path(a.below), Path(a.out), a.duration)
    else:
        ap.print_help()
