"""ep11 uplift: 6 new storyboard pages (F01B F04B F07B F09B F10 redraw F10B) + new two-beat animation
prompts for existing stills F03/F05/F06/F07. Imports the episode's own builds/refs read-only."""
import copy, sys
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only
from swirls_page import PageSpec, Panel, Ref, assemble_still_prompt, assemble_animation_prompt  # noqa

UP = Path(__file__).resolve().parent
R_F09FACE = Ref("the Samaritan's face exactly as drawn on the earlier page F09: balding, receding hairline with thin short grey-flecked hair, short grey beard, deep-set eyes, weathered, about forty",
                str(UP / "stills" / "samaritan_f09_face.png"))

BASE = dict(seq_title="WHERE ARE THE NINE", panel_style="woodcut_hybrid", include_no_bubble_clause=False, corner_note="")

F01B = PageSpec(
    frame_label="F01B",
    panels=(Panel("afar off", "a tiny huddle of men far down a dry road, small, seen from a long way off"),
            Panel("the wall", "a stretch of dry-stone wall in close detail, field-stones and dry grass"),
            Panel("the road", "a long dry dirt road running straight away across open ground, empty")),
    still_shot_type="WIDE SIDE-ON shot", anim_shot_desc="wide side-on shot",
    main_scene_still=(
        f"seen from the side, a long flat stretch of dry dirt road running across the whole width of the frame from left to right, EMPTY for most of its length. "
        f"At the far left, small, the end of a village's dry-stone wall ({E.VILLAGE_EDGE_BUILD}) and {E.JESUS_BUILD}, standing on foot at the wall's end facing right, still, hands empty, fully inside the frame. "
        f"At the far right, small, at a long clear distance from him, {E.TEN_BUILD}, standing together in a huddle, stopped, looking toward him, exactly ten, count them. "
        "Late-afternoon light, long shadows, the ground dry ochre earth and stone, no water anywhere. "
        "A cold grey-umber stain lies in the paper itself beneath and around the huddle of ten, formless and matte, beneath the linework, bounded to the right third of the picture, never over any face; "
        "a wide band of clean paper between the stain and Jesus. No blue ink anywhere on this page."),
    material_closer="the cold stain in the paper beneath the ten men at the right is the only unusual ink at work on this page, and no blue appears anywhere.",
    panel_motions=("the tiny huddle holds still", "the wall sits still", "a thin banner of dust drifts across the road"),
    main_scene_animation=("a thin low haze of dust drifts slowly along the empty road between them for the first two seconds; then Jesus takes one slow breath, his lips closed and still, "
                          "and the loose ends of the ten men's rent garments and lip-cloths stir faintly in the wind, none of them stepping forward; the camera never moves;"),
    fence_kind="stain", fence_callout="the cold grey-umber stain in the paper beneath the ten men at the right",
    caption_lines=("at a distance",), refs=[E.R_JESUS, E.R_VILLAGE], clip_duration=4, **BASE)

