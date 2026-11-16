"""ep08 uplift: 4 new storyboard pages (+ new animation prompts for the existing F03/F04 stills).
Imports the episode's own builds/refs read-only. Prompts come from swirls_page.assemble_*_prompt, unchanged template."""
import sys
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only import
from swirls_page import PageSpec, Panel, Ref, assemble_still_prompt, assemble_animation_prompt  # noqa

R_N, R_P, R_J = E.R_NATHANAEL, E.R_PHILIP, E.R_JESUS
FIG_REF = Ref("the same fig tree and the same worn ground as in the earlier page's large picture (the tree and the ground ONLY; do not copy that page's layout, panels or figure)",
              str(EP / "swirls_episode_08_can_any_good_thing_f04_9x16.png"))

F03B = PageSpec(
    seq_title="CAN ANY GOOD THING", frame_label="F03B",
    panels=(Panel("caught", "Nathanael's narrowed eyes alone, wary and startled, a close crop"),
            Panel("never met", "an empty dirt road between low stone walls, nobody on it"),
            Panel("the tree", "a single fig leaf in close detail, veins drawn clearly")),
    still_shot_type="MEDIUM CLOSE shot", anim_shot_desc="medium close shot",
    main_scene_still=(
        f"open ground outside the village, afternoon light. {E.NATHANAEL_BUILD}, fully inside the frame, shown from the waist up, "
        "a half-step back from the viewer's side, brow knotted, eyes wide and wary, one hand half raised in front of his chest as if caught; "
        "his outer line is settled and whole. Only the edge of another man's shoulder in a green-olive mantle (Jesus, back turned, no face visible) "
        "intrudes at the right frame edge. Plain pale ground and hazy sky behind. No blue ink anywhere on this page, no glow, no motif."),
    material_closer="every line on this page is confident and whole; there is no blue or gold ink anywhere on the page.",
    panel_motions=("Nathanael's narrowed eyes hold", "the empty road sits still", "the fig leaf sits still"),
    main_scene_animation=("Nathanael draws back half a step in the first two seconds, then his raised hand lowers slowly and he holds; "
                          "the shoulder at the frame edge stays still;"),
    fence_kind="none", caption_lines=("Whence knowest thou me?",), corner_note="",
    refs=[R_N], panel_style="woodcut_hybrid", clip_duration=3)

F05A = PageSpec(
    seq_title="CAN ANY GOOD THING", frame_label="F05A",
    panels=(Panel("the doubt", "a cracked clay cup lying on dry ground, in close detail"),
            Panel("it fell", "dust rising from the ground in soft puffs, close crop"),
            Panel("before him", "two pairs of sandaled feet, one pair kneeling and one standing, close crop")),
    still_shot_type="LOW ANGLE shot", anim_shot_desc="low angle shot",
    main_scene_still=(
        "a low camera near the ground. A man's knees and shins meeting the dust as he kneels, the hem of an ochre-yellow wool robe with a clay-red sash end, "
        "his sandals; in front of him, close, two plain leather sandaled feet of a standing man in a cream-brown robe hem, standing still. No faces and no upper bodies "
        "are shown anywhere. Dust lifting softly where the knees land. A wide area of blank paper to the left of the knees. "
        "Stage 1: exactly one restrained thread of blue ink lying along the ground in the lower right corner, touching only the earth, the only blue on the whole page."),
    material_closer="every line is confident and whole, so the single blue thread on the ground is the only unusual ink on the page.",
    panel_motions=("the cracked cup stays still", "the dust settles", "the kneeling feet stay still"),
    main_scene_animation=("the knees land in the dust in the first second and the dust settles; then the robe hem stills and both pairs of feet hold; "
                          "the blue thread on the ground stays exactly as drawn, never fading;"),
    fence_kind="none", caption_lines=("It fell.",), corner_note="",
    refs=[], panel_style="woodcut_hybrid", clip_duration=3)

