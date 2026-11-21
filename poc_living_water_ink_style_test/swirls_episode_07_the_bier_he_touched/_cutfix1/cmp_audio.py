import subprocess, sys, numpy as np
def dec(p):
    b=subprocess.run(["ffmpeg","-v","error","-i",p,"-vn","-f","f32le","-ac","2","-ar","44100","-"],capture_output=True).stdout
    return np.frombuffer(b,np.float32).reshape(-1,2)
a=dec(sys.argv[1]); b=dec(sys.argv[2]); n=min(len(a),len(b)); print("len",len(a)/44100,len(b)/44100)
d=a[:n]-b[:n]
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-12)
print("ref rms %.1f dB, residual %.1f dB"%(db(a[:n]),db(d)))
for s,e in [(0,6),(6,74),(74,84)]:
    i,j=int(s*44100),min(int(e*44100),n); print(s,e,"ref %.1f res %.1f"%(db(a[i:j]),db(d[i:j])))
