"""Author the 16:9 long-form scene_plan.json for #06 The Two Goats (Day of Atonement, Lev 16).

25 scenes across the 7 movements (M1:3 M2:2 M3:3 M4:6 M5:3 M6:4 M7:4), windows tiled to the
REAL rendered turn timeline (532.6s, 3-voice; ffprobe ground truth). Baroque oil, veo3
atmospheric motion. Hero = S25 (the living/risen Christ, gospel-pivot close).

THREAD (one spine): one sin offering took TWO goats — the slain goat's blood behind the veil
(the price PAID) and the live scapegoat driven into the wilderness (the guilt CARRIED AWAY) —
both halves fulfilled once-for-all in Christ; the veil torn opens the way; come, be carried clean.

DESIGN-FOR-THE-ANIMATION (veo3 animates ambient motion, never subjects):
  * the GOATS are still/calm/standing — veo morphs live animals; never the writhing focus.
  * GOD / the divine presence is NEVER a face or figure — only the cloud of incense + warm
    radiance over the mercy seat.
  * every CROSS is the ROBED crucified Christ (waist-robed -> veo NSFW-safe), correct hanging
    pose, hands anatomically correct (five fingers). Crucifixions are VARIED (close blood-cross /
    outside-the-gate at dusk / monumental once-for-all) so no two clips repeat the same frame.
  * the CHRIST FACE is reserved for the hero close (S25) — M6's cross scenes keep the face
    bowed/shadowed to avoid near-identical face clips.
  * setting = the ANCIENT Israelite tabernacle/temple (goat-hair + dyed-linen curtains, acacia
    + gold, oil-lamp light) and 1st-century Judea — NO stone cathedral, NO medieval/European
    dress, NO modern anything. NO legible text anywhere (veil has no writing).
  * `atmos` is ONLY ambient motion (incense smoke drift, lamp/torch flame, dust motes, heat
    shimmer, cloud, cloth stir). NEVER subject motion. Almost all scenes BOOMERANG (locked cam);
    forward_slow only on S11 (scapegoat going out), S22 (carried to the horizon), S25 (hero).
"""
import json
from pathlib import Path

V1 = Path(__file__).resolve().parent / "v1"
OUT = V1 / "visual_16x9"

STYLE_BASE = ("an authentic seventeenth-century Baroque oil painting on canvas by an old master in the manner "
              "of Caravaggio, Rembrandt and Rubens — HEAVY visible impasto brushstrokes and palette-knife "
              "texture, the weave of the canvas and faint aged craquelure varnish showing through, deep "
              "tenebrist chiaroscuro, warm painted shafts of light, muted earthen oil pigments; the grand "
              "dramatic scale and composition of cinema but rendered WHOLLY as a hand-painted museum oil "
              "masterpiece, reverent sacred art")
STYLE_TAIL = ("hand-painted oil on canvas with bold visible brushwork, NOT a photograph, NOT a smooth digital "
              "render, NOT CGI, NOT glossy 3D, NOT airbrushed, no text, no legible writing, no modern or "
              "medieval or European dress (no tailored jackets, collars, buttons, lapels, hoods, pinafores), "
              "no modern tools, authentic ancient biblical-period setting and clothing, dramatic 16:9 composition")
OPEN = ("a single seamless full-bleed Baroque oil painting in the grand old-master manner, hard tenebrist "
        "Caravaggio chiaroscuro, masterful dramatic composition, warm painted shafts of light and deep "
        "layered atmospheric depth, thick visible oil brushwork")
CLOSE = ("one continuous FULL-BLEED image that fills the ENTIRE 16:9 frame edge to edge — NOT a framed "
         "canvas, NOT a painting hung on a wall, NO picture frame, NO canvas edge, NO surrounding matte or "
         "letterbox or pillarbox bars, NO border, no panels, no text")

TABERNACLE = ("the ancient Israelite tabernacle of the Old Testament — heavy goat-hair and dyed blue-and-crimson "
              "linen curtains, acacia-wood frames overlaid with gold, warm oil-lamp light, NO stone cathedral NO "
              "medieval architecture NO modern anything, an authentic ancient near-eastern sacred tent")
