"""Jericho -- step 6: hand-written ink captions over the finished cut, applying
the same recipe used on Bronze Serpent (memory `sketchbook-shorts-finishing-gap`).
Post-process only -- overlays onto the already-watermarked
JERICHO_living_sketchbook.mp4, does not touch _j5/watermark.

audio/timing.json nests word timing under each line (keys "s"/"e", absolute
seconds, confirmed by spot-check: l2's first word starts exactly at l2.start).
Flattened here into the flat w/start/end list the shared burner expects.

Skips every _j5_assemble.py REVEALS window (word-timed on-screen verse-reveal
text -- JOSHUA 2:18 / HEBREWS 11:31 / MATTHEW 1:5) so a caption never doubles
text already being typed on screen for those exact words.

  .venv\\Scripts\\python.exe poc_living_sketchbook/jericho/_j6_captions.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _short_captions import burn  # noqa: E402

TIMING_PATH = HERE / "audio" / "timing.json"
SRC = HERE / "JERICHO_living_sketchbook.mp4"
OUT = HERE / "JERICHO_living_sketchbook_cc.mp4"

# mirrors _j5_assemble.py's REVEALS: (line, i0, i1, ...)
REVEALS = [
    ("l4", 0, 8),
    ("l7", 4, 10),
    ("l8", 5, 9),
]


def main():
    timing = json.loads(TIMING_PATH.read_text(encoding="utf-8"))
    by_line = {ln["name"]: ln for ln in timing["lines"]}

    words = []
    for line in timing["lines"]:
        for w in line["words"]:
            words.append({"w": w["w"], "start": w["s"], "end": w["e"]})

    skips = []
    for line, i0, i1 in REVEALS:
        lwords = by_line[line]["words"]
        skips.append((lwords[i0]["s"], lwords[i1]["e"]))

    burn(SRC, OUT, words, skips, HERE / "_caption_frames")


if __name__ == "__main__":
    main()
