"""Piece 1 v3 SFX pass: night bed + the door easing open at the page4->5 turn.
Same restraint as v2 (the nail strike is already in the assembly mix, timed to
the THUD! lettering). All cue times shifted +2.0s for the cover.

  .venv\\Scripts\\python.exe poc_comic_page/_sfx_piece1_v3.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline import sfx_bed

HERE = ROOT / "poc_comic_page" / "_piece1"
SCORED = HERE / "IN_NO_WISE_GOLDSEAM_v3_ALIVE.mp4"
OUT = HERE / "IN_NO_WISE_GOLDSEAM_v3_ALIVE_sfx.mp4"

COVER = 1.3
CUES = [
    ("wind_desert_bleak", 0.0, 10_000.0, -22),
    ("door_gate_creak", 43.4 + COVER, 45.4 + COVER, -11),
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
