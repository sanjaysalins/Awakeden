"""WAVE A(a) spec upgrade — pierced (2026-07-14, ROLLOUT_PLAN.md v5.1).

Lighter touch than it_is_finished (already 3 templates, all still-uses legal):
2 grid conversions + the grade arc + smooth/no-ticks + 2 living-light slugs.

Judgment notes (recorded for the wave review):
- look_up_faces = THREE tear-streaked faces looking up -> frac3 on the three mourners
  (the Zech 12:10 mourning itself); anchors eyeballed on each face.
- soldiers_gambling = full scene -> band3: Christ above / the four soldiers / the
  garment + lots on the ground. (Quad too fast for a 2.1s beat.)
- Living-light: grace_poured_sky (beat 12 border-break, "the spirit of grace" — poured
  sky light IS the beat) + risen_mercy_hand (landing "LIVE"). Both figure-light; the
  mercy hand may carry a wound mark — the template's dry-wound lock covers it and the
  push target is the whole arm, never the palm (pilot v2 lesson).
- KJV beats 4 and 8 stay full-bleed sacred heroes, untouched.
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


def frac(i, tpl, anchors, slides, stagger=0.3):
    b = B[i - 1]
    b["tpl"] = tpl
    b["anchors"] = anchors
    b["panel_at"] = [round(b["t"][0] + k * stagger, 2) for k in range(len(anchors))]
    b["panel_slide"] = slides
    b["flash"] = True


# 9 DYING MAN: Christ above / four soldiers / garment+lots (whip kept)
frac(9, "hero_band3", [[1.15, 0.6, 0.15], [1.3, 0.5, 0.6], [1.8, 0.5, 0.85]],
     ["up", "left", "down"], stagger=0.25)
# 13 TEARS: the three mourners' faces (whip kept)
frac(13, "hero_frac3", [[1.6, 0.17, 0.32], [1.8, 0.52, 0.47], [1.8, 0.8, 0.4]],
     ["left", "up", "right"], stagger=0.28)

# grade arc: piercing/mourning cool -> grace poured -> LIVE warmest
FX = {1: 7400, 2: 7000, 4: 7600, 5: 7700, 6: 7400, 8: 7900, 9: 7600, 10: 7200,
      12: 6000, 13: 5800, 14: 5600, 15: 5400, 16: 5200, 17: 4900}
for i, k in FX.items():
    B[i - 1]["fx"] = {"temp": k}

SPEC.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"spec upgraded: smooth, no ticks, grids on 9+13, fx on {len(FX)}/17")

pj_p = PIECE / "piece.json"
pj = json.loads(pj_p.read_text(encoding="utf-8"))
pj["animate"]["living_light"] = {
    "grace_poured_sky": {
        "target": "the light pouring from the opened sky",
        "light": "the poured light from the opened sky slowly intensifies, its rays "
                 "widening and sweeping gently, warm haze drifting where the light meets "
                 "the ground"},
    "risen_mercy_hand": {
        "target": "the whole outstretched arm and the light around it",
        "light": "the glow around the outstretched arm slowly builds and breathes, soft "
                 "rays fanning outward, warm haze shimmering at the edges of the light"},
}
pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("piece.json: living_light = grace_poured_sky (reveal) + risen_mercy_hand (landing)")
