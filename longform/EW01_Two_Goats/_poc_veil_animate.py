"""POC step 2 of 3: animate the painted-comic veil plate into a LIVING plate.

Kling 3.0 pro, frozen tableau (Christ + veil locked), camera-only push + living
light in the torn-veil shaft. ~$0.50 (7.5cr). Records to the spend ledger.
Reuses the exact FROZEN/BASE pattern from _animate_inked.py.

  .venv\\Scripts\\python.exe longform/EW01_Two_Goats/_poc_veil_animate.py
"""
import re
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
DIR = Path(__file__).resolve().parent / "v1" / "visual_16x9_inked" / "_poc_kinetic_type"
PNG = DIR / "pc_20_veil_plate.png"
OUT = DIR / "pc_20_veil_clip.mp4"

FROZEN = ("Every figure stays perfectly frozen the entire time -- no limbs move, no heads "
          "turn, no faces change, no morphing, and no new figures, hands or objects appear. "
          "INVENT NOTHING: show only what is already drawn in this exact image. ")
BASE = ("A still finished inked graphic-novel illustration on flat canvas, 16:9, filmed as "
        "{move}. " + FROZEN + "Only the light and the air are alive: {living}.")
MOVE = "ONE slow, steady push-in toward the centre of the frame"
LIVING = ("the shaft of pale light through the torn veil breathes gently brighter and dimmer, "
          "fine dust motes drift, the seated Christ's warm golden radiance glows softly -- the "
          "seated Christ stays perfectly still, his head, face, eyes, gaze and hands never move")


def main():
    if not PNG.exists():
        print(f"missing plate: {PNG}"); sys.exit(1)
    dur = _hf_duration("kling3_0", 5)
    prompt = BASE.format(move=MOVE, living=LIVING)
    cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(PNG), "--prompt", prompt,
           "--duration", str(dur), "--aspect_ratio", "16:9", "--mode", "pro", "--sound", "off", "--wait"]
    print(f"[POC clip] kling3_0 pro {dur}s -> {OUT.name} ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("  NSFW-REJECTED"); sys.exit(2)
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"  no mp4 url:\n{blob.strip()[-400:]}"); sys.exit(1)
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(OUT)], check=True)
    if OUT.exists() and OUT.stat().st_size > 0:
        cost.record_hf("EW01_Two_Goats", "long", "animate", "kling3_0",
                       note="[POC kinetic-type] pc_20_veil_clip",
                       params={"duration": dur, "aspect_ratio": "16:9", "mode": "pro", "sound": "off"})
        print(f"  ok ({time.time()-t:.0f}s) -> {OUT}")
    else:
        print("  FAILED"); sys.exit(1)


if __name__ == "__main__":
    main()
