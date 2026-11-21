import json, subprocess
from pathlib import Path
import torch; torch.set_num_threads(3)
import whisperx
H = Path(__file__).resolve().parent
T = json.loads((H.parent/"audio"/"jericho"/"timing.json").read_text())["lines"]
spoken = ("When Jericho fell, the only family that walked out alive was a prostitute's. Her name was Rahab. She lived in Jericho's wall. The Bible calls her a prostitute. Two spies came from God's people, Israel. "
 + T[1]["text"] + " " + T[2]["text"] + " " + T[3]["text"] + " Rahab could not stop a wall. She tied one cord to a promise. Whatever they call you, her name is in His family. There is room for yours.").replace('"', "")
wav = H/"_align16k.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(H/"narration_linefix1.wav"),"-ac","1","-ar","16000",str(wav)],check=True)
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
audio = whisperx.load_audio(str(wav)); dur = len(audio)/16000
res = whisperx.align([{"start":0.0,"end":dur,"text":spoken}], m, meta, audio, "cpu")
words = [{"w":w["word"],"start":round(w["start"],3),"end":round(w["end"],3)} for w in res["word_segments"] if "start" in w]
(H/"alignment_linefix1.json").write_text(json.dumps(words), encoding="utf-8")
print(len(words), "of", len(spoken.split()), round(dur,2))
