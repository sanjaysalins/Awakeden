"""EW01 painted-comic REBUILD — Stage 2 animate (2026-07-23).

Fork of _animate_inked.py, pointed at the painted-comic stills. Tiered:
Kling 3.0 pro for multi-figure/complex (scene 18), Seedance 1.5 for the calm
single-figure tableaux. Motion-only, camera + living-light, INVENT NOTHING.
Successful clips also land in _remotion/public/pc/NN.mp4 for the Remotion slice
films. Painted-comic budget gate (EW01 rows >= 2026-07-23), separate from the
ink migration ceiling.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_animate.py --dry-run
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_animate.py --only 1,2
  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_paint_ew01_animate.py
"""
import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration

HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "v1" / "visual_16x9_painted"
CLIPS = STILLS / "clips"
PUBLIC_PC = ROOT / "_remotion" / "public" / "pc"
SLUG = "EW01_Two_Goats"

PC_START = "2026-07-23"
PC_CEILING = 18.0
TARGET_DUR = 5
KLING_SCENES = {6, 11, 13, 14, 18, 20, 21, 24}

# still slug per scene id (matches _paint_ew01_stills.py)
SLUGS = {1: "once_a_year", 2: "laid_aside_gold", 3: "plain_white_linen", 4: "went_in_alone",
         5: "cloud_mercy_seat", 16: "shadow_body_came", 17: "entered_in_once",
         18: "iniquity_of_us_all", 19: "without_the_gate"}

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image. ")
BASE = ("A still finished inked graphic-novel illustration on flat canvas, 16:9, filmed as "
        "{move}. " + FROZEN + "Only the light and the air are alive: {living}.")
PUSH = "ONE slow, steady push-in toward the centre of the frame"
WIDE = "ONE slow, gentle push-in across the scene"

MOTION = {
    1:  (WIDE, "dust motes drift in a shaft of temple light, faint incense smoke rises, robe hems stir almost imperceptibly"),
    2:  (PUSH, "a single shaft of light glints on the gold, fine dust drifts, the folded linen edge stirs faintly"),
    3:  (PUSH, "dust drifts in the corridor light, the plain linen robe stirs faintly, distant torch-glow breathes"),
    4:  (WIDE, "thin incense smoke curls upward, a shaft of light breathes brighter and dimmer, dust motes drift slowly"),
    5:  (WIDE, "the cloud of glory above the mercy seat glows and breathes gently, fine golden motes drift, the surrounding shadow deepens"),
    16: (WIDE, "warm light breathes gently across the scene, heat-haze and fine dust drift, the cross-shadow holds perfectly still"),
    17: (PUSH, "the radiant light at the torn veil glows and breathes gently, fine motes drift, Christ's robe and hair stir almost imperceptibly"),
    18: (PUSH, "the cross of soft light above Christ glows and breathes, fine golden motes drift -- both goats and every figure hold perfectly still"),
    19: (WIDE, "warm evening haze drifts over the skyline, the golden radiance around Christ breathes gently, fine dust drifts, his robe stirs faintly"),
}


def model_for(sid): return "kling3_0" if sid in KLING_SCENES else "seedance1_5"


def params_for(model):
    p = {"duration": _hf_duration(model, TARGET_DUR), "aspect_ratio": "16:9"}
    if model == "kling3_0":
        p["mode"] = "pro"; p["sound"] = "off"
    return p


def pc_spend():
    return round(sum(cost._usd(r.get("est_usd")) for r in cost.load()
                     if r.get("episode") == SLUG and r.get("ts", "") >= PC_START), 2)


def animate_one(png, out, model, prompt, params):
    cmd = [HF, "generate", "create", model, "--start-image", str(png), "--prompt", prompt]
    for k, v in params.items():
        cmd += [f"--{k}", str(v)]
    cmd += ["--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("       NSFW-REJECTED"); return False
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"       no mp4 url: {blob.strip()[-200:]}"); return False
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    return out.exists() and out.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--override", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()} if a.only else None
    ids = sorted(i for i in SLUGS if only is None or i in only)
    CLIPS.mkdir(parents=True, exist_ok=True); PUBLIC_PC.mkdir(parents=True, exist_ok=True)

    print(f"[budget] painted-comic spent so far: ${pc_spend():.2f} / ${PC_CEILING:.0f}")
    batch = 0.0
    for sid in ids:
        model = model_for(sid); est = cost.hf_estimate(model, params=params_for(model)) * cost.CREDITS_TO_USD
        batch += est
        print(f"   #{sid:02d} {model:<12} {params_for(model)['duration']}s ~${est:.2f}  {SLUGS[sid]}")
    print(f"[plan] batch ~${batch:.2f} -> projected painted-comic ~${pc_spend()+batch:.2f}")
    if a.dry_run:
        return

    ok = fail = skip = 0
    for sid in ids:
        name = f"{sid:02d}_{SLUGS[sid]}"
        png = STILLS / f"{name}.png"
        out = CLIPS / f"{name}.mp4"
        pub = PUBLIC_PC / f"{sid:02d}.mp4"
        if out.exists() and out.stat().st_size > 0 and not a.force:
            shutil.copyfile(out, pub); print(f"[skip] {out.name} (exists, copied to public/pc)"); skip += 1; continue
        if not png.exists():
            print(f"[FAIL] #{sid:02d}: missing still {png.name}"); fail += 1; continue
        model = model_for(sid); params = params_for(model)
        est = cost.hf_estimate(model, params=params) * cost.CREDITS_TO_USD
        proj = pc_spend() + est
        if proj > PC_CEILING and not a.override:
            print(f"[STOP] #{sid:02d} would push painted-comic to ~${proj:.2f} > ${PC_CEILING:.0f}. --override to proceed."); fail += 1; break
        move, living = MOTION[sid]
        prompt = BASE.format(move=move, living=living)
        print(f"[clip] #{sid:02d} {model} {params['duration']}s ~${est:.2f} -> {out.name} ...", flush=True)
        t = time.time()
        if animate_one(png, out, model, prompt, params):
            cost.record_hf(SLUG, "long", "animate", model, note=f"[painted-comic] #{sid:02d} {SLUGS[sid]}", params=params)
            shutil.copyfile(out, pub)
            print(f"       ok ({time.time()-t:.0f}s) -> public/pc/{pub.name}"); ok += 1
        else:
            print("       FAILED"); fail += 1
    print(f"\n[done] animated {ok}, skipped {skip}, failed {fail}")
    print(f"[budget] painted-comic total now ~${pc_spend():.2f} / ${PC_CEILING:.0f}")


if __name__ == "__main__":
    main()
