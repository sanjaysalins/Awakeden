#!/usr/bin/env python
"""Transform livingpage_full.spec.json to v3 (LIVINGPAGE_STANDARD 3b):
de-slopped captions (no dashes/ellipses), partial-verse tags (v.14a not '...'),
fresh-image beat remap (max 2 uses/still, never twice full-bleed), story-keyed SFX."""
import json
from pathlib import Path

POOL = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
spec = json.loads((POOL / "livingpage_full.spec.json").read_text(encoding="utf-8"))
B = spec["beats"]

def clip(slug, motion="pushin", **kw):
    d = {"slug": slug, "motion": motion}; d.update(kw); return d

# ---- 1. beat remap (index is 1-based beat number) ----
def setb(i, tpl=None, clips=None, **kw):
    b = B[i - 1]
    if tpl: b["tpl"] = tpl
    if clips is not None: b["clips"] = clips
    b.update(kw)

setb(12, "big_inset", [clip("david_psalmist"), clip("david_scroll_sealed", "static", at=45.36, slide="up", flash=False)])
setb(14, "full", [clip("execution_stakes_field", "static", cam="arc")])
setb(15, "quad", [clip("roman_nails_pouch", "static", cam="arc", at=59.91, slide="left"),
                  clip("hung_by_arms", "static", cam="arc", zoom=1.25, at=60.71, slide="right"),
                  clip("execution_stakes_field", "static", cam="arc", zoom=1.3, at=60.89, slide="left"),
                  clip("garment_tug", zoom=1.15, at=61.21, slide="right")])
setb(19, "full", [clip("spit_shout_macro", "static", cam="arc")])
setb(20, "full", [clip("mockers_below_cross_low")])
setb(21, "two_v", [clip("david_old_deathbed"), clip("old_king_hands_rings", "static", cam="arc", at=83.68, slide="right")])
setb(22, "two_v", [clip("shepherd_boy_sling", "static", cam="arc", at=85.13, slide="left"),
                   clip("war_helmet_spear_rest", "static", cam="arc", at=86.84, slide="right")])
setb(23, "full", [clip("scholars_debate_two", "static", cam="arc")])
setb(25, "two_v", [clip("two_scrolls_compared", "static", cam="arc", at=95.52, slide="left"),
                   clip("water_spilled_stone", "static", cam="arc", at=95.78, slide="right")])
setb(26, "full", [clip("golgotha_three_crosses_ridge")])
setb(33, "two_v", [clip("jerusalem_night_lyre", "static", cam="arc"),
                   clip("roman_nails_pouch", "static", cam="arc", zoom=1.2, at=131.10, slide="right")])
setb(34, "full", [clip("wrists_bound_beam_macro")])
setb(35, "two_v", [clip("disputed_word_marks", "static", cam="arc", at=139.66, slide="left"),
                   clip("quill_ink_drop", "static", cam="arc", at=140.51, slide="right")])
setb(39, "full", [clip("hill_crowd_watching_storm", "static", cam="arc")])
setb(40, "two_v", [clip("dice_cup_shadow", "static", cam="arc", zoom=1.2, at=162.76, slide="left"),
                   clip("quill_ink_drop", "static", cam="arc", zoom=1.2, at=164.30, slide="right")])
setb(44, "full", [clip("hebrew_scroll_edge_light", "static", cam="arc")])
setb(46, "full", [clip("lion_shadow_wall", "static", cam="arc")])
setb(47, "two_v", [clip("scholars_debate_two", "static", cam="arc", zoom=1.2, at=193.20, slide="left"),
                   clip("hebrew_scroll_edge_light", "static", cam="arc", zoom=1.2, at=194.56, slide="right")])
setb(48, "two_v", [clip("worm_reproach", zoom=1.15, at=198.68, slide="left"),
                   clip("ribs_stretched_macro", "static", cam="arc", at=200.58, slide="right")])
setb(49, "two_v", [clip("clay_potsherd_dust", "static", cam="arc", at=202.35, slide="left"),
                   clip("vesture_seamless_folded", "static", cam="arc", at=203.72, slide="right")])
