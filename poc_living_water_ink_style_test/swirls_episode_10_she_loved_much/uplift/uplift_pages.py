"""ep10 uplift: 7 new storyboard pages. Imports the episode's builds/refs read-only; template unchanged.
Animation prompts: positive wording only (no 'no bubble' clause: it backfired in the ep08 pilot)."""
import sys, json
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only import
from swirls_page import PageSpec, Panel, assemble_still_prompt, assemble_animation_prompt  # noqa

STAIN = ("The same cold grey-umber stain lies in the paper itself at the lower-right corner of the large picture, formless and matte, crossing the drawn frame border "
         "into the page's own lower-right margin, exactly as on the earlier pages, never touching the feet, the flask or any figure, a band of clean paper between. ")

def mk(label, panels, shot, main, closer, pm, anim, caption, refs, dur, stain=False):
    return PageSpec(
        seq_title="SHE LOVED MUCH", frame_label=label, panels=tuple(Panel(a, b) for a, b in panels),
        still_shot_type=shot, anim_shot_desc=shot.lower(), main_scene_still=main, material_closer=closer,
        panel_motions=pm, main_scene_animation=anim,
        fence_kind="stain" if stain else "none",
        fence_callout="the cold grey-umber stain in the paper at the lower right" if stain else "",
        caption_lines=(caption,), corner_note="", refs=refs, panel_style="woodcut_hybrid", clip_duration=dur,
        include_no_bubble_clause=False)

F03A = mk("F03A",
    [("the dust", "a bare dusty foot sole in close detail, road dust in the creases"),
     ("a tear", "a single drop of water falling through lamplight toward a stone floor"),
     ("the basin", "the plain clay foot-basin and folded towel standing dry beside a doorway, unused")],
    "HIGH OVERHEAD CLOSE shot",
    "looking down from above at one bare dusty foot of Jesus resting on the couch-end, the lower hem of his plain cream robe at the top edge, the wooden couch-foot beneath, "
    "and a single fresh tear-drop just landing on the dusty top of the foot, a small clean wet circle spreading in the dust around it. Only the foot, the drop and the couch are shown: "
    "no face, no head, no mouth, no hands, no other figure anywhere in the picture. Wide pale paper around it. " + STAIN +
    "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page, no blue ink anywhere in the scene, the panels, or the margins.",
    "the cold stain in the paper at the lower right is the only unusual ink at work on this page, and no blue appears anywhere.",
    ("the dust sits still", "the falling drop falls slowly and lands", "the dry basin sits still"),
    "camera locked top-down; in the first two seconds one tear-drop falls onto the dusty foot and a small wet circle spreads in the dust; then for the rest of the clip a second tear-drop falls onto the same foot beside the first and the foot stays completely still; the stain in the paper stays exactly as drawn, in place, for the whole clip;",
    "with tears", [E.R_JESUS, E.R_ROOM], 4, stain=True)

F03B = mk("F03B",
    [("her hair", "the loosed ends of long black hair lying across stone floor, close"),
     ("the cloth", "a plain cream head-cloth lying discarded on the floor stones"),
     ("wiped", "a bare foot's instep with a damp sheen, close")],
    "MEDIUM CLOSE shot",
    f"seen from behind and a little above her left shoulder: {E.WOMAN_BUILD}, kneeling on the floor at the couch-end, her head bowed so low that her long loosed black hair falls forward in a curtain "
    "completely covering her face and lying across the bare foot of Jesus, only the hair, the back of her neck and her red mantle covering her shoulders and back are visible; "
    "no face, no profile, no eyes, no mouth are visible anywhere; her dress is full and modest, never a sensual pose; her contour drawn steady and single-struck, no doubled or tremored line. "
    "The bare foot of Jesus rests on the couch-end under the hair, the lower hem of his plain cream robe above it. " + STAIN +
    "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page, no blue ink anywhere.",
    "the cold stain in the paper at the lower right is the only unusual ink at work on this page, and no blue appears anywhere.",
    ("the hair ends sit still", "the cloth lies still", "the damp sheen holds"),
    "camera locked; in the first two seconds her long black hair shifts and sways gently along the foot as she breathes, her shoulders rising once and settling, her head staying bowed and her face staying hidden under her hair; then for the rest of the clip only the ends of her hair and the folds of her red mantle stir softly while the foot stays completely still; the stain in the paper stays exactly as drawn, in place, for the whole clip;",
    "her hair", [E.R_WOMAN, E.R_JESUS], 4, stain=True)

