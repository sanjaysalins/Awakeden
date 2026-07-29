"""Full-colour variant (2026-07-24): third point on the same spectrum as round
4 / the slight-colour test -- muted -> slight colour -> FULL rich natural
colour, all within the SAME painted-comic style (ink + dry-brush + chiaroscuro).
NOT a return to the earlier rejected Ben-Day-dot/CMYK/Silver-Age recipe -- that
was a different style family entirely. Same 2 test subjects as before. 2
renders, ~$0.60.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_full_color.py
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
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
CHRIST_REF = PCT / "christ_pc_ref.png"
AARON_REF = PCT / "aaron_pc_ref.png"

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
    " Render in full rich natural colour throughout -- a vivid blue sky, warm golden vestments, "
    "natural warm skin tones, rich earth-brown ground and tent fabric. Painterly and reverent, not "
    "flat or garish, not a comic-book primary-colour look, no Ben-Day dots, no CMYK misregistration.")
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

plan = json.loads((HERE.parent / "v1" / "visual_16x9_inked" / "scene_plan.json").read_text(encoding="utf-8"))
scene1 = plan["scenes"][0]["subject_block"]

R_CHRIST_PORTRAIT = ("the risen Lord Jesus Christ, gentle and majestic, warm compassionate face, "
                      "shoulder-length dark hair and a short beard, in a simple luminous undyed white "
                      "robe; a close head-and-shoulders portrait cropped at the chest, hands and arms "
                      "out of frame, gazing upward and slightly to the side in quiet contemplation; a "
                      "soft warm key light glowing gently from above and behind him, deep chiaroscuro "
                      "shadow, a dark background")

JOBS = [
    ("07_christ_portrait_fullcolour", R_CHRIST_PORTRAIT, [CHRIST_REF]),
    ("08_scene1_fullcolour", scene1, [AARON_REF]),
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
    for name, shot, refs in JOBS:
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{STYLE} Compose this frame: {shot}. {AVOID_FULL_COLOR} {MATCH}"
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-fullcolour] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
