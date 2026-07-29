"""Piece 1 production (v2/PRODUCTION_PLAN_400CR.md): NEW character sheets for Jesus +
the Seeker, rendered fresh IN the Action Painterly / Gold Seam style -- deliberately
NOT chained to the old inked charsheets (a bare reference-sheet prompt is thin enough
that the old ref's ink style would drag the whole sheet backward; a full scene prompt
has enough new style content to resist that, which is why the proof renders could
safely chain the old ref but a fresh charsheet cannot). These become the identity refs
for every Piece 1 panel. NBP nano_banana_pro, 2cr each, 4cr total.

  .venv\\Scripts\\python.exe poc_comic_page/_render_piece1_charsheets.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_InNoWise_GoldSeam"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_piece1" / "charsheets_v2"
OUT.mkdir(parents=True, exist_ok=True)
AR = "3:4"

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

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

CLOSING = (
    "Render with the gold-seam rule throughout: light-side edges are thin "
    "warm gold seams, shadow-side ink stays thick and black."
)

JESUS_SCENE = (
    "SCENE: A simple three-quarter reference portrait of Jesus, standing "
    "against a plain neutral studio backdrop, arms relaxed at his sides, "
    "calm and dignified expression. Long dark wavy hair to the shoulders, "
    "short dark beard, deep-set compassionate eyes. A simple undyed "
    "homespun wool tunic in the first-century Judean style, ankle-length, "
    "with a plain woven cord sash at the waist. Bare feet in simple leather "
    "thong sandals -- no boots, no shoes. Even, clear studio lighting "
    "showing the whole figure plainly, no dramatic shadow -- a clean "
    "character reference study, full figure head to feet visible, feet and "
    "sandals clearly shown."
)

SEEKER_SCENE = (
    "SCENE: A simple three-quarter reference portrait of a weary traveler, "
    "standing against a plain neutral studio backdrop, arms relaxed at his "
    "sides. A lined, careworn face, short greying hair. He wears a plain "
    "undyed earth-tone wool tunic and a separate rectangular woolen mantle "
    "draped loosely over both shoulders and pulled up over his head as a "
    "simple first-century head-covering -- loose draped cloth, not a "
    "tailored or pointed hood. A plain woven cord or braided leather belt "
    "at the waist. His hands and forearms are bare and unwrapped. Bare feet "
    "in simple leather thong sandals -- no boots, no shoes, no laced "
    "footwear of any kind. Even, clear studio lighting showing the whole "
    "figure plainly, no dramatic shadow -- a clean character reference "
    "study, full figure head to feet visible, feet and sandals clearly "
    "shown."
)

SHEETS = [
    ("jesus", JESUS_SCENE),
    ("seeker", SEEKER_SCENE),
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
    spent = 0.0
    for name, scene in SHEETS:
        out = OUT / f"{name}.png"
        prompt = GLORY_STYLE + "\n\n" + scene + "\n\n" + CLOSING + "\n\n" + CONSTRAINT
        print(f"[img] charsheet_{name} ...", flush=True)
        ok = run(prompt, out, [], AR)
        if not ok:
            print("   retrying once ...")
            time.sleep(5)
            ok = run(prompt, out, [], AR)
        if ok:
            row = cost.record_hf(EPISODE, "short", "charsheets", MODEL, note=f"[piece1] charsheet_{name}")
            spent += float(row.get("est_usd") or 0)
            print(f"   ok -> {out}  spend ~${spent:.2f}")
        else:
            print("   FAILED (twice)")
    print(f"\n[out] {OUT}  total ~${spent:.2f}")


if __name__ == "__main__":
    main()
