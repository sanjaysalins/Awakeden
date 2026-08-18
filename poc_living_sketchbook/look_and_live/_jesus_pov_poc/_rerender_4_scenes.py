"""Targeted re-render of scenes 6, 10, 11, 13 only, after the user fixed their
prompts in scene_plan.json (fixing leaked faces / invented wound / ring /
averted gaze). Reuses pipeline.visual_render.render_scene per-scene -- same
machinery as the full Phase B run, just scoped to 4 indices.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_rerender_4_scenes.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
from pipeline import visual_render, visual_handoff  # noqa: E402
from pipeline.visual_models import ScenePlan  # noqa: E402

V1_FOLDER = Path(
    r"F:\slk\PycharmProjects\PythonProject1\jesus\narration\POC_Jesus_POV_LookAndLive\v1"
)
PLAN_PATH = V1_FOLDER / "visual" / "scene_plan.json"
TARGET_INDICES = {6, 10, 11, 13}


def main() -> None:
    doc = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    plan = ScenePlan.from_json(doc["plan"])

    provider_obj = visual_render.get_provider("hf")
    render_dir = V1_FOLDER / "visual" / provider_obj.name

    targets = [s for s in plan.scenes if s.index in TARGET_INDICES]
    print(f"[rerender] {len(targets)} scene(s): {[s.index for s in targets]}")

    for scene in targets:
        png_path, audit = visual_render.render_scene(
            scene, provider_obj, render_dir,
            max_retries=config.MAX_NBP_RETRIES, log=print,
        )
        print(f"  -> scene {scene.index}: passed={audit.passed}")

    visual_handoff.write_review_index_html(V1_FOLDER, provider_obj.name, plan=plan)
    print("[rerender] done.")


if __name__ == "__main__":
    main()
