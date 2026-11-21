"""Jericho linefix1 narration: old per-line takes kept (l2,l3,l4 untouched); l1 = new first sentence + old l1 from just before 'Her';
l5 = old l5 up to 'promise.' + new last two sentences. Gaps as record_v4 (.32 / 1.0 / .32 / 1.0). Writes narration_linefix1.wav"""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent; A = H.parent / "audio" / "jericho"
F = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo"
def sil(d): return f"aevalsrc=0:d={d}:s=44100,aformat=sample_fmts=fltp:channel_layouts=stereo"
L1_CUT = 3.95            # old l1: 'alive.' ends 3.221, 'Her' starts 4.082
L5_CUT = 49.55 - 45.411  # old l5: 'promise.' ends 49.32 (narr time), 'Tie' 49.8
GAP_A, GAP_B = 0.52, 0.27
inp = [A/"l2.mp3", A/"l3.mp3", A/"l4.mp3", H/"first_a.mp3", A/"l1.mp3", A/"l5.mp3", H/"last_a.mp3"]
fc = ";".join([
 f"[3:a]{F}[fa]", f"[4:a]{F},atrim=start={L1_CUT},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005[o1]", sil(GAP_A)+"[sA]",
 f"[5:a]{F},atrim=end={L5_CUT},asetpts=PTS-STARTPTS,afade=t=out:st={L5_CUT-0.005}:d=0.005[o5]", sil(GAP_B)+"[sB]", f"[6:a]{F}[la]",
 f"[fa][sA][o1]concat=n=3:v=0:a=1[l1n]", f"[o5][sB][la]concat=n=3:v=0:a=1[l5n]",
 f"[0:a]{F}[l2]", f"[1:a]{F}[l3]", f"[2:a]{F}[l4]",
 sil(0.32)+"[g1]", sil(1.0)+"[g2]", sil(0.32)+"[g3]", sil(1.0)+"[g4]",
 "[l1n][g1][l2][g2][l3][g3][l4][g4][l5n]concat=n=9:v=0:a=1[out]"])
cmd = ["ffmpeg","-y","-v","error"]
for p in inp: cmd += ["-i", str(p)]
subprocess.run(cmd+["-filter_complex", fc, "-map","[out]","-c:a","pcm_s16le", str(H/"narration_linefix1.wav")], check=True)
print("ok")
