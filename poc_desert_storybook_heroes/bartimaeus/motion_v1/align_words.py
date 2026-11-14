"""$0 offline word times for the motion layer (faster-whisper ASR aligned to the known script)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT))
from pipeline.assembly_align import _whisper_align
B = Path(__file__).resolve().parents[1]
tl = json.loads((B / "audio/timeline.json").read_text(encoding="utf-8"))
words = _whisper_align(B / "audio/narration.mp3", " ".join(x["text"] for x in tl))
out = [{"w": getattr(w, "text", None) or getattr(w, "word", ""), "s": round(w.start, 3), "e": round(w.end, 3)} for w in words]
(B / "motion_v1/words.json").write_text(json.dumps(out, indent=0), encoding="utf-8")
print(len(out), "words")