F03C = mk("F03C",
    [("the flask", "the open alabaster flask held tilted, its stone stopper beside it, close"),
     ("the oil", "one amber drop of oil gathering at the lip of a stone flask, close"),
     ("his feet", "two bare feet resting on a couch-end, close")],
    "CLOSE shot",
    f"two hands of the woman, cropped at the forearms (her red mantle sleeve and ochre tunic sleeve visible), tipping {E.ALABASTER_BUILD}, open, stopper removed, over the bare foot of Jesus resting on the couch-end; "
    "a thin glossy amber stream of ointment runs from the flask's mouth onto the instep and over the foot, a matte sheen on the skin. "
    "Only the hands, the flask and the foot are shown: no face, no head, no other figure. " + STAIN +
    "Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page, no blue ink anywhere.",
    "the cold stain in the paper at the lower right is the only unusual ink at work on this page, and no blue appears anywhere.",
    ("the open flask holds", "the amber drop gathers and falls", "the two feet hold"),
    "camera locked; in the first two seconds her hands tip the flask a little further and the amber ointment runs slowly over the instep of the foot; then for the rest of the clip the thin stream thins to a last drop and her hands hold the flask steady while the foot stays completely still; the stain in the paper stays exactly as drawn, in place, for the whole clip;",
    "the ointment", [E.R_WOMAN, E.R_ALABASTER, E.R_JESUS], 4, stain=True)

F04B = mk("F04B",
    [("he heard", "one small oil-lamp flame on a bronze stand, close"),
     ("Simon", "a thickset man's folded hands resting on a cream-and-umber striped mantle, close"),
     ("answered", "an open hand lifted palm out toward the left, close")],
    "MEDIUM CLOSE shot",
    f"{E.JESUS_BUILD}, shown from the chest up, reclining on the near couch, his head turned toward the upper left, his steady gaze going to a man out of frame, calm, his lips closed; "
    "his right hand lifted a little, palm open, fully inside the frame; only the edge of a cream-and-umber striped mantle intrudes at the far left frame edge. "
    "Warm plastered wall and a lamp-stand behind him. Stage 1 dosage: exactly one restrained thread of blue ink curling up from the back of Jesus's lifted right hand, "
    "touching only the hand and the air just above it, the only blue on the whole page, one stroke of wet ink bled into the paper, smooth and open in its curl, never blot-shaped.",
    "the single blue thread at his hand is the only unusual ink at work on this page.",
    ("the lamp flame wavers softly", "the folded hands hold", "the open hand holds"),
    "camera locked; in the first two seconds Jesus's head turns slowly from the lower right toward the upper left and settles with his gaze steady, his lips staying closed; then his robe and the cushion settle with one slow breath; the single blue ink thread at his hand stays exactly as drawn, in place, for the whole clip;",
    "answered anyway", [E.R_JESUS], 3)

F06B = mk("F06B",
    [("a shrug", "a thickset man's shoulder lifting a little under a striped mantle, close"),
     ("half a nod", "a man's hand turning palm half-outward in a reluctant concession, close"),
     ("the most", "a small clay tablet with tally marks on a table, close")],
    "MEDIUM CLOSE shot",
    f"{E.SIMON_BUILD}, shown from the chest up, close, a bearded man of about fifty-five with an iron-grey square-trimmed beard and a fine cream linen head-cloth, reclining and propped on his elbow, "
    "his eyes dropping down and away, his brow slightly drawn, his lips closed, one hand turned half open in a small reluctant shrug, courteous and closed, never a sneer. "
    "Plain plastered wall behind him. Stage 1 dosage: one thin restrained thread of blue ink curling in the empty air at the right of the picture, far from his face, touching nothing, the only blue on the whole page.",
    "the single thin blue thread in the air is the only unusual ink at work on this page.",
    ("the shoulder holds", "the hand holds", "the tablet sits still"),
    "camera locked; in the first two seconds his eyes lower and his shoulders lift in one small shrug and settle, his lips staying closed; then his folded hand rests and the lamp-light on the wall behind him wavers softly; the thin blue ink thread in the air stays exactly as drawn, in place, for the whole clip;",
    "I suppose", [E.R_SIMON, E.R_SIMON_FACE], 4)

