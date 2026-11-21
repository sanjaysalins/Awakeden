import json, subprocess
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
old = (H.parent/"_spoken.txt").read_text(encoding="utf-8")
i = old.index("God hung up a snake.")
spoken = ("People were dying of snake bites. God's cure was a snake on a pole. " + old[i:]).replace('"', "")
wav = H/"_align16k.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_linefix1.wav"),"-ac","1","-ar","16000",str(wav)],check=True)
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
audio = whisperx.load_audio(str(wav)); dur = len(audio)/16000
res = whisperx.align([{"start":0.0,"end":dur,"text":spoken}], m, meta, audio, "cpu")
words = [{"w":w["word"],"start":round(w["start"],3),"end":round(w["end"],3)} for w in res["word_segments"] if "start" in w]
(H/"alignment_linefix1.json").write_text(json.dumps(words), encoding="utf-8")
print(len(words), "of", len(spoken.split()), round(dur,2)); print(words[:18]); print(words[-2:])
