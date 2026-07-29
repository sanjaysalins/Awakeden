"""Gold Seam DNA proof, round 2 (poc_comic_page/_ACTION_PAINTERLY_DNA.md "Round 2 -- The
Full House Grammar"): tests the Bowed Camera rule. 2 stills:
  1. cross_leveled -- passion-beat block (Sec 5e): level witness-height camera, faint seam,
     hardened gaunt body wording. Tests whether the camera fix pulls the ab-drift human.
  2. resurrection_heroshot -- house block (Sec 3): explicit low-angle hero shot, wide radiant
     seam. The glory-register contrast pair.
NBP nano_banana_pro, $0.30/still, $0.60 -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_gold_seam_camera_proof.py
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
AR = "1:1"

HARD_CAP_USD = 0.80

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

# --- passion-beat variant (Sec 5e) ---
PASSION_STYLE = (
    "Modern dynamic painted comic-book art: energetic loose black ink "
    "drawing over fully painted color; where the failing light touches a "
    "figure's edge the ink line gives way to a thin, faint seam of warm "
    "gold rim-light, the shadow side holding thick loose ink. A palette of "
    "deep storm blue-black shadow and earthy desert tans under a dimmed "
    "gold light, painted with atmospheric depth. One clear key light with "
    "a stated direction. Skies are deep, still, even fields of painted "
    "tone -- calm, windless, held -- their drama carried by light and "
    "color alone. The camera stands level at the eye height of a grieving "
    "witness on the ground, a quiet mid-distance away, the horizon level "
    "and calm in frame. A gaunt, wasted, everyday human body in the "
    "servant register, sorrowful and marred; expressive lifelike faces; "
    "visible painterly brushwork in cloth and ground."
)

CROSS_SCENE_LEVELED = (
    "SCENE: One wooden cross stands alone on the rocky crest of Golgotha -- "
    "a single upright, a single crossbeam. Jesus hangs on that one cross, "
    "the only figure in the frame, his arms stretched out along the "
    "crossbeam with his wrists near its ends. At each wrist and at his feet "
    "is a dark ragged pierced wound, the blood long since dried into dark "
    "matted stains, fixed and still upon his skin. He wears only a rough "
    "cloth loincloth; his body is gaunt, wasted and ordinary, an everyday "
    "unremarkable build, ribs shadowed, his head bowed beneath the crown of "
    "thorns, his face sorrowful and marred with suffering -- the same face "
    "as the reference image: long dark hair, short dark beard. Seen level "
    "from a quiet mid-distance, at the eye height of one standing on the "
    "ground nearby, the horizon level. Supernatural darkness lies over the "
    "land -- the sun blotted out, daylight failed to a deep still dusk, "
    "the far hills and city wall sunk in shadow. Still, silent, reverent. "
    "The gold seam on this figure is faint and close to the body -- glory "
    "hidden in suffering, never a halo, never triumphant."
)

CLOSING_PASSION = (
    "Render with the gold-seam rule throughout: the seam stays faint and "
    "close to the body, the camera level and human -- never a hero angle "
    "-- skies calm and still."
)

# --- glory/house variant (Sec 3) ---
GLORY_STYLE = (
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

RESURRECTION_HEROSHOT_SCENE = (
    "SCENE: A quiet garden at first dawn light. A great round stone lies "
    "rolled away from the low doorway of a rock-hewn tomb. Jesus stands "
    "just outside the open tomb in the soft gold of early morning, alive "
    "and radiant with new life, wearing a simple pale robe, his face calm "
    "and full of quiet joy. His open hands rest at his sides, the wounds in "
    "them now healed and glorified. Folded linen grave-cloths rest just "
    "inside the dark tomb opening behind him. Seen from a low angle looking "
    "up at him, triumphant, the bright morning sky opening wide behind him. "
    "The garden is still and hushed, dew on the grass, the first light "
    "breaking over the hills. He matches the reference image: long dark "
    "hair, short dark beard. The gold seam here is wide and radiant, fully "
    "earned."
)

CLOSING_GLORY = (
    "Render with the gold-seam rule throughout: the seam is wide and "
    "radiant, the camera a low earned hero angle looking up at him."
)

RENDERS = [
    ("cross_leveled", PASSION_STYLE, CROSS_SCENE_LEVELED, CLOSING_PASSION),
    ("resurrection_heroshot", GLORY_STYLE, RESURRECTION_HEROSHOT_SCENE, CLOSING_GLORY),
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
    for name, style, scene, closing in RENDERS:
        out = OUT / f"goldseam_{name}.png"
        prompt = style + "\n\n" + scene + "\n\n" + closing + "\n\n" + CONSTRAINT
        print(f"[img ] goldseam_{name} ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = run(prompt, out, [JESUS_REF], AR)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run(prompt, out, [JESUS_REF], AR)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills_goldseam_camera_proof", MODEL,
                                      note=f"[goldseam-camera-proof] {name}")
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
