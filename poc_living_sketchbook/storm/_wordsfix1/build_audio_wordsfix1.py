"""Storm wordsfix1 narration: old narration.mp3 lines kept (cut at pauses), new lines = new takes (atempo 1.2371 like the film's narrator turns).
Writes narration_wordsfix1.wav + lines_wordsfix1.json (start/end of each line)."""
import json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
OLD = r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\20 He Was Asleep in the Storm\v1\narration.mp3"
F = "aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo"
# (id, kind, src/range, gap_after)
L = [
 ("L1_ship",   "new", "l1.mp3", 0.9),
 ("L2_stern",  "old", (6.60, 9.30), 1.4),     # And in the stern - He is asleep.
 ("L3_bible",  "new", "l3.mp3", 1.0),
 ("L4a_wake",  "new", "l4a.mp3", 0.30),
 ("L4b_cry",   "new", "l4b.mp3", 1.0),
 ("L5_eyes",   "old", (21.90, 22.90), 0.70),  # He opens His eyes:
 ("L6_jesus",  "old", (23.50, 26.95), 0.65),  # Why are ye fearful...  (Jesus voice)
 ("L7_arose",  "old", (27.38, 31.40), 0.90),  # Then he arose... great calm. (narrator)
 ("L8_exactly","old", (32.15, 39.30), 1.0),   # You'll say... with a word.
 ("L9_storm",  "new", "l9.mp3", 1.0),
 ("L10_little","old", (49.05, 53.15), 0.9),   # He doesn't despise little faith. He grows it...
 ("L11_stood", "new", "l11.mp3", 1.0),
 ("L12_asking","old", (56.55, 59.62), 0.0),   # He is asking you - why are you afraid?
]
inp, fc, labels, tl, t = [], [], [], [], 0.0
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip())
n = 0
for i, (lid, kind, src, gap) in enumerate(L):
    if kind == "new":
        inp += ["-i", str(H/src)]; d = dur(H/src)
        fc.append(f"[{n}:a]{F},afade=t=in:st=0:d=0.005[a{i}]")
    else:
        a, b = src; inp += ["-i", OLD]; d = b - a
        fc.append(f"[{n}:a]{F},atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01[a{i}]")
    n += 1
    tl.append({"id": lid, "start": round(t, 3), "end": round(t + d, 3), "src": kind})
    labels.append(f"[a{i}]")
    t += d
    if gap:
        fc.append(f"aevalsrc=0:d={gap}:s=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[g{i}]"); labels.append(f"[g{i}]"); t += gap
fc.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]")
subprocess.run(["ffmpeg","-y","-v","error"] + inp + ["-filter_complex", ";".join(fc), "-map","[out]","-c:a","pcm_s16le", str(H/"narration_wordsfix1.wav")], check=True)
json.dump(tl, open(H/"lines_wordsfix1.json","w"), indent=1)
print(round(t,2), dur(H/"narration_wordsfix1.wav"))
for x in tl: print(x)
