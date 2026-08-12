"""Look and Live (Bronze Serpent short #1, Numbers 21:8-9) — step 0:
force-align the existing LOCKED narration.mp3.

Same pattern as poc_living_sketchbook/bronze_serpent/_s0_align.py. $0 local
forced-alignment MEASUREMENT pass over an already-locked, already-voiced
narration — no API spend, no text changes.

Source narration is already clean spoken text (no [tags], single narrator
voice throughout, per narration-tagged.md) — used verbatim from narration.md.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s0_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = (Path(__file__).resolve().parents[3] / "PythonProject1" / "jesus" /
       "narration" / "41_The_Cure_Looked_Like_the_Curse" / "v1")
OUT_DIR = Path(__file__).resolve().parent


def _clean_spoken(raw: str) -> str:
    text = re.sub(r"\[[^\]]*\]", " ", raw)
    text = re.sub(r"^#.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    raw = (SRC / "narration.md").read_text(encoding="utf-8")
    spoken = _clean_spoken(raw)
    (OUT_DIR / "_spoken.txt").write_text(spoken, encoding="utf-8")

    words = forced_align_script(str(SRC / "narration.mp3"), spoken)
    (OUT_DIR / "_alignment.json").write_text(
        json.dumps(words, indent=1), encoding="utf-8")
    print(f"wrote {len(words)} words -> _alignment.json")
    if words:
        print(f"first word: {words[0]}")
        print(f"last word:  {words[-1]}")


if __name__ == "__main__":
    main()
