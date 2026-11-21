import subprocess
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
TX = {"first": "Adam and Eve hid among the trees, afraid.", "last": "That promise has a name now: Jesus. Before the sentence, grace spoke first."}
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
for n, text in TX.items():
  for t in "ab":
    w = H/f"_{n}_{t}.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/f"{n}_narrator_{t}.mp3"),"-ac","1","-ar","16000",str(w)],check=True)
    a = whisperx.load_audio(str(w)); dur=len(a)/16000
    r = whisperx.align([{"start":0.0,"end":dur,"text":text}], m, meta, a, "cpu")
    print(n, t, round(dur,3), [(x["word"],round(x["start"],2),round(x["end"],2)) for x in r["word_segments"]])
