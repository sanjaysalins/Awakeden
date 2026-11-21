import sys
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=3)
for f in sys.argv[1:]:
    segs, _ = m.transcribe(f, language="en", word_timestamps=True)
    ws = [w for s in segs for w in s.words]
    print(f, "|", " ".join(w.word.strip() for w in ws))
