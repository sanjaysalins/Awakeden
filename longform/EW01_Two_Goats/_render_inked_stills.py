"""Render the 25 retro-comic stills for the EW01 Two Goats rebuild.
Reads v1/visual_16x9_inked/scene_plan.json (ported by _build_inked_scene_plan.py,
style text updated 2026-07-24 for the Awakeden Comic DNA pilot), renders via
HFProvider at 16:9 forced to config.VISUAL_STYLE=retro (v2/AWAKEDEN_COMIC_DNA.md
§1 — Ben-Day dots / vintage 1960s comic recipe), same pattern as
longform/04_The_Bronze_Serpent/_render_inked_stills.py. Stems match the archived
oil shot names (NN_title_slug) so the shot list lines up with the legacy
production. Vision audit happens by eye afterward
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
config.VISUAL_STYLE = "retro"  # force the retro-comic DNA pilot recipe, not the graphic_novel default
from pipeline.visual_models import Scene
from pipeline import visual_render
from pipeline import cost

HERE = Path(__file__).resolve().parent
V1 = HERE / "v1"
PLAN_DIR = V1 / "visual_16x9_inked"   # scene_plan.json lives here (unchanged)
# 2026-07-24: retro-comic PNGs write to a NEW sibling folder, NOT visual_16x9_inked/ --
# that folder holds the approved, already-animated ink-migration stills at the SAME
# filenames (stem_for() is unchanged), which the idempotent skip-if-exists check would
# otherwise silently protect from a real run, and --force would destroy if ever used here.
OUT = V1 / "visual_16x9_retro"
OUT.mkdir(exist_ok=True)
SLUG = "EW01_Two_Goats"

plan = json.loads((PLAN_DIR / "scene_plan.json").read_text(encoding="utf-8"))
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

# Retro-DNA character ref registry (2026-07-23 punch-list — real wiring, not the ad-hoc smoke
# test). Per-scene style_base text in scene_plan.json is NOT read by the renderer (it's
# decorative — assemble_final_prompt always pulls style_base/style_tail from
# config.STYLE_REGISTRY[config.VISUAL_STYLE], set to "retro" above); the JSON text was synced
# 2026-07-24 for documentation accuracy only. See v2/AWAKEDEN_COMIC_DNA.md §9 for the pilot cost
# table before running this for real (~$29-34 full 25-scene run; test-gate 3-5 scenes first).
RETRO_DNA = HERE / "_retro_dna"
CHARACTER_REFS = {
    "aaron": RETRO_DNA / "aaron_retro_ref.png",
    "christ": V1 / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png",
}
CHARACTER_MODEL = "nano_banana_pro"  # user decision, 2026-07-23 — character-locked scenes only
PLATE_MODEL = config.still_model()   # neutral plates keep the style-registry default (seedream_v4_5)

# world.period_negatives in scene_plan.json ("no stone-temple or cathedral architecture -- it is
# a tent") is NOT read by this script (same dead-field problem style_base had) -- the 2026-07-24
# test-gate render proved it out: 2 of 4 test scenes drew Greco-Roman fluted columns around the
# Tabernacle despite no scene ever mentioning columns, a systemic style-level default the "vintage
# 1960s comic epic" framing pulls toward. Fixed here for scenes that actually SHOW the Tabernacle
# structure (keyword-scoped, not blanket -- most scenes are open wilderness/gate/crowd with no
# tent in frame at all, and forcing tent language onto those would be wrong). Purely positive
# phrasing -- never names "column"/"stone"/"masonry" even to forbid them
# (seedream-no-negative-channel: naming the concrete noun can draw it).
MOOD_BASE = "reverent, sacred, solemn"
MOOD_TENT = (", a portable tent of woven skins and linen curtain walls hung from bare undressed "
             "wooden tent-poles and ropes, humble and plain")
_TENT_KEYWORDS = ("tabernacle", "holy of holies", "mercy seat", "the veil", "curtained")


def mood_block_for(subject_block: str) -> str:
    return MOOD_BASE + (MOOD_TENT if any(k in subject_block.lower() for k in _TENT_KEYWORDS) else "")

prov = visual_render.HFProvider()
print(f"[provider] hf plates={PLATE_MODEL} / character={CHARACTER_MODEL} @ 16:9 (VISUAL_STYLE={config.VISUAL_STYLE})")

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
        subject_block=s["subject_block"], mood_block=mood_block_for(s["subject_block"]),
        jesus_variant=None,
    )
    scene_refs = [k for k in s.get("refs", []) if k in CHARACTER_REFS]
    ref_paths = [CHARACTER_REFS[k] for k in scene_refs if CHARACTER_REFS[k].exists()]
    prov._model = CHARACTER_MODEL if ref_paths else PLATE_MODEL
    try:
        print(f"[img ] {s['id']:02d} {s['title'][:44]} "
              f"({'+'.join(scene_refs) or 'plate'}, {prov._model}) ...", flush=True)
        t = time.time()
        png_bytes = prov.generate(scene, extra_ref_paths=ref_paths)
        png.write_bytes(png_bytes)
        print(f"       ok ({len(png_bytes):,} b, {time.time()-t:.0f}s) -> {png.name}")
        cost.record_hf(SLUG, "long", "stills", prov._model, note=f"#{s['id']:02d} {s['title'][:36]}")
        ok += 1
    except Exception as e:
        print(f"       FAIL: {e}")
        fail += 1

print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail} -> {OUT}")
