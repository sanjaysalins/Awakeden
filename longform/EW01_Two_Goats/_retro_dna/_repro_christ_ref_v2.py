"""Reproducibility attempt #2 (2026-07-24): the first repro drifted in POSE
(arms raised, visible palm wounds, a halo ring) vs the ORIGINAL christ_pc_ref.png
(calm head-and-shoulders crop, gazing up, no arms/hands in frame, soft glow not
a halo ring) -- likely pulled toward the reference image's own arms-raised/
wounds pose. Tightening the framing language to explicitly lock the CROP
(chest-up, hands not in frame) since that's the biggest visible difference.
Same STYLE/AVOID, same reference image. 2 rolls, ~$0.60.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_repro_christ_ref_v2.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
OUT = Path(__file__).resolve().parent
REF = ROOT / "image_library" / "stills" / "christ_risen_face_scars.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich muted earth-tone painting, dramatic single strong key light "
         "with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth "
         "airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
AVOID = ("AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
         "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
         "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
         "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
         "separately by Remotion); no logo or watermark; no photoreal live-action; no smooth 3D "
         "render; no halftone dots; no modern machinery, clothing or tools; no gore.")
# tightened crop/pose language vs the original R_CHRIST -- explicit chest-up crop,
# hands out of frame, gazing up, soft glow (not a distinct halo ring)
R_CHRIST_V2 = ("the risen Lord Jesus Christ, gentle and majestic, warm compassionate face, "
               "shoulder-length dark hair and a short beard, in a simple luminous undyed white robe "
               "and NOT any high-priestly breastplate or ornate vestments; a close head-and-shoulders "
               "portrait cropped at the chest, hands and arms out of frame, gazing upward and slightly "
               "to the side in quiet contemplation; a warm soft golden light glowing gently from above "
               "and behind him, deep chiaroscuro shadow, dark background")

PROMPT = f"{STYLE} Compose this frame: {R_CHRIST_V2}. {AVOID}"


def run(out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", PROMPT, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    if not REF.exists():
        print(f"missing ref: {REF}"); sys.exit(1)
    for i in (1, 2):
        out = OUT / f"christ_pc_ref_REPRO_v2_{i}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        print(f"[img ] christ_pc_ref_REPRO_v2_{i} (tightened crop) ...", flush=True)
        t = time.time()
        if run(out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[repro-v2] christ_pc_ref_{i}")
            print(f"   ok ({time.time()-t:.0f}s) -> {out}")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
