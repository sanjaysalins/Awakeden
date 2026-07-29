"""Prove: RESTRAINED retro (the 'B' look the user liked) + CHARACTER-LOCKED (same
man) — on the nano_banana_pro + chained-reference path. 2 frames, ~$0.60.
Same ref as _prove_it.py (christ_pc_ref) so we can check it's the same man.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_restrained_locked.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
OUT = Path(__file__).resolve().parent / "_restrained_locked"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

# RESTRAINED retro — the 'B' feel: subtle dots, grounded, NO blazing halo
RETRO = ("Inked biblical graphic-novel illustration, bold confident black ink holding lines, flat "
         "muted earth-tone comic colour, only SUBTLE fine Ben-Day halftone dots in the sky, cream "
         "newsprint, gentle natural daylight, restrained, calm and reverent, premium comic-cover finish")
AVOID = ("no blazing sunburst, no glowing halo, no radiant holy-card rays, no heavy dots everywhere, "
         "no text, no lettering, no captions, no speech balloons, no panel borders or gutters, no "
         "watermark, no smooth digital gradients, no airbrushing, no glossy 3D render, no gore")
MATCH = "Keep the SAME man as the reference image: same face, same hair, same full beard, simple undyed robe."
TAIL = "reverent, ancient Near-Eastern period-accurate, NOT high-priestly vestments"

JOBS = {
    "restrained_hero": "The risen Lord Jesus Christ standing calmly, gentle reverent face, hands lowered at his sides, soft even daylight, a quiet ancient Near-Eastern landscape behind him",
    "restrained_welcome": "The risen Christ standing in a plain stone doorway, one hand extended in welcome toward the viewer, soft warm daylight (not blazing), calm and reverent",
}


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-160:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, subj in JOBS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{RETRO}. Compose this frame: {subj}. {TAIL}. {MATCH} AVOID: {AVOID}"
        print(f"[img ] {name} (nbp + ref, restrained) ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[restrained-locked] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
