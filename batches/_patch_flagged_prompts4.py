# -*- coding: utf-8 -*-
"""Re-roll round 4 (2026-07-11): golgotha MORNING only. Round-3 misses: a tiny
church-style cross on a rooftop skyline (anachronism) + a stray cord dangling
from Christ's feet. Positive-only fixes: skyline is bare rooftops + open sky;
feet described resting together on the wood."""
import json
from pathlib import Path

CL = Path(__file__).resolve().parent / "cluster_01_cross"

_GOLGOTHA_CORE = ("a wide view of three crosses standing on the low rocky rise of Golgotha "
                  "outside the walls of Jerusalem, the crosses short rough wooden posts, the "
                  "crucified men stripped to plain loincloths with their feet hanging just "
                  "above the bystanders' heads, the centre cross bearing the crucified "
                  "Christ, his bare dark hair against the open sky and his bare feet resting "
                  "together against the wood, a crucified thief stripped to a loincloth on "
                  "each cross beside him, small mourners standing close below, low stone "
                  "houses with plain bare flat earthen roofs beyond the wall, the skyline "
                  "beyond only plain rooftops under open sky, ")
GOLGOTHA_MORNING = _GOLGOTHA_CORE + ("clear morning light under a plain pale sky, wide, "
                                     "vertical, 1st-century Judea")

for piece in ["crucifixion_foretold_ps2218", "today_paradise_luke2343",
              "watch_one_hour_matt2640", "woman_behold_john1926"]:
    pj_path = CL / piece / "piece.json"
    d = json.loads(pj_path.read_text(encoding="utf-8"))
    d["stills"]["jobs"]["golgotha_hill_wide"]["prompt"] = GOLGOTHA_MORNING
    pj_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[{piece}] golgotha_hill_wide: patched v4 (morning)")
print("done")
