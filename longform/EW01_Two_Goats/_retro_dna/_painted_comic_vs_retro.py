"""Same-scene bake-off (2026-07-24): render scenes 1 and 5 in the PAINTED-COMIC
style (verbatim recipe from _painted_comic_test.py, 2026-07-22 — ink+dry-brush+
chiaroscuro, no halftone dots) using the EXACT same subject_block content
already rendered in retro-comic (v1/visual_16x9_retro/), so the user gets a
true apples-to-apples same-content comparison between the two style families.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_painted_comic_vs_retro.py
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
OUT = HERE / "_painted_comic_vs_retro"
OUT.mkdir(exist_ok=True)
PCT = HERE.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test"
AARON_REF = PCT / "aaron_pc_ref.png"

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
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

plan = json.loads((HERE.parent / "v1" / "visual_16x9_inked" / "scene_plan.json").read_text(encoding="utf-8"))
scenes = {s["id"]: s for s in plan["scenes"]}

JOBS = {
    1: ("pc_vs_retro_01_once_a_year", [AARON_REF]),
    5: ("pc_vs_retro_05_mercy_seat", [AARON_REF]),
}


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "16:9",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-200:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    for sid, (name, refs) in JOBS.items():
        out = OUT / f"{name}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        shot = scenes[sid]["subject_block"]
        prompt = f"{STYLE} Compose this frame: {shot} {AVOID} {MATCH}"
        print(f"[img ] scene {sid} (painted-comic + aaron ref) ...", flush=True); t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW01_Two_Goats", "long", "stills", MODEL, note=f"[pc-vs-retro] scene {sid}")
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"[out] {OUT}")


if __name__ == "__main__":
    main()
