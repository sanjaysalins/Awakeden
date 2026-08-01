"""Bronze Serpent episode -- step 4: assemble the CORE cut (visual + real
narration audio only -- no score/sfx/captions/watermark, those are separate
follow-up stages). Real word-timed spread windows from `_TIMING.md` (forced
WhisperX alignment, 198/198 words, `_bronzeserpent_alignment.json`).

Architecture follows storm/_s4_assemble.py's own pattern (per the round's own
briefing: adapt the STRUCTURE, not Storm's specific paper-layer effects --
none of wash_creep/tide_mark/damp_cockle/still_water_mirror/raking_light-as-
a-per-frame-device are used here, this episode's device list is different):
  - ffmpeg extracts every clip to its own frame sequence (scale+crop to
    1080x1920 cover, 30fps), once, up front.
  - a shared ping-pong frame-index helper holds/bounces a clip's own frames
    across a real window that may be longer OR shorter than the clip's own
    rendered length (both happen in this episode -- s06/s07/s10 windows run
    longer than their clips; s01/s03/s04/s05/s09/s13 windows run shorter).
  - two REAL transition-class instances (not a crossfade dissolve): a single
    `LiftAwayPage` (panel_animator/lift_away.py) at the s07->s08 seam, ending
    exactly on s08's own first frame so the handoff is seamless; a single
    `TornOutPage` (panel_animator/page_transitions.py) at the s13->s14 seam,
    resolving onto s14's static landing still.
  - s08 gets ONE Scribed-Ink verse card for the John 3:14 quote (LAW 1: this
    is red-letter/Jesus speech, so it ARRIVES WHOLE -- a single scale+fade
    pop of the complete card, never a letter-by-letter build-up; ported from
    storm/_s4_assemble.py's own scribed_ink_card(), which itself already
    renders one complete static raster per call -- the per-glyph jitter is a
    baked-in HAND-LETTERED STYLE, not a temporal reveal, confirmed against
    poc_living_sketchbook/_lettering_compare/_render_candidates.py which has
    no reveal/progress parameter either).
  - narration.mp3 (69.309s, the REAL current file, see _TIMING.md's blocking
    finding re: stale sidecar metadata) is muxed in, then silence-padded via
    apad=whole_dur=TOTAL (never apad=pad_dur=X -- that bug is documented in
    the landing-hold-standard memory) to the INV-26 minimum: last word
    "live." finishes at 68.297s, so TOTAL must be >= 71.297s. TOTAL=71.5s
    here (0.2s safety margin, frame-exact at 30fps: 2145 frames).
  - `--test-window START END` for fast partial iteration, same CLI shape as
    Storm's own.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s4_assemble.py --test-window 33 38
  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s4_assemble.py
"""
import argparse
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT  # noqa: E402 -- reuse, don't duplicate

sys.path.insert(0, str(ROOT / "panel_animator"))
from candle_only import apply_candle, radius_from_keyframes, flicker_R  # noqa: E402
from lift_away import LiftAwayPage  # noqa: E402
from page_transitions import TornOutPage  # noqa: E402
from raking_light import scale_crop  # noqa: E402 -- reuse, don't duplicate

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
STILLS = HERE / "stills"
SRC_AUDIO = ROOT / "longform" / "EW04_Bronze_Serpent" / "v1" / "short" / "narration.mp3"
OUT = HERE / "BRONZESERPENT_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
LAST_WORD_END = 68.297   # "live." real offset, _TIMING.md
HOLD = 3.203              # >= INV-26's 3.0s minimum hold, small safety margin
TOTAL = 71.5              # LAST_WORD_END + HOLD, frame-exact at 30fps (2145 frames)

INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"
F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"

# (name, t0, t1) -- real word-timed windows, _TIMING.md's table (identical
# to the task brief's own table). s14 has no clip -- the landing is the
# TornOutPage's own resolved static frame, held to TOTAL.
SHOTS = [
    ("s01_wide", 0.387, 3.657),
    ("s02_grief", 3.657, 8.230),
    ("s03_complaint", 8.230, 11.433),
    ("s04_serpents", 11.433, 14.856),
    ("s05_intercession", 14.856, 18.798),
    ("s06_forge", 18.798, 28.105),
    ("s07_horizon", 28.105, 36.879),
    ("s08_typology", 36.879, 43.887),
    ("s09_shadow", 43.887, 46.386),
    ("s10_golgotha", 46.386, 52.572),
    ("s11_hearme", 52.572, 57.128),
    ("s12_echo", 57.128, 62.936),
    ("s13_lifted", 62.936, 66.723),
    ("s14_landing", 66.723, TOTAL),
]
CLIP_SHOTS = [s for s in SHOTS if s[0] != "s14_landing"]

