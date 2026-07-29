"""MODEL bake-off (2026-07-23): same Christ subject + same reference, across every
viable HF image model — to find the best for our retro look + character-hold.
~$2.60 total. Records to the ledger. Idempotent.
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_retro_dna/_model_bakeoff.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
OUT = Path(__file__).resolve().parent / "_model_bakeoff"
OUT.mkdir(exist_ok=True)
REF = Path(__file__).resolve().parent.parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

MODELS = ["seedream_v4_5", "seedream_v5_pro", "seedream_v5_lite", "flux_2", "flux_kontext",
          "recraft_v4_1", "gpt_image_2", "z_image", "grok_image", "text2image_soul_v2", "soul_cinematic",
          "kling_omni_image", "openai_hazel", "soul_cast"]  # final sweep

RETRO = ("Authentic vintage 1960s Silver Age comic book art printed on aged cream newsprint, bold "
         "black ink holding lines, flat limited four-colour comic colour, clearly visible coarse "
         "Ben-Day halftone dots in the sky and shadows, slight CMYK misregistration, low-fi retro print")
SUBJ = "The risen Lord Jesus Christ standing, gentle reverent face, warm side light, an ancient Near-Eastern landscape behind him"
MATCH = "Keep the SAME man as the reference image: same face, same hair, same full beard, undyed robe."
TAIL = "reverent, ancient Near-Eastern, simple undyed robe, NOT high-priestly vestments"
AVOID = "no text, no lettering, no watermark, no gore, no blazing halo, no heroic muscle, no six-pack"
PROMPT = f"{RETRO}. {SUBJ}. {TAIL}. {MATCH} AVOID: {AVOID}"


NO_REF = {"recraft_v4_1", "z_image", "soul_cast"}  # rejects media inputs — render ref-free
ASPECT = {"openai_hazel": "3:2"}  # per-model aspect overrides (hazel disallows 16:9)


def run(model, out):
    cmd = [HF, "generate", "create", model, "--prompt", PROMPT,
           "--aspect_ratio", ASPECT.get(model, "16:9"), "--wait"]
    if model not in NO_REF:
        cmd += ["--image", str(REF)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   FAIL: {blob.strip()[-150:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    ok = fail = 0
    for m in MODELS:
        out = OUT / f"{m}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {m}"); continue
        print(f"[img ] {m} ...", flush=True); t = time.time()
        if run(m, out):
            cost.record_hf("EW01_Two_Goats", "long", "stills", m, note=f"[model-bakeoff] {m}")
            print(f"   ok ({time.time()-t:.0f}s)"); ok += 1
        else:
            fail += 1
    print(f"\n[done] {ok} ok, {fail} failed -> {OUT}")


if __name__ == "__main__":
    main()
