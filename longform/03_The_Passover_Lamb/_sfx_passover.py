"""Lay a reverent, choir-free ambient/SFX bed UNDER the scored Passover film.

Layer stack (feedback-audio-layer-stack): narration (base) -> orchestral SCORE ->
SFX (quietest, this). NO sustained choir/musical pad here (feedback-no-choir-pad-under-score)
— the orchestral score is the single musical bed. Reuse-only from sound_library ($0).

Cues are mapped to the scene_plan time windows. Builds an SFX bed, then sums it under
the scored film's audio (amix normalize=0 so narration+score stay full and the SFX only
adds, low). Output: Passover_Lamb_16x9_scored_sfx.mp4 (then caption it).
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "sound_library" / "clips"
VIS = Path(__file__).resolve().parent / "v1" / "visual_16x9"
SCORED = VIS / "Passover_Lamb_16x9_scored.mp4"
OUT = VIS / "Passover_Lamb_16x9_scored_sfx.mp4"
WORK = VIS / "_sfx_work"
WORK.mkdir(exist_ok=True)
TOTAL = 509.5

# (slug, start_s, end_s, gain_db) — ambient only, low. NO choir, NO score_* clips.
CUES = [
    ("wind_desert_bleak",     0.0,   509.5, -37),  # faint ancient air throughout
    ("fire_crackling",        0.0,    13.4, -30),  # S1 lamp
    ("flock_sheep_field",    33.9,    53.2, -32),  # S3 the lamb
    ("rumble_deep_sub",      53.2,   102.9, -28),  # M2 death passes over Egypt
    ("thunder_low_roll",     55.0,    63.0, -26),  # the smiting (subtle)
    ("flock_sheep_field",   102.9,   121.6, -32),  # S6 flock at dawn
    ("dawn_morning_warm",   102.9,   121.6, -35),  # S6 dawn
    ("fire_crackling",      121.6,   146.4, -30),  # S7 hearth, four days
    ("crowd_murmur_distant",146.4,   167.6, -37),  # S8 the whole nation
    ("fire_crackling",      167.6,   213.9, -32),  # S9/S10 lamp + embers
    ("rumble_deep_sub",     213.9,   256.7, -31),  # M4 Golgotha weight
    ("crowd_murmur_distant",213.9,   240.7, -38),  # S11 Jerusalem below
    ("soldiers_march_armor",240.7,   256.7, -38),  # S12 soldiers (faint)
    ("air_hollow_desolate", 304.2,   365.3, -35),  # M5 the honest doubt, hollow
    ("fire_crackling",      414.3,   440.6, -31),  # S21 lamp, blood applied
    ("fire_crackling",      456.6,   477.7, -34),  # S23 inside the house
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
              f"afade=t=out:st={max(0,d-1.5):.2f}:d=1.5,"
              f"adelay={delay}|{delay}")
        run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(src), "-t", f"{d:.3f}",
             "-af", af, "-ar", "44100", "-ac", "2", str(out)])
        cue_files.append(out)
        print(f"  cue {i:02d} {slug:22s} [{start:6.1f}-{end:6.1f}] {gain}dB")

    # sum all cues into one bed (normalize=0 -> simple sum, no auto-attenuation)
    bed = WORK / "sfx_bed.wav"
    inputs = []
    for f in cue_files:
        inputs += ["-i", str(f)]
    amix = f"amix=inputs={len(cue_files)}:normalize=0:duration=longest[b]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", amix, "-map", "[b]",
         "-t", f"{TOTAL:.3f}", "-ar", "44100", "-ac", "2", str(bed)])
    print(f"[bed] {len(cue_files)} cues -> {bed.name}")

    # mix the bed UNDER the scored film (narration+score stay full; SFX only adds, low)
    run(["ffmpeg", "-y", "-i", str(SCORED), "-i", str(bed),
         "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0:duration=first[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         str(OUT)])
    print(f"[done] {OUT}")


if __name__ == "__main__":
    main()
