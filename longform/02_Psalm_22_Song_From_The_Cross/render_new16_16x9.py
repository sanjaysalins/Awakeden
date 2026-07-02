#!/usr/bin/env python
"""Render the 16 NEW inked 16:9 stills for the FULL Psalm-22 long (mocomic_16x9_full.spec.json).

Reuses the LOCKED BytePlus Seedream 4.5 client + ref-lock from render_fresh_16x9.py. LEAN prompting
(memory byteplus-lean-prompting / REDO_NOTE): ONE subject ~25-40 words, no detail lists, no legible
text, no named buildings/languages, positive end-states only (no "NO x"), lean on the ref for the
face. Ref-lock: suffering Christ -> crux (bare-torso ref); risen Christ -> risen-face ref; everything
else -> NONE (face-bleed fix). Idempotent (skip existing). List-only until --render.

  ...python longform/02_Psalm_22_Song_From_The_Cross/render_new16_16x9.py            # list
  ...python longform/02_Psalm_22_Song_From_The_Cross/render_new16_16x9.py --render   # ~$0.80
"""
import argparse, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
rf_spec = importlib.util.spec_from_file_location("rf", HERE / "render_fresh_16x9.py")
rf = importlib.util.module_from_spec(rf_spec); rf_spec.loader.exec_module(rf)  # reuse call/CH/INK/REFMAP/OUT

CH, INK = rf.CH, rf.INK

# slug -> (LEAN prompt, ref)   ref: "crux" | "risen" | None
PROMPTS = {
 "david_hands_lyre": (f"{INK}: an aged shepherd-king's weathered hands cradling and plucking a wooden lyre by warm lamplight, close and intimate, the strings catching the light; Iron-Age Israelite; 1st-millennium-BC", None),
 "worm_lowest": (f"{INK}: the suffering Christ ({CH}) stripped to a plain loincloth, standing bowed and broken with head hung low and shoulders sunk, both arms hanging limp at his sides, utterly despised and alone in deep shadow; dark, 1st-century", "crux"),
 "mocker_faces_trio": (f"{INK}: three 1st-century men close in the foreground sneering with cruel contempt at someone below, lips curled back, teeth bared in derision, cold hostile narrowed eyes, a dark blurred hostile crowd behind; dusty earth tones; antiquity", None),
 "pierced_feet": (f"{INK}: a tight macro of two bare feet laid one flat over the other on dark rough wood, a single large iron nail driven straight down through the centre of both feet deep into the beam, dark blood welling around the iron; warm hard light; reverent, 1st-century", None),
 "lots_dice_closeup": (f"{INK}: a tight close-up of rough Roman soldiers' hands casting small knucklebone dice on a folded pale robe on the stony ground; dusty, warm light; 1st-century", None),
 "scholar_hand_on_text": (f"{INK}: a bearded scholar's weathered hand resting thoughtfully at the edge of a spread parchment by lamplight, the parchment surface only soft indistinct texture; antiquity, period robes", None),
 "two_scrolls_compared": (f"{INK}: two aged parchment scrolls unrolled side by side on a wooden table in warm lamplight, their surfaces soft indistinct texture, one older and darker than the other; antiquity", None),
 "cross_hill_pullback": (f"{INK}: a lone rough wooden cross on a rocky hill seen wide from far off under a vast brooding sky, small and stark against the land, one pale shaft of light; epic, 1st-century", None),
 "face_anguish_closeup": (f"{INK}: an extreme tight close-up of the crucified Christ's ({CH}) face lifted and crying out with his last strength, brow furrowed in anguish, eyes toward heaven, a hard shaft of light across the face; reverent, 1st-century", "crux"),
 "empty_tomb_open": (f"{INK}: inside a dark empty rock-hewn tomb chamber, a bare stone burial ledge with folded white linen grave-cloths resting on it, a soft shaft of pale dawn light falling across the empty ledge from the open entrance; still, hopeful, 1st-century", None),
 "risen_hands_raised": (f"{INK}: the risen Christ ({CH}) standing glorified in warm radiant light, both arms lifted and open in praise, a real bodily risen man, a closed healed nail-print flat in each open palm; triumphant, 1st-century", "risen"),
 "nations_streaming_wide": (f"{INK}: a vast epic wide of a great multitude of many peoples streaming across the land from far horizons toward warm light on a hill, countless tiny figures flowing home, dwarfing scale; awe", None),
 "kneeling_at_cross": (f"{INK}: a few small bowed figures kneeling low at the foot of a rough wooden cross on the hill in warm breaking light, quiet and humbled; grace, reverent, 1st-century", None),
 "hand_reaching_closeup": (f"{INK}: a close view of the risen Christ's ({CH}) open right hand reaching gently toward the viewer in warm golden light, a single small pale closed scar in the very centre of the open palm, his serene face behind; inviting; 1st-century", "risen"),
 "cry_face_tears": (f"{INK}: an extreme tight close-up of the suffering Christ's ({CH}) face streaked with a single tear, eyes lifted and mouth open in a raw cry, deep shadow around, a shaft of light on the face; reverent, 1st-century", "crux"),
}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--render", action="store_true"); ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    for slug, (prompt, refk) in PROMPTS.items():
        if only and slug not in only:
            continue
        ref = rf.REFMAP.get(refk)
        print(f"\n{slug:24} ref={refk or 'NONE':5}")
        if a.render:
            print(f"   -> {rf.call(prompt, rf.OUT / f'{slug}.png', ref)}", flush=True)
    if not a.render:
        print(f"\n[list only] {len(PROMPTS)} NEW 16:9 stills @ {rf.SIZE}. --render ~$0.80")


if __name__ == "__main__":
    main()
