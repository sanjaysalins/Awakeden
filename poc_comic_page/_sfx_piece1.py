"""Piece 1 SFX pass: a quiet ambient night bed under the whole piece + ONE
meaningful accent (the door easing open) at the page4->page5 turn, where the
narration crosses from "the only way to be cast out is to never come" into
"So come." Reuses the project's shared engine (pipeline/sfx_bed.py) -- no new
mixing code. Restraint by design: one true sound, not a hit per beat.

  .venv\\Scripts\\python.exe poc_comic_page/_sfx_piece1.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import sfx_bed

HERE = ROOT / "poc_comic_page" / "_piece1"
SCORED = HERE / "IN_NO_WISE_GOLDSEAM_v2_period.mp4"
OUT = HERE / "IN_NO_WISE_GOLDSEAM_v2_period_sfx.mp4"

# page starts (absolute, s): p1=0, p2=10.08, p3=21.04, p4=33.14, p5=43.78
# page4->5 turn lands at 43.78s -- the door eases open right as the record's
# fear gives way to the welcome.
TOTAL = 61.767  # updated after the landing-hold extend; corrected below at runtime

CUES = [
    ("wind_desert_bleak", 0.0, TOTAL, -22),      # quiet constant night ambience
    ("door_gate_creak", 43.4, 45.4, -11),        # the one true sound: the door, easing open
]


def probe_duration(p: Path) -> float:
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    total = probe_duration(SCORED)
    cues = [(slug, s, min(e, total), g) for slug, s, e, g in CUES]
    sfx_bed.build(SCORED, OUT, cues, total)
    print(f"[final] {OUT} -> {probe_duration(OUT):.3f}s")


if __name__ == "__main__":
    main()
