#!/usr/bin/env python
"""Register the Pierced (Zech 12:10) pilot's NEW assets in the global asset index.
7 BytePlus stills + 6 HF-Kling 9:16 clips. Banked fft assets are already indexed."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="pierced_zech1210", piece_title="Pierced (Zechariah 12:10)",
              verse="Zechariah 12:10", source="byteplus seedream-4-5", created="2026-07-02")

STILLS = {
 "spear_thrust_up": ("Roman soldier thrusts spear up at the crucified Christ", ["soldier", "Christ"],
                     ["spear", "cross", "storm sky"], "Golgotha, storm", "hero",
                     "the piercing of John 19:34/Zech 12:10"),
 "zechariah_night_scroll": ("prophet Zechariah under night stars with scroll", ["Zechariah"],
                     ["scroll", "stars", "rooftop", "city"], "Judean rooftop, night", "specific",
                     "the prophecy given ~500 BC"),
 "mourners_only_son": ("father and mother collapsed in grief beside a shrouded bier", ["father", "mother"],
                     ["bier", "shroud", "torches"], "stone courtyard, night", "neutral",
                     "mourning as for an only son (Zech 12:10)"),
 "john_watching": ("young disciple John flinching at the foot of the cross", ["John"],
                     ["cloak", "storm light"], "foot of the cross", "specific",
                     "the eyewitness of John 19:35-37"),
 "blood_water_wood": ("macro: water and blood run down the cross's wood grain", [],
                     ["blood", "water", "wood grain", "stone"], "base of the cross", "neutral",
                     "blood and water of John 19:34"),
 "grace_poured_sky": ("golden light pours like a waterfall through broken storm clouds onto a stone city", [],
                     ["light waterfall", "storm clouds", "city"], "sky over Jerusalem", "neutral",
                     "I will pour the spirit of grace (Zech 12:10a)"),
 "look_up_faces": ("three upturned tearful 1st-century faces catching warm light", ["onlookers"],
                     ["tears", "warm light"], "half-light", "neutral",
                     "they shall look upon me and mourn"),
}
KLING = ["spear_thrust_up", "zechariah_night_scroll", "mourners_only_son",
         "look_up_faces", "grace_poured_sky", "blood_water_wood"]

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"pz_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, storm greys to warm gold",
                 "mood": "prophetic, pierced, grace", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "pilot", "zech1210"],
                 "used_in": ["pierced_zech1210 short"]})
for slug in KLING:
    s = STILLS[slug]
    ax.register({**COMMON, "id": f"pz_{slug}_clip", "type": "clip", "media": "video",
                 "path": V / "clips" / f"{slug}.mp4", "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "pilot", "zech1210", "kling"],
                 "used_in": ["pierced_zech1210 short"]})
print(f"registered {len(STILLS)} stills + {len(KLING)} clips -> {ax.INDEX}")
