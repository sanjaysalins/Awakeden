"""QC sheet per clip: frames at 0, 25, 50, 75, 100% + mean pixel change first->last and max step. $0."""
import subprocess, sys, numpy as np
from pathlib import Path
from PIL import Image
D = Path(__file__).resolve().parent
def frames(f, n=5):
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
    out = []
    for i in range(n):
        t = min(d - 0.05, d * i / (n - 1))
        raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(f),"-frames:v","1","-vf","scale=268:482","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        out.append(np.frombuffer(raw, np.uint8).reshape(482, 268, 3))
    return d, out
for k in sys.argv[1:]:
    f = D/f"{k}.mp4"; d, fr = frames(f)
    diff = [float(np.abs(fr[i+1].astype(int)-fr[i].astype(int)).mean()) for i in range(4)]
    tot = float(np.abs(fr[-1].astype(int)-fr[0].astype(int)).mean())
    Image.fromarray(np.hstack(fr)).save(D/f"_qc_{k}.jpg", quality=80)
    print(f"{k} {d:.2f}s  first->last {tot:5.1f}  steps {' '.join(f'{x:4.1f}' for x in diff)}")
