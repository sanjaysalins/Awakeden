"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Seed of the Woman film.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). NO sustained choir/musical pad (feedback-no-choir-pad-under-score)
— the orchestral score is the single musical bed. Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (503.25s). Builds an SFX bed, sums it under
the scored film (amix normalize=0 so narration+score stay full and the SFX only adds, low).
Output: Seed_Of_The_Woman_16x9_scored_sfx.mp4 (then caption it).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Seed_Of_The_Woman_16x9_scored.mp4"
OUT = VIS / "Seed_Of_The_Woman_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 503.25

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",    0.0,   503.25, -39),  # faint ambient air base throughout
    ("river_well_water",       0.0,    53.0,  -34),  # M1 the Eden garden (the still river)
    ("rumble_deep_sub",       53.0,    94.5,  -31),  # M2 the weight of judgment entering
    ("thunder_low_roll",      53.0,    67.5,  -28),  # S4 death enters the world (subtle)
    ("river_well_water",      94.5,   158.5,  -37),  # M3 still in the garden (faint presence)
    ("rumble_deep_sub",      130.2,   140.2,  -29),  # S9 the promise / holy weight
    ("fire_crackling",       183.4,   202.7,  -31),  # S12 the manger lamp
    ("rumble_deep_sub",      319.9,   345.1,  -30),  # S18 head/heel — the exchange weight
    ("wind_desert_bleak",    345.1,   415.1,  -34),  # M6 Golgotha desolate air
    ("thunder_low_roll",     345.1,   392.0,  -26),  # S19/S20 the cross / the turn (storm)
    ("dawn_morning_warm",    392.0,   415.1,  -29),  # S21 the empty tomb (dawn resolve)
    ("river_well_water",     415.1,   466.5,  -37),  # M7 back in the garden (where it was spoken)
    ("dawn_morning_warm",    466.5,   503.25, -28),  # S24/S25 step out + risen-Christ hero (resolve)
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
