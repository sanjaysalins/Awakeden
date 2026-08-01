"""Storm episode -- step 6: the FULL-COVERAGE device pass over the v5 base
cut, per _STORM_V6_SCORE.md (Fable design -> Sonnet implementation,
2026-07-30). Every timestamp below is bound to a real word in
_storm_alignment.json or to a real spread boundary in _s4_assemble.py's own
SHOTS table -- see the inline comment on each constant for its provenance.

ARCHITECTURE: a separate script that IMPORTS _s4_assemble.py (as S4) rather
than a --v6 flag threaded through it. _s4_assemble.py is the shipped v5
deliverable (STORM_living_sketchbook.mp4) and the HARD RULE is "keep v5
intact" -- zero lines of _s4_assemble.py are touched. This also matches the
codebase's own established pattern (_vault_poc imports _keeper_poc,
_vault2_poc imports both) of POC/next-round scripts chain-importing a prior
script's proven functions rather than re-implementing them. Reused as-is
from S4: SHOTS, TRANSITIONS (paperRip@23.55), WM_TOP, scribed_ink_card,
stamped_text, noise_layers, transition_mask, storm_tide_curve,
STILL_WATER_HORIZON, build_paper_resources, apply_paper_devices (the v5
paper-layer dispatch -- v6 wraps it, see apply_paper_devices_v6 below,
rather than editing it, so s04's candle grade and s05's raking-light drop
are additive/conditional, not surgery on S4's own function).

Reused as-is from the keeper-hand engine (_keeper_poc/_build_poc.py, BOLD=1
already the standing 2026-07-30 art direction): entry_events, compose_at,
KEEPER_INK, F_KEEPER, pencil_study, sweep_reveal, leader_layer -- imported
as K, called with new text/timing/seeds, the hand-rendering math itself is
untouched.

The Torn-Out Page (s06->s07) and Bleeding Word drop (s03) mechanics are
PROMOTED from _bold_poc/_build_bold.py's poc_2 (torn page) and poc_3
(bleed) into standalone functions below (torn_page_frame, apply_bleed_drop)
with the SAME math/coefficients/seeds, since the POC versions were written
as one-off closures over demo timing, not reusable functions -- re-timed to
the real episode's alignment, nothing about the physical simulation itself
changed. The Candle-Only grade (s04) is promoted from _vault2_poc/
_build_vault2.py's poc_candle the same way (same R_of/lit/glow formula, same
lamp position, re-timed to "asleep." (8.843s) instead of the POC's t=0).

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s6_assemble.py
  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s6_assemble.py --test-window 21 22.5
"""
import argparse
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa

sys.path.insert(0, str(ROOT / "panel_animator"))
import wash_creep          # noqa
import tide_mark           # noqa
import damp_cockle         # noqa
import still_water_mirror  # noqa
import raking_light        # noqa
import set_off as set_off_mod   # noqa
import blue_line           # noqa
import annotators_circle   # noqa
from held_breath import energy_envelope  # noqa
import scriptorium_foley as foley  # noqa

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _s4_assemble as S4  # noqa -- the v5 base assembler, reused not rewritten

sys.path.insert(0, str(HERE / "_keeper_poc"))
import _build_poc as K  # noqa -- keeper-hand engine (entry_events/compose_at/BOLD=1)

W, H, FPS, TOTAL = S4.W, S4.H, S4.FPS, S4.TOTAL
CLIPS = S4.CLIPS
STILLS = S4.STILLS
SRC_AUDIO = S4.SRC_AUDIO
ALIGN_PATH = S4.ALIGN_PATH
SHOTS = S4.SHOTS
TRANSITIONS = S4.TRANSITIONS
WM_TOP = S4.WM_TOP
SHOTS_BY_NAME = {n: (t0, t1) for (n, t0, t1) in SHOTS}
S02_END = SHOTS_BY_NAME["s02_water"][1]        # 4.25 -- header's own hard exit bound
S03_END = SHOTS_BY_NAME["s03_screaming"][1]    # 6.67 -- s03 entry+bleed's own hard exit bound
S05_END = SHOTS_BY_NAME["s05_hands"][1]        # 18.36 -- inkwell+margin-studies' own hard exit bound

OUT = HERE / "STORM_living_sketchbook_v6.mp4"

INK = S4.INK
RUBRIC = S4.RUBRIC


