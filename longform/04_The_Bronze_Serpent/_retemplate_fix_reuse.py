"""Fix the 3 reuse_violations the --lint pass surfaced after _retemplate_variety.py:
  - B42 split_v: 'reuse_bowed_head_finished' landed on the SAME crop as its beat-30
    use (same aspect, no override) -- give B42's panel a distinct zoom so the crop
    differs, satisfying the R2 reuse rule's "different crop" half.
  - B47/B49/B52 all used '21_look_to_the_one_lifted_up_hero_close' within a 5-beat
    span (gaps 2 and 3, need >=8) -- this was PRE-EXISTING (all three already
    referenced it before this session's changes). Swap B47 and B49 to different
    already-available, thematically-fitting Christ images so the true closing
    hero shot at B52 is the only survivor near the end (best practice: the hero
    bookend should not be diluted by lookalikes right before the close anyway).
$0, text only."""
import json
from pathlib import Path

p = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1\visual_16x9_inked\livingpage_full.spec.json")
d = json.loads(p.read_text(encoding="utf-8"))
beats = d["beats"]


def find(idx1based):
    return beats[idx1based - 1]


# B42 split_v: differentiate the bowed-head crop from its beat-30 use
b = find(42)
assert b["clips"][1]["slug"] == "reuse_bowed_head_finished"
b["clips"][1]["zoom"] = 1.35

# B47 two_v: swap the hero-close lookalike for the face-on-cross reuse clip
b = find(47)
assert b["clips"][1]["slug"] == "21_look_to_the_one_lifted_up_hero_close"
b["clips"][1] = {"slug": "reuse_face_on_cross"}

# B49 full: swap for the risen-mercy-hand reuse clip
b = find(49)
assert b["clips"][0]["slug"] == "21_look_to_the_one_lifted_up_hero_close"
b["clips"][0] = {"slug": "reuse_risen_mercy_hand"}

p.write_text(json.dumps(d, indent=1), encoding="utf-8")
print("fixed reuse violations: B42 crop, B47 swap, B49 swap")
