"""Jesus-POV POC -- run Phase B (render stills) + Phase C (Kling animate)
directly against the hand-authored scene_plan.json, bypassing cli_visual.py's
create_visuals() entry point (which hard-requires narration.creation.json +
a real series id -- irrelevant to this bespoke one-off POC; Phase B/C
(visual_runner._run_phase_bc) needs none of that, only the plan itself).

Reuses the REAL render/animate machinery (pipeline.visual_render.render_scene,
pipeline.visual_handoff.run_kling_pipeline via image_to_kling.py) -- nothing
here is a reimplementation.

LLM calls (the Vision content audit per still, the Kling cut-plan director +
Stage A.5 audit per clip) route through the agent-bridge ($0, LLM_PROVIDER=agent
default) -- run this in the background and service .agent_bridge/requests/
(check BOTH F:\\slk\\PycharmProjects\\JesusInTheBible\\.agent_bridge\\ and the
stale C:\\Users\\sanjay\\PycharmProjects\\JesusInTheBible\\.agent_bridge\\ --
see memory feedback_agent_bridge_no_api.md) same as the audio stage.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_jesus_pov_poc/_run_visual_phase_bc.py

2026-08-17 update: forced VISUAL_STYLE=sketchbook (full-bleed sketchbook, config.py
STYLE_REGISTRY["sketchbook"]) -- the "baroque"-toned prose this script originally ran
was actually rendered under the graphic_novel default (VISUAL_STYLE was never set),
and 4 of 13 scenes failed content audit repeatedly regardless. See scene_plan.json's
self_review + config.py's VISUAL_STYLE_BASE_SKETCH comment for the full history.
"""
import json
import os
import sys
from pathlib import Path

os.environ["VISUAL_STYLE"] = "sketchbook"   # MUST be set before `import config`

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pipeline import visual_runner  # noqa: E402
from pipeline.visual_models import ScenePlan, ScenePlanReview, CohesionAudit  # noqa: E402

V1_FOLDER = Path(
    r"F:\slk\PycharmProjects\PythonProject1\jesus\narration\POC_Jesus_POV_LookAndLive\v1"
)
PLAN_PATH = V1_FOLDER / "visual" / "scene_plan.json"


def main() -> None:
    doc = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    plan = ScenePlan.from_json(doc["plan"])
    self_review = ScenePlanReview.from_json(doc["self_review"])
    paper = CohesionAudit.from_json(doc["paper_cohesion"])

    print(f"[run] {len(plan.scenes)} scenes, hero=#{plan.hero_candidate:02d}, "
          f"short_priority={plan.short_priority}")

    result = visual_runner._run_phase_bc(
        v1_folder=V1_FOLDER,
        folder=V1_FOLDER / "visual",
        plan=plan,
        self_review=self_review,
        independent_review=None,
        paper=paper,
        revisions=0,
        provider="hf",
        short_only=True,
        animate=True,
        plan_only=False,
        kling_skip_audit=True,   # per CLAUDE.md: skip Stage A.5's nit-picky audit on Baroque
        log=print,
    )

    passed = sum(1 for _, _, a in (result.rendered or []) if a.passed)
    print(f"\n[done] rendered {len(result.rendered or [])} scenes, "
          f"{passed} passed content audit, provider={result.provider_used}")
    print(f"[done] output folder: {result.folder}")


if __name__ == "__main__":
    main()
