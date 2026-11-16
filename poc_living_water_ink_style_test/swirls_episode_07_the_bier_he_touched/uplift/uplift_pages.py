"""ep07 uplift: new storyboard pages (positive wording only). Imports the episode read-only."""
import sys, json
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only
from swirls_page import PageSpec, Panel, assemble_still_prompt  # noqa

JB = E.JESUS_BUILD
BB = "the open flat wooden hand-bier, a plain rectangular pallet of weathered olive-brown wood boards with two long carrying poles running its full length, its top entirely open to the sky"
FLAT = ("the SAME flat plank-and-poles stretcher as earlier, a bare plain plank with no raised edge, wall, lip or rim on any side, "
        "never a coffin, never a casket, never a box, never a tray, never on built-in legs")

F01B = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F01B",
    panels=(Panel("kept their distance", "a villager's hand drawn back against a rough stone wall, fingers curled away"),
            Panel("a bare strip of road", "an empty dusty road between two walls, nobody on it"),
            Panel("survival", "a plain clay water jar in a doorway shadow")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=(
        "the dusty road outside the gate of Nain, seen along the road. On the left and right, villagers pressed back against the drystone walls in halted clusters, "
        f"leaving a wide empty strip of bare road down the middle; {BB}, now set down on the bare ground in the middle of that strip, {FLAT}, "
        f"with {E.SON_SHROUDED} lying on it, and the veiled widow standing beside it, her contour steady and single-struck. "
        "Nobody stands within arm's reach of the bier except the widow and two bearers. A wide band of clean empty road between the bier and the crowd on each side. "
        "A cold grey-umber stain lies in the paper beneath the bier only, formless and matte, with clean paper between it and every living figure. "
        "No blue ink anywhere on this page, no glow."),
    material_closer="the cold stain beneath the bier is the only unusual ink on this page, and no blue appears anywhere.",
    panel_motions=("the hand holds", "the road sits still", "the jar sits still"),
    main_scene_animation=("the villagers shift their weight and draw one small step further back against the walls; the bearers stand and the widow breathes slowly; "
                          "the bier and the shrouded form lie completely still, exactly as drawn; the stain in the paper stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("kept their distance",), corner_note="",
    refs=[E.R_BIER, E.R_GATE, E.R_WIDOW], panel_style="woodcut_hybrid", clip_duration=5)

F02A = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F02A",
    panels=(Panel("toward", "a pair of sandaled feet mid-stride on dust, close crop"),
            Panel("not away", "a widow's bare feet standing still on the road, close crop"),
            Panel("the gap", "an open strip of dusty road between two lines of people, seen from low")),
    still_shot_type="LOW ANGLE shot", anim_shot_desc="low angle shot",
    main_scene_still=(
        "a low camera near the ground on a dusty road outside a village gate: two plain worn leather-sandaled feet in the hem of a plain cream-brown wool robe, "
        "walking steadily toward the viewer through an open gap, one foot just lifting, dust stirring softly at the heels; on both sides of the gap, at the edges of the picture, "
        "the bare feet and hems of villagers standing back. No faces and no upper bodies are shown anywhere. "
        "A wide area of blank pale paper in the lower left corner. No blue ink anywhere on this page, no glow."),
    material_closer="every line is confident and whole, and there is no blue or gold ink anywhere on the page.",
    panel_motions=("the striding feet hold", "the still feet hold", "the road sits still"),
    main_scene_animation="the walking feet take two steady steps toward the viewer and dust lifts at the heels and settles; the feet at the picture edges stay still;",
    fence_kind="none", caption_lines=("toward her",), corner_note="",
    refs=[], panel_style="woodcut_hybrid", clip_duration=3)

F03A = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F03A",
    panels=(Panel("stood still", "four pairs of sandaled feet halted on dusty ground, close"),
            Panel("no one else would", "a villager's hand drawn back against a wall, close"),
            Panel("the bare pole", "a weathered olive-brown wooden carrying pole lying on the ground, close")),
    still_shot_type="CLOSE shot", anim_shot_desc="close shot",
    main_scene_still=(
        f"a close, tight crop low over the bier: {BB}, with its two long carrying poles lying flat on the bare ground, {FLAT}. "
        "From the upper edge of the frame a man's right hand and wrist, with the sleeve of a cream-brown wool robe and the edge of an olive mantle, comes down open and flat onto the weathered wooden pole, palm down, fingertips resting on the wood. "
        "No face and no head are shown anywhere. Behind the pole, soft and slightly out of focus, four pairs of dusty sandaled feet of the bearers standing halted. "
        "The shrouded form is out of frame. One single thin thread of blue ink rises straight up from the back of this exact hand, its root touching the skin and nowhere else, "
        "the only blue on the whole page. The paper around the hand is clean cream, and a small grey-umber stain lies in the paper far at the lower edge, never near the hand."),
    material_closer="the single blue thread at the hand is the only blue on the page, and the paper around the hand is clean.",
    panel_motions=("the feet hold", "the hand holds", "the pole sits still"),
    main_scene_animation=("the open hand lowers onto the wooden pole in the first two seconds and lands flat; then the hand rests and presses without moving while the bearers' feet behind stay still and one soft puff of dust settles; "
                          "the blue thread at the hand stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("touched the bier",), corner_note="",
    refs=[E.R_JESUS, E.R_BIER], panel_style="woodcut_hybrid", clip_duration=5)

