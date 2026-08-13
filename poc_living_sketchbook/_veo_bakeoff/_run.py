"""veo3_1_lite bake-off POC -- cost/quality comparison against this
project's existing Kling/Seedance shorts tiering. Reuses already-approved
stills and the EXACT motion prompts already used for them, so the only
variable is the animation model.

ROUND 1 (2026-08-13, both "hold perfectly still" cases):
  s08_cross_hero (Kling, hero/reverent-hold) -- veo won, genuine
    atmospheric cloud drift, held perfectly.
  s07_nicodemus_skeptic (Seedance, calm/portrait) -- veo softened face
    fidelity (gaze/expression drifted from the source still) vs Seedance.
  Real billed cost both times: veo 4cr/$0.60 vs Kling 7.5cr/$1.13 vs
  Seedance 4.8cr/$0.72.
Decision from round 1: veo3_1_lite ADOPTED as the shorts hero-tier
default (see CLAUDE.md + memory feedback-spend-only-for-cinematic-value).

ROUND 2 (2026-08-13, filling the 2 known gaps + a replicate test):
  s05_acting_memory_bleed (Kling, DESIGNED motion -- a gesture, not just
    hold-still) -- tests whether veo can execute a cued motion, not just
    freeze.
  s10_crowd_multivignette (Seedance, multi-figure crowd) -- tests the
    exact failure mode from the 2026-05-30 prior bake-off (veo invented
    movement/dissolves on a dynamic multi-figure scene).
  look_and_live's s12b_landing_gold (Kling, 2nd hero/wide shot) --
    replicate test: does the round-1 hero-tier win hold on a SECOND shot,
    or was s08_cross_hero a lucky draw?

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
LYL = ROOT / "poc_living_sketchbook" / "look_and_live" / "stills"

LOCK = ("The camera does not move, zoom, or change angle at all. INVENT "
        "NOTHING new -- no new figures, objects, or marks appear; the paper "
        "texture, torn edges, and every sketch line hold perfectly still. ")
NOGLITTER = ("the light stays a steady, even glow -- it does not sparkle, "
             "flicker into particles, or scatter into glitter. ")

# (name, still, duration, motion) -- same prompts as each episode's own
# _s2_animate.py verbatim
JOBS = [
    # -- round 1 (done, kept for the record / idempotent skip) --
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

    # -- round 2 (new) --
    ("s05_acting_memory_bleed_VEO", SOMLU / "s05_acting_memory_bleed.png", 4,
     "Jesus's head and hand complete ONE slow, small motion -- gesturing "
     "gently as He speaks, His hand lifting slightly -- then holding that "
     "position still for the rest of the clip. Nicodemus holds his exact "
     "listening pose, perfectly still. The memory-bleed wilderness/"
     "serpent scene behind Him holds its exact translucent shape, "
     "unmoving. INVENT NOTHING new otherwise. Nothing else in the frame "
     "changes."),

    ("s10_crowd_multivignette_VEO", SOMLU / "s10_crowd_multivignette.png", 4,
     "Every figure holds their exact position and pose, perfectly still "
     "-- no one turns or gestures further. INVENT NOTHING new. Only: the "
     "light breathes very faintly. Nothing else changes."),

    # Retry, positive-only phrasing -- the first attempt used Kling's own
    # NOGLITTER negative phrasing verbatim and got heavy sparkle/glitter
    # hallucination, matching this project's own already-documented veo
    # weakness (feedback-veo-no-glitter-glow: negative "no glitter" text
    # does NOT reliably suppress it on bright/glowing scenes -- needs
    # positive-only "stays exactly as it is" phrasing instead, no particle
    # words anywhere in the prompt).
    ("s12b_landing_gold_VEO", LYL / "s12b_landing_gold.png", 4,
     "The figure on the cross stays perfectly frozen like a statue -- His "
     "exact pose, head, and arms never change, no movement at all. The "
     "torn paper edges hold their exact shape. The radiant gold light "
     "surrounding Him stays exactly as warm and steady as it already is "
     "in this image, completely unchanged. Nothing else in the frame "
     "changes."),
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
