"""Round 3 fixes: the user's 7 flagged-still defects from the click-to-flag HTML
gallery (2026-07-16), each independently confirmed by eye before patching:
  #5  (05_they_beg) a floating snake reads as emerging from a background man's
      head/neck -- add an explicit no-snake-near-heads guard.
  #8  (08_raised) the pole is drawn skyscraper-giant vs the human figures at its
      base -- the old prompt's own "small dim figures... at the foot of the pole"
      phrasing invited this; bound the pole's height explicitly to ~4-5x a
      standing person and keep the figures at readable human scale.
  #10 (10_camp_looks) multiple bronze-serpent-topped poles/banners scattered
      through the camp instead of the ONE Numbers 21:9 standard -- explicit
      single-standard guard (also risked idol-multiplication doctrinally).
  #20 (20_whosoever) the foreground everyman's face/hair is styled identically
      to this piece's Jesus design (see 21_look_to_the_one_lifted_up_hero_close)
      -- this is Numbers 21, NOT a Christ appearance; lock a distinct look.
  #24 (24_trust) the "shattered" bronze serpent still rendered as a whole
      intact coiled snake lying on the floor -- force disconnected debris with
      no coiled/snake silhouette.
  #25 (25_we_are_all_bitten) the dying man's open hand reads as a gaping wound
      cavity, and the cross shows wrist-wrap+floating nails instead of nails
      driven through -- fix both.
  #27 (27_outward) small living snakes still coiled/attached to at least 2
      forearms instead of bite-wound marks -- these people are AFTER the bite,
      pleading; explicit no-snakes-on-bodies guard.
$0, no render (text only). Run _render_inked_stills.py --only 5,8,10,20,24,25,27
after this to reroll."""
import json
from pathlib import Path

p = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1\visual_16x9_inked\scene_plan.json")
d = json.loads(p.read_text(encoding="utf-8"))
by_id = {s["id"]: s for s in d["scenes"]}

# #5 -- ban any snake touching/near a person's head or body
s5 = by_id[5]
s5["subject_block"] = s5["subject_block"].replace(
    "the people begging for the snakes to be taken away, reverent and urgent,",
    "the people begging for the snakes to be taken away -- any snakes visible in "
    "the scene lie only on the open ground, far from and never touching or "
    "overlapping any person's head, neck, shoulders, or body, absolutely no "
    "snake near, on, or emerging from anyone's head -- reverent and urgent,"
)

# #8 -- bound the pole's scale explicitly; drop the "small dim figures" framing
# that invited a giant pole, keep Moses/elders at readable human scale.
s8 = by_id[8]
sb8 = s8["subject_block"]
sb8 = sb8.replace(
    "raised HIGH against a vast open desert sky at golden hour, the tall pole "
    "standing over",
    "raised on a tall wooden standard-pole roughly FOUR to FIVE TIMES the "
    "height of a standing person -- a believable raised standard, NOT a "
    "skyscraper, NOT towering to the top of the frame, NOT absurdly gigantic "
    "-- set against a vast open desert sky at golden hour, the modestly tall "
    "pole standing over"
)
sb8 = sb8.replace(
    "small dim figures of the stricken below at the foot of the pole;",
    "clearly-readable human figures of the stricken at the foot of the pole, "
    "their scale making plain the pole is only a few times taller than a man, "
    "not a monument;"
)
s8["subject_block"] = sb8

# #10 -- exactly ONE serpent-on-pole standard in the whole camp
s10 = by_id[10]
s10["subject_block"] = s10["subject_block"].replace(
    "some rising restored, some still reaching from the ground, the lifted "
    "bronze small but luminous in the far midground;",
    "some rising restored, some still reaching from the ground; there is "
    "EXACTLY ONE bronze-serpent standard in the entire camp -- absolutely NO "
    "other poles, banners, standards, or repeated serpent shapes anywhere else "
    "in the scene, near or far, foreground or background -- only the single "
    "lifted bronze, small but luminous, in the far midground;"
)

# #20 -- lock a face/hair distinct from the piece's Jesus design
s20 = by_id[20]
s20["subject_block"] = s20["subject_block"].replace(
    "many different people",
    "an ordinary Bronze-Age Israelite everyman in the foreground with SHORT "
    "cropped dark hair (NOT long, NOT flowing, NOT wavy shoulder-length hair) "
    "and rough short stubble (NOT a full groomed beard) -- an ordinary "
    "wilderness face, explicitly NOT resembling this film's Christ/Jesus "
    "character design (no long hair, no serene idealized messianic look, no "
    "halo, no white robe) -- this is Numbers 21, no Christ figure appears "
    "here; many different people"
)

# #24 -- force disconnected debris, no coiled/whole-serpent silhouette
s24 = by_id[24]
s24["subject_block"] = s24["subject_block"].replace(
    "on the floor in shadow the shattered pieces of a broken bronze serpent "
    "statue, dull gold-bronze cast-metal fragments;",
    "on the floor in shadow several small, separate, DISCONNECTED broken "
    "bronze fragments -- angular dull gold-bronze metal shards and chunks, "
    "scattered apart from each other like rubble or broken pottery -- the "
    "fragments do NOT form a coiled body, a head, or any continuous serpent "
    "silhouette; absolutely NOT a whole or recognizable snake shape, NOT a "
    "snake-like creature, just unrecognizable broken metal debris;"
)

# #25 -- fix the dying man's hand wound + the cross nails/wrists
s25 = by_id[25]
sb25 = s25["subject_block"]
sb25 = sb25.replace(
    "weak and unable to heal himself, his hand open and empty;",
    "weak and unable to heal himself, his hand open and relaxed, anatomically "
    "normal and whole with all five fingers -- only a small pair of red "
    "puncture-mark snakebite dots on the back of the hand or wrist, subtle "
    "and realistic, absolutely NOT a gaping hole, NOT a wound cavity, NOT "
    "torn or graphic flesh, NOT anatomically distorted;"
)
sb25 = sb25.replace(
    "both arms outstretched and NAILED to the crossbeam, wrists fastened to "
    "the wood, body hanging,",
    "both arms outstretched, a single large iron nail driven straight through "
    "the centre of EACH wrist, the dark round nail head flush against the "
    "skin on the front of each wrist, blood only at the small nail wound "
    "itself -- absolutely NOT rope, NOT cord, NOT cloth wrapping, NOT a "
    "bandage, wrists NOT bound or tied with any material, the nail alone "
    "fastens each wrist to the wood -- body hanging,"
)
s25["subject_block"] = sb25

# #27 -- bite-wound marks only, never a living snake still on the body
s27 = by_id[27]
s27["subject_block"] = s27["subject_block"].replace(
    "while the unhealed serpent-bites still mark their arms;",
    "while their arms still show only small red puncture-wound bite MARKS or "
    "scars -- absolutely NO snakes, NO snake creatures, NO coiled or living "
    "serpents on, wrapped around, or attached to anyone's arms or body "
    "anywhere in the frame, the snakes themselves are gone, only the wound "
    "marks remain;"
)

p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print("patched subject_block for scenes 5, 8, 10, 20, 24, 25, 27")

OUT = p.parent
REROLL_FILES = [
    "05_they_beg_moses_take_the_serpents_away.png",
    "08_raised.png",
    "10_and_moses_made_a_serpent_of_brass_the_camp_looks.png",
    "20_whosoever.png",
    "24_trust.png",
    "25_we_are_all_bitten__the_cure_outside_us.png",
    "27_outward.png",
]
for fn in REROLL_FILES:
    fp = OUT / fn
    if fp.exists():
        fp.unlink()
        print(f"deleted {fp.name} for reroll")
