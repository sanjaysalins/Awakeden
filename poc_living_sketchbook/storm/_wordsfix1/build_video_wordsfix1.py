"""Storm wordsfix1 -- re-time the whole film to the new (owner-locked) narration. Re-renders the film's OWN device pass
(S4/S6 functions, unchanged math) on a NEW slot plan. Rules: every slot <= its clip (frames), trim only, NO loop/boomerang/ping-pong;
each clip used once; fail hard otherwise. Unspoken Keeper-hand note texts (Galilee..., storm wind fear, we bailed..., he stood up and,
not a breath of wind, still burning) are NOT drawn (burned words = spoken words).

  ..\\..\\..\\.venv\\Scripts\\python.exe build_video_wordsfix1.py [--test-window 14 17] [--mux-only]
Writes _silent_wordsfix1.mp4 and wordsfix1_pre.mp4 (video + new audio mix)."""
import argparse, json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ST = HERE.parent
ROOT = ST.parents[1]
sys.path.insert(0, str(ST))
import _s6_assemble as S6          # noqa
S4 = S6.S4
from pipeline.score_mix import AFMT, SIDECHAIN  # noqa
from held_breath import energy_envelope         # noqa
import scriptorium_foley as foley                # noqa
import raking_light, tide_mark, damp_cockle, still_water_mirror, wash_creep, blue_line, set_off as set_off_mod, annotators_circle  # noqa

W, H, FPS = 1080, 1920, 30
TOTAL = 56.4                      # last spoken word ends 53.12 -> 3.28 s landing hold
NFR = round(TOTAL * FPS)
g = lambda t: round(t * FPS) / FPS

# ------------------------------------------------------------------ alignment (new narration)
words = [w for w in json.load(open(HERE / "alignment_wordsfix1.json")) if any(c.isalnum() for c in w["w"])]
def wt(word, nth=0, key="start"):
    m = [w for w in words if w["w"].lower().strip(".,:;?") == word.lower().strip(".,:;?")]
    return m[nth][key]
assert abs(wt("faith", 0) - 19.63) < 0.05 and abs(wt("calm", 0) - 24.35) < 0.05

# ------------------------------------------------------------------ slot plan  (name, t0, t1)
SLOTS = [
    ("s01_waves",     0.00,   2.73),   # L1  The ship is covered with the waves.
    ("s04_asleep",    2.73,   6.83),   # L2  And in the stern - He is asleep.            (candle collapse on "asleep.")
    ("s06_shaken",    6.83,  11.454),  # L3 + "They wake Him:"
    ("s03_screaming", 11.454, 14.973), # the cry: Lord, save us: we perish.
    ("s07_eyes",     14.973, 16.73),   # He opens His eyes:
    ("s08_verse",    16.73,  20.81),   # Why are ye fearful, O ye of little faith?  (verse card)
    ("s09_rebuke",   20.81,  23.67),   # Then he arose, and rebuked the winds and the sea;
    ("s10_calm",     23.67,  25.83),   # and there was a great calm.
    ("s11_exactly",  25.83,  29.87),   # You'll say - easy for Him, He's God. Exactly.   (EXACTLY. stamp)
    ("s02_water",    29.87,  33.84),   # The One who could sleep through it ... a word.
    ("s12_knees",    33.84,  40.93),   # Maybe your own storm is loud right now. ... Lord, save us.
    ("s05_hands",    40.93,  43.03),   # He doesn't despise little faith.
    ("s13_landing",  43.03,  TOTAL),   # He grows it ... Their faith was little ... He is asking you - why are you afraid?
]
SLOTS = [(n, g(a), (g(b) if b != TOTAL else TOTAL)) for n, a, b in SLOTS]
SHOTS = SLOTS
BYNAME = {n: (a, b) for n, a, b in SLOTS}
FRAMES = {n: (round(a * FPS), round(b * FPS)) for n, a, b in SLOTS}
assert FRAMES[SLOTS[0][0]][0] == 0 and FRAMES[SLOTS[-1][0]][1] == NFR
for (n1, _, _), (n2, _, _) in zip(SLOTS, SLOTS[1:]):
    assert FRAMES[n1][1] == FRAMES[n2][0], (n1, n2)

