"""Look and Live -- step 4: hand-written ink captions over the finished cut,
reusing the shared _short_captions.py burner (same recipe as Two Goats/
Jericho/Storm).

NO card skip windows needed here, unlike Two Goats' own Isaiah-card skip --
checked the actual screen positions before copying that pattern: Two Goats'
card sat at cy=0.735 (near the caption baseline, CAPTION_Y_FRAC=0.78 -- a
real conflict). This episode's title/quote/citation cards
(_s3b_titlecards.py's CARD_DEFS) all sit in the TOP third of the frame
(cy 0.09-0.38), nowhere near the caption zone -- so skipping captions under
them was an unnecessary copy of a pattern that doesn't apply here, and it
silenced the opening 7.7s of captions for no reason (caught by the user).

The narration timeline here is the ORIGINAL, uncompacted narration.mp3 (no
segment-splicing/remapping like the bronze_serpent/forsaken_cry examples),
so _alignment.json's real word timestamps apply directly, no offsetting.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s4_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = HERE / "_alignment.json"
SRC = HERE / "LOOKANDLIVE_living_sketchbook.mp4"
OUT = HERE / "LOOKANDLIVE_living_sketchbook_cc.mp4"

CARD_SKIPS = []


def main():
    words = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    burn(SRC, OUT, words, CARD_SKIPS, HERE / "_caption_frames")


if __name__ == "__main__":
    main()
