"""Build a real word-level [{w,start,end}] timing file for the MERGED
trailer+film deliverable (SEEDOFTHEWOMAN_LONG_WITH_TRAILER.mp4), so
pipeline/publish_pack.py's build_srt() has real data instead of nothing.

The film's own portion already has real forced-aligned timing
(_alignment.json, 1346 words) -- just needs shifting by the trailer's
real duration. The trailer's own narration was never forced-aligned
(no whisperx pass was run when it was built), so this runs veed_io's
forced_align_script() against its known, exact script text (the same
text visible in _trailer/narration-tagged.md, tags stripped) rather
than guessing/interpolating timing.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from veed_io.aligner import forced_align_script  # noqa: E402

HERE = Path(__file__).resolve().parent
TRAILER_NARR = HERE.parent.parent.parent / "longform" / "05_The_Seed_Of_The_Woman" / "v1" / "_trailer" / "narration.mp3"
FILM_ALIGNMENT = HERE.parent / "_alignment.json"
TRAILER_DUR_OFFSET = 29.666667  # the real trailer video's duration (measured, matches PLAN sum)
OUT = HERE.parent / "SEEDOFTHEWOMAN_LONG_WITH_TRAILER.words.json"

TRAILER_SCRIPT = (
    "In the garden, everything just broke. "
    "Two people -- hiding from the God who made them. "
    "But before He sentenced the guilty. "
    "He made a promise. To the enemy. "
    # KJV-exact Gen 3:15b: a comma, not the tagged script's performance-pacing
    # "..." (that mark was for the TTS voice direction, never meant to reach
    # the caption/quote text -- caught by caption_slop_check.py's own new
    # ellipsis check finding it in the ALREADY-RENDERED captions.srt).
    "\"It shall bruise thy head, and thou shalt bruise his heel.\" "
    "Centuries before the cross. Before the empty tomb. "
    "The oldest promise in the Bible is about to be kept. "
    "The Seed of the Woman."
)


def main():
    if not TRAILER_NARR.exists():
        sys.exit(f"missing {TRAILER_NARR}")
    if not FILM_ALIGNMENT.exists():
        sys.exit(f"missing {FILM_ALIGNMENT}")

    print("[align] forced-aligning the trailer's own narration...")
    trailer_words = forced_align_script(str(TRAILER_NARR), TRAILER_SCRIPT)
    print(f"[align] trailer: {len(trailer_words)} words, "
          f"{trailer_words[0]['start']:.2f}-{trailer_words[-1]['end']:.2f}s")

    film_words = json.loads(FILM_ALIGNMENT.read_text(encoding="utf-8"))
    shifted = [{"w": w["w"], "start": w["start"] + TRAILER_DUR_OFFSET,
                "end": w["end"] + TRAILER_DUR_OFFSET} for w in film_words]
    print(f"[shift] film: {len(shifted)} words, shifted +{TRAILER_DUR_OFFSET:.3f}s -> "
          f"{shifted[0]['start']:.2f}-{shifted[-1]['end']:.2f}s")

    combined = list(trailer_words) + shifted
    OUT.write_text(json.dumps(combined, ensure_ascii=False, indent=None), encoding="utf-8")
    print(f"[ok] {len(combined)} words -> {OUT}")


if __name__ == "__main__":
    main()
