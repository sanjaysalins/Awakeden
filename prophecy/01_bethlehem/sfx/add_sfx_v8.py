"""[v8: words-v4 film] SFX bed under film/BETHLEHEM_SCORED_v8.mp4 -> film/BETHLEHEM_FINAL_v5.mp4. $0, sound_library clips only.
Re-keyed from add_sfx_v6.py to narration_v4.words.json real times. Dropped: the walk footsteps + the tax-order coins (those beats are cut).
Kept: fire (hook), wind (time back), far sheep at the birth, soft camel steps, 3 dry taps on the hollow prints, gold-print steps on WENT,
dawn birds; booms on slams (knew, GO?, Herod, WENT, the '?', 'born there'); whooshes on the 3 whips. Nothing in the 29.6-30.7 silence.
No paper/pen sound exists in the local library, so the scroll line 'from everlasting' has none (not bought).
Voice-keyed duck on the SFX bed only."""
import json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
LIB = H.parents[2] / "sound_library" / "clips"
FILM = H.parent / "film"
SRC, KEY, OUT = FILM / "BETHLEHEM_SCORED_v8.mp4", FILM / "BETHLEHEM_FILM_v8.mp4", FILM / "BETHLEHEM_FINAL_v5.mp4"
WD = json.loads((H.parent / "audio_v4" / "narration_v4.words.json").read_text(encoding="utf-8"))
wt = lambda i: WD[i]["start"]
SLAMS = [(wt(3), -3), (wt(12), -3), (wt(61), -3), (wt(83), -3), (40.16, -8), (44.04, -3)]   # knew, GO?, Herod, WENT, '?', born there
WHIPS = [wt(13), 22.20, wt(69)]
T = 59.0
ins = [SRC, KEY, LIB / "fire_crackling.mp3", LIB / "wind_desert_bleak.mp3", LIB / "footsteps_dirt_approach.mp3",
       LIB / "flock_sheep_field.mp3", LIB / "waterpot_drop_run.mp3", LIB / "dawn_morning_warm.mp3", LIB / "impact_low_boom.mp3"]
args = []
for p in ins:
    args += ["-i", str(p)]
args += ["-f", "lavfi", "-t", "1", "-i", "anoisesrc=color=pink:r=44100:a=0.5"]
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"

def place(src, start, dur, gain, fi=0.3, fo=0.4, tag="x", pre=""):
    return (f"[{src}]{pre}atrim=0:{dur},asetpts=N/SR/TB,afade=t=in:d={fi},afade=t=out:st={max(0, dur - fo):.2f}:d={fo},"
            f"volume={gain}dB,adelay={int(start * 1000)}|{int(start * 1000)},apad=whole_dur={T}[{tag}]")

NS, NW = len(SLAMS), len(WHIPS)
fc = ";".join([
    f"[0:a]{F}[mix]", f"[1:a]{F}[key]",
    f"[2:a]{F}[fire]", f"[3:a]{F},areverse[wind]",
    f"[4:a]{F},asplit=2[s2][s3]", f"[5:a]{F}[sheep]", f"[6:a]{F},asplit=3[t1][t2][t3]", f"[7:a]{F}[birds]",
    place("fire", 0.0, 3.95, 0, fi=0.05, fo=0.8, tag="a1"),
    place("wind", 4.0, 2.1, -10, fi=0.3, fo=0.6, tag="a2"),
    place("sheep", 17.2, 3.7, 2, fi=0.6, fo=0.8, tag="a5"),
    place("s2", 21.3, 1.7, 5, fi=0.4, fo=0.6, tag="a6", pre="asetrate=44100*0.8,aresample=44100,lowpass=f=1800,"),
    place("t1", wt(79) + 0.1, 0.35, -8, fi=0.005, fo=0.1, tag="a7"),
    place("t2", wt(79) + 0.3, 0.35, -9, fi=0.005, fo=0.1, tag="a8"),
    place("t3", wt(79) + 0.5, 0.22, -10, fi=0.005, fo=0.1, tag="a9"),
    place("s3", wt(83) + 0.15, 1.7, 6, fi=0.05, fo=0.5, tag="b1"),
    place("birds", 51.9, 6.9, -6, fi=2.0, fo=1.2, tag="b2"),
    f"[8:a]{F},asplit={NS}" + "".join(f"[bm{i}]" for i in range(NS)),
    *[f"[bm{i}]atrim=0:1.6,asetpts=N/SR/TB,afade=t=out:st=1.0:d=0.6,volume={g}dB,adelay={int(x*1000)}|{int(x*1000)},apad=whole_dur={T}[sl{i}]" for i, (x, g) in enumerate(SLAMS)],
    f"[9:a]{F},asplit={NW}" + "".join(f"[wn{i}]" for i in range(NW)),
    *[f"[wn{i}]atrim=0:0.32,asetpts=N/SR/TB,bandpass=f=1800:w=1600,afade=t=in:d=0.12,afade=t=out:st=0.14:d=0.18,volume=-14dB,adelay={int((x-0.14)*1000)}|{int((x-0.14)*1000)},apad=whole_dur={T}[wh{i}]" for i, x in enumerate(WHIPS)],
    "[a1][a2][a5][a6][a7][a8][a9][b1][b2]" + "".join(f"[sl{i}]" for i in range(NS)) + "".join(f"[wh{i}]" for i in range(NW)) + f"amix=inputs={9+NS+NW}:duration=first:normalize=0[bed]",
    "[bed][key]sidechaincompress=threshold=0.08:ratio=4:attack=15:release=300[bedd]",
    "[mix][bedd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", *args, "-filter_complex", fc, "-map", "0:v",
                "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T}", "-movflags", "+faststart",
                str(OUT)], check=True)
print(OUT)
