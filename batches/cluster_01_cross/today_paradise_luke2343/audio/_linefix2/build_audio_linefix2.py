r"""today_paradise linefix2 audio: linefix1 mix kept to new 55.86 s, then the film's OWN score (run_piece.score_cmd, outro_hold 6 s; same music files/dips/cta_dip)
continues past the last word: +5 dB lift (1.2 s smooth) through the landing hold, then a 2.5 s cos^2 fade ending at exactly zero on the last frame.
usage: build_audio_linefix2.py <video_seconds>"""
import subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
H=Path(__file__).resolve().parent; SR=44100
T=float(sys.argv[1]); N=int(round(T*SR))
def dec(src):
    out=H/"_tmp_dec2.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vn","-ac","2","-ar",str(SR),"-c:a","pcm_s16le",str(out)],check=True)
    return wf.read(out)[1].astype(np.float64)/32768
L1=wf.read(H.parent/"_linefix1"/"narration_linefix1_mix.wav")[1].astype(np.float64)/32768
SX=dec(H/"scored_ext.mp4")
si=int((7.78-(7.8333-4.7))*SR) ; so=int(7.78*SR); shift=so-si; LAG=219; g=0.9965
# fit shift/lag check on narration+music region new 40..55 s
a,b=int(40*SR),int(55*SR)
best=max(((float((L1[a:b]*SX[a+shift-LAG+d:b+shift-LAG+d]).sum()/np.sqrt((L1[a:b]**2).sum()*(SX[a+shift-LAG+d:b+shift-LAG+d]**2).sum())),d) for d in range(-40,41,1)))
print("align corr,delta",best); d=best[1]
ext=np.zeros((N,2)); n0=0; seg=SX[shift-LAG+d:shift-LAG+d+N]; ext[:len(seg)]=g*seg
t=np.arange(N)/SR
# lift (music-only region after the last word 55.84)
L0=55.90; x=np.clip((t-L0)/1.2,0,1); lift=10**((5*(x*x*(3-2*x)))/20)
ext*=lift[:,None]
base=np.zeros((N,2)); m=min(N,len(L1)); base[:m]=L1[:m]
xs=int(55.86*SR); xf=int(0.05*SR); w=np.zeros(N); w[xs:xs+xf]=np.linspace(0,1,xf); w[xs+xf:]=1
out=base*(1-w[:,None])+ext*w[:,None]
f0=T-2.5; y=np.clip((t-f0)/2.5,0,1); env=0.5*(1+np.cos(np.pi*y)); out*=env[:,None]; out[-1]=0
out=np.clip(out,-0.97,0.97)
wf.write(H/"narration_linefix2_mix.wav",SR,(out*32767).astype(np.int16)); print("ok",N/SR)
