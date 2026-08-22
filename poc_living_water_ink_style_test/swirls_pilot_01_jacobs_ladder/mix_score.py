"""Mix the approved 'modern groove' score under the narration on the already-
assembled pilot cut.

FIRST ATTEMPT (2026-08-22) reused `pipeline/score_mix.py`'s shared mix_tail()
verbatim (its SIDECHAIN constant: threshold=0.12:ratio=2.5) — the user
reported "I did not hear the score". Measured cause: at every timestamp
where narration is actively speaking, the scored mix's volumedetect reading
was within 1-3dB of the narration-ALONE reading — the duck was crushing the
groove to near-inaudibility for the ~95% of runtime narration is speaking,
audible only in the rare <1s pauses. That threshold/ratio is tuned for this
repo's usual ambient orchestral pads (fine ducked to near-zero); a rhythmic
groove is the wrong content for that same duck — the whole point of a groove
is a felt, continuous pulse, so this file uses its OWN looser sidechain
(higher threshold, gentler ratio) and less initial attenuation instead of
the shared mix_tail(), verified by the same before/after volumedetect check
this time BEFORE calling it done.

Requires assemble_pilot.py to have already produced `_assembly/silent_concat.mp4`.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\mix_score.py [score.mp3] [out.mp4]
  (defaults: score_groove.mp3 -> THE_LADDER_pilot_cut_scored.mp4)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, output_args  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
SCORE = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "score_groove.mp3"
SILENT_VIDEO = HERE / "_assembly" / "silent_concat.mp4"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "THE_LADDER_pilot_cut_scored.mp4"
OUTRO_HOLD = 3.0

# Looser than pipeline/score_mix.py's shared SIDECHAIN (threshold=0.12:ratio=2.5)
# — deliberately, per this file's own docstring: a groove must stay felt
# under speech, not duck to near-zero the way an ambient pad safely can.
# SECOND PASS (2026-08-22): the first attempt above (-4dB/0.35/1.6/300ms) was
# audible but the user reported it too loud AND "I hear two scores together"
# — most likely the duck pumping audibly in time with the groove's own kick/
# bass hits, phasing against it enough to read as a second, competing layer.
# Softer overall level + a higher threshold + gentler ratio + slower release
# reduces both: quieter overall, and the duck only engages on real narration
# peaks instead of pumping on every beat.
MUSIC_GAIN_DB = -8
DUCK_THRESHOLD = 0.45
DUCK_RATIO = 1.3
DUCK_RELEASE = 500


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def main() -> None:
    for p in (SILENT_VIDEO, NARRATION, SCORE):
        if not p.exists():
            sys.exit(f"missing: {p}")

    narration_len = dur(NARRATION)
    total = narration_len + OUTRO_HOLD

    with_narration = HERE / "_assembly" / "with_narration.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(SILENT_VIDEO), "-i", str(NARRATION),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(with_narration)], check=True)

    filt = (
        f"[1:a]{AFMT},volume={MUSIC_GAIN_DB}dB[mus];"
        f"[0:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[mus][key]sidechaincompress=threshold={DUCK_THRESHOLD}:ratio={DUCK_RATIO}:"
        f"attack=20:release={DUCK_RELEASE}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO_HOLD}[vout]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(with_narration), "-i", str(SCORE),
         "-filter_complex", filt] + output_args(OUT, preset="medium", total=total),
        check=True)
    print(f"[done] {OUT}  ({dur(OUT):.2f}s)")


if __name__ == "__main__":
    main()
