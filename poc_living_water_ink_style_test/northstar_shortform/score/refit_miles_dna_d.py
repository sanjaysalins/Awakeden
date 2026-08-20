"""Refit the Look-and-Live Robert-Miles/'Children'-direction score (dna_d,
the round-3 refinement) from its own raw generation to THIS piece's length
(narration + 3.0s landing hold). User's explicit call, 2026-08-19: swap out
the fresh water-theme score for this direction instead.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test/northstar_shortform/score/refit_miles_dna_d.py
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC_RAW = (HERE.parents[2] / "poc_living_sketchbook" / "look_and_live"
           / "_score_swap_poc" / "dna_d_raw.mp3")
NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\SwirlsOfLife_JohnFour_POC\v1\narration.mp3"
)
OUT = HERE / "score_miles_dna_d.mp3"
OUTRO_HOLD = 3.0


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def _mean_db(path: Path, ss: float, d: float) -> float | None:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-ss", str(ss), "-t", str(d), "-i", str(path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", out)
    return float(m.group(1)) if m else None


def main() -> None:
    if not SRC_RAW.exists():
        raise SystemExit(f"missing: {SRC_RAW}")
    total = dur(NARRATION_MP3) + OUTRO_HOLD
    draw = dur(SRC_RAW)
    aud_end, t = draw, max(4.0, draw - 2.0)
    while t > draw * 0.55:
        m = _mean_db(SRC_RAW, t, 2.0)
        if m is not None and m > -30.0:
            aud_end = min(draw, t + 2.0)
            break
        t -= 2.0
    aud_end = max(aud_end, draw * 0.6)
    tempo = max(0.5, min(1.0, aud_end / total))
    af = (f"atrim=0:{aud_end:.2f},asetpts=PTS-STARTPTS,atempo={tempo:.4f},"
          f"afade=t=in:st=0:d=1.5,afade=t=out:st={total-2.5:.2f}:d=2.5")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(SRC_RAW), "-af", af,
         "-t", f"{total:.2f}", str(OUT)], check=True)
    print(f"[fit] {SRC_RAW.name} ({draw:.1f}s) audible 0-{aud_end:.1f}s -> "
          f"stretched to fill {total:.2f}s (atempo {tempo:.4f}) -> {OUT}")


if __name__ == "__main__":
    main()
