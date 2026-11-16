import sys, subprocess
from PIL import Image
out = sys.argv[1]; clips = sys.argv[2:]
rows = []
for c in clips:
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",c],capture_output=True,text=True).stdout)
    ims = []
    for f in (0, .3, .6, .9):
        t = min(dur * f, dur - 0.1) if f < .9 else min(4.4 if dur < 6 else 6.1, dur - 0.05)
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.3f}","-i",c,"-frames:v","1","-vf","scale=330:-2","_t.png"])
        ims.append(Image.open("_t.png").convert("RGB"))
    r = Image.new("RGB", (330*4, ims[0].height))
    for i, m in enumerate(ims): r.paste(m, (330*i, 0))
    rows.append(r)
s = Image.new("RGB", (330*4, sum(r.height for r in rows)))
y = 0
for r in rows: s.paste(r, (0, y)); y += r.height
s.save(out, quality=88)
