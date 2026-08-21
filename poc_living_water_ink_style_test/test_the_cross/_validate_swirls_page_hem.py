"""$0 validation #2: same approach as _validate_swirls_page.py, against Hem
F04 -- exercises the "stain" fence family and the no-bubble-clause-absent
path (F04 predates that fix), which Thomas F01v2 didn't cover.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_the_hem as orig
from swirls_page import Panel, PageSpec, assemble_still_prompt, assemble_animation_prompt

STILL = orig.F04_STILL_PROMPT
ANIM = orig.F04_ANIMATION_PROMPT

still_start_anchor = "shot: "
still_end_anchor = " Small handwritten"
i = STILL.index(still_start_anchor) + len(still_start_anchor)
j = STILL.index(still_end_anchor)
main_scene_still = STILL[i:j]

mat_start_anchor = "never a magic-particle glow, and "
mat_i = STILL.index(mat_start_anchor) + len(mat_start_anchor)
material_closer = STILL[mat_i:]

anim_body_start = "Large bottom panel: "
fence_anchor = "every stain and mark in the paper"
ai = ANIM.index(anim_body_start) + len(anim_body_start)
aj = ANIM.index(fence_anchor)
main_scene_animation = ANIM[ai:aj].strip()

panel_motion_start = "Animate isolated motion inside each panel: "
lb_anchor = "Large bottom panel:"
pm_i = ANIM.index(panel_motion_start) + len(panel_motion_start)
pm_j = ANIM.index(lb_anchor)
panel_motion_str = ANIM[pm_i:pm_j].strip()
if panel_motion_str.endswith("."):
    panel_motion_str = panel_motion_str[:-1]
p1, p2, p3 = [p.split(" ", 2)[2] for p in panel_motion_str.split("; ")]

spec = PageSpec(
    seq_title="THE HEM",
    frame_label="F04",
    panels=(
        Panel("spent all", "a small sketch of an empty open coin purse lying flat with two small worn coins beside it"),
        Panel("the reach", "a close study of the woman's reaching hand alone, fingers extended, drawn in fine tentative cross-hatching"),
        Panel("the throng", "a small sketch of the pressing crowd from behind, tight shoulders and backs and head coverings packed close, no faces"),
    ),
    still_shot_type="MEDIUM WIDE shot",
    anim_shot_desc="medium wide shot",
    main_scene_still=main_scene_still,
    material_closer=material_closer,
    panel_motions=(p1, p2, p3),
    main_scene_animation=main_scene_animation,
    fence_kind="stain",
    fence_callout="the grey stain beneath the woman",
    caption_lines=("If I may touch", "but his clothes"),
    corner_note="NOTE: stain in paper",
    model_tier="kling3_0",
    include_no_bubble_clause=False,
)

generated_still = assemble_still_prompt(spec)
generated_anim = assemble_animation_prompt(spec)

# panel-1 content in the source is "a small sketch of an empty open coin purse..." but the
# generated version's panel_prose adds "a small sketch of" only via the authored content string,
# so this spec's panel 1 content intentionally omits the leading "a small sketch of" that panel 1
# lacks in the ORIGINAL text too (checked directly below in the diff) -- if this shows a mismatch
# it's informative either way.

print("=== STILL PROMPT DIFF (Hem F04) ===")
if generated_still == STILL:
    print("BYTE-IDENTICAL, PASS")
else:
    print("MISMATCH")
    for k in range(min(len(generated_still), len(STILL))):
        if generated_still[k] != STILL[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{generated_still[max(0,k-60):k+60]!r}...")
            print(f"    original:  ...{STILL[max(0,k-60):k+60]!r}...")
            break
    else:
        print(f"  (one is a prefix of the other) generated len={len(generated_still)} original len={len(STILL)}")

print("\n=== ANIMATION PROMPT DIFF (Hem F04) ===")
if generated_anim == ANIM:
    print("BYTE-IDENTICAL, PASS")
else:
    print("MISMATCH")
    for k in range(min(len(generated_anim), len(ANIM))):
        if generated_anim[k] != ANIM[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{generated_anim[max(0,k-60):k+60]!r}...")
            print(f"    original:  ...{ANIM[max(0,k-60):k+60]!r}...")
            break
    else:
        print(f"  (one is a prefix of the other) generated len={len(generated_anim)} original len={len(ANIM)}")
