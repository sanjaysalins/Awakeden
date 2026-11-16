import sys, subprocess
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
ts=[0.0,d*0.33,d*0.66,d-0.1]; ims=[]
for i,t in enumerate(ts):
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.2f}","-i",src,"-frames:v","1","-vf","scale=450:-2",f"work/_t{i}.png"])
    ims.append(Image.open(f"work/_t{i}.png"))
s=Image.new("RGB",(450*4,ims[0].height))
for i,im in enumerate(ims): s.paste(im,(450*i,0))
s.save(out,quality=85)