# --- transitions -----------------------------------------------------------
# lift_away: calm turn, s07 (reflective Moses) -> s08 (insert page). Uses the
# class's own defaults (grab_t=0.9, lift_t=1.5, settle_t=2.3 => 2.3s active),
# placed so it FINISHES exactly on s08's real start -- the "below" frame is
# s08's own first frame, so the handoff at LIFT_AWAY_END is seamless (no pop).
LIFT_AWAY_END = 36.879
LIFT_AWAY_START = LIFT_AWAY_END - 2.3

# torn_out_page: the landing device, s13 (Christ lifted, radiant) -> s14 (the
# torn-page reveal). Class defaults (grab_t=0.9, rip_t=1.5, gone_t=1.95 =>
# 1.95s active), placed so it finishes exactly on s14's real start -- "below"
# is s14's own static landing frame.
TORN_OUT_END = 66.723
TORN_OUT_START = TORN_OUT_END - 1.95

# s08 verse card (John 3:14, LAW 1 whole-arrival): pops in just after the
# quote finishes being spoken ("up:" ends 42.316s per the alignment json),
# holds, hard exit margin (0.287s) before s09 begins at 43.887s -- matches
# Storm's own margin discipline (~0.33s) for the letterer law ("always give
# an overlay a hard exit margin before the next spread begins").
VERSE_CARD_T0, VERSE_CARD_T1 = 42.4, 43.6
VERSE_CARD_POPIN = 0.18

# --- candle-only device (s06_forge only, /candle-only skill) ---------------
# s06_forge's real window is 18.798-28.105s (9.307s) but its clip is a 5.0s
# $0 deterministic camera push-in fallback (3 real generative-animation
# attempts -- 2x Kling, 1x Seedance -- all invented the same hammer-strike
# motion; see _s3_animate.py's documented history) -- so shot_frame() below
# ping-pongs those 5s of pure camera motion to fill the remaining ~4.3s, the
# most mechanically-repeated stretch in the cut. Layered ON TOP of those
# ping-ponged frames (not replacing them), candle_only's radial light budget
# gives that stretch real, non-mechanical life: the glowing bronze on the
# anvil (a real drawn light source already in the approved still, not
# invented) reads tight/cold through the dread of forging the very thing
# killing them, then breathes open warm exactly as the spread's own turn
# lands on "look -- and live."
#
# LAMP anchor: authored from a hot-metal pixel isolation pass over
# stills/s06_forge.png (saturated R>190,B<130,R-B>70 pixels restricted to
# the anvil region, weighted centroid), eye-verified against a full-res crop
# -- it sits centered in the S-curve of glowing bronze where the tongs grip
# it on the anvil surface, not floating off into the tape margin or the
# hammer's own edge-highlight.
S06_LAMP_FRAC = (0.298, 0.691)
S06_LAMP = (int(W * S06_LAMP_FRAC[0]), int(H * S06_LAMP_FRAC[1]))

# R(t) keyframes, spread-relative seconds -- real word onsets from
# _bronzeserpent_alignment.json minus s06's own t0 (18.798):
#   0.000s "Instead" starts (18.798) -> 4.277s "high." ends (23.075):
#     CLOSED/tight, 420px -- the dread of forging the very thing killing
#     them ("Instead He told me to forge the image of the very thing
#     killing us, and lift it high.").
#   5.304s "The" starts (24.102): 480px, a faint first give -- the silence
#     from 23.075-24.102 already leans toward the turn.
#   6.370s "look" starts (25.168): 620px -- still mostly closed as the
#     turn's own verb is spoken ("The bitten had only to look").
#   7.639s "live." ends (26.437): 1450px -- FULLY OPEN, warm across nearly
#     the whole frame (face included) -- the swell is timed to land exactly
#     as "look -- and live" finishes, not before.
#   9.307s (window end, 28.105): held open through the rest of the spread.
S06_KEYFRAMES = [
    (0.000, 420.0),
    (4.277, 420.0),
    (5.304, 480.0),
    (6.370, 620.0),
    (7.639, 1450.0),
    (9.307, 1450.0),
]
S06_R = flicker_R(lambda t: radius_from_keyframes(S06_KEYFRAMES, t), seed=51, amplitude=10.0)


def ease(t):
    t = max(0.0, min(1.0, t))
    import math
    return 0.5 - 0.5 * math.cos(3.14159265 * t)


def _fit_font_size(lines, max_w, start=48, floor=26, step=2):
    """Shrink Kunstler font size until the longest line's summed char width
    fits max_w. Storm's own scribed_ink_card() hardcoded size=48 because its
    lines were short (<=23 chars); this episode's John 3:14 lines run
    30-36 chars, so the fit needs to be computed, not assumed."""
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    size = start
    while size > floor:
        font = ImageFont.truetype(F_KUNSTLER, size)
        widest = max(sum(td.textlength(ch, font=font) for ch in ln) for ln in lines)
        if widest <= max_w:
            return size
        size -= step
    return floor


