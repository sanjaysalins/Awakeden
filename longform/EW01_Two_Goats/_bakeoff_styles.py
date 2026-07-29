"""Style BAKE-OFF (2026-07-23): INKED graphic-novel vs PAINTED-comic, same 3 subjects.
Helps the user decide which look to standardise on.
  Subjects: Jesus (as himself) · Jesus on the cross · Noah + ark + rainbow + animals
  Styles:   inked (seedream_v4_5, graphic_novel recipe) · painted (nano_banana_pro, painted-comic recipe)
6 stills, ~2cr each (~$1.80). Records to the ledger. Idempotent (skip if exists).

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_bakeoff_styles.py
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_bakeoff_styles.py --only jesus,cross
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
OUT = Path(__file__).resolve().parent / "_style_bakeoff"
OUT.mkdir(parents=True, exist_ok=True)
SKILL_REF = ROOT / ".claude" / "skills" / "painted-comic" / "references"
CHRIST = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked" / "_painted_comic_test" / "christ_pc_ref.png"
NOAH = SKILL_REF / "noah_ref.png"
ARK = SKILL_REF / "ark_ref.png"

# ---- inked (graphic_novel) recipe, from config ----
GN_BASE = config.VISUAL_STYLE_BASE_GN
GN_TAIL = config.VISUAL_STYLE_TAIL_GN.replace(" --ar 9:16", "").strip()

# ---- painted-comic recipe ----
PC_DARK = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
           "dry-brush texture over rich muted earth-tone painting, dramatic single strong key light "
           "with deep chiaroscuro shadow, a premium comic-cover finish. Non-photoreal, not smooth "
           "airbrushed, not a 3D render, no halftone dots, no vintage newsprint.")
PC_BRIGHT = ("Bold inked biblical graphic-novel illustration: heavy confident black ink linework and "
             "dry-brush texture over rich luminous earth-tone painting, a warm radiant bright key light "
             "with soft lifted shadows and a bright airy exposure, glowing golden highlights, a premium "
             "comic-cover finish. Non-photoreal, not smooth airbrushed, not a 3D render, no halftone dots.")
PC_AVOID = ("AVOID: no text, letters, numbers or captions anywhere; no speech balloons; no card, plate, "
            "banner, title-box, blank rectangle, gutter line or panel border of any kind; no logo or "
            "watermark; no photoreal live-action; no smooth 3D render; no halftone dots; no modern items; "
            "no gore. The illustration bleeds fully to all four edges: no drawn border or frame.")

# subject_block, painted light, painted refs
SUBJECTS = {
    "jesus": ("The risen Lord Jesus Christ standing in a simple undyed white robe, gentle reverent "
              "face, warm holy light behind him, ancient Near-Eastern setting", "bright", [CHRIST]),
    "cross": ("Jesus Christ upon the cross at Golgotha seen reverently, head bowed, a simple plain "
              "cloth at his waist, a dark brooding sky behind, distant hills; solemn and holy; no "
              "blood, no gore", "dark", [CHRIST]),
    "noah": ("Noah, an aged patriarch with a long grey beard and undyed robe, standing before the "
             "great rectangular flat-bottomed wooden box-ark (no mast, no sail, straight vertical "
             "ends, one door, one long window band), pairs of animals boarding two by two, a bright "
             "many-coloured rainbow arching across the sky above the ark", "bright", [NOAH, ARK]),
}


def run(model, prompt, refs, out: Path, extra=None) -> bool:
    cmd = [HF, "generate", "create", model, "--prompt", prompt, "--aspect_ratio", "16:9", "--wait"]
    if extra:
        cmd += extra
    for r in refs:
        if r and Path(r).exists():
            cmd += ["--image", str(r)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (p.stdout or "") + "\n" + (p.stderr or "")
    urls = re.findall(r'https?://\S+?\.(?:png|jpg|jpeg|webp)', blob) or re.findall(r'https?://\S+', blob)
    if not urls:
        print(f"       no url: {blob.strip()[-160:]}")
        return False
    subprocess.run(["curl", "-s", "-L", urls[-1], "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()} if a.only else None
    keys = [k for k in SUBJECTS if only is None or k in only]

    ok = fail = skip = 0
    for k in keys:
        subj, light, refs = SUBJECTS[k]
        jobs = [
            ("inked",   "seedream_v4_5",   f"{GN_BASE} {subj}. reverent, sacred. {GN_TAIL}", [], None),
            ("painted", "nano_banana_pro", f"{(PC_BRIGHT if light=='bright' else PC_DARK)} Compose this frame: {subj}. {PC_AVOID}", refs, ["--resolution", "2k"]),
        ]
        for style, model, prompt, r, extra in jobs:
            out = OUT / f"{k}_{style}.png"
            if out.exists() and out.stat().st_size > 1000 and not a.force:
                print(f"[skip] {out.name}"); skip += 1; continue
            print(f"[img ] {k:6} {style:8} ({model}) ...", flush=True)
            t = time.time()
            if run(model, prompt, r, out, extra):
                cost.record_hf("EW01_Two_Goats", "long", "stills", model, note=f"[style-bakeoff] {k}/{style}")
                print(f"       ok ({time.time()-t:.0f}s) -> {out.name}"); ok += 1
            else:
                print("       FAILED"); fail += 1
    print(f"\n[done] rendered {ok}, skipped {skip}, failed {fail} -> {OUT}")


if __name__ == "__main__":
    main()
