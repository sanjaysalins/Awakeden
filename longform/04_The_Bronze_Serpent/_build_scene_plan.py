"""Author the 16:9 long-form scene_plan.json for #04 The Bronze Serpent.

21 scenes across the 7 movements (M1:3 M2:2 M3:5 M4:4 M5:3 M6:1 M7:3), content-
matched to the narration sequence (windows are proportional tiles; the assembler
re-times against the forced whisper alignment). Baroque oil, veo3 atmospheric motion.
Hero = S21 (the risen Christ lifted up, gospel-pivot close).

DESIGN-FOR-THE-ANIMATION (the whole point — cut #03's ~10 redos):
  * the BRONZE SERPENT is a STILL cast-metal sculpture, never a living/moving snake
    (veo animates living things -> morph). It is the inert subject; only dust/heat/
    light move around it.
  * LIVE desert serpents (M1/M2) stay peripheral + in shadow; the drama is the
    stricken PEOPLE, not snake action.
  * every cross is ROBED at the waist (veo NSFW-safe -> no Kling fallback needed),
    correct hanging crucifixion pose, hands anatomically correct (five fingers).
  * NO legible text anywhere (no Hebrew on poles/scrolls); period-locked
    (Bronze-Age wilderness ~1400 BC for Numbers; 1st-century Judea for Nicodemus/cross).
  * `atmos` describes ONLY ambient motion (heat-shimmer, dust, lamp-flicker, cloth
    stir, light breathing). NEVER subject motion. boomerang scenes use a LOCKED
    camera (a push boomeranged = zoom yo-yo); one-way pushes are FORWARD_SLOW.
"""
import json
from pathlib import Path

V1 = Path(__file__).resolve().parent / "v1"
OUT = V1 / "visual_16x9"

STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and Rembrandt lighting, "
              "deep shadow and warm golden light, reverent sacred art, muted earth tones, "
              "fine visible brushwork")
STYLE_TAIL = ("no text, no legible writing, no modern or medieval or European dress (no tailored "
              "jackets, collars, buttons, lapels, hoods, pinafores), no modern tools, authentic "
              "ancient biblical-period setting and clothing, cinematic 16:9 widescreen composition")
OPEN = "a single seamless full-bleed Baroque oil painting, hard Caravaggio chiaroscuro"
CLOSE = "one continuous image, no frame, no panels, no border, no text"

# Reusable, carefully-guarded motifs ------------------------------------------------
WILD = ("Bronze-Age Israelite wilderness camp (~1400 BC) of goat-hair tents in a sun-baked desert "
        "of rock and dust, people in simple undyed handwoven wool tunics and rough mantles, "
        "bare-headed or in plain cloth head-cloths, NO modern NO medieval NO European dress")
# the bronze serpent = an INERT metal sculpture, never a live snake (veo must not animate it)
BRONZE = ("a STILL cast-bronze serpent sculpture — gleaming lifeless polished bronze metal coiled "
          "and fixed at the top of a tall rough wooden pole, plainly an inert metal artifact, "
          "NOT a living snake, NOT writhing, NOT moving")
# live serpents kept peripheral, never the animated focus
LIVESNAKE = ("a few coppery-red desert serpents low among the rocks half-lost in shadow, kept small "
             "and peripheral, NOT a writhing mass and NOT the focus")
ROBEDCROSS = ("the robed Christ CRUCIFIED — both arms outstretched and NAILED to the crossbeam, "
              "wrists fastened to the wood, body hanging, head bowed, NOT standing NOT leaning on "
              "the cross, robed at the waist NOT bare, hands anatomically correct with five fingers")

