"""god_hung_up_a_snake linefix1 narration: new first two sentences (take a, narrator atempo 0.9721 as the film's own turn 0)
+ old narration.mp3 from 6.033 s (silence just before 'God hung up a snake.'; old 'God' starts 6.183).
Everything after the cut is the OLD audio exactly, shifted by D = -17 frames = -0.5667 s (frame-exact splice)."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
OLD = r"F:\slk\PycharmProjects\PythonProject1\jesus\narration\42_God_Hung_Up_a_Snake\v1\narration.mp3"
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
CUT = 6.033; L = 4.62; D = -17/30
S = round((6.183 + D) - 0.15 - L, 4)   # new 'God' = 5.6163
print("silence", S)
fc = (f"[0:a]atempo=0.9721,{F},apad=whole_dur={L},atrim=0:{L},asetpts=PTS-STARTPTS,afade=t=out:st={L-0.01}:d=0.01[h];"
      f"aevalsrc=0:d={S}:s=44100,{F}[s];"
      f"[1:a]{F},atrim=start={CUT},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005[o];"
      "[h][s][o]concat=n=3:v=0:a=1[out]")
subprocess.run(["ffmpeg","-y","-v","error","-i",str(H/"first_narrator_a.mp3"),"-i",OLD,"-filter_complex",fc,"-map","[out]","-c:a","pcm_s16le",str(H/"narration_linefix1.wav")],check=True)
print("ok")