CLIPS = ST / "clips"
def clip_frames30(n):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(CLIPS / f"{n}.mp4")], capture_output=True, text=True)
    return int(float(r.stdout) * FPS + 0.01)   # 4.041667 s -> 121 frames at 30 fps CFR
NEED = {}
for n, _, _ in SLOTS:
    need = FRAMES[n][1] - FRAMES[n][0]; have = clip_frames30(n); NEED[n] = need
    print(f"slot {n:14s} {BYNAME[n][0]:7.3f}-{BYNAME[n][1]:7.3f} need {need:4d} fr  clip {have:4d} fr  {'OK' if need <= have else 'FAIL'}")
    if need > have:
        sys.exit(f"FAIL: slot longer than its clip, no fills allowed: {n} need {need} have {have}")

# ------------------------------------------------------------------ device timing (all bound to new alignment)
T_ASLEEP = wt("asleep.", 0)                     # candle collapse
T_CALM = wt("calm.", 0)                         # gold flare
S04_T0, S04_T1 = BYNAME["s04_asleep"]
S6.T_ASLEEP = T_ASLEEP
S6.CANDLE_COLLAPSE_END = T_ASLEEP + S6.CANDLE_COLLAPSE_DUR
S6.CANDLE_REOPEN_START = S04_T1 - 0.5
S6.S04_T1 = S04_T1
S6.SHOTS = SHOTS; S6.SHOTS_BY_NAME = BYNAME; S4.SHOTS = SHOTS
S6.DROP_RAKING_S05 = False
S07_T0 = BYNAME["s07_eyes"][0]
S6.TORN_GRAB0 = S07_T0 - 0.65; S6.TORN_RIP0 = S6.TORN_GRAB0 + S6.TORN_GRAB_DUR; S6.TORN_GONE = S07_T0
CARD_T = BYNAME["s08_verse"][0]                 # "Why"
CARD_T1 = BYNAME["s09_rebuke"][0] - 0.33        # same 0.33 s before the next cut as the original
S4.CIRCLE_T0 = wt("faith?", 0); S4.CIRCLE_T_DRAW = S4.CIRCLE_T0 + 0.54
EXACTLY_T = wt("Exactly.", 0)
STAMP = (EXACTLY_T - 0.20, BYNAME["s11_exactly"][1] - 0.04)
asking = [w for w in words if w["w"] == "asking"][0]["start"]
HE_ASKING = asking - 0.14                       # "He" start
SETOFF_END = HE_ASKING - 0.6                    # original: card finished 0.6 s before "He is asking"
SETOFF_T0 = SETOFF_END - 2.5
KNEES_T = wt("storm", 0)                        # tide snaps back on "storm" (original: on "knees")
S13_T0 = BYNAME["s13_landing"][0]

def tide_curve(t):
    a_end = BYNAME["s04_asleep"][1]
    if t < a_end: return 0.20 * min(1.0, t / a_end)
    v_cut = BYNAME["s09_rebuke"][0]
    if t < v_cut: return 0.20                   # frozen under the KJV verse
    c_end = BYNAME["s11_exactly"][0]
    if t < c_end:
        k = (t - v_cut) / (c_end - v_cut); return 0.20 * (1 - k) + 0.03 * k
    if t < KNEES_T: return 0.03
    if t < KNEES_T + 1.2: return 0.20
    if t < S13_T0:
        k = (t - (KNEES_T + 1.2)) / (S13_T0 - (KNEES_T + 1.2)); return 0.20 * (1 - k)
    return 0.0
S4.storm_tide_curve = tide_curve