def smootherstep(t):
    """The Perlin smootherstep _bold_poc/_build_bold.py and _vault2_poc/
    _build_vault2.py both used for the torn-page / bleed / candle curves --
    a DIFFERENT (gentler-middle) curve than S4.ease's raised-cosine. Kept
    distinct on purpose: these three devices are promoted from those POCs
    verbatim, S4.ease stays reserved for genuinely-S4-owned motion."""
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (t * 6 - 15) + 10)


# =============================================================================
# TIMING CONSTANTS -- every one bound to _storm_alignment.json (word start/end)
# or to SHOTS' own spread boundaries. See _STORM_V6_SCORE.md's table for the
# design intent; the exact numbers here are the "re-bind to alignment" pass
# the score explicitly asked for (its own approx numbers were placeholders).
# =============================================================================

# ---- s01 Field Header ----
# blue-line's own ink-arrival front completes at t=0.9 (S4 apply_paper_devices,
# "s01_waves" branch: `if t < 0.9`). Score: "writes ~0.6s AFTER" that.
HEADER_T0 = 0.9 + 0.6          # 1.50
HEADER_DUR = 1.8
HEADER_ORIGIN = (int(W * 0.28), int(H * 0.045))   # x>=0.26W clears the logo zone (x40-240)

# ---- s03 Bleeding Word (clip is MOVING -- Two-Hands application) ----
# s03 window 4.25-6.67 (_storm_alignment.json has no literal "fear" token in
# this window -- "Men screaming for their lives." is what's actually spoken.
# "screaming" (4.608-5.032) is the literal fear-word here; the drop is bound
# to its END, not the alternate candidate "lives." (5.375-5.739, the
# sentence's own climax) -- see the report for both readings.)
S03_ENTRY_T0 = 4.35
S03_ENTRY_DUR = 0.65
S03_ORIGIN = (int(W * 0.28), int(H * 0.05))       # TOP cream lane, x 0.28-0.75W
S03_DROP_T = 5.032                                 # "screaming" ends

# ---- s04 Candle-Only (grade, no text) ----
T_ASLEEP = 8.843               # "asleep." onset, first instance, inside s04's own window
CANDLE_COLLAPSE_DUR = 1.2      # score: "R -> ~330px over 1.2s"
CANDLE_COLLAPSE_END = T_ASLEEP + CANDLE_COLLAPSE_DUR      # 10.043
S04_T0, S04_T1 = SHOTS_BY_NAME["s04_asleep"]
CANDLE_REOPEN_START = S04_T1 - 0.5                          # 10.34, spread's final 0.5s

# ---- s05 Inkwell Runs Dry (+ Margin Studies fallback, raking-light dropped) ----
# score's own approx (write 11.5-13.5, blot 14.2, resume 14.5-16.5) re-bound
# to the nearest real alignment word boundary in each case:
S05_WRITE_T0 = 11.628           # "asleep" (1st, negated) ends -- approx target 11.5, diff 0.128
S05_WRITE_DUR = 14.146 - 11.628  # ends exactly at S05_BLOT_T, see below
S05_BLOT_T = 14.146             # "asleep" (2nd) ends -- approx target 14.2, diff 0.054
S05_RESUME_T0 = 14.589          # "He" starts -- approx target 14.5, diff 0.089
S05_RESUME_DUR = 16.551 - 14.589  # "is" (of "that is killing") starts -- approx target 16.5, diff 0.051
S05_WRITE_ORIGIN = (int(W * 0.245), int(H * 0.006))   # v6.1: clear of the AWAKEDEN
                                                       # zone (x 40-240) entirely
S05_RESUME_ORIGIN = (int(W * 0.055), int(H * 0.085))  # v6.1b: lower-LEFT, over the light
                                                       # sleeve/cream -- the first indent try
                                                       # (0.335, 0.052) landed on the dark
                                                       # cloud wash and vanished
S05_BLOT_XY = (int(W * 0.042), int(H * 0.092))  # v6.1b: rides with the resume line

# Margin Studies FALLBACK (score's own escape hatch): s07's window is only
# 1.6s (21.95-23.55) -- genuinely too short for 2 studies + leader + caption
# to read (the reference POC took ~3.5s for this device), AND the leader-line
# geometry only makes sense pointing at a lamp that's actually visible in
# frame, which s07 (eyes) is not while s04/s05 (where the lamp lives) are
# adjacent. So: studies move to s05's TAIL (after the Inkwell resume
# finishes at 16.551, before s05 ends at 18.36 -- 1.809s) and s05's
# raking-light is DROPPED, exactly as the score's own fallback specifies.
DROP_RAKING_S05 = True
MARGIN_ST1_T0, MARGIN_ST1_DUR = 16.551, 0.35
MARGIN_ST2_T0, MARGIN_ST2_DUR = 16.75, 0.35
MARGIN_LEADER_T0, MARGIN_LEADER_DUR = 17.10, 0.25
MARGIN_CAP_T0, MARGIN_CAP_DUR = 17.35, 0.6
MARGIN_S1_POS = (560, 1000)
MARGIN_S2_POS = (810, 1030)
MARGIN_CAP_ORIGIN = (620, 1300)

