"""Standalone remix of the v2 epic score onto the already-assembled Ashes
cut -- bypasses swirls_assemble.py's sa.assemble()/EpisodeManifest path on
purpose. A concurrent session was found mid-task (2026-08-27) editing shared
files including pipeline/score_mix.py, which had its `sidechain` kwarg
removed (uncommitted, not this repo's doing), breaking sa.assemble()'s call
into it. This script only uses score_mix.AFMT/mix_tail/output_args WITHOUT
passing a sidechain override, so it works against either version of that
file -- and the desired duck for this score (threshold=0.12:ratio=2.5:
attack=20:release=250, the "ambient pad" family) happens to be
score_mix.SIDECHAIN's own default anyway, so no override is even needed.

Reuses _assembly/with_narration.mp4 (already produced by the earlier
sa.assemble() call before it crashed on the music-mix step).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\mix_score_epic.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import score_mix  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
SCORE = HERE / "score_epic.mp3"
WITH_NARRATION = HERE / "_assembly" / "with_narration.mp4"
OUT = HERE / "THE_ASHES_BOOK_final_epic.mp4"
OUTRO_HOLD = 3.0
MUSIC_GAIN_DB = -6


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main() -> None:
    for p in (WITH_NARRATION, NARRATION, SCORE):
        if not p.exists():
            sys.exit(f"missing: {p}")

    total = dur(NARRATION) + OUTRO_HOLD

    music_chain = f"[1:a]{score_mix.AFMT},volume={MUSIC_GAIN_DB}dB[mus];"
    tail = score_mix.mix_tail(total, OUTRO_HOLD, fmt_narration=True)
    filt = music_chain + tail

    cmd = ["ffmpeg", "-y", "-v", "error",
           "-i", str(WITH_NARRATION), "-i", str(SCORE),
           "-filter_complex", filt]
    cmd += score_mix.output_args(OUT, preset="medium", total=total)
    subprocess.run(cmd, check=True)
    print(f"[done] {OUT}  ({dur(OUT):.2f}s)")


if __name__ == "__main__":
    main()
