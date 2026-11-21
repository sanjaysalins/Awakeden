import subprocess, sys, numpy as np
b=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-vn","-f","f32le","-ac","1","-ar","44100","-"],capture_output=True).stdout
x=np.frombuffer(b,np.float32); n=len(x)/44100; print("audio s %.3f"%n)
t0=n-5
out=[]
for k in range(20):
    s=int((t0+k*0.25)*44100); e=int((t0+(k+1)*0.25)*44100); seg=x[s:e]
    out.append(20*np.log10(np.sqrt(np.mean(seg**2))+1e-9) if len(seg) else -99)
print(" ".join("%.0f"%v for v in out)); print("last 0.1 s peak %.5f"%np.abs(x[-4410:]).max())
