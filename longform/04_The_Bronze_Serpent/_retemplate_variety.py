"""Round 2 (user, 2026-07-16): "not using all the rich grid templates we have in
our collection" -- comic_engine.py defines 11 templates (full, two_v, split_v,
stack_h, big_inset, triptych_v, strip_h3, quad, hero_frac3, hero_frac4,
hero_band3) but the dense rebuild only ever used 5. Convert 7 of the longest
single-image "full" holds (the beats that read most like a slideshow -- "full"
never gets a slam event, see build_livingpage_16x9.py main()) into the 6
templates that had zero real usage, picked so no R2 reuse-gap rule (>=8 beats
between reuses of the same still, memory `feedback-no-reuse-beat-match`) is
broken -- verified after the fact with `--lint`.

  B10 (22.92s, single) -> hero_frac4  (fracture-of-self, zero reuse risk)
  B11 (12.56s, redletter) -> hero_frac4  (fracture-of-self, sacred-safe: no
       panel_at means simultaneous reveal, no slam/flash -- stillness intact)
  B17 (13.24s, redletter) -> hero_band3  (fracture-of-self, sacred-safe)
  B29 (12.96s) -> stack_h  (2 distinct: own two related "lifted up" stills)
  B33 (17.22s) -> quad  (4 distinct: a callback montage of early-film beats)
  B42 (9.00s)  -> split_v (2 distinct: nail + bowed-head reuse clips)
  B44 (10.10s) -> strip_h3 (3 distinct: three "looking" beats)

$0, text only. Run build_livingpage_16x9.py --lint after this to verify DoD +
zero reuse_violations before a full render."""
import json
from pathlib import Path

p = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1\visual_16x9_inked\livingpage_full.spec.json")
d = json.loads(p.read_text(encoding="utf-8"))
beats = d["beats"]


def find(idx1based):
    return beats[idx1based - 1]


# B10 -> hero_frac4 (fracture-of-self '22_curse', 4 crops)
b = find(10)
assert b["clips"][0]["slug"] == "22_curse"
b["tpl"] = "hero_frac4"
b["anchors"] = [[1.6, 0.5, 0.30], [1.4, 0.22, 0.62], [1.4, 0.78, 0.55], [1.1, 0.5, 0.72]]
b["flash"] = False

# B11 -> hero_frac4 (fracture-of-self '08_raised', 4 crops) -- sacred, no panel_at
b = find(11)
assert b["clips"][0]["slug"] == "08_raised"
b["tpl"] = "hero_frac4"
b["anchors"] = [[1.3, 0.5, 0.18], [1.6, 0.5, 0.45], [1.3, 0.25, 0.75], [1.3, 0.75, 0.78]]
b["flash"] = False

# B17 -> hero_band3 (fracture-of-self '12_even_so...', 3 stacked rows) -- sacred
b = find(17)
assert b["clips"][0]["slug"] == "12_even_so_must_the_son_of_man_be_lifted_up"
b["tpl"] = "hero_band3"
b["anchors"] = [[1.5, 0.5, 0.22], [1.3, 0.5, 0.5], [1.5, 0.5, 0.8]]
b["flash"] = False

# B29 -> stack_h (2 rows): the curse-typology still + the "lifted up" still
b = find(29)
assert b["clips"][0]["slug"] == "16_the_likeness_of_the_curse_lifted_up"
b["tpl"] = "stack_h"
b["clips"] = [{"slug": "16_the_likeness_of_the_curse_lifted_up"},
              {"slug": "12_even_so_must_the_son_of_man_be_lifted_up"}]

# B33 -> quad: a 4-up callback montage (early-film beats recalled under the
# "look of faith" line)
b = find(33)
assert b["clips"][0]["slug"] == "18_curse"
b["tpl"] = "quad"
b["clips"] = [{"slug": "18_curse"}, {"slug": "02_worn_down_they_despise_the_bread_of_heaven"},
              {"slug": "04_venom"}, {"slug": "06_not"}]

# B42 -> split_v: nail + bowed-head (both reuse_ Cross-cluster clips)
b = find(42)
assert b["clips"][0]["slug"] == "reuse_nail_through_hand"
b["tpl"] = "split_v"
b["clips"] = [{"slug": "reuse_nail_through_hand"}, {"slug": "reuse_bowed_head_finished"}]

# B44 -> strip_h3: three "looking" beats
b = find(44)
assert b["clips"][0]["slug"] == "20_whosoever"
b["tpl"] = "strip_h3"
b["clips"] = [{"slug": "20_whosoever"}, {"slug": "09_look"},
              {"slug": "05_they_beg_moses_take_the_serpents_away"}]

p.write_text(json.dumps(d, indent=1), encoding="utf-8")
print("retemplated beats 10, 11, 17, 29, 33, 42, 44")
