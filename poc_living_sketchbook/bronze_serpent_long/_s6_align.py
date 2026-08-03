"""Bronze Serpent LONG -- step 6: force-align the LOCKED long-form narration
(the real "Types & Shadows" deep-dive this whole pilot is built against, NOT
the short's own narration). Same $0 local pattern as
`poc_living_sketchbook/bronze_serpent/_s0_align.py` -- a MEASUREMENT pass
over already-locked, already-voiced audio, no API spend, no text changes.

This gives assembly real word-level onsets/offsets to snap the _PLAN.md
table's estimated sub-turn spread boundaries to (the turn-level boundaries
in the plan are already ffprobe-hard per _PLAN.md sec 1c; only the
INTERIOR/sub-turn seams inside a turn are estimates that need this).

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent_long/_s6_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = ROOT / "longform" / "EW04_Bronze_Serpent" / "v1"
OUT_DIR = Path(__file__).resolve().parent


def _clean_spoken(raw: str) -> str:
    text = re.sub(r"\[[^\]]*\]", " ", raw)          # [Jesus] / [Witness] tags
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