setb(51, "full", [clip("roads_converge_valley", "static", cam="arc")])
setb(52, "full", [clip("alexandria_harbor_night", "static", cam="arc")])
setb(53, "full", [clip("greek_ot_scroll", "static", cam="arc")])
setb(54, "two_v", [clip("scholar_hand_on_text", "static", at=223.64, slide="left"),
                   clip("water_spilled_stone", "static", cam="arc", zoom=1.2, at=224.43, slide="right")])
setb(55, "full", [clip("seventy_scribes_lamps", "static", cam="arc")])
setb(56, "full", [clip("ribs_stretched_macro", "static", cam="arc", zoom=1.2)])
setb(58, "full", [clip("jerusalem_night_lyre", "static", cam="arc", zoom=1.15)])
setb(59, "two_v", [clip("david_hands_lyre", "static", at=244.18, slide="left"),
                   clip("congregation_hands_lifted", "static", cam="arc", at=245.89, slide="right")])
setb(60, "two_v", [clip("synagogue_listeners_lean", "static", cam="arc", at=248.31, slide="left"),
                   clip("alexandria_harbor_night", "static", cam="arc", zoom=1.2, at=248.42, slide="right")])
setb(61, "full", [clip("cry_profile_dark")])
setb(63, "two_v", [clip("wrists_bound_beam_macro", zoom=1.2, at=265.62, slide="left"),
                   clip("dice_cup_shadow", "static", cam="arc", at=267.42, slide="right")])
setb(64, "two_v", [clip("vesture_seamless_folded", "static", cam="arc", zoom=1.2, at=271.71, slide="left"),
                   clip("john_at_cross_foot", zoom=1.15, at=272.56, slide="right")])
setb(65, "two_v", [clip("hill_crowd_watching_storm", "static", cam="arc", zoom=1.2, at=276.46, slide="left"),
                   clip("spit_shout_macro", "static", cam="arc", zoom=1.2, at=277.14, slide="right")])
setb(66, "full", [clip("tear_track_macro", "static", cam="arc")])
setb(67, "two_v", [clip("golgotha_three_crosses_ridge", zoom=1.15, at=283.19, slide="left"),
                   clip("ninth_hour_darkness", "static", cam="arc", at=284.02, slide="right")])
setb(68, "full", [clip("synagogue_listeners_lean", "static", cam="arc", zoom=1.15)])
setb(73, "full", [clip("clay_potsherd_dust", "static", cam="arc", zoom=1.25)])
setb(74, "full", [clip("kindreds_bowing")])
setb(75, "two_v", [clip("two_scrolls_compared", "static", cam="arc", zoom=1.2, at=315.20, slide="left"),
                   clip("david_scroll_sealed", "static", cam="arc", zoom=1.15, at=317.16, slide="right")])
setb(76, "two_v", [clip("finished_work", at=319.62, slide="left"),
                   clip("grave_clothes_folded_macro", "static", cam="arc", at=320.16, slide="right")])
setb(80, "full", [clip("congregation_hands_lifted", "static", cam="arc", zoom=1.15)])
setb(89, "two_v", [clip("ninth_hour_darkness", "static", cam="arc", zoom=1.2, at=375.47, slide="left"),
                   clip("morning_birds_hill", "static", cam="arc", at=375.97, slide="right")])
setb(90, "full", [clip("substitute_shadow")])
setb(91, "two_v", [clip("parting_storm_light", at=382.61, slide="left"),
                   clip("grave_clothes_folded_macro", "static", cam="arc", zoom=1.2, at=383.81, slide="right")])
setb(92, "two_v", [clip("the_turn", zoom=1.1, at=385.85, slide="left"),
                   clip("risen_hands_raised", "static", at=386.42, slide="right")])
setb(96, "full", [clip("threshold_open_door", "static", cam="arc")])
setb(97, "full", [clip("stone_rolled_groove", "static", cam="arc")])
setb(98, "two_v", [clip("risen_worshipper", "pullback", at=411.33, slide="left"),
                   clip("morning_birds_hill", "static", cam="arc", zoom=1.2, at=412.02, slide="right")])

