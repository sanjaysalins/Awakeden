"""Comic Page Pipeline POC -- Rung 2, PHASE A (11 panel stills, NO animation).

Renders the remaining 4 pages (1, 2, 4, 5) of "In No Wise Cast Out" (page 3
already exists from Rung 1). Each panel references ONE of the four Rung 1
canon stills directly (poc_comic_page/rung1/stills/panel_{a,b,c,d}_*.png) --
NOT chained panel-to-panel within this run. Reuses the verbatim aesthetic /
GLOBAL TEXTUAL CONSTRAINT / CORE CHARACTER DESIGN ANCHORS / style-tail blocks
and the ledger try/except pattern from poc_comic_page/rung1/_render_panel_stills.py.

  .venv\\Scripts\\python.exe poc_comic_page/rung2/_render_panel_stills.py
"""
import re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
EPISODE = "CPP_Rung2_InNoWise"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(parents=True, exist_ok=True)
REF_DIR = ROOT / "poc_comic_page" / "rung1" / "stills"

HARD_CAP_USD = 4.50

# ---- Master Comic Blueprint sections (verbatim from rung1) -----------------
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

# ---- 11 panels: (name, aspect_ratio, ref_filename, composition text) -------
PANELS = [
    ("p1a_night_door", "1:1", "panel_b_door.png",
     "Wide establishing shot at night: the Seeker standing alone and small "
     "before the great arch-topped iron-banded door, shut, in a vast rough "
     "stone wall. Cold slate-blue darkness everywhere; one thin line of warm "
     "light escaping under the closed door. He stands a few paces back, "
     "ledger clutched to his chest. Lighting: cold moonless night, the only "
     "warmth is the thin light-line under the door."),

    ("p1b_hesitant_hand", "1:1", "panel_c_ledger.png",
     "Close-up from behind and beside the Seeker: his weathered hand "
     "half-raised toward the closed door's dark wood, hesitating, knuckles "
     "bent, NOT touching it; his other arm presses the worn leather ledger "
     "to his chest. Lighting: dim cold light, a faint warm glow from the gap "
     "below the door edge."),

    ("p2a_rehearsing", "9:16", "panel_d_threshold.png",
     "Tall portrait shot: the Seeker leaning his forehead against the closed "
     "door's frame, eyes shut, lips parted mid-whisper -- rehearsing his "
     "plea. The ledger pressed between his chest and the door frame. "
     "Lighting: cold surroundings, the warm under-door light touching his "
     "sandals."),

    ("p2b_jesus_speaks", "9:16", "panel_a_jesus.png",
     "Close-up of Jesus' face in three-quarter profile, mid-speech, calm and "
     "certain, warm light on his face against deep shadow. Same man as the "
     "reference: broader rugged face, shoulder-length dark wavy hair, full "
     "beard, undyed woolen robe."),

    ("p2c_light_line", "9:16", "panel_b_door.png",
     "Extreme close-up at floor level: the thin line of warm golden light "
     "under the great door's edge, spilling across worn stone flags toward "
     "the viewer, the Seeker's sandaled feet standing at its edge in the "
     "cold shadow. Lighting: one warm light-line cutting the cold dark."),

    ("p4a_turning_away", "9:16", "panel_d_threshold.png",
     "Tall portrait shot: the Seeker half-turned AWAY from the door, head "
     "bowed, face falling into deep shadow, the ledger hanging heavy in one "
     "hand at his side. Behind him the door's warm light-line still glows. "
     "Lighting: his face and chest in cold shadow, the warm light behind "
     "him low and patient."),

    ("p4b_open_hands", "9:16", "panel_a_jesus.png",
     "Close-up of Jesus' two open hands held out palms-up, empty and "
     "unmarked, the sleeves of the undyed woolen robe falling back from the "
     "wrists. Warm light pooling in the open palms against deep shadow. "
     "Exactly two hands, five fingers each, natural proportions."),

    ("p4c_empty_doorway", "9:16", "panel_d_threshold.png",
     "The great arch-topped door standing wide open with no one in the "
     "doorway: warm golden light flooding out across empty worn stone "
     "flags. Lighting: radiant warm light from the empty doorway into cold "
     "blue surroundings."),

    ("p5a_the_welcome", "1:1", "panel_d_threshold.png",
     "Wide warm shot at the open threshold: Jesus laying one hand on the "
     "Seeker's shoulder, the Seeker's head lifting, the radiant doorway "
     "light surrounding them both. Same two men as the reference: Jesus "
     "with the broader rugged face and undyed woolen robe; the Seeker with "
     "short greying hair, lined face, earth-tone cloak, ledger under his "
     "arm. Lighting: full warm radiance, shadows breaking apart."),

    ("p5b_record_received", "3:4", "panel_c_ledger.png",
     "Close-up: the worn leather ledger with its frayed strap now resting "
     "in Jesus' open hand, held gently, the Seeker's empty hands releasing "
     "it in the soft-focus background warmth. Lighting: warm light on the "
     "ledger and the receiving hand."),

    ("p5c_never_locked", "3:4", "panel_b_door.png",
     "Close-up of the great door's edge standing open: a simple iron latch "
     "resting freely open, the door swung wide, warm light along its worn "
     "wood. Lighting: warm and settled, the cold blue gone."),
]


def _find_job(model, started_after_iso):
    """Timeout-recovery fallback: search recent jobs for one created after
    `started_after_iso` matching `model`; return its result_url once
    status == completed, else None."""
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
    for name, ar, ref_name, comp in PANELS:
        out = OUT / f"{name}.png"
        ref = REF_DIR / ref_name
        prompt = PREFIX + CHAIN_LINE + f"SINGLE PANEL COMPOSITION: {comp}\n\n" + STYLE_TAIL
        print(f"[img ] {name} (AR {ar}, ref {ref_name}) ...", flush=True)
        if spent_usd >= HARD_CAP_USD:
            print(f"   STOP: hard cap ${HARD_CAP_USD:.2f} reached before this panel -- escalating.")
            results.append((name, "ESCALATED-cap", None))
            continue
        t = time.time()
        ok = run(prompt, out, [ref], ar)
        if ok:
            try:
                row = cost.record_hf(EPISODE, "short", "stills", MODEL, note=f"[rung2-phase-a] {name}")
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
