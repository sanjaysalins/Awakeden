import json, subprocess
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
spoken = open(H/"spoken_wordsfix1.txt", encoding="utf-8").read().strip()
wav = H/"_align16k.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_wordsfix1.wav"),"-ac","1","-ar","16000",str(wav)],check=True)
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
audio = whisperx.load_audio(str(wav)); dur = len(audio)/16000
res = whisperx.align([{"start":0.0,"end":dur,"text":spoken}], m, meta, audio, "cpu")
words = [{"w":w["word"],"start":round(w["start"],3),"end":round(w["end"],3)} for w in res["word_segments"] if "start" in w]
(H/"alignment_wordsfix1.json").write_text(json.dumps(words), encoding="utf-8")
print(len(words), "of", len(spoken.split()), round(dur,2))
print(" ".join("%s@%.2f-%.2f"%(w["w"],w["start"],w["end"]) for w in words))
