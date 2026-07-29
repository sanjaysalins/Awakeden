"""Test: seedream_v4_5 (the richer 'B' look) + a chained Christ reference (--image)
to hold the same man. 2 frames, ~$0.60. If seedream accepts --image AND keeps the
face, we get the good look + consistency. Same ref + milder-retro prompt that made
the liked jesus_finished.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_seedream_ref.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "seedream_v4_5"
OUT = Path(__file__).resolve().parent / "_seedream_ref"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

# the milder-retro prompt that produced the liked 'B' jesus_finished
# FIXED 2026-07-23: "printed on aged cream newsprint" + "low-fi retro print texture" made
# nano_banana_pro render a physical PAGE (black border + cream margin) instead of just the
# style — confirmed reproducible on 2 other renders using this same base. Positive full-bleed
# phrasing instead ([[seedream-no-negative-channel]]: describe the end-state, don't name the
# drawable object even to forbid it).
RETRO = ("Vintage 1960s Silver Age comic book illustration style, bold black ink holding lines, "
         "flat limited four-colour comic colour with NO gradients, clearly visible coarse Ben-Day "
         "halftone dots in the sky and shadows, slight CMYK misregistration, warm cream colour palette")
MATCH = "Keep the SAME man as the reference image: same face, same hair, same full beard, undyed robe."
TAIL = ("reverent, ancient Near-Eastern period-accurate, a simple undyed robe, NOT high-priestly "
        "vestments, a full-bleed digital illustration filling the entire canvas edge-to-edge")
AVOID = ("no text, no lettering, no captions, no speech balloons, no watermark, no "
         "gore, no blazing halo, no heroic muscle, no six-pack, no athletic bodybuilder build, no bright droplet blood")

JOBS = {
    "sr_hero": "The risen Lord Jesus Christ standing, gentle reverent face, warm side light, an ancient Near-Eastern landscape behind him",
    "sr_welcome": "The risen Christ in a stone doorway, one hand extended in welcome toward the viewer, warm light through the doorway, calm and reverent",
    "sr_teaching": "The Lord Jesus Christ standing and teaching a small gathered crowd on a grassy hillside by the sea, a gentle open-handed gesture, warm afternoon daylight, ancient Near-Eastern",
    "sr_cross": ("Jesus Christ crucified on a wooden cross, a GAUNT thin marred exhausted body with NO heroic "
                 "muscle and no defined abs (Isaiah 53, no beauty that we should desire him), head bowed low in "
                 "sorrow, only faint matted blood, a dark brooding storm sky, deeply reverent and sorrowful"),
}


def run(prompt, out, use_ref=True):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
    if use_ref:
        cmd += ["--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url (may not accept --image): {blob.strip()[-200:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for name, subj in JOBS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        prompt = f"{RETRO}. {subj}. {TAIL}. {MATCH} AVOID: {AVOID}"
        print(f"[img ] {name} (seedream + ref) ...", flush=True); t = time.time()
        if run(prompt, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[seedream-ref] {name}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
