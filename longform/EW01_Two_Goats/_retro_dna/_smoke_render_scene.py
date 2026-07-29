"""Smoke test: prove `render_scene()` (the REAL production function, not an
ad-hoc script) now actually chains a character ref through to the provider.
Closes the gap all 5 external reviewers found (2026-07-23): the ref-path
parameter existed on both providers but no real call site ever supplied it.

Temporarily monkeypatches config.STYLE_REGISTRY with a throwaway "retro" entry
using the DNA's actual proven prompt (from _hook_splash.py) — NOT written back
to config.py; the real retro STYLE_REGISTRY key is still a separate, deferred
BUILD item. This just lets the smoke test render in-style instead of the
default graphic_novel look, so the proof is representative.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_smoke_render_scene.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import os
os.environ["HF_MODEL_ID"] = "nano_banana_pro"  # the user's 2026-07-23 decision for character scenes

import config
from pipeline import visual_render
from pipeline.visual_models import Scene

RETRO_BASE = (
    "Vintage 1960s Silver Age comic book illustration style, bold black ink holding lines, flat "
    "limited four-colour comic colour with NO gradients, clearly visible coarse Ben-Day halftone "
    "dots in the sky and shadows, slight CMYK misregistration, warm cream colour palette,"
)
RETRO_TAIL = (
    "reverent, ancient Near-Eastern period-accurate, a full-bleed digital illustration filling the "
    "entire canvas edge-to-edge, no text, no lettering, no captions, no speech balloons, no "
    "watermark --ar 16:9"
)
config.STYLE_REGISTRY["retro"] = {
    "style_base": RETRO_BASE,
    "style_tail": RETRO_TAIL,
    "still_model": ("hf", "nano_banana_pro"),
    "anim_model": ("hf", "cinematic_studio_video_v2"),
    "audit_rubric": config.STYLE_AUDIT_RUBRIC["graphic_novel"],
    "audit_medium": "reverent retro-comic illustration",
}
config.VISUAL_STYLE = "retro"

REF = ROOT / "longform/EW01_Two_Goats/v1/visual_16x9_inked/_painted_comic_test/christ_pc_ref.png"
OUT = Path(__file__).resolve().parent / "_smoke_render_scene"
OUT.mkdir(exist_ok=True)


def main():
    assert REF.exists(), f"missing ref: {REF}"
    scene = Scene(
        index=1, slug="smoke_teaching_v2", title="Smoke test — Christ teaching (no-border fix)",
        scene_type="single", arc_position="revelation", framing="mid",
        purpose="prove ref-chaining through render_scene()", rationale="panel-gap fix",
        visible_elements="Jesus Christ, a hillside, a small gathered crowd",
        emotional_tone="warm, teaching",
        subject_block=(
            "The Lord Jesus Christ standing and teaching a small gathered crowd on a grassy "
            "hillside, a gentle open-handed gesture, warm afternoon daylight, ancient Near-Eastern"
        ),
        mood_block="warm, reverent, unhurried",
    )
    provider = visual_render.get_provider("hf")
    print(f"[smoke] rendering via render_scene() with extra_ref_paths=[{REF.name}] ...")
    png_path, audit = visual_render.render_scene(
        scene, provider, OUT, max_retries=0, extra_ref_paths=[REF],
    )
    print(f"[smoke] wrote {png_path} — audit passed={audit.passed}")


if __name__ == "__main__":
    main()
