#!/usr/bin/env python
"""Register It Is Finished (John 19:30) NEW assets: 10 stills + their Kling clips."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
import asset_index as ax

V = HERE / "visual"
COMMON = dict(aspect="9:16", style="graphic_novel_inked", cluster="cluster_01_cross",
              piece="it_is_finished_john1930", piece_title="It Is Finished (John 19:30)",
              verse="John 19:30 + Gen 2:1 + John 1:3 + John 17:4", source="byteplus seedream-4-5", created="2026-07-03")

STILLS = {
 "eden_garden_finished": ("pristine garden valley at golden dawn, creation complete", [], ["rivers", "flowering trees", "mountains"], "Eden", "neutral", "the heavens and the earth were finished (Gen 2:1)"),
 "seventh_day_light": ("golden evening calm over young hills and still water", [], ["golden light", "hills", "still water"], "young earth", "neutral", "God rested (Gen 2:2)"),
 "jesus_prays_night": ("Jesus kneeling in prayer among olive trees, face lifted to the moon", ["Christ"], ["olive trees", "moon", "flat rock"], "Gethsemane", "specific", "I have finished the work (John 17:4)"),
 "vinegar_sponge_reed": ("sponge on a reed lifted toward the crucified Christ, from below", ["Christ crucified"], ["sponge", "reed", "cross"], "Golgotha", "specific", "had received the vinegar (John 19:30)"),
 "bowed_head_finished": ("thorn-crowned Christ, head bowed in stillness, at peace", ["Christ crucified"], ["crown of thorns", "parting storm"], "Golgotha", "hero", "he bowed his head, and gave up the ghost (John 19:30)"),
 "tomb_stone_sealed": ("great round stone sealing the rock-cut tomb at dusk", [], ["round stone", "tomb", "dusk hillside"], "garden tomb", "neutral", "rested in the tomb through the sabbath"),
 "first_day_morning": ("dawn light bursting from the open garden tomb, stone rolled aside", [], ["open tomb", "rolled stone", "dawn gold"], "garden tomb", "hero", "on the first day, morning came (Luke 24:1)"),
 "hands_shaping_light": ("two strong hands cupping a sphere of golden light in starry darkness", [], ["hands", "light sphere", "stars"], "creation", "neutral", "All things were made by him (John 1:3)"),
 "carpenter_bench_rest": ("carpenter's bench with a finished stool, tools laid down at rest", [], ["workbench", "stool", "tools", "shavings"], "workshop", "neutral", "He does not leave work half done"),
 "man_lifting_face_dawn": ("a weathered man lifting his face into warm dawn light, at peace", ["us"], ["dawn light", "lifted face"], "dawn", "neutral", "He bowed his head so you could lift yours"),
}

for slug, (subject, chars, elems, setting, scope, doctrine) in STILLS.items():
    ax.register({**COMMON, "id": f"iif_{slug}", "type": "still", "media": "image",
                 "path": V / f"{slug}.png", "title": subject, "subject": subject,
                 "characters": chars, "elements": elems, "setting": setting,
                 "palette": "inked cel-flat, Eden gold to storm dark to dawn gold",
                 "mood": "two finished works, rest", "doctrine": doctrine,
                 "reuse_scope": scope, "tags": ["livingpage", "john1930", "creation"],
                 "used_in": ["it_is_finished_john1930 short"]})
n = 0
for slug, s in STILLS.items():
    clip = V / "clips" / f"{slug}.mp4"
    if not clip.exists():
        continue
    n += 1
    ax.register({**COMMON, "id": f"iif_{slug}_clip", "type": "clip", "media": "video",
                 "path": clip, "title": s[0] + " (Kling push-in)",
                 "subject": s[0], "characters": s[1], "elements": s[2], "setting": s[3],
                 "source": "HF kling3_0 pro 9:16, INK camera-only push-in",
                 "doctrine": s[5], "reuse_scope": s[4],
                 "tags": ["livingpage", "john1930", "kling"],
                 "used_in": ["it_is_finished_john1930 short"]})
print(f"registered {len(STILLS)} stills + {n} clips")
