import json, subprocess, sys
from pathlib import Path
import numpy as np, scipy.io.wavfile as wf
sys.argv = [sys.argv[0], sys.argv[1], "x"]
sys.path.insert(0, str(Path(__file__).parent))
src = open(Path(__file__).parent / "tool.py", encoding="utf-8").read().split('if stage == "prep"')[0]
exec(src)
S = Path(r"C:\Users\sanjay\AppData\Local\Temp\claude\6f3845a98aec2db1\ecb1ec02-c324-461d-961b-93c565ac5a20\scratchpad"); S.mkdir(exist_ok=True)
R = V / "_review_holdfix1"; R.mkdir(exist_ok=True)
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
def probe(f, sel): return sh("ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", "stream=duration,nb_frames", "-of", "csv=p=0", str(f)).strip()
print("video", probe(OUT, "v"), "audio", probe(OUT, "a"))
def md5(f, n):
    o = sh("ffmpeg", "-v", "error", "-i", str(f), "-an", "-frames:v", str(n), "-f", "framemd5", "-")
    return [l.split(",")[-1].strip() for l in o.splitlines() if not l.startswith("#")]
a, b = md5(FINAL, f0), md5(OUT, f0); print("frames 0..%d identical to old final:" % (f0 - 1), a == b, len(a), len(b))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(OUT), "-vn", "-ac", "2", "-ar", "44100", str(S / "n.wav")])
sr, x = wf.read(S / "n.wav"); x = x.astype(float) / 32768; Tn = len(x) / sr
r = lambda s, e: round(20 * np.log10(np.sqrt((x[int(s * sr):int(e * sr)] ** 2).mean()) + 1e-9), 1)
print("hold after last word:", round(Tn - LASTEND, 3), "last sample", x[-1], "last .1s peak", abs(x[-int(.1 * sr):]).max())
print("rms/0.5s last 5s:", [r(Tn - 5 + i * .5, Tn - 4.5 + i * .5) for i in range(10)])
# crossfade smoothness
Lend = len(sf := wf.read(A / "_cur.wav")[1]) / sr
print("rms/50ms around old end", [r(Lend - .4 + i * .05, Lend - .35 + i * .05) for i in range(12)])
ts = [f0 / 30 - .05, f0 / 30 + .1, LASTEND, f1 / 30 - .05, f1 / 30 + .05, (f1 + f2) / 60, T - .05]
for i, t in enumerate(ts):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(OUT), "-frames:v", "1", "-vf", "scale=240:-1", str(R / f"f{i}.png")])
subprocess.run(["ffmpeg", "-y", "-v", "error"] + sum([["-i", str(R / f"f{i}.png")] for i in range(7)], []) + ["-filter_complex", "hstack=inputs=7", str(R / "sheet.png")])
print("sheet", R / "sheet.png")
