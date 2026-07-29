"""Action Painterly DNA proof test (poc_comic_page/_ACTION_PAINTERLY_DNA.md):
2 stills on the FIXED style block ("the Gold Seam" signature) -- the cross
(proves it survives restraint) and the doorway welcome (proves it sings).
NBP nano_banana_pro, $0.30/still, $0.60 -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_action_painterly_dna_proof.py
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
OUT = HERE / "_style_bakeoff" / "_goldseam_proof"
OUT.mkdir(parents=True, exist_ok=True)
JESUS_REF = HERE / "rung2" / "_charsheet_jesus.png"
SEEKER_REF = HERE / "rung2" / "_charsheet_seeker.png"
AR = "1:1"

HARD_CAP_USD = 0.80

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

STYLE = (
    "Modern dynamic painted comic-book art: energetic loose black ink drawing "
    "over fully painted color; where the key light strikes a figure's edge "
    "the ink line gives way to a thin seam of warm gold rim-light, the "
    "shadow side holding thick loose ink. A palette of warm gold light, deep "
    "storm blue-black shadow, and earthy desert tans, painted with "
    "atmospheric depth. One clear key light with a stated direction. Skies "
    "are deep, still, even fields of painted tone -- calm, windless, held -- "
    "their drama carried by light and color alone. A sweeping cinematic "
    "camera angle; lean everyday human figures in simple first-century "
    "dress; expressive lifelike faces; visible painterly brushwork in cloth "
    "and ground."
)

CLOSING = (
    "Render with the gold-seam rim-light rule throughout: light-side edges "
    "are thin warm gold seams, shadow-side ink stays thick and black, skies "
    "stay calm and still."
)

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
    "in shadow. Still, silent, reverent. The gold seam on this figure is "
    "faint and close to the body -- glory hidden in suffering, never a "
    "halo, never triumphant."
)

DOORWAY_SCENE = (
    "SCENE: A weary grey-haired traveler in a rough, ragged hooded cloak "
    "steps through a heavy arched wooden door, clutching a rolled parchment "
    "scroll. Jesus -- long dark hair, short dark beard, simple cream "
    "first-century robe with a cloth sash and sandals -- stands just "
    "inside, one hand resting on the traveler's shoulder, his face open and "
    "glad, welcoming him in. Ancient stone archway and flagstone floor, "
    "first-century Judea. Warm golden light fills the space beyond the "
    "door; the outer wall sits in cool evening shadow. Both faces clearly "
    "visible. The two men match the reference images exactly: same faces, "
    "same builds, same dress. The gold seam is wide and radiant here, at "
    "full warmth."
)

RENDERS = [
    ("cross", CROSS_SCENE, [JESUS_REF]),
    ("doorway", DOORWAY_SCENE, [JESUS_REF, SEEKER_REF]),
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
    spent_usd = 0.0
    results = []
    for name, scene, refs in RENDERS:
        out = OUT / f"goldseam_{name}.png"
        prompt = STYLE + "\n\n" + scene + "\n\n" + CLOSING + "\n\n" + CONSTRAINT
        print(f"[img ] goldseam_{name} ...", flush=True)
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
                row = cost.record_hf(EPISODE, "short", "stills_goldseam_proof", MODEL,
                                      note=f"[goldseam-proof] {name}")
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
