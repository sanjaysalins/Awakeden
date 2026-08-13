"""Her Seed (Seed of the Woman short #2, Galatians 4:4)
-- step 0: force-align the existing LOCKED narration.mp3. Same pattern as
every other living-sketchbook short's own _s0_align.py. $0 local forced-
alignment MEASUREMENT pass over an already-locked, already-voiced
narration -- no API spend, no text changes.

Source narration folder title is "Not Plan B"
(PythonProject1/jesus/narration/45_Not_Plan_B/) -- same piece, different
working title than the manifest's own "Her Seed."

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s0_align.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script

SRC = (Path(__file__).resolve().parents[3] / "PythonProject1" / "jesus" /
       "narration" / "45_Not_Plan_B" / "v1")
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
