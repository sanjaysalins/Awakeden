"""Timestamped .srt captions for any swirls-of-life episode, via ElevenLabs
forced-alignment (pipeline/assembly_align.py) -- a plain upload-alongside
subtitle file, NOT burned into the video (per feedback_swirls_no_burned_captions:
this series drops the /caption burn-in stage entirely).

Shared across episodes (unlike generate_score.py, which is intentionally
per-episode for its own authored prompt) -- this is pure mechanism, no
per-episode creative content, so one copy takes a folder argument instead.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\build_srt.py "<episode folder>"
"""
import os
os.environ["ASSEMBLY_ALIGN_BACKEND"] = "elevenlabs"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline.assembly_align import align  # noqa: E402

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


def build(folder: Path) -> Path:
    folder = Path(folder)
    out = folder / f"{folder.name}.srt"
    words = align(folder, force=True)
    print(f"[align] {folder.name}: {len(words)} words")
    cards = group_words(words)
    lines = []
    for i, card in enumerate(cards, start=1):
        start, end = card[0].start, card[-1].end
        text = " ".join(w.text for w in card)
        lines.append(str(i))
        lines.append(f"{srt_ts(start)} --> {srt_ts(end)}")
        lines.append(text)
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ok] {out}  ({len(cards)} cards)")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: build_srt.py <episode folder>")
    build(Path(sys.argv[1]))
