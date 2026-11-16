import sys, subprocess
from PIL import Image
clip, out = sys.argv[1], sys.argv[2]
fr = sys.argv[3:] or ["0", "30", "60", "90", "-1"]
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",clip],capture_output=True,text=True).stdout)
ims = []
for t in fr:
    tt = float(t)
    if tt < 0: tt = dur - 0.05
    else: tt = tt / 24.0 if tt > 20 else tt
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{tt:.3f}","-i",clip,"-frames:v","1","-vf","scale=432:-2","_t.png"])
    ims.append(Image.open("_t.png").convert("RGB"))
s = Image.new("RGB", (sum(i.width for i in ims), ims[0].height))
x = 0
for i in ims: s.paste(i, (x, 0)); x += i.width
s.save(out, quality=88)
print(dur)
