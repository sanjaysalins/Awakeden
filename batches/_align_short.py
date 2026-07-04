#!/usr/bin/env python
"""Force-align a short's narration.mp3 to its spoken text -> alignment.json.
Reusable across the cluster roll:  _align_short.py "<piece>/audio"
Builds narration.spoken.txt from narration-tagged.md, 16k mono wav, whisperx align."""
import json, re, subprocess, sys
from pathlib import Path

AUD = Path(sys.argv[1]).resolve()
tagged = (AUD / "narration-tagged.md").read_text(encoding="utf-8")
spoken = " ".join(m.group(1).strip() for m in
                  re.finditer(r"<speaker name=\"[^\"]+\">(.*?)</speaker>", tagged, re.S))
(AUD / "narration.spoken.txt").write_text(spoken, encoding="utf-8")

wav = AUD / "_align16k.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(AUD / "narration.mp3"),
                "-ac", "1", "-ar", "16000", str(wav)], check=True)

import whisperx
audio = whisperx.load_audio(str(wav))
dur = len(audio) / 16000.0
model_a, meta = whisperx.load_align_model(language_code="en", device="cpu")
result = whisperx.align([{"start": 0.0, "end": dur, "text": spoken}],
                        model_a, meta, audio, "cpu")
words = [{"w": w["word"], "start": round(w["start"], 3), "end": round(w["end"], 3)}
         for w in result["word_segments"] if "start" in w]
(AUD / "alignment.json").write_text(json.dumps(words), encoding="utf-8")
print(f"aligned {len(words)} words over {dur:.2f}s -> {AUD / 'alignment.json'}")
