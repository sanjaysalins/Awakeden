# -*- coding: utf-8 -*-
"""Re-roll round 2 (2026-07-11): tighten the 6 prompts that missed on eye-audit.
Misses: robe lost its lots; both golgothas grew church-crosses on rooftops + tall crosses +
clothed thieves; bowed-head grew shoulder artifacts + gripping fists; thirty blood grew floating
drops + leg smudges; coin swapped the clay lamp for a candle."""
import json
from pathlib import Path

CL = Path(__file__).resolve().parent / "cluster_01_cross"

ROBE = ("four Roman soldiers kneeling and standing around a wide boxy rectangular tunic of "
        "undyed cloth held spread between them, woven in one single piece from shoulder to "
        "hem, short sleeve folds of the same cloth, beside them a flat stone with small plain "
        "pebble lots scattered across it, bright morning light, close, vertical, 1st-century Judea")

_GOLGOTHA_CORE = ("a wide view of three crosses standing on the low rocky rise of Golgotha "
                  "outside the walls of Jerusalem, the crosses short rough wooden posts, the "
                  "crucified men bare in loincloths with their feet hanging just above the "
                  "bystanders' heads, the centre cross bearing the crucified Christ, a "
                  "crucified thief on each cross beside him, small mourners standing close "
                  "below, low stone houses with plain flat earthen roofs beyond the wall, ")
GOLGOTHA_MORNING = _GOLGOTHA_CORE + "clear morning light, wide, vertical, 1st-century Judea"
GOLGOTHA_DARK = (_GOLGOTHA_CORE + "the sky black at midday, the hill and city lying dim in "
                 "deep shadow, wide, vertical, 1st-century Judea")

BOWED = ("the crucified Christ dead on the cross seen from the chest up, head bowed low, "
         "thorn crown over closed eyes, both arms stretched up and outward along the wooden "
         "crossbeam, open hands lying flat against the wood, bare shoulders against deep "
         "darkness behind the cross, stillness on his face, close, vertical, 1st-century Judea")

BLOOD_FOOT = ("the crucified Christ on a low wooden cross at Golgotha seen from below, thin "
              "trickles of blood running from his pierced hands and feet down the wood, a "
              "small dark pool gathering on the pale stone at the foot of the cross, heavy "
              "grey afternoon sky, low angle, vertical, 1st-century Judea")

COIN = ("a broad unrolled ancient scroll of faint faded illegible marks on a wooden table, "
        "one small silver shekel the size of a fingertip lying alone on the wide parchment, "
        "a small clay oil lamp burning beside it, warm lamplight, close, vertical, ancient Judea")

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
    "thirty_pieces_zech11": {"blood_water_wood": BLOOD_FOOT, "coin_on_scroll": COIN},
}

for piece, fixes in PATCH.items():
    pj_path = CL / piece / "piece.json"
    d = json.loads(pj_path.read_text(encoding="utf-8"))
    for slug, prompt in fixes.items():
        d["stills"]["jobs"][slug]["prompt"] = prompt
        print(f"[{piece}] {slug}: patched v2")
    pj_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("done")
