"""Animate the 8 Penitent Thief POC stills. Reuses the exact validated
frozen-tableau + camera-move-only prompt pattern from
longform/EW01_Two_Goats/_animate_inked.py (BASE/FROZEN/MOTION), tiered
Kling (multi-figure/complex) vs Seedance (calm single-figure), 9:16, 5s clips.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate.py
"""
import json, re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost
from pipeline.video_render import _hf_duration
HF = str(config.HF_CLI_PATH)
HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
CLIPS = HERE / "clips"
CLIPS.mkdir(exist_ok=True)

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image. ")
BASE = ("A still finished inked graphic-novel illustration on flat canvas, 9:16, filmed as "
        "{move}. " + FROZEN + "Only the light and the air are alive: {living}.")
PUSH = "ONE slow, steady push-in toward the centre of the frame"
WIDE = "ONE slow, gentle push-in across the scene"

KLING_SCENES = {1, 3, 5}
TARGET_DUR = 5

MOTION = {
    1: (WIDE, "dust drifts across the desolate hill, storm clouds shift slowly overhead, the shaft of light breathes gently"),
    2: (PUSH, "dust drifts in the harsh sunlight, distant heat-haze shimmers faintly"),
    3: (WIDE, "dust drifts between the two crosses, harsh light breathes faintly, the distant hazy cross holds still"),
    4: (PUSH, "shadow and light breathe faintly in the dim space, dust drifts"),
    5: (PUSH, "storm light breathes faintly behind the crosses, dust drifts"),
    6: (PUSH, "storm clouds part slowly with a soft breathing light behind him, dust drifts"),
    7: (PUSH, "the soft light behind him breathes gently brighter, dust drifts faintly"),
    8: (WIDE, "the golden light breathes and glows gently around him, dust motes drift in the radiant beam"),
}


def model_for(sid: int) -> str:
    return "kling3_0" if sid in KLING_SCENES else "seedance1_5"


def params_for(model: str) -> dict:
    dur = _hf_duration(model, TARGET_DUR)
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
    plan = json.loads((HERE / "scene_plan.json").read_text(encoding="utf-8"))
    ok = fail = 0
    for s in plan["scenes"]:
        sid = s["id"]
        png = STILLS / f"{sid:02d}.png"
        out = CLIPS / f"{sid:02d}.mp4"
        if out.exists() and out.stat().st_size > 0:
            print(f"[skip] {out.name}"); continue
        if not png.exists():
            print(f"[FAIL] #{sid:02d}: missing still"); fail += 1; continue
        model = model_for(sid)
        params = params_for(model)
        move, living = MOTION[sid]
        prompt = BASE.format(move=move, living=living)
        print(f"[clip] #{sid:02d} {model} {params['duration']}s -> {out.name} ...", flush=True)
        t = time.time()
        if animate_one(png, out, model, prompt, params):
            cost.record_hf("EW_Thief_POC", "short", "animate", model, note=f"#{sid:02d}", params=params)
            print(f"       ok ({time.time()-t:.0f}s)")
            ok += 1
        else:
            print("       FAILED")
            fail += 1
    print(f"\n[done] animated {ok}, failed {fail} -> {CLIPS}")


if __name__ == "__main__":
    main()
