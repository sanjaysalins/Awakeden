"""Burn real on-screen ink captions into the SCORED trailer -- a real gap the
user caught by eye: the trailer's first ~30s of the merged deliverable had NO
burned-in captions at all (only the .srt sidecar built for YouTube upload),
while the rest of the film has them throughout. Reuses _finish_long.py's own
caption-rendering functions verbatim (chunk_words/render_chunk_png/
build_caption_segment) rather than reimplementing the ink-caption look.

Skips the title-card window (27.017-29.667s): the narrator says "The Seed of
the Woman" at the same moment the title card's own hand-lettered text reads
"The Seed of the Woman" -- an ink caption there would double-text the same
words, the same double-caption problem the film's own skip_spreads already
guards against for verse cards.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "poc_living_sketchbook"))
from _finish_long import chunk_words, build_caption_segment  # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = HERE / "SEED_OF_THE_WOMAN_TRAILER_scored.mp4"
OUT = HERE / "SEED_OF_THE_WOMAN_TRAILER_captioned.mp4"
WORDS_JSON = HERE.parent / "SEEDOFTHEWOMAN_LONG_WITH_TRAILER.words.json"

TITLE_CARD_SKIP = (27.017, 29.667)  # matches _t10_final_assembly.py's PLAN S12 start


def main():
    all_words = json.loads(WORDS_JSON.read_text(encoding="utf-8"))
    # trailer words are the ones before the film's own shifted block starts
    trailer_words = [w for w in all_words if w["end"] <= 29.7]
    print(f"[caption] {len(trailer_words)} trailer words")

    chunks = chunk_words(trailer_words, [TITLE_CARD_SKIP])
    print(f"[caption] {len(chunks)} caption chunks (title-card window skipped)")

    seg_dir = HERE / "_caption_segments"
    work_dir = HERE / "_caption_frames"
    seg_dir.mkdir(exist_ok=True)
    work_dir.mkdir(exist_ok=True)
    seg = build_caption_segment(SRC, seg_dir, work_dir, 0, 0.0, 29.667, chunks, rebuild=True)

    import shutil
    shutil.copy2(seg, OUT)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
