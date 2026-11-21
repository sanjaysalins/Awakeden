r"""$0 SFX bed (sound_library clips only) under film/NAZARETH_SCORED_v6_lf1.mp4 -> film/NAZARETH_FINAL_v2_lf1.mp4 (words v7). Pattern = prophecy/01_bethlehem/sfx/add_sfx_v8.py.
Times from audio/narration_v7.words.json + v6 page turns (build/nazareth_episode_v6.json). SILENT windows (no SFX): Isaiah hush + 'sat down' + Jesus' line (10.1-22.6), and nothing
but soft wind on the cross (40.3-49.8). Booms only on the hook dive ('sentence.') and the mob ('Furious', 'cliff'); soft whooshes on 4 page turns.
Last bed (evening birds) fades over the final 2.6 s (owner end-fade rule). Voice-keyed duck on the SFX bed only."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
LIB = H.parents[2] / "sound_library" / "clips"
FILM = H.parent / "film"
SRC, KEY, OUT = FILM / "NAZARETH_SCORED_v6_lf1.mp4", FILM / "NAZARETH_COMIC_v6_lf1.mp4", FILM / "NAZARETH_FINAL_v2_lf1.mp4"
T = 61.067
SLAMS = [(1.80, -8), (36.44, -7), (37.38, -10)]          # hook dive 'sentence.', 'Furious', 'cliff'
WHIPS = [7.03, 23.80, 30.70, 39.60]                      # page turns outside the sacred windows
ins = [SRC, KEY, LIB / "fire_crackling.mp3", LIB / "dawn_morning_warm.mp3", LIB / "crowd_murmur_distant.mp3", LIB / "sea_waves_shore.mp3",
       LIB / "crowd_shout_mob.mp3", LIB / "footsteps_dirt_approach.mp3", LIB / "wind_desert_bleak.mp3", LIB / "impact_low_boom.mp3"]
args = []
for p in ins:
    args += ["-i", str(p)]
args += ["-f", "lavfi", "-t", "1", "-i", "anoisesrc=color=pink:r=44100:a=0.5"]
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

def place(src, start, dur, gain, fi=0.3, fo=0.4, tag="x", pre="", off=0.0):
    return (f"[{src}]{pre}atrim={off}:{off + dur},asetpts=N/SR/TB,afade=t=in:d={fi},afade=t=out:st={max(0, dur - fo):.2f}:d={fo},"
            f"volume={gain}dB,adelay={int(start * 1000)}|{int(start * 1000)},apad=whole_dur={T}[{tag}]")

NS, NW = len(SLAMS), len(WHIPS)
fc = ";".join([
    f"[0:a]{F}[mix]", f"[1:a]{F}[key]",
    f"[2:a]{F}[lamp]", f"[3:a]{F},asplit=2[bird1][bird2]", f"[4:a]{F},asplit=2[mur1][mur2]", f"[5:a]{F}[sea]",
    f"[6:a]{F}[mob]", f"[7:a]{F}[steps]", f"[8:a]{F}[wind]",
    place("lamp", 0.0, 4.2, -15, fi=0.05, fo=0.5, tag="a1"),            # lamp-lit synagogue under the hook
    place("bird1", 4.2, 2.9, -12, fi=0.4, fo=0.6, tag="a2"),           # Nazareth village morning
    place("mur1", 7.03, 4.2, -18, fi=0.6, fo=0.8, tag="a3"),             # synagogue room, very low
    place("mur2", 25.6, 4.9, -16, fi=0.3, fo=0.6, tag="a4", off=3.0),  # the town doubts
    place("sea", 30.7, 5.6, -14, fi=0.6, fo=0.6, tag="a5"),            # Zarephath by the sea
    place("mob", 36.44, 3.0, -21, fi=0.05, fo=0.9, tag="a6"),            # furious crowd
    place("steps", 39.65, 1.75, -2, fi=0.1, fo=0.5, tag="a7"),          # calm steps through them
    place("wind", 41.53, 9.5, -18, fi=1.0, fo=1.5, tag="a8"),            # the hill at dusk, nothing else
    place("bird2", 51.07, 10.0, -12, fi=2.0, fo=2.6, tag="a9"),           # evening birds over Nazareth, gentle end fade
    f"[9:a]{F},asplit={NS}" + "".join(f"[bm{i}]" for i in range(NS)),
    *[f"[bm{i}]atrim=0:1.6,asetpts=N/SR/TB,afade=t=out:st=1.0:d=0.6,volume={g}dB,adelay={int(x*1000)}|{int(x*1000)},apad=whole_dur={T}[sl{i}]" for i, (x, g) in enumerate(SLAMS)],
    f"[10:a]{F},asplit={NW}" + "".join(f"[wn{i}]" for i in range(NW)),
    *[f"[wn{i}]atrim=0:0.32,asetpts=N/SR/TB,bandpass=f=1800:w=1600,afade=t=in:d=0.12,afade=t=out:st=0.14:d=0.18,volume=-14dB,adelay={int((x-0.14)*1000)}|{int((x-0.14)*1000)},apad=whole_dur={T}[wh{i}]" for i, x in enumerate(WHIPS)],
    "[a1][a2][a3][a4][a5][a6][a7][a8][a9]" + "".join(f"[sl{i}]" for i in range(NS)) + "".join(f"[wh{i}]" for i in range(NW)) + f"amix=inputs={9+NS+NW}:duration=first:normalize=0[bed]",
    "[bed][key]sidechaincompress=threshold=0.08:ratio=4:attack=15:release=300[bedd]",
    "[mix][bedd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", *args, "-filter_complex", fc, "-map", "0:v",
                "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T}", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
