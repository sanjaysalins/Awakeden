"""CHARACTER-CONSISTENCY STRESS TEST.
One distinctive witness (Caleb, hard markers: scar/earring/rust scarf/black beard).
Two tracks per model:
  P = prompt-only (identical char text, vary scene)  -> text-locked stability
  R = reference-locked (--image = model's own REF portrait) -> true char lock
1 REF portrait + 5 diverse stress scenes. Idempotent, rate-limit-aware. Scratchpad only."""
import re, subprocess, urllib.request
from pathlib import Path

HF = str(Path.home() / "bin" / "hf.exe")
URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
HERE = Path(__file__).parent
OUT = HERE / "charcon"
OUT.mkdir(parents=True, exist_ok=True)

# model -> accepts --image reference?
MODELS = {
    "z_image": False,            # no media inputs -> prompt-only only
    "flux_2": True,
    "grok_image": True,
    "nano_banana": True,
    "seedream_v4_5": True,
    "seedream_v5_lite": True,
    "nano_banana_flash": True,
}
ASPECT = "9:16"

CHAR = ("Caleb, a Hebrew man of about twenty-five, olive skin, a lean angular face, a short "
        "black beard, deep-set dark brown eyes, thick black eyebrows, a thin pale scar through "
        "his left eyebrow, a small gold hoop earring in his left ear, wearing a faded rust-red "
        "headscarf and a coarse undyed linen tunic")
STYLE = (" Biblical epic graphic novel style, cinematic manga composition, dramatic ink shadows, "
         "sacred reverent atmosphere, realistic proportions, ancient Near-Eastern period-accurate, "
         "mature teen-and-up tone. No text, no lettering, no panels, no speech bubbles, "
         "no watermark, no signature.")

REF = (CHAR + ", clean character reference portrait, head and shoulders, facing forward, neutral "
       "calm expression, even soft studio light, plain dark neutral background." + STYLE)

# (slug, scene-suffix) — deliberately diverse setting / light / framing / emotion / action
SCENES = [
 ("noon_close", " extreme close-up of his face under harsh desert noon sun, squinting against the "
   "glare, sweat on his brow, blazing white sky behind."),
 ("night_fire", " wide shot sitting beside a small campfire at night, warm orange firelight on one "
   "side of his face, deep darkness around, distant stars."),
 ("lamp_room", " inside a dim stone room lit by a single small oil lamp, three-quarter profile, "
   "somber and thoughtful, holding a clay cup, deep shadows."),
 ("storm_ridge", " mid shot standing on a rocky ridge in a driving rainstorm, shouting, his "
   "rust-red headscarf and tunic whipping in the wind, lightning behind."),
 ("crowd_market", " mid-distance among a busy ancient marketplace crowd, anxious expression, other "
   "robed figures around him, dusty stalls and hanging cloth."),
]
LOCK = " Keep the exact same face, beard, scar over the left eyebrow and gold earring as the reference image."


def run(args, dest):
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[skip] {dest.name}", flush=True); return True
    for attempt in (1, 2, 3):
        try:
            r = subprocess.run([HF, "generate", "create", *args, "--aspect_ratio", ASPECT, "--wait"],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=600)
        except Exception as e:
            print(f"[ERR ] {dest.name}: {e}", flush=True); continue
        blob = (r.stdout or "") + (r.stderr or "")
        m = URL_RE.search(blob)
        if m:
            req = urllib.request.Request(m.group(0), headers={"User-Agent": "poc/1.0"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                dest.write_bytes(resp.read())
            print(f"[ok  ] {dest.name}", flush=True); return True
        print(f"[{'retry' if attempt<3 else 'FAIL'}] {dest.name} (rc={r.returncode})"
              f"{'' if attempt<3 else chr(10)+blob[-240:]}", flush=True)
    return False


if __name__ == "__main__":
    ok = total = 0
    for model, has_ref in MODELS.items():
        # 1) canonical REF portrait
        ref_png = OUT / f"CC__{model}__REF.png"
        total += 1
        if run([model, "--prompt", REF], ref_png):
            ok += 1
        # 2) prompt-only scenes
        for slug, suf in SCENES:
            total += 1
            if run([model, "--prompt", CHAR + suf + STYLE], OUT / f"CC__{model}__P_{slug}.png"):
                ok += 1
        # 3) reference-locked scenes (only ref-capable models, needs the REF to exist)
        if has_ref and ref_png.exists():
            for slug, suf in SCENES:
                total += 1
                if run([model, "--prompt", CHAR + suf + LOCK + STYLE, "--image", str(ref_png)],
                       OUT / f"CC__{model}__R_{slug}.png"):
                    ok += 1
    print(f"\nDONE {ok}/{total} char-consistency stills in {OUT}", flush=True)
