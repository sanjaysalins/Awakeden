"""Mix v2 ($0): voice (from SECOND_FIRE_PREVIEW_v2.mp4) + score_v2 + SFX bed from the blind panel plan
(score_sfx_panel/panel_r1). The SAME fire_crackling file, from the same start point, plays at all 3 fires:
night (cool, low-passed), beach (warm), end (with bread tear). Music + SFX are sidechain-ducked under the
voice, then loudnorm to -14 LUFS. Gentle: 3 threads."""
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
LIB = H.parent / "sound_library" / "clips"
VID, SCORE = H / "SECOND_FIRE_PREVIEW_v3.mp4", H / "score_v2" / "score_v2.mp3"
OUT = H / "SECOND_FIRE_SCORED_v3.mp4"
END = 87.9

# (file, start_s, end_s, gain_db, fade_in, fade_out, extra_filter, loop)
EVENTS = [
    (LIB / "fire_crackling.mp3",       0.0, 15.7, -15, 1.0, 1.5, "lowpass=f=2500", True),   # fire 1: denial
    (LIB / "crowd_murmur_distant.mp3", 3.3, 13.2, -17, 1.0, 1.5, "", False),
    (H / "sfx_new/rooster_t1.mp3",    14.8, 17.8, -17, 0.0, 0.3, "aecho=0.6:0.5:180:0.25", False),
    (LIB / "boat_creak_oars.mp3",     18.9, 23.9, -16, 0.8, 1.0, "", False),
    (LIB / "sea_waves_shore.mp3",     18.9, END,  -19, 1.0, 2.0, "", True),
    (LIB / "dawn_morning_warm.mp3",   23.7, 45.0, -17, 2.0, 3.0, "", True),
    (H / "sfx_new/splash_t1.mp3",     35.9, 38.9, -9, 0.0, 0.5, "", False),
    (LIB / "fire_crackling.mp3",      36.7, 53.2, -10, 0.6, 2.0, "", True),                 # fire 2: beach
    (H / "sfx_new/sizzle_t1.mp3",     37.4, 45.4, -2, 1.0, 2.0, "", False),
    (LIB / "bread_tearing.mp3",       50.9, 53.4, -6, 0.0, 0.5, "", False),
    (LIB / "fire_crackling.mp3",      53.2, 80.3, -18, 1.0, 1.0, "", True),                 # under the questions
    (LIB / "flock_sheep_field.mp3",   71.4, 76.0, -25, 0.8, 1.2, "", False),
    (LIB / "fire_crackling.mp3",      80.3, END,  -15, 0.8, 1.2, "", True),                 # fire 3: end
    (LIB / "bread_tearing.mp3",       84.9, END,  -6, 0.0, 0.6, "", False),
]

inputs = ["-i", str(VID), "-i", str(SCORE)]
fc = ["[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,asplit=2[v][sc]",
      # score: -12 dB (5 dB dip under 'Feed my sheep / Take care of my people' 71-76 s), lift to -6 dB only in the hold after the last word (84.7 s)
      "[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
      "volume='pow(10,(if(lt(t,71.0),-12,if(lt(t,71.6),-12-5*(t-71.0)/0.6,if(lt(t,75.0),-17,if(lt(t,76.0),-17+5*(t-75.0),if(lt(t,84.7),-12,if(lt(t,86.2),-12+6*(t-84.7)/1.5,-6)))))))/20)':eval=frame[m]"]
labels = ["[m]"]
for i, (f, s, e, g, fi, fo, extra, loop) in enumerate(EVENTS):
    if loop:
        inputs += ["-stream_loop", "-1"]
    inputs += ["-i", str(f)]
    d = round(e - s, 3)
    chain = (f"[{i + 2}:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
             f"atrim=0:{d},asetpts=PTS-STARTPTS,")
    if extra:
        chain += extra + ","
    if fi:
        chain += f"afade=t=in:st=0:d={fi},"
    chain += f"afade=t=out:st={max(0, d - fo):.3f}:d={fo},volume={g}dB,adelay={int(s * 1000)}:all=1[e{i}]"
    fc.append(chain)
    labels.append(f"[e{i}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,apad=whole_dur={END},atrim=0:{END}[bed]")
fc.append("[bed][sc]sidechaincompress=threshold=0.10:ratio=3:attack=20:release=300[bd]")
fc.append(f"[v][bd]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false,"
          f"aresample=44100,atrim=0:{END}[a]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", *inputs, "-filter_complex", ";".join(fc),
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(OUT)], check=True)
print(OUT)
