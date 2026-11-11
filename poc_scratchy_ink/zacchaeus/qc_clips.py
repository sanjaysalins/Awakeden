"""QC sheet per clip: first / mid / last frame + mean pixel diff first->last (frozen check). Usage: qc_clips.py c01,c02,..."""
import subprocess, sys, json
from pathlib import Path
import numpy as np
C = Path(__file__).resolve().parent/"clips"; Q = C/"_qc"; Q.mkdir(exist_ok=True)
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
def frame(f,t,w=160):
    r=subprocess.run(["ffmpeg","-v","error","-threads","3","-ss",f"{t:.3f}","-i",str(f),"-frames:v","1","-vf",f"scale={w}:-2","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True)
    return np.frombuffer(r.stdout,np.uint8).astype(float)
ks=sys.argv[1].split(",")
for k in ks:
    f=C/f"{k}.mp4"; d=dur(f)
    a,b,m=frame(f,0),frame(f,d-0.2),frame(f,d/2)
    print(k, f"{d:.2f}s", "diff first->mid %.1f  first->last %.1f" % (abs(a-m).mean(), abs(a-b).mean()))
    subprocess.run(["ffmpeg","-v","error","-threads","3","-y","-i",str(f),"-ss",f"{d/2:.3f}","-i",str(f),"-sseof","-0.2","-i",str(f),"-filter_complex",
      "[0:v]trim=end_frame=1,scale=300:-2[a];[1:v]trim=end_frame=1,scale=300:-2[b];[2:v]trim=end_frame=1,scale=300:-2[c];[a][b][c]hstack=3","-frames:v","1",str(Q/f"{k}.jpg")])
