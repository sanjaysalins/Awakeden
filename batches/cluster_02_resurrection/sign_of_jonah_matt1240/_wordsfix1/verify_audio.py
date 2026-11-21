import numpy as np, scipy.io.wavfile as wf, subprocess, re, sys
from pathlib import Path
H=Path(__file__).resolve().parent; P=H.parent
F=P/"visual/sign_of_jonah_matt1240_sfx_v6trim_wordsfix1.mp4"
w=H/"_final44.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(F),"-vn","-ac","1","-ar","44100","-c:a","pcm_s16le",str(w)],check=True)
sr,x=wf.read(w); x=x/32768.
print("dur",len(x)/sr)
rows=[]
for a in np.arange(55.0,63.9,0.25):
    seg=x[int(a*sr):int(min(63.9,a+0.25)*sr)]; rows.append((round(a,2),round(20*np.log10(np.sqrt((seg**2).mean())+1e-9),1)))
print(rows); print("last 20 samples max",abs(x[-20:]).max())
# narration-only transcript diff vs locked text
locked="I told the sailors to throw me into the sea and a great fish swallowed me whole and buried me alive in the dark I ran from God because His mercy was too wide He sent me to Nineveh and I fled I knew He is gracious and would spare her The storm came for my sake the lot fell on me Then centuries later scribes demanded a sign Jesus gave them only my name For as Jonas was three days and three nights in the whale's belly so shall the Son of man be three days and three nights in the heart of the earth I went down guilty the storm was mine He went down innocent bearing what was ours He gave Himself The grave no more held Him than the deep held me He rose You who are sure you've fallen too far that is how far His mercy reaches The One who went down into your dark and rose again is Jesus He can bring you up"
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_wordsfix1.mp3"),"-ac","1","-ar","16000",str(H/"_n16.wav")],check=True)
def tx(f):
    seg,_=m.transcribe(str(f),language="en",vad_filter=False); return " ".join(s.text.strip() for s in seg)
norm=lambda s:re.sub(r"[^a-z' ]","",s.lower().replace("—"," ")).split()
import difflib
for name,f in (("narration.mp3",H/"_n16.wav"),("final film",H/"_f16.wav")):
    if name=="final film": subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(F),"-vn","-ac","1","-ar","16000",str(f)],check=True)
    a,b=norm(locked),norm(tx(f))
    sm=difflib.SequenceMatcher(None,a,b); print(name,"ratio",round(sm.ratio(),4))
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!="equal": print("  ",op,a[i1:i2],"->",b[j1:j2])