# (id, mvt, [t0,t1], title, subject_block, sfx, camera, atmos, jesus, jesus_variant, directional)
S = [
 # ---- M1 The Picture ----
 (1, "M1 The Picture", [0.0, 30.0], "A whole camp dying of snakebite (hook)",
  f"{OPEN}, WIDE desolate tableau: a {WILD} at harsh noon, several Israelites fallen and stricken on "
  f"the hot ground among the tents, others kneeling over them in dread and grief, {LIVESNAKE}; the "
  f"mood plague-stricken and hopeless under a vast bleached sky, restrained NOT gory, {CLOSE}",
  "wind_desert_dry + distant_moan_low", "locked, faint drift",
  "heat-shimmer rising off the rock, fine dust drifting on the wind, tent cloth and robes stirring faintly", False, None, False),

 (2, "M1 The Picture", [30.0, 55.0], "Worn down, they despise the bread of heaven",
  f"{OPEN}, DEEP unified composition: in the warm foreground a weary {WILD}, gaunt faces hard with "
  f"bitterness, a man turning away in contempt from pale flakes of manna scattered on the ground at "
  f"dawn; in the midground the long dusty caravan of the wilderness journey trailing back toward "
  f"distant barren hills; tents, water-skins and woven baskets around them; weary and resentful, {CLOSE}",
  "wind_desert_dry + camp_murmur_faint", "locked, faint drift",
  "dawn light strengthening over the dust, manna flakes and robes stirring in a thin breeze, heat-haze", False, None, False),

 (3, "M1 The Picture", [55.0, 79.4], "The LORD sent fiery serpents — and people died",
  f"{OPEN}, ominous and weighty, restrained NOT gory: dusk falling over the {WILD}, the ground itself "
  f"seeming to turn against them — {LIVESNAKE} emerging from the rocks and tent-shadows, people drawing "
  f"back in terror, one figure sinking to the sand clutching a bitten foot; cold blue shadow against the "
  f"last red light, dread and judgment, {CLOSE}",
  "wind_desert_dry + low_rumble_sub", "locked, slow breathing drift",
  "the last red light fading, dust and sand sifting in the wind, robes and tent cloth stirring", False, None, False),

 # ---- M2 The Problem ----
 (4, "M2 The Problem", [79.4, 89.3], "The venom is already inside",
  f"{OPEN}, intimate close composition: a single bitten Israelite man lying in lamplit shadow inside a "
  f"goat-hair tent, his face pale and sweat-sheened, one hand pressed to the dark swollen serpent-bite "
  f"on his arm, his eyes open and afraid — the poison already in his blood, nothing he can do to stop it; "
  f"undyed wool tunic, NO modern dress, deep Rembrandt shadow, tender and grave, {CLOSE}",
  "tent_wind_low + breath_shallow", "locked, faint breathing drift",
  "the low lamp flame wavering over his face, a thread of smoke rising, the tent cloth breathing in the wind", False, None, False),

 (5, "M2 The Problem", [89.3, 99.2], "They beg Moses: take the serpents away",
  f"{OPEN}, DEEP composition: a crowd of desperate {WILD} pressing toward Moses, a bearded elder in a "
  f"plain mantle, their hands outstretched in pleading and confession, faces upturned and stricken; behind "
  f"them the stricken camp in shadow; Moses listening grave and still; the people begging for the snakes to "
  f"be taken away, reverent and urgent, {CLOSE}",
  "crowd_plead_soft + wind_desert_dry", "locked, faint drift",
  "dust drifting through a shaft of hard light, robes and mantles stirring, heat-haze rising", False, None, False),

 # ---- M3 The Strange Detail ----
 (6, "M3 The Strange Detail", [99.2, 120.6], "God does not do what they asked",
  f"{OPEN}, solemn and hushed: Moses alone kneeling in a pool of pale light on the desert floor at the edge "
  f"of the {WILD}, head lifted as if listening, a great stillness and a strange holy weight around him, the "
  f"camp dim and waiting behind; the command not yet seen, only awaited; reverent, expectant, {CLOSE}",
  "wind_desert_low + drone_holy_faint", "locked, faint breathing drift",
  "a shaft of pale light strengthening on Moses, fine dust adrift, his mantle stirring faintly", False, None, False),

 (7, "M3 The Strange Detail", [120.6, 142.0], "Make a fiery serpent, set it on a pole",
  f"{OPEN}, close and weighty, firelit: at a low forge-fire in the desert night Moses' weathered hands lifting "
  f"{BRONZE} — the freshly cast metal serpent gleaming dull gold in the firelight as it is bound to the head of "
  f"the wooden pole; the cure being shaped in the very image of the curse; deep shadow, undyed wool sleeves, "
  f"reverent and strange, {CLOSE}",
  "forge_fire_low + hammer_faint", "locked, faint breathing drift",
  "the forge-fire glowing and pulsing warm over the bronze, embers and smoke rising, the still metal catching the light", False, None, False),

 (8, "M3 The Strange Detail", [142.0, 163.4], "The serpent lifted up on the pole (signature)",
  f"{OPEN}, WIDE awe-struck tableau, the raised pole the heart of the frame: {BRONZE} raised HIGH against a vast "
  f"open desert sky at golden hour, the tall pole standing over the {WILD}, the gleaming bronze serpent "
  f"silhouetted and catching the low gold light; small dim figures of the stricken below at the foot of the "
  f"pole; the one thing lifted up for all to see, reverent and arresting, {CLOSE}",
  "wind_open_desert + drone_holy_low", "very slow push UP toward the lifted bronze serpent",
  "heat-haze and dust rising past the still bronze, low cloud drifting behind the pole, robes stirring far below — the bronze serpent itself perfectly still", False, None, True),

 (9, "M3 The Strange Detail", [163.4, 184.8], "Look, and live — a dying man lifts his eyes",
  f"{OPEN}, intimate and decisive: a bitten Israelite collapsed on the desert ground in the foreground, weak "
  f"and dying, slowly lifting his face and eyes UPWARD toward the off-frame lifted pole, one shaft of gold light "
  f"falling on his upturned face the instant he looks; the cure costing him nothing but the turn of his eyes; "
  f"undyed wool, deep shadow, tender and urgent, {CLOSE}",
  "wind_desert_low + breath_relief_faint", "very slow push toward the upturned face",
  "the shaft of light strengthening on his face, fine dust drifting up through the beam, his mantle stirring", False, None, True),

 (10, "M3 The Strange Detail", [184.8, 206.2], "And Moses made a serpent of brass (the camp looks)",
  f"{OPEN}, DEEP unified composition: across the whole {WILD} at golden hour, scattered stricken people all "
  f"turning and lifting their eyes toward the distant raised pole bearing {BRONZE}; some rising restored, some "
  f"still reaching from the ground, the lifted bronze small but luminous in the far midground; one nation of the "
  f"dying turning to look; reverent, hopeful, {CLOSE}",
  "wind_open_desert + crowd_soft", "locked, slow drift",
  "golden dusk light deepening, dust and heat-haze drifting across the camp, robes and tents stirring in the wind", False, None, False),

 # ---- M4 The Centuries-Early Match ----
 (11, "M4 The Centuries-Early Match", [206.2, 233.7], "Nicodemus comes to Jesus by night",
  f"{OPEN}, intimate first-century Judea night interior: the living robed Christ seated in warm lamplight in "
  f"quiet conversation with Nicodemus, an older bearded Pharisee in a plain mantle leaning in to listen; a single "
  f"clay oil lamp between them, deep shadow all around, the city dark beyond a low stone window; reverent, "
  f"searching, intimate, {CLOSE}",
  "night_low + lamp_flame_soft", "locked, faint breathing drift",
  "the oil lamp flame wavering between them, a thin thread of smoke rising, shadows breathing on the stone wall", True, "ministry", False),

 (12, "M4 The Centuries-Early Match", [233.7, 261.2], "Even so must the Son of man be lifted up",
  f"{OPEN}, DEEP unified echo composition: on one side, half in shadow, {BRONZE} on its pole against a desert sky; "
  f"on the other, lit by warm light, {ROBEDCROSS} against a darkening sky — the tall pole and the upright of the "
  f"cross quietly rhyming, the serpent lifted up a thousand years before the Son of man lifted up; a serene "
  f"reverent visual rhyme, {CLOSE}",
  "wind_low + choir_distant_faint", "locked, slow drift",
  "warm light pulsing across the cross, heat-haze drifting past the still bronze, slow cloud, dust motes adrift", True, "passion", False),

 (13, "M4 The Centuries-Early Match", [261.2, 288.7], "Lifted up — signifying what death He should die",
  f"{OPEN}, restrained WIDE cinematic tableau, NO foreground portrait: a hill outside the walls of first-century "
  f"Jerusalem at the ninth hour seen wide and distant, {ROBEDCROSS} on the central cross on the crest as the "
  f"dominant subject, silhouetted against a vast bruised darkening sky, cold shafts of storm-light breaking "
  f"through cloud, the city dim below; sombre, reverent, {CLOSE}",
  "wind_desolate + distant_city_low", "very slow push toward the cross on the crest",
  "storm cloud rolling slowly behind the cross, shafts of light shifting, dust and cold mist adrift", True, "passion", True),

 (14, "M4 The Centuries-Early Match", [288.7, 316.4], "For God so loved the world",
  f"{OPEN}, luminous and tender, WIDE cinematic tableau, NO foreground figure NO portrait NO close-up person: a "
  f"vast darkened world at the ninth hour — open wilderness and a distant first-century city under a great "
  f"storm-dark sky — with broad warm shafts of golden light breaking through the heavy clouds and pouring down "
  f"across the whole land onto a small distant cross on its far hill, the darkness giving way to a deep tender "
  f"radiance, the love of God breaking over the whole world; reverent, hopeful, deep Rembrandt shadow at the "
  f"edges, {CLOSE}",
  "light_swell_low + choir_warm_soft", "very slow push into the breaking light",
  "the shafts of golden light strengthening and breathing, fine dust drifting up through the beams, slow cloud", True, "passion", True),

 # ---- M5 The Honest Objection ----
 (15, "M5 The Honest Objection", [316.4, 350.2], "Hezekiah breaks the brazen serpent",
  f"{OPEN}, weighty and resolute, first-century-earlier ancient Judah: a godly bearded king in a plain robe "
  f"swinging a heavy stone maul to STRIKE and shatter an old bronze serpent-on-a-pole idol in a dim temple "
  f"court, fragments of broken bronze flying, a thin haze of incense the people had wrongly burned to it drifting "
  f"in the shadow; NO legible text anywhere; the relic smashed so none mistake the sign for the Saviour, {CLOSE}",
  "stone_strike + incense_hiss_faint", "locked, faint drift",
  "incense smoke drifting and curling in the shafts of light, dust hanging in the air, a brazier flame wavering", False, None, False),

 (16, "M5 The Honest Objection", [350.2, 384.0], "The likeness of the curse, lifted up",
  f"{OPEN}, DEEP unified composition holding the two together: half in shadow {BRONZE} on its desert pole — the "
  f"likeness of the very thing that was killing them; lit on the other side {ROBEDCROSS}, the One made a curse in "
  f"our place hanging on the tree; the same shape lifted up, the serpent-image and the sinless Son in solemn "
  f"rhyme; reverent, grave, worshipful, {CLOSE}",
  "wind_low + drone_holy_faint", "locked, slow drift",
  "warm light pulsing across the cross, heat-haze past the still bronze, dust and slow cloud drifting", True, "passion", False),

 (17, "M5 The Honest Objection", [384.0, 417.9], "Made a curse for us — on the tree",
  f"{OPEN}, sombre and worshipful, three-quarter view: {ROBEDCROSS} seen against a vast dark sky, one shaft of "
  f"warm light breaking across the bowed head and the nailed outstretched arms, the curse of the law fallen "
  f"wholly on the lifted sinless One; deep Rembrandt shadow, reverent, restrained NOT graphic, {CLOSE}",
  "wind_low + choir_distant_faint", "locked, faint breathing drift",
  "warm light pulsing across the figure and the shadow, robes and dust stirring gently, slow cloud", True, "passion", False),

 # ---- M6 The Exchange ----
 (18, "M6 The Exchange", [417.9, 429.8], "The curse fell on the lifted One",
  f"{OPEN}, intimate and grave, DEEP composition: in the foreground a bitten dying Israelite on the desert "
  f"ground lifting his eyes; far beyond and above him, luminous against the dark, {ROBEDCROSS} — the curse the "
  f"man could never neutralise fallen instead on the lifted Son, the cure entirely outside the dying man; tender, "
  f"weighty, the exchange made plain, {CLOSE}",
  "low_drone + choir_distant_faint", "very slow push toward the lifted Christ",
  "warm light strengthening on the distant cross, dust drifting up through the light, the man's mantle stirring", True, "passion", True),

 # ---- M7 The Invitation ----
 (19, "M7 The Invitation", [429.8, 442.4], "The cure was a look",
  f"{OPEN}, intimate and kind: a weak dying Israelite, too weak to stand, lying back on the desert ground and "
  f"simply lifting his eyes upward into a breaking shaft of warm light, his weathered face filling with relief — "
  f"the one thing a dying man can still do; undyed wool, deep shadow giving way to light, tender and hopeful, {CLOSE}",
  "wind_desert_low + light_swell_faint", "very slow push toward the upturned face",
  "the shaft of warm light strengthening on his face, fine dust drifting up through the beam, his robe stirring", False, None, True),

 (20, "M7 The Invitation", [442.4, 455.0], "Whosoever — a nation turns its eyes up",
  f"{OPEN}, DEEP unified composition, hopeful: across the whole {WILD} at golden hour, many different people — "
  f"young and old, strong and dying — all turning and lifting their eyes together toward the off-frame lifted "
  f"One, faces catching the warm gold light as they look; the invitation as wide as 'whosoever'; reverent, "
  f"welcoming, {CLOSE}",
  "wind_open_desert + choir_warm_soft", "locked, slow drift",
  "golden light deepening across the upturned faces, dust and heat-haze drifting, robes stirring in the wind", False, None, False),

 (21, "M7 The Invitation", [455.0, 467.6], "Look to the One lifted up (HERO close)",
  f"{OPEN}, NOT smooth modern devotional art, full-bleed close hero: the risen glorified Christ filling the frame "
  f"in warm radiant golden light, a dark-haired bearded man with a serene tender face turned toward the viewer, "
  f"reaching one open pierced hand gently forward in welcome, a clear nail-wound scar in the centre of the open "
  f"palm, the hand anatomically correct with five fingers, deep Rembrandt shadow behind; the gospel-pivot hero "
  f"image that closes the film on the One lifted up, {CLOSE}",
  "choir_warm_soft + light_swell_low", "very slow reverent push-in toward the open pierced hand",
  "the warm golden light glowing softly and steadily, the robe and hair stirring almost imperceptibly", True, "resurrection", True),
]