# ---- 2. drop dyncam overrides where a real clip now exists (batch A + B slugs) ----
CLIPPED = {"worm_reproach", "scholar_hand_on_text", "mocker_faces_trio", "worm_lowest", "dogs_encompass",
           "lion_gape", "kindreds_bowing", "nations_streaming_wide", "dawn_empty_cross", "kneeling_at_cross",
           "hand_reaching_closeup", "vinegar_sponge", "cry_face_tears", "risen_hands_raised", "david_hands_lyre",
           "garment_tug", "ends_of_earth", "cry_profile_dark", "wrists_bound_beam_macro", "substitute_shadow",
           "mockers_below_cross_low", "john_at_cross_foot", "golgotha_three_crosses_ridge"}
for b in B:
    for c in b["clips"]:
        if c["slug"] in CLIPPED and "cam" in c:
            del c["cam"]
            if c.get("motion") == "static":
                c["motion"] = "pushin"

# ---- 3. caption de-slop (no dashes/ellipses/colons on screen) ----
for b in B:
    c = b.get("cap")
    if not c:
        continue
    if c["type"] == "caption":
        t = c["text"].replace(" - ", ". ").replace("Or: like", "Or like").replace("say: this", "say it. This")
        t = t.replace("...", "").replace("ends: God", "ends. God")
        c["text"] = t
    else:
        t = c["text"]
        if t.startswith("..."): t = t[3:]
        if t.endswith("...") and not t.endswith("...."): t = t[:-3].rstrip() if t[:-3].rstrip().endswith(".") else t[:-3].rstrip()
        c["text"] = t
# partial-verse tags instead of ellipses
RETAG = {18: "v.7a", 27: "v.14a", 29: "v.15b", 31: "v.16b", 39: "19:24b", 79: "v.24b", 85: "v.31b"}
for i, ref in RETAG.items():
    B[i - 1]["cap"]["ref"] = ref

# ---- 4. story-keyed SFX (beat-level events, absolute times) ----
SFX = {9: [["rumble_deep_sub", 35.0, -16]], 17: [["air_hollow_desolate", 65.6, -17]],
       18: [["crowd_murmur_distant", 71.2, -16]], 19: [["crowd_shout_mob", 75.1, -15]],
       27: [["air_hollow_desolate", 101.9, -17]], 37: [["coins_clinking", 148.8, -14]],
       43: [["wind_desert_bleak", 176.0, -14]], 45: [["rumble_deep_sub", 183.7, -13]],
       63: [["coins_clinking", 267.4, -16]], 69: [["stone_roll_tomb", 289.3, -12]],
       83: [["dawn_morning_warm", 351.3, -14]], 95: [["crowd_murmur_distant", 396.4, -16]],
       96: [["footsteps_dirt_approach", 400.5, -16]], 98: [["crowd_murmur_distant", 410.6, -17]]}
for i, evs in SFX.items():
    B[i - 1].setdefault("sfx", []).extend(evs)

spec["_doc"] = spec["_doc"] + " V3: distinct-image upgrade (max 2 uses/still, never 2x full-bleed), de-slopped captions, partial tags, story SFX."
(POOL / "livingpage_full.spec.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")

# ---- 5. report usage stats ----
from collections import Counter
cnt = Counter(); fb = Counter()
for b in B:
    for c in b["clips"]:
        cnt[c["slug"]] += 1
        if b["tpl"] == "full":
            fb[c["slug"]] += 1
over = {s: n for s, n in cnt.items() if n > 2}
fb2 = {s: n for s, n in fb.items() if n > 1}
full_beats = sum(1 for b in B if b["tpl"] == "full")
print("distinct stills:", len(cnt), " slots:", sum(cnt.values()))
print("stills used >2x:", over or "NONE")
print("stills full-bleed >1x:", fb2 or "NONE")
print("full-bleed beats:", full_beats, "/", len(B))
dash = [i + 1 for i, b in enumerate(B) if b.get("cap") and ("-" in b["cap"]["text"] or "..." in b["cap"]["text"])]
print("captions w/ dash or ellipsis:", dash or "NONE")
