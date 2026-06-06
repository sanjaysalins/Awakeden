"""Batch-render the 16:9 long-form Baroque stills from scene_plan.json (NBP).
Idempotent: skips a scene whose PNG already exists. Image gate happens AFTER this
(user reviews, rerolls), THEN animation. Reuses the NBP provider."""
import sys, time, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from pipeline.visual_models import Scene
from pipeline import visual_render
from _test_gate import apply_test_gate  # noqa: E402
sys.path.insert(0, str(ROOT / "image_library"))
from image_library import ImageLibrary, ImageEntry  # noqa: E402

EP = "01_Isaiah_53_Suffering_Servant"
# id -> (bank_slug, reuse_scope, [tags]) — topical-fit: neutral plates + gospel-Christ
# images are reusable anywhere; story-bound scenes are this-thread "specific".
BANK = {
    1:  ("wilderness_dusk_lone_figure", "neutral", ["wilderness","desert","dusk","lone-figure","landscape"]),
    2:  ("scroll_candlelight_hands", "neutral", ["scroll","parchment","candlelight","hands","study"]),
    3:  ("glory_exalted_light_figure", "neutral", ["glory","light","exalted","heaven","radiance"]),
    4:  ("isa53_marred_face", "specific", ["suffering","face","sorrow","passion"]),
    5:  ("isa53_despised_rejected", "specific", ["rejection","crowd","isolation","sorrow"]),
    6:  ("christ_crucified_robed_pierced", "neutral", ["crucifixion","cross","christ","passion"]),
    7:  ("isa53_servant_bearing_weight", "specific", ["substitution","burden","servant"]),
    8:  ("scattered_sheep_hillside_dusk", "neutral", ["sheep","flock","hillside","astray","shepherd"]),
    9:  ("lamb_led_to_slaughter", "neutral", ["lamb","sacrifice","altar","sheep"]),
    10: ("isa53_servant_silent_trial", "specific", ["trial","silence","accusers","servant"]),
    11: ("exiled_nation_column_grey", "neutral", ["exile","nation","israel","procession","journey"]),
    12: ("rich_mans_tomb_dusk", "neutral", ["tomb","grave","burial","stone","dusk"]),
    13: ("isa53_eunuch_chariot_gaza", "specific", ["chariot","eunuch","gaza-road","acts8","desert-road"]),
    14: ("isa53_philip_meets_chariot", "specific", ["philip","chariot","meeting","road","acts8"]),
    15: ("isa53_philip_preaches_jesus", "specific", ["philip","revelation","christ","acts8"]),
    16: ("christ_crucified_dark_sky_golgotha", "neutral", ["crucifixion","cross","christ","storm-sky","golgotha"]),
    17: ("dawn_over_tomb_stone", "neutral", ["dawn","tomb","morning","resurrection","stone"]),
    18: ("christ_risen_morning_light", "neutral", ["resurrection","christ","risen","glory","morning"]),
    19: ("christ_arm_of_the_lord_hand", "neutral", ["christ","hand","arm","light","risen"]),
    20: ("christ_reaching_hand_grace", "neutral", ["christ","grace","hand","invitation"]),
    21: ("christ_risen_glory_hero", "neutral", ["christ","risen","glory","hero","light"]),
}

V1 = ROOT / "longform" / "01_Isaiah_53_Suffering_Servant" / "v1"
OUT = V1 / "visual_16x9"
OUT.mkdir(exist_ok=True)

config.VISUAL_STYLE_BASE = ("Baroque oil painting, dramatic chiaroscuro, Caravaggio and "
    "Rembrandt lighting, deep shadow and warm golden light, reverent sacred art, muted "
    "earth tones, fine visible brushwork")
config.VISUAL_STYLE_TAIL = "no text, no modern elements, cinematic 16:9 widescreen composition"
visual_render.NBPProvider.ASPECT_RATIO = "16:9"

JESUS = {6: "passion", 15: "resurrection", 16: "passion", 18: "resurrection",
         19: "resurrection", 20: "resurrection", 21: "resurrection"}

def slug(t): return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:40]

plan = json.loads((OUT / "scene_plan.json").read_text(encoding="utf-8"))
prov = visual_render.NBPProvider()
lib = ImageLibrary()

def bank(scene_id, png):
    slug, scope, tags = BANK[scene_id]
    s = next(x for x in plan["scenes"] if x["id"] == scene_id)
    lib.import_file(png, slug=slug, aspect="16:9", tags=tags, subject=s["subject_block"],
                    reuse_scope=scope, jesus_variant=JESUS.get(scene_id), style="baroque-oil",
                    source="nbp", source_episode=EP, created="2026-06-04", used_in=[EP])
    print(f"       banked -> image_library/{slug} ({scope})")

# reuse the approved test render as scene 1
s1 = OUT / f"01_{slug(plan['scenes'][0]['title'])}.png"
if not s1.exists() and (OUT / "test_s01.png").exists():
    s1.write_bytes((OUT / "test_s01.png").read_bytes())
    print(f"[copy] test_s01.png -> {s1.name}")
if s1.exists() and not lib.by_slug(BANK[1][0]):
    bank(1, s1)

# TEST GATE: render 1-2 test stills, STOP for full-res QC + approval, THEN batch.
gate_ids, gate_stop, gate_banner = apply_test_gate(
    sys.argv, OUT, stage="stills",
    all_ids=[s["id"] for s in plan["scenes"]],
    default_test=[1, 6],  # opening (must grip) + the cross (hardest / anachronism-prone)
    qc_hint="Open each PNG full-size — never a contact sheet (that hid the anachronisms).",
)

ok = fail = skip = 0
for s in plan["scenes"]:
    if s["id"] not in gate_ids:
        continue
    png = OUT / f"{s['id']:02d}_{slug(s['title'])}.png"
    if png.exists():
        print(f"[skip] {png.name}"); skip += 1; continue
    scene = Scene(
        index=s["id"], slug=slug(s["title"]), title=s["title"],
        scene_type="single", arc_position=s["mvt"], framing="cinematic wide",
        purpose=s["title"], rationale=s["mvt"],
        visible_elements=s["subject_block"][:200], emotional_tone=s["mvt"],
        subject_block=s["subject_block"], mood_block="reverent, sacred, solemn, Baroque",
        jesus_variant=JESUS.get(s["id"]),
    )
    try:
        print(f"[img ] {s['id']:02d} {s['title'][:40]} "
              f"(jesus={JESUS.get(s['id']) or '-'}) ...", flush=True)
        t = time.time()
        png.write_bytes(prov.generate(scene))
        print(f"       ok ({png.stat().st_size:,} b, {time.time()-t:.0f}s) -> {png.name}")
        bank(s["id"], png)
        ok += 1
    except Exception as e:
        print(f"       FAIL: {e}"); fail += 1
print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail}  -> {OUT}")
if gate_stop:
    print(gate_banner); sys.exit(0)
