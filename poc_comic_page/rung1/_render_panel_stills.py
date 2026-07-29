"""Comic Page Pipeline POC -- Rung 1, PHASE 1 (panel stills ONLY, no animation).

Renders the 4 separate-panel stills for page 3 of "In No Wise Cast Out"
(narration span 21.04-33.14s, layout 2x2). Follows the validated separate-
panel architecture from poc_thief_e2e/_test_separate_panel_stills.py (chained
panel-to-panel via --image) and the ledger try/except pattern from
poc_thief_e2e/_test_captionless_bakeoff.py. Prompt section order per
.claude/skills/comic-strip-native/COMIC_STRIP_NATIVE_SPEC.md sec1.2: aesthetic
-> global textual constraint -> character anchors -> panel spec -> style tail.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_render_panel_stills.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_Rung1_InNoWise"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)

HARD_CAP_USD = 3.00

# ---- Master Comic Blueprint sections (verbatim, per the brief) ------------
AESTHETIC = (
    "A 9:16 vertical single comic-book panel illustration. Rendered in a "
    "vintage graphic novel illustration style characterized by heavy black "
    "ink linework, high-contrast chiaroscuro shadows, cross-hatching, and a "
    "desaturated, muted earth-tone color palette (dominant slate grays, deep "
    "ochre, raw umber, muted blues). Subtle aged, textured vintage comic "
    "print finish."
)

CONSTRAINT = (
    "GLOBAL TEXTUAL CONSTRAINT: NO text of any kind anywhere -- no speech "
    "bubbles, no caption boxes, no lettering, no words. Pure artwork only."
)

ANCHORS = (
    "CORE CHARACTER DESIGN ANCHORS:\n"
    "Jesus Christ: a lean Jewish man in his early thirties, shoulder-length "
    "dark wavy hair, full beard, deep-set compassionate eyes, wearing a "
    "simple undyed woolen robe with a rough-woven mantle. Dignified, gentle, "
    "welcoming presence. A teaching scene -- no wounds, no crown of thorns.\n"
    "The Seeker: an ordinary weary man in his forties, short greying hair, "
    "lined face, plain earth-tone tunic and cloak, carrying a worn "
    "leather-bound ledger book pressed to his chest. Posture guarded, "
    "hopeful.\n"
    "The Door: a massive ancient wooden door, iron-banded, set in a rough "
    "stone wall, standing ajar with warm golden light spilling through the "
    "gap."
)

PREFIX = AESTHETIC + "\n\n" + CONSTRAINT + "\n\n" + ANCHORS + "\n\n"

CHAIN_LINE = (
    "This panel continues directly from the reference image: same figures, "
    "same world, same ink style.\n\n"
)

STYLE_TAIL = (
    "EXPLICIT STYLE CONSTRAINTS: Vintage graphic novel comic-book art, heavy "
    "black ink linework, high-contrast chiaroscuro, muted earth tones, "
    "reverent and dignified treatment throughout, absolutely no text or "
    "lettering anywhere."
)

PANEL_A = PREFIX + (
    "SINGLE PANEL COMPOSITION: Close-up of Jesus' face and shoulders, turned "
    "slightly toward the viewer, expression of quiet, certain welcome -- the "
    "moment of \"I will in no wise cast out.\" Lighting: soft single warm "
    "key against deep shadow.\n\n"
) + STYLE_TAIL

PANEL_B = PREFIX + CHAIN_LINE + (
    "SINGLE PANEL COMPOSITION: The Seeker seen from behind at medium "
    "distance, stepping toward the great ancient door standing ajar, warm "
    "golden light spilling through the gap onto the stone floor toward his "
    "feet. Lighting: cold slate surroundings, warm light only from the door "
    "gap.\n\n"
) + STYLE_TAIL

PANEL_C = PREFIX + CHAIN_LINE + (
    "SINGLE PANEL COMPOSITION: Extreme close-up of the Seeker's hands "
    "clutching the worn leather ledger to his chest, knuckles tense, a "
    "frayed strap hanging. Lighting: dim, a sliver of the door's warm light "
    "catching the ledger's edge.\n\n"
) + STYLE_TAIL

PANEL_D = PREFIX + CHAIN_LINE + (
    "SINGLE PANEL COMPOSITION: Wide shot -- the Seeker crossing the "
    "threshold into the light, door swung open, and beyond it the standing "
    "figure of Jesus with a hand extended in welcome. Lighting: the warm "
    "light now dominant, shadows breaking.\n\n"
) + STYLE_TAIL

PANELS = [
    ("panel_a_jesus", PANEL_A),
    ("panel_b_door", PANEL_B),
    ("panel_c_ledger", PANEL_C),
    ("panel_d_threshold", PANEL_D),
]


def _find_job(model, started_after_iso):
    """Timeout-recovery fallback (spec sec6 item 3): search recent jobs for one
    created after `started_after_iso` matching `model`; return its result_url
    once status == completed, else None."""
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


def run(prompt, out, refs, ar="9:16"):
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
        print("   --wait timed out; polling `hf generate list` for the real job status ...")
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
    prev = None
    for name, prompt in PANELS:
        out = OUT / f"{name}.png"
        refs = [prev] if prev else []
        print(f"[img ] {name} ({'chained' if refs else 'reference, no chain'}) ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached before this panel -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = run(prompt, out, refs)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[rung1-phase1] {name}")
                spent_usd += float(row.get("est_usd") or 0)
            except Exception as e:
                print(f"   (ledger record skipped: {e})")
            print(f"   ok ({time.time()-t:.0f}s)  running spend ~${spent_usd:.2f}")
            results.append((name, "clean", out))
            prev = out
        else:
            print("   FAILED")
            results.append((name, "FAILED", None))
            # keep `prev` as-is so a later panel doesn't chain off a missing file
    print(f"\n[out] {OUT}")
    print(f"[spend] ~${spent_usd:.2f} of ${HARD_CAP_USD:.2f} cap")
    for name, status, out in results:
        print(f"  {name}: {status}" + (f" -> {out}" if out else ""))


if __name__ == "__main__":
    main()
