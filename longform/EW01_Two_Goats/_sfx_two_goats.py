"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Two Goats film.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). NO sustained choir/musical pad (feedback-no-choir-pad-under-score)
— the orchestral score is the single musical bed. Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (589.2s narration, 591.7s scored). The bed is
summed under the scored film (amix normalize=0 so narration+score stay full, SFX only adds).
Output: EW01_Two_Goats_16x9_scored_sfx.mp4 (then caption it).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "EW01_Two_Goats_16x9_scored.mp4"
OUT = VIS / "EW01_Two_Goats_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 591.7

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",   0.0,   591.7, -40),  # faint sacred air base throughout
    ("crowd_murmur_distant",  0.0,    99.0, -36),  # M1 the hushed multitude outside the court
    ("rumble_deep_sub",      58.5,    99.0, -31),  # S4-S5 behind the veil / the cloud / holy weight
    ("rumble_deep_sub",      99.0,   122.0, -30),  # S6 the dead sons — strange fire judgment
    ("fire_crackling",       78.0,   195.0, -35),  # incense + the altar fire through the act
    ("wind_desert_bleak",   167.0,   213.0, -33),  # S9-S10 the scapegoat into "a land not inhabited"
    ("rumble_deep_sub",     313.0,   360.0, -32),  # S15 the ache — "pointing at a greater atonement"
    ("rumble_deep_sub",     360.0,   428.0, -29),  # M6 the reveal building (Christ, his own blood)
    ("wind_desert_bleak",   405.8,   428.0, -33),  # S19 "suffered without the gate"
    ("thunder_low_roll",    383.0,   428.0, -27),  # S18-S20 the cross / the iniquity laid on him
    ("veil_tearing",        428.4,   433.5, -25),  # S20 "the veil rent from the top to the bottom"
    ("crowd_murmur_distant",531.0,   558.0, -39),  # S24 boldness to enter — the quiet procession
    ("dawn_morning_warm",   451.0,   591.7, -29),  # M7 the invitation + close on Christ (warm resolve)
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
