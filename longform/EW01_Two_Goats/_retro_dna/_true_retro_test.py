"""TRUE-RETRO recipe test (2026-07-23): push the render hard toward authentic
vintage comic PRINT — visible Ben-Day dots, flat 4-colour, newsprint, misreg —
so the base itself is retro (not ink). seedream_v4_5. ~2cr each.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_true_retro_test.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "seedream_v4_5"
OUT = Path(__file__).resolve().parent / "_true_retro"
OUT.mkdir(exist_ok=True)

RETRO = ("Authentic vintage 1960s Silver Age comic book art printed on aged cream newsprint, "
         "bold black ink holding lines, flat limited four-colour comic colour with NO gradients, "
         "clearly VISIBLE coarse Ben-Day halftone dots filling every sky and shadow, slight CMYK "
         "colour misregistration, low-fi retro print texture")
TAIL = "reverent, ancient Near-Eastern period-accurate, no gore, no modern items"
AVOID = "no smooth digital gradients, no airbrushing, no glossy 3D render, no painterly brushwork"

JOBS = {
    "jesus": "The risen Lord Jesus Christ standing in a simple undyed robe, gentle reverent face, warm light behind",
    "cross": "Jesus Christ on the cross at Golgotha, dark storm sky, a shaft of light, dramatic low angle",
    "veil": "the great temple veil torn in two from top to bottom, brilliant light bursting through the gap",
    "aaron_wide": "wide establishing shot, the high priest Aaron small before the great curtained desert Tabernacle TENT of woven curtains at dawn, a hushed crowd of Israelites in shadow, NOT an Egyptian temple, no stone columns",
    "reaction": "extreme close-up of an awed ancient Near-Eastern man's face looking up in astonishment and wonder, wide eyes",
    "welcome": "the risen Christ standing in a bright open doorway of light, one hand extended in welcome toward the viewer, warm and reverent",
}


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
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
        prompt = f"{RETRO}. {subj}. {TAIL}. AVOID: {AVOID}"
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[true-retro] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
