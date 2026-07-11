# -*- coding: utf-8 -*-
"""2026-07-11 user stills-review fixes: patch the flagged prompts in every carrying piece.json.
Fact-card basis per slug in comments. Shared plates get IDENTICAL prompts so run_piece's
reuse pre-flight pays once and copies to siblings."""
import json
from pathlib import Path

CL = Path(__file__).resolve().parent / "cluster_01_cross"

# John 19:23-24 — four soldiers, coat without seam woven from the top throughout.
# Fix: boxy one-piece ancient cut (was reading like a modern T-shirt).
ROBE = ("four Roman soldiers gathered around a wide boxy rectangular tunic of undyed cloth "
        "held spread between them, woven in one single piece from shoulder to hem, short "
        "sleeve folds of the same cloth, small plain lots on a flat stone, bright morning "
        "light, close, vertical, 1st-century Judea")

# Roman crosses were low — feet near the ground; crosses were flagged rendering giant.
# Keeps forsaken_cry world canon VERBATIM: "three crosses standing on the low rocky rise of Golgotha"
_GOLGOTHA_CORE = ("a wide view of three crosses standing on the low rocky rise of Golgotha "
                  "outside the walls of Jerusalem, each cross short and barely taller than a "
                  "man, the crucified men's feet hanging near the ground, the centre cross "
                  "bearing the crucified Christ, a crucified thief on each cross beside him, "
                  "small mourners standing close below, low flat-roofed stone houses beyond "
                  "the wall, ")
GOLGOTHA_MORNING = _GOLGOTHA_CORE + "clear morning light, wide, vertical, 1st-century Judea"
GOLGOTHA_DARK = (_GOLGOTHA_CORE + "the sky black at midday and the whole land lying dim in "
                 "deep shadow, wide, vertical, 1st-century Judea")

# John 19:30 — bowed his head; the body still hangs by the hands on the patibulum
# (was rendering with arms slack at his sides).
BOWED = ("the crucified Christ dead on the cross seen from the chest up, head bowed low, "
         "thorn crown over closed eyes, both arms stretched up and outward with hands fixed "
         "to the wooden crossbeam above, stillness on his face, deep darkness behind the "
         "cross, close, vertical, 1st-century Judea")

# John 19:34 — blood and water came out of HIS side (was: the wood itself bleeding).
BLOOD_SIDE = ("a tight close view of the spear wound in the side of the crucified Christ, a "
              "thin stream of dark blood and clear water running from the wound down his skin "
              "and falling to the stones below, dim darkened afternoon light, macro, vertical, "
              "1st-century Judea")
BLOOD_FOOT = ("the crucified Christ on a low wooden cross at Golgotha seen from below, dark "
              "drops of blood falling from his pierced hands and feet onto the pale stone "
              "beneath, a small dark pool gathering on the rock, heavy grey afternoon sky, "
              "low angle, vertical, 1st-century Judea")

# Zech 12:10 fulfilled John 19:37 — they LOOK ON HIM and mourn (was: invented dead-son bier).
MOURNERS = ("a huddle of Judean mourners in rough cloaks at the foot of the cross at "
            "Golgotha, men and women weeping as they gaze up toward the crucified Christ "
            "above them, dim darkened afternoon light, low angle, vertical, 1st-century Judea")

# Zech 11:12 — a real shekel is thumbnail-small (was dinner-plate sized).
COIN = ("a broad unrolled ancient scroll of faded illegible marks on a wooden table, one "
        "small silver shekel the size of a fingertip lying alone on the wide parchment, "
        "warm oil-lamp light, close, vertical, ancient Judea")

PATCH = {
    "crucifixion_foretold_ps2218": {"seamless_robe_lots": ROBE, "golgotha_hill_wide": GOLGOTHA_MORNING},
    "today_paradise_luke2343": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "watch_one_hour_matt2640": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "woman_behold_john1926": {"golgotha_hill_wide": GOLGOTHA_MORNING},
    "forsaken_cry_ps221": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "into_thy_hands_luke2346": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "it_is_finished_john1930": {"golgotha_hill_wide": GOLGOTHA_DARK, "bowed_head_finished": BOWED},
    "i_thirst_john1928": {"bowed_head_finished": BOWED},
    "pierced_zech1210": {"seamless_robe_lots": ROBE, "golgotha_hill_wide": GOLGOTHA_DARK,
                          "blood_water_wood": BLOOD_SIDE, "mourners_only_son": MOURNERS},
    "thirty_pieces_zech11": {"blood_water_wood": BLOOD_FOOT, "coin_on_scroll": COIN},
}

for piece, fixes in PATCH.items():
    pj_path = CL / piece / "piece.json"
    d = json.loads(pj_path.read_text(encoding="utf-8"))
    jobs = d["stills"]["jobs"]
    for slug, prompt in fixes.items():
        if slug not in jobs:
            jobs[slug] = {"prompt": prompt, "ref": None}
            print(f"[{piece}] {slug}: ADDED job (was legacy spec-era file)")
        else:
            jobs[slug]["prompt"] = prompt
            print(f"[{piece}] {slug}: patched")
    pj_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("done")
