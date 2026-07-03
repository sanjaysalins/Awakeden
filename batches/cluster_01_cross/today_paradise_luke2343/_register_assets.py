#!/usr/bin/env python
"""Register Today in Paradise (Luke 23:43) NEW assets: 9 stills + 6 Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="today_paradise_luke2343", piece_title="Today in Paradise (Luke 23:43)",
              verse="Luke 23:39-43", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "mocker_thief_face": ("the railing thief snarling from his cross", ["mocker thief"], ["ropes", "storm"], "Golgotha", "specific", "the mocker's taunt (Luke 23:39)"),
 "penitent_thief_face": ("the penitent thief bound and tearful, head turned", ["penitent thief"], ["ropes", "tears"], "Golgotha", "specific", "the confession (Luke 23:40-41)"),
 "thief_looks_to_jesus": ("over the thief's shoulder toward the crucified Christ", ["penitent thief", "Christ"], ["two crosses", "storm"], "Golgotha", "specific", "Lord, remember me (Luke 23:42)"),
 "jesus_turns_to_thief": ("thorn-crowned Christ turning his head in compassion", ["Christ"], ["crown of thorns", "cross"], "Golgotha", "hero", "To day shalt thou be with me (Luke 23:43)"),
 "two_thieves_wide": ("three crucified men on a stormy hilltop, middle cross taller", ["Christ", "two thieves"], ["three crosses", "storm"], "Golgotha wide", "neutral", "crucified with the malefactors (Luke 23:33)"),
 "confession_face_hands": ("the bound thief's face pressed by his roped fist, eyes shut", ["penitent thief"], ["rope", "beam"], "Golgotha close", "specific", "we indeed justly (Luke 23:41)"),
 "kingdom_light_clouds": ("a shaft of pale light opening in heavy storm clouds", [], ["light shaft", "storm clouds", "hills"], "sky", "neutral", "when thou comest into thy kingdom (Luke 23:42)"),
 "answer_light_profile": ("thorn-crowned profile calm against breaking light", ["Christ"], ["crown of thorns", "light break"], "Golgotha", "hero", "Verily I say unto thee (Luke 23:43)"),
 "paradise_dawn": ("dawn garden with a robed figure in the light on the hilltop", ["Christ figure"], ["olive trees", "cypress", "dawn light", "garden path"], "paradise garden", "neutral", "with me in paradise (Luke 23:43)"),
}
KLING = ["mocker_thief_face", "penitent_thief_face", "thief_looks_to_jesus",
         "jesus_turns_to_thief", "paradise_dawn", "two_thieves_wide"]

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"tpd_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, storm greys to paradise gold",
                 "mood": "two responses, mercy, paradise", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "luke2343", "thief"],
                 "used_in": ["today_paradise_luke2343 short"]})
for slug in KLING:
    s = STILLS[slug]
    ax.register({**COMMON, "id": f"tpd_{slug}_clip", "type": "clip", "media": "video",
                 "path": V / "clips" / f"{slug}.mp4", "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "luke2343", "kling"],
                 "used_in": ["today_paradise_luke2343 short"]})
print(f"registered {len(STILLS)} stills + {len(KLING)} clips")
