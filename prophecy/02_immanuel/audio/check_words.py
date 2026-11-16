"""$0: transcribe each mix (faster-whisper, word times) and diff against the locked words."""
import re, sys, json
from pathlib import Path
from faster_whisper import WhisperModel
H = Path(__file__).resolve().parent
ref = " ".join(t for _, t in re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H / "narration-tagged.md").read_text(encoding="utf-8")))
norm = lambda s: re.sub(r"[^a-z' ]", " ", s.lower().replace("immanuel", "emmanuel")).split()
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for take in sys.argv[1:]:
    segs, _ = m.transcribe(str(H / f"narration_{take}.mp3"), word_timestamps=True, language="en")
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
    (H / f"narration_{take}.whisper.json").write_text(json.dumps(words, indent=0), encoding="utf-8")
    hyp = norm(" ".join(w["w"] for w in words)); r = norm(ref)
    import difflib
    miss = [(op, r[a:b], hyp[c:d]) for op, a, b, c, d in difflib.SequenceMatcher(None, r, hyp).get_opcodes() if op != "equal"]
    print(take, "words", len(hyp), "/", len(r), "last word ends", words[-1]["e"], "diffs:", miss)
