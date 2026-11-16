"""$0 sound_library SFX bed for Immanuel v2 (same recipe as Ep 01 add_sfx_v6.py): low beds, a low boom on each big comic
word, coins on the temple gold, soft steps + dawn birds on the risen walk. Nothing over the angel/dream (sacred).
Voice-keyed duck on the SFX bed only.  python add_sfx.py <scored.mp4> <voice_key.mp4> <out.mp4>"""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]; LIB = ROOT / "sound_library" / "clips"
SRC, KEY, OUT = (Path(a) for a in sys.argv[1:4])
W = json.loads((ROOT / "_remotion" / "public" / "immanuel" / "words.json").read_text(encoding="utf-8"))
wt = lambda i: W[i]["s"]
SLAMS = [wt(5), wt(36), wt(56), wt(78), wt(92), wt(111), wt(116)]   # NO. SAVE ME IMMANUEL FEAR NOT JESUS HE SAVES GOD WITH US
T = 65.44
ins = [SRC, KEY, LIB / "wind_desert_bleak.mp3", LIB / "fire_crackling.mp3", LIB / "coins_clinking.mp3",
       LIB / "footsteps_dirt_approach.mp3", LIB / "dawn_morning_warm.mp3", LIB / "impact_low_boom.mp3"]
args = []
for p in ins: args += ["-i", str(p)]
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
def place(src, start, dur, gain, fi=0.3, fo=0.4, tag="x", pre=""):
    return (f"[{src}]{pre}atrim=0:{dur},asetpts=N/SR/TB,afade=t=in:d={fi},afade=t=out:st={max(0, dur - fo):.2f}:d={fo},"
            f"volume={gain}dB,adelay={int(start * 1000)}|{int(start * 1000)},apad=whole_dur={T}[{tag}]")
fc = ";".join([
    f"[0:a]{F}[mix]", f"[1:a]{F}[key]", f"[2:a]{F}[wind]", f"[3:a]{F}[fire]", f"[4:a]{F}[coin]", f"[5:a]{F}[steps]", f"[6:a]{F}[birds]",
    place("wind", 0.0, 11.9, -8, fi=0.05, fo=0.8, tag="a1"),                  # night wind on Jerusalem's wall
    place("fire", 3.0, 9.0, -10, fi=1.0, fo=1.0, tag="a2"),                   # far enemy campfires
    place("coin", 12.2, 2.2, -10, fi=0.02, fo=0.5, tag="a3"),                 # temple gold in the chest
    place("steps", 59.2, 6.0, 2, fi=0.6, fo=1.2, tag="a4", pre="lowpass=f=2500,"),   # walking with friends
    place("birds", 59.2, 6.2, -6, fi=1.5, fo=1.2, tag="a5"),                  # morning, risen
    f"[7:a]{F},asplit={len(SLAMS)}" + "".join(f"[bm{i}]" for i in range(len(SLAMS))),
    *[f"[bm{i}]atrim=0:1.6,asetpts=N/SR/TB,afade=t=out:st=1.0:d=0.6,volume=-5dB,adelay={int(x*1000)}|{int(x*1000)},apad=whole_dur={T}[sl{i}]" for i, x in enumerate(SLAMS)],
    "[a1][a2][a3][a4][a5]" + "".join(f"[sl{i}]" for i in range(len(SLAMS))) + f"amix=inputs={5+len(SLAMS)}:duration=first:normalize=0[bed]",
    "[bed][key]sidechaincompress=threshold=0.08:ratio=4:attack=15:release=300[bedd]",
    "[mix][bedd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.85:level=disabled[a]",
])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", *args, "-filter_complex", fc, "-map", "0:v",
                "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T}", "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
