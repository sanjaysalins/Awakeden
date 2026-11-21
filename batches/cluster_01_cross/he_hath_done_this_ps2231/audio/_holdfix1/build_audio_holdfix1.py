r"""he_hath_done_this holdfix1 audio: the CURRENT final's audio (narration+score+sfx) is kept to its end (42.70 s), cross-faded (0.35 s)
into the film's OWN score continued by run_piece.score_cmd (outro_hold 6 s, same music/dips) - +5 dB lift (1.2 s smooth) after the last
word, then a 2.5 s cos^2 fade ending at exactly zero on the last frame.  usage: build_audio_holdfix1.py <video_seconds>"""
import subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
H=Path(__file__).resolve().parent; SR=44100; PIECE=H.parents[1]
T=float(sys.argv[1]); N=int(round(T*SR))
def dec(src,name):
    out=H/name
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vn","-ac","2","-ar",str(SR),"-c:a","pcm_s16le",str(out)],check=True)
    return wf.read(out)[1].astype(np.float64)/32768
L=dec(PIECE/"visual/he_hath_done_this_ps2231_sfx.mp4","_cur.wav")
X=dec(H/"scored_ext.mp4","_ext.wav")
from scipy.signal import fftconvolve
a,b=int(20*SR),int(36*SR)
x=L[a:b].mean(1); y=X[a-3000:b+3000].mean(1)
cc=fftconvolve(y,x[::-1],mode="valid"); d=int(np.argmax(cc))-3000
xs=X[a+d:b+d].mean(1); print("align delta",d,"corr",float((x*xs).sum()/np.sqrt((x*x).sum()*(xs*xs).sum())))
ext=np.zeros((N,2)); i0=max(0,-d); seg=X[i0+d:i0+d+N-i0]; ext[i0:i0+len(seg)]=seg
# gain match over the music-only region (fit)
t=np.arange(N)/SR
base=np.zeros((N,2)); m=min(N,len(L)); base[:m]=L[:m]
x0=int(42.35*SR); xf=int(0.35*SR); w=np.zeros(N); w[x0:x0+xf]=np.linspace(0,1,xf); w[x0+xf:]=1
L0=42.70; x=np.clip((t-L0)/1.2,0,1); lift=10**((5*(x*x*(3-2*x)))/20); ext=ext*lift[:,None]
out=base*(1-w[:,None])+ext*w[:,None]
f0=T-2.5; y=np.clip((t-f0)/2.5,0,1); env=0.5*(1+np.cos(np.pi*y)); out*=env[:,None]; out[-1]=0
out=np.clip(out,-0.97,0.97)
wf.write(H/"narration_holdfix1_mix.wav",SR,(out*32767).astype(np.int16)); print("ok",N/SR)
