"""One-off: derive real per-unit boundaries from narration.alignment.json,
walked through the MANIFEST word counts, per SCORE_DESIGN_EARLY.md section 6.2
and swirls_assemble.py's _unit_slots_from_timing_file() contract (unit k spans
[start_s of unit k's first spoken word, start_s of unit k+1's first spoken
word); last unit runs to narration_end + outro_hold).
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTRO_HOLD = 3.0

UNITS = [
    ("front", 14), ("f01", 25), ("f02", 21), ("f03", 22), ("f04", 14),
    ("f05", 28), ("f06", 28), ("f07", 17), ("f08", 13), ("f09", 21), ("back", 24),
]


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


d = json.load(open(HERE / "narration.alignment.json", encoding="utf-8"))
words = [w for w in d["words"] if re.search(r"[A-Za-z0-9]", w["text"])]
assert len(words) == 227, f"expected 227 spoken tokens, got {len(words)}"

narration_seconds = dur(HERE / "narration.mp3")

idx = 0
first_starts = []  # (tag, first_word_start, text)
for tag, n in UNITS:
    chunk = words[idx:idx + n]
    first_starts.append((tag, chunk[0]["start"], " ".join(w["text"] for w in chunk)))
    idx += n

units_out = {}
for i, (tag, start, text) in enumerate(first_starts):
    start_s = 0.0 if i == 0 else start
    if i + 1 < len(first_starts):
        end_s = first_starts[i + 1][1]
    else:
        end_s = round(narration_seconds + OUTRO_HOLD, 3)
    units_out[tag] = {"start_s": round(start_s, 3), "end_s": round(end_s, 3)}
    print(f"{tag:6} {start_s:7.3f} -> {end_s:7.3f}  ({end_s - start_s:5.3f}s)  {text}")

out_doc = {
    "schema": "swirls-of-life/unit_timing v1",
    "episode": HERE.name,
    "written": "2026-09-07",
    "source": "narration.alignment.json (ElevenLabs forced alignment, real per-word timestamps)",
    "boundary_rule": "unit k spans [start_s of unit k's first spoken word, start_s of unit k+1's first spoken word); the last unit runs to narration_end + outro_hold",
    "narration_seconds": round(narration_seconds, 3),
    "outro_hold_seconds": OUTRO_HOLD,
    "units": units_out,
}
with open(HERE / "unit_timing.json", "w", encoding="utf-8") as f:
    json.dump(out_doc, f, indent=2)
print(f"\nwrote {HERE / 'unit_timing.json'}  (narration={narration_seconds:.3f}s)")
