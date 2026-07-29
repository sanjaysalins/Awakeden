"""Comic-style bake-off (Fable-authored brief, poc_comic_page/_STYLE_BAKEOFF_BRIEF.md):
render the SAME "Welcome at the Door" scene in 5 candidate comic-book art
styles, all chained to the existing Jesus + Seeker char sheets so the faces
stay recognizable while the STYLE is what's under test. NBP nano_banana_pro
(HF-billed, ~$0.30/still), $1.50 total for the round -- user-approved 2026-07-27.

  .venv\\Scripts\\python.exe poc_comic_page/_render_style_bakeoff.py
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
AR = "1:1"  # matches the baseline control p5a_the_welcome.png

HARD_CAP_USD = 2.00

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

# (name, style_block, closing_restatement)
CANDIDATES = [
    ("A_storybook_bible_strip",
     "Classic mid-century illustrated Bible storybook comic art: confident "
     "clean black ink outlines of even weight, warm flat color fills with "
     "simple two-tone shading, a sunny honeyed daylight palette of warm tan, "
     "terracotta, olive and sky blue, friendly naturalistic faces with clear "
     "readable expressions, minimal hatching, open uncluttered composition, "
     "smooth matte paper finish.",
     "Render in warm clean-ink storybook Bible-comic style throughout, sunny "
     "and inviting, not dark or painterly."),

    ("B_action_painterly",
     "Modern dynamic painted comic-book art: energetic loose ink drawing over "
     "fully painted color, a rich saturated palette with dramatic painted "
     "light and atmospheric depth, a sweeping cinematic camera angle, "
     "expressive lifelike faces, visible painterly brushwork in cloth and sky.",
     "Render in fully painted dynamic comic-book style throughout, rich and "
     "cinematic."),

    ("C_clean_line_european",
     "European clean-line comic album art: uniform-weight crisp black "
     "outlines around every form, perfectly flat color fills with zero "
     "gradients and zero hatching, a bright clear daylight palette, "
     "simplified accurately-proportioned figures against a precise detailed "
     "architectural background, calm balanced composition, smooth flat matte "
     "finish.",
     "Render in uniform clean-line European album style throughout, flat "
     "color, zero hatching."),

    ("D_watercolor_storybook",
     "Gentle watercolor storybook illustration: soft transparent watercolor "
     "washes over a fine light-brown ink drawing, a luminous warm palette "
     "that pools and blooms softly at the edges, generous pale paper "
     "breathing room, tender naturalistic faces, soft-edged shadows, the feel "
     "of a hand-painted Bible storybook plate.",
     "Render as a soft hand-painted watercolor storybook plate throughout, "
     "gentle and luminous."),

    ("E_modern_flat_webcomic",
     "Contemporary flat-color digital webcomic art: crisp dark-brown line "
     "art, bold simple shapes, flat cel shading in two clean tones per "
     "surface, a warm modern palette of amber, teal and cream, strong "
     "silhouette-first composition, large readable faces, generous negative "
     "space, clean smooth finish.",
     "Render in crisp flat-color modern webcomic style throughout, bold "
     "simple shapes, clean cel shading."),
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
                                      note=f"[style-bakeoff] {name}")
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
