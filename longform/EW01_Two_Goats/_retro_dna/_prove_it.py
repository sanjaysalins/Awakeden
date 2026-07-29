"""PROVE-IT bake-off (2026-07-23) — test the 2 red-team blockers at once:
  (1) CHARACTER LOCK: render 3 different Christ scenes on nano_banana_pro with the
      SAME reference chained (--image), per _painted_comic_bright.py + the locked
      NBP-for-faces rule. If it's the same man across all 3, drift is solved.
  (2) ISAIAH 53 CROSS: render the crucifixion MARRED / non-heroic (no bodybuilder
      body, no bright blood) as the doctrine acceptance test.
Also fixes the render prompt: restores the no-text / no-panel / no-bubble negatives.
nano_banana_pro via HF (~2cr each). ~$0.90-1.20.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_prove_it.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
OUT = Path(__file__).resolve().parent / "_prove_it"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

RETRO = ("Authentic vintage 1960s Silver Age comic book art, bold black ink holding lines, flat "
         "limited four-colour comic colour, clearly visible coarse Ben-Day halftone dots in the "
         "skies and shadows, cream newsprint, slight CMYK misregistration, retro print look")
# blocker #2 fix: the no-text / no-panel / no-bubble negatives are back
AVOID = ("no text, no lettering, no numbers, no captions, no speech balloons, no panel borders or "
         "gutters, no title box, no watermark, no smooth digital gradients, no airbrushing, no glossy "
         "3D render, no painterly brushwork, no gore, no modern items")
MATCH = "Keep the SAME man as the reference image: same face, same hair, same full beard, undyed robe."
TAIL = "reverent, ancient Near-Eastern period-accurate, a simple undyed robe (NOT high-priestly vestments)"

JOBS = {
    "christ_hero": "The risen Lord Jesus Christ standing, calm reverent face, one hand gently raised, warm holy light behind him",
    "christ_welcome": "The risen Christ standing in an open doorway of light, one hand extended in welcome toward the viewer",
    "christ_cross_marred": ("Jesus Christ crucified on a wooden cross, a GAUNT, thin, marred, exhausted body with NO "
                            "heroic muscle, NO defined six-pack abs, NO athletic build - as Isaiah wrote, no beauty "
                            "that we should desire him; head bowed low in sorrow; only faint matted blood, NOT bright "
                            "droplets; a dark brooding storm sky; deeply reverent and sorrowful"),
}


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait", "--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED (bare-torso cross — may need a clothed framing)"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-160:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    if not REF.exists():
        print(f"missing ref: {REF}"); sys.exit(1)
    for name, subj in JOBS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{RETRO}. Compose this frame: {subj}. {TAIL}. {MATCH} AVOID: {AVOID}"
        print(f"[img ] {name} (nbp + ref) ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[prove-it] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
