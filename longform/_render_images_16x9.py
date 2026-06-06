"""Batch-render the 16:9 long-form Baroque stills from an episode's scene_plan.json (NBP).
EPISODE-GENERIC: pass an episode slug/dir as the first arg (bare = Isaiah, back-compat).
Idempotent: skips a scene whose PNG already exists. TEST-GATE: renders 1-2 test stills,
STOPS for full-res QC + --approved before the rest. Per-scene jesus_variant + image_library
`bank` metadata are read from the scene plan, not hardcoded. Reuses the NBP provider."""
import sys, time, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
from _episode import resolve, slugof  # noqa: E402
from _test_gate import apply_test_gate  # noqa: E402
sys.path.insert(0, str(ROOT / "image_library"))
from image_library import ImageLibrary, ImageEntry  # noqa: E402

ep = resolve(sys.argv)
ep.out.mkdir(exist_ok=True)

config.VISUAL_STYLE_BASE = ep.style_base or config.VISUAL_STYLE_BASE
config.VISUAL_STYLE_TAIL = ep.style_tail
visual_render.NBPProvider.ASPECT_RATIO = "16:9"

prov = visual_render.NBPProvider()
lib = ImageLibrary()
EP_SLUG = ep.slug

def bank(s, png):
    b = s.get("bank")
    if not b:
        return
    lib.import_file(png, slug=b["slug"], aspect="16:9", tags=b.get("tags", []),
                    subject=s["subject_block"], reuse_scope=b.get("scope", "specific"),
                    jesus_variant=s.get("jesus_variant"), style="baroque-oil",
                    source="nbp", source_episode=EP_SLUG, created="2026-06-06", used_in=[EP_SLUG])
    print(f"       banked -> image_library/{b['slug']} ({b.get('scope')})")

# reuse an approved test render as the first scene, if present
s1 = ep.png(ep.scenes[0])
if not s1.exists() and (ep.out / "test_s01.png").exists():
    s1.write_bytes((ep.out / "test_s01.png").read_bytes())
    print(f"[copy] test_s01.png -> {s1.name}")
if s1.exists() and ep.scenes[0].get("bank") and not lib.by_slug(ep.scenes[0]["bank"]["slug"]):
    bank(ep.scenes[0], s1)

# TEST GATE: opening scene + the first jesus/gospel-pivot scene (generic analog of Isaiah's [1,6]).
pivot = next((s["id"] for s in ep.scenes if s.get("jesus_variant")), None)
default_test = [ep.scenes[0]["id"]] + ([pivot] if pivot else [])
gate_ids, gate_stop, gate_banner = apply_test_gate(
    sys.argv, ep.out, stage="stills",
    all_ids=[s["id"] for s in ep.scenes],
    default_test=default_test or [ep.scenes[0]["id"]],
    qc_hint="Open each PNG full-size — never a contact sheet (that hid the anachronisms).",
)

ok = fail = skip = 0
for s in ep.scenes:
    if s["id"] not in gate_ids:
        continue
    png = ep.png(s)
    if png.exists():
        print(f"[skip] {png.name}"); skip += 1; continue
    scene = Scene(
        index=s["id"], slug=slugof(s["title"]), title=s["title"],
        scene_type="single", arc_position=s.get("mvt", ""), framing="cinematic wide",
        purpose=s["title"], rationale=s.get("mvt", ""),
        visible_elements=s["subject_block"][:200], emotional_tone=s.get("mvt", ""),
        subject_block=s["subject_block"], mood_block="reverent, sacred, solemn, Baroque",
        jesus_variant=s.get("jesus_variant"),
    )
    try:
        print(f"[img ] {s['id']:02d} {s['title'][:40]} "
              f"(jesus={s.get('jesus_variant') or '-'}) ...", flush=True)
        t = time.time()
        png.write_bytes(prov.generate(scene))
        print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s) -> {png.name}")
        bank(s, png)
        ok += 1
    except Exception as e:
        print(f"       FAIL: {e}"); fail += 1
print(f"\n[done] {ep.slug}: rendered {ok}, skipped {skip}, failed {fail}  -> {ep.out}")
if gate_stop:
    print(gate_banner); sys.exit(0)
