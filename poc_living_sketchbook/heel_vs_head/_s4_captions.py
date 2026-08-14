"""Heel vs Head -- step 4: hand-written ink captions over the finished cut,
reusing the shared _short_captions.py burner (same recipe as every other
episode in this cluster).

NO card skip windows needed -- this episode's title/quote/citation cards
(_s3b_titlecards.py's CARD_DEFS) all sit at cy 0.09-0.37, nowhere near the
caption zone (CAPTION_Y_FRAC=0.78).

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s4_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

ALIGN_PATH = HERE / "_alignment.json"
SRC = HERE / "HEELVSHEAD_living_sketchbook.mp4"
OUT = HERE / "HEELVSHEAD_living_sketchbook_cc.mp4"

CARD_SKIPS = []


def main():
    words = json.loads(ALIGN_PATH.read_text(encoding="utf-8"))
    burn(SRC, OUT, words, CARD_SKIPS, HERE / "_caption_frames")


if __name__ == "__main__":
    main()
