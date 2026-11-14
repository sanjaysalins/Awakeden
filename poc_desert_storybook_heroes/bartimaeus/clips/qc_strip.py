"""QC: 5 frames (first..last) side by side per clip + mean pixel diff first->last. Usage: qc_strip.py s01 s02 ..."""
import subprocess, sys, json
from pathlib import Path
import numpy as np
from PIL import Image
H = Path(__file__).resolve().parent; Q = H / "_qc"; Q.mkdir(exist_ok=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).decode())
def frame(p, t):
    raw = subprocess.check_output(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(p),"-frames:v","1","-vf","scale=270:480","-f","rawvideo","-pix_fmt","rgb24","-"])
    return np.frombuffer(raw, np.uint8).reshape(480,270,3)
out = {}
for s in sys.argv[1:]:
    p = H / f"{s}.mp4"; d = dur(p)
    ts = [0, d*.25, d*.5, d*.75, d-0.06]
    fr = [frame(p,t) for t in ts]
    Image.fromarray(np.hstack(fr)).save(Q / f"{s}_strip.jpg", quality=85)
    diffs = [float(np.abs(fr[i+1].astype(int)-fr[i].astype(int)).mean()) for i in range(4)]
    out[s] = {"dur": round(d,2), "step_diffs": [round(x,1) for x in diffs]}
    print(s, out[s])
