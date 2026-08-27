"""Mix the new epic-soft felt-piano score (score_epic.mp3) under the
narration on the ACTUAL shipped pilot cut. FIXED (2026-08-27): the first
version of this script used `_assembly/silent_concat.mp4`, an early "quick
look" render from assemble_pilot.py that has NO front/back covers at all
(different art style entirely -- storyboard-sketch pages, not the Durer-
woodcut covers). The real THE_LADDER_BOOK_final.mp4 was built by a later
script (assemble_book_v2.py) that folds the woodcut front/back covers into
the narrated timeline; that script's own intermediate files were gone/stale
by the time this redo happened. Instead of trying to reconstruct that whole
pipeline, this just takes THE_LADDER_BOOK_final.mp4's own video track
(already the correct, final visual sequence, already includes the 3.0s
landing hold) and remixes fresh narration+new score onto it -- no re-tpad,
no re-encode of video, just a clean audio swap at the exact same duration.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\mix_score_epic.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, SIDECHAIN, output_args  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
SCORE = HERE / "score_epic.mp3"
VIDEO_SRC = HERE / "THE_LADDER_BOOK_final.mp4"  # the real shipped visual (covers included)
OUT = HERE / "THE_LADDER_cut_scoreEpic.mp4"

MUSIC_GAIN_DB = -6


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main() -> None:
    for p in (VIDEO_SRC, NARRATION, SCORE):
        if not p.exists():
            sys.exit(f"missing: {p}")

    # VIDEO_SRC already includes the 3.0s landing hold baked in -- its own
    # total duration IS the target; do not add another tpad/hold on top.
    total = dur(VIDEO_SRC)

    filt = (
        f"[2:a]{AFMT},volume={MUSIC_GAIN_DB}dB[mus];"
        f"[1:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[mus][key]sidechaincompress={SIDECHAIN}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(VIDEO_SRC), "-i", str(NARRATION), "-i", str(SCORE),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[mix]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", "-t", f"{total:.3f}", str(OUT)],
        check=True)
    print(f"[done] {OUT}  ({dur(OUT):.2f}s, target {total:.2f}s)")


if __name__ == "__main__":
    main()
