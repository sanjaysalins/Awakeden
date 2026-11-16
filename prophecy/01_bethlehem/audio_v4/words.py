"""$0 faster-whisper word times for each take -> narration_v4_take<N>.whisper.json + a word-diff vs the locked script."""
import json, re, sys
from pathlib import Path
from faster_whisper import WhisperModel
H = Path(__file__).resolve().parent
m = WhisperModel("small.en", device="cpu", compute_type="int8")
script = re.sub(r"<[^>]+>", " ", (H / "narration-tagged.md").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower()).split()
for take in sys.argv[1:]:
    segs, _ = m.transcribe(str(H / f"narration_v4_take{take}.mp3"), word_timestamps=True, language="en", initial_prompt="Micah, Bethlehem, Judaea, Galilee, Herod")
    W = [{"w": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in s.words]
    (H / f"narration_v4_take{take}.whisper.json").write_text(json.dumps(W, indent=0), encoding="utf-8")
    import difflib
    a, b = norm(script), norm(" ".join(x["w"] for x in W))
    diffs = [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes() if op != "equal"]
    print("take", take, "words", len(b), "script", len(a), "last word end", W[-1]["end"], "diffs:", diffs)
