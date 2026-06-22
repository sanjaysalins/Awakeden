"""Author the 16:9 long-form scene_plan.json for #03 The Passover Lamb.

25 scenes, content-matched to the forced turn timeline (see _movement_windows.json),
all 7 movements covered (M1:3 M2:2 M3:5 M4:4 M5:3 M6:3 M7:5). Baroque oil, veo3
atmospheric motion. Hero = S25 (the risen Christ, gospel-pivot close).

Style/format mirror Psalm 22 (the "absolutely stunning" build). Period: Bronze-Age
Egypt/Israel (~1400 BC) for the Exodus scenes, 1st-century Judea for the cross.
No legible text (scrolls = faint illegible marks). Robed Christ (veo NSFW-safe).
"""
import json
from pathlib import Path

V1 = Path(__file__).resolve().parent / "v1"
OUT = V1 / "visual_16x9"

STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and Rembrandt lighting, "
              "deep shadow and warm golden light, reverent sacred art, muted earth tones, "
              "fine visible brushwork")
STYLE_TAIL = ("no text, no modern or medieval or European dress (no tailored jackets, collars, "
              "buttons, lapels, hoods, pinafores), no iron stoves or modern tools, authentic "
              "ancient biblical-period setting and clothing, cinematic 16:9 widescreen composition")
OPEN = "a single seamless full-bleed Baroque oil painting, hard Caravaggio chiaroscuro"
CLOSE = "one continuous image, no frame, no panels, no border, no text"

