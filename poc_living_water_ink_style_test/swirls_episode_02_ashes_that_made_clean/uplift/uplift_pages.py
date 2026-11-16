"""ep02 uplift: 6 new storyboard pages + new two-beat clip prompts for existing F01/F03 (re-animation).
Imports the episode's own builds/refs read-only."""
import sys, copy
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only
import render_ashes as RA
from swirls_page import PageSpec, Panel, Ref, assemble_still_prompt, assemble_animation_prompt  # noqa

MAN, PRIEST = RA._MAN_BUILD, RA._PRIEST_BUILD
R_MAN, R_FACE, R_PRIEST, R_PLACE = RA.R_MAN, RA.R_MAN_FACE, RA.R_PRIEST, RA.R_PLACE
NOBLUE = ("Stage 0 dosage: no blue Swirls of Life ink motif anywhere on this page - no blue ink appears anywhere in the scene, "
          "the panels, or the margins.")
CLOSER = "the ash on his hand behaves like real dry soot resting on skin, matte and grey, never a wet ink stain and never glowing."


def P(**k):
    k.setdefault("seq_title", "THE ASHES")
    k.setdefault("fence_kind", "none")
    k.setdefault("corner_note", "")
    k.setdefault("panel_style", "woodcut_hybrid")
    return PageSpec(**k)


F02B = P(frame_label="F02B",
    panels=(Panel("dust", "a handful of dry grey dust held in a cupped palm, in close detail"),
            Panel("rubbing", "a hand rubbing its own palm with dust, close crop"),
            Panel("the mark stays", "a palm with the faint dry grey-ash smudge still in place, close crop")),
    still_shot_type="MEDIUM shot", anim_shot_desc="medium shot",
    main_scene_still=("bare, stony ground outside the camp under a flat, pale overcast sky; the unclean man kneels alone, fully inside the frame, "
        "rubbing his own open palm with a pinch of dry dust from the ground, brow slightly furrowed, patient not ashamed; the faint dry matte grey-ash smudge "
        "still plainly shows on his palm and the side of his hand; low tents of the camp sit small and far off behind him; no other person appears anywhere on the page. "
        "The unclean man (match his reference images): " + MAN + ". " + NOBLUE),
    material_closer=CLOSER,
    panel_motions=("the dust in the palm settles", "the rubbing hand pauses", "the light across the palm shifts gently, nothing else changes"),
    main_scene_animation=("he rubs his palm with the dust twice, slowly, then stops and looks down at his palm; the grey ash mark stays exactly as drawn, in place, for the whole clip; "
        "the dry grass stirs faintly; the distant tents stay exactly as drawn;"),
    caption_lines=("cannot cleanse himself",), refs=[R_MAN, R_FACE, R_PLACE], clip_duration=3)

