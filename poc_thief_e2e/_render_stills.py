"""Render the 8 painted-comic stills for the Penitent Thief E2E POC.
Reuses the exact validated full-colour recipe from
longform/EW01_Two_Goats/_retro_dna/_painted_comic_*.py (same STYLE/AVOID/MATCH),
9:16 aspect for a vertical short. Chains christ_pc_ref.png on every scene where
Christ appears (per the doctrine-gate finding: robed reads reliably ~75% of
the time on the crucifixion -- eye-check every Christ-on-cross scene here).

  .venv\\Scripts\\python.exe poc_thief_e2e/_render_stills.py
"""
import json, re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
HF = str(config.HF_CLI_PATH)
MODEL = "nano_banana_pro"
HERE = Path(__file__).resolve().parent
OUT = HERE / "stills"
OUT.mkdir(exist_ok=True)
CHRIST_REF = ROOT / "longform" / "EW01_Two_Goats" / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"

STYLE = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
         "dry-brush texture over rich painting, dramatic single strong key light with deep "
         "chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth airbrushed, "
         "not a 3D render, no halftone dots, no vintage newsprint.")
AVOID_FULL_COLOR = (
    "AVOID: no text, letters, numbers, digits, panel numbers, chapter numbers or captions "
    "anywhere in the frame, including carved into rock, wood, corners or borders; no speech "
    "balloons; no card, plate, tab, ribbon, banner, title-box, blank rectangle, empty caption "
    "box, page margin, gutter line or panel border of any kind (all text and framing are drawn "
    "separately later); no logo or watermark; no photoreal live-action; no smooth 3D render; no "
    "halftone dots; no modern machinery, clothing or tools; no gore. Render in full rich natural "
    "colour throughout, painterly and reverent, not flat or garish, not a comic-book primary-colour "
    "look, no Ben-Day dots, no CMYK misregistration."
)
MATCH = "Match the inked chiaroscuro rendering of the reference image(s)."

plan = json.loads((HERE / "scene_plan.json").read_text(encoding="utf-8"))


def run(prompt, out, refs):
    cmd = [HF, "generate", "create", MODEL, "--prompt", prompt, "--aspect_ratio", "9:16",
           "--resolution", "2k", "--wait"]
    for r in refs:
        cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return False
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"   no url: {blob.strip()[-300:]}"); return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    ok = fail = 0
    for s in plan["scenes"]:
        out = OUT / f"{s['id']:02d}.png"
        if out.exists() and out.stat().st_size > 1000:
            print(f"[skip] {out.name}"); continue
        refs = [CHRIST_REF] if "christ" in s.get("refs", []) else []
        prompt = f"{STYLE} Compose this frame: {s['subject_block']}. {AVOID_FULL_COLOR}"
        if refs:
            prompt += " " + MATCH
        print(f"[img ] {s['id']:02d} {s['title'][:40]} ({'christ' if refs else 'plate'}) ...", flush=True)
        t = time.time()
        if run(prompt, out, refs):
            cost.record_hf("EW_Thief_POC", "short", "stills", MODEL, note=f"#{s['id']:02d} {s['title'][:30]}")
            print(f"   ok ({time.time()-t:.0f}s)")
            ok += 1
        else:
            print("   FAILED")
            fail += 1
    print(f"\n[done] rendered {ok}, failed {fail} -> {OUT}")


if __name__ == "__main__":
    main()
