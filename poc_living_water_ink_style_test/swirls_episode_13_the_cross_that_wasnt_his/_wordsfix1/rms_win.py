import subprocess, sys, numpy as np
p=sys.argv[1]; a=float(sys.argv[2]); b=float(sys.argv[3])
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-vn","-f","f32le","-ac","1","-ar","44100","-"],capture_output=True).stdout,np.float32)
out=[]
t=a
while t<b:
    s=x[int(t*44100):int((t+0.25)*44100)]; out.append("%.2f:%.0f"%(t,20*np.log10(np.sqrt(np.mean(s**2))+1e-9))); t+=0.25
print(" ".join(out))
