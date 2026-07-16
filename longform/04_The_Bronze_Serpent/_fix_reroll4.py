"""Round 4: scene 25's nail rendering still hallucinated rope binding the wrist
below the nail (visible in the reroll3 render), despite the prompt repeatedly
saying "NOT rope, NOT cord, NOT bound". Memory `seedream-no-negative-channel`
locked exactly this failure mode: naming a forbidden noun repeatedly DRAWS it,
because these models have no true negative channel. Rewrite scene 25's cross
description POSITIVE-ONLY (no "not rope" language at all) and describe the
nail as a flat coin-sized disc, not a giant sphere. $0, no render (text only).
Run _render_inked_stills.py --only 25 after this to reroll."""
import json
from pathlib import Path

p = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\longform\04_The_Bronze_Serpent\v1\visual_16x9_inked\scene_plan.json")
d = json.loads(p.read_text(encoding="utf-8"))
by_id = {s["id"]: s for s in d["scenes"]}

s25 = by_id[25]
s25["subject_block"] = (
    "a single seamless full-bleed inked graphic-novel panel, bold black "
    "linework, DEEP intimate composition, tender and grave: in the "
    "foreground EXACTLY ONE bitten dying Israelite lying alone on the desert "
    "ground -- no second person, no one kneeling over him, no companion "
    "figure -- weak and unable to heal himself, his hand open and relaxed, "
    "anatomically normal and whole with all five fingers, a small pair of "
    "red puncture-mark snakebite dots on the back of the hand, subtle and "
    "realistic; far beyond and above him, small and luminous against the "
    "dark, the robed Christ crucified, both arms outstretched along the "
    "crossbeam, each bare wrist pressed flat against the plain wood with "
    "clean skin visible all around it, a single flat coin-sized iron nail "
    "head lying flush against the centre of each wrist, a thin trickle of "
    "blood below each nail, plain wood grain touching skin directly on "
    "every other side of the wrist, body hanging, head bowed, robed at the "
    "waist, hands with five fingers each, on its distant cross -- the cure "
    "never inside the dying man but hanging entirely outside him; reverent, "
    "no text, one continuous image, no frame, no panels, no border, no text"
)

p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
print("patched subject_block for scene 25 (positive-only nail description)")

OUT = p.parent
fp = OUT / "25_we_are_all_bitten__the_cure_outside_us.png"
if fp.exists():
    fp.unlink()
    print(f"deleted {fp.name} for reroll")
