"""WAVE C spec upgrades — watch_one_hour, woman_behold, thirty_pieces
(2026-07-14, ROLLOUT_PLAN.md v5.1 + clean-light target rule).

All anchors from eyeballed stills (10 viewed this wave; zechariah_night_scroll reuses the
proven David-writing-family anchors — flagged for the build eye-check like confession was).
Living-light: cup_moonlight + us_under (sunset) + simeon temple shaft + scattered silver —
all clean-light (still-lifes / light shafts / no painted blood). risen_mercy_hand lands
woman_behold + thirty_pieces as $0 sibling copies. KJV sacred beats stay full."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
FACE_CROSS = [[1.3, 0.35, 0.22], [1.4, 0.68, 0.5], [1.2, 0.5, 0.8]]
GOLGOTHA = [[1.0, 0.5, 0.2], [1.25, 0.5, 0.5], [1.35, 0.5, 0.8]]
DAVID = [[1.0, 0.5, 0.45], [1.8, 0.45, 0.3], [1.9, 0.55, 0.62]]
MERCY_LL = {"target": "the whole outstretched arm and the light around it",
            "light": "the glow around the outstretched arm slowly builds and breathes, soft "
                     "rays fanning outward, warm haze shimmering at the edges of the light"}

PIECES = {
    "watch_one_hour_matt2640": {
        "grids": [
            (1, "hero_frac3", [[1.7, 0.24, 0.72], [1.7, 0.5, 0.7], [1.7, 0.78, 0.72]],
             ["left", "up", "right"], 0.3),
            (2, "hero_band3", [[1.0, 0.5, 0.25], [1.25, 0.5, 0.55], [1.3, 0.5, 0.8]],
             ["up", "left", "down"], 0.28),
            (4, "hero_frac3", [[1.0, 0.5, 0.5], [1.7, 0.5, 0.4], [1.6, 0.8, 0.15]],
             ["left", "right", "up"], 0.25),
            (12, "hero_frac3", [[1.0, 0.5, 0.5], [1.8, 0.6, 0.55], [1.7, 0.72, 0.15]],
             ["left", "right", "up"], 0.35),
            (13, "hero_band3", FACE_CROSS, ["up", "left", "down"], 0.28),
        ],
        "fx": {2: 7000, 4: 7200, 5: 7400, 6: 7600, 7: 7300, 8: 7900, 9: 5800, 10: 6800,
               11: 7000, 12: 7400, 13: 7600, 14: 6400, 15: 6000, 16: 4900},
        "living_light": {
            "cup_moonlight": {
                "target": "the stone cup on the moonlit rock",
                "light": "the moonlight over the cup slowly brightens and softens, the "
                         "olive-branch shadows breathing across the rock, thin night mist "
                         "drifting low"},
            "us_under_cross_shadow": {
                "target": "the cross against the sunset",
                "light": "the sunset glow beyond the cross slowly warms and breathes, the "
                         "long cross shadow softening, thin dusk haze drifting over the sand"}},
    },
    "woman_behold_john1926": {
        "grids": [
            (3, "hero_band3", GOLGOTHA, ["up", "left", "down"], 0.35),
            (5, "hero_frac3", [[1.7, 0.3, 0.5], [1.9, 0.4, 0.63], [1.5, 0.8, 0.3]],
             ["left", "up", "right"], 0.45),
            (6, "hero_band3", FACE_CROSS, ["up", "left", "down"], 0.45),
            (11, "hero_band3", [[1.3, 0.3, 0.15], [1.5, 0.65, 0.45], [1.2, 0.5, 0.8]],
             ["up", "left", "down"], 0.4),
        ],
        "fx": {2: 7000, 3: 7200, 4: 7400, 5: 7600, 6: 7700, 7: 7900, 8: 7500, 9: 6400,
               10: 6000, 11: 7000, 12: 6400, 13: 4900},
        "living_light": {
            "simeon_baby_temple": {
                "target": "the temple light shaft over the lifted child",
                "light": "the temple light shaft over the lifted child slowly brightens and "
                         "widens, warm haze drifting between the pillars"},
            "risen_mercy_hand": MERCY_LL},
    },
    "thirty_pieces_zech11": {
        "grids": [
            (3, "hero_frac3", DAVID, ["left", "right", "up"], 0.4),
            (4, "hero_frac3", [[1.6, 0.5, 0.18], [1.8, 0.25, 0.62], [1.8, 0.75, 0.72]],
             ["up", "left", "right"], 0.28),
            (8, "hero_frac3", [[1.5, 0.5, 0.45], [1.4, 0.5, 0.65], [1.5, 0.2, 0.15]],
             ["left", "right", "up"], 0.4),
            (9, "hero_frac3", [[1.6, 0.5, 0.42], [1.8, 0.13, 0.5], [1.8, 0.87, 0.48]],
             ["up", "left", "right"], 0.25),
            (10, "hero_frac3", [[1.6, 0.5, 0.4], [1.7, 0.42, 0.15], [1.8, 0.85, 0.55]],
             ["left", "up", "right"], 0.3),
        ],
        "fx": {3: 7000, 4: 7300, 5: 7600, 7: 7400, 8: 6800, 9: 7500, 10: 7700, 11: 7300,
               12: 7900, 13: 7000, 14: 7800, 15: 7400, 16: 7600, 17: 6400, 18: 4900},
        "living_light": {
            "thirty_coins_scatter": {
                "target": "the scattered silver on the temple stones",
                "light": "the cold light across the scattered silver slowly shifts and "
                         "breathes, the shadows of the temple steps deepening and softening"},
            "risen_mercy_hand": MERCY_LL},
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
        b.pop("takeover", None)
    for i, k in plan["fx"].items():
        B[i - 1]["fx"] = {"temp": k}
    # living-light hook beats keep their full-bleed but lose any takeover (motion-on-motion)
    for b in B:
        if {c["slug"] for c in b["clips"]} & set(plan["living_light"]):
            b.pop("takeover", None)
            for c in b["clips"]:
                c.pop("cam", None)   # a cam key would dyncam-discard the paid clip
    spec_p.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    pj_p = piece / "piece.json"
    pj = json.loads(pj_p.read_text(encoding="utf-8"))
    pj["animate"]["living_light"] = plan["living_light"]
    pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{name}: grids {[g[0] for g in plan['grids']]}, fx {len(plan['fx'])}, "
          f"ll {list(plan['living_light'])}")
