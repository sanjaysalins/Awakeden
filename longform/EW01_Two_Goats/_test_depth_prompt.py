"""A/B test (2026-07-22): does the ArkAIology SHOT-formula discipline (explicit
depth layers + shallow DoF + foreground crossing the lens + one committed angle)
elevate OUR inked stills? Same seedream pipeline + the SAME ink style block/tail
as the real render — the ONLY change is a depth-disciplined subject_block.
Renders 2 test stills into visual_16x9_inked/_depth_test/ for side-by-side vs the
originals. ~$0.60 (2 stills). Records to the ledger.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_test_depth_prompt.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render, cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked" / "_depth_test"
OUT.mkdir(parents=True, exist_ok=True)

# reworked subject_blocks — ORIGINAL content, + their depth/DoF/foreground discipline
TESTS = {
    1: (
        "Deep three-layer cinematic composition. Extreme foreground, close to the lens and "
        "slightly out of focus: the dark silhouetted backs, heads and shoulders of a vast hushed "
        "multitude of Israelites, kept in shadow, framing the lower edge of the frame. Sharp "
        "mid-ground: the high priest Aaron, small in golden vestments, stands alone on the pale "
        "stone before the court. Deep background: the towering curtained Tabernacle court rises "
        "severe and dominant into an immense pale dawn sky. Strong shallow depth of field with the "
        "foreground crowd soft and Aaron in crisp focus, a low three-quarter angle looking up past "
        "the crowd toward the lone priest, dramatic scale contrast between the tiny priest and the "
        "colossal sacred tent"
    ),
    7: (
        "Extreme macro foreground, huge and close to the lens and in sharp focus: Aaron's two "
        "weathered hands in plain white linen sleeves hold up two small marked lot-stones directly "
        "toward the camera, filling the lower frame; the markings on the stones are only illegible "
        "scratches, not readable text. Mid-ground, soft with shallow depth of field: Aaron's aged "
        "bearded face and a bronze vessel, gently out of focus behind the stones. Deep background, "
        "softest: two goats standing close together before the bronze altar, the tabernacle court "
        "in shadow. Strong shallow depth of field racking all attention onto the lots, a low angle, "
        "Aaron alone, no other priests"
    ),
}


def main():
    visual_render.HFProvider.ASPECT = "16:9"
    prov = visual_render.HFProvider()
    print(f"[provider] hf {config.still_model()} @ 16:9 (VISUAL_STYLE={config.VISUAL_STYLE})")
    for sid, subj in TESTS.items():
        scene = Scene(
            index=sid, slug=f"depth_{sid:02d}", title=f"depth-test #{sid}",
            scene_type="single", arc_position="", framing="cinematic",
            purpose="", rationale="", visible_elements=subj[:200], emotional_tone="",
            subject_block=subj, mood_block="reverent, sacred, solemn", jesus_variant=None,
        )
        print(f"[img ] depth-test #{sid} ...", flush=True)
        t = time.time()
        png_bytes = prov.generate(scene)
        out = OUT / f"depth_{sid:02d}.png"
        out.write_bytes(png_bytes)
        cost.record_hf("EW01_Two_Goats", "long", "stills", config.still_model(),
                       note=f"[depth-test] #{sid}")
        print(f"       ok ({len(png_bytes):,} b, {time.time()-t:.0f}s) -> {out.name}")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
