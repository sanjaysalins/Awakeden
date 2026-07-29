"""Ink-family style BAKE-OFF (2026-07-23): 6 distinct ink looks, ONE subject (Jesus),
so the only variable is the ink style. Model held constant (seedream_v4_5) for fairness.
~2cr each (~$1.80). Idempotent.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_bakeoff_ink_variants.py
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_bakeoff_ink_variants.py --only woodcut,noir_spot
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HF = str(config.HF_CLI_PATH)
MODEL = "seedream_v4_5"
OUT = Path(__file__).resolve().parent / "_ink_bakeoff"
OUT.mkdir(parents=True, exist_ok=True)

SUBJECT = ("The risen Lord Jesus Christ standing in a simple undyed robe, gentle reverent face, "
           "warm holy light behind him, ancient Near-Eastern setting")
TAIL = "reverent holy atmosphere, ancient Near-Eastern period-accurate, no text, no lettering, no panels, no speech bubbles, no watermark"

# name, label, ink-style prefix
STYLES = [
    ("clean_comic", "Clean comic (baseline)",
     "Bold clean black ink linework and outlines, flat cel-shaded comic colour, hand-drawn 2D graphic-novel art, dramatic ink shadows"),
    ("ligne_claire", "Ligne claire (clean-line)",
     "Ligne claire clean-line comic art, uniform thin black outlines, flat bright even colour, minimal shading, crisp hand-drawn 2D"),
    ("comic_halftone", "Retro comic + halftone dots",
     "Vintage American comic-book art, bold black ink outlines, Ben-Day halftone dot shading, saturated retro four-colour print look"),
    ("woodcut", "Woodcut / engraving",
     "Antique woodcut engraving illustration, dense black cross-hatching and etched linework, high-contrast monochrome ink, classic Bible engraving"),
    ("noir_spot", "Noir B&W + spot red",
     "Sin City high-contrast black and white ink, stark pure black shadows and bright white, a single spot of deep red colour, dramatic noir graphic novel"),
    ("heavy_black", "Heavy-black brush (Mignola)",
     "Bold heavy black-shape ink art, massive solid black areas, thick expressive brush ink, moody minimal detail, dramatic graphic-novel style"),
    ("colour_woodcut", "Colour woodcut / lino-print",
     "Colour woodcut linocut block-print illustration, bold carved black shapes and thick outlines, limited flat printed colour, hand-pressed relief-print texture"),
    ("ink_watercolour", "Ink + watercolour wash",
     "Bold black ink linework with loose translucent watercolour washes, wet-on-wet colour bleeds, expressive hand-painted look, airy negative space"),
    ("duotone", "Duotone (black + crimson)",
     "Two-colour duotone ink illustration, pure black and deep crimson red only on a cream ground, bold graphic limited palette, high contrast"),
    ("sumi_e", "Sumi-e brush",
     "Loose sumi-e East-Asian brush-ink painting, expressive gestural black brushstrokes, generous empty negative space, minimal, elegant, wet ink"),
    ("scratchboard", "Scratchboard (white-on-black)",
     "Scratchboard scraperboard art, fine white lines scratched out of solid black, glowing white highlights on deep black, dramatic engraved negative image"),
    ("illuminated", "Illuminated + gold",
     "Medieval illuminated-manuscript ink illustration, fine black pen linework with burnished gold-leaf accents and rich jewel-tone inks, sacred and ornamental"),
]


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=""); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()} if a.only else None
    ok = fail = skip = 0
    for name, label, prefix in STYLES:
        if only and name not in only:
            continue
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000 and not a.force:
            print(f"[skip] {out.name}"); skip += 1; continue
        prompt = f"{prefix}. {SUBJECT}. {TAIL}"
        print(f"[img ] {name:16} ...", flush=True)
        t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[ink-bakeoff] {name}")
            print(f"       ok ({time.time()-t:.0f}s)"); ok += 1
        else:
            print("       FAILED"); fail += 1
    print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail} -> {OUT}")


if __name__ == "__main__":
    main()
