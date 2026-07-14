"""WAVE A(a) spec upgrade — it_is_finished (2026-07-14, ROLLOUT_PLAN.md v5.1).

Grid conversion (anchors placed from eyeballing the stills), cold->warm grade arc,
smooth motion, cut_ticks off, 2 living-light slugs. Beat timings untouched (audio-locked).

Judgment notes (recorded for the wave review):
- nail_through_hand shows dripping blood in the STILL -> living-light there would bait
  the pilot's v2 bleeding-wound failure; it keeps its camera-only move. The Christ-CU
  proof is bowed_head_finished (thorn-crown face CU = the expression-lock stress test).
- carpenter_bench_rest has NO figure (empty bench + light shaft) -> frac3 wide/tools/light.
- tomb_stone_sealed is a wide dusk scene w/ two departing figures -> frac3 wide/stone/figures.
- man_lifting_face_dawn is a single face CU -> stays FULL (never shatter a single face).
"""
import json
import shutil
from pathlib import Path

PIECE = Path(__file__).parent
SPEC = PIECE / "visual" / "livingpage_short.spec.json"

spec = json.loads(SPEC.read_text(encoding="utf-8"))
shutil.copy2(SPEC, SPEC.with_suffix(".json.bak_prewave"))
spec["motion"] = "smooth"
spec["cut_ticks"] = False
B = spec["beats"]


def frac(i, tpl, anchors, slides, stagger=0.3, first_at=None):
    b = B[i - 1]
    t0 = b["t"][0]
    b["tpl"] = tpl
    b["anchors"] = anchors
    n = len(anchors)
    at0 = t0 if first_at is None else first_at
    b["panel_at"] = [round(at0 + k * stagger, 2) for k in range(n)]
    b["panel_slide"] = slides
    b["flash"] = True


# 1 HOOK: eden valley band tour (punch kept; ramp/takeover dropped - slams carry it)
frac(1, "hero_band3", [[1.0, 0.5, 0.18], [1.2, 0.5, 0.5], [1.3, 0.5, 0.8]],
     ["up", "left", "down"])
B[0].pop("ramp", None); B[0].pop("takeover", None)
# 3 HALF DONE: empty bench frac3 - wide / tools CU / light shaft
frac(3, "hero_frac3", [[1.0, 0.5, 0.45], [1.9, 0.5, 0.42], [1.6, 0.5, 0.15]],
     ["left", "right", "up"])
# 4 TO MEND IT: golgotha wide bands (whip kept)
frac(4, "hero_band3", [[1.0, 0.5, 0.2], [1.25, 0.5, 0.5], [1.35, 0.5, 0.8]],
     ["up", "left", "down"], stagger=0.28)
# 7 HE PRAYED: night grove bands (1.8s -> tight stagger)
frac(7, "hero_band3", [[1.0, 0.5, 0.25], [1.25, 0.5, 0.55], [1.3, 0.5, 0.8]],
     ["left", "right", "left"], stagger=0.25)
# 9 TO THE END: kneelers+cross / shadow-fall / long shadow (1.6s, whip kept)
frac(9, "hero_band3", [[1.2, 0.5, 0.28], [1.35, 0.5, 0.55], [1.5, 0.5, 0.8]],
     ["up", "left", "down"], stagger=0.25)
# 13 RESTED: tomb frac3 - wide dusk / stone CU / the two departing figures
frac(13, "hero_frac3", [[1.0, 0.5, 0.4], [1.7, 0.5, 0.35], [2.2, 0.63, 0.7]],
     ["left", "right", "up"], stagger=0.42)

# grade arc: creation neutral -> death coolest -> RESTED thaw -> ENTER HIS REST warmest
FX = {4: 7200, 6: 7600, 7: 7000, 9: 7400, 10: 7900, 11: 7700,
      12: 6800, 13: 6800, 14: 5800, 15: 5400, 16: 5200, 17: 4900}
for i, k in FX.items():
    B[i - 1]["fx"] = {"temp": k}

SPEC.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"spec upgraded: motion=smooth cut_ticks=false grids on 1,3,4,7,9,13 fx on {len(FX)}/17")

pj_p = PIECE / "piece.json"
pj = json.loads(pj_p.read_text(encoding="utf-8"))
pj["animate"]["living_light"] = {
    "bowed_head_finished": {
        "target": "the bowed, thorn-crowned head",
        "light": "the dim light behind the bowed figure breathes almost imperceptibly, a "
                 "faint pale glow slowly rising around the silhouette while the darkness "
                 "softens toward the horizon"},
    "cross_at_dawn": {
        "target": "the empty cross on the hilltop",
        "light": "the great dawn sun behind the cross slowly intensifies, its rays sweeping "
                 "gently across the sky, warm haze shimmering over the rocks below"},
}
pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("piece.json: living_light = bowed_head_finished (Christ-CU proof) + cross_at_dawn (landing)")