def scribed_ink_card(lines, ref):
    """SCRIBED INK grammar (SKILL.md sec.5), ported from
    storm/_s4_assemble.py's scribed_ink_card(): hand-written script, seeded
    per-glyph baseline/rotation wobble (a STATIC hand-lettered style baked
    into the raster -- not a temporal reveal), underline swash, small
    rubric-red reference caps, no box ever. Font size auto-fit for this
    episode's longer lines (see _fit_font_size)."""
    font_size = _fit_font_size(lines, max_w=940)
    font = ImageFont.truetype(F_KUNSTLER, font_size)
    PUNCT = set(".,;:'\u2019\u201c\u201d?")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(font_size * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)

    def char_w(ch, f=font):
        return td.textlength(ch, font=f)

    line_h = int(font_size * 1.3)
    canvas = Image.new("RGBA", (W, line_h * len(lines) + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    rng = random.Random(26)
    y = 10
    last_lw = last_x0 = 0
    for ln in lines:
        tw = sum(char_w(ch) for ch in ln)
        x = (W - tw) / 2
        last_lw, last_x0 = tw, x
        cx = x
        for ch in ln:
            jy = rng.uniform(-2.2, 2.2)
            jr = rng.uniform(-1.1, 1.1)
            draw_font = font_punct if ch in PUNCT else font
            layer = Image.new("RGBA", (90, 100), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.text((10, 10), ch, font=draw_font, fill=(*INK, 255),
                     stroke_width=1 if ch in PUNCT else 0, stroke_fill=(*INK, 255))
            layer = layer.rotate(jr, resample=Image.BICUBIC, center=(10, 10 + 32))
            canvas.alpha_composite(layer, (int(cx) - 10, int(y + jy) - 10))
            cx += char_w(ch)
        y += line_h
    swash = [(last_x0, y - 6)]
    for i in range(1, 9):
        swash.append((last_x0 + last_lw * i / 8, y - 6 + rng.uniform(-3, 3)))
    d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
    rw = d.textlength(ref, font=ref_font)
    d.text(((W - rw) / 2, y + 16), ref, font=ref_font, fill=(*RUBRIC, 235))
    return canvas.crop((0, 0, W, y + 60))


VERSE_LINES = [
    "And as Moses lifted up the serpent",
    "in the wilderness, even so must the",
    "Son of man be lifted up:",
]
VERSE_REF = "JOHN 3:14"


def extract_clip_frames(work: Path) -> dict:
    """ffmpeg-extract every real clip to its own frame sequence, scale+crop
    to 1080x1920 cover (matches storm's own extraction step exactly)."""
    frames = {}
    for name, _t0, _t1 in CLIP_SHOTS:
        src = CLIPS / f"{name}.mp4"
        if not src.exists():
            raise SystemExit(f"missing clip: {src}")
        d = work / f"_{name}"
        d.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(src),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
             "-r", str(FPS), "-start_number", "0", str(d / "f%05d.png")],
            check=True,
        )
        seq = sorted(d.glob("f*.png"))
        if not seq:
            raise SystemExit(f"no frames extracted from {src}")
        frames[name] = seq
    return frames


def _ppindex(li: int, n: int) -> int:
    cyc = 2 * n - 2 if n > 1 else 1
    j = li % cyc
    if j >= n:
        j = cyc - j
    return max(0, min(n - 1, j))


def shot_frame(frames: dict, name: str, t: float, t0: float) -> Image.Image:
    """Ping-pong frame index (byte-identical logic to storm's own helper):
    holds a clip's own frames across ANY real window, whether the window
    runs longer (bounces back and forth rather than plain-modulo jump-
    cutting) or shorter (simply plays the clip's own opening span) than the
    clip's rendered length -- both happen across this episode's 14 spreads.

    Defensive re-glob on a missing path: a Windows-side race (antivirus/
    indexer touching just-written PNGs) was observed once mid-build where a
    path present in the original glob() had vanished by read time -- rather
    than trust a possibly-stale path list forever, re-discover this shot's
    own frames fresh from disk on a miss and retry once before failing loud."""
    seq = frames[name]
    li = int((t - t0) * FPS)
    j = _ppindex(li, len(seq))
    path = seq[j]
    if not path.exists():
        fresh = sorted(path.parent.glob("f*.png"))
        if not fresh:
            raise FileNotFoundError(f"{name}: no frames in {path.parent} (fresh reglob also empty)")
        frames[name] = fresh
        j = _ppindex(li, len(fresh))
        path = fresh[j]
    return Image.open(path).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-window", nargs=2, type=float, default=None,
                     help="render only [start end] seconds, for fast iteration (video only, no audio)")
    args = ap.parse_args()

    work = HERE / "_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    print("[extract] pulling frame sequences from all 13 real clips ...")
    frames = extract_clip_frames(work)
    for name, seq in frames.items():
        print(f"    {name}: {len(seq)} frames")

    # s14 landing still, scaled/cropped once, reused for every frame of the hold.
    s14_still = scale_crop(Image.open(STILLS / "s14_landing.png").convert("RGB"), W, H)

    # lift_away transition: above = s07's own frame at the transition's real
    # start instant; below = s08's own first frame (local t=0) -- so the
    # transition's settle_t lands byte-identical to normal s08 playback.
    s07_t0 = next(t0 for n, t0, t1 in SHOTS if n == "s07_horizon")
    s08_t0 = next(t0 for n, t0, t1 in SHOTS if n == "s08_typology")
    lift_above = shot_frame(frames, "s07_horizon", LIFT_AWAY_START, s07_t0)
    lift_below = shot_frame(frames, "s08_typology", s08_t0, s08_t0)
    lift_tr = LiftAwayPage(lift_above, lift_below)

    # torn_out_page transition: above = s13's own frame at the transition's
    # real start instant; below = s14's static landing still.
    s13_t0 = next(t0 for n, t0, t1 in SHOTS if n == "s13_lifted")
    torn_above = shot_frame(frames, "s13_lifted", TORN_OUT_START, s13_t0)
    torn_tr = TornOutPage(torn_above, s14_still)

    verse_card = scribed_ink_card(VERSE_LINES, VERSE_REF)

    print(f"[transitions] lift_away  {LIFT_AWAY_START:.3f}-{LIFT_AWAY_END:.3f}s")
    print(f"[transitions] torn_out   {TORN_OUT_START:.3f}-{TORN_OUT_END:.3f}s")
    print(f"[overlay]     verse card {VERSE_CARD_T0:.3f}-{VERSE_CARD_T1:.3f}s "
          f"(font size auto-fit, {len(VERSE_LINES)} lines)")

    n_frames = int(round(TOTAL * FPS))
    outdir = work / "grid"
    outdir.mkdir()

    if args.test_window:
        frame_range = range(int(args.test_window[0] * FPS), min(n_frames, int(args.test_window[1] * FPS)))
    else:
        frame_range = range(n_frames)

    for i in frame_range:
        t = i / FPS

        if LIFT_AWAY_START <= t < LIFT_AWAY_END:
            frame = lift_tr.compose(t - LIFT_AWAY_START).convert("RGBA")
        elif TORN_OUT_START <= t < TORN_OUT_END:
            frame = torn_tr.compose(t - TORN_OUT_START).convert("RGBA")
        else:
            shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
            name, t0, t1 = shot
            if name == "s14_landing":
                frame = s14_still.copy().convert("RGBA")
            else:
                frame = shot_frame(frames, name, t, t0).convert("RGBA")
                if name == "s06_forge":
                    # layer the candle-only light budget ON TOP of the
                    # ping-ponged push-in frame, spread-relative time (t-t0)
                    frame = apply_candle(frame.convert("RGB"), t - t0, S06_LAMP, S06_R).convert("RGBA")

        if VERSE_CARD_T0 <= t <= VERSE_CARD_T1:
            dt = t - VERSE_CARD_T0
            k = ease(min(1.0, dt / VERSE_CARD_POPIN))
            s2 = 1.28 - 0.28 * k
            oimg = verse_card.resize((int(verse_card.width * s2), int(verse_card.height * s2)), Image.LANCZOS)
            if k < 1.0:
                oimg.putalpha(oimg.split()[3].point(lambda v: int(v * k)))
            ox = int(W * 0.5 - oimg.width / 2)
            oy = int(H * 0.15 - oimg.height / 2)
            frame.alpha_composite(oimg, (ox, oy))

        frame.convert("RGB").save(outdir / f"g{i:05d}.png")

    if args.test_window:
        test_out = HERE / f"_test_{args.test_window[0]:.1f}_{args.test_window[1]:.1f}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
             "-start_number", str(frame_range.start),
             "-i", str(outdir / "g%05d.png"),
             "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
             str(test_out)],
            check=True,
        )
        print(f"[test] {test_out}")
        shutil.rmtree(work)
        return

    silent = HERE / "_silent.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
         "-i", str(outdir / "g%05d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", str(FPS), str(silent)],
        check=True,
    )

    if not SRC_AUDIO.exists():
        raise SystemExit(f"missing narration audio: {SRC_AUDIO}")

    filt = f"[1:a]{AFMT},apad=whole_dur={TOTAL}[aout]"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(silent), "-i", str(SRC_AUDIO),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}",
         str(OUT)],
        check=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
