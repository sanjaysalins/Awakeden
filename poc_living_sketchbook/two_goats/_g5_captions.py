"""Two Goats -- step 5: hand-written ink captions over the finished cut,
applying the same recipe used on Bronze Serpent (memory
`sketchbook-shorts-finishing-gap`). Post-process only -- overlays onto the
already-watermarked TWO_GOATS_living_sketchbook.mp4, does not touch _g4/watermark.

Skips the Isaiah 53:6 illuminated rubric card window (43.9-47.55s per
_g4_assemble.py's own isaiah_card timing) so a caption never doubles the
on-screen KJV text.

  .venv\\Scripts\\python.exe poc_living_sketchbook/two_goats/_g5_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = HERE / "audio" / "alignment.json"
SRC = HERE / "TWO_GOATS_living_sketchbook.mp4"
OUT = HERE / "TWO_GOATS_living_sketchbook_cc.mp4"

ISAIAH_CARD_SKIP = (43.9, 47.55)


def main():
    words = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    burn(SRC, OUT, words, [ISAIAH_CARD_SKIP], HERE / "_caption_frames")


if __name__ == "__main__":
    main()
