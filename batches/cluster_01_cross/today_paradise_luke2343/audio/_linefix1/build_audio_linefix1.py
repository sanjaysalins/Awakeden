r"""today_paradise linefix1 audio: head 0..seam = 0.xx x score-stage(new engine head: new narration + engine sfx), then the pinned film's audio
from OLD 7.78 s (silent gap before 'Both') shifted earlier by DELTA. Writes narration_linefix1_mix.wav (stereo 44.1k)."""
import json, subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
H=Path(__file__).resolve().parent; PIECE=H.parents[1]; ROOT=PIECE.parents[2]
sys.path.insert(0,str(ROOT)); import run_piece
pj=json.loads((PIECE/"piece.json").read_text(encoding="utf-8"))
pj["score"]["src"]=str(PIECE/"visual/_linefix1_pool/livingpage_short.linefix1.spec_preview.mp4")
tmp=H/"_score_head_new.mp4"; pj["score"]["out"]=str(tmp)
cmd=run_piece.score_cmd(PIECE,pj); cmd=cmd[:-1]+["-t","6.0",cmd[-1]]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
SR=44100
def dec(src):
    out=H/"_tmp_dec.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-vn","-ac","2","-ar",str(SR),"-c:a","pcm_s16le",str(out)],check=True)
    return wf.read(out)[1].astype(np.float64)/32768
F=dec(PIECE/"visual/today_paradise_luke2343_sfx_v5hook.mp4"); SC=dec(tmp); SCOLD=dec(PIECE/"visual/today_paradise_luke2343_scored.mp4")
a,b=int(0.3*SR),int(7.0*SR)
best=None
for LAG in range(0,800,1):
    x=F[a+LAG:b+LAG].ravel(); y=SCOLD[a:b].ravel()
    c=float((x*y).sum()/np.sqrt((x*x).sum()*(y*y).sum()))
    if best is None or c>best[0]: best=(c,LAG)
c,LAG=best; x=F[a+LAG:b+LAG]; y=SCOLD[a:b]; g=float((x*y).sum()/(y*y).sum()); print("corr",c,"LAG",LAG,"gain",g)
DELTA=7.8333-4.7                      # old->new shift (s)
SEAM_OLD=7.78; SEAM_NEW=SEAM_OLD-DELTA
si=int(SEAM_NEW*SR); so=int(SEAM_OLD*SR); xf=int(0.06*SR)
head=np.zeros((si+LAG,2)); n=min(len(head)-LAG,len(SC)); head[LAG:LAG+n]=g*SC[:n]; head[:LAG]=F[:LAG]
tail=F[so:]
out=np.zeros((si+len(tail),2)); out[:si]=head[:si]; out[si:]=tail
t=np.linspace(0,1,xf)[:,None]
out[si-xf:si]=head[si-xf:si]*(1-t)+F[so-xf:so]*t
out=np.clip(out,-0.99,0.99)
wf.write(H/"narration_linefix1_mix.wav",SR,(out*32767).astype(np.int16)); print("ok",len(out)/SR)
