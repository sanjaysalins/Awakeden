import json, subprocess, sys
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
TEXT = "People were dying of snake bites. God's cure was a snake on a pole."
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
for t in "ab":
    w = H/f"first_{t}.wav"   # atempo 0.9721 (the film's own narrator tempo), 16k mono for alignment
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/f"first_narrator_{t}.mp3"),"-filter:a","atempo=0.9721","-ac","1","-ar","16000",str(w)],check=True)
    a = whisperx.load_audio(str(w)); dur=len(a)/16000
    r = whisperx.align([{"start":0.0,"end":dur,"text":TEXT}], m, meta, a, "cpu")
    ws = [(x["word"],round(x["start"],3),round(x["end"],3)) for x in r["word_segments"]]
    print(t, round(dur,3), ws)