F08B = mk("F08B",
    [("forgiven first", "one open empty hand, palm up, close"),
     ("the jar", "the open alabaster flask lying empty on floor stones, stopper beside it, close"),
     ("freely", "a folded cream cloth resting on a stone floor, close")],
    "CLOSE shot",
    f"two hands of the woman in her lap, cropped at the chest (her red mantle and ochre tunic sleeves visible, no face, no head), held open with the palms up and completely empty, kneeling; "
    f"beside her on the floor stones the {E.ALABASTER_BUILD}, open and empty, its stopper lying beside it, on clean pale paper. A low steady light from the left. "
    "The old stain has dried to a pale ring in the paper beneath her, with no wet remainder anywhere. Stage 2 dosage: one small pale blue-gold watercolor bloom floating in the blank paper above her hands, "
    "with one thin blue thread descending a little toward her open palms, touching only the air, the only blue on the whole page, behaving like wet ink bled into the paper.",
    "the dried pale ring in the paper and the small blue-gold bloom above her hands are the only unusual ink at work on this page.",
    ("the open hand holds", "the empty flask sits still", "the folded cloth sits still"),
    "camera locked; in the first three seconds her open hands settle a little lower and relax, the palms staying open and empty; then for the rest of the clip her mantle stirs softly and the lamp-light across the empty flask wavers; the blue-gold bloom and its thread stay exactly as drawn, in place, for the whole clip;",
    "the receipt, not the price", [E.R_WOMAN, E.R_ALABASTER, E.R_ROOM], 6)

F09B = mk("F09B",
    [("the door", "an open wooden doorway with bright street light beyond, from inside"),
     ("the street", "a sunlit dusty lane between low stone walls"),
     ("her path", "bare footprints in pale dust leading away")],
    "MEDIUM WIDE shot",
    f"{E.WOMAN_BUILD}, seen from the side and a little behind, walking out through the open doorway of the dining room into the bright light of the street, her face lifted up toward the sky, calm and at peace, "
    "her deep madder-red mantle drawn over her hair as a hood, full and modest, her bare feet on the threshold stones; her contour drawn steady and single-struck. "
    f"In the dim room behind her, on the floor stones, the {E.ALABASTER_BUILD}, open and empty, left behind. The dry foot-basin by the door. A bright dusty lane beyond. "
    "No stain anywhere on the page, the paper beneath is clean. Stage 3 dosage: one flowing blue-and-gold ink ribbon sweeping across the upper part of the room over the doorway, the only blue and gold on the whole page, "
    "behaving like wet ink bled into the paper.",
    "the blue-and-gold ribbon over the doorway is the only unusual ink at work on this page.",
    ("the door light holds", "the lane sits still", "the footprints sit still"),
    "camera locked; in the first three seconds she walks forward across the threshold into the street light, her mantle moving gently as she steps; then for the rest of the clip she continues away along the lane, her face still lifted, and the dust stirs softly at her feet; the blue-and-gold ribbon stays exactly as drawn, in place, for the whole clip;",
    "Thy faith", [E.R_WOMAN, E.R_WOMAN_FACE, E.R_ALABASTER, E.R_ROOM], 7)

PAGES = {"f03a": F03A, "f03b": F03B, "f03c": F03C, "f04b": F04B, "f06b": F06B, "f08b": F08B, "f09b": F09B}
if __name__ == "__main__":
    out = {k: assemble_still_prompt(v) for k, v in PAGES.items()}
    out.update({"anim_" + k: assemble_animation_prompt(v) for k, v in PAGES.items()})
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
