"""World-aware 16:9 stills renderer (EPISODE-GENERIC).

Reads the top-level `world` block in scene_plan.json so an episode renders as ONE
coherent world instead of 25 isolated prompts: locked era / place / light / palette +
a CAST of reference portraits attached to the relevant scenes via NBP `extra_ref_paths`.
This kills the scene-to-scene drift (Aaron's face changing, sets/lighting wandering)
and the NBP generic-old-bearded-man bleed. Standing rule: feedback-episode-world-consistency.

  python _render_world.py EW01_Two_Goats --anchors        # render the cast anchor portraits only
  python _render_world.py EW01_Two_Goats --scenes 14,24   # render specific scene ids (refs attached)
  python _render_world.py EW01_Two_Goats                   # render all MISSING scenes
  python _render_world.py EW01_Two_Goats --force           # re-render even if the PNG exists

Idempotent (skips an existing PNG unless --force). Per-PNG period/reverence audit
(fail-closed, writes <stem>.audit.json). NBP only — the cast refs need it.

scene_plan.json additions consumed here:
  top-level "world": {era, place, light, palette, style, period_negatives:[...],
                      cast: { <name>: {portrait:"<anchor subject_block>"}        # rendered -> _anchors/<name>.png
                                     | {ref:"<path rel to repo root or absolute>"} } }  # external, used as-is
  per-scene   "refs": ["aaron", ...]   # which locked cast faces attach to this scene
"""
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

ep = resolve(sys.argv)
ep.out.mkdir(exist_ok=True)
ANCH = ep.out / "_anchors"
ANCH.mkdir(exist_ok=True)

world = ep.plan.get("world")
if not world:
    raise SystemExit(f"no `world` block in {ep.scene_plan_path}. Author the World Bible first.")

# --- world constants -> the fixed style base/tail (same for every scene) ----------
NEG = "; ".join(world.get("period_negatives", []))
STYLE = world.get("style", "Baroque oil painting, dramatic chiaroscuro, reverent sacred art")
WORLD_LINE = " ".join(p for p in (world.get("era"), world.get("place"),
                                  world.get("light"), world.get("palette")) if p)
config.VISUAL_STYLE_BASE = f"{STYLE}. {WORLD_LINE}"
config.VISUAL_STYLE_TAIL = ("no text, strictly period-authentic ancient Near-Eastern setting, "
                            "cinematic 16:9 widescreen composition" + (f". Avoid: {NEG}" if NEG else ""))

# Provider: HF nano_banana_2 by default (NBP/Gemini is monthly-spend-capped); both attach
# the cast refs (NBP via fileData, HF via --image). --provider nbp forces Gemini.
USE_NBP = "--provider" in sys.argv and sys.argv[sys.argv.index("--provider") + 1] == "nbp"
if USE_NBP:
    visual_render.NBPProvider.ASPECT_RATIO = "16:9"
    prov = visual_render.NBPProvider(); PROV = "nbp"
    print("[provider] NBP (Gemini), 16:9 — refs via fileData")
else:
    visual_render.HFProvider.ASPECT = "16:9"
    prov = visual_render.HFProvider(); PROV = "hf"
    print("[provider] HF nano_banana_2, 16:9 — refs via --image")

def record(note):
    if PROV == "hf":
        cost.record_hf(ep.slug, "long", "stills", config.HF_MODEL_ID, note=note)
    else:
        cost.record_nbp(ep.slug, "long", "stills", note=note)

# --- flags -----------------------------------------------------------------------
ANCHORS_ONLY = "--anchors" in sys.argv
FORCE = "--force" in sys.argv                       # re-render SCENES even if the PNG exists
FORCE_ANCHORS = "--force-anchors" in sys.argv       # re-roll a locked anchor (kept stable otherwise)
DO_AUDIT = "--no-audit" not in sys.argv
PICK = None
if "--scenes" in sys.argv:
    PICK = {int(x) for x in sys.argv[sys.argv.index("--scenes") + 1].split(",")}

def ref_path(name):
    """Resolve a cast member's locked reference PNG (external `ref` or rendered _anchors/<name>.png)."""
    spec = world.get("cast", {}).get(name, {})
    if spec.get("ref"):
        p = Path(spec["ref"])
        return p if p.is_absolute() else (ROOT / spec["ref"])
    return ANCH / f"{name}.png"

