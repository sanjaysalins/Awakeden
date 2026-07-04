#!/usr/bin/env python
"""Register The Forsaken Cry (Ps 22:1) NEW assets: 1 still + clip (david_writing_psalm is cf_*)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="forsaken_cry_ps221", piece_title="The Forsaken Cry (Ps 22:1 / Matt 27:46)",
              verse="Psalm 22:1 + Matthew 27:46", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "ninth_hour_darkness": ("three distant crosses under a sky gone black, dim swallowed sun", [], ["three crosses", "darkened sun", "black clouds"], "Golgotha", "neutral", "darkness over all the land, the ninth hour (Matt 27:45-46)"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"fc_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, near-black with pale sun",
                 "mood": "the dereliction, darkness at noon", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "ps221", "darkness"],
                 "used_in": ["forsaken_cry_ps221 short"]})
    clip = V / "clips" / f"{slug}.mp4"
    if clip.exists():
        ax.register({**COMMON, "id": f"fc_{slug}_clip", "type": "clip", "media": "video",
                     "path": clip, "title": subject + " (Kling push-in)",
                     "subject": subject, "characters": chars, "elements": elems, "setting": setting,
                     "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                     "doctrine": doctrine, "reuse_scope": scope,
                     "tags": ["livingpage", "ps221", "kling"],
                     "used_in": ["forsaken_cry_ps221 short"]})
fl = V / "clips" / "father_lamp_doorway.mp4"
if fl.exists():
    ax.register({**COMMON, "id": "fc_father_lamp_doorway_clip", "type": "clip", "media": "video",
                 "path": fl, "title": "father with lamp in doorway (Kling push-in)",
                 "subject": "robed father holding a clay oil lamp in a stone doorway at night",
                 "characters": ["father"], "elements": ["oil lamp", "doorway", "threshold light"],
                 "setting": "stone house", "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": "the way home is open", "reuse_scope": "neutral",
                 "tags": ["livingpage", "kling"], "used_in": ["forsaken_cry_ps221 short"]})
print("registered forsaken assets")