F05B = PageSpec(
    seq_title="CAN ANY GOOD THING", frame_label="F05B",
    panels=(Panel("further", "Jesus' eyes alone, lifted upward, calm, no glow"),
            Panel("greater things", "a narrow seam of pale light opening in a bank of cloud"),
            Panel("than these", "Nathanael's upturned face, wonder, lit from above")),
    still_shot_type="MEDIUM shot", anim_shot_desc="medium shot",
    main_scene_still=(
        f"{E.JESUS_BUILD}, fully inside the frame, medium shot, standing with his face lifted toward the sky and one open hand raised toward it; "
        f"{E.NATHANAEL_BUILD}, fully inside the frame, small and low at his side, kneeling, looking up the same way. A wide blank pale sky fills the top third of the picture. "
        "Late golden light. Stage 2 dosage: one small blue ink thread rising from Jesus' raised open hand into the air above it, touching no skin, "
        "and one small blue-gold watercolor bloom in the sky above, the only blue on the whole page, behaving like wet ink bled into the paper."),
    material_closer="every line is confident and whole, so the single blue thread and bloom in the sky are the only unusual ink on the page.",
    panel_motions=("Jesus' lifted eyes hold", "the seam of light holds as drawn", "Nathanael's upturned face holds"),
    main_scene_animation=("Jesus' raised hand rises a little and holds; then the thin cloud drifts slowly and his robe hem stirs; "
                          "Nathanael kneels still; the blue thread and bloom stay exactly as drawn, never fading;"),
    fence_kind="none", caption_lines=("greater things than these",), corner_note="",
    refs=[R_J, R_N], panel_style="woodcut_hybrid", clip_duration=5)

F07 = PageSpec(
    seq_title="CAN ANY GOOD THING", frame_label="F07",
    panels=(Panel("your place", "a woven reed mat lying on the ground, in close detail"),
            Panel("already seen", "leaf shade falling on dry ground, dappled"),
            Panel("come and see", "an open dirt road curving away into hazy hills")),
    still_shot_type="HIGH OVERHEAD shot", anim_shot_desc="high overhead shot",
    main_scene_still=(
        "a high overhead view looking nearly straight down through the canopy of the same broad fig tree, and nobody is there: no person, no figure, no face anywhere. "
        "Under the tree on the worn ground lie a woven reed mat (plain pale woven reed, ancient Galilee) and a pair of plain leather sandals left beside it, the shade a soft dark ring around them. "
        "A wide blank paper margin on the right side of the picture. Stage 2 dosage: soft blue ink threads tracing along the outer edge of the canopy's shadow-ring, "
        "the same thin blue contour ring as in the earlier page, touching only the ground and leaf edges, the only blue on the whole page."),
    material_closer="every line is confident and whole, so the thin blue contour ring at the canopy's edge is the only unusual ink on the page.",
    panel_motions=("the woven mat stays still", "the dappled leaf shade slides slowly", "the road sits still"),
    main_scene_animation=("camera locked top-down; the leaves stir gently and the dappled light slides across the ground; then one leaf drops slowly onto the mat and rests; "
                          "the sandals and mat stay still; the blue contour ring stays exactly as drawn, never fading;"),
    fence_kind="none", caption_lines=("under your fig tree",), corner_note="",
    refs=[FIG_REF], panel_style="woodcut_hybrid", clip_duration=5)

# re-animations of existing approved stills (new two-beat prompts, per spec 5.3)
import copy
F03_RE = copy.deepcopy(E.F03)
F03_RE.clip_duration = 8
F03_RE.main_scene_animation = (
    "Nathanael's stride slows and he comes to a stop in the first three seconds, his lifted foot planting on the ground; then, for the rest of the clip, "
    "Jesus' raised hand lowers a little and the robe hems and the grass stir gently; the three figures standing behind Jesus stay as drawn; "
    "the blue threads and the small blue flower at Jesus' feet stay exactly as drawn, in place, for the whole clip;")
F03_RE.fence_kind = "none"
F04_RE = copy.deepcopy(E.F04)
F04_RE.clip_duration = 10
F04_RE.main_scene_animation = (
    "camera locked top-down. For the first four seconds the fig leaves stir gently and dappled light slides slowly across the ground; "
    "then for the rest of the clip the man under the tree lifts his head once, slowly, and holds; the cloud above the tree and the thin blue contour ring "
    "round the canopy stay exactly as drawn, in place, for the whole clip;")
F04_RE.fence_kind = "none"

PAGES = {"f03b": F03B, "f05a": F05A, "f05b": F05B, "f07": F07}
ANIM = {"f03": F03_RE, "f04": F04_RE, "f03b": F03B, "f05a": F05A, "f05b": F05B, "f07": F07}

if __name__ == "__main__":
    import json
    out = {k: assemble_still_prompt(v) for k, v in PAGES.items()}
    out.update({"anim_" + k: assemble_animation_prompt(v) for k, v in ANIM.items()})
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