def period_audit(scene, png):
    try:
        audit = visual_render.verify_image(scene, png.read_bytes())
        png.with_suffix(".audit.json").write_text(
            json.dumps({"passed": audit.passed, "issues": audit.issues,
                        "banned_token_hits": audit.banned_token_hits}, indent=1), encoding="utf-8")
        print("       [audit] " + ("PASS — period/reverent OK" if audit.passed
              else "*** FAIL — period/anachronism/tone ***"))
        for i in (audit.issues[:4] if not audit.passed else []):
            print(f"         - {i.get('claim','')}: {i.get('actual','')}")
        return audit
    except Exception as e:
        print(f"       [audit] SKIPPED ({str(e)[:70]})"); return None

# --- 1) cast anchor portraits ----------------------------------------------------
print(f"[world] {ep.slug} — {WORLD_LINE[:70]}...")
for name, spec in world.get("cast", {}).items():
    if spec.get("ref"):
        p = ref_path(name)
        print(f"[anchor] {name}: EXTERNAL ref {'OK' if p.exists() else 'MISSING'} -> {p}")
        continue
    dst = ANCH / f"{name}.png"
    if dst.exists() and not FORCE_ANCHORS:
        print(f"[anchor] {name}: LOCKED (exists) — --force-anchors to re-roll"); continue
    sc = Scene(index=0, slug=name, title=f"{name} anchor portrait",
               scene_type="single", arc_position="anchor", framing="portrait",
               purpose="locked character reference", rationale="world cast lock",
               visible_elements=spec["portrait"][:200], emotional_tone="reverent",
               subject_block=spec["portrait"],
               mood_block="reverent, solemn, Baroque, clean character study",
               jesus_variant=None)
    print(f"[anchor] {name}: rendering ...", flush=True)
    t = time.time()
    dst.write_bytes(prov.generate(sc))
    record(f"anchor {name}")
    print(f"       ok ({dst.stat().st_size:,} b, {time.time()-t:.0f}s) -> {dst}")
    if DO_AUDIT:
        period_audit(sc, dst)

if ANCHORS_ONLY:
    print("\n[anchors-only] done — review _anchors/ before the full render."); sys.exit(0)

# --- 2) scenes with their locked refs attached -----------------------------------
ok = fail = skip = afail = 0
for s in ep.scenes:
    if PICK and s["id"] not in PICK:
        continue
    png = ep.png(s)
    refs = [ref_path(r) for r in s.get("refs", [])]
    missing = [str(p) for p in refs if not p.exists()]
    if missing:
        print(f"[warn] scene {s['id']:02d} refs MISSING: {missing} — render anchors first"); fail += 1; continue
    scene = Scene(index=s["id"], slug=slugof(s["title"]), title=s["title"],
                  scene_type="single", arc_position=s.get("mvt", ""), framing=s.get("framing", "cinematic wide"),
                  purpose=s["title"], rationale=s.get("mvt", ""),
                  visible_elements=s["subject_block"][:200], emotional_tone=s.get("mvt", ""),
                  subject_block=s["subject_block"], mood_block="reverent, sacred, solemn, Baroque",
                  jesus_variant=s.get("jesus_variant"))
    if png.exists() and not FORCE:
        print(f"[skip] {png.name}"); skip += 1; continue
    try:
        rnote = ("+refs:" + ",".join(s.get("refs", []))) if refs else "no-ref"
        print(f"[img ] {s['id']:02d} {s['title'][:38]} ({rnote}) ...", flush=True)
        t = time.time()
        data = None
        for attempt in range(3):                      # HF returns transient empty responses; retry
            try:
                data = prov.generate(scene, extra_ref_paths=refs)
                break
            except Exception as ge:
                if attempt == 2:
                    raise
                print(f"       retry {attempt+1}/2 ({str(ge)[:60]})", flush=True)
        png.write_bytes(data)
        record(f"#{s['id']:02d} {s['title'][:30]}")
        print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s)")
        ok += 1
        if DO_AUDIT:
            a = period_audit(scene, png)
            if a and not a.passed:
                afail += 1
    except Exception as e:
        print(f"       FAIL: {e}"); fail += 1
print(f"\n[done] {ep.slug}: rendered {ok}, skipped {skip}, failed {fail}")
if afail:
    print(f"[audit] *** {afail} still(s) FAILED the period gate — reroll before animating ***")
