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
from pipeline import cost  # noqa: E402
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

DO_AUDIT = "--no-audit" not in sys.argv  # period/reverent Claude-Vision gate (default ON)

def period_audit(scene, png):
    """Fail-closed period/anachronism + reverence audit (verify_image check #6).
    Writes a <stem>.audit.json sidecar; returns the ImageAudit. Never crashes the
    render — on an audit error it flags needs-review rather than passing silently."""
    try:
        audit = visual_render.verify_image(scene, png.read_bytes())
        (png.with_suffix(".audit.json")).write_text(
            json.dumps({"passed": audit.passed, "issues": audit.issues,
                        "banned_token_hits": audit.banned_token_hits}, indent=1),
            encoding="utf-8")
        if audit.passed:
            print("       [audit] PASS — period/reverent OK")
        else:
            print("       [audit] *** FAIL — period/anachronism/tone issue ***")
            for i in audit.issues[:4]:
                print(f"         - {i.get('claim','')}: {i.get('actual','')}")
        return audit
    except Exception as e:
        print(f"       [audit] SKIPPED (error: {str(e)[:80]}) — review by eye")
        return None

ok = fail = skip = audited_fail = 0
for s in ep.scenes:
    if s["id"] not in gate_ids:
        continue
    png = ep.png(s)
    scene = Scene(
        index=s["id"], slug=slugof(s["title"]), title=s["title"],
        scene_type="single", arc_position=s.get("mvt", ""), framing="cinematic wide",
        purpose=s["title"], rationale=s.get("mvt", ""),
        visible_elements=s["subject_block"][:200], emotional_tone=s.get("mvt", ""),
        subject_block=s["subject_block"], mood_block="reverent, sacred, solemn, Baroque",
        jesus_variant=s.get("jesus_variant"),
    )
    if png.exists():
        print(f"[skip] {png.name}"); skip += 1
        if DO_AUDIT and not png.with_suffix(".audit.json").exists():
            a = period_audit(scene, png)
            if a and not a.passed:
                audited_fail += 1
        continue
    try:
        print(f"[img ] {s['id']:02d} {s['title'][:40]} "
              f"(jesus={s.get('jesus_variant') or '-'}) ...", flush=True)
        t = time.time()
        png.write_bytes(prov.generate(scene))
        print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s) -> {png.name}")
        cost.record_nbp(ep.slug, "long", "stills", note=f"#{s['id']:02d} {s['title'][:36]}")
        bank(s, png)
        ok += 1
        if DO_AUDIT:
            a = period_audit(scene, png)
            if a and not a.passed:
                audited_fail += 1
    except Exception as e:
        print(f"       FAIL: {e}"); fail += 1
print(f"\n[done] {ep.slug}: rendered {ok}, skipped {skip}, failed {fail}  -> {ep.out}")
if DO_AUDIT and audited_fail:
    print(f"[audit] *** {audited_fail} still(s) FAILED the period/reverent gate — "
          f"reroll them (delete the PNG + re-run) before animating. ***")
if gate_stop:
    print(gate_banner); sys.exit(0)
