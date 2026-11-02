"""Force-align each v4 narration.mp3 to its spoken text -> audio/<piece>/alignment.json (same format as v3)."""
import json, subprocess, sys
from pathlib import Path
import torch
torch.set_num_threads(3)
H = Path(__file__).resolve().parent
import whisperx
model_a, meta = whisperx.load_align_model(language_code="en", device="cpu")
for n in ["jericho", "two_goats", "bronze_serpent"]:
    A = H / "audio" / n
    spoken = " ".join(l["text"] for l in json.loads((A / "timing.json").read_text())["lines"])
    spoken = spoken.replace("“", "").replace("”", "").replace('"', "")
    wav = A / "_align16k.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(A / "narration.mp3"), "-ac", "1", "-ar", "16000", "-threads", "3", str(wav)], check=True)
    audio = whisperx.load_audio(str(wav)); dur = len(audio) / 16000.0
    res = whisperx.align([{"start": 0.0, "end": dur, "text": spoken}], model_a, meta, audio, "cpu")
    words = [{"w": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in res["word_segments"] if "start" in w]
    (A / "alignment.json").write_text(json.dumps(words), encoding="utf-8")
    print(n, len(words), "words of", len(spoken.split()), round(dur, 1), "s", flush=True)
