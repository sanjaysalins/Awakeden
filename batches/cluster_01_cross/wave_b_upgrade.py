"""WAVE B spec upgrades — forsaken_cry, i_thirst, into_thy_hands, today_paradise
(2026-07-14, ROLLOUT_PLAN.md v5.1 + the Wave A clean-light target rule).

Anchors from eyeballed stills (proven anchors reused where the same sibling still was
already studied in Wave A: david_writing, golgotha_hill, us_under_cross, look_up_faces,
face_on_cross bands). confession_face_hands is the ONE formulaic-anchor exception
(center face / center hands) — flagged for the build eye-check.

Living-light (clean-light rule): every target is a light-source scene or figure-free —
living_water_stream, hands_of_light_open, kingdom_light_clouds, paradise_dawn (distant
figure at dawn-walker scale). cross_at_dawn + grace_poured_sky slots are $0 sibling
copies of Wave A keepers (byte-identity verified by the copy script, never re-rolled).
KJV/sacred beats stay full-bleed everywhere; no living-light on any painted-blood still.
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# proven anchor sets (Wave A eyeballed stills, same sibling compositions)
DAVID = [[1.0, 0.5, 0.45], [1.8, 0.45, 0.3], [1.9, 0.55, 0.62]]
GOLGOTHA = [[1.0, 0.5, 0.2], [1.25, 0.5, 0.5], [1.35, 0.5, 0.8]]
US_UNDER = [[1.2, 0.5, 0.28], [1.35, 0.5, 0.55], [1.5, 0.5, 0.8]]
LOOK_UP = [[1.6, 0.17, 0.32], [1.8, 0.52, 0.47], [1.8, 0.8, 0.4]]
FACE_CROSS = [[1.3, 0.35, 0.22], [1.4, 0.68, 0.5], [1.2, 0.5, 0.8]]
FATHER_LAMP = [[1.0, 0.5, 0.5], [2.0, 0.47, 0.42], [2.2, 0.56, 0.56]]

CROSS_DAWN_LL = {"target": "the empty cross on the hilltop",
                 "light": "the great dawn sun behind the cross slowly intensifies, its rays "
                          "sweeping gently across the sky, warm haze shimmering over the rocks below"}
GRACE_LL = {"target": "the light pouring from the opened sky",
            "light": "the poured light from the opened sky slowly intensifies, its rays "
                     "widening and sweeping gently, warm haze drifting where the light meets "
                     "the ground"}

PIECES = {
    "forsaken_cry_ps221": {
        "grids": [
            (2, "hero_frac3", DAVID, ["left", "right", "up"], 0.4),
            (3, "hero_band3", GOLGOTHA, ["up", "left", "down"], 0.35),
            (4, "hero_band3", US_UNDER, ["up", "left", "down"], 0.25),
            (8, "hero_frac3", LOOK_UP, ["left", "up", "right"], 0.28),
            (9, "hero_band3", FACE_CROSS, ["up", "left", "down"], 0.4),
            (12, "hero_frac3", FATHER_LAMP, ["left", "right", "up"], 0.35),
        ],
        "fx": {1: 7400, 3: 7200, 4: 7400, 6: 7800, 7: 7900, 8: 7000, 9: 7600,
               10: 5800, 11: 5400, 12: 5200, 13: 4900},
        "living_light": {"grace_poured_sky": GRACE_LL, "cross_at_dawn": CROSS_DAWN_LL},
    },
    "i_thirst_john1928": {
        "grids": [
            (1, "hero_band3", [[1.0, 0.5, 0.2], [1.25, 0.5, 0.5], [1.35, 0.5, 0.8]],
             ["up", "left", "down"], 0.35),
            (2, "hero_band3", FACE_CROSS, ["up", "left", "down"], 0.3),
            (3, "hero_frac3", DAVID, ["left", "right", "up"], 0.4),
            (4, "hero_band3", US_UNDER, ["up", "left", "down"], 0.25),
            (9, "hero_frac3", [[1.0, 0.5, 0.5], [1.8, 0.55, 0.42], [1.6, 0.75, 0.12]],
             ["left", "right", "up"], 0.45),
        ],
        "fx": {2: 7400, 4: 7400, 5: 7700, 6: 7000, 7: 7900, 8: 7800, 9: 7000,
               10: 5600, 11: 5200, 12: 4900},
        "living_light": {
            "living_water_stream": {
                "target": "the falling stream of water",
                "light": "the falling water flows gently and continuously, sunlight playing "
                         "softly across the stream and the pool, thin mist drifting off the splash"},
            "cross_at_dawn": CROSS_DAWN_LL},
    },
    "into_thy_hands_luke2346": {
        "grids": [
            (1, "hero_band3", GOLGOTHA, ["up", "left", "down"], 0.3),
            (2, "hero_frac3", [[1.0, 0.5, 0.5], [1.8, 0.5, 0.68], [1.6, 0.3, 0.28]],
             ["left", "right", "up"], 0.4),
            (4, "hero_band3", FACE_CROSS, ["up", "left", "down"], 0.3),
            (7, "hero_frac3", [[1.0, 0.5, 0.5], [1.5, 0.45, 0.5], [1.9, 0.78, 0.72]],
             ["left", "right", "up"], 0.35),
            (8, "hero_frac3", FATHER_LAMP, ["left", "right", "up"], 0.32),
            (12, "hero_frac3", [[1.0, 0.5, 0.5], [1.7, 0.38, 0.28], [1.8, 0.35, 0.68]],
             ["left", "up", "right"], 0.4),
        ],
        "fx": {3: 7000, 4: 7600, 5: 7900, 6: 7400, 7: 6400, 8: 6000, 9: 6800,
               10: 5800, 11: 5600, 12: 5400, 13: 5200, 14: 4900},
        "living_light": {
            "hands_of_light_open": {
                "target": "the open hands in the parted clouds",
                "light": "the light streaming from the open hands slowly intensifies, the rays "
                         "lengthening and sweeping downward, the glow between the parted clouds "
                         "breathing brighter"},
            "cross_at_dawn": CROSS_DAWN_LL},
    },
    "today_paradise_luke2343": {
        "grids": [
            (1, "hero_band3", GOLGOTHA, ["up", "left", "down"], 0.25),
            (7, "hero_frac3", [[1.6, 0.5, 0.22], [1.9, 0.19, 0.3], [1.9, 0.82, 0.32]],
             ["up", "left", "right"], 0.5),
            (8, "hero_frac3", [[1.0, 0.5, 0.5], [1.7, 0.5, 0.35], [1.8, 0.5, 0.65]],
             ["left", "right", "up"], 0.4),   # formulaic — eye-check at build
        ],
        "fx": {2: 7400, 4: 7600, 5: 7800, 6: 7200, 7: 7900, 8: 7000, 9: 6000,
               10: 5800, 11: 5400, 13: 7000, 14: 6400, 15: 5000, 16: 4900},
        "living_light": {
            "kingdom_light_clouds": {
                "target": "the pillar of light through the parted storm",
                "light": "the great pillar of light slowly widens and brightens, the dark "
                         "clouds parting almost imperceptibly, its rays sweeping the hills below"},
            "paradise_dawn": {
                "target": "the sunrise beyond the distant figure on the hill",
                "light": "the dawn rays streaming past the distant figure slowly strengthen "
                         "and sweep across the garden, the soft mist drifting slowly between "
                         "the olive trees"}},
    },
}

for name, plan in PIECES.items():
    piece = ROOT / name
    spec_p = piece / "visual" / "livingpage_short.spec.json"
    spec = json.loads(spec_p.read_text(encoding="utf-8"))
    shutil.copy2(spec_p, spec_p.with_suffix(".json.bak_prewave"))
    spec["motion"] = "smooth"
    spec["cut_ticks"] = False
    B = spec["beats"]
    for i, tpl, anchors, slides, stagger in plan["grids"]:
        b = B[i - 1]
        b["tpl"] = tpl
        b["anchors"] = anchors
        b["panel_at"] = [round(b["t"][0] + k * stagger, 2) for k in range(len(anchors))]
        b["panel_slide"] = slides
        b["flash"] = True
        b.pop("takeover", None)      # slams carry the beat now; a takeover would fight them
    for i, k in plan["fx"].items():
        B[i - 1]["fx"] = {"temp": k}
    spec_p.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    pj_p = piece / "piece.json"
    pj = json.loads(pj_p.read_text(encoding="utf-8"))
    pj["animate"]["living_light"] = plan["living_light"]
    pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{name}: grids {[g[0] for g in plan['grids']]}, fx {len(plan['fx'])} beats, "
          f"living_light {list(plan['living_light'])}")
