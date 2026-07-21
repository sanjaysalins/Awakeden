"""Render the 25 inked graphic-novel stills for the EW01 Two Goats rebuild.
Reads v1/visual_16x9_inked/scene_plan.json (ported by _build_inked_scene_plan.py),
renders via HFProvider at 16:9 (config.VISUAL_STYLE=graphic_novel -> seedream),
same pattern as longform/04_The_Bronze_Serpent/_render_inked_stills.py.
Stems match the archived oil shot names (NN_title_slug) so the shot list lines
up with the legacy production. Vision audit happens by eye afterward
(feedback-verify-by-looking-not-running; Anthropic key dead). Idempotent:
skips an id whose PNG already exists unless --force.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_render_inked_stills.py --only 1,8   # test pair
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_render_inked_stills.py             # the rest
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
from pipeline import cost

HERE = Path(__file__).resolve().parent
V1 = HERE / "v1"
OUT = V1 / "visual_16x9_inked"
SLUG = "EW01_Two_Goats"

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
scenes = plan["scenes"]

ap = argparse.ArgumentParser()
ap.add_argument("--only", default="", help="comma-separated scene ids")
ap.add_argument("--force", action="store_true")
a = ap.parse_args()
only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None


def stem_for(s: dict) -> str:
    t = s["title"].lower()
    t = "".join(c if (c.isalnum() or c == " ") else "" for c in t)
    return f"{s['id']:02d}_{'_'.join(t.split())[:46]}"


visual_render.HFProvider.ASPECT = "16:9"
prov = visual_render.HFProvider()
print(f"[provider] hf {config.still_model()} @ 16:9 (VISUAL_STYLE={config.VISUAL_STYLE})")

ok = fail = skip = 0
for s in scenes:
    if only is not None and s["id"] not in only:
        continue
    png = OUT / f"{stem_for(s)}.png"
    if png.exists() and not a.force:
        print(f"[skip] {png.name}")
        skip += 1
        continue
    scene = Scene(
        index=s["id"], slug=png.stem, title=s["title"],
        scene_type="single", arc_position=s.get("mvt", ""), framing=s.get("framing", "cinematic wide"),
        purpose=s["title"], rationale=s.get("mvt", ""),
        visible_elements=s["subject_block"][:200], emotional_tone=s.get("atmos", ""),
        subject_block=s["subject_block"], mood_block="reverent, sacred, solemn",
        jesus_variant=None,
    )
    try:
        print(f"[img ] {s['id']:02d} {s['title'][:44]} ...", flush=True)
        t = time.time()
        png_bytes = prov.generate(scene)
        png.write_bytes(png_bytes)
        print(f"       ok ({len(png_bytes):,} b, {time.time()-t:.0f}s) -> {png.name}")
        cost.record_hf(SLUG, "long", "stills", config.still_model(), note=f"#{s['id']:02d} {s['title'][:36]}")
        ok += 1
    except Exception as e:
        print(f"       FAIL: {e}")
        fail += 1

print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail} -> {OUT}")
