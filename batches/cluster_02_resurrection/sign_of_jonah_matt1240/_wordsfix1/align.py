import json, subprocess, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent; P=H.parent
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_wordsfix1.mp3"),"-ac","1","-ar","16000",str(H/"_a16k.wav")],check=True)
old=json.load(open(P/"audio/alignment.json",encoding="utf-8"))
# new spoken text: old words, with the three blocks replaced
txt=" ".join(w["w"] for w in old if w["w"]!="—")
rep=[("He sent me to Nineveh, that great city, but I fled toward Tarshish.","He sent me to Nineveh, and I fled. I knew He is gracious, and would spare her."),
     ("Then, long after I was dust, scribes","Then, centuries later, scribes"),
     ("Stop running, and turn: the One who went down into your dark and rose again is Jesus. Come up out of the deep, and live.","The One who went down into your dark and rose again is Jesus. He can bring you up.")]
for a,b in rep:
    assert a in txt,a; txt=txt.replace(a,b)
print(txt)
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
audio=whisperx.load_audio(str(H/"_a16k.wav")); dur=len(audio)/16000
r=whisperx.align([{"start":0.0,"end":dur,"text":txt}],m,meta,audio,"cpu")
ws=[{"w":x["word"],"start":round(float(x["start"]),3),"end":round(float(x["end"]),3)} for x in r["word_segments"]]
assert len(ws)==len(txt.split()),(len(ws),len(txt.split()))
# re-insert the em-dash tokens as the old alignment had them (after 'sea', 'sign', 'guilty', 'far')
out=[]
for i,w in enumerate(ws):
    nxt=ws[i+1]["w"] if i+1<len(ws) else ""
    out.append(w)
    if (w["w"],nxt) in (("sea","and"),("sign","Jesus"),("guilty","the"),("far","that")):
        out.append({"w":"—","start":round(w["end"]+0.02,3),"end":round(w["end"]+0.04,3)})
json.dump(out,open(H/"alignment_wordsfix1.json","w",encoding="utf-8"),ensure_ascii=False)
(H/"narration.spoken_wordsfix1.txt").write_text(" ".join(w["w"] for w in out),encoding="utf-8")
print(" ".join(f"{w['w']}@{w['start']:.2f}-{w['end']:.2f}" for w in out))