# ---- 6 ADDED scenes (v2: bring windows into the clean 7-22s band; long ones use a
#      monotonic forward-slow push so they extend without a yo-yo). Same guards. ----
NEW_S = [
 (22, "M3 The Strange Detail", "The cure is shaped like the curse",
  f"{OPEN}, contemplative CLOSE study, NO wide landscape NO crowd: {BRONZE} filling much of the frame, the "
  f"gleaming cast-bronze coils and the serpent's head catching a single shaft of warm gold light against deep "
  f"shadow and a dim desert sky — the strange beauty of a cure shaped in the very image of the curse; "
  f"reverent, weighty, {CLOSE}",
  "wind_open_desert + drone_holy_faint", None, False,
  "heat-haze and fine dust drifting slowly past the still bronze, the warm light gleaming and breathing across the metal — the bronze itself perfectly still"),

 (23, "M4 The Centuries-Early Match", "Not a preacher's picture — Jesus Himself",
  f"{OPEN}, intimate reverent CLOSE of the living robed Christ in warm first-century lamplight, his face calm "
  f"and certain, one open hand raised calmly near his chest in unhurried teaching — the hand anatomically "
  f"correct with exactly five natural fingers, no fused, extra, elongated or distorted fingers — his steady "
  f"eyes toward the listener, the One who Himself names the wilderness pole as a picture of His own cross; "
  f"deep Rembrandt shadow behind, NO crowd, NO text, {CLOSE}",
  "night_low + lamp_flame_soft", "ministry", True,
  "the lamplight wavering warm across his face, a thin thread of smoke rising, the shadow breathing gently behind him"),

 (24, "M5 The Honest Objection", "Looking was never magic — it was trust",
  f"{OPEN}, sober and clear, DEEP composition: in a dim ancient stone temple court the shattered fragments of "
  f"the broken bronze serpent lie scattered on the floor in shadow; above and beyond them a humble bare-headed "
  f"Israelite turns his face away from the lifeless relic and lifts his eyes UPWARD into a single shaft of pale "
  f"heavenly light — trust aimed where God told them to aim it, not at the metal; reverent, no legible text, {CLOSE}",
  "lamp_flame_soft + low_drone", None, False,
  "the shaft of light strengthening on his upturned face, fine dust and a wisp of incense smoke drifting through the beam"),

 (25, "M6 The Exchange", "We are all bitten — the cure outside us",
  f"{OPEN}, DEEP intimate composition, tender and grave: in the foreground a bitten dying Israelite on the "
  f"desert ground, weak and unable to heal himself, his hand open and empty; far beyond and above him, small "
  f"and luminous against the dark, {ROBEDCROSS} on its distant cross — the cure never inside the dying man but "
  f"hanging entirely outside him; reverent, no text, {CLOSE}",
  "low_drone + choir_distant_faint", "passion", True,
  "fine dust drifting up through a shaft of light toward the distant cross, the dying man's mantle and the desert air stirring faintly"),

 (26, "M7 The Invitation", "You do not have to climb, pay, or be strong",
  f"{OPEN}, intimate and tender, ONE single unified close-up of an open EMPTY human hand filling the frame, "
  f"NO face NO portrait NO figure: a weak open upturned human hand with nothing in it, the plain undyed cuff "
  f"of a wool robe at the wrist, lifted gently into a breaking shaft of warm gold light, the hand anatomically "
  f"correct with five fingers — nothing to offer, nothing to brew or earn, only the empty-handed reach of "
  f"faith; deep shadow, no text, {CLOSE}",
  "light_swell_low + wind_soft", None, False,
  "the shaft of warm light strengthening across the open palm, fine dust drifting up slowly through the beam"),

 (27, "M2 The Problem", "Their confession is real — but they reach outward",
  f"{OPEN}, DEEP composition, grave: a crowd of stricken {WILD} on their knees in confession, hands lifted and "
  f"reaching OUTWARD into the dark toward the edge of the camp — begging for the danger outside to be taken "
  f"away — while the unhealed serpent-bites still mark their arms; their plea aimed at their circumstances, "
  f"not the poison already within; sober, weighty, no text, {CLOSE}",
  "crowd_plead_soft + wind_night_low", None, False,
  "dust and cold night air drifting through the lamplight over the kneeling crowd, robes and raised hands stirring faintly"),
]

