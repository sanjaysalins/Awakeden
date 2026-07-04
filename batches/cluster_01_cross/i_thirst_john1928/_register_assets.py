#!/usr/bin/env python
"""Register I Thirst (John 19:28) NEW assets: 3 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="i_thirst_john1928", piece_title="I Thirst (John 19:28 / Ps 22:15)",
              verse="John 19:28 + Psalm 22:15", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "ocean_creation_wide": ("vast curling ocean wave under golden dawn, spray in the light", [], ["great wave", "dawn sun", "spray"], "open sea", "neutral", "All things were made by him (John 1:3)"),
 "potsherd_dry_clay": ("broken dry clay shard on cracked parched earth", [], ["potsherd", "cracked earth"], "desert", "neutral", "my strength is dried up like a potsherd (Ps 22:15)"),
 "living_water_stream": ("clear spring pouring over mossy rocks, sunlight in the water", [], ["spring water", "mossy rocks", "sparkle"], "spring", "neutral", "living water (John 4:14 / 7:37)"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"it_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, dawn gold / parched tan / water blue",
                 "mood": "the Maker thirsting, living water offered", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "john1928", "thirst"],
                 "used_in": ["i_thirst_john1928 short"]})
n = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n += 1
    ax.register({**COMMON, "id": f"it_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "john1928", "kling"],
                 "used_in": ["i_thirst_john1928 short"]})
print(f"registered {len(STILLS)} stills + {n} clips")
