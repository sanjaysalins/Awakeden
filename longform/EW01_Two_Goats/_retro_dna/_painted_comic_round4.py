"""Painted-comic round 4 (2026-07-24): test the refined recipe (crop-locked +
explicit muted/desaturated tone, confirmed closest to the original in round 3)
across more content: a different Christ pose, a middle-ground tone variant,
Aaron in the same recipe, and a re-test of scene 1 (an environmental multi-
figure scene, not just a headshot) with the corrected tone. 4 renders, ~$1.20.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_round4.py
"""
import json, re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "_round4"
OUT.mkdir(exist_ok=True)
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = PCT / "christ_pc_ref.png"
AARON_REF = PCT / "aaron_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich muted earth-tone painting, dramatic single strong key light "
         "with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth "
         "airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
AVOID_BASE = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
              "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
              "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
              "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
              "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
              "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
AVOID_MUTED = AVOID_BASE + (" AVOID vivid saturated golden-yellow colour; keep the palette muted, "
                            "desaturated, near-monochrome warm sepia-brown and black.")
AVOID_MID = AVOID_BASE + (" Keep a warm sepia-brown palette with gentle warmth -- restrained and "
                          "muted, not vividly saturated, but not fully monochrome either.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

plan = json.loads((HERE.parent / "v1" / "visual_16x9_inked" / "scene_plan.json").read_text(encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

S_WELCOME = ("HERO splash: the risen Christ standing in a full open doorway of radiant light, a great "
             "torn temple veil framing him on either side, one hand extended toward the viewer in "
             "welcome, the way wide open behind him; ancient Near-Eastern setting; keep the lower "
             "third quiet")
S_AARON_PORTRAIT = ("Aaron, the aged high priest of Israel, a close head-and-shoulders portrait cropped "
                     "at the chest, hands and arms out of frame, weathered dignified face turned "
                     "slightly aside in quiet solemnity, plain undyed linen visible at the shoulders")

JOBS = [
    # (out_name, prompt_shot, avoid_text, refs, use_match)
    ("01_christ_welcome_muted", S_WELCOME, AVOID_MUTED, [CHRIST_REF], True),
    ("02_christ_portrait_midtone",
     ("the risen Lord Jesus Christ, gentle and majestic, warm compassionate face, shoulder-length dark "
      "hair and a short beard, in a simple luminous undyed white robe; a close head-and-shoulders "
      "portrait cropped at the chest, hands and arms out of frame, gazing upward and slightly to the "
      "side in quiet contemplation; a soft warm key light glowing gently from above and behind him, "
      "deep chiaroscuro shadow, a dark near-black background"),
     AVOID_MID, [CHRIST_REF], True),
    ("03_aaron_portrait_muted", S_AARON_PORTRAIT, AVOID_MUTED, [AARON_REF], True),
    ("04_scene1_muted", scenes[1]["subject_block"], AVOID_MUTED, [AARON_REF], True),
]


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, shot, avoid, refs, use_match in JOBS:
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{STYLE} Compose this frame: {shot}. {avoid}"
        if use_match:
            prompt += " " + MATCH
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-round4] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
