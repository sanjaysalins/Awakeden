#!/usr/bin/env python
"""Register Could Ye Not Watch One Hour (Matt 26:40) NEW assets: 10 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="watch_one_hour_matt2640", piece_title="Could Ye Not Watch One Hour (Matt 26:40)",
              verse="Matthew 26:36-46", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "gethsemane_olives_night": ("moonlit olive grove on the hillside above the city wall", [], ["olive trees", "moon", "city wall"], "Gethsemane", "neutral", "Gethsemane, the night before the cross"),
 "disciples_sleeping": ("three robed men slumped asleep against olive roots at night", ["Peter", "James", "John"], ["olive tree", "cloaks", "moonlight"], "Gethsemane", "specific", "findeth them asleep (Matt 26:40)"),
 "jesus_stands_over_sleepers": ("Jesus standing in sorrowful tenderness over three sleeping men", ["Christ", "disciples"], ["olive tree", "moonlight"], "Gethsemane", "specific", "could ye not watch with me one hour (Matt 26:40)"),
 "cup_moonlight": ("a plain stone cup on a flat rock in cold moonlight", [], ["stone cup", "flat rock", "olive shadows"], "Gethsemane", "hero", "let this cup pass from me (Matt 26:39)"),
 "jesus_praying_close": ("anguished praying face, eyes shut tight, clasped hands, moonlit", ["Christ"], ["clasped hands", "sweat", "moon rim light"], "Gethsemane", "hero", "nevertheless not as I will (Matt 26:39)"),
 "jesus_leads_three": ("a robed man leading three companions up a moonlit garden path, from behind", ["Christ", "disciples"], ["moonlit path", "olive trees"], "Gethsemane", "specific", "tarry ye here, and watch with me (Matt 26:38)"),
 "sleeping_peter_close": ("older bearded fisherman fast asleep against an olive trunk, mouth slack", ["Peter"], ["olive trunk", "cloak", "moonlight"], "Gethsemane", "specific", "saith unto Peter (Matt 26:40)"),
 "kneeling_lamp_prayer": ("robed figure kneeling in prayer beside a small clay lamp in a dark room", ["us"], ["clay oil lamp", "stone room", "night window"], "night interior", "neutral", "Watch and pray (Matt 26:41)"),
 "same_prayer_again": ("kneeling man bowed low to the ground in prayer among olives, side view", ["Christ"], ["olive trees", "moonlight", "bowed prayer"], "Gethsemane", "specific", "he returned to the same prayer (Matt 26:42)"),
 "weak_flesh_hands": ("rough weathered hands clasped tight and trembling against dark wool", ["us"], ["clasped hands", "dark cloak"], "night", "neutral", "the flesh is weak (Matt 26:41)"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"wo_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, deep blue night, moon silver, lamp warm",
                 "mood": "the lonely watch, weak flesh, mercy", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "matt2640", "gethsemane"],
                 "used_in": ["watch_one_hour_matt2640 short"]})
n = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n += 1
    ax.register({**COMMON, "id": f"wo_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "matt2640", "kling"],
                 "used_in": ["watch_one_hour_matt2640 short"]})
print(f"registered {len(STILLS)} stills + {n} clips")