F02C = P(frame_label="F02C",
    panels=(Panel("outside the camp", "a few low tents far off on a bare rise, seen across open ground"),
            Panel("seven stones", "seven plain pebbles laid in a neat row on bare dirt"),
            Panel("waiting", "a single worn footpath ending at a bare patch of ground")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=("a wide view of bare open ground outside the camp under a flat, pale overcast sky; the unclean man sits alone in the middle distance, fully inside the frame, "
        "knees drawn up, patient; beside him on the ground, seven plain flat stones set in one neat row, exactly seven; the low tents of the camp far off at the horizon; "
        "a wide area of pale empty sky above the horizon; no other person appears anywhere on the page. "
        "The unclean man (match his reference images): " + MAN + ". " + NOBLUE),
    material_closer=CLOSER,
    panel_motions=("the far tents stay still", "the seven pebbles sit still", "the footpath sits still"),
    main_scene_animation=("he sits still, breathing slowly, and turns his gaze to the row of stones beside him, then rests it there; "
        "then the dry grass bends in a passing wind and his tunic stirs faintly; the seven stones stay exactly as arranged, in place, for the whole clip; the distant tents stay exactly as drawn;"),
    caption_lines=("unclean seven days",), refs=[R_MAN, R_FACE, R_PLACE], clip_duration=6)

F02D = P(frame_label="F02D",
    panels=(Panel("the water", "a plain clay water vessel set on bare ground, in close detail"),
            Panel("hyssop", "a green hyssop sprig lying across a hand, close crop"),
            Panel("third day", "three plain pebbles laid in a row on bare dirt")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=("bare open ground outside the camp under a flat, pale overcast sky; the priest walks toward the seated unclean man across an open gap of ground, fully inside the frame, "
        "carrying a plain clay vessel of water in one hand and a green hyssop sprig in the other, his own hands clean, no ash on him; the unclean man sits on the ground in the middle distance with his knees drawn up, "
        "looking toward him, the faint dry grey-ash mark showing on his hand; seven plain flat stones in a neat row on the ground beside the seated man; a wide area of pale empty sky above the horizon; no other person appears anywhere on the page. "
        "The priest (match his reference images): " + PRIEST + ". The unclean man (match his reference images): " + MAN + ". "
        "Stage 1 dosage: exactly one restrained brushstroke of blue ink drawn once down the neck of the clay vessel, a single thin flat stroke lying flat in the surface of the paper "
        "against the vessel's own drawn outline, overlapping only the vessel, touching neither man, the only blue on the whole page, behaving like one stroke of wet ink bled flat into the paper - never dripping, never pooling."),
    material_closer="the single flat blue stroke on the vessel is the only unusual ink on the page.",
    panel_motions=("the vessel sits still", "the hyssop sprig stirs faintly", "the three pebbles sit still"),
    main_scene_animation=("the priest walks a few slow steps across the gap and slows, the water in the vessel steady; then the seated man looks up toward him and holds; "
        "the dry grass stirs faintly; the seven stones stay exactly as arranged, in place; the blue brushstroke on the vessel stays exactly as drawn, in place, for the whole clip;"),
    caption_lines=("on the third day",), refs=[R_PRIEST, R_MAN, R_FACE, R_PLACE], clip_duration=6)

F03A = P(frame_label="F03A",
    panels=(Panel("his hand", "an open palm with a faint dry grey-ash smudge, in close detail"),
            Panel("the mark", "dry grey ash resting on skin, a close crop"),
            Panel("no wrong done", "an ordinary plain working road with nobody on it")),
    still_shot_type="CLOSE shot", anim_shot_desc="close shot",
    main_scene_still=("bare ground outside the camp, flat pale overcast sky and hazy distance behind; a close shot of the unclean man from the chest up, fully inside the frame, "
        "his face lowered and turned slightly, eyes looking down at his own open hand held in front of him, the faint dry matte grey-ash smudge on his palm; his expression is plain and quietly weary, patient, never ashamed; "
        "no other person appears anywhere on the page. The unclean man (match his reference images): " + MAN + ". " + NOBLUE),
    material_closer=CLOSER,
    panel_motions=("the light across the palm shifts gently", "the ash rests still", "the road sits still"),
    main_scene_animation=("he looks down at his open palm, his chest rising in one slow breath, then his fingers curl slowly and open again; the grey ash mark stays exactly as drawn, in place, for the whole clip; "
        "a faint wind stirs his hair;"),
    caption_lines=("to feel unclean",), refs=[R_MAN, R_FACE, R_PLACE], clip_duration=4)

F04B = P(frame_label="F04B",
    panels=(Panel("hyssop", "a hyssop stalk in close detail, small leaves on a thin woody stem"),
            Panel("outside the wall", "a pale stone city wall and gate seen from far off"),
            Panel("the hill", "a bare rocky hill under a heavy sky")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=("a wide view of a bare rocky hill outside a pale limestone city wall of ancient Jerusalem far off to one side, under a heavy grey overcast sky with a narrow seam of pale gold light low on the horizon; "
        "on the hill, small and far off, a single plain wooden cross standing empty, no figure on it; in the near corner of the picture a hyssop stalk with small leaves rising from the dry ground; "
        "no person appears anywhere on the page; reverent, quiet, no blood, nothing graphic. " + NOBLUE),
    material_closer="every line is confident and whole; there is no blue or gold ink anywhere on the page.",
    panel_motions=("the hyssop leaves stir faintly", "the far wall sits still", "the bare hill sits still"),
    main_scene_animation=("the hyssop stalk in the near corner sways gently in a passing wind and the heavy cloud drifts slowly; then the seam of pale light slides slowly along the horizon; the cross stands still, exactly as drawn;"),
    caption_lines=("the blood of Christ",), refs=[], clip_duration=4)

F05 = P(frame_label="F05",
    panels=(Panel("the reach", "a clean open hand reaching down from above, close crop"),
            Panel("the mark", "a palm with a faint dry grey-ash smudge, close crop"),
            Panel("not unclean", "a clean hand resting gently on another hand, close crop")),
    still_shot_type="MEDIUM CLOSE shot", anim_shot_desc="medium close shot",
    main_scene_still=("bare ground in dry grass at the edge of a bare field, under a heavy ash-grey overcast with one narrow low shaft of warm amber light breaking through; "
        "the unclean man sits slumped on the ground, fully inside the frame, one hand lifted and open toward the viewer's upper right showing the faint dry grey-ash smudge on his palm; "
        "from the upper right frame edge only a serene, clean, unhurried human hand and wrist in a warm cream-tan linen sleeve reaches down and rests gently on his ash-marked hand; "
        "the reaching hand stays perfectly clean, no ash on it, no face and no body of the other person is shown anywhere, only the hand and sleeve. "
        "The unclean man (match his reference images): " + MAN + ". " + NOBLUE),
    material_closer=CLOSER,
    panel_motions=("the reaching hand holds", "the ash rests still", "the two hands hold"),
    main_scene_animation=("the clean hand settles onto his ash-marked hand and rests there, still and steady, the man's fingers closing slowly around it; "
        "then the dry grass bends in a passing wind, the sleeve stirs faintly, and the shaft of amber light holds exactly as steady as it already is; "
        "the grey ash mark on his hand stays exactly as drawn, in place;"),
    caption_lines=("He touched what makes us unclean",), refs=[R_MAN, R_FACE, R_PLACE], clip_duration=9)

F01_RE = copy.deepcopy(E.PAGES["f01"]); F01_RE.clip_duration = 8; F01_RE.fence_kind = "none"
F01_RE.main_scene_animation = ("for the first four seconds the priest feeds the last of the cedar wood into the fire with one slow, deliberate motion, his hands steady; "
    "then for the rest of the clip the flame flickers and the grey smoke drifts upward and his robe stirs faintly; the thin blue ink thread rising in the smoke stays exactly as drawn, in place, for the whole clip; "
    "the dry grey ash on his hands and forearms stays exactly as drawn; the distant tents stay exactly as drawn;")
F03_RE = copy.deepcopy(E.PAGES["f03"]); F03_RE.clip_duration = 8; F03_RE.fence_kind = "none"
F03_RE.main_scene_animation = ("for the first four seconds the unclean man kneels, breathing slowly, and slides his hand a little across the topmost stone, then lays it still; "
    "then for the rest of the clip his shoulders drop slightly and the grass and his tunic stir faintly in the wind; the grey ash mark on his hand stays exactly as drawn, in place, for the whole clip; "
    "the water vessel sits still, exactly as drawn, with the flat blue brushstroke on its neck staying exactly as drawn, in place;")

PAGES = {"f02b": F02B, "f02c": F02C, "f02d": F02D, "f03a": F03A, "f04b": F04B, "f05": F05}
ANIM = {**PAGES, "f01": F01_RE, "f03": F03_RE}

if __name__ == "__main__":
    import json
    out = {k: assemble_still_prompt(v) for k, v in PAGES.items()}
    for k, v in ANIM.items():
        v2 = copy.deepcopy(v)
        v2.include_no_bubble_clause = False
        out["anim_" + k] = assemble_animation_prompt(v2)
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
