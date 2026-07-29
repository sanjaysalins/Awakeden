"""Reproducibility check (2026-07-24): re-run the EXACT bootstrap prompt that made
christ_pc_ref.png (verbatim from _painted_comic_test.py's JOBS list, the
"christ_pc_ref" entry: use_match=False, so NO "Match the inked chiaroscuro..."
suffix -- that was only added to the LATER jobs that reuse this ref). Same
model, same reference image, same resolution/aspect. $0.30, 1 render.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_repro_christ_ref.py
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

# verbatim from _painted_comic_test.py
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
R_CHRIST = ("the risen Lord Jesus Christ, gentle and majestic, warm compassionate face, "
            "shoulder-length dark hair and a short beard, in a simple luminous undyed white robe "
            "and NOT any high-priestly breastplate or ornate vestments; head-and-shoulders "
            "portrait, a warm radiant single key light, deep chiaroscuro shadow, dark background")

# EXACT same assembly as gen() in _painted_comic_test.py, use_match=False (bootstrap job)
PROMPT = f"{STYLE} Compose this frame: {R_CHRIST}. {AVOID}"


def main():
    if not REF.exists():
        print(f"missing ref: {REF}"); sys.exit(1)
    out = OUT / "christ_pc_ref_REPRO.png"
    if out.exists() and out.stat().st_size > 1000:
        print(f"[skip] {out.name}"); return
    cmd = [HF, "generate", "create", MODEL, "--prompt", PROMPT, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(REF)]
    print("[img ] christ_pc_ref_REPRO (verbatim bootstrap prompt) ...", flush=True)
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 1000:
        cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note="[repro] christ_pc_ref_REPRO")
        print(f"   ok ({time.time()-t:.0f}s) -> {out}")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
