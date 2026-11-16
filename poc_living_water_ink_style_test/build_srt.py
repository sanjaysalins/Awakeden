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


def _marked(folder: Path) -> bool:
    """True if `folder` (or a parent) holds a `.swirls_short` marker (a guarded Swirls short)."""
    p = Path(folder).resolve()
    return any((q / ".swirls_short").is_file() for q in [p, *p.parents])


def build(folder: Path) -> Path:
    """LEGACY: re-aligns with ElevenLabs (force=True) -- a PAID, unlogged call that also overwrites
    the timing alignment. REFUSED for a marked Swirls short folder (use build_from_cache)."""
    folder = Path(folder)
    if _marked(folder):
        raise RuntimeError("build_srt.build() would call ElevenLabs alignment (paid, unlogged) and is "
                           "refused for a .swirls_short folder: use build_from_cache()")
    words = align(folder, force=True)
    print(f"[align] {folder.name}: {len(words)} words")
    return _write_srt(folder, words)


def build_from_cache(folder: Path) -> Path:
    """$0: the .srt from the CACHED narration.alignment.json only. Never calls `align`; raises if
    there is no cache."""
    import json
    from pipeline.assembly_align import _parse_words
    folder = Path(folder)
    cache = folder / "narration.alignment.json"
    if not cache.exists():
        raise FileNotFoundError(f"no cached alignment at {cache}: nothing to build the .srt from "
                                "(this function never aligns)")
    words = _parse_words(json.loads(cache.read_text(encoding="utf-8")))
    if not words:
        raise ValueError("cached alignment has no usable words")
    return _write_srt(folder, words)


def _write_srt(folder: Path, words) -> Path:
    out = folder / f"{folder.name}.srt"
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
