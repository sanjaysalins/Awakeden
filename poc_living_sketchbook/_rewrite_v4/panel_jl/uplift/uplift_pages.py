"""JL uplift: new Jesus page (F07) + new woodcut back cover prompts, and animation prompts for F03/F04/F07/back.
Imports ep08's episode (builds, refs) read-only. Writes prompts.json next to this file."""
import sys, json
from pathlib import Path
EP8 = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_08_can_any_good_thing")
JL = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_pilot_01_jacobs_ladder")
sys.path.insert(0, str(EP8))
import episode as E  # read-only import
from swirls_page import PageSpec, Panel, Ref, assemble_still_prompt, assemble_animation_prompt  # noqa

R_J, R_N = E.R_JESUS, E.R_NATHANAEL
R_STONE = Ref("the field stone -- one rough uncut tan-brown boulder with a flattened top", str(JL / "refs" / "stone_ref.png"))
R_LADDER = Ref("the ladder -- plain weathered wood, two straight rails and flat rungs", str(JL / "refs" / "ladder_ref.png"))

F07 = PageSpec(
    seq_title="THE LADDER", frame_label="F07",
    panels=(Panel("the same stone", "the rough uncut field stone alone (match its reference image), a quiet dry object on bare ground"),
            Panel("the same ladder", "a close study of one ladder rail and two rungs of plain weathered wood (match the ladder reference image), standing on bare dirt"),
            Panel("the Son of man", "a man's open hand lifted palm upward, drawn calm and still, a close crop")),
    still_shot_type="MEDIUM WIDE shot", anim_shot_desc="medium wide shot",
    main_scene_still=(
        f"a hillside in Galilee at midday under a broad fig tree, soft dappled shade. {E.JESUS_BUILD}, fully inside the frame, standing on the left, "
        "one hand lifted and open toward the sky as he speaks, his face turned toward the other man; "
        f"{E.NATHANAEL_BUILD}, fully inside the frame, standing on the right at the foot of the fig tree, looking up at him with open wonder. "
        "Exactly two men are in the picture. Stage 2 dosage: one small blue ink thread rising from Jesus' lifted open hand into the air above it, touching no skin, "
        "the only blue on the whole page."),
    material_closer="every line is confident and whole, so the single blue thread above the lifted hand is the only unusual ink on the page.",
    panel_motions=("the stone sits still", "the ladder rail sits still", "the open hand holds"),
    main_scene_animation=("Jesus' lifted hand rises a little and holds while he speaks; then the fig leaves stir and dappled shade slides across the ground and the robe hems stir; "
                          "Nathanael stands and listens; the blue thread stays exactly as drawn, in place, for the whole clip;"),
    fence_kind="none", caption_lines=("that same picture",), corner_note="",
    refs=[R_J, R_N, R_STONE, R_LADDER], panel_style="woodcut_hybrid", clip_duration=7)

BACK_STYLE = ("16th-century Albrecht Durer woodcut linework blended with contemporary cinematic landscape photography, dense parallel hatching, hard black contours, "
              "ink-on-block texture, vertical 9:16 aspect ratio, wide static shot, ultra-crisp.")
TITLE_STYLE = ("bold engraved wood-block title lettering, carved in the same dense woodcut style as the rest of the image, thick confident carved strokes, "
               "not a modern font, no drop shadow, no glow, no banner or box behind it, sitting naturally within the composition")
BACK = (
    "Dawn over the same wind-scoured stony hill country. In the centre foreground one rough uncut field stone (match the stone reference image) stands set upright on end "
    "like a small pillar on bare ground, with a little scattered oil-dark stain at its foot, small stones and sparse dry grass around it. No person and no figure anywhere. "
    "A wide open sky above, the first golden sun on the horizon, carved cloud forms parting, soft rays of light fanning across the sky. "
    "Low golden light, atmospheric haze, deep teal shadows, photographic tonality. Match the style of the first reference image (the earlier dawn cover) closely. "
    f"{BACK_STYLE} Near the bottom of the frame, {TITLE_STYLE}, reading: \"GOD CAME TO HIM FIRST\", with smaller matching lettering beneath it reading: \"GENESIS 28\". "
    "No other text, letters, numbers or words appear anywhere on the image beyond these two lines. Avoid: modern clothing, any ladder, any angel, busy foreground, deformed anatomy, smooth photorealism without linework.")
BACK_ANIM = ("Stationary camera, locked wide static shot. The baked lettering at the bottom of the frame stays perfectly identical and still for every frame of the clip. "
             "For the first three seconds the sun rises very slightly and the carved clouds drift slowly across the sky; for the rest of the clip a little dust blows across the ground "
             "and the dry grass sways in the morning wind. The stone stands exactly as drawn.")

F03_ANIM = ("Stationary camera, locked wide static shot. The angels continue the motion they are drawn in, very slowly: for the first four seconds the ascending angels ease upward "
            "and the descending angels ease downward, each moving at most one rung, every angel keeping both feet on the ladder rungs. "
            "For the rest of the clip their robes sway gently, Jacob sleeps at the ladder's foot with his chest rising and falling slowly, the dry grass stirs, and the stars hold steady. "
            "The ladder, the stone and the staff stay exactly as drawn. The blue ink thread along the right rail stays exactly as drawn, in place, for the whole clip.")
F04_ANIM = ("Stationary camera, locked wide static shot. The broad pale brightness at the top of the ladder stays exactly as warm and steady as it already is for the whole clip. "
            "For the first four seconds the angels on the lower rungs stand still with heads bowed, their robes stirring faintly, and the dry grass bows in a passing wind. "
            "For the rest of the clip Jacob sleeps far below with his chest rising and falling slowly, and one hand on his mantle tightens once and settles. "
            "The ladder stays exactly as drawn. The few soft blue threads and the small bloom stay exactly as drawn, in place, for the whole clip. The stars hold steady.")

if __name__ == "__main__":
    out = {"f07": assemble_still_prompt(F07), "anim_f07": assemble_animation_prompt(F07),
           "back": BACK, "anim_back": BACK_ANIM, "anim_f03": F03_ANIM, "anim_f04": F04_ANIM}
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items(): print(k, len(v))
