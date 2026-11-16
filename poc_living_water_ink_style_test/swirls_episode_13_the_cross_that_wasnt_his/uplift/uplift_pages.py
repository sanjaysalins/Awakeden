"""ep13 uplift: 7 new storyboard pages. Imports the episode's own builds/refs read-only; unchanged page template.
python uplift_pages.py  -> writes prompts.json (still + anim prompt per page, plus cover anim)."""
import sys, json
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EP))
import episode as E  # read-only import
from swirls_page import PageSpec, Panel, assemble_still_prompt, assemble_animation_prompt  # noqa

SEQ = E.SEQ_TITLE
SB, CB, GB, RB = E.SIMON_BUILD, E.CROSS_BUILD, E.GATE_BUILD, E.ROAD_BUILD

def mk(label, panels, shot, shot_l, scene, closer, pm, anim, cap, note, refs, dur):
    return PageSpec(seq_title=SEQ, frame_label=label, panels=panels, still_shot_type=shot, anim_shot_desc=shot_l,
                    main_scene_still=scene, material_closer=closer, panel_motions=pm, main_scene_animation=anim,
                    fence_kind="none", caption_lines=(cap,), corner_note=note, refs=refs,
                    clip_duration=dur, panel_style="woodcut_hybrid", include_no_bubble_clause=False)

F01B = mk("F01B",
    (Panel("the country", "open stony fields under morning light, a dry road coming in over a rise, no one on it"),
     Panel("empty hands", "a countryman's two empty sun-browned hands, swinging loose, close, no face"),
     Panel("passed by", "worn leather sandals walking on dusty road stones, close and low, no face")),
    "CLOSE shot", "close shot",
    (f"{SB} shown from the chest up, close, in profile turned three-quarter toward the left, walking along the dry road, "
     f"{E.SIMON_UNBURDENED}, his eyes fixed on the road ahead and not on anything behind him, his mouth closed, his brow level, "
     "dust on his cheek, the plain head-cloth tied at the nape, the rust-striped mantle over his left shoulder, fully inside the frame; "
     "behind him only the dry road, a pale-gold limestone wall far back and soft, and hazy morning sky; no other figure anywhere, no gate "
     "detail, no hill, no crosses, no crowd. Stage 0: no blue ink motif anywhere on this page, no blue or gold anywhere."),
    "no unusual ink of any kind is at work on this page -- no blue, no gold, no stain.",
    ("the fields sit still", "the empty hands sway slightly", "the sandals walk in place"),
    ("Simon walks on the spot with steady unhurried steps, his shoulders rolling gently, his eyes on the road ahead and his lips closed and still; "
     "his body stays in the same place and the same size in the frame for the whole clip; a thin haze of dust drifts behind him; the wall and the sky stay as drawn;"),
    "passed by", "", [E.R_SIMON_FACE, E.R_SIMON], 3)

F02B = mk("F02B",
    (Panel("seized", "a soldier's hand closed around a man's upper arm through an oatmeal wool sleeve, close, no face"),
     Panel("the road", "dust of the road close and low with one pair of sandals planted, no face"),
     Panel("no answer", "a plain iron helmet seen from behind against pale sky, close, no face")),
    "CLOSE shot", "close shot",
    (f"{SB} shown from the chest up, close, his face turned in three-quarter toward the viewer, startled and still, his eyes wide, his mouth closed, "
     "dust on his cheek, the plain head-cloth tied at the nape; a soldier's one strong hand closed firmly around Simon's upper arm through his oatmeal wool sleeve, "
     "the soldier himself cropped by the frame edge so that only his forearm, hand and the edge of his rust-brown tunic and iron cuirass show, his face NOT shown; "
     "no cross, no beam and no wood anywhere on this page; behind them soft pale limestone wall and hazy sky; no other figure anywhere. "
     "Stage 0: no blue ink motif anywhere on this page, no blue or gold anywhere."),
    "no unusual ink of any kind is at work on this page -- no blue, no gold, no stain.",
    ("the gripping hand holds, still", "the dust settles", "the helmet sits still"),
    ("Simon draws one slow breath, his eyes wide and his lips closed and still; the soldier's hand stays closed on his arm and does not move; "
     "his body stays in the same place and the same size in the frame for the whole clip; a thin haze of dust drifts low across the road; the wall and the sky stay as drawn;"),
    "Nobody asked him", "", [E.R_SIMON_FACE, E.R_SIMON, E.R_SOLDIERS], 4)

