"""Test-gate render ROUND 2 (2026-07-24): re-render scenes 1/5/11 only, after
fixing the 2 real defects round 1 found by eye (see _TEST_GATE_REVIEW.html):
  - scenes 1+5 drew Greco-Roman fluted columns around the Tabernacle (no scene
    text ever mentioned columns -- a systemic style-level default) -> mood_block
    now carries a positive tent-architecture anchor on tabernacle/veil scenes.
  - scene 11 drew blood-red streaks on the altar steps (recurrence of a defect
    the ink migration had already fixed once) -> subject_block reworded again
    in scene_plan.json, dropping "red" near the altar/goat entirely.
Scene 17 (Christ at the veil) passed round 1 clean -- not re-spent here.

Writes _v2 files alongside round 1's so both are visible side by side.
Vision audit skipped (Anthropic API key dead, feedback-api-key-dead-use-inchat)
-- eye-check the PNGs directly after.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_test_gate.py
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
config.VISUAL_STYLE = "retro"
from pipeline.visual_models import Scene
from pipeline import visual_render
from pipeline import cost

HERE = Path(__file__).resolve().parent
V1 = HERE.parent / "v1"
PLAN = V1 / "visual_16x9_inked" / "scene_plan.json"
OUT = HERE / "_test_gate"
OUT.mkdir(exist_ok=True)
SLUG = "EW01_Two_Goats"
TEST_IDS = [5, 11]
VERSION_SUFFIX = "_v3"

MOOD_BASE = "reverent, sacred, solemn"
MOOD_TENT = (", a portable tent of woven skins and linen curtain walls hung from bare undressed "
             "wooden tent-poles and ropes, humble and plain")
_TENT_KEYWORDS = ("tabernacle", "holy of holies", "mercy seat", "the veil", "curtained")


def mood_block_for(subject_block: str) -> str:
    return MOOD_BASE + (MOOD_TENT if any(k in subject_block.lower() for k in _TENT_KEYWORDS) else "")

plan = json.loads(PLAN.read_text(encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

visual_render.HFProvider.ASPECT = "16:9"

CHARACTER_REFS = {
    "aaron": HERE / "aaron_retro_ref.png",
    "christ": V1 / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png",
}
CHARACTER_MODEL = "nano_banana_pro"
PLATE_MODEL = config.still_model()

prov = visual_render.HFProvider()
print(f"[provider] hf plates={PLATE_MODEL} / character={CHARACTER_MODEL} @ 16:9 (VISUAL_STYLE={config.VISUAL_STYLE})")

ok = fail = 0
for sid in TEST_IDS:
    s = scenes[sid]
    stem = f"{s['id']:02d}_test_" + "".join(
        c if (c.isalnum() or c == " ") else "" for c in s["title"].lower()
    ).replace(" ", "_")[:50] + VERSION_SUFFIX
    png = OUT / f"{stem}.png"
    if png.exists():
        print(f"[skip] {png.name}")
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
        cost.record_hf(SLUG, "long", "stills", prov._model, note=f"[retro-test-gate] #{s['id']:02d} {s['title'][:30]}")
        ok += 1
    except Exception as e:
        print(f"       FAIL: {e}")
        fail += 1

print(f"\n[done] rendered {ok}, failed {fail} -> {OUT}")
