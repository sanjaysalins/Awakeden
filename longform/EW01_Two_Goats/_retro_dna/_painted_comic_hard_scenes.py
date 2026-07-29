"""Hardest-content stress test (2026-07-24): crucifixion, flogging, crown of
thorns close-up -- the content this series has historically struggled with
(Isaiah-53 marred-not-heroic body gate, gore/blood restraint, ink render
failure modes on scars). Full-colour painted-comic recipe, same reference.
Crucifixion wording reused verbatim from the proven doctrine-gate test
(_prove_it.py's christ_cross_marred, 2026-07-23) -- already validated to
satisfy the AWAKEDEN COMIC DNA Sec5a body gate. 3 renders, ~$0.90.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_hard_scenes.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_round4"
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = PCT / "christ_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich painting, dramatic single strong key light with deep "
         "chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, "
         "not a 3D render, no halftone dots, no vintage newsprint.")
AVOID_BASE = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
              "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
              "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
              "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
              "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
              "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
AVOID_FULL_COLOR = AVOID_BASE + (
    " Render in full rich natural colour throughout, painterly and reverent, not flat or garish, not "
    "a comic-book primary-colour look, no Ben-Day dots, no CMYK misregistration.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

# crucifixion: verbatim from _prove_it.py's christ_cross_marred (proven to satisfy the
# Sec5a body gate -- gaunt/marred/sorrowful, no heroic muscle, no bright blood)
S_CROSS = ("Jesus Christ crucified on a wooden cross, a GAUNT, thin, marred, exhausted body with NO "
           "heroic muscle, NO defined six-pack abs, NO athletic build - as Isaiah wrote, no beauty "
           "that we should desire him; head bowed low in sorrow; only faint matted blood, NOT bright "
           "droplets; a dark brooding storm sky, deeply reverent and sorrowful")

S_FLOGGING = ("Jesus Christ bound at a low stone scourging post in a dim Roman judgment courtyard, "
              "head bowed low, back turned partly from view so no graphic wounds are shown, a Roman "
              "soldier standing at a distance with a scourge lowered at his side, the moment held in "
              "silence, gaunt and suffering but composed, deeply sorrowful and reverent, restrained "
              "and not graphic")

S_THORNS = ("Jesus Christ's face in close profile, a crown of twisted thorns pressed upon his brow, "
            "a single thin restrained line of blood at the forehead only, gaunt sorrowful expression, "
            "eyes downcast, deeply reverent and composed, subtle and restrained, not gory")

JOBS = [
    ("12_crucifixion_marred", S_CROSS),
    ("13_flogging_restrained", S_FLOGGING),
    ("14_crown_thorns_closeup", S_THORNS),
]


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(CHRIST_REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, shot in JOBS:
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{STYLE} Compose this frame: {shot}. {AVOID_FULL_COLOR} {MATCH}"
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-hard] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
