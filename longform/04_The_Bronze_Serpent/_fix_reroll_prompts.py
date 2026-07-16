"""Patch 5 defective scene subject_blocks found by the agent's eye-audit
(2026-07-16) and delete their PNGs so _render_inked_stills.py --only rerolls
them. Defects: #12/#16/#18 rendered ROPE at the wrists instead of NAILS
(project-standing trap, memory `crucifixion-still-facts`: "nails->rope");
#14 rendered a foreground face close-up when the spec explicitly banned any
foreground figure (wanted a wide landscape); #25 rendered a second figure +
rope on the tiny distant cross. $0, no render (this script only edits text)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked"
p = OUT / "scene_plan.json"
d = json.loads(p.read_text(encoding="utf-8"))

NAIL_FIX = (" a single large iron nail driven straight through the centre of EACH wrist, "
            "the dark round nail head clearly visible on the front of each wrist, blood "
            "only at the small nail wound itself -- absolutely NOT rope, NOT cord, NOT "
            "leather strap, NOT tied or bound,")

by_id = {s["id"]: s for s in d["scenes"]}

# #12, #16, #18: force nails, strip the "wrists fastened to the wood" phrase that the
# model kept reading as an invitation to tie rope.
for sid in (12, 16, 18):
    s = by_id[sid]
    sb = s["subject_block"]
    sb = sb.replace(
        "both arms outstretched and NAILED to the crossbeam, wrists fastened to the wood,",
        "both arms outstretched," + NAIL_FIX)
    s["subject_block"] = sb

# #14: the model defaulted to a foreground face despite "NO foreground figure NO portrait
# NO close-up person" being present -- move the ban to the very front, add an explicit
# camera instruction, and repeat the ban at the end as a final guard.
s14 = by_id[14]
s14["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black linework, AERIAL "
    "WIDE LANDSCAPE ONLY, camera high above the earth looking down and out across the "
    "whole land -- ABSOLUTELY NO PERSON, NO FACE, NO FIGURE, NO PORTRAIT anywhere in "
    "frame, this is an empty landscape shot: a vast darkened world at the ninth hour "
    "-- open wilderness and a distant first-century city under a great storm-dark sky "
    "-- with broad warm shafts of golden light breaking through the heavy clouds and "
    "pouring down across the whole land onto a small distant cross on its far hill, the "
    "cross tiny and far away on the horizon, the darkness giving way to a deep tender "
    "radiance, the love of God breaking over the whole world; reverent, hopeful, deep "
    "ink shadow at the edges, REMEMBER: no human figure anywhere in this frame, one "
    "continuous image, no frame, no panels, no border, no text"
)

# #25: force exactly one foreground figure (no second bending-over figure) + nails on
# the tiny distant cross too.
s25 = by_id[25]
sb = s25["subject_block"]
sb = sb.replace(
    "in the foreground a bitten dying Israelite on the desert ground, weak and unable "
    "to heal himself, his hand open and empty;",
    "in the foreground EXACTLY ONE bitten dying Israelite lying alone on the desert "
    "ground -- no second person, no one kneeling over him, no companion figure -- weak "
    "and unable to heal himself, his hand open and empty;")
sb = sb.replace(
    "the robed Christ CRUCIFIED",
    "the robed Christ CRUCIFIED, a tiny nail-head visible at each wrist (NOT rope, NOT "
    "cord),", 1)
s25["subject_block"] = sb

p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print("patched subject_block for scenes 12, 14, 16, 18, 25")

# delete the stale PNGs so the render script treats them as missing
REROLL_FILES = ["12_even_so_must_the_son_of_man_be_lifted_up.png", "14_for_god_so_loved_the_world.png",
                 "16_the_likeness_of_the_curse_lifted_up.png", "18_curse.png",
                 "25_we_are_all_bitten__the_cure_outside_us.png"]
for fn in REROLL_FILES:
    fp = OUT / fn
    if fp.exists():
        fp.unlink()
        print(f"deleted {fp.name} for reroll")
