"""Camera-motion variety test (2026-07-24): re-render 2 already-animated stills
with genuinely different, SAFE camera directions (from this project's own
proven-safe camera_palette_green vocabulary: dolly_in/pull_back/tracking, never
orbit/360/pov/top_down/worms_eye) instead of the uniform push-in every clip in
the POC used so far. Direct before/after: same still, same frozen-tableau
discipline, only the {move} differs.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_camera_variety.py
"""
import re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "clips" / "_camera_variety"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image. ")
BASE = ("A still finished inked graphic-novel illustration on flat canvas, 9:16, filmed as "
        "{move}. " + FROZEN + "Only the light and the air are alive: {living}.")

PULL_BACK = "ONE slow, steady pull-back away from the centre of the frame, revealing more of the scene"
TRACKING = "ONE slow lateral tracking movement, the camera gliding gently sideways across the frame"

JOBS = [
    # (still_id, model, move, move_name, living, KLING_SCENES_orig)
    (5, "kling3_0", PULL_BACK, "pullback",
     "storm light breathes faintly behind the crosses, dust drifts"),
    (6, "seedance1_5", TRACKING, "tracking",
     "storm clouds part slowly with a soft breathing light behind him, dust drifts"),
]


def params_for(model: str) -> dict:
    dur = _hf_duration(model, 5)
    p = {"duration": dur, "aspect_ratio": "9:16"}
    if model == "kling3_0":
        p["mode"] = "pro"
        p["sound"] = "off"
    return p


def animate_one(png: Path, out: Path, model: str, prompt: str, params: dict) -> bool:
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
    for sid, model, move, move_name, living in JOBS:
        png = STILLS / f"{sid:02d}.png"
        out = OUT / f"{sid:02d}_{move_name}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"[skip] {out.name}"); continue
        params = params_for(model)
        prompt = BASE.format(move=move, living=living)
        print(f"[clip] #{sid:02d} {model} {move_name} {params['duration']}s -> {out.name} ...", flush=True)
        t = time.time()
        if animate_one(png, out, model, prompt, params):
            cost.record_hf("EW_Thief_POC", "short", "animate", model, note=f"[camera-variety] #{sid:02d} {move_name}", params=params)
            print(f"       ok ({time.time()-t:.0f}s)")
        else:
            print("       FAILED")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
