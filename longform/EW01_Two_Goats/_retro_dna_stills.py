"""Retro-comic DNA example stills (2026-07-23) — for the retro-comic study board.
Shows the Silver-Age look (Ben-Day dots, 4-colour, bold ink) on OUR content:
a splash, an action panel, a reaction close-up, a hero. seedream_v4_5. ~2cr each.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna_stills.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "seedream_v4_5"
OUT = Path(__file__).resolve().parent / "_retro_dna"
OUT.mkdir(parents=True, exist_ok=True)
RETRO = ("Vintage Silver Age comic-book art, bold black ink outlines and spot blacks, Ben-Day "
         "halftone dot shading, limited saturated four-colour print on aged cream newsprint, retro")
TAIL = "ancient Near-Eastern period-accurate, reverent, no gore, no modern items"

JOBS = {
    "splash_cross": f"{RETRO} dramatic full splash-page composition: Jesus Christ on the cross at Golgotha, low heroic angle, dark storm sky with lightning, a shaft of light. {TAIL}",
    "action_veil": f"{RETRO} dynamic action panel with bold speed-lines and motion streaks: the great temple veil ripping in two from top to bottom, brilliant light bursting through the tear, dramatic. {TAIL}",
    "reaction_face": f"{RETRO} extreme close-up reaction panel: an awed ancient Near-Eastern man's face looking up in astonishment and wonder, sweat, wide eyes, dramatic. {TAIL}",
}


def run(prompt, out):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"       no url: {blob.strip()[-160:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, prompt in JOBS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        print(f"[img ] {name} ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[retro-dna] {name}")
            print(f"       ok ({time.time()-t:.0f}s)")
        else:
            print("       FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
