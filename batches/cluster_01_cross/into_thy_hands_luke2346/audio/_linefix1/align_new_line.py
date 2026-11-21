import json, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
spoken="If you are afraid to die, listen to the last thing Jesus said."
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
res={}
for t in "ab":
    audio=whisperx.load_audio(str(H/f"_first_{t}_16k.wav")); dur=len(audio)/16000
    r=whisperx.align([{"start":0.0,"end":dur,"text":spoken}],m,meta,audio,"cpu")
    w=[{"w":x["word"],"start":round(float(x["start"]),3),"end":round(float(x["end"]),3)} for x in r["word_segments"] if "start" in x]
    res[t]={"dur":dur,"words":w}; print(t,dur,[(x["w"],x["start"],x["end"]) for x in w])
(H/"new_first_words_rel.json").write_text(json.dumps(res,indent=1),encoding="utf-8")