F03B = mk("F03B",
    (Panel("the stone", "the broad worn threshold stone of a gate, close and low, a little dust on it, no figure"),
     Panel("the doorway", "the dark open doorway of a city gate seen from the road outside, no figure"),
     Panel("the road", "the dry road beginning at the foot of the gate, no figure")),
    "LOW ANGLE shot", "low angle shot",
    (f"a low camera near the ground at the gate's threshold: the broad worn threshold stone of the gate ({GB}) lying across the doorway's foot; "
     "one plain flat leather sandal of a man stepping across it from the dark doorway side to the bright road side, the foot of Simon of Cyrene in an oatmeal wool tunic hem "
     "with bare dusty shin, his other foot still on the doorway side; just behind him and lifted clear of the ground, the lower end of a long dark weathered rough-hewn timber "
     f"trailing after him, matching image reference 'the cross' in wood colour and roughness ({'a plain Latin-cross timber'}), only its lower end visible; "
     "no face and no upper body shown anywhere, no other figure. A wide area of blank pale wall to the left. "
     "Stage 1: exactly one restrained thread of blue ink rising a short way from the threshold stone itself, touching only the stone, the only blue on the whole page."),
    "the one thin blue thread rising from the threshold stone is the only unusual ink on the page, and the wood, the foot and the paper are free of any ink.",
    ("the stone lies still", "a little dust drifts over the doorway", "the road sits still"),
    ("the stepping foot crosses the stone and plants on the road side in the first two seconds, then the trailing timber end follows and stays lifted clear of the ground; "
     "dust lifts softly where the sandal lands and settles; the blue thread on the stone stays exactly as drawn, in place, for the whole clip;"),
    "through the gate", "", [E.R_GATE, E.R_CROSS, E.R_SIMON], 4)

F05B = mk("F05B",
    (Panel("the camp", "dark goat-hair tents in a ring on dry desert ground, no figure"),
     Panel("the fire", "a fire of wood burning on open bare ground, close, no figure"),
     Panel("without", "the last tent's edge with open empty ground beyond it, no figure")),
    "MEDIUM WIDE shot", "medium wide shot",
    ("an Old Testament scene on older, browner, more aged paper than the other pages: the edge of an ancient camp of dark goat-hair tents at the left; "
     "two plain working men in coarse undyed wool tunics and head-cloths carrying the carcass of a bull slung from a long wooden pole between their shoulders, walking RIGHT "
     "away from the last tent toward a wood fire burning on open bare ground beyond the camp; the carcass is an animal's body, nothing else; dry desert ground, "
     "a low pale sky; exactly two men, no other figure, no priest, no cross, no gate. No blue ink and no gold anywhere on this page."),
    "no unusual ink of any kind is at work on this page -- no blue, no gold, no stain.",
    ("the tents sit still", "the flames flicker", "the open ground sits still"),
    ("the two men walk RIGHT with slow steady steps, the pole swaying gently on their shoulders, away from the last tent toward the fire; "
     "the flames of the fire flicker and a little smoke drifts upward; the tents stay as drawn; both men stay fully in the frame for the whole clip;"),
    "without the camp", "", [], 5)

F06B = mk("F06B",
    (Panel("the wall", "a high wall of pale-gold limestone blocks seen from outside, no figure"),
     Panel("the road", "a dry dirt road running along the foot of a wall, no figure"),
     Panel("the rise", "a low stony rise with a dry road going over it, no figure")),
    "HIGH ANGLE WIDE shot", "high angle wide shot",
    (f"a high camera looking down from above the city wall: the long pale-gold limestone wall running along the left side with the gate of the city ({GB}) small in it, "
     f"and the dry dirt road outside running along the foot of the wall and away over a low stony rise at the right; on the road, small and far below, "
     f"{SB} walking RIGHT along the road, the plain head-cloth and rust-striped mantle just readable, carrying the long dark weathered timber cross across his shoulders "
     f"(match image reference 'the cross': {'a plain rough Latin cross'}); much further ahead, tinier, three small figures walking away; the ground dry, no water anywhere, no hill, no crosses on the horizon, no crowd. "
     "Stage 2: a few soft blue threads rise from the threshold stone into the dark opening of the gate and one small soft hazy blue patch sits strictly inside that dark opening, "
     "never above the lintel, never on the road, never on the wood or the man, behaving like wet ink bled into paper, never a glow."),
    "the blue threads and the one small bloom held inside the gate's dark opening are the only unusual ink on the page, and the wood, the road and every figure are free of any ink.",
    ("the wall sits still", "a thin banner of dust drifts along the road", "the rise sits still"),
    ("camera locked high; Simon keeps walking RIGHT along the road at a steady pace, the cross steady on his shoulders, staying small and fully visible in the frame; "
     "the tiny figures ahead keep walking away; a low thin haze of dust drifts along the road; the blue threads and the small bloom in the gate's opening stay exactly as drawn, in place, for the whole clip;"),
    "out there", "", [E.R_SIMON, E.R_CROSS, E.R_GATE, E.R_ROAD], 3)