# (id, mvt, [t0,t1], title, subject_block, sfx, camera, atmos, fill, jesus, jesus_variant, directional)
S = [
 (1, "M1 The Picture", [0.0, 13.4], "The over-specified instructions (foreshadow)",
  f"{OPEN}, DEEP layered composition centred on a low guttering clay oil lamp and an aged Israelite scribe's weathered hand resting still beside it; an unrolled parchment lies mostly in shadow at the edge, its marks only a faint illegible texture, never the focus; in the far shadowed background, almost unnoticed, a plain wooden doorway of two uprights and a beam catching one thin shaft of pale light; the whole image hushed and expectant, {CLOSE}",
  "parchment_rustle + lamp_flame_soft", "locked, the faintest breathing drift",
  "the lamp flame guttering, a thread of smoke rising, dust motes adrift in the light", "boomerang", False, None, False),

 (2, "M1 The Picture", [13.4, 33.9], "The last night in Egypt — kill a lamb",
  f"{OPEN}, DEEP unified composition dominated by the intimate foreground: a poor Israelite family in simple linen close and large in warm lamplight, the father gently holding a young spotless lamb as the children watch, faces tender and grave; the low mud-brick doorway of their house just behind them; only a small distant glimpse of the dark Egyptian city far beyond through the doorway, kept tiny and faint; reverent and intimate, {CLOSE}",
  "wind_night_low + distant_murmur", "locked, faint drift",
  "night air stirring the lamp and the family's robes, the lamb's slow breathing, drifting dust", "boomerang", False, None, False),

 (3, "M1 The Picture", [33.9, 53.2], "One lamb, described before a firstborn died",
  f"{OPEN}, intimate close composition: an ancient Israelite shepherd-father, a bearded man in a simple ankle-length undyed handwoven wool tunic with a plain rectangular mantle over one shoulder and a cloth belt, bare-headed, NO hood NO collar NO modern clothing, cradling a single flawless white lamb against deep Rembrandt shadow, one warm shaft of golden lamplight falling across the lamb's clean unblemished wool and the man's tender weathered face, the lamb calm and unafraid, quiet and weighty as though the animal were a portrait of someone yet to come, {CLOSE}",
  "lamb_soft + lamp_flame_soft", "locked, the faintest breathing drift",
  "lamplight flickering warm across the wool, soft dust motes, the lamb's breath gently moving", "boomerang", False, None, False),

 (4, "M2 The Problem", [53.2, 78.0], "I will pass through — death over Egypt",
  f"{OPEN}, vast and ominous yet restrained NOT graphic: a great cold shadow sweeping low over the moonlit rooftops of an ancient Egyptian city at the dead of midnight, pale silver moonlight raking the flat mud-brick roofs and silent streets, a sense of unseen judgment moving across every house, deep blue-black darkness, no visible figures of horror, only weight and dread and stillness, {CLOSE}",
  "wind_desolate + rumble_deep_sub", "locked, slow breathing drift",
  "thin cloud sliding across the moon, cold mist creeping low over the rooftops, faint dust", "boomerang", False, None, False),

 (5, "M2 The Problem", [78.0, 102.9], "Only a blood-marked door turns death aside",
  f"{OPEN}, DEEP composition, the threshold the heart of the frame: a humble ancient doorway at night, two side posts and an upper beam, a father's hand reaching up with a bunch of hyssop to strike dark blood across the wood; warm safe lamplight glowing within the house behind him where his family waits; beyond the door a cold dark street under judgment; the marked doorway the one line between life and death, {CLOSE}",
  "wind_night_low + cloth_rustle", "slow push toward the doorway",
  "the interior lamplight wavering, the hyssop and cloak stirring, a wisp of smoke", "directional", False, None, True),

 (6, "M3 The Strange Detail", [102.9, 121.6], "Without blemish — the flawless one chosen",
  f"{OPEN}, pastoral but solemn: at dawn an ancient Israelite shepherd, a bearded man in a simple ankle-length undyed handwoven wool tunic and a rough rectangular mantle over one shoulder with a plain cloth belt, bare-headed, NO tailored jacket NO collar NO buckled satchel NO modern clothing, gently lifting and inspecting a single spotless young male lamb from among a dim huddled flock in a rough stone fold, his hands deliberate as he checks it for any flaw, one shaft of pale gold morning light singling out the chosen lamb's clean white wool against the shadowed others, reverent and tender, {CLOSE}",
  "flock_soft + dawn_birds_faint", "locked, faint drift",
  "soft dawn light strengthening, breath and dust in the cold air, wool and straw stirring", "boomerang", False, None, False),

 (7, "M3 The Strange Detail", [121.6, 146.4], "Kept four days, lived with, found faultless",
  f"{OPEN}, DEEP unified ancient-Israelite domestic interior, a humble Bronze-Age dwelling of rough mud-brick walls lit by small clay oil lamps: in the warm foreground the spotless lamb lying among the family's young children who watch over it, the children in simple undyed linen tunics; in the midground the mother in a plain ankle-length tunic and a cloth head-covering kneeling beside a low clay oven with earthenware jars and woven baskets nearby; faint scored tally-marks on the mud wall counting the passing days; NO European cottage NO iron stove or skillet NO modern dress; tender and intimate, {CLOSE}",
  "hearth_fire_soft + children_faint", "locked, faint breathing drift",
  "hearth flames flickering warm, lamp smoke rising, the lamb's slow breathing, dust in the light", "boomerang", False, None, False),

 (8, "M3 The Strange Detail", [146.4, 167.6], "The whole nation at the same twilight",
  f"{OPEN}, vast unified twilight composition: a wide elevated view over a whole ancient Israelite quarter at the same blood-orange dusk, countless low rooftops and lamplit doorways receding into the haze, a faint figure at each distant threshold at the very same appointed hour, smoke of many fires rising together into the deepening sky, a sense of one nation acting as one, {CLOSE}",
  "evening_wind + distant_crowd_soft", "locked, slow drift",
  "dusk light deepening, many threads of smoke rising and bending, slow low cloud", "boomerang", False, None, False),

 (9, "M3 The Strange Detail", [167.6, 191.7], "Blood struck on the two posts and the beam",
  f"{OPEN}, stark and close: a single ancient doorway of bare timber filling the frame at night, two upright posts and one heavy beam across the top, fresh dark blood roughly daubed and smeared with a bunch of hyssop across both posts and the upper beam, irregular streaks and drips running down the rough grain, NO cross shapes NO symbols NO neat marks — only rough thrown blood, one low warm clay oil lamp throwing the timber and the wet blood into sharp relief, deep shadow all around, hushed and weighty, {CLOSE}",
  "lamp_flame_soft + wind_night_low", "very slow push onto the doorframe",
  "lamplight wavering across the wet blood and grain, a thread of smoke, faint dust", "directional", False, None, True),

 (10, "M3 The Strange Detail", [191.7, 213.9], "Not one bone broken — when I see the blood",
  f"{OPEN}, solemn still-life composition: a whole roasted Passover lamb laid out unbroken on a plain wooden board in warm lamplight, entirely intact with not a single bone broken, bitter herbs and unleavened bread beside it, and beyond the low table the blood-marked doorframe just visible in the shadow; reverent, weighty, the centre of the night, {CLOSE}",
  "hearth_embers + lamp_flame_soft", "locked, faint breathing drift",
  "embers glowing and fading, lamp smoke curling, warm light pulsing gently", "boomerang", False, None, False),

 (11, "M4 The Centuries-Early Match", [213.9, 240.7], "Fourteen centuries later — the Passover cross",
  f"{OPEN}, restrained NOT graphic, WIDE cinematic tableau, NO foreground portrait NO standing figure: a hill outside the walls of first-century Jerusalem at the ninth hour seen wide and distant, three crosses on the crest in silhouette against a bruised darkening sky as the dominant subject, the central cross bearing a small distant crucified robed figure, the holy city spread below with the smoke of countless Passover sacrifices rising from the temple, cold shafts of storm-light breaking through cloud, reverent and sombre, {CLOSE}",
  "wind_desolate + distant_temple_low", "locked, slow drift",
  "storm cloud rolling, temple smoke rising far below, shafts of light shifting, dust adrift", "boomerang", True, None, False),

 (12, "M4 The Centuries-Early Match", [240.7, 256.7], "They brake not his legs",
  f"{OPEN}, reverent and restrained: at the foot of the cross Roman soldiers in 1st-century iron and leather pausing before the central robed crucified figure, having just broken the legs of the two beside him, now staying their hand at the third because he is already dead, the moment hushed and strange, cold light on the soldiers' armour, the central figure serene in death, robed at the waist NOT bare, {CLOSE}",
  "wind_low + armor_clink_faint", "locked, faint drift",
  "cold wind stirring cloaks and a soldier's plume, thin cloud, dust in the shaft of light", "boomerang", True, "passion", False),

 (13, "M4 The Centuries-Early Match", [256.7, 282.0], "Christ our passover — the same frame of wood",
  f"{OPEN}, DEEP unified echo composition: on one side, half in shadow, an ancient blood-marked Israelite doorway — two upright wooden posts and a beam across the top; on the other, lit by warm light, the robed crucified Christ on the wooden cross — its upright and crossbeam quietly rhyming with the doorway's posts and beam, the same frame of bloodied wood a thousand years apart; a serene reverent visual rhyme, the Lamb of God, {CLOSE}",
  "wind_low + choir_distant_faint", "locked, slow drift",
  "warm light pulsing across the cross, faint smoke, slow cloud, dust motes drifting", "boomerang", True, "passion", False),

 (14, "M4 The Centuries-Early Match", [282.0, 304.2], "Found faultless, killed anyway",
  f"{OPEN}, tense and weighty: the robed Christ standing bound and silent before Pilate in a cold stone Roman hall, the Roman governor turning aside with a troubled gesture as if to say he finds no fault in him, hard side-light falling on Christ's calm unblemished face, deep shadow and a few watching figures behind, reverent and grave, {CLOSE}",
  "hall_echo_low + crowd_murmur_faint", "locked, faint drift",
  "a brazier flame flickering, cold light shifting, robes stirring faintly, dust in the air", "boomerang", True, "passion", False),

 (15, "M5 The Honest Objection", [304.2, 317.3], "Be fair to the doubt",
  f"{OPEN}, sober and searching: a solitary figure seated alone in deep shadow, head bowed into one hand in honest unresolved doubt, lit by a single low lamp; around him, dim and receding into the dark, the faint half-seen shapes of many different ancient cultures' stone sacrificial altars — the objection that every people killed animals — pressing in as unanswered questions; nothing written anywhere in view, only the weight of a hard honest question, {CLOSE}",
  "lamp_flame_soft + low_drone", "locked, faint breathing drift",
  "lamp flame wavering, smoke rising, the shadows and dust stirring gently", "boomerang", False, None, False),

 (16, "M5 The Honest Objection", [317.3, 341.0], "Weigh the details — strongest first",
  f"{OPEN}, symbolic DEEP composition: a balanced set of old bronze scales in warm lamplight, on one pan a small carved lamb and on the other a single iron nail, held in even weight; behind, dim and layered, a row of moon-phase discs (no numerals, no writing) and a shadowed blood-marked doorway receding into the dark; the convergence of many threads quietly resolving, reverent and contemplative, {CLOSE}",
  "lamp_flame_soft + low_drone", "locked, slow drift",
  "lamplight pulsing, the scales barely settling, smoke and dust adrift", "boomerang", False, None, False),

 (17, "M5 The Honest Objection", [341.0, 365.3], "A design stepping into the light",
  f"{OPEN}, luminous and resolving, NOT a doorway: broad warm shafts of golden dawn light breaking at a low angle through a dim ancient stone hall, sweeping across drifting dust to reveal a quiet still-life half-hidden in the shadow — a spotless lamb and a single nail lying together on stone — a long-hidden design at last stepping into the open, reverent, hopeful, {CLOSE}",
  "wind_soft + light_swell_low", "very slow push into the light",
  "the shafts of light strengthening and breathing, fine dust drifting through the beams", "directional", False, None, True),

 (18, "M6 The Exchange", [365.3, 382.3], "A life for a life — the lamb instead",
  f"{OPEN}, DEEP unified composition, tender and grave: in the warm foreground a slain Passover lamb lying still on the stone threshold; just behind it a young firstborn child sleeping safe and unharmed in lamplight in the mother's arms; the blood-marked doorframe above them; the exchange made plain — the lamb in the child's place, death already fallen on the substitute, {CLOSE}",
  "lamp_flame_soft + heartbeat_low", "locked, faint breathing drift",
  "lamplight wavering warm, the child's slow breathing, a thread of smoke, dust in the light", "boomerang", False, None, False),

 (19, "M6 The Exchange", [382.3, 393.1], "That is the cross — the substitute given",
  f"{OPEN}, reverent and clear: the robed Christ CRUCIFIED — both arms outstretched and NAILED to the crossbeam, wrists fastened to the wood, his body hanging on the cross, head bowed, NOT standing, NOT leaning on or embracing the cross; seen three-quarter against a vast dark sky, one shaft of warm light breaking across him, given by the Father as the substitute in the sinner's place, sombre and worshipful, deep Rembrandt shadow, robed at the waist NOT bare, {CLOSE}",
  "wind_low + choir_distant_faint", "locked, faint breathing drift",
  "warm light pulsing across the figure and shadow, robes and dust stirring gently", "boomerang", True, "passion", False),

 (20, "M6 The Exchange", [393.1, 414.3], "The precious blood — cost everything",
  f"{OPEN}, intimate and worshipful, ONE single unified close-up of a HAND ONLY filling the frame, NO face NO portrait NO split NO diptych NO second panel: a single open human hand, palm upward in warm low light, a clear dark nail-wound through the centre of the palm, the hand anatomically correct with exactly five fingers, the cuff of a plain undyed robe at the wrist, deep shadow all around, a sense of infinite cost held out as free gift, tender and sacred, restrained NOT graphic, {CLOSE}",
  "low_drone + choir_distant_faint", "locked, faint breathing drift",
  "warm light pulsing across the wound, faint smoke, dust drifting slowly", "boomerang", False, None, False),

 (21, "M7 The Invitation", [414.3, 440.6], "It had to be applied to the door",
  f"{OPEN}, close and decisive: a hand grasping a bunch of hyssop dipped in blood, in the act of striking it across the grain of an ancient doorpost, warm lamplight on the wet red blood and the rough wood, the basin of blood waiting below no longer unused but applied, deep shadow around, weighty and personal, {CLOSE}",
  "cloth_rustle + lamp_flame_soft", "locked, faint drift",
  "lamplight flickering on the wet blood, the hyssop leaves trembling, a wisp of smoke", "boomerang", False, None, False),

 (22, "M7 The Invitation", [440.6, 456.6], "Held out to you — Christ in the open door",
  f"{OPEN}, warm and inviting, the DOORWAY the heart of the frame echoing the Passover door: the risen robed Christ standing framed within an ancient wooden doorway of two posts and a beam, behind him radiant golden light pouring out through the opening into the surrounding dark, his figure seen at a gentle distance in the lit threshold rather than close, the same frame of wood that once bore the blood now flung open in welcome, tender and personal, {CLOSE}",
  "light_swell_low + choir_warm_soft", "locked, the faintest breathing drift",
  "the warm golden light glowing softly and steadily through the doorway, the robe stirring almost imperceptibly", "boomerang", True, "resurrection", False),

 (23, "M7 The Invitation", [456.6, 477.7], "From inside the house — security outside them",
  f"{OPEN}, DEEP intimate interior composition: inside a dark Israelite house on the night of judgment, a family huddled together in a small pool of lamplight, faces neither brave nor certain, only trusting; the door before them faintly edged with the glow of the blood they cannot even see from within; their whole safety resting on the marked door outside, hushed and tender, {CLOSE}",
  "wind_night_low + heartbeat_low", "locked, faint breathing drift",
  "the lamp flame wavering over the faces, the door-glow pulsing faintly, slow drifting dust", "boomerang", False, None, False),

 (24, "M7 The Invitation", [477.7, 494.0], "When I see the blood — not yours, His",
  f"{OPEN}, luminous and resolving: an ancient doorway of two wooden posts and a beam, its blood-marked timber bathed now in strong warm golden light, the dark blood on the posts and beam glowing rich and alive, deep shadow giving way wholly to light, the gospel of Exodus made plain, reverent and hopeful, {CLOSE}",
  "light_swell_low + wind_soft", "very slow push into the light",
  "the golden light strengthening and breathing, dust drifting up through the glow", "directional", False, None, True),

 (25, "M7 The Invitation", [494.0, 509.5], "Rest under the blood of the Lamb (HERO close)",
  f"{OPEN}, NOT smooth modern devotional art, NO doorway, full-bleed close hero: the risen glorified Christ filling the frame in warm radiant golden light, a dark-haired bearded man with a serene tender face turned toward the viewer, reaching one open pierced hand gently forward in welcome, a clear nail-wound scar visible in the centre of the open palm, deep Rembrandt shadow behind, luminous and merciful, the gospel-pivot hero image that closes the film on Christ, {CLOSE}",
  "choir_warm_soft + light_swell_low", "very slow reverent push-in toward the open hand",
  "the warm golden light glowing softly and steadily, the robe and hair stirring almost imperceptibly", "directional", True, "resurrection", True),
]

