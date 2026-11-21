import json, subprocess, sys, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
T={"mid":"Long before, in God's law, the animal offered for sin was burned outside the camp.",
   "end":"Reproach means shame. Simon was forced out there. You are invited. If shame has put you outside, Jesus is already there. The dying, the finishing, was His alone. You only come to Him."}
takes=sys.argv[1:] or ["mid_a","end_a"]
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
res={}
for k in takes:
    which,take=k.split("_"); src=H/f"{which}_narrator_{take}.mp3"; wav=H/f"_{k}_16k.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(src),"-ac","1","-ar","16000",str(wav)],check=True)
    audio=whisperx.load_audio(str(wav)); dur=len(audio)/16000
    r=whisperx.align([{"start":0.0,"end":dur,"text":T[which]}],m,meta,audio,"cpu")
    w=[{"w":x["word"],"start":round(x["start"],3),"end":round(x["end"],3)} for x in r["word_segments"] if "start" in x]
    res[k]={"dur":dur,"words":w}
    print(k,dur,[(x["w"],x["start"],x["end"]) for x in w])
p=H/"new_words_rel.json"; old=json.loads(p.read_text()) if p.exists() else {}
old.update(res); p.write_text(json.dumps(old,indent=1),encoding="utf-8")