# Real per-turn cumulative END times (ffprobe of the rendered _turns, total 467.6s) — the
# ground truth the windows tile to. Each scene declares the turn-range it covers.
TURN_END = [16.4, 23.7, 37.5, 43.3, 45.5, 53.8, 63.5, 67.9, 73.5, 103.2, 108.0, 111.9, 121.1,
 143.9, 152.7, 156.6, 159.0, 171.5, 190.1, 203.7, 214.4, 220.0, 226.5, 227.7, 232.1, 239.2,
 243.4, 247.9, 253.0, 256.0, 270.2, 274.9, 289.9, 310.1, 315.6, 316.4, 324.0, 341.1, 354.5,
 366.1, 371.6, 376.0, 382.6, 388.6, 412.3, 436.6, 448.5, 452.4, 467.6]
AUDIO = 467.6
# scene id -> [first_turn, last_turn] (contiguous, covers turns 0..48 exactly once)
TURN_RANGE = {
 1:[0,0], 2:[1,3], 3:[4,5], 4:[6,6], 5:[7,8], 27:[9,9], 6:[10,11], 7:[12,12], 22:[13,13],
 8:[14,15], 9:[16,16], 10:[17,17], 11:[18,19], 23:[20,21], 12:[22,23], 13:[24,25], 14:[26,28],
 15:[29,31], 24:[32,32], 16:[33,35], 17:[36,37], 25:[38,39], 18:[40,42], 19:[43,44], 26:[45,45],
 20:[46,46], 21:[47,48]}