F04B = PageSpec(
    frame_label="F04B",
    panels=(Panel("stopped", "two bare feet planted still on dry dust, close"),
            Panel("look", "an open hand turned palm-up in warm light, clean and unmarked, close"),
            Panel("the road", "the dry road ahead over a low rise, empty, open")),
    still_shot_type="MEDIUM CLOSE shot", anim_shot_desc="medium close shot",
    main_scene_still=(
        f"the road ({E.ROAD_BUILD}) behind. One gaunt sun-worn man of the region, about fifty, in a coarse rent tunic of undyed grey-cream wool torn open at the breast, head bare with short grey-black hair, "
        "his strip of lip-cloth now loosed and hanging at his throat, his mouth and face bare. He has stopped on the road and is staring down in wonder at his own bare forearm held up in front of him, turned a little toward the viewer: "
        "the skin of the forearm and the back of the hand is clear and unmarked, no pale patches at all. Shown from the waist up, fully inside the frame, drawn with the same care as every figure in this episode. "
        "No other person appears anywhere on this page. Dry ochre ground, no water. No stain, ring or grey blot anywhere in the paper. "
        "Stage 1 dosage: exactly one restrained thread of blue ink high in the sky, entering at the upper-left edge and running across the upper air, thin as a hair, tied to no figure, touching nothing, the only blue on the page."),
    material_closer="the single blue thread high in the sky is the only unusual ink on the page, and the paper beneath the man is wholly clean.",
    panel_motions=("the planted feet hold still", "the open hand holds, the light across it warming very slightly", "a thin haze drifts over the far road"),
    main_scene_animation=("the man turns his raised forearm slowly in the light and holds it there, his eyes on it, in the first two seconds; then his chest rises in one slow breath and the loosed cloth at his throat stirs in the wind; "
                          "the thin blue ink thread high in the sky stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("they were cleansed",), refs=[E.R_ROAD], clip_duration=4, **BASE)

F07B = PageSpec(
    frame_label="F07B",
    panels=(Panel("the rise", "a low rise of stony hill in close detail, dry grass and field-stones"),
            Panel("dust", "a little dust hanging in still air above bare ground, soft, close"),
            Panel("no one", "a bare patch of dry road with one faint sandal print fading, close")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=(
        "the dry dirt road curving away to the right over a low rise into open stony hill country, wide and EMPTY -- no person, no figure, no animal anywhere, no building, no tree; "
        "a little dust still hanging in the air over the crest of the rise where men have gone; dry ochre earth, scattered field-stones, thin dry grass, a wide pale hazy sky filling the top third; late clear golden light; no water anywhere. "
        "No stain, ring or grey blot anywhere in the paper. No blue ink anywhere on this page."),
    material_closer="every line on this page is confident and whole, and there is no blue or gold ink anywhere on it.",
    panel_motions=("the rise holds still", "the hanging dust drifts and thins", "the faint print lies still"),
    main_scene_animation=("camera locked; the dust hanging over the crest of the rise drifts slowly and thins for the first two seconds; then the dry grass at the road's edge stirs gently in the wind and the light stays steady;"),
    fence_kind="none", caption_lines=("where are the nine?",), refs=[E.R_ROAD], clip_duration=4, **BASE)

F09B = PageSpec(
    frame_label="F09B",
    panels=(Panel("kept walking", "bare feet mid-stride on dry dust seen from behind, close"),
            Panel("not looking back", "the back of a man's bare head and shoulders, small, close"),
            Panel("the rise", "the dry road climbing over a rise in morning light, empty")),
    still_shot_type="WIDE shot", anim_shot_desc="wide shot",
    main_scene_still=(
        f"the road ({E.ROAD_BUILD}) running up and away to the right over a low rise in clear morning light. Exactly nine men -- count them, nine, no more, no fewer -- small in the middle distance, seen from BEHIND, "
        "walking away together up the road toward the rise, backs to the viewer, upright and unhurried, coarse tunics of undyed grey-cream and ochre wool, heads bare, loosed cloths hanging at their throats, none looking back, all different men drawn in the same steady line. "
        "No other figure anywhere. The ground dry, no water. No stain, ring or grey blot anywhere in the paper. "
        "Stage 3 dosage: one loose open band of blue ink threads with traces of muted gold drifting high in the sky above the road, tied to no figure, touching no man and nothing on the ground, the only blue on the page, like wet ink bled into the sky wash, never a glow."),
    material_closer="the loose blue-and-gold band high in the sky is the only unusual ink on the page, and the paper beneath the men is wholly clean.",
    panel_motions=("the striding feet keep their step", "the small figure holds still", "a thin haze drifts over the road"),
    main_scene_animation=("the nine men keep walking away up the road at an even pace, one continuous steady stride, none turning, for the first three seconds; then dust lifts softly behind their steps and drifts; "
                          "the loose blue-and-gold band high in the sky stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("kept walking",), refs=[E.R_ROAD], clip_duration=5, **BASE)

# F10 redraw: same page, the Samaritan gets his real face (same man as F06-F09)
F10 = copy.deepcopy(E.F10)
F10.panel_style = "woodcut_hybrid"; F10.corner_note = ""; F10.include_no_bubble_clause = False
F10.main_scene_still = F10.main_scene_still.replace(
    "RISEN -- standing upright", "RISEN, the SAME man as on the earlier pages with the SAME face (balding with a receding hairline and thin short grey-flecked hair, short grey beard, deep-set eyes, weathered, about forty; NO other figure on this page has this face and Jesus has shoulder-length dark hair) -- standing upright")
F10.main_scene_still = F10.main_scene_still.replace("a close-cropped black beard flecked with grey; dark hair cut short, his head bare", "a short grey beard; thin short grey-flecked hair on a balding head, his head bare")
assert "short grey beard; thin short" in F10.main_scene_still
assert "SAME man as on the earlier pages" in F10.main_scene_still
F10.refs = [E.R_JESUS, E.R_SAMARITAN, E.R_SAMARITAN_FACE, R_F09FACE, E.R_VILLAGE]
F10.clip_duration = 8
F10.main_scene_animation = (
    "camera locked. For the first four seconds the Samaritan's chest rises once in a slow breath and his open hands settle at his sides, his eyes on Jesus's, his lips closed; "
    "then for the rest of the clip the loosed cloth at the man's throat stirs and Jesus takes one slow breath, his open hand not moving, his lips closed and still; "
    "the blue-and-gold ink threads in the air above both heads stay exactly as drawn, in place, for the whole clip;")
F10.fence_kind = "none"

F10B = PageSpec(
    frame_label="F10B",
    panels=(Panel("away", "a line of bare footprints leading away in dry dust, close"),
            Panel("turned", "one pair of bare footprints turned round, close"),
            Panel("back", "the dry road coming toward the viewer, empty, wide")),
    still_shot_type="LOW EYE-LEVEL shot", anim_shot_desc="low eye-level shot",
    main_scene_still=(
        f"the road ({E.ROAD_BUILD}) seen from a low viewpoint at the viewer's own eye level, running away over a low rise in morning light, EMPTY of people -- no figure, no animal anywhere. "
        "In the dust of the road in the foreground, a single track of bare footprints leads away from the viewer toward the rise; at one point along the track, one pair of footprints is turned round and points back toward the viewer. "
        "The footprints are clearly visible and sharp. The ground dry, no water. No stain, ring or grey blot anywhere. "
        "Stage 3 dosage: one loose open band of blue ink threads with traces of muted gold drifting high in the sky above the road, touching nothing on the ground, the only blue on the page, like wet ink bled into the sky wash, never a glow."),
    material_closer="the loose blue-and-gold band in the sky is the only unusual ink on the page, and the road and footprints are wholly clean.",
    panel_motions=("the footprint track lies still", "the turned prints lie still", "a thin haze drifts along the road"),
    main_scene_animation=("camera locked; a thin low haze of dust drifts slowly along the road for the first two seconds; then the dry grass at the road's edge stirs gently in the wind; the footprints stay exactly as drawn; "
                          "the loose blue-and-gold band in the sky stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("didn't end with the nine",), refs=[E.R_ROAD], clip_duration=4, **BASE)

def _re(page, dur, anim, motions=None):
    p = copy.deepcopy(page); p.clip_duration = dur; p.main_scene_animation = anim; p.include_no_bubble_clause = False
    if motions: p.panel_motions = motions
    return p

F03_RE = _re(E.F03, 6,
    "camera locked. For the first three seconds Jesus's raised hand lowers a little and settles, while the ten men keep walking away to the right along the road at an even pace, backs to him, none turning; "
    "then for the rest of the clip the loose ends of their garments stir and dust lifts softly at their feet; Jesus's lips stay closed and still; "
    "the single blue ink thread at his hand and the cold stain in the paper beneath the walking men stay exactly as drawn, in place, for the whole clip;",
    ("the far hill town holds still", "the two backs hold their step", "the hand holds still"))
F05_RE = _re(E.F05, 6,
    "camera locked. For the first three seconds the Samaritan's raised open hands lift a little higher and hold, his face lifting with them, his lips closed and still, while the nine men beyond him keep walking away to the right at an even pace, none turning; "
    "then for the rest of the clip the loosed cloth at his throat stirs and dust lifts softly at the walkers' feet; "
    "the single thin blue ink thread high in the sky stays exactly as drawn, in place, for the whole clip;",
    ("the striding feet hold still", "the raised hands hold still", "the far village holds still"))
F06_RE = _re(E.F06, 7,
    "camera locked, the frame never changes. For the first three seconds the Samaritan's shoulders heave once with the breath of his thanks and settle, his forehead staying to the dust; "
    "Jesus stays as drawn, his lowered open hand not reaching down, his lips closed and still; "
    "then for the rest of the clip a low thin haze of dust drifts along the empty road beyond and the hem of Jesus's robe stirs gently; "
    "the soft blue threads at his hand stay exactly as drawn, in place, for the whole clip;",
    ("the turned feet hold still", "the pressed dust lies still", "the bowed profile holds still"))
F07_RE = _re(E.F07, 6,
    "camera locked, the frame never changes. For the first three seconds Jesus's lifted hand opens a little wider toward the empty road and holds, his face toward the road, his lips closed and still, "
    "the Samaritan at his feet holding still with one slow breath through his back; "
    "then for the rest of the clip a low thin haze of dust drifts along the empty road and Jesus's robe hem stirs gently; "
    "the soft blue threads at his hand stay exactly as drawn, in place, for the whole clip;",
    ("the ten small figures hold still", "the hanging dust drifts and thins", "the profile holds still"))

PAGES = {"f01b": F01B, "f04b": F04B, "f07b": F07B, "f09b": F09B, "f10": F10, "f10b": F10B}
ANIM = {"f01b": F01B, "f03": F03_RE, "f04b": F04B, "f05": F05_RE, "f06": F06_RE, "f07": F07_RE,
        "f07b": F07B, "f09b": F09B, "f10": F10, "f10b": F10B}

if __name__ == "__main__":
    import json
    out = {k: assemble_still_prompt(v) for k, v in PAGES.items()}
    out.update({"anim_" + k: assemble_animation_prompt(v) for k, v in ANIM.items()})
    (UP / "prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
