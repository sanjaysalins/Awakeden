#!/usr/bin/env python
"""Register Crucifixion Foretold (Ps 22:18) NEW assets: 2 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="crucifixion_foretold_ps2218", piece_title="The Crucifixion Foretold (Ps 22:18)",
              verse="Psalm 22:18 + John 19:24", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "david_writing_psalm": ("aged King David writing the psalm by lamplight, harp beside", ["David"], ["scroll", "oil lamp", "harp", "crown"], "night chamber", "neutral", "David wrote it in the first person (Ps 22:1)"),
 "lots_cup_close": ("leather cup with two knucklebone lots spilled on stone, garment beside", [], ["knucklebone lots", "leather cup", "woven garment"], "Golgotha", "specific", "cast lots upon my vesture (Ps 22:18)"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"cf_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, lamplight gold to storm grey",
                 "mood": "prophecy written, prophecy fulfilled", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "ps2218", "prophecy"],
                 "used_in": ["crucifixion_foretold_ps2218 short"]})
n = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n += 1
    ax.register({**COMMON, "id": f"cf_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "ps2218", "kling"],
                 "used_in": ["crucifixion_foretold_ps2218 short"]})
print(f"registered {len(STILLS)} stills + {n} clips")
