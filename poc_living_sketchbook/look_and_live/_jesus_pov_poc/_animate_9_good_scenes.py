"""Animate the 9 scenes that passed the stills content-audit cleanly (all
except 6, 10, 11, 13, which are still being iterated on). Uses the CORRECT
provider path for this project's shorts standard -- HF Kling pro / hybrid,
via pipeline.video_render.animate_scenes() -- NOT the direct-Kling-only
visual_handoff.run_kling_pipeline path, whose account is out of balance.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_animate_9_good_scenes.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pipeline import video_render  # noqa: E402

V1_FOLDER = Path(
    r"F:\slk\PycharmProjects\PythonProject1\jesus\narration\POC_Jesus_POV_LookAndLive\v1"
)
GOOD_INDICES = [1, 2, 3, 4, 5, 7, 8, 9, 12]


def main() -> None:
    made = video_render.animate_scenes(
        V1_FOLDER, "hf", indices=GOOD_INDICES, provider_name="hybrid", log=print,
    )
    print(f"[animate] {made} new clip(s) made this run.")


if __name__ == "__main__":
    main()
