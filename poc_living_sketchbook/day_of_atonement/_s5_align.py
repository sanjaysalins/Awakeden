"""Day of Atonement LONG -- step 5: force-align the LOCKED EW01_Two_Goats
long-form narration. Same $0 local pattern as
`poc_living_sketchbook/bronze_serpent_long/_s6_align.py` -- a MEASUREMENT
pass over already-locked, already-voiced audio, no API spend, no text
changes.

Gives assembly real word-level onsets/offsets to snap `_PLAN.md`'s
plan-estimated sub-turn spread boundaries to (turn-level boundaries in the
plan are already ffprobe-hard per _PLAN.md sec 1c; only the INTERIOR/
sub-turn seams inside a turn are estimates that need this).

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s5_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = ROOT / "longform" / "EW01_Two_Goats" / "v1"
OUT_DIR = Path(__file__).resolve().parent


def _clean_spoken(raw: str) -> str:
    text = re.sub(r"\[[^\]]*\]", " ", raw)          # [witness] / [the LORD] / [scripture] tags
    text = re.sub(r"^#.*$", " ", text, flags=re.MULTILINE)  # markdown headers
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    raw = (SRC / "narration.spoken.txt").read_text(encoding="utf-8")
    spoken = _clean_spoken(raw)
    (OUT_DIR / "_alignment_spoken.txt").write_text(spoken, encoding="utf-8")

    words = forced_align_script(str(SRC / "narration.mp3"), spoken)
    (OUT_DIR / "_alignment.json").write_text(
        json.dumps(words, indent=1), encoding="utf-8")
    print(f"wrote {len(words)} words -> _alignment.json")
    if words:
        print(f"first word: {words[0]}")
        print(f"last word:  {words[-1]}")


if __name__ == "__main__":
    main()
