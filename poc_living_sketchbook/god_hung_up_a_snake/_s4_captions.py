"""God Hung Up a Snake -- step 4: hand-written ink captions over the finished
cut, reusing the shared _short_captions.py burner (same recipe as Look and
Live/Two Goats/Jericho/Storm).

NO card skip windows needed here -- checked the actual screen positions
before copying Two Goats' skip pattern: this episode's title/quote/citation
cards (_s3b_titlecards.py's CARD_DEFS) all sit in the TOP portion of the
frame (cy 0.09-0.44), nowhere near the caption zone (CAPTION_Y_FRAC=0.78),
same as Look and Live's own confirmed-clear layout.

The narration timeline here is the ORIGINAL, uncompacted narration.mp3 (no
segment-splicing/remapping), so _alignment.json's real word timestamps apply
directly, no offsetting.

  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s4_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = HERE / "_alignment.json"
SRC = HERE / "GODHUNGUPASNAKE_living_sketchbook.mp4"
OUT = HERE / "GODHUNGUPASNAKE_living_sketchbook_cc.mp4"

CARD_SKIPS = []


def main():
    words = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    burn(SRC, OUT, words, CARD_SKIPS, HERE / "_caption_frames")


if __name__ == "__main__":
    main()