PRIEST = ("the high priest of Israel, an ancient bearded man robed in plain undyed WHITE LINEN garments (humble "
          "white linen, NOT gold vestments, on this one day), a simple linen mitre, reverent and grave")
MERCYSEAT = ("the golden ark of the covenant deep within the Most Holy Place, its lid the mercy seat overshadowed "
             "by two golden cherubim with outstretched wings, half-veiled in a thick cloud of fragrant incense "
             "smoke and warm holy radiance — the presence of God shown ONLY as light and cloud, never a face or figure")
TABERNACLE_VEIL = ("the heavy inner veil of the tabernacle, a thick woven curtain of blue and crimson hung to seal off "
                   "the Most Holy Place, deep shadow and warm edge-light, NO legible text NO writing NO pattern-letters")
TEMPLE_VEIL = ("the great heavy veil of the Jerusalem temple, a vast woven curtain of blue and crimson hung floor to "
               "ceiling, deep shadow and warm edge-light, NO legible text NO writing NO pattern-letters")
GOATTWO = ("two ordinary goats standing calm and STILL side by side at the door of the tabernacle, plain and "
           "unadorned, quiet and motionless, NOT moving NOT writhing NOT the focus")
SCAPEGOAT = ("a single live goat standing still and small far out in the open wilderness beside a fit man, already "
             "deep in the desert distance with the camp a faint line far behind, plain and unadorned, motionless, "
             "NOT writhing NOT struggling")
ALTAR = ("the bronze altar of sacrifice with low flames and rising smoke and a basin of dark blood, ancient "
         "near-eastern, restrained and reverent, NOT gory")
WILDERNESS = ("a vast empty barren wilderness of pale rock and dust under a wide pale sky, a land not inhabited, "
              "heat-shimmer and drifting dust")
SHEEP = ("a scattered flock of sheep standing apart across a dim hillside, each one having strayed its own way, "
         "motionless in the shadow")
CITYHILL = ("the bare hill of execution just outside the ancient city wall of Jerusalem at dusk, the city gate and "
            "wall behind, 1st-century Judea")
ROBEDCROSS = ("Christ CRUCIFIED and SUSPENDED HIGH on a TALL wooden cross, lifted well above the ground — both arms "
              "stretched wide and NAILED through the wrists along the crossbeam, the FEET nailed together and lifted "
              "CLEAR off the ground, the whole body HANGING and sagging downward by the nails, head fallen onto the "
              "chest (face bowed and shadowed), a cloth wound about the waist and hips; NOT standing, NOT on the "
              "ground, NOT leaning against the cross; hands anatomically correct with five fingers")
RISEN = ("the risen glorified Christ filling the frame in warm radiant golden light, a dark-haired bearded man with "
         "a serene tender face turned toward the viewer, reaching one open pierced hand gently forward in welcome, a "
         "CLEAR dark nail-wound scar visibly piercing the centre of the open palm (prominent and unmistakable), the "
         "hand anatomically correct with five fingers, deep Rembrandt shadow behind")

FORWARD_IDS = {11, 22, 25}  # scapegoat going out · carried to the horizon · hero

