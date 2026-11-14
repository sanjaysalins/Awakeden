import subprocess,sys,os
from PIL import Image, ImageDraw
CUT=[0,99,240,396,471,567,711,867,1023,1101,1206,1434,1596,1806,2034,2256,2409,2637]
A={2:6,5:6,6:7,7:8,9:3,10:6,12:10,17:8}  # incoming a (index 1-based shot)
B={2:8,5:8,6:7,7:6,9:7,10:8,12:4,17:6}
CLIP="F:/slk/PycharmProjects/JesusInTheBible/_remotion/public/sf/s%02d.mp4"
os.makedirs("fr",exist_ok=True)
for n in range(1,18):
    start=CUT[n-1]-A.get(n,0); end=CUT[n]+B.get(n+1,0)
    ts=[(CUT[n-1]-start)/30,((CUT[n-1]+CUT[n])/2-start)/30,(CUT[n]-1-start)/30]
    for k,t in enumerate(ts):
        out="fr/s%02d_%d.png"%(n,k)
        subprocess.run(["ffmpeg","-y","-v","error","-threads","3","-ss","%.3f"%t,"-i",CLIP%n,"-frames:v","1","-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",out])
    print(n,start,end,(end-start)/30,ts)
