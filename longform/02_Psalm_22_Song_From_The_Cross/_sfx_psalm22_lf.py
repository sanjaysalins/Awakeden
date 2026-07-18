"""Ambient/SFX bed for Psalm 22 ('Song From The Cross'), same reverent
choir-free-under-the-score approach as Bronze Serpent's _sfx_bronze_inked.py
(feedback-no-choir-pad-under-score) -- ambience/accents only, layered UNDER
the Suno score, never a musical/choir pad.

No prior sfx script was found for this piece (the shipped LivingPage_Psalm22_
16x9_scored_sfx.mp4 predates a saved, reusable script) -- this is a fresh
cue sheet, authored from the piece's own beat captions
(v1/visual_16x9_inked/livingpage_full.spec.json), not a byte-exact recovery
of whatever ran before. Re-run after any score rebuild (2026-07-19: landing
hold extended to 3.0s, INV-26).

Arc: the forsaken cry (desolate) -> stripped/mocked (crowd) -> pierced hands
and feet / gambled garments (tension, then the exact detail) -> the honest
objection / scholarly weighing (quiet, contemplative) -> back to the cross,
the storm (weight) -> the turn to life, the congregation (warmth rising) ->
the ends of the earth streaming home, through the extended landing hold.

Output: LivingPage_Psalm22_16x9_scored_sfx.mp4
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "LivingPage_Psalm22_16x9_scored.mp4"
OUT = VIS / "LivingPage_Psalm22_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 421.2  # 418.2s narration + 3.0s landing hold (INV-26, 2026-07-19)

CUES = [
    ("wind_desert_bleak",     0.0,   418.2, -37),   # continuous base
    ("air_hollow_desolate",   0.0,    45.0, -34),   # the forsaken cry
    ("crowd_murmur_distant", 59.4,    95.0, -36),   # stripped, mocked, the witness statement
    ("rumble_deep_sub",     101.8,   143.0, -30),   # bones out of joint, the tension before "pierced"
    ("nail_strike_single",  121.3,   122.3, -22),   # "they pierced my hands and my feet"
    ("coins_clinking",      143.0,   166.0, -32),   # "they part my garments... cast lots"
    ("air_hollow_desolate", 166.0,   230.0, -38),   # the honest objection, quiet and contemplative
    ("thunder_low_roll",    233.6,   279.0, -28),   # back to the cross, the storm
    ("rumble_deep_sub",     233.6,   289.0, -32),   # weight under the storm
    ("heavenly_choir_soft", 289.2,   340.0, -35),   # the turn to life, the congregation
    ("impact_low_boom",     370.5,   372.0, -18),   # "It is finished."
    ("dawn_morning_warm",   339.9,   TOTAL, -30),   # the ends of the earth stream home, through the landing hold
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(str(c) for c in cmd[:8])}...\n{r.stderr[-1000:]}")


def main():
    if not SCORED.exists():
        raise SystemExit(f"missing scored film: {SCORED}")
    cue_files = []
    for i, (slug, start, end, gain) in enumerate(CUES):
        src = LIB / f"{slug}.mp3"
        if not src.exists():
            raise SystemExit(f"missing sound: {src}")
        d = end - start
        delay = int(start * 1000)
        out = WORK / f"cue_{i:02d}.wav"
        af = (f"volume={gain}dB,afade=t=in:d=1.0,"
              f"afade=t=out:st={max(0, d - 1.5):.2f}:d=1.5,"
              f"adelay={delay}|{delay}")
        run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{d:.3f}",
             "-af", af, "-ar", "44100", "-ac", "2", str(out)])
        cue_files.append(out)
        print(f"  cue {i:02d} {slug:22s} [{start:6.1f}-{end:6.1f}] {gain}dB")

    bed = WORK / "sfx_bed.wav"
    inputs = []
    for f in cue_files:
        inputs += ["-i", str(f)]
    amix = f"amix=inputs={len(cue_files)}:normalize=0:duration=longest[b]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", amix, "-map", "[b]",
         "-t", f"{TOTAL:.3f}", "-ar", "44100", "-ac", "2", str(bed)])
    print(f"[bed] {len(cue_files)} cues -> {bed.name}")

    run(["ffmpeg", "-y", "-i", str(SCORED), "-i", str(bed),
         "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         str(OUT)])
    print(f"[done] {OUT}")


if __name__ == "__main__":
    main()
