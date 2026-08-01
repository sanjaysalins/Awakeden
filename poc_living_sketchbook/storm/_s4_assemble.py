"""Storm episode — step 4: assemble the full 63.0s episode. Real word-timed
spread windows (from the offline WhisperX forced-alignment, 172/172 exact).

THE TWEAK THIS EPISODE PROVES: SCRIBED INK (SKILL.md sec.5) for the Matthew
8:26 verse -- the recommended default lettering, never shipped past a still
test until now. Ink Stamp for the "Exactly." display beat. No card/box
either way. Multi-stage hard cut for the rebuke/calm pair (s09/s10) --
straight hard cut, no transition, per SKILL.md sec.3 (the CUT carries the
event). One paperRip transition into the verse. Grain-boil, cold-to-warm
score arc turning on the rebuke, near-silence under the KJV quote.

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s4_assemble.py
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
import wash_creep
import tide_mark
import damp_cockle
import still_water_mirror
import raking_light
import set_off as set_off_mod
import blue_line
import annotators_circle
from held_breath import energy_envelope  # noqa

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
SRC_AUDIO = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\20 He Was Asleep in the Storm\v1\narration.mp3")
OUT = HERE / "STORM_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
TOTAL = 63.0   # 59.40s last spoken word + 3.6s tail -> INV-26 hold >=3.0s
INK = (35, 30, 26)
RUBRIC = (150, 26, 22)
GOLD = (185, 146, 74)
FADED_INK = (75, 62, 48)

F_ZILLA = "C:/Windows/Fonts/ZillaSlab-SemiBold.ttf"
F_KUNSTLER = "C:/Windows/Fonts/KUNSTLER.TTF"

# (name, t0, t1) -- word-timed from _storm_alignment.json
SHOTS = [
    ("s01_waves", 0.00, 2.10),
    ("s02_water", 2.10, 4.25),
    ("s03_screaming", 4.25, 6.67),
    ("s04_asleep", 6.67, 10.84),
    ("s05_hands", 10.84, 18.36),
    ("s06_shaken", 18.36, 21.95),
    ("s07_eyes", 21.95, 23.55),
    ("s08_verse", 23.55, 27.43),
    ("s09_rebuke", 27.43, 29.79),
    ("s10_calm", 29.79, 32.20),
    ("s11_exactly", 32.20, 39.97),
    ("s12_knees", 39.97, 49.11),
    ("s13_landing", 49.11, TOTAL),
]
TRANSITIONS = {23.55: "paperRip"}   # into the verse; s09/s10 stay a hard cut
WM_TOP = 160

STILLS = HERE / "stills"
ALIGN_PATH = HERE / "_storm_alignment.json"

# Fable's paper-layer enhancement pass (2026-07-29, user-approved, all $0
# deterministic panel_animator/ devices, tested + verified independently
# before this integration). Tide-Mark curve authored to the narration's own
# word timing -- rises with the fear, freezes under Scripture, recedes at
# the calm, snaps back to the old high-water height on "knees" (43.16s),
# the narration's own callback from their fear to yours.
def storm_tide_curve(t):
    if t < 6.67:
        return 0.20 * min(1.0, t / 6.67)
    if t < 23.55:
        return 0.20
    if t < 27.43:
        return 0.20  # frozen under the KJV verse -- the page does not editorialise under Scripture
    if t < 32.20:
        k = (t - 27.43) / (32.20 - 27.43)
        return 0.20 * (1 - k) + 0.03 * k
    if t < 43.16:
        return 0.03
    if t < 44.36:
        return 0.20  # snaps back to the old high-water height on "knees"
    if t < 49.11:
        k = (t - 44.36) / (49.11 - 44.36)
        return 0.20 * (1 - k)
    return 0.0


# horizon rows found by eye-check (detect_horizon() proved unreliable on
# this style's painted skies per still-water-mirror's own Locked Lessons --
# always verify by eye per still, never trust the heuristic blind).
STILL_WATER_HORIZON = {"s10_calm": 760, "s11_exactly": 700}

# Annotator's Circle (_FABLE_ROUND4_REMOTION_SKILLS.md sec.2): the pixel bbox
# of the word "faith" inside verse_card's own scribed_ink_card() raster --
# NOT eyeballed. Computed by replicating scribed_ink_card's own char_w()
# cursor math (line 2 "O ye of little faith?", chars 15-19), then verified
# pixel-identical against the real function's own output and against a
# rendered debug rectangle before use. Card-relative tight alpha-bbox was
# (578, 84, 662, 123); the card pastes onto the frame at ox=0 (card width ==
# frame width W, settled pop-in) and oy=160 (== WM_TOP, since
# int(H*0.134 - card.height/2) == 160 for this card's height of 194) --
# so the frame-absolute bbox is (578, 244, 662, 283).
FAITH_BBOX = (578, 244, 662, 283)
# "faith?" is spoken 26.46-26.782s (_storm_alignment.json, first occurrence,
# inside the s08_verse/verse-card window 23.75-27.10s). The circle draws
# across 26.46 -> 27.00s (two passes), settling with ~0.10s to spare before
# the verse card itself exits at 27.10 -- it must never outlive its host card.
CIRCLE_T0, CIRCLE_T_DRAW = 26.46, 27.00


def ease(t):
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def wrap_text(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def stamped_text(text, font_path, size, color, letter_spacing=0, max_w=None):
    """INK STAMP grammar (SKILL.md sec.5): glyph mask x blurred noise, no box."""
    font = ImageFont.truetype(font_path, size)
    tmp = Image.new("L", (10, 10))
    td = ImageDraw.Draw(tmp)
    lines = wrap_text(text, font, max_w, td) if max_w else [text]
    line_h = int(size * 1.2)
    if letter_spacing:
        line_widths = [sum(td.textlength(ch, font=font) for ch in ln) +
                       letter_spacing * (len(ln) - 1) for ln in lines]
    else:
        line_widths = [td.textlength(ln, font=font) for ln in lines]
    tw = int(max(line_widths)) + 4
    th = line_h * len(lines) + 4
    pad = 24
    stamp = Image.new("L", (tw + 2 * pad, th + 2 * pad), 0)
    sd = ImageDraw.Draw(stamp)
    for i, ln in enumerate(lines):
        y = pad + i * line_h
        x0 = pad + (tw - line_widths[i]) / 2
        if letter_spacing:
            x = x0
            for ch in ln:
                sd.text((x, y), ch, font=font, fill=255)
                x += td.textlength(ch, font=font) + letter_spacing
        else:
            sd.text((x0, y), ln, font=font, fill=255)
    rng = random.Random(len(text))
    noise = Image.new("L", stamp.size)
    noise.putdata([rng.randint(70, 255) for _ in range(stamp.width * stamp.height)])
    noise = noise.filter(ImageFilter.GaussianBlur(1.0))
    a = (np.array(stamp).astype(float) / 255.0) * (np.array(noise).astype(float) / 255.0)
    a = np.clip(a * 1.5, 0, 1) * 255
    alpha = Image.fromarray(a.astype("uint8"))
    inked = Image.new("RGBA", stamp.size, (*color, 0))
    inked.putalpha(alpha)
    return inked


def scribed_ink_card(lines, ref):
    """SCRIBED INK grammar (SKILL.md sec.5, poc_living_sketchbook/
    _lettering_compare/_render_candidates.py's render_scribed_ink -- the
    device this episode exists to prove in motion): hand-written script,
    letter-by-letter seeded baseline/rotation wobble, underline swash, small
    rubric-red reference caps. NO box, ever. Kunstler's comma/period glyphs
    are nearly invisible at body size -- draw punctuation from a larger
    stroked instance of the same font (fixed bug, backported per SKILL.md)."""
    font = ImageFont.truetype(F_KUNSTLER, 48)
    PUNCT = set(".,;:'\u2019\u201c\u201d?")
    font_punct = ImageFont.truetype(F_KUNSTLER, int(48 * 1.7))
    ref_font = ImageFont.truetype(F_ZILLA, 24)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)

    def char_w(ch, f=font):
        return td.textlength(ch, font=f)

    line_h = 62
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
    swash = [(last_x0, y - 6)]
    for i in range(1, 9):
        swash.append((last_x0 + last_lw * i / 8, y - 6 + rng.uniform(-3, 3)))
    d.line(swash, fill=(*RUBRIC, 255), width=3, joint="curve")
    rw = d.textlength(ref, font=ref_font)
    d.text(((W - rw) / 2, y + 16), ref, font=ref_font, fill=(*RUBRIC, 235))
    return canvas.crop((0, 0, W, y + 60))


def noise_layers():
    layers = []
    for seed in range(8):
        rng = random.Random(200 + seed)
        small = Image.new("L", (W // 4, H // 4))
        small.putdata([rng.randint(0, 255) for _ in range(small.width * small.height)])
        layers.append(small.resize((W, H), Image.BILINEAR))
    return layers


def transition_mask(kind, k):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    rng = random.Random(77)
    edge = int((W + 300) * k) - 150
    pts = [(0, 0)]
    y = 0
    while y <= H:
        pts.append((edge + rng.randint(-70, 70), y))
        y += 60
    pts += [(0, H)]
    d.polygon(pts, fill=255)
    return m.filter(ImageFilter.GaussianBlur(2))


def build_paper_resources(frames):
    """Precompute the per-still resources the paper-layer devices need ONCE
    (masks/plates), reused every frame within that spread's window --
    per each device's own docstring guidance, never recomputed per-frame."""
    res = {}

    def first(name):
        return Image.open(frames[name][0]).convert("RGB")

    res["wash_s01"] = wash_creep.isolate_storm_wash(first("s01_waves"))
    res["wash_s04"] = wash_creep.isolate_storm_wash(first("s04_asleep"))
    res["tooth_s05"] = raking_light.paper_tooth_highpass(first("s05_hands"))
    res["tooth_s10"] = raking_light.paper_tooth_highpass(first("s10_calm"))
    res["gold_s10"] = raking_light.isolate_gold_leaf(first("s10_calm"))

    s01_still = damp_cockle.scale_crop(Image.open(STILLS / "s01_waves.png").convert("RGB"), W, H)
    res["blue_line_under_s01"] = blue_line.make_underdrawing_plate(s01_still)

    return res


