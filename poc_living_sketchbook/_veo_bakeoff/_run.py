"""veo3_1_lite bake-off POC -- cost/quality comparison against this
project's existing Kling/Seedance shorts tiering. Two test clips, reusing
already-approved stills from son_of_man_lifted_up and the EXACT motion
prompts already used there, so the only variable is the animation model:

  s08_cross_hero (currently Kling, the hero/reverent-hold tier)
  s07_nicodemus_skeptic (currently Seedance, the calm/portrait tier)

Real HF cost-estimator quotes before this run: veo3_1_lite 4s@9:16 = 4cr
(~$0.60) vs. Kling pro 5s@9:16 verified actual = 7.5cr (~$1.13) vs.
Seedance 4s@9:16 verified actual = 4.8cr (~$0.72) -- veo estimate is
cheaper than both if it holds.

Known prior finding (2026-05-30 bake-off, this project's own history):
veo does NOT respect the shorts' "camera-only, INVENT NOTHING new" crop-
cut discipline -- it tends to animate the subject and invent movement
instead of holding still. This POC re-tests that on today's model version.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_veo_bakeoff/_run.py
"""
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
EPISODE = "POC_VeoBakeoff"
HERE = Path(__file__).resolve().parent
OUT = HERE / "clips"
OUT.mkdir(exist_ok=True)

SOMLU = ROOT / "poc_living_sketchbook" / "son_of_man_lifted_up" / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")

# (name, still, duration, motion) -- same prompts as _s2_animate.py verbatim
JOBS = [
    ("s07_nicodemus_skeptic_VEO", SOMLU / "s07_nicodemus_skeptic.png", 4,
     "Nicodemus holds his exact expression and head position, perfectly "
     "still -- no blink, no head turn. Only: the lamp-glow on his face "
     "breathes very faintly. Nothing else changes."),

    ("s08_cross_hero_VEO", SOMLU / "s08_cross_hero.png", 4,
     "The figure on the cross stays perfectly frozen like a statue -- "
     "His exact pose, head, and arms never change, no movement at all. "
     "INVENT NOTHING new. Only: the storm clouds behind Him drift and "
     "shift very slowly, the light breathes softly. Nothing else in the "
     "frame changes."),
]


def run(name, still, duration, motion):
    if not still.exists():
        print(f"[HOLD] {name}: still missing ({still})")
        return
    out = OUT / f"{name}.mp4"
    if out.exists():
        print(f"[skip] {name}")
        return
    prompt = LOCK + motion
    cmd = [HF, "generate", "create", "veo3_1_lite",
           "--start-image", str(still), "--prompt", prompt,
           "--aspect_ratio", "9:16", "--duration", str(duration), "--wait"]
    print(f"[clip] {name} (veo3_1_lite) ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED")
        return
    m = re.search(r"https?://\S+?\.mp4", blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-400:]}")
        return
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        try:
            cost.record_hf(EPISODE, "clip", "animate", "veo3_1_lite",
                            image=still, note=f"[bakeoff] {name}",
                            params={"duration": duration, "aspect_ratio": "9:16"})
        except Exception as e:
            print(f"   (ledger skipped: {e})")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
    else:
        print("   FAILED")


def main():
    for name, still, duration, motion in JOBS:
        run(name, still, duration, motion)


if __name__ == "__main__":
    main()
