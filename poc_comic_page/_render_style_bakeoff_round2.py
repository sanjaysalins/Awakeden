"""Comic-style bake-off ROUND 2 (poc_comic_page/_STYLE_BAKEOFF_BRIEF.md "## Round 2"):
5 more candidates (F-J) reaching into widely-loved comic genres not tried in round 1,
same doorway scene, same Jesus+Seeker char sheets. NBP nano_banana_pro, ~$0.30/still,
$1.50 total -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_style_bakeoff_round2.py
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
OUT = HERE / "_style_bakeoff"
OUT.mkdir(parents=True, exist_ok=True)
REFS = [HERE / "rung2" / "_charsheet_jesus.png", HERE / "rung2" / "_charsheet_seeker.png"]
AR = "1:1"

HARD_CAP_USD = 1.80

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

SCENE = (
    "SCENE: A weary grey-haired traveler in a rough, ragged hooded cloak steps "
    "through a heavy arched wooden door, clutching a rolled parchment scroll. "
    "Jesus -- long dark hair, short dark beard, simple cream first-century "
    "robe with a cloth sash and sandals -- stands just inside, one hand "
    "resting on the traveler's shoulder, his face open and glad, welcoming "
    "him in. Ancient stone archway and flagstone floor, first-century Judea. "
    "Warm light fills the space beyond the door; the outer wall sits in cool "
    "evening shadow. Both faces clearly visible. The two men match the "
    "reference images exactly: same faces, same builds, same dress."
)

CANDIDATES = [
    ("F_manga_ink",
     "Japanese manga ink comic art: confident varied-weight black ink "
     "linework, expressive finely drawn eyes full of feeling, screentone dot "
     "shading in the shadows and cloth folds, dynamic diagonal composition "
     "with strong perspective, fine hatching in hair and stone, a restrained "
     "warm wash of amber and slate color over the ink, naturalistic adult "
     "proportions, dignified serious faces, crisp bright paper.",
     "Render in Japanese manga ink style throughout, screentone shading, "
     "expressive dignified eyes."),

    ("G_mainstream_ink",
     "Bold contemporary comic-book inking: confident tapering brush-and-pen "
     "lines, deep solid spot blacks, crisp feathered hatching at the edges of "
     "forms, dramatic low-angle composition with strong depth, rich "
     "saturated color with warm rim light, lean everyday human figures in "
     "simple first-century robes, expressive lifelike faces, glossy "
     "printed-comic finish.",
     "Render in bold mainstream comic-book inking throughout, deep spot "
     "blacks, plain first-century dress, ordinary human build."),

    ("H_webtoon_painterly",
     "Korean webtoon digital painting: soft painterly rendering with "
     "delicate minimal linework, luminous glowing light and smooth gentle "
     "color gradients, a warm radiant palette, lifelike faces with soft "
     "cinematic shading, atmospheric glow around the light source, clean "
     "polished finish, composition built for a phone screen.",
     "Render in soft Korean webtoon painterly style throughout, luminous "
     "glow, phone-native polish."),

    ("I_noir_spotcolor",
     "Stark monochrome noir comic art: high-contrast black-and-white ink, "
     "great pools of solid black shadow, bold graphic silhouettes and "
     "hard-edged shapes of light, heavy dry-brush texture, lifelike serious "
     "faces, dramatic composition -- and one single spot color, the warm "
     "amber glow of the doorway light, the only color in the frame, "
     "monochrome everywhere else.",
     "Monochrome black-and-white throughout except the single warm amber "
     "spot color -- no other color anywhere."),

    ("J_dore_engraving",
     "Classical nineteenth-century engraved Bible illustration in the "
     "tradition of Gustave Dore: fine parallel engraving lines and dense "
     "cross-hatching, a full monochrome tonal range from deep velvet shadow "
     "to radiant white light, a great shaft of light breaking over the "
     "scene, epic monumental composition, reverent naturalistic figures with "
     "lifelike anatomy, the look of a steel engraving printed on cream "
     "paper, monochrome throughout.",
     "Render as a monochrome steel-engraved illustration throughout, "
     "cross-hatch line, no color anywhere."),
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
    for r in REFS:
        assert r.exists(), f"missing ref: {r}"
    spent_usd = 0.0
    results = []
    for name, style, closing in CANDIDATES:
        out = OUT / f"{name}.png"
        prompt = style + "\n\n" + CONSTRAINT + "\n\n" + SCENE + "\n\n" + closing
        print(f"[img ] {name} ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = run(prompt, out, REFS, AR)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills_bakeoff", MODEL,
                                      note=f"[style-bakeoff-r2] {name}")
                spent_usd += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)  running spend ~${spent_usd:.2f}")
            results.append((name, "clean", out))
        else:
            print("   FAILED")
            results.append((name, "FAILED", None))
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent_usd:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status, out in results:
        print(f"  {name}: {status}" + (f" -> {out}" if out else ""))


if __name__ == "__main__":
    main()
