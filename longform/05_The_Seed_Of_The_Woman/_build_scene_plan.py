"""Author the 16:9 long-form scene_plan.json for #05 The Seed of the Woman (Gen 3:15).

25 scenes across the 7 movements (M1:3 M2:3 M3:4 M4:4 M5:3 M6:4 M7:4), windows tiled
to the REAL rendered turn timeline (503.4s, 3-voice; ffprobe/meta ground truth). Baroque
oil, veo3 atmospheric motion. Hero = S25 (the risen Christ, gospel-pivot close).

v2 (post 5-CLI panel, 20260624-124956 — cursor/claude REVISE convergent): cut 26->25 (LF-INV-4
cap); merged the adjacent heel pair; only TWO crucifixions now (close + wide-turn), S14 demoted
from a 3rd cross to a serpent-defeat-light; removed the S15 scroll (veo writing-morph hazard);
fixed the S17 atmos copy-paste + S11 dropped word + S8 quote; fill is now mostly BOOMERANG
(locked cam, atmosphere-only, no end-of-push freeze, no continuation-clip cost) — forward_slow
only on S9 (the promise) + S25 (hero). Reuse (S19/S20 cross, S21 tomb, S25 risen) is eye-checked
at the render stage per the REVIEWED_REUSABLE discipline, not auto-matched here.

DESIGN-FOR-THE-ANIMATION (veo3 animates ambient motion, never subjects):
  * THE SERPENT is the trap. veo morphs living snakes -> it is ALWAYS coiled, still, low,
    peripheral, half-lost in shadow — NEVER the writhing animated focus. In crushed beats it
    is an inert lifeless form, not moving.
  * GOD is NEVER a face or figure — only a shaft of warm holy light / radiance.
  * every CROSS is the ROBED crucified Christ (waist robed -> veo NSFW-safe), correct hanging
    pose, hands anatomically correct (five fingers).
  * EDEN is primeval/timeless; manger + cross are 1st-century Judea. NO modern/medieval/European
    dress. NO legible text anywhere.
  * `atmos` is ONLY ambient motion (mist drift, leaves stir, light breathing, dust motes, cloud,
    lamp-flame, cloth stir). NEVER subject motion. Almost all scenes BOOMERANG (locked camera);
    forward_slow only on S9 + S25.
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

EDEN = ("the primeval garden of Eden at the dawn of the world — lush ancient trees heavy with leaf, "
        "deep ferns and pristine undergrowth, a still river and low ground-mist, timeless and untouched, "
        "NO modern NO medieval NO European anything")
COUPLE = ("the first man and the first woman, primeval Adam and Eve, covered ONLY in rough primitive "
          "fig-leaf aprons and untailored animal-skin wraps, bare-armed and bare-shouldered, long loose "
          "unkempt hair, NO woven robe NO mantle NO veil NO head-covering NO halo, NO medieval or devotional "
          "dress, ancient and unadorned, deep shadow")
# primeval Eve alone — must NOT render as a veiled medieval Madonna (HF default to avoid)
WOMANEDEN = ("the first woman, primeval Eve, covered ONLY in a rough fig-leaf and animal-skin wrap, "
             "bare-armed and bare-shouldered, long loose hair, NO woven robe NO mantle NO veil NO "
             "head-covering NO halo, ancient and unadorned")
SERPENT = ("a single serpent low among the roots and shadow, coiled and STILL, kept small and peripheral, "
           "plainly inert, NOT writhing NOT moving NOT the focus")
DEADSERPENT = ("an inert lifeless serpent crushed and still on the ground, plainly dead, NOT moving NOT writhing")
PRESENCE = ("the unseen presence of the LORD shown ONLY as a great shaft of warm holy light breaking "
            "through the trees, God never depicted as a face or a figure, only radiance and light")
ROBEDCROSS = ("Christ CRUCIFIED and SUSPENDED HIGH on a TALL wooden cross, lifted well above the ground — "
              "both arms stretched wide and NAILED through the wrists along the crossbeam, the FEET nailed "
              "together and lifted CLEAR off the ground, the whole body HANGING and sagging downward by the "
              "nails, head fallen onto the chest, a cloth wound about the waist and hips; NOT standing, NOT on "
              "the ground, NOT leaning against the cross; hands anatomically correct with five fingers")
MADONNA = ("a young mother in a dim humble ancient interior cradling a newborn infant close, wrapped in "
           "plain cloth, warm low lamplight on the child, deep Rembrandt shadow, reverent and tender, "
           "no halo, no modern dress")

FORWARD_IDS = {9, 12, 25}  # push (no boomerang yo-yo); S12 manger is a deterministic ffmpeg push-in (veo NSFW-refuses the newborn)

# (id, mvt, [t0,t1], title, subject_block, sfx, atmos, jesus, jesus_variant)
S = [
 # ---- M1 The Picture (0–53) ----
 (1, "M1 The Picture", [0.0, 11.8], "Something has gone terribly wrong (hook)",
  f"{OPEN}, intimate and ominous: {COUPLE} crouched and HIDING low among the deep shadowed trees of {EDEN} "
  f"at dusk, their faces turned away in shame and fear, a first chill of guilt over a once-perfect garden, "
  f"the warm light they are shrinking from glimmering beyond the trunks; tender, grave, {CLOSE}",
  "garden_birdsong_uneasy + wind_leaves_low", "ground-mist drifting between the trunks, leaves and ferns stirring faintly, far light breathing", False, None),

 (2, "M1 The Picture", [11.8, 31.3], "They heard the voice of the LORD — Where art thou",
  f"{OPEN}, WIDE reverent tableau: {EDEN} in the cool of the day, {PRESENCE} moving through the garden, and "
  f"in the shadowed foreground {COUPLE} pressed back behind a great tree, hiding from the approaching radiance; "
  f"the holy light searching the garden for them; awe and dread, {CLOSE}",
  "wind_leaves_low + drone_holy_faint", "the great shaft of light strengthening and breathing through the trees, ground-mist and dust motes adrift", False, None),

 (3, "M1 The Picture", [31.3, 53.0], "The blame goes round — the serpent beguiled me",
  f"{OPEN}, DEEP unified composition, grave: in the warm foreground the man and the woman half-turned in mutual "
  f"blame, hands low and accusing, while {SERPENT} lies half-hidden among the roots in the dark below them; the "
  f"once-whole harmony of {EDEN} unravelling, the three caught in one chain of blame under the fading light; "
  f"sombre, reverent, {CLOSE}",
  "wind_leaves_low + low_unease_drone", "ground-mist creeping low over the roots, leaves stirring, the light dimming and breathing", False, None),

 # ---- M2 The Problem (53–94) ----
 (4, "M2 The Problem", [53.0, 67.5], "Judgment must fall — death enters the world",
  f"{OPEN}, sombre WIDE tableau: {EDEN} now under a darkening, heavier sky, the first long shadows falling across "
  f"the garden, {COUPLE} small and exposed at the edge of the trees as the warmth withdraws — innocence gone, a cold "
  f"new mortality entering a world that was deathless; restrained, weighty, {CLOSE}",
  "wind_rising_low + drone_low_sub", "the sky darkening and cloud drifting in, ground-mist thickening, cold air stirring the leaves", False, None),

 (5, "M2 The Problem", [67.5, 81.0], "They took the creature's word against the Creator",
  f"{OPEN}, intimate close composition: the man and the woman half-lit in deep shadow, faces lowered and stricken "
  f"with the dawning weight of what they have done, {SERPENT} coiled still and watchful in the dark nearby — the "
  f"terrible bargain already made, trust given to the creature over the Maker; tender, grave, deep Rembrandt shadow, {CLOSE}",
  "wind_low + breath_shallow", "the low light wavering over their faces, faint mist and dust drifting, leaves barely stirring", False, None),

 (6, "M2 The Problem", [81.0, 94.5], "No human way back — rescue must come from God",
  f"{OPEN}, WIDE and desolate: {COUPLE} very small at the mouth of {EDEN}, standing before the vast darkening "
  f"wilderness beyond the garden's edge, their backs to the last warm light, no road back the way they came — "
  f"if rescue comes it must come from God's side of the breach; lonely, reverent, hopeful undertone, {CLOSE}",
  "wind_open_low + drone_holy_faint", "cloud drifting over the far wilderness, ground-mist at the garden edge, robes and leaves stirring", False, None),

 # ---- M3 The Strange Detail (94–158) ----
 (7, "M3 The Strange Detail", [94.5, 108.2], "Watch closely — God turns to the serpent",
  f"{OPEN}, hushed and weighty: {PRESENCE} bending low toward {SERPENT} coiled still at the foot of a great tree in "
  f"deep shadow, the man and woman dim and waiting behind — the holy light turning first to the enemy, not yet to the "
  f"guilty pair; a strange expectant stillness, reverent, {CLOSE}",
  "wind_low + drone_holy_faint", "the shaft of light strengthening on the still serpent and roots, ground-mist and dust adrift", False, None),

 (8, "M3 The Strange Detail", [108.2, 130.2], "Cursed above all — the serpent's judgment",
  f"{OPEN}, solemn close composition: {SERPENT} low in the dust at the base of the tree, half-lit by the descending "
  f"holy radiance, pressed low toward the ground under the weight of the curse — brought down into the dust; the "
  f"enemy humbled, the pure curse before the promise; deep shadow, grave, NOT gory, {CLOSE}",
  "drone_low + wind_leaves_low", "the radiance pulsing over the still serpent, fine dust and mist drifting low along the ground", False, None),

 (9, "M3 The Strange Detail", [130.2, 140.2], "I will put enmity — her seed shall bruise (the promise)",
  f"{OPEN}, the SIGNATURE protoevangelium image, reverent and arresting: {WOMANEDEN} standing small in a strong warm "
  f"shaft of holy light, looking down toward {SERPENT} coiled low in the foreground shadow, the shaft of light falling "
  f"like a drawn line of enmity between the woman and the serpent — the promised crushing of the serpent foretold, not "
  f"yet done; deep shadow, the light breaking the darkness, worshipful and weighty, {CLOSE}",
  "drone_holy_low + light_swell_faint", "the shaft of holy light strengthening and breathing, fine dust motes drifting up through the beam", False, None),

 (10, "M3 The Strange Detail", [140.2, 158.5], "Before a word to Eve or Adam — grace gets the first word",
  f"{OPEN}, DEEP unified composition, hopeful undertone in deep shadow: {COUPLE} still waiting unsentenced in the dim "
  f"midground, while over the serpent in the foreground a warm promise-light has already broken — the order made "
  f"visible, mercy spoken into the curse before the sentence falls on the man or the woman; reverent, tender, {CLOSE}",
  "drone_holy_faint + wind_low", "the promise-light strengthening across the scene, ground-mist and dust drifting, leaves stirring faintly", False, None),

 # ---- M4 The Centuries-Early Match (158–253) ----
 (11, "M4 The Centuries-Early Match", [158.5, 183.4], "Her seed — strangely specific",
  f"{OPEN}, contemplative CLOSE study: {WOMANEDEN} half-lit in deep shadow, one hand resting low at her side, the warm "
  f"light gathered on her alone against the surrounding dark — the hope of the world narrowing strangely to the "
  f"woman's seed; reverent, quiet, weighty, {CLOSE}",
  "drone_holy_faint + wind_low", "the gathered light breathing softly over the figure, fine dust motes adrift in the shadow", False, None),

 (12, "M4 The Centuries-Early Match", [183.4, 202.7], "Made of a woman — the child arrives",
  f"{OPEN}, intimate and tender, 1st-century Judea: {MADONNA} — the long-promised seed of the woman come at last, "
  f"the fulness of time; the single warm lamp the only light in the deep shadow, the newborn the heart of the frame; "
  f"reverent, hushed, holy, {CLOSE}",
  "lamp_flame_soft + night_low", "the lamp flame wavering warm over the child, a thin thread of smoke rising, shadow breathing", False, None),

 (13, "M4 The Centuries-Early Match", [202.7, 226.8], "Not a citation — a trajectory (the honest beat)",
  f"{OPEN}, DEEP unified composition holding the long arc: on one side, half in deep shadow, the dim garden of Eden "
  f"with its still serpent; on the other, far and small, the silhouette of a single hill catching the first pale "
  f"light beyond rolling country — the whole story bending from the garden toward what is coming, a quiet visual "
  f"trajectory not a proof; reverent, contemplative, {CLOSE}",
  "drone_low + wind_distant", "slow cloud drifting over the far hill, ground-mist over the dim garden, dust motes adrift", False, None),

 (14, "M4 The Centuries-Early Match", [226.8, 252.9], "The works of the devil destroyed",
  f"{OPEN}, weighty and hopeful, DEEP unified composition, NO cross in frame: low in deep shadow {DEADSERPENT}, the "
  f"old serpent named the Devil now lifeless; and breaking down over it from above a great broad shaft of warm "
  f"victory-light driving back the darkness — the works of the devil undone, the enemy defeated; reverent, "
  f"awe-struck, {CLOSE}",
  "drone_holy_low + light_swell_faint", "the victory-light strengthening and breathing down over the still serpent, fine dust drifting up through the beam", False, None),

 # ---- M5 The Honest Objection (253–320) ----
 (15, "M5 The Honest Objection", [252.9, 275.0], "A fair skeptic — reading Jesus in",
  f"{OPEN}, sober and clear, intimate: a single thoughtful bare-headed ancient man seated alone on a stone in a shaft "
  f"of pale light in deep shadow, chin resting on his hand, brow furrowed as he weighs a hard question, hands "
  f"otherwise empty, no props; the honest doubt given room; reverent, restrained, no text, {CLOSE}",
  "low_drone + wind_faint", "the pale shaft of light breathing over the figure, fine dust motes drifting slowly through the beam", False, None),

 (16, "M5 The Honest Objection", [275.0, 296.7], "We follow the line out from within",
  f"{OPEN}, DEEP unified composition, contemplative: a dim continuous landscape running from the shadowed garden of "
  f"Eden on one side, through low hills, toward a far faint dawn-light gathering on the horizon — a single unbroken "
  f"line followed out from within the story itself, not forced from outside; reverent, quiet, {CLOSE}",
  "drone_low + wind_distant", "slow cloud and ground-mist drifting along the landscape, the far dawn-light breathing", False, None),

 (17, "M5 The Honest Objection", [296.7, 319.9], "Under His feet — the church shares the victory",
  f"{OPEN}, DEEP unified composition, hopeful: a small company of ordinary ancient people standing together in a broad "
  f"warm shaft of light that pours down from a faint robed cross on a distant hill beyond them, the dim still serpent "
  f"far back in the shadow behind — the people sharing the victory only because they stand on the ground the One won "
  f"first; reverent, no text, {CLOSE}",
  "drone_holy_low + crowd_soft", "the broad shaft of light strengthening over the standing people, fine dust and ground-mist drifting", False, None),

 # ---- M6 The Exchange (320–415) ----
 (18, "M6 The Exchange", [319.9, 345.1], "Head and heel — two wounds, not equal",
  f"{OPEN}, the heel/head exchange held in one unified frame, intimate and grave: a single bare human heel in warm "
  f"light bearing a dark serpent-bite wound, pressed down upon the crushed still head of {DEADSERPENT} in deep shadow "
  f"below — the costly bruise to the heel and the crushing blow to the head, the two unequal wounds made plain; "
  f"restrained NOT gory, deep Rembrandt shadow, {CLOSE}",
  "drone_low + light_swell_faint", "the warm light wavering over the wounded heel, fine dust motes adrift, shadow breathing", False, None),

 (19, "M6 The Exchange", [345.1, 369.4], "That is the cross — bearing what we had earned",
  f"{OPEN}, sombre and worshipful three-quarter view: {ROBEDCROSS} against a vast dark sky at the ninth hour, one shaft "
  f"of warm light breaking across the bowed head and the nailed outstretched arms — the Son bearing the death that was "
  f"our wages, stepping into the very judgment we deserved; deep Rembrandt shadow, reverent, restrained NOT graphic, {CLOSE}",
  "wind_desolate + choir_distant_faint", "storm cloud drifting slowly behind the cross, the warm shaft of light breathing, cold mist adrift", True, "passion"),

 (20, "M6 The Exchange", [369.4, 392.0], "The turn — through death He broke the serpent's head",
  f"{OPEN}, the turn made visible, EPIC monumental WIDE tableau: {ROBEDCROSS} lifted HIGH and CENTRAL and towering on "
  f"the crest of a barren hill, dominant against a vast luminous sky of breaking storm-cloud shot through with great "
  f"shafts of warm golden god-light, sweeping atmospheric distance falling away below; small and far in the deep "
  f"shadow at the foot of the hill {DEADSERPENT} crushed and lifeless — the blow that looked like the serpent winning "
  f"is the blow that broke his head; awe-inspiring, monumental, sombre turning to dawning hope, {CLOSE}",
  "low_drone + light_swell_low", "warm light strengthening down over the distant cross, slow storm-cloud parting, dust drifting up through the beams", True, "passion"),

 (21, "M6 The Exchange", [392.0, 415.1], "The One whose heel was struck rose (the empty tomb)",
  f"{OPEN}, luminous and hopeful, 1st-century Judea at dawn: the open empty rock tomb in a garden, the great stone "
  f"rolled aside, the dark doorway spilling warm radiant light, folded grave-cloths within catching the glow, no figure "
  f"in the doorway — the heel that was struck has risen, the enemy's head will never lift again; reverent, dawn-bright, {CLOSE}",
  "dawn_birdsong_soft + light_swell_low", "broad warm dawn light strengthening from the tomb doorway, fine dust and mist drifting, leaves stirring", True, "resurrection"),

 # ---- M7 The Invitation (415–503) ----
 (22, "M7 The Invitation", [415.1, 440.0], "Where it was spoken — into the enemy's curse",
  f"{OPEN}, DEEP unified composition mirroring the hook: the dim garden of Eden with {COUPLE} waiting in shadow and "
  f"{SERPENT} still in the dark, while a warm promise-light already breaks over the scene and runs forward toward a "
  f"distant gathering dawn — the oldest promise spoken into the curse, in the enemy's hearing, before the guilty were "
  f"sentenced; reverent, tender, {CLOSE}",
  "drone_holy_faint + wind_low", "the promise-light strengthening across the garden toward the far dawn, ground-mist and dust adrift", False, None),

 (23, "M7 The Invitation", [440.0, 466.5], "The serpent still whispers — but the promise was kept",
  f"{OPEN}, intimate and grave: a lone figure in deep shadow at the edge of the trees, half-turned toward a breaking "
  f"warm light, {SERPENT} still and dim in the dark behind — the old lie still hissed (God is against you, stay hidden) "
  f"against the warm light of a promise already kept; tender, hopeful, deep Rembrandt shadow, {CLOSE}",
  "wind_low + drone_holy_faint", "the warm light strengthening and breathing through the trees, ground-mist and dust drifting low", False, None),

 (24, "M7 The Invitation", [466.5, 485.0], "Step out from behind the trees",
  f"{OPEN}, intimate and kind: a single human figure standing at the edge of the deep tree-shadow facing a broad "
  f"breaking shaft of warm golden light, face lifted into the light, hands open and empty at the sides — not healed "
  f"first, not strong, simply out of hiding; the dying do not heal themselves; tender, hopeful, {CLOSE}",
  "light_swell_faint + wind_soft", "the broad shaft of warm light strengthening, fine dust motes drifting up through the beam, leaves stirring", False, None),

 (25, "M7 The Invitation", [485.0, 503.4], "Be found by Him (HERO close)",
  f"{OPEN}, NOT smooth modern devotional art, full-bleed close hero: the risen glorified Christ filling the frame in "
  f"warm radiant golden light, a dark-haired bearded man with a serene tender face turned toward the viewer, reaching "
  f"one open pierced hand gently forward in welcome, a CLEAR dark nail-wound scar visibly piercing the centre of the open "
  f"palm (prominent and unmistakable), the hand anatomically correct with five fingers, deep Rembrandt shadow behind — the rescue God named from the very "
  f"beginning, the gospel-pivot hero that closes the film on the risen Christ, {CLOSE}",
  "choir_warm_soft + light_swell_low", "the warm golden light glowing softly and steadily, the robe and hair stirring almost imperceptibly", True, "resurrection"),
]

AUDIO = 503.4


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
                       "window_s": win})
    scenes.sort(key=lambda s: s["t"][0])
    plan = {
        "format": "16:9 long-form deep-dive",
        "episode": "The Seed of the Woman — Genesis 3:15 (the protoevangelium) fulfilled in Christ",
        "audio": "narration.mp3 — 503.4s (natural pace, 3-voice); scene t[] tile the turn timeline",
        "image_provider": "nbp (Nano Banana Pro, Baroque oil)",
        "animation": {"model": "veo3_1_lite", "aspect": "16:9", "duration": 8,
                      "note": "the serpent is ALWAYS still/peripheral (veo morphs live snakes); God shown only as light; all crosses robed -> veo NSFW-safe; almost all scenes boomerang (locked cam) so long windows never freeze"},
        "fill_design": ("ANIMATION-AWARE: every subject (serpent, couple, cross, risen Christ) is FROZEN; only "
                        "ambient (mist/light/dust/cloud/cloth) moves. Almost all scenes BOOMERANG on a LOCKED "
                        "camera (no end-of-push freeze, no continuation-clip cost); forward_slow only on S9 + S25."),
        "style_base": STYLE_BASE,
        "rule": ("ONE spine: the first promise of rescue is spoken into the serpent's curse, before Adam/Eve "
                 "are sentenced (the woman's seed who crushes by being wounded); the head/heel exchange is the "
                 "cross; every quote's visual matches its narration cue; the film CLOSES on the risen Christ (hero S25)."),
        "film_name": "Seed_Of_The_Woman_16x9.mp4",
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
    assert all(s["atmos"] for s in scenes), "every scene needs an atmospheric element"
    n_unified = sum(1 for s in scenes if "unified" in s["subject_block"].lower())
    assert n_unified >= 2, f"need >=2 unified scenes, have {n_unified}"
    # exactly two crucifixions (no premature-cross repetition); the only ROBEDCROSS scenes
    n_crux = sum(1 for s in scenes if "christ crucified" in s["subject_block"].lower())
    assert n_crux == 2, f"expected exactly 2 crucifixion scenes, have {n_crux}"
    for s in scenes:
        b = s["subject_block"].lower()
        assert "no text" in b, f"scene {s['id']} missing no-text guard"
        assert "scroll" not in b and "codex" not in b and "writing" not in b.replace("no legible writing", ""), \
            f"scene {s['id']} has a writing surface (veo morph hazard)"
        if "serpent" in b:
            assert any(w in b for w in ("still", "inert", "dead", "lifeless", "crushed")), \
                f"scene {s['id']} serpent not marked still/inert"
        # atmos must not reference elements absent from the scene (copy-paste guard)
        if "heel" in s["atmos"].lower():
            assert "heel" in b, f"scene {s['id']} atmos references a heel not in the scene"
    assert abs(scenes[0]["t"][0]) < 0.05, "must start at 0"
    for a, b in zip(scenes, scenes[1:]):
        assert abs(a["t"][1] - b["t"][0]) < 0.05, f"gap between {a['id']} and {b['id']}"
    assert abs(scenes[-1]["t"][1] - AUDIO) < 0.3, f"must end at {AUDIO}, ends {scenes[-1]['t'][1]}"
    assert "biblical-period" in plan["style_tail"]
    jn = sum(1 for s in scenes if s["jesus"])
    fwd = sorted(s["id"] for s in scenes if s["fill"] == "forward_slow")
    maxwin = max(s["window_s"] for s in scenes)
    maxfwd = max((s["window_s"] for s in scenes if s["fill"] == "forward_slow"), default=0)
    print(f"[ok] scene_plan.json — {len(scenes)} scenes, movements {dict(mv)}")
    print(f"[ok] unified={n_unified}  crucifixions={n_crux}  jesus={jn}  forward_slow={fwd} (max {maxfwd}s)  hero=S{scenes[-1]['id']}")
    print(f"[ok] tiling contiguous 0.0 -> {scenes[-1]['t'][1]}s · max window {maxwin}s (boomerang handles long windows; no freeze)")


if __name__ == "__main__":
    main()
