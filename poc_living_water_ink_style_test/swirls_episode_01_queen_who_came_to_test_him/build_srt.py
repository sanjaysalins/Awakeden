"""Timestamped .srt captions for episode 1, via ElevenLabs forced-alignment
(the project's own pipeline/assembly_align.py) -- a plain upload-alongside
subtitle file, NOT burned into the video (per the series' own "no burned
captions" rule, feedback_swirls_no_burned_captions).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_01_queen_who_came_to_test_him\\build_srt.py
"""
import os
os.environ["ASSEMBLY_ALIGN_BACKEND"] = "elevenlabs"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline.assembly_align import align  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "THE_QUEEN_WHO_CAME_TO_TEST_HIM.srt"

MAX_WORDS_PER_CARD = 7
MAX_CHARS_PER_CARD = 42


def srt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def group_words(words):
    cards = []
    cur = []
    for w in words:
        cur.append(w)
        text = " ".join(x.text for x in cur)
        ends_sentence = w.text.rstrip().endswith((".", "?", "!", ":", ";"))
        if len(cur) >= MAX_WORDS_PER_CARD or len(text) >= MAX_CHARS_PER_CARD or ends_sentence:
            cards.append(cur)
            cur = []
    if cur:
        cards.append(cur)
    return cards


def main():
    words = align(HERE, force=True)
    print(f"[align] {len(words)} words")
    cards = group_words(words)
    lines = []
    for i, card in enumerate(cards, start=1):
        start, end = card[0].start, card[-1].end
        text = " ".join(w.text for w in card)
        lines.append(str(i))
        lines.append(f"{srt_ts(start)} --> {srt_ts(end)}")
        lines.append(text)
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ok] {OUT}  ({len(cards)} cards)")


if __name__ == "__main__":
    main()
