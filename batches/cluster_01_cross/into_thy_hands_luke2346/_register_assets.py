#!/usr/bin/env python
"""Register Into Thy Hands (Luke 23:46) NEW assets: 9 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="into_thy_hands_luke2346", piece_title="Father Into Thy Hands (Luke 23:46)",
              verse="Luke 23:46 + Psalm 31:5", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "child_sleeping_lamp": ("small child asleep under a wool blanket by a low clay lamp", ["child"], ["oil lamp", "woven mat", "mother silhouette"], "night interior", "neutral", "an evening prayer a child could learn"),
 "psalm_scroll_night": ("open scroll of faded script beside a burning clay oil lamp", [], ["scroll", "oil lamp", "night table"], "night interior", "neutral", "Into thine hand I commit my spirit (Ps 31:5)"),
 "father_holds_sleeping_child": ("bearded father cradling his sleeping child by lamplight", ["father", "child"], ["lamplight", "shoulder cradle"], "night interior", "neutral", "like a child falling asleep in his father's arms"),
 "hands_of_light_open": ("vast gentle hands of golden light opening through parted storm clouds", [], ["hands of light", "storm clouds", "rays"], "sky", "hero", "Father, into thy hands I commend my spirit (Luke 23:46)"),
 "child_waking_dawn": ("child stirring awake as dawn light pours through a small window", ["child"], ["dawn window", "waking eyes"], "morning interior", "neutral", "death loses its last word"),
 "father_hand_childs_hand": ("a child's hand resting inside a large weathered father's hand, lamp beside", ["father", "child"], ["hands", "clay oil lamp"], "night interior", "neutral", "He begins with Father"),
 "father_lamp_doorway": ("robed father holding a clay oil lamp in a stone doorway at night", ["father"], ["oil lamp", "doorway", "threshold light"], "stone house", "neutral", "Not judge. Not stranger. Father"),
 "child_eyes_closing": ("child's peaceful face eyes closed, a father's hand on the blanket, lamp low", ["father", "child"], ["blanket", "oil lamp", "resting hand"], "night interior", "neutral", "close your eyes in those same hands"),
 "cross_at_dawn": ("empty wooden cross on a rocky hilltop against a golden sunrise", [], ["empty cross", "sunrise", "hilltop"], "Golgotha at dawn", "hero", "He keeps the morning"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"ith_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, lamp warm to storm dark to dawn gold",
                 "mood": "bedtime prayer, trust, the strong hands", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "luke2346", "child"],
                 "used_in": ["into_thy_hands_luke2346 short"]})
n = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n += 1
    ax.register({**COMMON, "id": f"ith_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "luke2346", "kling"],
                 "used_in": ["into_thy_hands_luke2346 short"]})
print(f"registered {len(STILLS)} stills + {n} clips")
