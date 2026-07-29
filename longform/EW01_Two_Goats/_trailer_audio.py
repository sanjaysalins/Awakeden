"""Build the EW01 Two Goats TRAILER audio master (2026-07-22).

The PACE ENGINE: the driving score + sound-design hits + the dramatic STOP that
make a cold-open trailer grip. Structure (mirrors the film's own ascent->triumph
arc, compressed to ~35s):
  0.0 - 23.0s   ASCENT bed (tense build) under waves 1-3, + ominous sub + hits
  23.0 - 25.5s  THE STOP — music drops to near silence on "...and sat down"
                (the lean-in), only VO + a low sub tail
  25.5s         VEIL TEAR hit -> TRIUMPH bed swells to the peak and resolves warm
VO sits on top (priority); music/hits are the bed. All $0 from music_library +
sound_library.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_trailer_audio.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TRAILER = HERE / "v1" / "visual_16x9_inked" / "_trailer"
VO = TRAILER / "trailer_vo_fast.mp3"
OUT = TRAILER / "trailer_audio.mp3"

MUSIC = ROOT / "music_library" / "clips"
SFX = ROOT / "sound_library" / "clips"

TOTAL = 38.0  # VO ends ~35.4s + ~2.5s title-card tail

# (path, in_offset_s, take_len_s, fade_in, fade_out_start, fade_out_len, gain, place_at_s)
STEMS = [
    # --- music bed: ascent build, then the drop, then triumph peak ---
    (MUSIC / "ew01_ancient_epic_ascent.mp3",   28.0, 23.5, 1.3, 21.0, 2.5, 0.42, 0.0),
    (MUSIC / "ew01_ancient_epic_triumph.mp3",   96.0, 12.5, 1.1,  9.5, 3.0, 0.52, 25.5),
    # --- sound design hits (place_at = the VO cue) ---
    (SFX / "rumble_deep_sub.mp3",    0.0,  9.0, 0.5,  7.0, 2.0, 0.38, 0.0),    # ominous floor under the open
    (SFX / "impact_low_boom.mp3",    0.0,  4.0, 0.0,  2.5, 1.5, 0.60, 4.0),    # "...one door."
    (SFX / "thunder_low_roll.mp3",   0.0,  7.0, 0.0,  4.0, 3.0, 0.50, 13.6),   # "...Why two?"
    (SFX / "impact_low_boom.mp3",    0.0,  4.0, 0.0,  2.5, 1.5, 0.55, 20.1),   # "It was never enough."
    (SFX / "rumble_deep_sub.mp3",    0.0,  3.0, 0.3,  1.5, 1.5, 0.30, 23.2),   # the STOP — low tail only
    (SFX / "veil_tearing.mp3",       0.0,  5.0, 0.0,  3.5, 1.5, 0.78, 25.6),   # "The veil tore." — signature
    (SFX / "impact_low_boom.mp3",    0.0,  4.0, 0.0,  2.5, 1.5, 0.62, 35.3),   # title card
]


def main():
    if not VO.exists():
        raise SystemExit(f"missing VO: {VO} (run _trailer_vo.py first)")
    inputs = ["-i", str(VO)]
    for st in STEMS:
        p, off, take = st[0], st[1], st[2]
        if not p.exists():
            raise SystemExit(f"missing asset: {p}")
        inputs += ["-ss", str(off), "-t", str(take), "-i", str(p)]

    parts = []
    labels = []
    # VO (input 0): keep on top, gentle level
    parts.append("[0:a]volume=1.05,aresample=48000[vo]")
    labels.append("[vo]")
    for i, st in enumerate(STEMS, start=1):
        _, _, take, fin, fos, fol, gain, place = st
        f = (f"[{i}:a]afade=t=in:st=0:d={fin},"
             f"afade=t=out:st={fos}:d={fol},"
             f"volume={gain},aresample=48000,"
             f"adelay={int(place*1000)}|{int(place*1000)}[s{i}]")
        parts.append(f)
        labels.append(f"[s{i}]")

    n = len(labels)
    mix = (f"{''.join(labels)}amix=inputs={n}:duration=longest:normalize=0[mixed];"
           f"[mixed]alimiter=limit=0.95,loudnorm=I=-14:TP=-1.2:LRA=11,"
           f"atrim=0:{TOTAL},asetpts=N/SR/TB[out]")
    fc = ";".join(parts) + ";" + mix

    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs,
           "-filter_complex", fc, "-map", "[out]",
           "-c:a", "libmp3lame", "-q:a", "2", str(OUT)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{r.stderr[-1500:]}")

    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(OUT)], capture_output=True, text=True).stdout.strip())
    print(f"[done] {OUT}  ({dur:.1f}s)")


if __name__ == "__main__":
    main()
