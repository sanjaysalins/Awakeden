# -*- coding: utf-8 -*-
"""Re-roll round 5 (2026-07-11): user fixed-stills gate feedback.
1. robe: read like a wide T-shirt, not the long chiton Jesus wore -> long
   ankle-length narrow tunic (John 19:23).
2. bowed head: user wants NAILS visible fixing the hands (dark iron nail head
   per palm; thin blood line). Eye-check for blob nails per crucifixion memory.
3. pierced blood: spearhead pointed OUT of the chest (read as exiting) + rocks
   on the loincloth -> spear thrust upward from below by a soldier, head sunk
   INTO his side; plain loincloth."""
import json
from pathlib import Path

CL = Path(__file__).resolve().parent / "cluster_01_cross"

ROBE = ("four Roman soldiers kneeling and standing around a long ankle-length tunic of "
        "undyed linen held up spread between them, the tunic narrow with a plain round neck "
        "opening, one smooth unbroken weave from the shoulders down to the hem, beside them "
        "a flat stone with small plain pebble lots scattered across it, bright morning "
        "light, close, vertical, 1st-century Judea")

BOWED = ("the crucified Christ dead on the cross seen from the chest up, head bowed low, "
         "thorn crown over closed eyes, both arms stretched up and outward along the wooden "
         "crossbeam, each open palm pressed flat against the beam's wood with a dark iron "
         "nail head set in the centre of the palm, a thin line of blood running from each "
         "pierced palm down the wood, bare shoulders against deep darkness behind the "
         "cross, stillness on his face, close, vertical, 1st-century Judea")

BLOOD_SIDE = ("the crucified Christ on the cross, a Roman soldier's long spear thrust "
              "upward from below, the iron spearhead sunk deep into the side of his chest, "
              "the wooden shaft slanting down toward the ground, a stream of dark blood and "
              "clear water running from the wound down his skin, a plain cloth loincloth at "
              "his waist, dim darkened afternoon light, close, vertical, 1st-century Judea")

PATCH = {
    "crucifixion_foretold_ps2218": {"seamless_robe_lots": ROBE},
    "pierced_zech1210": {"seamless_robe_lots": ROBE, "blood_water_wood": BLOOD_SIDE},
    "forsaken_cry_ps221": {"bowed_head_finished": BOWED},
    "into_thy_hands_luke2346": {"bowed_head_finished": BOWED},
    "it_is_finished_john1930": {"bowed_head_finished": BOWED},
    "i_thirst_john1928": {"bowed_head_finished": BOWED},
}

for piece, fixes in PATCH.items():
    pj_path = CL / piece / "piece.json"
    d = json.loads(pj_path.read_text(encoding="utf-8"))
    for slug, prompt in fixes.items():
        d["stills"]["jobs"][slug]["prompt"] = prompt
        print(f"[{piece}] {slug}: patched v5")
    pj_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("done")
