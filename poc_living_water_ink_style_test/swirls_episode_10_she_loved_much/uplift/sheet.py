import subprocess, os, sys
from PIL import Image
name=sys.argv[1]; n=6
d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{name}.mp4"],capture_output=True,text=True).stdout)
ims=[]
for i in range(n):
    t=min(d-0.05,d*i/(n-1))
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.3f}","-i",f"{name}.mp4","-frames:v","1","-vf","crop=1072:1300:0:628,scale=300:-2",f"_t{i}.png"])
    ims.append(Image.open(f"_t{i}.png").copy())
s=Image.new("RGB",(sum(i.width for i in ims),ims[0].height)); x=0
for i in ims: s.paste(i,(x,0)); x+=i.width
s.save(f"{name}_sheet.jpg",quality=85)
for i in range(n): os.remove(f"_t{i}.png")
