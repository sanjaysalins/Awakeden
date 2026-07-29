"""Style-spectrum bake-off (2026-07-24): 3 NEW middle-ground style variants,
same ★ reference face (christ_pc_ref.png) + same nano_banana_pro + chained
--image ref as every other proven identity test, same "standing hero" pose
so it's a fair side-by-side with the 2 EXISTING extremes:
  - HARD  (today's, rejected by the user): _prove_it/christ_hero.png
  - RESTRAINED (yesterday's, "the look the user liked"): _restrained_locked/restrained_hero_finished.png
Goal: give the user real options between those two poles, not guess again.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_style_spectrum_bakeoff.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
OUT = Path(__file__).resolve().parent / "_style_spectrum"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

# Same pose for all 3, chosen to sit between the existing hard/restrained hero shots.
SUBJ = ("The risen Lord Jesus Christ standing calmly, gentle reverent face, one hand resting at "
        "his side, soft warm daylight, a quiet ancient Near-Eastern landscape behind him")
MATCH = "Keep the SAME man as the reference image: same face, same hair, same full beard, simple undyed robe."
TAIL = "reverent, ancient Near-Eastern period-accurate, NOT high-priestly vestments"
AVOID_BASE = ("no blazing sunburst, no glowing halo, no radiant holy-card rays, no heavy dots on skin or "
              "face, no text, no lettering, no captions, no speech balloons, no panel borders or gutters, "
              "no watermark, no smooth digital gradients, no airbrushing, no glossy 3D render, no gore")

VARIANTS = {
    "m1_warm_moderate": (
        "Inked biblical comic illustration, bold confident black ink holding lines, warm richly-coloured "
        "comic palette (not flat primaries, not muted earth-tone), soft fine Ben-Day halftone dots visible "
        "only in the sky, cream paper tone, gentle warm daylight",
        AVOID_BASE,
    ),
    "m2_storybook_ink": (
        "Premium illustrated storybook art with confident black ink outlines, soft painted colour shading "
        "within the linework, a warm muted palette, faint halftone texture only in the sky, gentle natural "
        "light, timeless and reverent",
        AVOID_BASE,
    ),
    "m3_punchy_clean": (
        "Inked comic-book illustration, bold black ink holding lines, rich saturated but tasteful comic "
        "colour, clearly visible Ben-Day halftone dots in the sky only, clean bright daylight, premium "
        "comic-cover finish",
        AVOID_BASE,
    ),
}


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-200:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    if not REF.exists():
        print(f"missing ref: {REF}"); sys.exit(1)
    for name, (retro, avoid) in VARIANTS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{retro}. Compose this frame: {SUBJ}. {TAIL}. {MATCH} AVOID: {avoid}"
        print(f"[img ] {name} (nbp + ref) ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[style-spectrum] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
