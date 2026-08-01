"""Bronze Serpent episode — step 0: force-align the existing LOCKED narration.mp3.

Same pattern as poc_living_sketchbook/storm/_s0_align.py. This is a $0 local
forced-alignment MEASUREMENT pass over an already-locked, already-voiced
narration — no API spend, no text changes. It replaces the character-count
ESTIMATED sub-turn windows in `_FABLE_ROUND9_BRONZESERPENT_E2E_PLAN.md`
section A1 with real word-level onsets/offsets (see that plan's A0 section).

Spoken text is read straight from the episode's own narration.spoken.txt (the
clean spoken-text source, no [Jesus]/beat-header tags — per the
feedback-caption-clean-spoken-script discipline) rather than hardcoded, since
that file already exists for this episode as a single clean paragraph.

  .venv\\Scripts\\python.exe poc_living_sketchbook/bronze_serpent/_s0_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = ROOT / "longform" / "EW04_Bronze_Serpent" / "v1" / "short"
OUT_DIR = Path(__file__).resolve().parent


def _clean_spoken(raw: str) -> str:
    """Strip any stray [Speaker] tags / beat headers, collapse whitespace.

    narration.spoken.txt for this episode is already a single clean paragraph
    with no tags, but guard anyway rather than assume the format.
    """
    text = re.sub(r"\[[^\]]*\]", " ", raw)          # [Jesus] / [Witness] tags
    text = re.sub(r"^#.*$", " ", text, flags=re.MULTILINE)  # markdown headers
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    raw = (SRC / "narration.spoken.txt").read_text(encoding="utf-8")
    spoken = _clean_spoken(raw)
    (OUT_DIR / "_bronzeserpent_spoken.txt").write_text(spoken, encoding="utf-8")

    words = forced_align_script(str(SRC / "narration.mp3"), spoken)
    (OUT_DIR / "_bronzeserpent_alignment.json").write_text(
        json.dumps(words, indent=1), encoding="utf-8")
    print(f"wrote {len(words)} words -> _bronzeserpent_alignment.json")
    if words:
        print(f"first word: {words[0]}")
        print(f"last word:  {words[-1]}")


if __name__ == "__main__":
    main()
