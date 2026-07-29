"""Reroll scenes 2, 3, 4 with fixed wording:
- 2/3: explicit "already nailed/hanging on the cross" grounding (round-1 drew a
  man CARRYING a cross beam instead of one crucified on it).
- 3: make the rebuke readable -- one thief distinctly grave/honest, the other
  still visible sneering, both clearly on their own crosses.
- 4: reinforce the "robed" instruction even further (round-1 background Christ
  came back bare-chested despite the same base wording that passed on 4 other
  scenes -- known ~25% stochastic miss, reinforcing wording rather than
  assuming a rewrite fixes it for certain).

  .venv\\Scripts\\python.exe poc_thief_e2e/_reroll_2_3_4.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
CHRIST_REF = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich painting, dramatic single strong key light with deep "
         "chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, "
         "not a 3D render, no halftone dots, no vintage newsprint.")
AVOID_FULL_COLOR = (
    "AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
    "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
    "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
    "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
    "separately later); no logo or watermark; no photoreal live-action; no smooth 3D render; no "
    "halftone dots; no modern machinery, clothing or tools; no gore. Render in full rich natural "
    "colour throughout, painterly and reverent, not flat or garish, not a comic-book primary-colour "
    "look, no Ben-Day dots, no CMYK misregistration."
)
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

JOBS = {
    2: (
        "One of the two criminals, already nailed to a wooden cross and hanging still, his arms "
        "stretched along the crossbeam, feet nailed at the base of the upright; his face twisted in "
        "scorn and pain, sneering sideways off-frame toward the centre cross; harsh midday sun, no "
        "other figures close, no blood, restrained.",
        [],
    ),
    3: (
        "Two men, each already nailed to his own wooden cross and hanging still, arms stretched along "
        "the crossbeams, side by side; the one on the left sneering with scorn, the one on the right "
        "grave and honest, turning his head to rebuke him; the centre cross with Jesus faintly visible "
        "beyond in the haze; harsh daylight, dust in the air, restrained, no blood.",
        [],
    ),
    4: (
        "Close on the penitent thief's weary, resigned face, his eyes now turning toward Jesus on the "
        "centre cross in the soft distance -- Jesus's ENTIRE body completely covered from shoulder to "
        "ankle by a long pale robe, no bare chest or skin visible on his torso, head bowed -- a flicker "
        "of honesty and hope breaking through the thief's pain.",
        [CHRIST_REF],
    ),
}


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "9:16",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
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
    for sid, (shot, refs) in JOBS.items():
        out = OUT / f"{sid:02d}.png"
        prompt = f"{STYLE} Compose this frame: {shot}. {AVOID_FULL_COLOR}"
        if refs:
            prompt += " " + MATCH
        print(f"[img ] reroll scene {sid} ...", flush=True)
        t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note=f"[reroll] scene {sid}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
