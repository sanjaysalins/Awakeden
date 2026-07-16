"""Lay the SAME reverent, choir-free ambient/SFX bed as _sfx_bronze.py UNDER the
graphic-novel rebuild's scored film (2026-07-16 test). Cues/timings are IDENTICAL
(sound design doesn't change with art style; the scene ids/timings are unchanged
from the archived Baroque plan) -- only the visual_16x9 path -> visual_16x9_inked
and the film name change.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). Reuse-only from sound_library ($0).
Output: BronzeSerpent_16x9_scored_sfx.mp4
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
SCORED = VIS / "BronzeSerpent_16x9_scored.mp4"
OUT = VIS / "BronzeSerpent_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 477.77  # matches BronzeSerpent_16x9_scored.mp4 (dense rebuild, 2026-07-16)

# Cue timings are tied to NARRATIVE time (what's being said), not to specific beat
# boundaries -- the underlying narration.mp3 is byte-identical to the original cut,
# so these word-timeline anchors still land on the same moments after the dense
# beat-authoring rebuild. Only the tail (dawn_morning_warm/wind_desert_bleak) end
# points are nudged to the new total.
CUES = [
    ("wind_desert_bleak",      0.0,   477.7, -37),
    ("air_hollow_desolate",    0.0,    76.9, -34),
    ("crowd_murmur_distant",  16.4,    43.3, -38),
    ("rumble_deep_sub",       43.3,    76.9, -29),
    ("thunder_low_roll",      45.0,    53.5, -27),
    ("crowd_murmur_distant",  63.5,   109.6, -36),
    ("fire_crackling",       118.4,   150.4, -29),
    ("air_hollow_desolate",  150.4,   178.0, -35),
    ("fire_crackling",       178.0,   220.9, -33),
    ("rumble_deep_sub",      220.9,   262.5, -31),
    ("thunder_low_roll",     234.2,   262.5, -26),
    ("air_hollow_desolate",  262.5,   330.5, -34),
    ("impact_low_boom",      275.5,   278.5, -15),
    ("rumble_deep_sub",      330.5,   361.0, -30),
    ("dawn_morning_warm",    418.9,   477.7, -30),
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
