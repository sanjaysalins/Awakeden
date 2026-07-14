"""WAVE A(a) spec upgrade — crucifixion_foretold (2026-07-14, ROLLOUT_PLAN.md v5.1).

86% full-bleed -> 4 grid conversions (57%), grade arc, smooth/no-ticks, 2 living-light.

Judgment notes (recorded for the wave review):
- crowd_mocking frac3 on the THREE foreground shouting faces (crowd behind is already
  shadow-silhouette per the standard); slams land before the 26.6s heartbeat hush begins.
- david_writing_psalm frac3 = wide / face / quill-hand+lamp — panels deliberately avoid
  framing the scroll TEXT close-up (writing stays un-animated and un-scrutinized).
- golgotha_hill_wide + us_under_cross_shadow reuse the band anchors proven on the same
  stills in it_is_finished.
- living_light: jesus_looks_down (the gospel-pivot beat "A NAME: JESUS") +
  risen_mercy_hand (landing "TO WIN YOU BACK"). NOTE: pierced's landing uses the same
  risen_mercy_hand still — at A(b), verify byte-identical siblings and COPY the first
  QC-passed clip ($0) instead of paying for a second render.
- KJV beats 7 and 9 stay full-bleed sacred heroes, untouched.
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


# 3 NEVER EXECUTED: David writing - wide / face / quill-hand+lamp (long beat, slow build)
frac(3, "hero_frac3", [[1.0, 0.5, 0.45], [1.8, 0.45, 0.3], [1.9, 0.55, 0.62]],
     ["left", "right", "up"], stagger=0.4)
# 4 SOMEONE ELSE: golgotha bands (anchors proven on the same still in it_is_finished)
frac(4, "hero_band3", [[1.0, 0.5, 0.2], [1.25, 0.5, 0.5], [1.35, 0.5, 0.8]],
     ["up", "left", "down"], stagger=0.28)
# 6 WATCH ONE LINE: the three mocking faces (whip kept; slams clear the heartbeat)
frac(6, "hero_frac3", [[1.6, 0.2, 0.55], [1.7, 0.5, 0.48], [1.7, 0.82, 0.52]],
     ["left", "up", "right"], stagger=0.4)
# 10 NO ACCIDENT: kneelers + cross shadow bands (proven anchors)
frac(10, "hero_band3", [[1.2, 0.5, 0.28], [1.35, 0.5, 0.55], [1.5, 0.5, 0.8]],
     ["up", "left", "down"], stagger=0.5)

# grade arc: prophecy night -> fulfillment coolest -> A NAME: JESUS thaw -> landing warm
FX = {2: 7000, 4: 7200, 5: 7600, 6: 7400, 7: 7900, 8: 7300, 9: 7700, 10: 7400,
      11: 6800, 12: 6000, 13: 5600, 14: 4900}
for i, k in FX.items():
    B[i - 1]["fx"] = {"temp": k}

SPEC.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"spec upgraded: smooth, no ticks, grids on 3,4,6,10, fx on {len(FX)}/14")

pj_p = PIECE / "piece.json"
pj = json.loads(pj_p.read_text(encoding="utf-8"))
pj["animate"]["living_light"] = {
    "jesus_looks_down": {
        "target": "the whole figure on the cross seen from below",
        "light": "the pale light around the cross slowly deepens and breathes, a soft "
                 "glow gathering behind the crossbeam while thin haze drifts below"},
    "risen_mercy_hand": {
        "target": "the whole outstretched arm and the light around it",
        "light": "the glow around the outstretched arm slowly builds and breathes, soft "
                 "rays fanning outward, warm haze shimmering at the edges of the light"},
}
pj_p.write_text(json.dumps(pj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("piece.json: living_light = jesus_looks_down (gospel pivot) + risen_mercy_hand (landing)")
