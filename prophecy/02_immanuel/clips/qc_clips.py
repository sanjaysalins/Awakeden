"""$0 clip QC: 6-frame strip incl. true first + last frame, and mean motion (pixel diff) per clip.
  python qc_clips.py P1 M1 ...  -> _strip_<n>.jpg + printed duration / motion"""
import sys, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image
H = Path(__file__).resolve().parent
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
def frame(f, t):
    r = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(f),"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True)
    import io; return Image.open(io.BytesIO(r.stdout)).convert("RGB")
for n in sys.argv[1:]:
    f = H / f"{n}.mp4"; d = dur(f)
    ts = [0.0] + [d * k / 5 for k in range(1, 5)] + [max(0.0, d - 0.06)]
    ims = [frame(f, t) for t in ts]
    w, h = 240, 426
    strip = Image.new("RGB", (w * 6 + 25, h), "white")
    for i, im in enumerate(ims): strip.paste(im.resize((w, h)), (i * (w + 5), 0))
    strip.save(H / f"_strip_{n}.jpg", quality=85)
    a = [np.asarray(im.resize((180, 320)), dtype=np.float32) for im in ims]
    diffs = [float(np.abs(a[i+1] - a[i]).mean()) for i in range(5)]
    print(n, f"{d:.2f}s", "motion", [round(x, 1) for x in diffs], "first-last", round(float(np.abs(a[-1]-a[0]).mean()), 1))