def apply_paper_devices(frame, name, t, t0, t1, energy, res):
    """The Fable enhancement pass (2026-07-29): everything here acts on the
    PAPER the drawing sits on, not the drawing itself -- $0 deterministic,
    structurally incapable of inventing doctrine (see each device's own
    SKILL.md). Ordering: wash (color-region) -> tide (bottom-band stain) ->
    mirror (water reflection) -> raking light (global brightness sweep) ->
    damp cockle (geometric warp, last so it doesn't misalign the masks the
    earlier steps computed against the undisplaced frame)."""
    if name == "s01_waves":
        if t < 0.9:
            progress = ease(min(1.0, t / 0.9))
            frame = blue_line.apply_blue_line_reveal(res["blue_line_under_s01"], frame, progress)
        local = t - t0
        adv = min(15.0, 15.0 * local / max(0.01, t1 - t0))
        frame = wash_creep.apply_wash_creep(frame, advance_px=adv, mask=res["wash_s01"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)

    elif name == "s03_screaming":
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)

    elif name == "s04_asleep":
        local = t - t0
        adv = min(15.0, 15.0 * local / max(0.01, t1 - t0))
        frame = wash_creep.apply_wash_creep(frame, advance_px=adv, mask=res["wash_s04"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)

    elif name == "s05_hands":
        sweep = (t - t0) / max(0.01, t1 - t0)
        frame = raking_light.apply_raking_light(frame, sweep_progress=sweep, tooth=res["tooth_s05"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)

    elif name == "s06_shaken":
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)

    elif name in ("s07_eyes", "s08_verse", "s12_knees"):
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))

    elif name == "s09_rebuke":
        taper = 1.0 - (t - t0) / max(0.01, t1 - t0)
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=taper * energy)

    elif name == "s10_calm":
        local = t - t0
        frac = local / max(0.01, t1 - t0)
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = still_water_mirror.apply_still_water_mirror(
            frame, horizon_y=STILL_WATER_HORIZON["s10_calm"], t=local, decay_tau=4.0, alpha=0.28)
        # gold flare: the light finds the leaf exactly on "and there was a
        # great calm" (30.96s) -- a short sweep centered on that instant,
        # not the same slow sweep used for s05 (a different beat, its own pass).
        flare_sweep = 0.5 + (t - 30.96) / 3.0  # crosses the gold strip mid-sweep at 30.96s
        frame = raking_light.apply_gold_flare(frame, sweep_progress=flare_sweep,
                                               gold_mask=res["gold_s10"], intensity=1.0)
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=(1 - frac) * energy)

    elif name == "s11_exactly":
        local = t - t0
        frame = tide_mark.apply_tide_mark(frame, height_frac=storm_tide_curve(t))
        frame = still_water_mirror.apply_still_water_mirror(
            frame, horizon_y=STILL_WATER_HORIZON["s11_exactly"], t=local + 2.4, decay_tau=4.0, alpha=0.22)

    return frame


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-window", nargs=2, type=float, default=None,
                     help="render only [start end] seconds, for fast iteration")
    args = ap.parse_args()

    work = HERE / "_frames"
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

    verse_card = scribed_ink_card(
        ["Why are ye fearful,", "O ye of little faith?"], "MATTHEW 8:26")
    exactly_stamp = stamped_text("EXACTLY.", F_ZILLA, 78, RUBRIC, letter_spacing=2)

    paper_res = build_paper_resources(frames)
    align_words = __import__("json").load(open(ALIGN_PATH, encoding="utf-8"))
    energy = energy_envelope(align_words, total_duration=TOTAL)

    OVERLAYS = [  # (t0, t1, img, cx_frac, cy_frac)
        # s08_verse: the lap/robe area is too busy with linework for thin
        # ink strokes to read (found on first QC pass -- the card was there
        # but nearly invisible against the tunic folds). The stormy sky
        # above his head is clean open space, well clear of the face
        # (letterer law). Hard exit margin before s09 starts at 27.43.
        (23.75, 27.10, verse_card, 0.5, 0.134),
        (35.05, 36.50, exactly_stamp, 0.5, 0.20),
    ]

    grain = noise_layers()
    n_frames = int(TOTAL * FPS)
    outdir = work / "grid"
    outdir.mkdir()

    if args.test_window:
        frame_range = range(int(args.test_window[0] * FPS), int(args.test_window[1] * FPS))
    else:
        frame_range = range(n_frames)

    prev_last = {"img": None}
    for i in frame_range:
        t = i / FPS
        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1 = shot
        seq = frames[name]
        li = int((t - t0) * FPS)
        n = len(seq)
        cyc = 2 * n - 2 if n > 1 else 1
        j = li % cyc
        if j >= n:
            j = cyc - j
        frame = Image.open(seq[j]).convert("RGB")

        for tt, kind in TRANSITIONS.items():
            if tt <= t < tt + 0.4 and prev_last["img"] is not None:
                k = ease((t - tt) / 0.4)
                mask = transition_mask(kind, k)
                frame = Image.composite(frame, prev_last["img"], mask)

        e = energy(t)
        frame = apply_paper_devices(frame, name, t, t0, t1, e, paper_res)

        if name == "s13_landing":
            so_progress = ease(min(1.0, max(0.0, (t - 53.5) / 2.5)))
            if so_progress > 0:
                frame = set_off_mod.apply_set_off(frame.convert("RGBA"), verse_card, so_progress).convert("RGB")

        for (oi0, oi1, img, cxf, cyf) in OVERLAYS:
            if oi0 <= t <= oi1:
                dt = t - oi0
                k = ease(min(1.0, dt / 0.18))
                s2 = 1.28 - 0.28 * k
                oimg = img.resize((int(img.width * s2), int(img.height * s2)), Image.LANCZOS)
                if k < 1.0:
                    oimg.putalpha(oimg.split()[3].point(lambda v: int(v * k)))
                ox = int(W * cxf - oimg.width / 2)
                oy = max(WM_TOP, int(H * cyf - oimg.height / 2))
                frame.paste(oimg, (ox, oy), oimg)

                # Annotator's Circle -- the narrator speaks "faith" and a
                # hand-drawn ink ellipse circles it on the card, two passes
                # (SKILL.md annotators-circle). Only ever runs while its host
                # card is on screen (this whole block is inside the card's own
                # oi0<=t<=oi1 window) and only once the pop-in settle is done.
                if img is verse_card and k >= 1.0 and t >= CIRCLE_T0:
                    circle_progress = max(0.0, min(
                        1.0, (t - CIRCLE_T0) / (CIRCLE_T_DRAW - CIRCLE_T0)))
                    frame = annotators_circle.apply_annotators_circle(
                        frame, FAITH_BBOX, circle_progress,
                        color=annotators_circle.RUBRIC)

        g = grain[i % len(grain)]
        frame = Image.composite(
            frame.point(lambda v: min(255, v + 6)), frame,
            g.point(lambda v: 22 if v > 236 else 0))

        if abs(t + 1 / FPS - t1) < 1 / FPS:
            prev_last["img"] = frame.copy()
        frame.save(outdir / f"g{i:05d}.png")

    if args.test_window:
        test_out = HERE / f"_test_{args.test_window[0]:.1f}_{args.test_window[1]:.1f}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                        "-start_number", str(frame_range.start),
                        "-i", str(outdir / "g%05d.png"),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                        str(test_out)], check=True)
        print(f"[test] {test_out}")
        shutil.rmtree(work)
        return

    silent = HERE / "_silent.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
                    "-i", str(outdir / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), str(silent)], check=True)

    SND = ROOT / "sound_library" / "clips"
    MUS = ROOT / "music_library" / "clips"
    vdur = TOTAL
    # near-silence + one low tone under the KJV quote (s08, 23.55-27.43) --
    # the voice owns the moment (SKILL.md sec.7).
    silence = "volume=0.18:enable='between(t,23.55,27.43)',"
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=2[main][key];"
        # cold bed under the storm, fades as the calm arrives
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,"
        f"afade=t=out:st=29.5:d=2.5,volume=-9dB,{silence}anull[musA];"
        # warm bed rising from the rebuke/calm pivot through the landing
        f"[3:a]{AFMT},adelay=28200|28200,atrim=0:{vdur},"
        f"afade=t=in:st=28.2:d=2.5,afade=t=out:st={vdur - 2.5:.1f}:d=2.5,"
        f"volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        # world SFX: boat/storm creak+thunder under the chaos, one low boom
        # on the rebuke, calm shore wash under the resolution
        f"[4:a]{AFMT},atrim=0:18.0,volume=-16dB[creak];"
        f"[5:a]atrim=0:6.0,volume=-14dB,adelay=0|0,{AFMT}[thunder];"
        f"[6:a]atrim=0:0.9,lowpass=f=700,volume=0.55,adelay=27800|27800,{AFMT}[boom];"
        f"[7:a]{AFMT},adelay=30000|30000,atrim=0:{vdur},volume=-18dB[shore];"
        f"[main][musd][creak][thunder][boom][shore]amix=inputs=6:normalize=0,"
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
                    "-filter_complex", filt,
                    "-map", "0:v", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-t", f"{vdur}",
                    str(OUT)], check=True)
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
