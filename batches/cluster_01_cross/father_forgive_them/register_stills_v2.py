#!/usr/bin/env python
"""Register the 13 final v2 stills into the global asset_index.json with rich reuse metadata."""
import importlib.util, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PLAN = HERE / "visual" / "scene_plan_v2.json"
BP = HERE / "visual" / "_byteplus"

s = importlib.util.spec_from_file_location("ax", ROOT / "asset_index.py")
ax = importlib.util.module_from_spec(s); s.loader.exec_module(ax)
gs = importlib.util.spec_from_file_location("g", HERE / "build_gallery_v2.py")
g = importlib.util.module_from_spec(gs); gs.loader.exec_module(g)   # reuse IMG map

SCOPE = {"christ_hero": "specific", "christ_detail": "specific", "christ_risen": "specific",
         "context_scene": "neutral", "ot_echo": "neutral", "human_us": "neutral", "symbolic": "neutral"}
CREATED = "2026-07-01"

def main():
    scenes = json.loads(PLAN.read_text(encoding="utf-8"))["final_plan"]["scenes"]
    n = 0
    for sc in scenes:
        slug = sc["slug"]
        img = g.IMG.get(slug)
        if not img:
            print("  ! no image for", slug); continue
        path = BP / img
        if slug == "risen_hero" or slug == "risen_mercy_hand_held_out":
            scope = "hero"
        else:
            scope = SCOPE.get(sc["subject_type"], "specific")
        ax.register({
            "id": f"fft_{slug}",
            "type": "still", "media": "image",
            "path": str(path), "aspect": "9:16", "style": "inked-graphic-novel",
            "cluster": "cluster_01_cross", "piece": "father_forgive_them",
            "piece_title": "Father, forgive them", "verse": "Luke 23:34",
            "beat": sc["beat"], "beat_role": sc["subject_type"],
            "title": sc["concept"], "subject": sc["concept"],
            "bible_ref": sc["bible_ref"], "macro_elements": sc.get("macro_elements", []),
            "mood": "reverent", "reuse_scope": scope,
            "tags": ["cross", "crucifixion", "luke23", sc["subject_type"], sc["beat"].lower()],
            "prompt": sc["prompt_seed"],
            "source": "byteplus_seedream_4_5_ref_locked", "created": CREATED,
            "used_in": ["father_forgive_them_short"],
        })
        n += 1
        print(f"  registered fft_{slug:26} [{scope}] -> {img}")
    print(f"\n{n} stills registered into asset_index.json")

if __name__ == "__main__":
    main()
