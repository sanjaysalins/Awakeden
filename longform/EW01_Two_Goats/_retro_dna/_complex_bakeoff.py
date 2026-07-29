"""COMPLEX bake-off (2026-07-23): grok_image vs seedream_v4_5 on hard multi-figure
scenes (crowds / action / crucifixion) — the frames where models really separate.
Christ ref chained on Christ scenes. 3 subjects x 2 models = 6 images, ~$0.90.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_complex_bakeoff.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
OUT = Path(__file__).resolve().parent / "_complex_bakeoff"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

MODELS = ["grok_image", "seedream_v4_5"]
RETRO = ("Authentic vintage 1960s Silver Age comic book art printed on aged cream newsprint, bold "
         "black ink holding lines, flat limited four-colour comic colour, clearly visible coarse "
         "Ben-Day halftone dots in the sky and shadows, slight CMYK misregistration, low-fi retro print")
MATCH = "Keep the SAME Christ as the reference image: same face, same hair, same full beard, undyed robe."
TAIL = "reverent, ancient Near-Eastern period-accurate"
AVOID = "no text, no lettering, no watermark, no gore, no blazing halo, no heroic muscle, no six-pack"

# name -> (subject, use_christ_ref)
SUBJECTS = {
    "atonement_crowd": ("The high priest Aaron in white linen at the bronze altar with two goats before him, "
                        "a great crowd of Israelites gathered around, the curtained desert Tabernacle tent "
                        "behind at dawn", False),
    "crucifixion_crowd": ("Jesus Christ crucified on a wooden cross, a gaunt marred body (Isaiah 53, no heroic "
                          "muscle), head bowed in sorrow, Roman soldiers and grieving women gathered below at "
                          "the foot of the cross, a dark brooding storm sky over the hill, faint blood only", True),
    "teaching_crowd": ("Jesus Christ standing and teaching a large crowd of seated people on a grassy hillside "
                       "above the sea of Galilee, many figures, a gentle gesture, warm afternoon light", True),
}


def run(model, subj, use_ref, out):
    match = f" {MATCH}" if use_ref else ""
    prompt = f"{RETRO}. {subj}. {TAIL}.{match} AVOID: {AVOID}"
    cmd = [HF, "generate", "create", model, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
    if use_ref:
        cmd += ["--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   FAIL: {blob.strip()[-140:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    ok = fail = 0
    for sname, (subj, use_ref) in SUBJECTS.items():
        for m in MODELS:
            out = OUT / f"{sname}__{m}.png"
            if out.exists() and out.stat().st_size > 1000:
                print(f"[skip] {out.name}"); continue
            print(f"[img ] {sname} / {m} ...", flush=True); t = time.time()
            if run(m, subj, use_ref, out):
                cost.record_hf("EW01_Two_Goats", "long", "stills", m, note=f"[complex-bakeoff] {sname}/{m}")
                print(f"   ok ({time.time()-t:.0f}s)"); ok += 1
            else:
                fail += 1
    print(f"\n[done] {ok} ok, {fail} failed -> {OUT}")


if __name__ == "__main__":
    main()
