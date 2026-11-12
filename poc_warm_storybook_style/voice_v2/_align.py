"""Force-align narration.mp3 to narration.md text -> narration.alignment.json (whisperx, CPU, $0)."""
import json, re, subprocess
from pathlib import Path
EP = Path(__file__).resolve().parent
txt = (EP / "narration.md").read_text(encoding="utf-8")
spoken = " ".join(re.sub(r"^(NARRATOR|JESUS|MARTHA):\s*", "", l).strip() for l in txt.splitlines() if l.strip() and not l.startswith("<!--"))
wav = EP / "_align16k.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "3", "-i", str(EP / "narration.mp3"), "-ac", "1", "-ar", "16000", str(wav)], check=True)
import whisperx
audio = whisperx.load_audio(str(wav)); dur = len(audio) / 16000.0
m, meta = whisperx.load_align_model(language_code="en", device="cpu")
res = whisperx.align([{"start": 0.0, "end": dur, "text": spoken}], m, meta, audio, "cpu")
words = [{"w": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in res["word_segments"] if "start" in w]
(EP / "narration.alignment.json").write_text(json.dumps(words), encoding="utf-8")
print(f"aligned {len(words)} words over {dur:.2f}s")
