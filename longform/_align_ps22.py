"""Force-align the Psalm 22 long-form narration -> alignment.json + print anchors."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible")
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script  # noqa: E402

V1 = ROOT / "longform" / "02_Psalm_22_Song_From_The_Cross" / "v1"
SPOKEN = (V1 / "narration.spoken.txt").read_text(encoding="utf-8")
WAV = V1 / "_align16k.wav"

if not WAV.exists():
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(V1 / "narration.mp3"), "-ac", "1", "-ar", "16000", str(WAV)], check=True)

print(f"[align] {len(SPOKEN.split())} words")
words = forced_align_script(str(WAV), SPOKEN)
(V1 / "alignment.json").write_text(json.dumps(words, indent=2), encoding="utf-8")
print(f"[align] wrote {len(words)} -> alignment.json")

ANCHORS = ["forsaken", "worm", "scorn", "deliver", "water", "joint", "tongue", "thirst",
           "pierced", "lots", "vesture", "garments", "divided", "brethren", "congregation",
           "heard", "ends", "nations", "finished", "done", "praise"]

for a in ANCHORS:
    hits = [w for w in words if re.sub(r"[^a-z]", "", w["w"].lower()) == a]
    for h in hits:
        print(f"  {a:<12} {h['start']:.2f}-{h['end']:.2f}s")
print(f"  [last] '{words[-1]['w']}' {words[-1]['end']:.2f}s")
