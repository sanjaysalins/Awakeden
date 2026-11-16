"""[v5: words-v3 timing; every start/length mapped through motion_v5/warp.o2n]
Lay a $0 sound_library SFX bed under film/BETHLEHEM_SCORED_v2.mp4 -> film/BETHLEHEM_FINAL_v1.mp4.
Plan = FABLE_EPISODE_DESIGN.md section 2, library clips only (paper/nib pack NOT bought, needs its own yes).
Key pair: Map B hollow prints = 3 dry taps, NO footsteps (35.7 s); Map C gold prints = real footsteps (40.6 s).
Nothing in the two silences (36.3-37.4, 39.5-40.5). Sacred windows: only far sheep at the birth, dawn birds at the end.
Gains from measured raw means (target ~-44 dB beds, ~-38 dB steps). Voice-keyed duck on the SFX bed only."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "motion_v5"))
from warp import o2n
LIB = H.parents[2] / "sound_library" / "clips"
FILM = H.parent / "film"
SRC, KEY, OUT = FILM / "BETHLEHEM_SCORED_v5.mp4", FILM / "BETHLEHEM_FILM_v5.mp4", FILM / "BETHLEHEM_FINAL_v2.mp4"
T = 59.5
ins = [SRC, KEY, LIB / "fire_crackling.mp3", LIB / "wind_desert_bleak.mp3", LIB / "footsteps_dirt_approach.mp3",
       LIB / "coins_clinking.mp3", LIB / "flock_sheep_field.mp3", LIB / "waterpot_drop_run.mp3", LIB / "dawn_morning_warm.mp3"]
args = []
for p in ins:
    args += ["-i", str(p)]
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"


def place(src, start, dur, gain, fi=0.3, fo=0.4, tag="x", pre=""):
    return (f"[{src}]{pre}atrim=0:{dur},asetpts=N/SR/TB,afade=t=in:d={fi},afade=t=out:st={max(0, dur - fo):.2f}:d={fo},"
            f"volume={gain}dB,adelay={int(start * 1000)}|{int(start * 1000)},apad=whole_dur={T}[{tag}]")


fc = ";".join([
    f"[0:a]{F}[mix]", f"[1:a]{F}[key]",
    f"[2:a]{F}[fire]", f"[3:a]{F},areverse[wind]",
    f"[4:a]{F},asplit=3[s1][s2][s3]", f"[5:a]{F}[coin]", f"[6:a]{F}[sheep]",
    f"[7:a]{F},asplit=3[t1][t2][t3]", f"[8:a]{F}[birds]",
    place("fire", o2n(0.0), o2n(3.90) - o2n(0.0), 0, fi=0.05, fo=0.8, tag="a1"),                        # torch-lit room under the hook
    place("wind", o2n(3.9), o2n(6.00) - o2n(3.9), -10, fi=0.3, fo=0.6, tag="a2"),                         # time pulled backwards
    place("s1", o2n(19.0), o2n(22.00) - o2n(19.0), 4, fi=0.5, fo=0.6, tag="a3"),                            # Mary and Joseph walk south
    place("coin", o2n(20.72), o2n(21.72) - o2n(20.72), -12, fi=0.01, fo=0.4, tag="a4"),                      # "tax order"
    place("sheep", o2n(22.7), o2n(25.10) - o2n(22.7), 2, fi=0.6, fo=0.8, tag="a5"),                         # far sheep at the birth, very low
    place("s2", o2n(25.2), o2n(27.80) - o2n(25.2), 5, fi=0.4, fo=0.6, tag="a6",
          pre="asetrate=44100*0.8,aresample=44100,lowpass=f=1800,"),               # soft padded camel steps
    place("t1", o2n(35.67), 0.35, -8, fi=0.005, fo=0.1, tag="a7"),                       # hollow prints: dry taps, no steps
    place("t2", o2n(35.87), 0.35, -9, fi=0.005, fo=0.1, tag="a8"),
    place("t3", o2n(36.07), 0.22, -10, fi=0.005, fo=0.1, tag="a9"),
    place("s3", o2n(40.6), o2n(42.30) - o2n(40.6), 6, fi=0.05, fo=0.5, tag="b1"),                           # gold prints: real footsteps now
    place("birds", o2n(51.7), o2n(59.30) - o2n(51.7), -6, fi=2.0, fo=1.2, tag="b2"),                        # dawn, risen
    "[a1][a2][a3][a4][a5][a6][a7][a8][a9][b1][b2]amix=inputs=11:duration=first:normalize=0[bed]",
    "[bed][key]sidechaincompress=threshold=0.08:ratio=4:attack=15:release=300[bedd]",
    "[mix][bedd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", *args, "-filter_complex", fc, "-map", "0:v",
                "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T}", "-movflags", "+faststart",
                str(OUT)], check=True)
print(OUT)
