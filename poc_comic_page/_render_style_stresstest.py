"""Comic-style STRESS TEST: 5 styles (A Storybook, B Action Painterly, C Clean-Line
European, G Mainstream Ink, F Manga Ink) x 4 hard scenes (crucifixion, resurrection
tomb, Noah + rainbow, ark boarding). 20 stills, NBP nano_banana_pro ~$0.30 each,
$6.00 -- user-approved 2026-07-27.

Style blocks are TECHNIQUE-ONLY (no baked-in daylight/mood words) so they don't fight
a scene's own lighting -- mood/palette lives entirely in the scene block. The cross
scene wording is hardened vs the earlier round (positive-only "dried into dark matted
stains, fixed and still" instead of negating "not dripping").

Noah scenes reuse the existing ref_library canon (character/object anchors already
built for EW06_Noah) -- reuse-first, no new characters invented for this test.

  .venv\\Scripts\\python.exe poc_comic_page/_render_style_stresstest.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_StyleBakeoff"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_style_bakeoff" / "_stresstest"
OUT.mkdir(parents=True, exist_ok=True)
JESUS_REF = HERE / "rung2" / "_charsheet_jesus.png"
REFLIB = ROOT / "ref_library"
AR = "1:1"

HARD_CAP_USD = 6.50

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

# (style_key, style_block, closing_restate)
STYLES = [
    ("A_storybook",
     "Classic mid-century illustrated Bible storybook comic art: confident "
     "clean black ink outlines of even weight, flat color fills with simple "
     "two-tone shading, friendly naturalistic faces with clear readable "
     "expressions, minimal hatching, open uncluttered composition, smooth "
     "matte paper finish.",
     "Render in clean storybook comic-ink style throughout: even black "
     "outlines, flat two-tone color shading, clear readable faces."),

    ("B_action_painterly",
     "Modern dynamic painted comic-book art: energetic loose ink drawing "
     "over fully painted color, dramatic painted light and atmospheric "
     "depth, a sweeping cinematic camera angle, expressive lifelike faces, "
     "visible painterly brushwork in cloth and sky.",
     "Render in fully painted dynamic comic-book style throughout, rich "
     "cinematic light and brushwork."),

    ("C_clean_line",
     "European clean-line comic album art: uniform-weight crisp black "
     "outlines around every form, perfectly flat color fills with zero "
     "gradients and zero hatching, simplified accurately-proportioned "
     "figures against a precise detailed background, calm balanced "
     "composition, smooth flat matte finish.",
     "Render in uniform clean-line European album style throughout: flat "
     "color, zero hatching, zero gradients."),

    ("G_mainstream_ink",
     "Bold contemporary comic-book inking: confident tapering brush-and-pen "
     "lines, deep solid spot blacks, crisp feathered hatching at the edges "
     "of forms, dramatic low-angle composition with strong depth, lean "
     "everyday human figures with ordinary builds, expressive lifelike "
     "faces, glossy printed-comic finish.",
     "Render in bold mainstream comic-book inking throughout: deep spot "
     "blacks, tapering brush lines, ordinary human builds."),

    ("F_manga_ink",
     "Japanese manga ink comic art: confident varied-weight black ink "
     "linework, expressive finely drawn eyes full of feeling, screentone "
     "dot shading in the shadows and cloth folds, dynamic diagonal "
     "composition with strong perspective, fine hatching in hair and "
     "fabric, naturalistic adult proportions, dignified serious faces.",
     "Render in Japanese manga ink style throughout: screentone shading, "
     "expressive dignified eyes."),
]

CROSS_SCENE = (
    "SCENE: One wooden cross stands alone on the rocky crest of Golgotha -- "
    "a single upright, a single crossbeam. Jesus hangs on that one cross, "
    "the only figure in the frame, his arms stretched out along the "
    "crossbeam with his wrists near its ends. At each wrist and at his feet "
    "is a dark ragged pierced wound, the blood long since dried into dark "
    "matted stains, fixed and still upon his skin. He wears only a rough "
    "cloth loincloth; his body is gaunt, wasted and ordinary, an everyday "
    "unremarkable build, ribs shadowed, his head bowed beneath the crown of "
    "thorns, his face sorrowful and marred with suffering -- the same face "
    "as the reference image: long dark hair, short dark beard. The whole "
    "figure is visible from a quiet mid-distance below the cross. "
    "Supernatural darkness lies over the land -- the sun blotted out, "
    "daylight failed to a deep still dusk, the far hills and city wall sunk "
    "in shadow. Still, silent, reverent."
)

RESURRECTION_SCENE = (
    "SCENE: A quiet garden at first dawn light. A great round stone lies "
    "rolled away from the low doorway of a rock-hewn tomb. Jesus stands "
    "just outside the open tomb in the soft gold of early morning, alive "
    "and radiant with new life, wearing a simple pale robe, his face calm "
    "and full of quiet joy. His open hands rest at his sides, the wounds in "
    "them now healed and glorified. Folded linen grave-cloths rest just "
    "inside the dark tomb opening behind him. The garden is still and "
    "hushed, dew on the grass, the first light breaking over the hills. He "
    "matches the reference image: long dark hair, short dark beard."
)

NOAH_RAINBOW_SCENE = (
    "SCENE: Noah stands on wet gleaming ground before his colossal "
    "gopher-wood ark, its long low roof and single high doorway behind him. "
    "Rain has just ceased; the ground is soaked and shining. He looks up in "
    "wonder and gratitude, his face lifted toward a soft luminous rainbow "
    "arcing across a washed pale sky. He matches the reference image "
    "exactly: exceedingly aged, long flowing white beard and hair, deeply "
    "weathered sun-browned skin, a coarse undyed woven tunic and rough "
    "goat-hair mantle, work-hardened carpenter's hands."
)

ARK_BOARDING_SCENE = (
    "SCENE: Noah's household and pairs of living creatures process calmly "
    "up toward the single high doorway of the colossal gopher-wood ark, its "
    "long low pitched roof filling the scene. Noah's three grown sons and "
    "their wives and his own wife stand together near the great doorway, an "
    "orderly line of paired clean beasts and fowls filing past them into "
    "the dark opening above. The sky is heavy and overcast, threatening "
    "rain. The scene is reverent, orderly and calm. Noah's household "
    "matches the reference image: an ancient Near-Eastern family in coarse "
    "undyed and earth-toned woven robes and head-coverings, gathered close "
    "together."
)

# (scene_key, scene_text, refs)
SCENES = [
    ("cross", CROSS_SCENE, [JESUS_REF]),
    ("resurrection", RESURRECTION_SCENE, [JESUS_REF]),
    ("noah_rainbow", NOAH_RAINBOW_SCENE,
     [REFLIB / "characters" / "NOAH.png", REFLIB / "objects" / "NOAHS_ARK.png",
      REFLIB / "objects" / "RAINBOW.png"]),
    ("ark_boarding", ARK_BOARDING_SCENE,
     [REFLIB / "characters" / "NOAH.png", REFLIB / "characters" / "NOAHS_HOUSEHOLD.png",
      REFLIB / "objects" / "NOAHS_ARK.png", REFLIB / "objects" / "ANIMAL_PAIRS.png"]),
]


def _find_job(model, started_after_iso):
    try:
        r = subprocess.run([HF, "generate", "list", "--image", "--size", "10", "--json"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        import json
        jobs = json.loads(r.stdout or "[]")
    except Exception as e:
        print(f"   (job lookup failed: {e})")
        return None
    for j in jobs:
        if j.get("job_type") == model and j.get("created_at", "") >= started_after_iso:
            if j.get("status") == "completed" and j.get("result_url"):
                return j["result_url"]
    return None


def run(prompt, out, refs, ar):
    started = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", ar,
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls and re.search(r"time(d)?\s*out|timeout", blob, re.IGNORECASE):
        print("   --wait timed out; polling `hf generate list` ...")
        for _ in range(20):
            time.sleep(15)
            u = _find_job(MODEL, started)
            if u:
                urls = [u]
                print("   recovered job via `hf generate list`")
                break
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for _, _, refs in SCENES:
        for r in refs:
            assert r.exists(), f"missing ref: {r}"

    spent_usd = 0.0
    results = []
    for scene_key, scene_text, refs in SCENES:
        for style_key, style, closing in STYLES:
            name = f"{style_key}__{scene_key}"
            out = OUT / f"{name}.png"
            prompt = style + "\n\n" + scene_text + "\n\n" + closing + "\n\n" + CONSTRAINT
            print(f"[img ] {name} ...", flush=True)
            if spent_usd >= HARD_CAP_USD:
                print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
                results.append((name, "ESCALATED-cap", None))
                continue
            t = time.time()
            ok = run(prompt, out, refs, AR)
            if not ok:
                print("   retrying once ...")
                time.sleep(5)
                ok = run(prompt, out, refs, AR)
            if ok:
                try:
                    row = cost.record_hf(EPISODE, "short", "stills_stresstest", MODEL,
                                          note=f"[style-stresstest] {name}")
                    spent_usd += float(row.get("est_usd") or 0)
                except Exception as e:
                    print(f"   (ledger record skipped: {e})")
                print(f"   ok ({time.time()-t:.0f}s)  running spend ~${spent_usd:.2f}")
                results.append((name, "clean", out))
            else:
                print("   FAILED (twice)")
                results.append((name, "FAILED", None))
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent_usd:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status, out in results:
        print(f"  {name}: {status}" + (f" -> {out}" if out else ""))


if __name__ == "__main__":
    main()
