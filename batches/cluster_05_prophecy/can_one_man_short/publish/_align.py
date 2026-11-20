import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs,_ = m.transcribe(sys.argv[1], word_timestamps=True, language="en")
out=[]
for s in segs:
    for w in s.words: out.append({"w":w.word.strip(),"start":round(w.start,2),"end":round(w.end,2)})
json.dump(out, open(sys.argv[2],"w"), indent=1)
print(len(out), " ".join(x["w"] for x in out))
