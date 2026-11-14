"""Lay an SFX bed under film/bartimaeus_scored_v2.mp4 -> film/bartimaeus_final_v1.mp4 ($0 mix).
Library: wind (whole film), crowd murmur 3.0-25.6 (stops with the music when Jesus stops) + faint again 56-61,
dirt footsteps 56-61 (he follows). New (ElevenLabs): hush_t1 @3.2, cloak_t1 @35.9 (gap after "and came"),
birds_t1 69.4-79.17 sunset. Voice-keyed duck on the SFX bed only. Gains from measured raw means."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
LIB = H.parents[2] / "sound_library" / "clips"
FILM = H.parent / "film"
SRC, KEY, OUT = FILM / "bartimaeus_scored_v2.mp4", FILM / "bartimaeus_draft_v2.mp4", FILM / "bartimaeus_final_v1.mp4"
T = 79.17
ins = [SRC, KEY, LIB / "wind_desert_bleak.mp3", LIB / "crowd_murmur_distant.mp3", H / "hush_t1.mp3",
       H / "cloak_t1.mp3", LIB / "footsteps_dirt_approach.mp3", H / "birds_t1.mp3"]
loop = {2, 3, 6}
args = []
for i, p in enumerate(ins):
    args += (["-stream_loop", "-1"] if i in loop else []) + ["-i", str(p)]
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
def place(i, start, dur, gain, fi=0.3, fo=0.4, tag=None):
    return (f"[{i}:a]{F},atrim=0:{dur},afade=t=in:d={fi},afade=t=out:st={max(0, dur-fo):.2f}:d={fo},"
            f"volume={gain}dB,adelay={int(start*1000)}|{int(start*1000)},apad=whole_dur={T}[{tag}]")
fc = ";".join([
    f"[0:a]{F}[mix]", f"[1:a]{F},asplit=1[key]",
    f"[2:a]{F},atrim=0:{T},volume=-16dB,volume='pow(10,-6*min(1,max(0,min((t-25.4)/0.3,(29.8-t)/1.0)))/20)':eval=frame,afade=t=in:d=1.0,afade=t=out:st={T-1.5}:d=1.5[wind]",
    f"[3:a]{F},asplit=2[c1][c2]",
    f"[c1]atrim=0:22.6,afade=t=in:d=1.0,afade=t=out:st=22.15:d=0.45,volume=10dB,adelay=3000|3000,apad=whole_dur={T}[crowdA]",
    f"[c2]atrim=0:5,afade=t=in:d=1.0,afade=t=out:st=3.5:d=1.5,volume=6dB,adelay=56000|56000,apad=whole_dur={T}[crowdB]",
    place(4, 3.2, 3.0, -24, tag="hush"),
    place(5, 35.9, 2.0, -17, fi=0.02, fo=0.3, tag="cloak"),
    f"[6:a]{F},atrim=0:5,afade=t=in:d=0.6,afade=t=out:st=4.0:d=1.0,volume=2dB,adelay=56000|56000,apad=whole_dur={T}[steps]",
    place(7, 69.4, 9.77, 6, fi=1.5, fo=1.5, tag="birds"),
    "[wind][crowdA][crowdB][hush][cloak][steps][birds]amix=inputs=7:duration=first:normalize=0[bed]",
    "[bed][key]sidechaincompress=threshold=0.08:ratio=4:attack=15:release=300[bedd]",
    f"[mix][bedd]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", *args, "-filter_complex", fc, "-map", "0:v",
                "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{T}", "-movflags", "+faststart",
                str(OUT)], check=True)
print(OUT)
