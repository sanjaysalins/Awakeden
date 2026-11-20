"""Full forced alignment (narrator + scripture) of the locked narration.mp3 -> audio/alignment.json.
(batches/_align_short.py only reads <speaker> tags, so it missed every narrator line here.)"""
import json, re
from pathlib import Path
AUD = Path(__file__).resolve().parents[1] / "audio"
t = (AUD / "narration-tagged.md").read_text(encoding="utf-8")
t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
t = re.sub(r"</?speaker[^>]*>", "", t)
t = re.sub(r"\[[a-z\- ]+\]", "", t)
spoken = " ".join(t.split())
(AUD / "narration.spoken.txt").write_text(spoken, encoding="utf-8")
import whisperx
audio = whisperx.load_audio(str(AUD / "_align16k.wav"))
dur = len(audio) / 16000.0
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
r = whisperx.align([{"start": 0.0, "end": dur, "text": spoken}], m, meta, audio, "cpu")
words = [{"w": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in r["word_segments"] if "start" in w]
(AUD / "alignment.json").write_text(json.dumps(words), encoding="utf-8")
print(len(spoken.split()), "words in text,", len(words), "aligned over", round(dur, 2))