# ---- s06->s07 Torn-Out Page transition ----
# bound to the s06/s07 spread cut (21.95) so the tear completes EXACTLY as
# s07 begins -- score: "grab/lift 0.3s, rip-away 0.35s" (0.65s total).
S06_S07_CUT = SHOTS_BY_NAME["s07_eyes"][0]         # 21.95
TORN_GRAB_DUR = 0.3
TORN_RIP_DUR = 0.35
TORN_GRAB0 = S06_S07_CUT - (TORN_GRAB_DUR + TORN_RIP_DUR)   # 21.30
TORN_RIP0 = TORN_GRAB0 + TORN_GRAB_DUR                       # 21.60
TORN_GONE = S06_S07_CUT                                      # 21.95

# ---- s08 THE WORD ARRIVES WHOLE (LAW 1) ----
CARD_T = 23.545                 # "Why" onset -- the quote's first word
CARD_T1 = 27.10                 # unchanged from v5 (hard cutoff, no fade either way)
STUB_T0 = 22.756                # "eyes:" ends (s07's own last word)
STUB_DUR = 1.6                  # full-text pace had it finished by t0+1.6=24.36; interrupted at CARD_T (~49% through)
STUB_ORIGIN = (int(W * 0.28), int(H * 0.05))

# ---- s10 calm-register Entry 3 ----
S10_ENTRY_T0 = 31.35             # "calm." ends (30.958-31.241) + a beat -- POC-B's own settle gap
S10_ENTRY_DUR = 2.0              # bleeds ~1.15s into s11's own window (32.20) -- s10's own tail
                                  # (31.35->32.20) is only 0.85s, too short for calm-register legibility;
                                  # documented deviation, see report.
S10_ORIGIN = (int(W * 0.09), int(H * 0.050))   # POC-B's own proven upper-sky lane


# =============================================================================
# apply_paper_devices_v6 -- wraps S4.apply_paper_devices (unmodified), adds
# the s04 candle grade (after S4's own wash/tide/damp) and the s05
# raking-light drop (a small standalone re-implementation of JUST that one
# branch, since Python can't splice a flag into the middle of S4's own
# per-name dispatch without editing S4 itself).
# =============================================================================

def apply_paper_devices_v6(frame, name, t, t0, t1, energy, res):
    if name == "s04_asleep":
        frame = S4.apply_paper_devices(frame, name, t, t0, t1, energy, res)
        frame = candle_only_grade(frame, t)
        return frame
    if name == "s05_hands" and DROP_RAKING_S05:
        frame = tide_mark.apply_tide_mark(frame, height_frac=S4.storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)
        return frame
    return S4.apply_paper_devices(frame, name, t, t0, t1, energy, res)


# =============================================================================
# s04 CANDLE-ONLY grade (promoted from _vault2_poc/_build_vault2.py poc_candle)
# =============================================================================
_CANDLE_LAMP = (W * 0.295, H * 0.495)   # same lamp position the POC used
_cys, _cxs = np.mgrid[0:H, 0:W].astype(np.float32)
_CANDLE_DIST = np.sqrt((_cxs - _CANDLE_LAMP[0]) ** 2 + (_cys - _CANDLE_LAMP[1]) ** 2)
_candle_flick_rng = random.Random(51)   # same seed as the POC
_CANDLE_FLICK = [_candle_flick_rng.uniform(-1, 1) for _ in range(400)]
_CANDLE_WARM = np.array([1.08, 1.00, 0.88], np.float32)
_CANDLE_COLD = np.array([0.82, 0.87, 1.00], np.float32)


