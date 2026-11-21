"""first_gospel_in_the_curse linefix1 narration (frame-exact splice, D = -155 frames = -5.1667 s):
  head   = new first sentence (take a) padded to 3.9453 s
  middle = OLD narration.mp3 [9.112, 52.6] exactly (starts 0.15 s before old 'But', ends in the silence after 'asked.'), shifted by D
  tail   = silence + new last two sentences (take a), its three long dramatic pauses tightened (1.21/0.96/0.67 s -> ~0.70/0.50/0.35 s)
           so 'Jesus ... first.' + 3.0 s hold fit the two landing clips (trim-only, no fill). 'That' lands at old-'That' + D."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
OLD = r"F:\slk\PycharmProjects\PythonProject1\jesus\narration\44_Grace_Spoken_First\v1\narration.mp3"
F = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
D = -155/30
B0 = 9.112; C1 = 52.6
L = round(B0 + D, 4)                       # head length
THAT_NEW = round(53.26 + D, 4)             # new 'That' start
TAKE0 = round(THAT_NEW - 0.10, 4)          # take starts 0.10 before its 'That'
S1 = round(TAKE0 - (C1 + D), 4)            # silence between middle end and take start
def sil(d, n): return f"aevalsrc=0:d={d}:s=44100,{F}[{n}]"
def rng(i, a, b, n):
    return f"[{i}:a]{F},atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.012,afade=t=out:st={round(b-a-0.012,4)}:d=0.012[{n}]"
fc = ";".join([
  f"[0:a]{F},apad=whole_dur={L},atrim=0:{L},asetpts=PTS-STARTPTS,afade=t=out:st={L-0.01}:d=0.01[h]",
  f"[1:a]{F},atrim={B0}:{C1},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005,afade=t=out:st={round(C1-B0-0.01,4)}:d=0.01[m]",
  sil(S1, "s1"),
  rng(2, 0.0, 1.62, "r1"), sil(0.42, "g1"), rng(2, 2.55, 3.35, "r2"), sil(0.14, "g2"),
  rng(2, 3.95, 5.25, "r3"), sil(0.05, "g3"), rng(2, 5.62, 7.36, "r4"),
  "[h][m][s1][r1][g1][r2][g2][r3][g3][r4]concat=n=10:v=0:a=1[out]"])
subprocess.run(["ffmpeg","-y","-v","error","-i",str(H/"first_narrator_a.mp3"),"-i",OLD,"-i",str(H/"last_narrator_a.mp3"),
                "-filter_complex",fc,"-map","[out]","-c:a","pcm_s16le",str(H/"narration_linefix1.wav")],check=True)
print("ok head L", L, "S1", S1, "THAT_NEW", THAT_NEW)
