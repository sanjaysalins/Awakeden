"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Day of Atonement film.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). NO sustained choir/musical pad (feedback-no-choir-pad-under-score)
— the orchestral score is the single musical bed. Reuse-only from sound_library ($0).

Cues mapped to the scene_plan time windows (532.6s, 25 scenes). The bed is summed
under the scored film (amix normalize=0 so narration+score stay full, SFX only adds).
Output: Day_Of_Atonement_16x9_scored_sfx.mp4 (then caption it).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Day_Of_Atonement_16x9_scored.mp4"
OUT = VIS / "Day_Of_Atonement_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 532.6

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("air_hollow_desolate",    0.0,   532.6, -40),  # faint sacred air base throughout
    ("shofar_blast",           0.5,     6.5, -26),  # M1 hook — the Day of Atonement ram's-horn call (Lev 25:9)
    ("fire_crackling",         0.0,    61.0, -33),  # M1 the lamp/incense warmth, the priest robing
    ("crowd_murmur_distant",  61.0,   102.0, -34),  # M2 "a guilty people" — the congregation's weight
    ("rumble_deep_sub",       61.0,   102.0, -30),  # M2 a year of sin piled up
    ("fire_crackling",       102.0,   166.0, -31),  # M3 goats at the altar, lots cast
    ("rumble_deep_sub",      166.0,   208.0, -30),  # M4 blood behind the veil / hands on the goat
    ("wind_desert_bleak",    208.0,   293.1, -32),  # M4 the scapegoat into the wilderness, outside the gate
    ("footsteps_dirt_approach", 208.0, 212.0, -27), # S11 the scapegoat driven out
    ("thunder_low_roll",     229.3,   250.5, -26),  # S12 "by his own blood entered in" — the cross
    ("rumble_deep_sub",      250.5,   293.1, -28),  # S13-14 Isaiah 53 / outside the camp — holy weight
    ("fire_crackling",       316.1,   362.2, -28),  # M5 "the same blood, never finished" — endless altar smoke
    ("rumble_deep_sub",      362.2,   409.4, -27),  # M6 the priest stands / once for all — building weight
    ("veil_tearing",         411.5,   416.5, -22),  # S20 "the veil rent in twain from the top"
    ("dawn_morning_warm",    432.9,   532.6, -28),  # M6 close + M7 invitation + risen-Christ hero (grace resolve)
    ("crowd_murmur_distant", 494.6,   513.6, -37),  # S24 "boldness to enter" — the quiet approach
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
