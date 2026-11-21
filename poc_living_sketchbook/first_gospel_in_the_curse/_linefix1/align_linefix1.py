import json, subprocess
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
old = (H.parent/"_spoken.txt").read_text(encoding="utf-8")
iB = old.index("But before God ever"); iT = old.index("That promise has a name now")
spoken = ("Adam and Eve hid among the trees, afraid. " + old[iB:iT] + "That promise has a name now: Jesus. Before the sentence, grace spoke first.").replace('"', "")
(H/"spoken_linefix1.txt").write_text(spoken, encoding="utf-8")
wav = H/"_align16k.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_linefix1.wav"),"-ac","1","-ar","16000",str(wav)],check=True)
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
audio = whisperx.load_audio(str(wav)); dur = len(audio)/16000
res = whisperx.align([{"start":0.0,"end":dur,"text":spoken}], m, meta, audio, "cpu")
words = [{"w":w["word"],"start":round(w["start"],3),"end":round(w["end"],3)} for w in res["word_segments"] if "start" in w]
(H/"alignment_linefix1.json").write_text(json.dumps(words), encoding="utf-8")
print(len(words), "of", len(spoken.split()), round(dur,2)); print(words[:10]); print(words[-16:])
old_w = json.load(open(H.parent/"_alignment.json", encoding="utf-8-sig"))
# middle words: old 'But'(index 26) .. 'asked.'(index 147?) compare
D = -155/30
bi = next(i for i,x in enumerate(old_w) if x["w"]=="But"); ai = next(i for i,x in enumerate(old_w) if x["w"]=="asked.")
nb = next(i for i,x in enumerate(words) if x["w"]=="But"); na = next(i for i,x in enumerate(words) if x["w"]=="asked.")
print("count mid old", ai-bi, "new", na-nb)
dif = [abs((words[nb+k]["start"])-(old_w[bi+k]["start"]+D)) for k in range(ai-bi+1)]
print("max |new - (old+D)| start:", round(max(dif),3), "mean", round(sum(dif)/len(dif),3))
