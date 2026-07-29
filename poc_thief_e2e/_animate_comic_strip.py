"""Animate the 2 native comic-strip pages (2026-07-24) as ONE clip each: a
slow vertical pan/scroll from the top panel down through to the bottom panel,
frozen-tableau discipline (no invented motion, nothing animates except light/
air) -- testing whether a real multi-panel PAGE reads well as a single
"page-scroll reveal" shot instead of per-panel crop-and-animate.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_comic_strip.py
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
STILLS = HERE / "stills" / "_comic_strip_native"
OUT = HERE / "clips" / "_comic_strip_native"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image, including the "
          "panel borders and gutters, which stay exactly where they are drawn. ")
SCROLL = ("A finished comic-strip page with three panels stacked vertically, filmed as ONE "
          "slow, steady vertical pan scrolling downward from the top panel to the bottom panel, "
          "revealing each panel in turn as the page moves. ")
BASE = SCROLL + FROZEN + "Only the light and the air are alive: {living}."

JOBS = [
    ("strip1_rebuke_noref", "storm clouds drift and breathe faintly behind the crosses, dust motes catch the light"),
    ("strip2_promise_ref", "the storm light breathes gently, faint dust drifts in the air"),
]


def params_for() -> dict:
    dur = _hf_duration("kling3_0", 5)
    return {"duration": dur, "aspect_ratio": "9:16", "mode": "pro", "sound": "off"}


def animate_one(png: Path, out: Path, prompt: str, params: dict) -> bool:
    cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png), "--prompt", prompt]
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
    for name, living in JOBS:
        png = STILLS / f"{name}.png"
        out = OUT / f"{name}.mp4"
        params = params_for()
        prompt = BASE.format(living=living)
        print(f"[clip] {name} kling3_0 {params['duration']}s -> {out.name} ...", flush=True)
        t = time.time()
        if animate_one(png, out, prompt, params):
            cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[comic-strip-scroll] {name}", params=params)
            print(f"       ok ({time.time()-t:.0f}s)")
        else:
            print("       FAILED")
    print(f"\n[done] -> {OUT}")


if __name__ == "__main__":
    main()
