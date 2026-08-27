"""Re-layer the already-designed SFX bed (see build_sfx.py's own LAYERS --
unit timeline is unchanged, only the score under it changed) onto the new
epic-soft-scored cut, for ear-review candidate purposes. Does not touch the
shipped THE_LADDER_BOOK_final_sfx.mp4.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\build_sfx_epic.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "sfx_pilots"))
sys.path.insert(0, str(HERE))
import sfxlib  # noqa: E402
from build_sfx import LAYERS  # noqa: E402

CUT = HERE / "THE_LADDER_cut_scoreEpic.mp4"
OUT = HERE / "THE_LADDER_cut_scoreEpic_sfx.mp4"

if __name__ == "__main__":
    sfxlib.show_plan("The Ladder (pilot) -- epic score candidate", LAYERS)
    sfxlib.build(CUT, OUT, LAYERS)
    print(f"[ok] {OUT}")
