"""$0 validation: re-express episode 1's real, non-defective front/back cover
prompts (render_covers.py / animate_covers.py) as CoverSpecs through
swirls_cover.py, and diff the generated text against the literal hardcoded
prompt strings -- byte for byte, MODULO two disclosed additions (the new
edge-to-edge clause, and an empty refs-manifest clause since the validation
specs carry no refs -- see NORTH_STAR_COVER_PROMPT.md). Content is SLICED
from the original constants (not retyped), same discipline as
test_the_cross/_validate_swirls_page.py. Episode 2's covers are the
DEFECTIVE example this module exists to prevent recurring -- not used here.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\_validate_swirls_cover.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WOODCUT_DIR = HERE / "swirls_pilot_01_jacobs_ladder" / "_style_test_durer_woodcut"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WOODCUT_DIR))

from swirls_cover import CoverSpec, EDGE_TO_EDGE_CLAUSE, assemble_cover_still_prompt, \
    assemble_cover_animation_prompt  # noqa: E402
import render_covers as covers_src  # noqa: E402
import animate_covers as anim_src  # noqa: E402


def slice_between(text: str, start_anchor: str, end_anchor: str, *, start_after=True) -> str:
    i = text.index(start_anchor)
    if start_after:
        i += len(start_anchor)
    j = text.index(end_anchor, i)
    return text[i:j]


def report(name: str, generated: str, original: str) -> bool:
    print(f"=== {name} ===")
    if generated == original:
        print("BYTE-IDENTICAL, PASS")
        return True
    print("MISMATCH")
    print(f"  generated len={len(generated)}  original len={len(original)}")
    for k in range(min(len(generated), len(original))):
        if generated[k] != original[k]:
            print(f"  first diff at char {k}:")
            print(f"    generated: ...{generated[max(0, k - 40):k + 40]!r}...")
            print(f"    original:  ...{original[max(0, k - 40):k + 40]!r}...")
            break
    else:
        print("  one string is a prefix of the other (lengths differ, no char mismatch)")
    return False


# ============================================================ FRONT STILL ===
FRONT = covers_src.FRONT_PROMPT
# scene = everything up to and including "...in an open sweeping sky."
front_scene = FRONT[:FRONT.index(" Low dusk sun")].rstrip()
front_lighting = FRONT[FRONT.index("Low dusk sun"):FRONT.index(" Far behind him")]
front_bg = FRONT[FRONT.index("Far behind him"):FRONT.index(" 16th-century")]

front_spec = CoverSpec(
    side="front",
    scene=front_scene,
    lighting=front_lighting,
    background_detail=front_bg,
    title="THE LADDER HE SAW",
    subtitle="GENESIS 28",
    title_position="top",
    animation="",  # not needed for the still-prompt check
)

# Original has NO edge-to-edge clause and NO refs clause (refs.=[] here matches that).
# Insert the disclosed edge-to-edge addition into the expected string at the same point
# the module inserts it (right after the title clause, before "No other text").
split_anchor = "No other text, letters, numbers, or words appear anywhere on the image"
a, b = FRONT[:FRONT.index(split_anchor)], FRONT[FRONT.index(split_anchor):]
front_expected = a + EDGE_TO_EDGE_CLAUSE + " " + b

ok1 = report("FRONT STILL PROMPT (+ disclosed edge-to-edge clause)",
             assemble_cover_still_prompt(front_spec), front_expected)

# ============================================================= BACK STILL ===
BACK = covers_src.BACK_PROMPT
back_scene = BACK[:BACK.index(" Low golden-hour sun")].rstrip()
back_lighting = BACK[BACK.index("Low golden-hour sun"):BACK.index(" 16th-century")]

back_spec = CoverSpec(
    side="back",
    scene=back_scene,
    lighting=back_lighting,
    background_detail="",   # back cover has no equivalent sentence in the source
    title="HE IS THAT LADDER",
    subtitle="JOHN 1:51",
    title_position="bottom",
    animation="",
)

a, b = BACK[:BACK.index(split_anchor)], BACK[BACK.index(split_anchor):]
back_expected = a + EDGE_TO_EDGE_CLAUSE + " " + b

ok2 = report("BACK STILL PROMPT (+ disclosed edge-to-edge clause)",
             assemble_cover_still_prompt(back_spec), back_expected)

# ======================================================== FRONT ANIMATION ===
FRONT_ANIM = anim_src.FRONT_ANIM
front_anim_body = slice_between(
    FRONT_ANIM, "never drifting position. ",
    "; no new figure, mark, or text appears anywhere on the frame at any point.")
front_spec_anim = CoverSpec(
    side="front", scene="", lighting="", title="", subtitle="", title_position="top",
    animation=front_anim_body,
)
ok3 = report("FRONT ANIMATION PROMPT", assemble_cover_animation_prompt(front_spec_anim), FRONT_ANIM)

# ========================================================= BACK ANIMATION ===
BACK_ANIM = anim_src.BACK_ANIM
back_anim_body = slice_between(
    BACK_ANIM, "stays perfectly static and unchanged for the whole clip. ",
    "; no new figure, mark, or text appears anywhere on the frame at any point.")
back_spec_anim = CoverSpec(
    side="back", scene="", lighting="", title="", subtitle="", title_position="bottom",
    animation=back_anim_body,
)
ok4 = report("BACK ANIMATION PROMPT", assemble_cover_animation_prompt(back_spec_anim), BACK_ANIM)

print()
print("ALL PASS" if all([ok1, ok2, ok3, ok4]) else "SOME FAILED -- see above")