# Clips whose motion is ONE-WAY (rising smoke, mist, a strike, or a camera push) — a
# boomerang would run that motion backwards (blood un-striking, pulling back from Christ),
# which reads wrong. These play FORWARD-ONLY, time-stretched to fill the window (no reverse,
# no freeze). Everything else uses boomerang (natural-speed, symmetric ambient drift).
FORWARD_SLOW_IDS = {5, 8, 9, 11, 17, 21, 24, 25}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    scenes = []
    for (sid, mvt, t, title, subj, sfx, cam, atmos, fill, jesus, jvar, directional) in S:
        if sid in FORWARD_SLOW_IDS:
            fill, directional = "forward_slow", False
        sc = {"id": sid, "mvt": mvt, "t": [round(t[0], 1), round(t[1], 1)], "title": title,
              "subject_block": subj, "sfx": sfx, "camera": cam, "atmos": atmos,
              "fill": fill, "jesus": jesus, "jesus_variant": jvar, "directional": directional}
        scenes.append(sc)
    plan = {
        "format": "16:9 long-form deep-dive",
        "episode": "The Passover Lamb — Exodus 12 fulfilled in Christ",
        "audio": "narration.mp3 — 509.5s (natural pace, 3-voice); scene t[] tile the turn timeline",
        "image_provider": "nbp (Nano Banana Pro, Baroque oil)",
        "animation": {"model": "veo3_1_lite", "aspect": "16:9", "duration": 8,
                      "note": "robed cross scenes; veo NSFW -> direct-Kling fallback"},
        "fill_design": ("ANIMATION-AWARE: windows kept <=~25s; STATIC scenes use boomerang so each still "
                        "is composed DEEP + atmosphere-dominant; long/reveal scenes marked directional."),
        "style_base": STYLE_BASE,
        "rule": ("the device is ONE portrait a thousand years apart: the Exodus lamb (spotless, inspected, "
                 "blood on a frame of wood, not one bone broken) is fulfilled at the cross; every quote's "
                 "visual matches its narration cue; the cut CLOSES on the risen Christ (hero S25)."),
        "film_name": "Passover_Lamb_16x9.mp4",
        "style_tail": STYLE_TAIL,
        "scenes": scenes,
    }
    (OUT / "scene_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n",
                                         encoding="utf-8")
    # --- deterministic self-checks (LF-SP guardrails) ---
    from collections import Counter
    mv = Counter(s["mvt"].split()[0] for s in scenes)
    assert all(mv[f"M{i}"] >= 2 for i in range(1, 8)), f"movement coverage FAIL: {mv}"
    assert any(s["jesus"] for s in scenes), "no Jesus/NT-link scene"
    assert scenes[-1]["jesus"] and scenes[-1]["jesus_variant"] == "resurrection", "hero must close on risen Christ"
    assert all(s["atmos"] for s in scenes), "every scene needs an atmospheric element"
    n_unified = sum(1 for s in scenes if "unified" in s["subject_block"].lower())
    assert n_unified >= 2, f"need >=2 unified multi-vignette scenes, have {n_unified}"
    # any scene with a scroll/parchment must mark the writing illegible (INV-17)
    for s in scenes:
        b = s["subject_block"].lower()
        if "scroll" in b or "parchment" in b or "pages" in b:
            assert "illegible" in b, f"scene {s['id']} has writing not marked illegible"
    # contiguous tiling 0 -> 509.5
    for a, b in zip(scenes, scenes[1:]):
        assert abs(a["t"][1] - b["t"][0]) < 0.05, f"gap between {a['id']} and {b['id']}"
    assert abs(scenes[0]["t"][0]) < 0.05 and abs(scenes[-1]["t"][1] - 509.5) < 0.2
    # period guard must be in the style tail (every render inherits it)
    assert "biblical-period" in plan["style_tail"], "style_tail missing the biblical-period guard"
    print(f"[ok] scene_plan.json — {len(scenes)} scenes, movements {dict(mv)}")
    print(f"[ok] unified={n_unified}  jesus={sum(1 for s in scenes if s['jesus'])}  "
          f"directional={sum(1 for s in scenes if s['directional'])}  hero=S{scenes[-1]['id']} (resurrection)")
    print(f"[ok] tiling contiguous 0.0 -> {scenes[-1]['t'][1]}s")

if __name__ == "__main__":
    main()
