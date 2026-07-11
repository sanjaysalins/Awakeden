# -*- coding: utf-8 -*-
"""Re-roll round 3 (2026-07-11): last 4 misses from the round-2 eye-audit.
Misses: golgotha morning grew a HALO on Christ; golgotha dark grew a tiny skyline
cross + a comet streak + a thief in a dark shirt; bowed-head has one palm floating
off the beam; robe grew a stitched neck placket (a SEAM on the seamless robe) +
gold sleeve bands. All fixes positive-only wording (seedream draws forbidden nouns)."""
import json
from pathlib import Path

CL = Path(__file__).resolve().parent / "cluster_01_cross"

ROBE = ("four Roman soldiers kneeling and standing around a wide boxy rectangular tunic of "
        "undyed cloth held spread between them, the cloth one smooth unbroken weave from "
        "shoulder to hem with a plain round neck opening, short sleeve folds of the same "
        "plain cloth, beside them a flat stone with small plain pebble lots scattered across "
        "it, bright morning light, close, vertical, 1st-century Judea")

_GOLGOTHA_CORE = ("a wide view of three crosses standing on the low rocky rise of Golgotha "
                  "outside the walls of Jerusalem, the crosses short rough wooden posts, the "
                  "crucified men stripped to plain loincloths with their feet hanging just "
                  "above the bystanders' heads, the centre cross bearing the crucified "
                  "Christ, his bare dark hair against the open sky, a crucified thief "
                  "stripped to a loincloth on each cross beside him, small mourners standing "
                  "close below, low stone houses with plain flat earthen roofs beyond the "
                  "wall, ")
GOLGOTHA_MORNING = _GOLGOTHA_CORE + ("clear morning light under a plain pale sky, wide, "
                                     "vertical, 1st-century Judea")
GOLGOTHA_DARK = _GOLGOTHA_CORE + ("the sky a smooth deep black at midday, the hill and city "
                                  "lying dim in deep shadow, wide, vertical, 1st-century Judea")

BOWED = ("the crucified Christ dead on the cross seen from the chest up, head bowed low, "
         "thorn crown over closed eyes, both arms stretched up and outward along the wooden "
         "crossbeam, each open palm pressed flat against the beam's wood, bare shoulders "
         "against deep darkness behind the cross, stillness on his face, close, vertical, "
         "1st-century Judea")

PATCH = {
    "crucifixion_foretold_ps2218": {"seamless_robe_lots": ROBE, "golgotha_hill_wide": GOLGOTHA_MORNING},
    "today_paradise_luke2343": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "watch_one_hour_matt2640": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "woman_behold_john1926": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "forsaken_cry_ps221": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "into_thy_hands_luke2346": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "it_is_finished_john1930": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "i_thirst_john1928": {"bowed_head_finished": BOWED},
    "pierced_zech1210": {"seamless_robe_lots": ROBE, "golgotha_hill_wide": GOLGOTHA_DARK},
}

for piece, fixes in PATCH.items():
    pj_path = CL / piece / "piece.json"
    d = json.loads(pj_path.read_text(encoding="utf-8"))
    for slug, prompt in fixes.items():
        d["stills"]["jobs"][slug]["prompt"] = prompt
        print(f"[{piece}] {slug}: patched v3")
    pj_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("done")