# (id, mvt, [t0,t1], title, subject_block, sfx, atmos, jesus, jesus_variant)
S = [
 # ---- M1 The Picture (0–60.6) ----
 (1, "M1 The Picture", [0.0, 20.2], "Once a year, only once (hook)",
  f"{OPEN}, hushed and monumental: {PRIEST} standing alone and small in a single shaft of warm lamp-light before the "
  f"towering shadowed entrance of {TABERNACLE}, the whole hushed nation waiting unseen in the dark beyond — one man, "
  f"the holiest day of the year, about to go where no one else may; grave, reverent, {CLOSE}",
  "deep_low_drone + distant_crowd_hush", "the lamp-flame wavering warm over the priest, fine incense haze and dust motes adrift in the beam", False, None),

 (2, "M1 The Picture", [20.2, 40.4], "Behind the veil — I will appear in the cloud",
  f"{OPEN}, reverent and awe-struck interior: {MERCYSEAT}, the dim gold of the ark glimmering through the rolling "
  f"incense cloud, one warm shaft of holy radiance falling on the mercy seat in the deep dark of the Most Holy Place "
  f"— the dwelling a man enters only this once, and not without dread; worshipful, weighty, {CLOSE}",
  "drone_holy_low + incense_hiss_faint", "the incense cloud rolling and breathing over the mercy seat, the holy radiance pulsing softly, dust adrift", False, None),

 (3, "M1 The Picture", [40.4, 60.6], "One curtain between a guilty people and a holy God",
  f"{OPEN}, solemn vertical composition: {PRIEST} standing very small before {TABERNACLE_VEIL} that towers over him in "
  f"deep shadow, a thin line of holy light burning along the edge of the curtain from the hidden glory behind — one "
  f"heavy curtain between a guilty people and a holy God; restrained, grave, {CLOSE}",
  "drone_low + wind_tent_faint", "the great curtain stirring almost imperceptibly, the edge-light breathing, faint incense haze drifting", False, None),

 # ---- M2 The Problem (60.6–102.2) ----
 (4, "M2 The Problem", [60.6, 81.4], "A year of sin piled up — a guilty people",
  f"{OPEN}, sombre DEEP unified composition before the distant tabernacle under a heavy darkening sky — a whole "
  f"year's weight of sin and uncleanness resting on the people and on the very place where God met them; restrained, "
  f"weighty, FIVE held vignettes in one frame: (1) a bowed family clinging together, (2) an old man with his face in "
  f"his hands, (3) a mother shielding a small child, (4) the dim distant tabernacle, (5) the heavy lowering sky; {CLOSE}",
  "wind_low + crowd_murmur_soft", "the heavy sky and cloud drifting slowly, dust stirring low over the crowd, far tent-curtains lifting faintly", False, None),

 (5, "M2 The Problem", [81.4, 102.2], "It is the blood that maketh atonement",
  f"{OPEN}, grave close composition: {ALTAR} before the tabernacle, one shaft of warm light falling across the rising "
  f"smoke and the basin of dark blood, {PRIEST} half-lit beside it with bowed head — something innocent must die in "
  f"the place of the guilty, the blood that makes atonement; reverent, restrained NOT gory, deep Rembrandt shadow, {CLOSE}",
  "altar_fire_low + drone_holy_faint", "the altar flames and smoke rising and breathing, warm light wavering over the blood-basin, dust adrift", False, None),

 # ---- M3 The Strange Detail (102.2–165.5) ----
 (6, "M3 The Strange Detail", [102.2, 123.3], "Two goats — one sin offering",
  f"{OPEN}, arresting DEEP unified composition, the strange detail: {GOATTWO}, presented before {PRIEST} at the tent "
  f"door in a shaft of warm light — ONE sin offering, yet TWO goats, the riddle set; reverent, expectant, FOUR held "
  f"vignettes in one frame: (1) the two still goats side by side, (2) the priest's open hands above them, (3) the "
  f"tabernacle tent-door, (4) the dim waiting congregation behind; {CLOSE}",
  "drone_low + crowd_hush", "the warm light breathing over the two still goats, fine dust and incense haze drifting, curtains stirring", False, None),

 (7, "M3 The Strange Detail", [123.3, 144.4], "Lots cast — one for the LORD, one for the scapegoat",
  f"{OPEN}, hushed close study: the weathered hands of {PRIEST} holding the two lots low over the heads of the two "
  f"still goats in a pool of warm light, deep shadow around — one lot for the LORD, the other for the scapegoat, the "
  f"two destinies divided; grave, reverent, {CLOSE}",
  "drone_low + breath_held", "warm light wavering over the priest's hands and the goats, fine dust motes drifting slowly", False, None),

 (8, "M3 The Strange Detail", [144.4, 165.5], "One killed, one kept alive and let go",
  f"{OPEN}, weighty contrast in one frame: on one side, half in shadow, the first goat still beneath the priest's "
  f"hand near {ALTAR}; on the other, a fit man holding the second goat by a cord, the goat kept ALIVE and already "
  f"turned toward the bright opening of the wilderness, both still — why send one away alive instead of killing it; "
  f"reverent, the riddle held, {CLOSE}",
  "wind_open_low + drone_low", "the wilderness light breathing at the frame's edge, dust drifting, the altar smoke rising faintly", False, None),

 # ---- M4 The Centuries-Early Match (165.5–293.1) ----
 (9, "M4 The Centuries-Early Match", [165.5, 186.8], "The slain goat's blood behind the veil (the price)",
  f"{OPEN}, reverent and awe-struck: {PRIEST} alone within the Most Holy Place, sprinkling dark blood with his finger "
  f"toward {MERCYSEAT}, the incense cloud and holy radiance around him — the price paid, a death carried in before "
  f"God; worshipful, restrained NOT gory, deep shadow, {CLOSE}",
  "drone_holy_low + incense_hiss_faint", "the incense cloud rolling over the mercy seat, the radiance pulsing, fine blood-mist and dust adrift", False, None),

 (10, "M4 The Centuries-Early Match", [186.8, 208.0], "Both hands on the live goat — confessing the sin",
  f"{OPEN}, intimate and grave: {PRIEST} laying BOTH his hands down firmly on the head of the still live goat, head "
  f"bowed in confession over it, in a shaft of warm light against deep shadow — every sin of the people pressed onto "
  f"the goat's head, the transfer made visible; reverent, weighty, {CLOSE}",
  "drone_low + low_voices_confession", "the warm light breathing over the priest's hands and the goat, fine dust motes drifting slowly", False, None),

 (11, "M4 The Centuries-Early Match", [208.0, 229.3], "The scapegoat bears it away — a land not inhabited",
  f"{OPEN}, lonely and vast: {SCAPEGOAT}, set deep within {WILDERNESS}, the tiny still figures far out near the empty "
  f"horizon with the camp only a faint line far behind in shadow — the guilt carried away, out of sight, into a land "
  f"not inhabited; reverent, desolate, hopeful undertone, {CLOSE}",
  "wind_desolate + drone_low", "heat-shimmer and dust drifting across the wilderness, the pale sky breathing, the figures small and far", False, None),

 (12, "M4 The Centuries-Early Match", [229.3, 250.5], "By His own blood — entered in once (the cross)",
  f"{OPEN}, intimate horizontal CLOSE composition that fills the ENTIRE 16:9 frame edge to edge: the upper body of the "
  f"crucified Christ — the bowed shadowed head at the centre and both arms stretched WIDE along the horizontal wooden "
  f"crossbeam that runs the full width of the frame, the wrists nailed, dark blood at the wounds, a cloth at the waist "
  f"below, face bowed and in shadow; one shaft of warm light breaking across the beam — the true and final blood, "
  f"entering in once for all where the goats' blood was only a shadow; deep Rembrandt shadow, reverent, restrained NOT "
  f"graphic, NO vertical panel, NO pillarbox, NO grey side-bars, the painting bleeds to all four edges, {CLOSE}",
  "wind_desolate + choir_distant_faint", "slow storm-cloud drifting behind the cross, the warm shaft of light breathing, cold mist adrift", True, "passion"),

 (13, "M4 The Centuries-Early Match", [250.5, 271.8], "All we like sheep — laid on Him the iniquity (Isaiah)",
  f"{OPEN}, DEEP unified composition, OT-echo of Isaiah 53:6: in the dim foreground {SHEEP}, while above and beyond a "
  f"great broad shaft of warm light gathers and falls upon a single distant robed figure bowed low under a great "
  f"weight — all our straying laid upon the One who carries it; reverent, weighty, FOUR held vignettes: (1) the "
  f"scattered strayed sheep, (2) the dim hillside, (3) the gathering shaft of light, (4) the distant bowed bearer; {CLOSE}",
  "wind_low + drone_holy_faint", "the gathering shaft of light breathing over the bowed figure, the scattered sheep still, dust and mist adrift", False, None),

 (14, "M4 The Centuries-Early Match", [271.8, 293.1], "Without the gate — taken outside the camp",
  f"{OPEN}, sombre WIDE tableau at dusk: the distant dark SILHOUETTE of a single cross bearing a crucified figure, "
  f"small and far against the failing dusk sky on the bare hill of {CITYHILL}, the dark city wall and gate in the "
  f"foreground shadow — driven out, suffering outside the gate where the day's offering was always carried; the "
  f"figure distant and shadowed (a far silhouette, NOT a close bare-torso study); lonely, grave, reverent, {CLOSE}",
  "wind_desolate + low_drone", "the failing dusk light and cloud drifting behind the wall, cold dust adrift, a far torch-flame guttering", True, "passion"),

 # ---- M5 The Honest Objection (293.1–362.2) ----
 (15, "M5 The Honest Objection", [293.1, 316.1], "A fair-minded skeptic weighs it",
  f"{OPEN}, sober and clear: a single thoughtful bare-headed ancient man seated alone on a stone in a shaft of pale "
  f"light, chin resting on his hand, brow furrowed, and in the dim distance behind him the faint tabernacle and the "
  f"two still goats he is weighing — asking whether it is all just primitive ritual; reverent, restrained, no text, {CLOSE}",
  "low_drone + wind_faint", "the pale shaft of light breathing over the figure, fine dust motes drifting slowly through the beam", False, None),

 (16, "M5 The Honest Objection", [316.1, 339.2], "Year after year — the same blood, never finished",
  f"{OPEN}, weary and weighty: {PRIEST} standing at {ALTAR} again, head bowed, the same rite worn into the stones, "
  f"dim ghosts of the same altar and smoke receding into the deep shadow behind him as if repeated without end — a "
  f"cure that must come back every year is not the final cure; restrained, sombre, NOT gory, {CLOSE}",
  "altar_fire_low + drone_low", "the altar smoke rising endlessly and breathing, warm light guttering, fine ash and dust drifting", False, None),

 (17, "M5 The Honest Objection", [339.2, 362.2], "A picture of an atonement still to come",
  f"{OPEN}, DEEP unified composition, hopeful — the whole rite a shadow drawn year after year, pointing forward to an "
  f"atonement not yet come; reverent, contemplative, FOUR held vignettes: (1) the dim tabernacle in foreground shadow, "
  f"(2) its smoking altar, (3) a single warm shaft of light breaking up from the altar-smoke, (4) a far faint hill "
  f"catching the first pale dawn beyond; {CLOSE}",
  "drone_low + wind_distant", "slow cloud and altar-smoke drifting toward the far hill, the dawn-light breathing, dust adrift", False, None),

 # ---- M6 The Exchange (362.2–456.4) ----
 (18, "M6 The Exchange", [362.2, 385.8], "The priest who never sits",
  f"{OPEN}, grave and weary, intimate vertical study: {PRIEST} standing alone and bowed at his unending service in the "
  f"dim bare interior of the tabernacle — and conspicuously NO seat, NO chair, NO bench anywhere in the whole space "
  f"behind or around him, nowhere at all to sit down; he always stands, for the work is never finished; restrained, "
  f"sombre, deep Rembrandt shadow, {CLOSE}",
  "drone_low + wind_tent_faint", "warm lamp-light wavering over the standing priest, fine dust motes adrift, the curtains stirring faintly", False, None),

 (19, "M6 The Exchange", [385.8, 409.4], "Both priest and offering — once for all (the cross)",
  f"{OPEN}, the Exchange centerpiece, a DISTINCT solitary upward composition (NOT a wide hilltop tableau): {ROBEDCROSS} "
  f"seen from a low three-quarter angle from close beneath, the cross rising off-centre and filling the frame against a "
  f"vast DAWN sky of warm gold and soft rose breaking through parting cloud, the first light of a finished work falling "
  f"along the nailed arms and the bowed shadowed head — the one offering of His own body, once for all, the work "
  f"finished; awe-inspiring, intimate yet monumental, dawn-gold light (NOT storm), {CLOSE}",
  "low_drone + light_swell_low + choir_distant_faint", "the warm dawn light strengthening and breathing through the parting cloud, fine dust drifting up through the shafts", True, "passion"),

 (20, "M6 The Exchange", [409.4, 432.9], "The veil rent in twain — from the top",
  f"{OPEN}, awe-struck signature image: {TEMPLE_VEIL} TORN clean down the middle from top to bottom, the two heavy "
  f"halves fallen wide apart, and a flood of warm holy radiance pouring OUT through the great rent from the dark "
  f"sanctuary beyond — torn from above, not by any human hand; the inner sanctuary shown only as deep radiant shadow "
  f"and light (do NOT reveal an ark or furniture); reverent, awe-inspiring, NO text on the curtain, {CLOSE}",
  "deep_rumble_low + light_swell_low", "the radiance flooding and breathing through the torn rent, the heavy curtain-halves stirring, dust adrift in the light", False, None),

 (21, "M6 The Exchange", [432.9, 456.4], "The way thrown open from His own side",
  f"{OPEN}, luminous and hopeful: the place the veil once sealed now OPEN and flooded edge to edge with warm holy "
  f"radiance, the deep approach before it lit and open, light pouring out from where the heavy curtain hung — the way "
  f"in thrown open from God's own side; the opened inner space shown empty and radiant (only light and drifting "
  f"incense, NO ark, NO furniture); worshipful, dawn-bright, {CLOSE}",
  "drone_holy_low + light_swell_low", "the warm radiance strengthening and breathing across the opened space, incense cloud drifting, dust motes rising through the light", False, None),

 # ---- M7 The Invitation (456.4–532.6) ----
 (22, "M7 The Invitation", [456.4, 475.5], "As far as east from west — carried away (Psalm)",
  f"{OPEN}, vast HORIZONTAL composition, OT-echo of Psalm 103:12: an immense dawn horizon stretching edge to edge from "
  f"east to west, and in the foreground a lone freed figure standing still with a heavy dark burden fallen from his "
  f"open hands onto the ground at his feet, his face lifted into the wide breaking light — the sin removed as far as "
  f"the east is from the west, gone beyond the horizon; reverent, freeing, dawn-bright, {CLOSE}",
  "wind_open_low + light_swell_faint", "the wide dawn light strengthening across the whole horizon, low mist and fine dust drifting, the far sky breathing", False, None),

 (23, "M7 The Invitation", [475.5, 494.6], "No more paying, no earning — the curtain already torn",
  f"{OPEN}, tender and hopeful: a single ordinary ancient figure standing still in deep shadow before the great TORN "
  f"veil, the warm radiance from the opened way falling on the lifted face and the open empty hands held at the sides "
  f"— no more paying, no earning a way in, the curtain already torn open; reverent, kind, {CLOSE}",
  "drone_holy_faint + light_swell_faint", "the warm radiance through the torn veil breathing over the still figure, fine dust motes drifting up the beam", False, None),

 (24, "M7 The Invitation", [494.6, 513.6], "Boldness to enter by the blood of Jesus",
  f"{OPEN}, worshipful: a single figure standing within the parted veil, bathed in the warm flooding light of the "
  f"opened way, face lifted into the radiance, the dark torn curtain framing him on either side — boldness to enter "
  f"into the holiest by the blood; reverent, hopeful (light and radiance only, NO ark, NO furniture), {CLOSE}",
  "light_swell_low + drone_holy_faint", "the flooding radiance strengthening and breathing, incense cloud and fine dust drifting up through the light", False, None),

 (25, "M7 The Invitation", [513.6, 532.6], "Come to Him, and be carried clean (HERO close)",
  f"{OPEN}, NOT smooth modern devotional art, full-bleed hero — the living risen Christ as the great High Priest who "
  f"opened the way: a dark-haired bearded man with a serene glorified face, robed in white and deep crimson, standing "
  f"WITHIN the great TORN temple veil; behind and around Him the opened inner sanctuary is shown ONLY as deep EMPTY "
  f"radiant golden light and drifting incense haze — NO ark, NO golden chest, NO altar, NO menorah, NO ornate "
  f"furniture of any kind, only empty glowing radiance; He lifts one open pierced hand toward the viewer in welcome "
  f"and holds the other open at His side, BOTH hands anatomically correct with five clearly separated fingers and a "
  f"clear dark nail-wound in the centre of each palm — He Himself the new and living way through the torn veil; the "
  f"heavy torn curtain framing Him on either side; tender, worshipful, {CLOSE}",
  "choir_warm_soft + light_swell_low", "the warm golden radiance breathing through the torn veil around Him, the curtain edges and His robe stirring almost imperceptibly", True, "resurrection"),
]