def paper_devices(frame, name, t, t0, t1, energy, res):
    if name == "s01_waves":
        if t < 0.9:
            frame = blue_line.apply_blue_line_reveal(res["blue_line_under_s01"], frame, S4.ease(min(1.0, t / 0.9)))
        adv = min(15.0, 15.0 * (t - t0) / max(0.01, t1 - t0))
        frame = wash_creep.apply_wash_creep(frame, advance_px=adv, mask=res["wash_s01"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)
    elif name in ("s03_screaming", "s06_shaken"):
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)
    elif name == "s04_asleep":
        adv = min(15.0, 15.0 * (t - t0) / max(0.01, t1 - t0))
        frame = wash_creep.apply_wash_creep(frame, advance_px=adv, mask=res["wash_s04"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)
    elif name == "s05_hands":
        frame = raking_light.apply_raking_light(frame, sweep_progress=(t - t0) / max(0.01, t1 - t0), tooth=res["tooth_s05"])
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=1.0 * energy)
    elif name in ("s07_eyes", "s08_verse", "s12_knees"):
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
    elif name == "s09_rebuke":
        taper = 1.0 - (t - t0) / max(0.01, t1 - t0)
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=taper * energy)
    elif name == "s10_calm":
        local = t - t0; frac = local / max(0.01, t1 - t0)
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = still_water_mirror.apply_still_water_mirror(frame, horizon_y=S4.STILL_WATER_HORIZON["s10_calm"], t=local, decay_tau=4.0, alpha=0.28)
        frame = raking_light.apply_gold_flare(frame, sweep_progress=0.5 + (t - T_CALM) / 3.0, gold_mask=res["gold_s10"], intensity=1.0)
        frame = damp_cockle.apply_damp_cockle(frame, t=t, amplitude=(1 - frac) * energy)
    elif name == "s11_exactly":
        local = t - t0
        frame = tide_mark.apply_tide_mark(frame, height_frac=tide_curve(t))
        frame = still_water_mirror.apply_still_water_mirror(frame, horizon_y=S4.STILL_WATER_HORIZON["s11_exactly"], t=local + 2.4, decay_tau=4.0, alpha=0.22)
    return frame
S4.apply_paper_devices = paper_devices         # S6.apply_paper_devices_v6 dispatches here (candle grade is added on top for s04)