def _candle_R(t):
    if t < T_ASLEEP:
        return 3000.0
    if t < CANDLE_COLLAPSE_END:
        return 3000.0 - (3000.0 - 330.0) * smootherstep((t - T_ASLEEP) / CANDLE_COLLAPSE_DUR)
    if t < CANDLE_REOPEN_START:
        f = _CANDLE_FLICK[int(t * 12) % 400] * 0.5 + _CANDLE_FLICK[int(t * 5) % 400] * 0.5
        return 330.0 + 10.0 * f
    return 330.0 + (950.0 - 330.0) * smootherstep((t - CANDLE_REOPEN_START) / (S04_T1 - CANDLE_REOPEN_START))


def candle_only_grade(frame_rgb, t):
    """Grade sits over the clip's own paper devices, under any lettering
    (there is none scheduled on s04 itself; the ordering guarantee still
    holds generally since this runs inside apply_paper_devices_v6, BEFORE
    the main loop's overlay/keeper-hand compositing pass)."""
    R = _candle_R(t)
    arr = np.asarray(frame_rgb, np.float32)
    lit = np.clip((R - _CANDLE_DIST) / 260.0 + 0.5, 0, 1)
    glow = np.clip(1.0 - _CANDLE_DIST / max(R, 1), 0, 1) ** 2
    gain = (_CANDLE_COLD[None, None, :] * 0.16) * (1 - lit[..., None]) \
        + (_CANDLE_WARM[None, None, :] * (1.0 + 0.10 * glow[..., None])) * lit[..., None]
    return Image.fromarray(np.clip(arr * gain, 0, 255).astype(np.uint8))


# =============================================================================
# s06->s07 TORN-OUT PAGE (promoted from _bold_poc/_build_bold.py poc_2)
# =============================================================================

def _torn_deckle(seed=13):
    rng = random.Random(seed)
    deckle = Image.new("RGBA", (46, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deckle)
    pts = [(46, 0)]
    for y in range(0, H, 14):
        pts.append((14 + rng.uniform(-9, 9), y))
    pts += [(46, H)]
    dd.polygon(pts, fill=(247, 242, 228, 255))
    return deckle


_TORN_DECKLE = _torn_deckle()


def torn_page_frame(above_frozen_rgba, below_rgb, t):
    """Same rotate/lift/fly-away math as poc_2, re-timed to TORN_GRAB0/
    TORN_RIP0/TORN_GONE (0.3s grab-lift + 0.35s rip-away, vs. the POC's
    demo-paced 0.6s/0.45s) -- same coefficients (-2.2 deg lean, 8/-6px lift
    drift, 1.45W/0.22H fly-out, ()**1.8 acceleration), just scaled to the
    real spread-cut window."""
    out = below_rgb.convert("RGBA")
    if t >= TORN_GONE:
        return out.convert("RGB")
    page = above_frozen_rgba.copy()
    page.alpha_composite(_TORN_DECKLE, (0, 0))
    if t < TORN_RIP0:
        p = smootherstep((t - TORN_GRAB0) / TORN_GRAB_DUR)
        ang, dx, dy, lift = -2.2 * p, int(8 * p), int(-6 * p), p
    else:
        p = ((t - TORN_RIP0) / TORN_RIP_DUR) ** 1.8
        ang = -2.2 - 16 * p
        dx = int(8 + (W * 1.45) * p)
        dy = int(-6 - (H * 0.22) * p)
        lift = 1.0
    page = page.rotate(ang, center=(60, int(H * 0.6)), resample=Image.BICUBIC)
    sil = page.split()[3].point(lambda a: min(a, int(70 * lift)))
    shadow = Image.new("RGBA", page.size, (25, 18, 12, 0))
    shadow.putalpha(sil)
    shadow = shadow.filter(ImageFilter.GaussianBlur(6 + 10 * lift))
    out.alpha_composite(shadow, (dx + int(10 * lift), dy + int(14 * lift)))
    out.alpha_composite(page, (dx, dy))
    return out.convert("RGB")


def _pick_loop_index(t, t0, n):
    li = int((t - t0) * FPS)
    cyc = 2 * n - 2 if n > 1 else 1
    j = li % cyc
    if j >= n:
        j = cyc - j
    return j


def freeze_shot_frame(name, t, frames, paper_res, energy):
    t0, t1 = SHOTS_BY_NAME[name]
    seq = frames[name]
    j = _pick_loop_index(t, t0, len(seq))
    frame = Image.open(seq[j]).convert("RGB")
    frame = apply_paper_devices_v6(frame, name, t, t0, t1, energy(t), paper_res)
    return frame.convert("RGBA")


def below_page_frame(t, frames, paper_res, energy):
    """s07's FIRST frame, held static through the tear (a torn-off page
    doesn't keep playing under the page still being ripped off it), with its
    own paper devices computed at the REAL transition time t so tide-mark
    hands off smoothly into s07's own window starting at S06_S07_CUT."""
    t0, t1 = SHOTS_BY_NAME["s07_eyes"]
    frame = Image.open(frames["s07_eyes"][0]).convert("RGB")
    return apply_paper_devices_v6(frame, "s07_eyes", t, t0, t1, energy(t), paper_res)


# =============================================================================
# s03 BLEEDING WORD drop (promoted from _bold_poc/_build_bold.py poc_3)
# =============================================================================

def compute_word_target(origin, before_words, hit_word, size=64):
    """Locate the center of `hit_word` on one keeper_line, using the SAME
    font-metric walk keeper_line() itself uses, so the target matches
    wherever the glyphs actually land."""
    font = ImageFont.truetype(K.F_KEEPER, size)
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    sp = probe.textlength(" ", font=font)
    x = sum(probe.textlength(w_, font=font) + sp for w_ in before_words)
    x += probe.textlength(hit_word, font=font) * 0.5
    return int(origin[0] + x), int(origin[1] + size * 0.55)


def apply_bleed_drop(frame_rgb, t, cx, cy, drop_t, trails, bloom_dur=0.6, trail_dur=1.2):
    if t < drop_t:
        return frame_rgb
    p = smootherstep((t - drop_t) / bloom_dur)
    arr = np.asarray(frame_rgb, np.float32)
    y0, y1 = max(0, cy - 90), min(H, cy + 90)
    x0, x1 = max(0, cx - 90), min(W, cx + 90)
    ys, xs = np.mgrid[y0:y1, x0:x1]
    r = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    R = 8 + 26 * p
    disc = np.clip((R - r) / 10.0, 0, 1)
    region = arr[y0:y1, x0:x1]
    blur = np.asarray(Image.fromarray(region.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2)), np.float32)
    region[:] = region * (1 - disc[..., None] * 0.5) + blur * (disc[..., None] * 0.5)
    region[:] *= (1.0 - 0.30 * p * disc)[..., None]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")
    pr = smootherstep((t - drop_t - 0.25) / trail_dur)
    if pr > 0:
        d = ImageDraw.Draw(out, "RGBA")
        for (tx, tlen, twid) in trails:
            ln = tlen * pr
            d.line([(tx, cy + 12), (tx, cy + 12 + ln)], fill=(58, 48, 40, 150), width=int(twid))
    return out