F03B = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F03B",
    panels=(Panel("the old law", "a plain clay water jar with a hyssop sprig, close"),
            Panel("clean paper", "a blank corner of cream paper with a faint pale ring, close"),
            Panel("the stain dries", "a dried pale ring in cracked dust, close")),
    still_shot_type="MEDIUM CLOSE shot", anim_shot_desc="medium close shot",
    main_scene_still=(
        f"a medium close view over the flat low bier lying on the bare ground: {FLAT}. A man's right hand, in the sleeve of a cream-brown wool robe, rests flat and calm on the wooden plank, palm down, fully clean. "
        "Only the lower part of his arm and his robed shoulder are shown, no face. On the boards and the paper beneath, a cold grey-umber stain lies wet and dark toward the far end of the bier, "
        "but the whole edge nearest his hand has dried to a pale ring; no stain touches his hand, sleeve or the paper under him. The wrapped form lies on the plank beyond his hand. "
        "One single thin thread of blue ink rises straight up from the back of his hand, touching only the hand and the air, the only blue on the page."),
    material_closer="the stain drying back from the hand and the single blue thread are the only two kinds of unusual ink on the page, kept apart by clean paper.",
    panel_motions=("the jar sits still", "the clean corner holds", "the dried ring holds"),
    main_scene_animation=("the hand rests on the plank and presses once, slowly, without sliding; a faint breeze stirs the hem of the sleeve; then everything holds; the stain and its dried pale ring stay exactly as drawn; the blue thread stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("it didn't work that way",), corner_note="",
    refs=[E.R_JESUS, E.R_BIER], panel_style="woodcut_hybrid", clip_duration=7)

F06B = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F06B",
    panels=(Panel("the only direction", "an open palm held out toward the viewer, close"),
            Panel("the road", "the dusty road curving up to a village gate, empty"),
            Panel("the gate", "a low stone gate in sunlight")),
    still_shot_type="MEDIUM CLOSE shot", anim_shot_desc="medium close shot",
    main_scene_still=(
        f"{JB}, shown from the chest up, his open right hand reaching toward the viewer, palm up and open, in the foreground; "
        "behind him the dusty road and the low drystone gate of Nain in warm morning light, no other people. "
        "No stain anywhere; the paper wholly clean. A few soft threads of blue ink drift in one loose band in the air beside his open hand, touching no skin."),
    material_closer="the soft blue threads beside his open hand are the only unusual ink on the page, and the paper is wholly clean.",
    panel_motions=("the palm holds", "the road sits still", "the gate sits still"),
    main_scene_animation="his open hand reaches a little further toward the viewer and holds; his robe and hair stir once in a faint breeze; the road and gate behind stay still; the blue threads stay exactly as drawn, in place, for the whole clip;",
    fence_kind="none", caption_lines=("the only direction",), corner_note="",
    refs=[E.R_JESUS, E.R_GATE], panel_style="woodcut_hybrid", clip_duration=5)

F06C = PageSpec(seq_title="THE BIER HE TOUCHED", frame_label="F06C",
    panels=(Panel("his hand in hers", "a young man's hand held in an older woman's hand, close"),
            Panel("left behind", "the empty bier leaning against a wall, folded linen on it"),
            Panel("home", "a warm lit open doorway, a low table laid")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=(
        f"the gate of Nain from outside, the low drystone wall and timber lintel inside the frame. {E.WIDOW_BUILD}, and her son ({E.SON_BUILD}, now in a plain borrowed mantle), walking in through the gate side by side, "
        "his hand held in hers, both contours steady and single-struck, exactly one of each person. Leaning upright against the wall beside the gate, small in the midground, the empty flat plank-and-two-poles bier, never a ladder, never a box, linen folded on it. "
        "No stain anywhere; the paper wholly clean. A few soft blue threads drift in one loose band in the air above the gate, touching no person."),
    material_closer="the soft blue band in the air is the only unusual ink, and the paper beneath is wholly clean.",
    panel_motions=("the joined hands hold", "the empty bier sits still", "the doorway light stays warm and steady"),
    main_scene_animation="the mother and son walk slowly in through the gate together, his hand in hers; the empty bier leans motionless against the wall; the blue threads stay exactly as drawn, in place, for the whole clip;",
    fence_kind="none", caption_lines=("what's his instead",), corner_note="",
    refs=[E.R_WIDOW, E.R_WIDOW_FACE, E.R_SON, E.R_GATE, E.R_BIER], panel_style="woodcut_hybrid", clip_duration=5)

PAGES = {"f01b": F01B, "f02a": F02A, "f03a": F03A, "f03b": F03B, "f06b": F06B, "f06c": F06C}

if __name__ == "__main__":
    out = {k: assemble_still_prompt(v) for k, v in PAGES.items()}
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
