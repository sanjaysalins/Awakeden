import subprocess, sys, numpy as np
def load(p):
    b=subprocess.run(["ffmpeg","-v","error","-i",p,"-vn","-f","f32le","-ac","1","-ar","44100","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32)
def env(x,a,b,step=0.25):
    out=[]
    t=a
    while t<b:
        s=x[int(t*44100):int((t+step)*44100)]
        out.append("%.2f:%.0f"%(t,20*np.log10(np.sqrt(np.mean(s**2))+1e-9)))
        t+=step
    return " ".join(out)
n=load("../narration.mp3"); s=load("../score_piano.mp3")
for a,b in ((11.5,17.5),(25,29.5)):
    print("NARR",env(n,a,b,0.2)); print("SCORE",env(s,a-1,b+1,0.25))
