"""Static-page animation, round 2 (2026-07-24): fix the round-1 finding on
strip2 -- a tear appeared on Christ's face, a real invented facial change
despite "no faces change" in the prompt. Reinforced wording (describe what
MUST stay identical, generalize "no new marks or liquid" rather than naming
the specific unwanted detail) + test on BOTH strips this time.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_page_static_v2.py
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

FROZEN_V2 = (
    "Every figure in every panel stays perfectly frozen the entire time -- no limbs move, no "
    "heads turn, no faces change, no expressions change, no skin changes, no new marks or "
    "liquid appear anywhere on any body or face, and no new figures, hands or objects appear. "
    "INVENT NOTHING AT ALL on any face or body -- every face stays pixel-for-pixel identical to "
    "this exact image throughout, in every panel, the whole time. "
)
STATIC = ("A finished comic-strip page with three panels stacked vertically, filmed with the "
          "camera held completely still -- the whole page and every panel border stay perfectly "
          "fixed in frame the entire time, no camera movement, no zoom, no pan, no scroll. ")
BASE = STATIC + FROZEN_V2 + "Only the light and the air are alive, and each panel breathes independently and differently from the others: {living}."

JOBS = [
    ("strip1_static_page",
     "in the TOP panel, storm clouds drift faintly behind the figure; in the MIDDLE panel, dust "
     "motes drift faintly in the harsh sunlight; in the BOTTOM panel, the storm clouds shift and "
     "breathe softly, faint heat-haze shimmers over the distant cross."),
    ("strip2_static_page_v2",
     "in the TOP panel, storm clouds drift faintly behind the figure; in the MIDDLE panel, the "
     "dark background breathes gently with faint shifting shadow; in the BOTTOM panel, the "
     "golden light rays shift and glow softly, brighter and dimmer."),
]
SRC = {"strip1_static_page": "strip1_rebuke_noref.png", "strip2_static_page_v2": "strip2_promise_ref.png"}


def main():
    dur = _hf_duration("kling3_0", 5)
    for name, living in JOBS:
        png = STILLS / SRC[name]
        out = OUT / f"{name}.mp4"
        prompt = BASE.format(living=living)
        cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(png), "--prompt", prompt,
               "--duration", str(dur), "--aspect_ratio", "9:16", "--mode", "pro", "--sound", "off", "--wait"]
        print(f"[clip] {name} kling3_0 {dur}s -> {out.name} ...", flush=True)
        t = time.time()
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        blob = (r.stdout or "") + "\n" + (r.stderr or "")
        if re.search(r"nsfw", blob, re.IGNORECASE):
            print("   NSFW-REJECTED"); continue
        m = re.search(r'https?://\S+?\.mp4', blob)
        if not m:
            print(f"   no mp4 url: {blob.strip()[-300:]}"); continue
        subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
        if out.exists() and out.stat().st_size > 0:
            cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[static-page-v2] {name}", params={"duration": dur})
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")


if __name__ == "__main__":
    main()
