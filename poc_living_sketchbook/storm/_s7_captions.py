"""Storm -- step 7: hand-written ink captions over the finished cut, applying
the same recipe used on Bronze Serpent (memory `sketchbook-shorts-finishing-gap`).
Post-process only -- overlays onto the already-watermarked
STORM_living_sketchbook_v6.mp4, does not touch _s4/_s6/watermark.

Skips the s08_verse Scribed Ink card window (23.75-27.10s per _s4_assemble.py's
own SHOTS/verse_card timing) so a caption never doubles the on-screen KJV text.

  .venv\\Scripts\\python.exe poc_living_sketchbook/storm/_s7_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = HERE / "_storm_alignment.json"
SRC = HERE / "STORM_living_sketchbook_v6.mp4"
OUT = HERE / "STORM_living_sketchbook_cc.mp4"

VERSE_CARD_SKIP = (23.75, 27.10)


def main():
    words = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    burn(SRC, OUT, words, [VERSE_CARD_SKIP], HERE / "_caption_frames")


if __name__ == "__main__":
    main()
