"""The Ashes That Made Clean (Numbers 19) — episode #2, Swirls of Life.

Second production episode, built to finalize the "north star" template
validated on Jacob's Ladder (poc_living_water_ink_style_test/
swirls_pilot_01_jacobs_ladder/): 4 interior ink-wash storyboard pages
(this file) + 2 full-woodcut cover stills (render_ashes_covers.py, once
refs exist), all animated, assembled with narration+score from second one.

Deliberately fewer interior pages than Jacob's Ladder (4, not 6) — this
story is more expository/typological than scene-by-scene narrative, and the
series plan's own pilot exit criteria anticipated variable page counts
("Northstar used 8, Hem validated 2 ... likely needs fewer").

TWO dead-ink motifs on this episode, per SWIRLS_OF_LIFE_SERIES_PLAN_V4.md:
  - STAIN (uncleanness) marks the unclean man/priest — a DRY, matte, ash-grey
    smudge, never wet/glowing like the swirl. Per the locked doctrine split
    (commit 1fc3118): this is ceremonial Levitical uncleanness-as-barrier,
    NEVER framed as guilt or shame — the man/priest read as ordinary, mildly
    inconvenienced, never hunched/ashamed. It washes CLEAR under the
    purification water (F04) — the opposite mechanic from swirl, which
    accumulates/bleeds rather than rinsing away.
  - SWIRL marks the ceremony's own divine provision, capped Stage 1-2 (OT
    rule, same cap as Jacob's Ladder). High-tide exclusion applies on any
    page where both appear: stainDose + swirlStage <= 4.

REF-CHAINING: F01 (the priest, alone with the heifer) and F02 (the unclean
man, alone) each establish their own character with NO ref (nothing else to
chain from yet). Human crops BOTH after approval -> refs/. F03 (needs the
unclean man) and F04 (needs both the man and the priest) chain forward.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes.py f01
  ... crop refs/unclean_man_ref.png + refs/unclean_man_face_ref.png from F02,
      refs/priest_ref.png from F01, refs/place_ref.png from either ...
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes.py f02
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes.py f03
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\render_ashes.py f04
  ... then --animate on each.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "test_the_cross"))
from swirls_page import (  # noqa: E402
    PageSpec, Panel, Ref, assemble_animation_prompt, assemble_still_prompt,
    render_animation, render_still,
)

REFS_DIR = HERE / "refs"


def _ref(name: str, subject: str) -> Ref:
    return Ref(subject, str(REFS_DIR / name))


# Locked builds — face/dress only, no motif, reused verbatim on every page.
# Deliberately plain and unremarkable ("whosoever" — the text's own framing;
# the anonymity is the point) — nothing distinguished, nothing shameful.
_MAN_BUILD = (
    "an ordinary man of middle years, plain sun-worn face, short dark hair, a plain "
    "undyed wool tunic belted at the waist, bare feet, drawn in fine, quick cross-hatching; "
    "his expression is matter-of-fact and mildly weary, never ashamed or hunched — he wears "
    "no blue and no gold anywhere"
)
_PRIEST_BUILD = (
    "an older man in a plain white linen priestly tunic and a simple wrapped linen headcloth, "
    "a grave and dutiful weathered face, grey-streaked beard, drawn in fine, quick "
    "cross-hatching; he wears no blue and no gold anywhere except where the swirl motif is "
    "explicitly dosed onto an object he holds, never onto his own person"
)

R_MAN = _ref("unclean_man_ref.png",
             "the unclean man, full figure — plain sun-worn face, short dark hair, undyed "
             "wool tunic, bare feet, matter-of-fact expression, never ashamed or hunched")
R_MAN_FACE = _ref("unclean_man_face_ref.png",
                   "the unclean man's face close up — plain sun-worn features, short dark "
                   "hair, matter-of-fact expression")
R_PRIEST = _ref("priest_ref.png",
                "the priest, full figure — white linen tunic, simple wrapped headcloth, "
                "grey-streaked beard, grave dutiful expression")
R_PLACE = _ref("place_ref.png",
               "the place — bare stony ground outside the camp, low scrub, pale overcast "
               "sky, no meadow, no lush greenery")

PAGES: dict[str, PageSpec] = {

    # ---------------------------------------------------------------- F01
    # The cost of the cure. Priest established. Stain D1 lands on HIM, not
    # the unclean man — the season's fresh, overlooked detail.
    "f01": PageSpec(
        seq_title="THE ASHES",
        frame_label="F01",
        panels=(
            Panel("the heifer",
                  "a small sketch of a red heifer without blemish, led by a rope, drawn as "
                  "a quiet still animal"),
            Panel("outside the camp",
                  "a small sketch of a scatter of tents far off on a bare rise, seen across "
                  "open ground"),
            Panel("the burning",
                  "a small sketch of a hand casting cedar wood, hyssop, and scarlet thread "
                  "into a small bright fire, drawn as a quiet plain action"),
        ),
        still_shot_type="MEDIUM WIDE shot",
        anim_shot_desc="medium wide shot",
        main_scene_still=(
            "bare, stony ground outside the camp under a flat, pale overcast sky, no meadow, "
            "no lush greenery; the priest kneels beside a modest fire, fully inside the frame, "
            "feeding cedar wood into the flame with one hand — the fire and its rising smoke "
            "are the only things burning anywhere in the frame; no animal, living or slain, "
            "appears anywhere in the main scene or anywhere else on the page, the burning "
            "already well underway and past the point of showing the heifer's own form; his "
            "sleeves are pushed back, both his hands and forearms marked with a faint, dry, "
            "matte grey-ash smudge — not a wound, not a wet stain, dry ash clinging to his "
            "skin like literal soot from tending the fire; his face is grave and dutiful, not "
            "distressed; low tents of the camp sit small and far off in the background; no "
            "other person appears anywhere on the page. "
            "The priest: " + _PRIEST_BUILD + ". Stage 0 dosage: no blue Swirls of Life ink "
            "motif anywhere on this page — no blue ink appears anywhere in the scene, the "
            "panels, or the margins."
        ),
        material_closer=(
            "the ash on the priest's hands behaves like real dry soot resting on skin, matte "
            "and grey, never a wet ink stain and never glowing."
        ),
        caption_lines=("that someone else becomes unclean too",),  # narration verbatim
        corner_note="NOTE: the cost of the cure",
        panel_motions=(
            "the sketched heifer's ear flicks once, then stills",
            "the sketched tent cloths ripple faintly once in a passing wind",
            "the sketched flame flickers gently, nothing else changes",
        ),
        main_scene_animation=(
            "the priest continues feeding the last of the cedar wood into the fire, one slow, "
            "deliberate motion, his hands steady, no animal appearing in the flame at any "
            "point; the dry grey ash on his "
            "hands and forearms stays exactly as drawn, in place, for the whole clip, never "
            "spreading, never changing shape; his robe stirs faintly in the wind; the "
            "distant tents stay exactly as drawn; no new stain, spot, or darkening appears "
            "anywhere on the page at any point."
        ),
        fence_kind="none",
        refs=[],  # ESTABLISHING page — priest_ref cropped FROM it
        model_tier="veo3_1_lite",  # atmospheric hold, nothing completes
    ),

    # ---------------------------------------------------------------- F02
    # The unclean man, alone, counting the days. Established here.
    "f02": PageSpec(
        seq_title="THE ASHES",
        frame_label="F02",
        panels=(
            Panel("marked",
                  "a close study of a hand with a faint dry grey-ash smudge across the "
                  "palm, drawn as a quiet plain detail"),
            Panel("apart",
                  "a small sketch of a single figure sitting apart from a distant camp, "
                  "seen small across open ground"),
            Panel("seven days",
                  "a small sketch of seven plain pebbles laid in a row on bare dirt"),
        ),
        still_shot_type="MEDIUM shot",
        anim_shot_desc="medium shot",
        main_scene_still=(
            "bare, stony ground outside the camp under a flat, pale overcast sky; the "
            "unclean man sits alone on the ground, fully inside the frame, his knees drawn "
            "up, one hand resting on his knee bearing a faint, dry, matte grey-ash smudge "
            "across the palm and along the side of the hand — not a wound, dry ash only; his "
            "face is plain and matter-of-fact, patient rather than ashamed; low tents of the "
            "camp sit small and far off across the open ground behind him; no other person "
            "appears anywhere on the page. The unclean man: " + _MAN_BUILD + ". Stage 0 "
            "dosage: no blue Swirls of Life ink motif anywhere on this page — no blue ink "
            "appears anywhere in the scene, the panels, or the margins."
        ),
        material_closer=(
            "the ash on his hand behaves like real dry soot resting on skin, matte and grey, "
            "never a wet ink stain and never glowing."
        ),
        caption_lines=("the law calls him unclean",),  # narration verbatim
        corner_note="NOTE: not out of sin",
        panel_motions=(
            "the light across the sketched hand and its ash mark shifts gently, nothing "
            "else changes",
            "the sketched grass at the man's feet bows faintly in a passing wind",
            "the light across the sketched pebbles shifts gently, nothing else changes",
        ),
        main_scene_animation=(
            "the unclean man sits completely still, only his chest rising and falling "
            "slowly in an ordinary breath, his gaze steady on the middle distance; the dry "
            "grey ash mark on his hand stays exactly as drawn, in place, for the whole clip, "
            "never spreading, never changing shape; the dry grass around him sways very "
            "gently; the distant tents stay exactly as drawn; no new stain, spot, or "
            "darkening appears anywhere on the page at any point."
        ),
        fence_kind="none",
        refs=[],  # ESTABLISHING page — unclean_man_ref cropped FROM it
        model_tier="veo3_1_lite",  # atmospheric hold, nothing completes
    ),

    # ---------------------------------------------------------------- F03
    # Direct address. Stain unchanged (D1) — ceremonial uncleanness doesn't
    # escalate with time/repetition the way a sin/guilt stain might; it
    # stays fixed until the ritual resolves it on day 3/7 (see F04).
    "f03": PageSpec(
        seq_title="THE ASHES",
        frame_label="F03",
        panels=(
            Panel("the grave",
                  "a small sketch of a plain mound of stones marking a grave, drawn as a "
                  "quiet still object"),
            Panel("worn path",
                  "a small sketch of a single worn footpath crossing open ground toward the "
                  "grave, drawn as a quiet plain detail"),
            Panel("out of reach",
                  "a small study of a plain clay water vessel sitting untouched some "
                  "distance away, drawn as a quiet still object"),
        ),
        still_shot_type="MEDIUM WIDE shot",
        anim_shot_desc="medium wide shot",
        main_scene_still=(
            "bare, open country under a flat, pale overcast sky, no meadow, no lush "
            "greenery; the unclean man kneels beside a plain mound of stones marking a "
            "grave, fully inside the frame, one hand resting on the topmost stone, bearing "
            "the same faint, dry, matte grey-ash smudge across the palm as before — not a "
            "wound, dry ash only, unchanged from before; his face is plain and matter-of-"
            "fact, weary rather than ashamed; a plain clay water vessel sits untouched on "
            "the ground some distance off, well apart from him; no other person appears "
            "anywhere on the page. The unclean man (match his reference images): " +
            _MAN_BUILD + ". Stage 0 dosage: no blue Swirls of Life ink motif anywhere on "
            "this page — no blue ink appears anywhere in the scene, the panels, or the "
            "margins."
        ),
        material_closer=(
            "the ash on his hand behaves like real dry soot resting on skin, matte and grey, "
            "never a wet ink stain and never glowing."
        ),
        caption_lines=("a stain water alone can't reach",),  # narration verbatim
        corner_note="NOTE: not from sin",
        panel_motions=(
            "the light across the sketched stones shifts gently, nothing else changes",
            "a thin drift of dust crosses the sketched footpath",
            "the light across the sketched vessel shifts gently, nothing else changes",
        ),
        main_scene_animation=(
            "the unclean man kneels completely still, only his chest rising and falling "
            "slowly in an ordinary breath, his gaze resting on the stones beneath his hand; "
            "the dry grey ash mark on his hand stays exactly as drawn, in place, for the "
            "whole clip, never spreading, never changing shape; the untouched water vessel "
            "sits still, exactly as drawn, well apart from him; no new stain, spot, or "
            "darkening appears anywhere on the page at any point."
        ),
        fence_kind="none",
        refs=[R_MAN, R_MAN_FACE, R_PLACE],
        model_tier="veo3_1_lite",  # atmospheric hold, nothing completes
    ),

    # ---------------------------------------------------------------- F04
    # NT link + purification. Stain visibly clears — the OPPOSITE mechanic
    # from swirl (which bleeds/accumulates): stain washes/rinses away under
    # real water, a literal cleaning action, never an ink dissolve. Swirl
    # Stage 1 lands on the water/vessel itself (the provision), never on
    # either man. High-tide check: stain(fading, ~D1) + swirl(Stage 1) = 2,
    # well under the stainDose+swirlStage<=4 ceiling.
    "f04": PageSpec(
        seq_title="THE ASHES",
        frame_label="F04",
        panels=(
            Panel("hyssop",
                  "a small sketch of a hyssop branch dipped into a plain clay vessel of "
                  "water, drawn as a quiet plain action"),
            Panel("the water",
                  "a small study of the ash-and-water vessel alone, drawn as a quiet still "
                  "object"),
            Panel("rinsed",
                  "a close study of a hand with its dry ash mark half rinsed away under a "
                  "trickle of water, drawn as a quiet plain detail"),
        ),
        still_shot_type="MEDIUM WIDE shot",
        anim_shot_desc="medium wide shot",
        main_scene_still=(
            "bare, open country under a flat, pale overcast sky; the priest kneels facing "
            "the unclean man, fully inside the frame, holding a dripping hyssop branch just "
            "above the unclean man's outstretched hand, a trickle of water running across "
            "the man's palm where the dry grey-ash mark is visibly rinsing and lifting away "
            "under the water, clean bare skin showing through where the water has already "
            "passed — the ash washing off like real dry soot under a real trickle, never "
            "dissolving like wet ink; the priest's own hands are clean, no ash on him in "
            "this scene; both men's faces are plain and purposeful, the unclean man's "
            "slightly open with quiet relief, neither dramatic nor tearful. The priest "
            "(match his reference images): " + _PRIEST_BUILD + ". The unclean man (match "
            "his reference images): " + _MAN_BUILD + ". Stage 1 dosage: exactly one "
            "restrained thread of blue ink, with the faintest trace of muted gold, winding "
            "once around the plain clay vessel of water the priest holds in his other hand, "
            "touching only the vessel, touching neither man, the only blue on the whole "
            "page, behaving like a single line of wet ink bled into the paper."
        ),
        material_closer=(
            "the water and the rinsing ash behave like real trickling water lifting real "
            "dry soot from skin, never wet ink dissolving; the single blue thread on the "
            "vessel is the only ink that behaves like living ink on this page."
        ),
        caption_lines=("the ashes could only point forward",),  # narration verbatim
        corner_note="NOTE: on the seventh day",
        panel_motions=(
            "a single drop of water falls from the sketched hyssop branch, then stills",
            "the sketched thread on the vessel shifts very slightly, nothing else changes",
            "the sketched trickle of water crosses a fraction further over the hand, then "
            "stills",
        ),
        main_scene_animation=(
            "the priest tips the hyssop branch a fraction further, one slow, deliberate "
            "motion, and a little more water runs across the unclean man's palm, the dry "
            "grey ash continuing to rinse and lift away beneath the trickle, clean skin "
            "spreading a little further where the water has passed, the motion completing "
            "early in the clip and then holding; the single thin blue ink thread on the "
            "vessel stays exactly as drawn, in place, for the whole clip; both men hold "
            "still otherwise, only their chests rising and falling in ordinary breath; no "
            "new stain, spot, or darkening appears anywhere on the page at any point."
        ),
        fence_kind="none",
        refs=[R_MAN, R_MAN_FACE, R_PRIEST, R_PLACE],
        model_tier="kling3_0",  # the rinsing-away + hyssop-tip motion must visibly COMPLETE
                                # mid-clip — Kling's lane
    ),
}


def _out_paths(page_id: str) -> tuple[Path, Path]:
    return (HERE / f"the_ashes_{page_id}_9x16.png",
            HERE / f"the_ashes_{page_id}_9x16.mp4")


def main() -> int:
    args = [a for a in sys.argv[1:]]
    if "--print" in args:
        wanted = [a for a in args if a in PAGES] or list(PAGES)
        for pid in wanted:
            spec = PAGES[pid]
            print(f"\n{'=' * 78}\n{spec.frame_label}  [{spec.model_tier}]  "
                  f"caption: {spec.caption_lines}\n{'-' * 78}")
            print("STILL:\n" + assemble_still_prompt(spec))
            print("\nANIMATION:\n" + assemble_animation_prompt(spec))
        return 0

    page_ids = [a for a in args if a in PAGES]
    if len(page_ids) != 1:
        print("usage: render_ashes.py <f01..f04> [--animate] | --print [fNN]")
        return 2
    pid = page_ids[0]
    spec = PAGES[pid]
    png, mp4 = _out_paths(pid)

    if "--animate" in args:
        if not png.exists():
            print(f"  FAILED: still {png.name} not rendered/approved yet.")
            return 1
        return 0 if render_animation(spec, png, mp4) else 1
    return 0 if render_still(spec, png) else 1


if __name__ == "__main__":
    sys.exit(main())