F07B = mk("F07B",
    (Panel("reproach", "a long dark weathered timber pressing on a man's shoulder, close, no face"),
     Panel("they stare", "a pointing hand of a roadside onlooker, close, no face"),
     Panel("shame", "dust of the road with one line of footprints, no figure")),
    "MEDIUM CLOSE shot", "medium close shot",
    (f"{SB} shown from the chest up, walking RIGHT along the dry road, his face visible in profile-to-three-quarter, calm, his eyes level on the road ahead, his mouth closed, "
     f"carrying the long dark weathered timber cross across the back of his shoulders with both hands gripping it (match image reference 'the cross'; {'plain rough Latin cross'}); "
     "at the roadside behind him, smaller, exactly three plain onlookers in simple everyday wool tunics, none wearing a head-cloth or a rust-red stripe, staring after him, one pointing; "
     "dry road, pale hazy sky; no soldiers, no gate, no hill, no crosses beyond the one he carries. "
     "Stage 3: one loose open band of blue ink threads with traces of muted gold drifting high in the sky above the road, touching nothing on the ground, never on the wood, never on any figure, behaving like wet ink bled into the sky wash, never a glow."),
    "the blue-and-gold band in the sky is the only unusual ink on the page, and the wood and every figure are free of any ink.",
    ("the timber presses, still", "the pointing hand holds", "the footprints sit still"),
    ("Simon keeps walking RIGHT with a steady stride, the cross steady across his shoulders, his lips closed and still, staying in the same place and the same size in the frame; "
     "the three onlookers stay at the roadside with their heads turning slowly to follow him; a thin haze of dust drifts along the road; the blue-and-gold threads drift within their own band in the sky;"),
    "Reproach is shame", "", [E.R_SIMON, E.R_SIMON_FACE, E.R_CROSS], 5)

F09B = mk("F09B",
    (Panel("asked", "a single open hand, palm up, empty, offered toward the viewer against plain paper, no figure, no ink on or near it"),
     Panel("freely", "two lines of sandal-prints in dust running away from the viewer, no figure"),
     Panel("only the shame", "a bare patch of dry road with a few field-stones, no figure")),
    "WIDE shot, very low", "wide shot, very low",
    (f"a very low camera on the road ({RB}): in the near foreground one large open human hand, palm up and empty, a plain sun-browned workman's hand and wrist rising from the bottom edge of the frame, "
     "offered toward the viewer, nothing in it; behind the hand the dry road runs straight away up the long gentle rise to the far crest, empty, nothing visible beyond the crest; no figure at all except the one hand, "
     "no gate, no wall, no cross, no crowd. Stage 3 dosage: the blue ink motif with traces of muted gold woven loosely through the upper air above the road from near to far crest, tied to no figure, "
     "touching nothing on the ground, never on the hand, behaving like wet ink bled through the page's sky wash, never a glow."),
    "the blue-and-gold band in the sky is the only unusual ink on the page, and the hand and the road are free of any ink.",
    ("the open hand holds", "the sandal-prints sit still", "the road patch sits still"),
    ("the open hand stays open and offered, the fingers easing a little and then holding; a thin haze of dust drifts along the road behind it; "
     "the blue-and-gold ink threads drift smoothly within their own band across the sky above the road; the hand stays fully in frame;"),
    "Only the shame", "", [E.R_ROAD, E.R_SIMON], 7)

PAGES = {"f01b": F01B, "f02b": F02B, "f03b": F03B, "f05b": F05B, "f06b": F06B, "f07b": F07B, "f09b": F09B}

if __name__ == "__main__":
    out = {}
    for k, v in PAGES.items():
        out[k] = assemble_still_prompt(v)
        out["anim_" + k] = assemble_animation_prompt(v)
    Path(__file__).with_name("prompts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k, v in out.items():
        print(k, len(v))