FWD_THRESHOLD = 20.0  # window > this -> forward_slow (monotonic push); else boomerang


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # normalize both lists to (id, mvt, title, subject, sfx, jesus_variant, jesus, atmos)
    rec = {}
    for (sid, mvt, _t, title, subj, sfx, _cam, atmos, jesus, jvar, _dir) in S:
        rec[sid] = (mvt, title, subj, sfx, jvar, jesus, atmos)
    for (sid, mvt, title, subj, sfx, jvar, jesus, atmos) in NEW_S:
        rec[sid] = (mvt, title, subj, sfx, jvar, jesus, atmos)

    scenes = []
    for sid, (a, b) in TURN_RANGE.items():
        start = 0.0 if a == 0 else TURN_END[a - 1]
        end = AUDIO if b == len(TURN_END) - 1 else TURN_END[b]
        win = end - start
        mvt, title, subj, sfx, jvar, jesus, atmos = rec[sid]
        fill = "forward_slow" if win > FWD_THRESHOLD else "boomerang"
        camera = "a very slow, steady cinematic push-in" if fill == "forward_slow" else "locked, the faintest breathing drift"
        directional = (fill == "forward_slow")
        scenes.append({"id": sid, "mvt": mvt, "t": [round(start, 1), round(end, 1)], "title": title,
                       "subject_block": subj, "sfx": sfx, "camera": camera, "atmos": atmos,
                       "fill": fill, "jesus": jesus, "jesus_variant": jvar, "directional": directional,
                       "window_s": round(win, 1)})
    scenes.sort(key=lambda s: s["t"][0])
    plan = {
        "format": "16:9 long-form deep-dive",
        "episode": "The Bronze Serpent — Numbers 21 fulfilled in Christ (John 3:14)",
        "audio": "narration.mp3 — 467.6s (natural pace, 4-voice); scene t[] tile the turn timeline",
        "image_provider": "nbp (Nano Banana Pro, Baroque oil)",
        "animation": {"model": "veo3_1_lite", "aspect": "16:9", "duration": 8,
                      "note": "all crosses robed -> veo NSFW-safe; bronze serpent is STILL metal (never animate it)"},
        "fill_design": ("ANIMATION-AWARE: the bronze serpent + every subject are FROZEN; only ambient "
                        "(heat/dust/light/cloth) moves. boomerang scenes use a LOCKED camera; one-way "
                        "pushes are forward_slow so they never reverse."),
        "style_base": STYLE_BASE,
        "rule": ("the device is ONE thing lifted up: the bronze serpent raised on a pole (the likeness of "
                 "the curse, look-and-live) is fulfilled in the Son of man lifted up on the cross (John 3:14); "
                 "every quote's visual matches its narration cue; the cut CLOSES on the risen Christ (hero S21)."),
        "film_name": "Bronze_Serpent_16x9.mp4",
        "style_tail": STYLE_TAIL,
        "scenes": scenes,
    }
    (OUT / "scene_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n",
                                         encoding="utf-8")
    # --- deterministic self-checks (LF-SP guardrails) ---
    from collections import Counter
    mv = Counter(s["mvt"].split()[0] for s in scenes)
    assert all(mv[f"M{i}"] >= 1 for i in range(1, 8)), f"movement coverage FAIL: {mv}"
    assert all(mv[f"M{i}"] >= 2 for i in (1, 3, 4, 5)), f"key movements thin: {mv}"
    assert any(s["jesus"] for s in scenes), "no Jesus/NT-link scene"
    assert scenes[-1]["jesus"] and scenes[-1]["jesus_variant"] == "resurrection", "hero must close on risen Christ"
    assert all(s["atmos"] for s in scenes), "every scene needs an atmospheric element"
    n_unified = sum(1 for s in scenes if "unified" in s["subject_block"].lower())
    assert n_unified >= 2, f"need >=2 unified multi-vignette scenes, have {n_unified}"
    # no legible text anywhere; any 'serpent' subject must be the STILL bronze OR peripheral live snake
    for s in scenes:
        b = s["subject_block"].lower()
        assert "no text" in b or "no legible text" in b, f"scene {s['id']} missing no-text guard"
    # bronze-serpent scenes must mark it inert (never-animate)
    for s in scenes:
        b = s["subject_block"].lower()
        if "cast-bronze serpent" in b:
            assert "not a living snake" in b and "not moving" in b, f"scene {s['id']} bronze not marked inert"
    # contiguous tiling 0 -> ~467.6
    for a, b in zip(scenes, scenes[1:]):
        assert abs(a["t"][1] - b["t"][0]) < 0.05, f"gap between {a['id']} and {b['id']}"
    assert abs(scenes[0]["t"][0]) < 0.05 and abs(scenes[-1]["t"][1] - 467.6) < 0.3
    assert "biblical-period" in plan["style_tail"], "style_tail missing the biblical-period guard"
    jn = sum(1 for s in scenes if s["jesus"])
    fwd = sorted(s["id"] for s in scenes if s["fill"] == "forward_slow")
    maxwin = max(s["window_s"] for s in scenes)
    print(f"[ok] scene_plan.json — {len(scenes)} scenes, movements {dict(mv)}")
    print(f"[ok] unified={n_unified}  jesus={jn}  forward_slow({len(fwd)})={fwd}  hero=S{scenes[-1]['id']} (resurrection)")
    print(f"[ok] tiling contiguous 0.0 -> {scenes[-1]['t'][1]}s · max window {maxwin}s")


if __name__ == "__main__":
    main()
