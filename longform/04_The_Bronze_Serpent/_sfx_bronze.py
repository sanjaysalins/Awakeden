"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Bronze Serpent film.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). NO sustained choir/musical pad (feedback-no-choir-pad-under-score)
— the orchestral score is the single musical bed. Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (467.6s). Builds an SFX bed, sums it under
the scored film (amix normalize=0 so narration+score stay full and the SFX only adds, low).
Output: Bronze_Serpent_16x9_scored_sfx.mp4 (then caption it).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Bronze_Serpent_16x9_scored.mp4"
OUT = VIS / "Bronze_Serpent_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 467.6

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("wind_desert_bleak",      0.0,   467.6, -37),  # faint ancient desert air throughout
    ("air_hollow_desolate",    0.0,    73.5, -34),  # M1-M2 the dying, plague-stricken camp
    ("crowd_murmur_distant",  16.4,    43.3, -38),  # S2 the murmuring / despising
    ("rumble_deep_sub",       43.3,    73.5, -29),  # S3 the fiery serpents / judgment
    ("thunder_low_roll",      45.0,    53.5, -27),  # the serpents strike (subtle)
    ("crowd_murmur_distant",  63.5,   103.2, -36),  # S5/S27 the plea + confession to Moses
    ("fire_crackling",       111.9,   143.9, -29),  # S7/S22 the forge casting the bronze
    ("air_hollow_desolate",  143.9,   171.5, -35),  # S8-S10 the lifted pole, open desert awe
    ("fire_crackling",       171.5,   214.4, -33),  # S11/S23 Nicodemus by night, the lamp
    ("rumble_deep_sub",      214.4,   256.0, -31),  # M4 the cross weight
    ("thunder_low_roll",     227.7,   256.0, -26),  # S13 storm-light at the cross
    ("air_hollow_desolate",  256.0,   324.0, -34),  # M5 Hezekiah temple + the honest objection
    ("impact_low_boom",      269.0,   272.0, -15),  # S15 Hezekiah's strike (accent)
    ("rumble_deep_sub",      324.0,   354.5, -30),  # S17 made-a-curse, the tree
    ("dawn_morning_warm",    412.3,   467.6, -30),  # S20/S21 whosoever + risen-Christ hero (resolve)
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
