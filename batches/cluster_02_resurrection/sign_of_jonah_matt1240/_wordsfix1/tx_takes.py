import sys, json, subprocess
from pathlib import Path
from faster_whisper import WhisperModel
H=Path(__file__).resolve().parent
m=WhisperModel("small",device="cpu",compute_type="int8")
for f in sorted(H.glob("n?_?.mp3")):
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout)
    seg,_=m.transcribe(str(f),language="en",word_timestamps=True,vad_filter=False)
    ws=[(w.word.strip(),round(w.start,2),round(w.end,2)) for s in seg for w in s.words]
    print(f.name,round(d,2)); print("  "," ".join(f"{a}@{b}-{c}" for a,b,c in ws))
