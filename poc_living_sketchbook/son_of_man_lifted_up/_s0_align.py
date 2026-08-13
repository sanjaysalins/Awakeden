"""Even So Must the Son of Man Be Lifted Up (Bronze Serpent short #3, John
3:14-15) -- step 0: force-align the existing LOCKED narration.mp3. Same
pattern as look_and_live/_s0_align.py and god_hung_up_a_snake/_s0_align.py.
$0 local forced-alignment MEASUREMENT pass over an already-locked, already-
voiced narration -- no API spend, no text changes.

Source narration folder title is "Lifted Up in Shame, Lifted Up in Glory"
(PythonProject1/jesus/narration/47_...) -- same piece, different working
title than the manifest's own "Even So Must the Son of Man Be Lifted Up."

  .venv\\Scripts\\python.exe poc_living_sketchbook/son_of_man_lifted_up/_s0_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = (Path(__file__).resolve().parents[3] / "PythonProject1" / "jesus" /
       "narration" / "47_Lifted_Up_in_Shame,_Lifted_Up_in_Glory" / "v1")
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
