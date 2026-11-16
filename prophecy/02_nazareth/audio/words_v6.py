"""$0 faster-whisper word times for narration_v6.mp3 (voice B, owner 'go with your pick' 2026-11-16) -> narration_v6.words.json + word-diff vs locked words v6."""
import json, re, difflib
from pathlib import Path
from faster_whisper import WhisperModel
H = Path(__file__).resolve().parent
script = re.sub(r"\[[a-z]+\]|\(pause\)", " ", (H.parent / "words/FINAL_WORDS_v6.md").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower()).split()
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(str(H / "narration_v6.mp3"), word_timestamps=True, language="en", initial_prompt="Nazareth, Isaiah, Physician, heal thyself")
W = [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in s.words]
(H / "narration_v6.words.json").write_text(json.dumps(W, indent=0), encoding="utf-8")
a, b = norm(script), norm(" ".join(x["w"] for x in W))
print("words", len(b), "script", len(a), "last word end", W[-1]["end"])
print("diffs:", [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"])