AUDIO = 532.6


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    scenes = []
    for (sid, mvt, (t0, t1), title, subj, sfx, atmos, jesus, jvar) in S:
        win = round(t1 - t0, 1)
        fill = "forward_slow" if sid in FORWARD_IDS else "boomerang"
        camera = "a very slow, steady cinematic push-in" if fill == "forward_slow" else "locked, the faintest breathing drift"
        directional = (fill == "forward_slow")
        scenes.append({"id": sid, "mvt": mvt, "t": [round(t0, 1), round(t1, 1)], "title": title,
                       "subject_block": subj, "sfx": sfx, "camera": camera, "atmos": atmos,
                       "fill": fill, "jesus": jesus, "jesus_variant": jvar, "directional": directional,
                       "hero": (sid == 25), "window_s": win})
    scenes.sort(key=lambda s: s["t"][0])
    plan = {
        "format": "16:9 long-form deep-dive",
        "episode": "The Two Goats — the Day of Atonement (Leviticus 16) fulfilled in Christ",
        "audio": "narration.mp3 — 532.6s (natural pace, 3-voice); scene t[] tile the turn timeline",
        "image_provider": "nbp (Nano Banana Pro, Baroque oil)",
        "animation": {"model": "veo3_1_lite", "aspect": "16:9", "duration": 8,
                      "note": "goats/sheep/figures are ALL still/frozen (veo morphs live subjects); subject_blocks are state-only, no locomotion verbs; God shown only as cloud+light; the loincloth crucifixions (S12/S19 close, S14 distant silhouette) are BARE-TORSO and will likely be refused by veo3 as NSFW -> fall back to direct-Kling per feedback-hf-video-blocks-cross (S14 is a distant silhouette to shrink that surface); Christ-face reserved for the hero S25; almost all scenes boomerang (locked cam) so long windows never freeze; forward_slow only on S11/S22/S25"},
        "fill_design": ("ANIMATION-AWARE: every subject (priest, goats, cross, risen Christ) is FROZEN; only ambient "
                        "(incense smoke/light/dust/heat-shimmer/cloud/cloth) moves. Almost all scenes BOOMERANG on a "
                        "LOCKED camera (no end-of-push freeze, no continuation-clip cost); forward_slow only on "
                        "S11 (scapegoat going out), S22 (carried to the horizon), S25 (hero)."),
        "style_base": STYLE_BASE,
        "rule": ("ONE spine: one sin offering took TWO goats — the slain goat's blood behind the veil (price PAID) and "
                 "the live scapegoat into the wilderness (guilt CARRIED AWAY) — both halves fulfilled once-for-all in "
                 "Christ; the veil is torn from above and the way thrown open; every quote's visual matches its "
                 "narration cue; the film CLOSES on the living risen Christ (hero S25)."),
        "film_name": "The_Two_Goats_16x9.mp4",
        "style_tail": STYLE_TAIL,
        "scenes": scenes,
    }
    (OUT / "scene_plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n",
                                         encoding="utf-8")
    # --- deterministic self-checks (LF-SP guardrails) ---
    from collections import Counter
    assert len(scenes) <= 25, f"LF-INV-4 cap: {len(scenes)} > 25"
    mv = Counter(s["mvt"].split()[0] for s in scenes)
    assert all(mv[f"M{i}"] >= 2 for i in range(1, 8)), f"movement coverage FAIL (need >=2 each): {mv}"
    assert any(s["jesus"] for s in scenes), "no Jesus/NT-link scene"
    assert scenes[-1]["jesus"] and scenes[-1]["jesus_variant"] == "resurrection", "hero must close on risen Christ"
    assert scenes[-1]["hero"] and sum(1 for s in scenes if s["hero"]) == 1, "exactly one hero flag, on the close"
    # named-vignette check (LF-SP-G6): unified scenes must list >=3 enumerated vignettes
    for s in scenes:
        if "unified" in s["subject_block"].lower():
            n_named = s["subject_block"].count("(1)") + s["subject_block"].count("(2)") + s["subject_block"].count("(3)")
            assert "(3)" in s["subject_block"], f"unified scene {s['id']} lacks 3-5 named vignettes"
    # no live 'temple' anachronism in the tabernacle-era movements (M1-M5)
    for s in scenes:
        if s["mvt"].split()[0] in ("M1", "M2", "M3", "M4", "M5"):
            assert "temple veil" not in s["subject_block"].lower(), f"scene {s['id']} uses 'temple veil' before Mt 27 (M6)"
    assert all(s["atmos"] for s in scenes), "every scene needs an atmospheric element"
    n_unified = sum(1 for s in scenes if "unified" in s["subject_block"].lower())
    assert n_unified >= 2, f"need >=2 unified scenes, have {n_unified}"
    # crucifixions: atonement subject justifies a few, but keep them VARIED (cap 4)
    n_crux = sum(1 for s in scenes if ("christ crucified" in s["subject_block"].lower()
                                       or "crucified christ" in s["subject_block"].lower()))
    assert 2 <= n_crux <= 4, f"expected 2-4 crucifixion scenes, have {n_crux}"
    # OT-echo scenes (Isaiah 53:6 + Psalm 103:12) present
    assert sum(1 for s in scenes if "ot-echo" in s["subject_block"].lower()) >= 2, "need >=2 OT-echo scenes"
    for s in scenes:
        b = s["subject_block"].lower()
        assert "no text" in b or "no legible" in b, f"scene {s['id']} missing no-text guard"
        assert "scroll" not in b and "codex" not in b and "writing" not in b.replace("no legible writing", "").replace("no writing", ""), \
            f"scene {s['id']} has a writing surface (veo morph hazard)"
        # only enforce still/calm when a LIVE goat is actually DEPICTED — ignore goat-hair
        # fabric and abstract possessive mentions ("the goats' blood was only a shadow")
        bc = b.replace("goat-hair", "").replace("goats'", "").replace("goats’", "")
        if "goat" in bc:
            assert any(w in b for w in ("still", "calm", "motionless", "quiet")), \
                f"scene {s['id']} goat not marked still/calm"
    assert abs(scenes[0]["t"][0]) < 0.05, "must start at 0"
    for a, b in zip(scenes, scenes[1:]):
        assert abs(a["t"][1] - b["t"][0]) < 0.05, f"gap between {a['id']} and {b['id']}"
    assert abs(scenes[-1]["t"][1] - AUDIO) < 0.3, f"must end at {AUDIO}, ends {scenes[-1]['t'][1]}"
    assert "biblical-period" in plan["style_tail"]
    jn = sum(1 for s in scenes if s["jesus"])
    fwd = sorted(s["id"] for s in scenes if s["fill"] == "forward_slow")
    maxwin = max(s["window_s"] for s in scenes)
    print(f"[ok] scene_plan.json — {len(scenes)} scenes, movements {dict(mv)}")
    print(f"[ok] unified={n_unified}  crucifixions={n_crux}  jesus={jn}  forward_slow={fwd}  hero=S{scenes[-1]['id']}")
    print(f"[ok] tiling contiguous 0.0 -> {scenes[-1]['t'][1]}s · max window {maxwin}s (boomerang handles long windows; no freeze)")


if __name__ == "__main__":
    main()
