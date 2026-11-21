import json, subprocess, whisperx
from pathlib import Path
H=Path(__file__).resolve().parent
spoken="You were not there. He spoke about you anyway, and called you blessed."
wav=H/"_a16k.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"28_narrator_a__atempo.mp3"),"-ac","1","-ar","16000",str(wav)],check=True)
audio=whisperx.load_audio(str(wav)); dur=len(audio)/16000
m,meta=whisperx.load_align_model(language_code="en",device="cpu")
r=whisperx.align([{"start":0.0,"end":dur,"text":spoken}],m,meta,audio,"cpu")
w=[{"w":x["word"],"start":round(x["start"],3),"end":round(x["end"],3)} for x in r["word_segments"] if "start" in x]
(H/"new_line_words_rel.json").write_text(json.dumps(w),encoding="utf-8"); print(dur,w)
