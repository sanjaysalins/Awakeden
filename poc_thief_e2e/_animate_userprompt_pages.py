"""Animate Page 1 and Page 3 of the user-prompt comic strip sequence (2026-07-24)
using the proven static-page technique: camera completely fixed, all 4 panels
visible the whole time, each panel independently alive with its own
atmospheric motion. Reuses the reinforced no-invention wording that fixed the
earlier "invented tear" finding.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_userprompt_pages.py
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
STILLS = HERE / "stills" / "_comic_strip_userprompt"
OUT = HERE / "clips" / "_comic_strip_userprompt"
OUT.mkdir(parents=True, exist_ok=True)

FROZEN_V2 = (
    "Every figure in every panel stays perfectly frozen the entire time -- no limbs move, no "
    "heads turn, no faces change, no expressions change, no skin changes, no new marks or "
    "liquid appear anywhere on any body or face, and no new figures, hands or objects appear. "
    "INVENT NOTHING AT ALL on any face or body -- every face stays pixel-for-pixel identical to "
    "this exact image throughout, in every panel, the whole time. All caption text stays "
    "exactly as drawn, unchanged. "
)
STATIC = ("A finished comic-strip page with four panels, filmed with the camera held "
          "completely still -- the whole page and every panel border and caption box stay "
          "perfectly fixed in frame the entire time, no camera movement, no zoom, no pan, no "
          "scroll. ")
BASE = STATIC + FROZEN_V2 + "Only the light and the air are alive, and each panel breathes independently and differently from the others: {living}."

JOBS = [
    ("page1_static",
     "in the TOP panel, lightning flashes and storm clouds churn slowly behind the three "
     "crosses; in the UPPER-MIDDLE panel, dust drifts faintly in the harsh light; in the "
     "LOWER-MIDDLE panel, the storm light shifts softly; in the BOTTOM panel, the light dims "
     "and brightens gently on his face."),
    ("page3_static",
     "in the TOP panel, lightning flashes behind him and storm clouds churn slowly; in the "
     "UPPER-MIDDLE panel, the warm light highlights shift softly; in the LOWER-MIDDLE panel, "
     "the warm glow between them breathes gently, brighter and dimmer; in the BOTTOM panel, "
     "the fading light dims further and the clouds drift slowly."),
]
SRC = {"page1_static": "page1.png", "page3_static": "page3.png"}


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
            cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[userprompt-static] {name}", params={"duration": dur})
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