_bleed_rng = random.Random(21)  # same seed as poc_3
S03_TRAILS = [(0, 0, 0)]  # placeholder, real values computed once cx is known in main()


# =============================================================================
# Margin Studies (fallback siting -- see MARGIN_* constants above). Promoted
# from _keeper_poc/_build_poc.py poc_C, unchanged math, new position/timing.
# =============================================================================

def build_margin_studies():
    src = Image.open(STILLS / "s04_asleep.png").convert("RGB")
    base_ref = raking_light.scale_crop(src, W, H)
    lamp_box = (int(W * 0.185), int(H * 0.435), int(W * 0.415), int(H * 0.565))
    lamp = base_ref.crop(lamp_box)
    st1 = K.pencil_study(lamp, 240, seed=7, contrast=2.6)  # v6.1: busy ground needs
    st2 = K.pencil_study(lamp, 210, seed=8, contrast=3.0)  # more graphite than the POC's calm paper
    return st1, st2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-window", nargs=2, type=float, default=None,
                     help="render only [start end] seconds, for fast iteration")
    args = ap.parse_args()

    work = HERE / "_frames_v6"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    frames = {}
    for name, t0, t1 in SHOTS:
        src = CLIPS / f"{name}.mp4"
        if not src.exists():
            raise SystemExit(f"missing clip: {src}")
        d = work / f"_{name}"
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-r", str(FPS), str(d / "f%05d.png")], check=True)
        frames[name] = sorted(d.glob("f*.png"))

    verse_card = S4.scribed_ink_card(
        ["Why are ye fearful,", "O ye of little faith?"], "MATTHEW 8:26")
    exactly_stamp = S4.stamped_text("EXACTLY.", S4.F_ZILLA, 78, RUBRIC, letter_spacing=2)

    paper_res = S4.build_paper_resources(frames)
    align_words = __import__("json").load(open(ALIGN_PATH, encoding="utf-8"))
    energy = energy_envelope(align_words, total_duration=TOTAL)

    # ---- precompute every keeper-hand device ONCE (seeded, deterministic) ----
    header_ev, header_ly = K.entry_events(
        [("Galilee. evening. crossing over.", 0, 0)],
        origin=HEADER_ORIGIN, size=60, energy=0.18, seed=44,
        t0=HEADER_T0, dur=HEADER_DUR)

    s03_ev, s03_ly = K.entry_events(
        [("~~storm~~ ~~wind~~ fear.", 0, 0)],
        origin=S03_ORIGIN, size=64, energy=0.85, seed=41,
        t0=S03_ENTRY_T0, dur=S03_ENTRY_DUR)
    s03_cx, s03_cy = compute_word_target(S03_ORIGIN, ["storm", "wind"], "fear.", size=64)
    s03_trails = [(s03_cx + _bleed_rng.randint(-14, 14), _bleed_rng.uniform(40, 85),
                   _bleed_rng.uniform(1.5, 2.6)) for _ in range(3)]

    s05_ev1, s05_ly1 = K.entry_events(
        [("we bailed and bailed and the", 0, 0)],
        origin=S05_WRITE_ORIGIN, size=54, energy=0.6, seed=91,
        t0=S05_WRITE_T0, dur=S05_WRITE_DUR)
    for k, a in enumerate([200, 150, 105, 65, 38]):
        layer, x, y = s05_ly1[-5 + k]
        s05_ly1[-5 + k] = (layer.point(lambda v, aa=a: min(v, aa) if v else 0), x, y)
    s05_ev2, s05_ly2 = K.entry_events(
        [("water kept coming.", 0, 0)],
        origin=S05_RESUME_ORIGIN, size=54, energy=0.6, seed=92,
        t0=S05_RESUME_T0, dur=S05_RESUME_DUR)

    stub_ev, stub_ly = K.entry_events(
        [("he stood up and", 0, 0)],
        origin=STUB_ORIGIN, size=60, energy=0.5, seed=55,
        t0=STUB_T0, dur=STUB_DUR)
    stub_ev = [(t, i) for (t, i) in stub_ev if t < CARD_T]   # LAW 1: interrupted forever

    s10_ev, s10_ly = K.entry_events(
        [("not a breath of wind. not one.", 0, 0)],
        origin=S10_ORIGIN, size=64, energy=0.08, seed=42,
        t0=S10_ENTRY_T0, dur=S10_ENTRY_DUR)

    st1_img, st2_img = build_margin_studies()
    cap_ev, cap_ly = K.entry_events(
        [("still burning.", 0, 0)],
        origin=MARGIN_CAP_ORIGIN, size=56, energy=0.25, seed=43,
        t0=MARGIN_CAP_T0, dur=MARGIN_CAP_DUR)
    margin_lead, margin_lx, margin_ly, _ = K.leader_layer(
        (MARGIN_CAP_ORIGIN[0] + 30, MARGIN_CAP_ORIGIN[1] - 4),
        (MARGIN_S2_POS[0] + st2_img.width // 2, MARGIN_S2_POS[1] + st2_img.height),
        seed=9)

    OVERLAYS = [  # (t0, t1, img, cx_frac, cy_frac) -- unchanged from v5, EXACTLY_stamp only;
                  # verse_card is handled separately below (LAW 1: instant, no popin)
        (35.05, 36.50, exactly_stamp, 0.5, 0.20),
    ]

    grain = S4.noise_layers()
    n_frames = int(TOTAL * FPS)
    outdir = work / "grid"
    outdir.mkdir()

    if args.test_window:
        frame_range = range(int(args.test_window[0] * FPS), int(args.test_window[1] * FPS))
    else:
        frame_range = range(n_frames)

    prev_last = {"img": None}
    torn_above = {"img": None}

    for i in frame_range:
        t = i / FPS

        # ---- s06->s07 Torn-Out Page: special-cased, bypasses normal shot render ----
        if TORN_GRAB0 <= t < TORN_GONE:
            if torn_above["img"] is None:
                torn_above["img"] = freeze_shot_frame("s06_shaken", TORN_GRAB0, frames, paper_res, energy)
            below = below_page_frame(t, frames, paper_res, energy)
            frame = torn_page_frame(torn_above["img"], below, t)
            g = grain[i % len(grain)]
            frame = Image.composite(
                frame.point(lambda v: min(255, v + 6)), frame,
                g.point(lambda v: 22 if v > 236 else 0))
            frame.save(outdir / f"g{i:05d}.png")
            continue

        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1 = shot
        seq = frames[name]
        j = _pick_loop_index(t, t0, len(seq))
        frame = Image.open(seq[j]).convert("RGB")

        for tt, kind in TRANSITIONS.items():
            if tt <= t < tt + 0.4 and prev_last["img"] is not None:
                k = S4.ease((t - tt) / 0.4)
                mask = S4.transition_mask(kind, k)
                frame = Image.composite(frame, prev_last["img"], mask)

        e = energy(t)
        frame = apply_paper_devices_v6(frame, name, t, t0, t1, e, paper_res)

        if name == "s13_landing":
            so_progress = S4.ease(min(1.0, max(0.0, (t - 53.5) / 2.5)))
            if so_progress > 0:
                frame = set_off_mod.apply_set_off(frame.convert("RGBA"), verse_card, so_progress).convert("RGB")

        # ---- generic popin overlays (v5-style: exactly_stamp only) ----
        for (oi0, oi1, img, cxf, cyf) in OVERLAYS:
            if oi0 <= t <= oi1:
                dt = t - oi0
                k = S4.ease(min(1.0, dt / 0.18))
                s2 = 1.28 - 0.28 * k
                oimg = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if k < 1.0:
                    oimg.putalpha(oimg.split()[3].point(lambda v: int(v * k)))
                ox = int(W * cxf - oimg.width / 2)
                oy = max(WM_TOP, int(H * cyf - oimg.height / 2))
                frame.paste(oimg, (ox, oy), oimg)

        # ---- LAW 1: THE WORD ARRIVES WHOLE -- instant, complete, no scale/fade ----
        if CARD_T <= t <= CARD_T1:
            frame = frame.convert("RGBA")
            ox = int(W * 0.5 - verse_card.width / 2)
            oy = max(WM_TOP, int(H * 0.134 - verse_card.height / 2))
            frame.alpha_composite(verse_card, (ox, oy))
            if t >= S4.CIRCLE_T0:
                circle_progress = max(0.0, min(1.0, (t - S4.CIRCLE_T0) / (S4.CIRCLE_T_DRAW - S4.CIRCLE_T0)))
                frame = annotators_circle.apply_annotators_circle(
                    frame.convert("RGB"), S4.FAITH_BBOX, circle_progress,
                    color=annotators_circle.RUBRIC)
            frame = frame.convert("RGB")

        # ---- keeper-hand devices (absolute-time, independent of `name`) ----
        # every block below is hard-bounded to its OWN spread's window end
        # (S02_END/S03_END/S05_END) -- without this bound the ink would keep
        # being redrawn on every later spread's completely unrelated footage
        # for the rest of the 63s episode (caught in code review before the
        # first full render, not left to the QC pass).
        if HEADER_T0 <= t <= S02_END:
            frame = K.compose_at(frame, header_ev, header_ly, t)

        if S03_ENTRY_T0 <= t <= S03_END:
            frame = K.compose_at(frame, s03_ev, s03_ly, t)
        if S03_DROP_T <= t <= S03_END:
            frame = apply_bleed_drop(frame, t, s03_cx, s03_cy, S03_DROP_T, s03_trails)

        if S05_WRITE_T0 <= t <= S05_END:
            frame = K.compose_at(frame, s05_ev1, s05_ly1, t)
        if S05_BLOT_T <= t <= S05_END:
            pblot = smootherstep((t - S05_BLOT_T) / 0.4)
            bx, by = S05_BLOT_XY
            d = ImageDraw.Draw(frame, "RGBA")
            r = 4 + 6 * pblot
            d.ellipse([bx - r, by - r, bx + r, by + r], fill=(48, 40, 34, 205))
            d.ellipse([bx - r * 1.7, by - r * 1.7, bx + r * 1.7, by + r * 1.7],
                      outline=None, fill=(48, 40, 34, int(35 * pblot)))
        if S05_RESUME_T0 <= t <= S05_END:
            frame = K.compose_at(frame, s05_ev2, s05_ly2, t)
        if MARGIN_ST1_T0 <= t <= S05_END:
            fr = frame.convert("RGBA")
            f1 = np.clip((t - MARGIN_ST1_T0) / MARGIN_ST1_DUR, 0, 1)
            if f1 > 0:
                fr.alpha_composite(K.sweep_reveal(st1_img, float(f1)), MARGIN_S1_POS)
            f2 = np.clip((t - MARGIN_ST2_T0) / MARGIN_ST2_DUR, 0, 1)
            if f2 > 0:
                fr.alpha_composite(K.sweep_reveal(st2_img, float(f2)), MARGIN_S2_POS)
            if t >= MARGIN_LEADER_T0:
                fl = np.clip((t - MARGIN_LEADER_T0) / MARGIN_LEADER_DUR, 0, 1)
                l_ = margin_lead.copy()
                if fl < 1.0:
                    a = np.asarray(l_.split()[3], dtype=np.float32)
                    hh = a.shape[0]
                    cut = int(hh * (1 - fl))
                    a[:cut, :] = 0
                    l_.putalpha(Image.fromarray(a.astype(np.uint8)))
                fr.alpha_composite(l_, (margin_lx, margin_ly))
            frame = fr.convert("RGB")
            frame = K.compose_at(frame, cap_ev, cap_ly, t)

        if STUB_T0 <= t < CARD_T:
            frame = K.compose_at(frame, stub_ev, stub_ly, t)

        if S10_ENTRY_T0 <= t <= S10_ENTRY_T0 + S10_ENTRY_DUR + 0.5:
            frame = K.compose_at(frame, s10_ev, s10_ly, t)

        g = grain[i % len(grain)]
        frame = Image.composite(
            frame.point(lambda v: min(255, v + 6)), frame,
            g.point(lambda v: 22 if v > 236 else 0))

        if abs(t + 1 / FPS - t1) < 1 / FPS:
            prev_last["img"] = frame.copy()
        frame.save(outdir / f"g{i:05d}.png")

    if args.test_window:
        test_out = HERE / f"_test_v6_{args.test_window[0]:.1f}_{args.test_window[1]:.1f}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                        "-start_number", str(frame_range.start),
                        "-i", str(outdir / "g%05d.png"),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                        str(test_out)], check=True)
        print(f"[test] {test_out}")
        shutil.rmtree(work)
        return

    silent = HERE / "_silent_v6.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(outdir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(silent)], check=True)

    # ---- audio: same v5 chain (narration + music beds + world SFX) + the
    # extended scriptorium-foley bus as ONE MORE additive SFX input ----
    SND = ROOT / "sound_library" / "clips"
    MUS = ROOT / "music_library" / "clips"
    vdur = TOTAL

    foley_bus = foley.build_foley_bus(foley.storm_cue_list(v6_devices=True), energy, TOTAL)
    foley_raw = HERE / "_foley_v6.raw"
    np.asarray(foley_bus, dtype=np.float32).tofile(foley_raw)

    silence = "volume=0.18:enable='between(t,23.55,27.43)',"
    filt = (
        # v5 split [key] into ONE sidechain consumer (the music bed); v6 adds
        # a SECOND sidechain consumer (the new foley bus), and ffmpeg only
        # lets a labeled pad be consumed once -- asplit=3 gives each its own
        # copy of the narration key signal (caught by an isolated audio-mux
        # self-test against a dummy silent video BEFORE the full frame
        # render finished, not after).
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=3[main][key1][key2];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=29.5:d=2.5,volume=-9dB,{silence}anull[musA];"
        f"[3:a]{AFMT},adelay=28200|28200,atrim=0:{vdur},"
        f"afade=t=in:st=28.2:d=2.5,afade=t=out:st={vdur - 2.5:.1f}:d=2.5,"
        f"volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key1]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:18.0,volume=-16dB[creak];"
        f"[5:a]atrim=0:6.0,volume=-14dB,adelay=0|0,{AFMT}[thunder];"
        f"[6:a]atrim=0:0.9,lowpass=f=700,volume=0.55,adelay=27800|27800,{AFMT}[boom];"
        f"[7:a]{AFMT},adelay=30000|30000,atrim=0:{vdur},volume=-18dB[shore];"
        f"[8:a]{AFMT}[foleyraw];"
        f"[foleyraw][key2]sidechaincompress={SIDECHAIN}[foleyd];"
        f"[main][musd][creak][thunder][boom][shore][foleyd]amix=inputs=7:normalize=0,"
        f"alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", str(silent), "-i", str(SRC_AUDIO),
                    "-i", str(MUS / "lonely_searching_a.mp3"),
                    "-i", str(MUS / "sacred_grace_rise_a.mp3"),
                    "-i", str(SND / "boat_creak_oars.mp3"),
                    "-i", str(SND / "thunder_low_roll.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"),
                    "-i", str(SND / "sea_waves_shore.mp3"),
                    "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", str(foley_raw),
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    foley_raw.unlink(missing_ok=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
