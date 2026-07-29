"""Comic-style bake-off ROUND 2b (poc_comic_page/_STYLE_BAKEOFF_BRIEF.md "## Round 2b"):
the hard-scene test -- Jesus on the cross -- on 3 finalists: A (round-1 leader),
H (Webtoon Painterly), J (Dore Engraving). Jesus-ref ONLY (no Seeker in this scene).
Style-mood language adapted where a candidate's original palette assumed daylight
(A, H) so it doesn't fight the scene's supernatural darkness -- the TECHNIQUE under
test (ink/line/shading approach) is preserved, only the daylight-specific palette
wording is swapped for a dusk-compatible one. J needed no change (already monochrome
shadow-to-light). NBP nano_banana_pro, ~$0.30/still, $0.90 -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_style_bakeoff_cross.py
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
REFS = [HERE / "rung2" / "_charsheet_jesus.png"]  # Jesus only -- no Seeker in this scene
AR = "1:1"

HARD_CAP_USD = 1.20

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering. Pure artwork only."
)

PASSION_SCENE = (
    "SCENE: One wooden cross stands alone on the rocky crest of Golgotha -- a "
    "single upright, a single crossbeam. Jesus hangs on that one cross, the "
    "only figure in the frame, his arms stretched out along the crossbeam "
    "with his wrists near its ends. At each wrist and at his feet is a dark "
    "ragged pierced wound, the blood dried dark and matted. He wears only a "
    "rough cloth loincloth; his body is gaunt and wasted, ribs shadowed, his "
    "head bowed beneath the crown of thorns, his face sorrowful and marred "
    "with suffering -- the same face as the reference image: long dark hair, "
    "short dark beard. The whole figure is visible from a quiet mid-distance "
    "below the cross. Supernatural darkness lies over the land -- the sun "
    "blotted out, daylight failed to a deep still dusk, the far hills and "
    "city wall sunk in shadow. Still, silent, reverent."
)

# (name, style_block adapted for darkness, closing restate)
CANDIDATES = [
    ("A_storybook_CROSS",
     "Classic mid-century illustrated Bible storybook comic art: confident "
     "clean black ink outlines of even weight, flat color fills with simple "
     "two-tone shading, a somber dusk palette of slate blue, ash grey and "
     "one dim amber torchlight glow, dignified sorrowful faces with clear "
     "readable expression, minimal hatching, open uncluttered composition, "
     "smooth matte paper finish.",
     "Render in the same clean storybook comic-ink style throughout: even "
     "black outlines, flat color shading, clear readable faces."),

    ("H_webtoon_CROSS",
     "Korean webtoon digital painting: soft painterly rendering with "
     "delicate minimal linework, one point of luminous glowing light against "
     "deep gathering darkness, smooth gentle color gradients, a somber dusk "
     "palette, lifelike sorrowful faces with soft cinematic shading, "
     "atmospheric glow around the light source, clean polished finish.",
     "Render in soft Korean webtoon painterly style throughout, one luminous "
     "glow against deep darkness, polished finish."),

    ("J_dore_CROSS",
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
        prompt = style + "\n\n" + PASSION_SCENE + "\n\n" + closing + "\n\n" + CONSTRAINT
        print(f"[img ] {name} ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = run(prompt, out, REFS, AR)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills_bakeoff_cross", MODEL,
                                      note=f"[style-bakeoff-cross] {name}")
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
