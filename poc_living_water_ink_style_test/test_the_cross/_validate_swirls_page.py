"""$0 validation: re-express Thomas F01 v2's already-validated prompts as a
PageSpec through swirls_page.py, and diff the generated text against the
literal hardcoded prompt strings in render_the_thomas_f01_v2.py -- byte for
byte. Content is SLICED from the original constants (not retyped) so this
test validates the boilerplate assembly logic only, not transcription
accuracy. See PRODUCTION_PIPELINE.md's migration path.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_the_thomas_f01_v2 as orig
from swirls_page import Panel, PageSpec, assemble_still_prompt, assemble_animation_prompt

STILL = orig.STILL_PROMPT
ANIM = orig.ANIMATION_PROMPT

# ---- slice main_scene_still out of the original STILL_PROMPT -----------------
still_start_anchor = "shot: "
still_end_anchor = " Small handwritten"
i = STILL.index(still_start_anchor) + len(still_start_anchor)
j = STILL.index(still_end_anchor)
main_scene_still = STILL[i:j]

# ---- slice material_closer ----------------------------------------------------
mat_start_anchor = "never a magic-particle glow, and "
mat_i = STILL.index(mat_start_anchor) + len(mat_start_anchor)
material_closer = STILL[mat_i:]

# ---- slice animation pieces ---------------------------------------------------
anim_body_start = "Large bottom panel: "
fence_anchor = "every ink line and mark on the page is long set"
ai = ANIM.index(anim_body_start) + len(anim_body_start)
aj = ANIM.index(fence_anchor)
main_scene_animation = ANIM[ai:aj].strip()
fence_text = ANIM[aj:]

panel_motion_start = "Animate isolated motion inside each panel: "
lb_anchor = "Large bottom panel:"
pm_i = ANIM.index(panel_motion_start) + len(panel_motion_start)
pm_j = ANIM.index(lb_anchor)
panel_motion_str = ANIM[pm_i:pm_j].strip()
if panel_motion_str.endswith("."):
    panel_motion_str = panel_motion_str[:-1]
p1, p2, p3 = [p.split(" ", 2)[2] for p in panel_motion_str.split("; ")]

spec = PageSpec(
    seq_title="THOMAS",
    frame_label="F01",
    panels=(
        Panel("not with them", "a small sketch of a shut wooden door with its heavy bar in place"),
        Panel("the proof", "a small plain study of a single iron nail lying on its side, drawn as a quiet dry object"),
        Panel("eight days", "a small sketch of a low-burned oil lamp beside a shuttered window, its oil nearly spent"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=main_scene_still,
    material_closer=material_closer,
    panel_motions=(p1, p2, p3),
    main_scene_animation=main_scene_animation,
    fence_kind="fray",
    fence_callout="the broken, tremored linework of Thomas's figure",
    caption_lines=("I will not believe",),
    corner_note="NOTE: line unsteady",
    model_tier="kling3_0",
)

generated_still = assemble_still_prompt(spec)
generated_anim = assemble_animation_prompt(spec)

print("=== STILL PROMPT DIFF ===")
if generated_still == STILL:
    print("BYTE-IDENTICAL, PASS")
else:
    print("MISMATCH")
    print(f"  generated len={len(generated_still)}  original len={len(STILL)}")
    for k in range(min(len(generated_still), len(STILL))):
        if generated_still[k] != STILL[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{generated_still[max(0,k-40):k+40]!r}...")
            print(f"    original:  ...{STILL[max(0,k-40):k+40]!r}...")
            break

print("\n=== ANIMATION PROMPT DIFF ===")
if generated_anim == ANIM:
    print("BYTE-IDENTICAL, PASS")
else:
    print("MISMATCH")
    print(f"  generated len={len(generated_anim)}  original len={len(ANIM)}")
    for k in range(min(len(generated_anim), len(ANIM))):
        if generated_anim[k] != ANIM[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{generated_anim[max(0,k-40):k+40]!r}...")
            print(f"    original:  ...{ANIM[max(0,k-40):k+40]!r}...")
            break
