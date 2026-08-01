#!/usr/bin/env python
"""Lift-Away Page -- the calm sibling to `torn_out_page` (Round 9 build,
`poc_living_sketchbook/_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md` sec. B1).
`page_transitions.py` ships exactly one transition -- `torn_out_page`, a
panic/rejection act-turn (grab -> lift+shadow -> accelerating rip-away,
deckle flash, `paper_tear` cue). Round 6's own doc named two open candidates
for the OTHER end of this family, a calm turn rather than a violent one, and
shipped neither: `slide_under` and `lift_away`. This is `lift_away`'s POC
build -- the closer sibling to `torn_out_page` (same grab->lift opening act,
different resolution: settle instead of rip), reusing `TornOutPage`'s own
scaffolding (the `_smootherstep` easing, the above/below frame-pair API, the
byte-stable-after-transition governor, the `--selftest` CLI pattern) rather
than inventing an unrelated geometry.

Deliberately the OPPOSITE curve from `torn_out_page`, not just a slower
version of it: the near/grab edge is the LEFT edge (torn_out_page rips to
the right), the arc hinges near the RIGHT edge (torn_out_page's own pivot
sits near the left), there is no deckle flash (nothing tears -- this is a
whole page), the hinge rotation is capped at ~35 degrees, and the arc moves
at a constant EASED velocity (`_smootherstep` only, never torn_out_page's
`** 1.8` accelerating curve) -- that curve is what makes torn_out_page read
as violent; its absence is what makes this read as deliberate/calm. The two
devices are meant to be visually distinguishable at a glance from a single
frame, in either direction of travel or hinge side.

NAMING (grok's rule from round 6, still binding): `torn_out_page` (violent
transition), `tear_hole` (the landing's own device), `lift_away` (this calm
transition) -- three distinct terms, no reuse of tear/rip/torn language
anywhere in this device's naming or cues.

GOVERNORS (caller's responsibility -- this class has no idea what a frame
contains):
  - Never on a page carrying the Word mid-reveal (LAW 1).
  - Reserved for CALM/REFLECTIVE turns, never panic/rejection (torn_out_page
    owns that beat) -- the two transitions are chosen by EMOTIONAL REGISTER,
    not just "which one is due."
  - <=1 per episode by default (same conservative starting budget as every
    other round-6-family device).
  - The 10-second rule is a COMBINED budget across the whole page-transition
    family: never two page-transition devices of any kind (torn_out_page +
    lift_away together) within 10s of each other in the same episode.
  - Never the landing spread (torn_out_page/tear_hole owns the landing).
  - Size mismatch raises `ValueError` (same defensive check as TornOutPage).

Open item, honestly flagged (unchanged from the Round 9 plan): there is no
clean page-turn/paper-rustle one-shot in `sound_library/clips/` yet -- the
`page_turn` foley cue this module emits needs a sourced or quoted asset
banked before this device ships to a real episode. Not fixed here.

API (mirrors `TornOutPage`'s shape on purpose):
    from lift_away import LiftAwayPage

    tr = LiftAwayPage(above=s07_reflective_moses, below=s08_typology_page,
                       grab_t=0.9, lift_t=1.5, settle_t=2.3, seed=13)
    frame = tr.compose(t)      # t = seconds since the transition's own t=0
    cues = tr.foley_cues()

Usage (CLI):
    .venv\\Scripts\\python.exe panel_animator\\lift_away.py --demo --above <a.png> --below <b.png> --out demo.mp4
    .venv\\Scripts\\python.exe panel_animator\\lift_away.py --selftest
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from page_transitions import _smootherstep, _render, scale_crop  # noqa: E402 -- reuse, don't duplicate

FPS = 30
W, H = 1080, 1920
MAX_HINGE_DEG = 35.0   # spec ceiling -- never exceeded, unlike torn_out_page's accelerating rip past it


class LiftAwayPage:
    """The Lift-Away Page transition: the Keeper calmly turns to a page they
    already prepared -- grab the LEFT edge, arc it left on a spine-side
    hinge near the RIGHT edge at constant eased velocity, settle. No deckle,
    nothing tears; `below` is already composited full-frame beneath and is
    revealed as `above` clears off to the left. $0, deterministic."""

    def __init__(self, above: Image.Image, below: Image.Image,
                 grab_t: float = 0.9, lift_t: float = 1.5, settle_t: float = 2.3,
                 seed: int = 13):
        """
        above: the page being turned away (a calm/reflective spread, never a
            panic/rejection one -- that is torn_out_page's beat).
        below: the page revealed beneath (already composited full-frame --
            this class never generates it).
        grab_t: the hand settles on the page's left edge, no motion yet
            before this.
        lift_t: the left edge has fully lifted (contact shadow at max); the
            page begins its arc here. Foley `page_turn` fires at this time.
        settle_t: the page has finished its arc and settled out of frame;
            `compose()` returns `below` unchanged for any t >= settle_t.
        seed: kept for API symmetry with TornOutPage (this device has no
            deckle to wobble, but the shadow softness uses it).
        """
        self.above = above.convert("RGBA")
        self.below = below.convert("RGB")
        if self.above.size != self.below.size:
            raise ValueError(f"above/below size mismatch: {self.above.size} vs {self.below.size}")
        self.grab_t, self.lift_t, self.settle_t = grab_t, lift_t, settle_t
        self.seed = seed

    def compose(self, t: float) -> Image.Image:
        out = self.below.convert("RGBA")
        if t >= self.settle_t:
            return out.convert("RGB")
        w, h = self.above.size
        page = self.above.copy()

        if t < self.grab_t:
            ang, dx, dy, lift = 0.0, 0, 0, 0.0
        elif t < self.lift_t:
            # grab phase: the LEFT edge lifts, a small growing contact
            # shadow signals it -- no deckle, nothing tears, only a tiny
            # nudge yet. Eased with the same _smootherstep torn_out_page uses.
            p = _smootherstep((t - self.grab_t) / (self.lift_t - self.grab_t))
            ang, dx, dy, lift = 1.5 * p, -int(6 * p), -int(4 * p), p
        else:
            # arc phase: plain _smootherstep only -- deliberately NO ** 1.8
            # acceleration curve. That curve is what makes torn_out_page
            # read as violent; its absence is what makes this read as
            # deliberate/calm. Rotates up to MAX_HINGE_DEG, translates LEFT
            # (torn_out_page goes right), bobs slightly up-then-down.
            p = _smootherstep((t - self.lift_t) / (self.settle_t - self.lift_t))
            ang = 1.5 - (1.5 + MAX_HINGE_DEG) * p
            dx = -int(6 + (w * 0.95) * p)
            dy = -int(4 * (1 - p)) - int(60 * math.sin(math.pi * p))
            lift = 1.0

        # spine-side hinge near the RIGHT edge -- the mirror of
        # torn_out_page's own near-left-edge pivot at (60, h*0.6). Opposite
        # side, so the two devices are distinguishable at a glance even from
        # a single frame.
        page = page.rotate(ang, center=(w - 60, int(h * 0.6)), resample=Image.BICUBIC)
        if lift > 0:
            sil = page.split()[3].point(lambda a: min(a, int(70 * lift)))
            shadow = Image.new("RGBA", page.size, (25, 18, 12, 0))
            shadow.putalpha(sil)
            shadow = shadow.filter(ImageFilter.GaussianBlur(6 + 10 * lift))
            out.alpha_composite(shadow, (dx - int(10 * lift), dy + int(14 * lift)))
        out.alpha_composite(page, (dx, dy))
        return out.convert("RGB")

    def foley_cues(self):
        """A single `page_turn` cue at lift_t (the instant the page is
        fully lifted and begins its arc), spanning the arc phase -- never
        `paper_tear`: nothing tears, this is a whole page turning."""
        return [("page_turn", self.lift_t, self.settle_t - self.lift_t)]


# ---------------------------------------------------------------------- demo


def render_demo(above: Path, below: Path, out_mp4: Path, duration: float):
    a = scale_crop(Image.open(above).convert("RGB"), W, H)
    b = scale_crop(Image.open(below).convert("RGB"), W, H)
    tr = LiftAwayPage(a, b)
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
    tr = LiftAwayPage(above, below, grab_t=0.9, lift_t=1.5, settle_t=2.3, seed=13)

    # 1. before grab, above fills the frame (no motion)
    f0 = np.asarray(tr.compose(0.0))
    check(np.array_equal(f0, np.asarray(above.convert("RGB"))),
          "before grab_t, frame is the untouched `above` page")

    # 2. at/after settle_t, below fills the frame, byte-stable forever after
    f_settle = np.asarray(tr.compose(2.3))
    f_later = np.asarray(tr.compose(50.0))
    check(np.array_equal(f_settle, np.asarray(below)), "at settle_t, `below` is fully revealed")
    check(np.array_equal(f_settle, f_later), "compose() is byte-stable for any t beyond settle_t")

    # 3. mid-arc, neither page alone explains the frame (page is moving/rotated)
    f_mid = np.asarray(tr.compose(2.1))
    check(not np.array_equal(f_mid, np.asarray(above.convert("RGB"))) and
          not np.array_equal(f_mid, np.asarray(below)),
          "mid-arc frame differs from both the pure above and pure below pages")

    # 4. foley cue is exactly one page_turn cue at lift_t, never paper_tear
    cues = tr.foley_cues()
    cue_ok = len(cues) == 1 and cues[0][0] == "page_turn" and cues[0][1] == 1.5 \
        and abs(cues[0][2] - 0.8) < 1e-6
    check(cue_ok, f"foley_cues() is exactly one page_turn cue at lift_t: {cues}")

    # 5. size mismatch raises
    try:
        LiftAwayPage(Image.new("RGB", (10, 10)), Image.new("RGB", (20, 20)))
        check(False, "size mismatch raises ValueError")
    except ValueError:
        check(True, "size mismatch raises ValueError")

    print(f"\n{'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


# -------------------------------------------------------------------- CLI


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="render a demo clip")
    ap.add_argument("--above", help="page being turned away (--demo mode)")
    ap.add_argument("--below", help="page revealed beneath (--demo mode)")
    ap.add_argument("--out", help="output mp4 (--demo mode)")
    ap.add_argument("--duration", type=float, default=3.0, help="--demo clip length, seconds")
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