# ------------------------------------------------------------------ audio mix
def mux(silent, out):
    vdur = TOTAL
    energy = energy_envelope(words, total_duration=TOTAL)
    cues = [foley.Cue("blue_line_stroke", 0.00, 0.90, "s01 ident stroke"),
            foley.Cue("wash_creep_wash", 0.0, BYNAME["s01_waves"][1], "s01 wash"),
            foley.Cue("wash_creep_wash", S04_T0, S04_T1 - S04_T0, "s04 wash"),
            foley.Cue("paper_tear", CARD_T, 0.40, "paperRip into verse"),
            foley.Cue("felt_press_tap", STAMP[0], 0.22, "EXACTLY. stamp"),
            foley.Cue("paper_tear", S6.TORN_RIP0, 0.35, "torn-out page rip")]
    bus = foley.build_foley_bus(cues, energy, TOTAL)
    raw = HERE / "_foley_wordsfix1.raw"; np.asarray(bus, dtype=np.float32).tofile(raw)
    SND = ROOT / "sound_library" / "clips"; MUS = ROOT / "music_library" / "clips"
    then_t = BYNAME["s09_rebuke"][0]
    musB_start = then_t + 0.77; boom_t = then_t + 0.37; shore_t = BYNAME["s10_calm"][0] + 0.21
    musA_out = then_t + 2.29 - 0.0                       # original: fade-out st 29.5 = "Then"+2.07
    musA_out = round(then_t + 2.07, 2)
    silence = f"volume=0.18:enable='between(t,{CARD_T},{BYNAME['s09_rebuke'][0]})',"
    creak_end = BYNAME["s07_eyes"][0]
    filt = (
        f"[1:a]{AFMT},apad=whole_dur={vdur},asplit=3[main][key1][key2];"
        f"[2:a]{AFMT},atrim=0:{vdur},afade=t=in:st=0:d=1.5,afade=t=out:st={musA_out}:d=2.5,volume=-9dB,{silence}anull[musA];"
        f"[3:a]{AFMT},adelay={int(musB_start*1000)}|{int(musB_start*1000)},atrim=0:{vdur},afade=t=in:st={musB_start:.2f}:d=2.5,"
        f"afade=t=out:st={vdur - 2.5:.2f}:d=2.5,volume=-8dB[musB];"
        f"[musA][musB]amix=inputs=2:normalize=0[mus];"
        f"[mus][key1]sidechaincompress={SIDECHAIN}[musd];"
        f"[4:a]{AFMT},atrim=0:{creak_end:.2f},afade=t=out:st={creak_end-0.6:.2f}:d=0.6,volume=-16dB[creak];"
        f"[5:a]atrim=0:6.0,volume=-14dB,adelay=0|0,{AFMT}[thunder];"
        f"[6:a]atrim=0:0.9,lowpass=f=700,volume=0.55,adelay={int(boom_t*1000)}|{int(boom_t*1000)},{AFMT}[boom];"
        f"[7:a]{AFMT},adelay={int(shore_t*1000)}|{int(shore_t*1000)},atrim=0:{vdur},volume=-18dB[shore];"
        f"[8:a]{AFMT}[foleyraw];"
        f"[foleyraw][key2]sidechaincompress={SIDECHAIN}[foleyd];"
        f"[main][musd][creak][thunder][boom][shore][foleyd]amix=inputs=7:normalize=0,alimiter=limit=0.97,aresample=44100[mix]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(HERE / "narration_wordsfix1.wav"),
                    "-i", str(MUS / "lonely_searching_a.mp3"), "-i", str(MUS / "sacred_grace_rise_a.mp3"),
                    "-i", str(SND / "boat_creak_oars.mp3"), "-i", str(SND / "thunder_low_roll.mp3"),
                    "-i", str(SND / "impact_low_boom.mp3"), "-i", str(SND / "sea_waves_shore.mp3"),
                    "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", str(raw),
                    "-filter_complex", filt, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{vdur}", str(out)], check=True)
    raw.unlink(missing_ok=True)

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-window", nargs=2, type=float, default=None)
    ap.add_argument("--mux-only", action="store_true")
    ap.add_argument("--prep", action="store_true", help="extract clip frames once")
    ap.add_argument("--chunk", nargs=2, type=int, default=None, help="render frames [a,b) into shared _frames/grid")
    ap.add_argument("--assemble", action="store_true", help="grid -> silent video -> mux")
    args = ap.parse_args()
    silent = HERE / "_silent_wordsfix1.mp4"
    pre = HERE / "wordsfix1_pre.mp4"
    if args.mux_only:
        mux(silent, pre); print("ok", pre); return
    work = HERE / "_frames"
    if args.assemble:
        out = work / "grid"
        assert len(list(out.glob("g*.png"))) == NFR, len(list(out.glob("g*.png")))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(out / "g%05d.png"),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(silent)], check=True)
        mux(silent, pre); print("ok", pre); return
    if not args.chunk:
        if work.exists(): shutil.rmtree(work)
        work.mkdir()
    frames = {}
    for n, _, _ in SLOTS:
        d = work / f"_{n}"
        if args.chunk:
            frames[n] = sorted(d.glob("f*.png")); assert len(frames[n]) >= NEED[n], n; continue
        d.mkdir()
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(CLIPS / f"{n}.mp4"), "-frames:v", str(NEED[n]),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-r", str(FPS), str(d / "f%05d.png")], check=True)
        frames[n] = sorted(d.glob("f*.png"))
        assert len(frames[n]) >= NEED[n], (n, len(frames[n]), NEED[n])
    if args.prep:
        print("prep ok"); return
    verse_card = S4.scribed_ink_card(["Why are ye fearful,", "O ye of little faith?"], "MATTHEW 8:26")
    exactly_stamp = S4.stamped_text("EXACTLY.", S4.F_ZILLA, 78, S4.RUBRIC, letter_spacing=2)
    res = S4.build_paper_resources(frames)
    energy = energy_envelope(words, total_duration=TOTAL)
    grain = S4.noise_layers()
    out = work / "grid"; out.mkdir(exist_ok=True)
    rng = range(*args.chunk) if args.chunk else range(NFR) if not args.test_window else range(int(args.test_window[0] * FPS), int(args.test_window[1] * FPS))
    prev_last = {"img": None}; torn_above = {"img": None}
    for i in rng:
        t = i / FPS
        if S6.TORN_GRAB0 <= t < S6.TORN_GONE:
            if torn_above["img"] is None:
                tg = g(S6.TORN_GRAB0)
                nm = "s03_screaming"; a0 = BYNAME[nm][0]
                fr = Image.open(frames[nm][round((tg - a0) * FPS)]).convert("RGB")
                torn_above["img"] = paper_devices(fr, nm, tg, *BYNAME[nm], energy(tg), res).convert("RGBA")
            below = S6.below_page_frame(t, frames, res, energy)
            frame = S6.torn_page_frame(torn_above["img"], below, t)
            gg = grain[i % len(grain)]
            frame = Image.composite(frame.point(lambda v: min(255, v + 6)), frame, gg.point(lambda v: 22 if v > 236 else 0))
            frame.save(out / f"g{i:05d}.png"); continue
        name = next(n for n, _, _ in SLOTS if FRAMES[n][0] <= i < FRAMES[n][1])
        t0, t1 = BYNAME[name]
        li = i - FRAMES[name][0]
        assert 0 <= li < NEED[name]                    # straight playback only: no loop / reverse / hold
        frame = Image.open(frames[name][li]).convert("RGB")
        if name == "s08_verse" and t < CARD_T + 0.4 and prev_last["img"] is not None:
            frame = Image.composite(frame, prev_last["img"], S4.transition_mask("paperRip", S4.ease((t - CARD_T) / 0.4)))
        e = energy(t)
        frame = S6.apply_paper_devices_v6(frame, name, t, t0, t1, e, res)
        if name == "s13_landing":
            p = S4.ease(min(1.0, max(0.0, (t - SETOFF_T0) / 2.5)))
            if p > 0:
                frame = set_off_mod.apply_set_off(frame.convert("RGBA"), verse_card, p).convert("RGB")
        if STAMP[0] <= t <= STAMP[1]:
            k = S4.ease(min(1.0, (t - STAMP[0]) / 0.18)); s2 = 1.28 - 0.28 * k
            oimg = exactly_stamp.resize((int(exactly_stamp.width * s2), int(exactly_stamp.height * s2)), Image.LANCZOS)
            if k < 1.0: oimg.putalpha(oimg.split()[3].point(lambda v: int(v * k)))
            frame.paste(oimg, (int(W * 0.5 - oimg.width / 2), max(S4.WM_TOP, int(H * 0.20 - oimg.height / 2))), oimg)
        if CARD_T <= t <= CARD_T1:
            frame = frame.convert("RGBA")
            frame.alpha_composite(verse_card, (int(W * 0.5 - verse_card.width / 2), max(S4.WM_TOP, int(H * 0.134 - verse_card.height / 2))))
            if t >= S4.CIRCLE_T0:
                cp = max(0.0, min(1.0, (t - S4.CIRCLE_T0) / (S4.CIRCLE_T_DRAW - S4.CIRCLE_T0)))
                frame = annotators_circle.apply_annotators_circle(frame.convert("RGB"), S4.FAITH_BBOX, cp, color=annotators_circle.RUBRIC)
            frame = frame.convert("RGB")
        gg = grain[i % len(grain)]
        frame = Image.composite(frame.point(lambda v: min(255, v + 6)), frame, gg.point(lambda v: 22 if v > 236 else 0))
        if i == FRAMES[name][1] - 1: prev_last["img"] = frame.copy()
        frame.save(out / f"g{i:05d}.png")
    if args.chunk:
        print("chunk done", args.chunk); return
    if args.test_window:
        tw = HERE / f"_test_{args.test_window[0]:.1f}_{args.test_window[1]:.1f}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-start_number", str(rng.start), "-i", str(out / "g%05d.png"),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(tw)], check=True)
        print("[test]", tw); shutil.rmtree(work); return
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(out / "g%05d.png"),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), str(silent)], check=True)
    shutil.rmtree(work)
    mux(silent, pre)
    print("ok", pre)

if __name__ == "__main__":
    main()
