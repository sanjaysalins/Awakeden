"""One-off: animate two_thieves_foreground.png -> clips/two_thieves_foreground.mp4
via HF Seedance 1.5 Pro (user's choice: try the cheaper model first before Kling),
frozen-tableau motion-only prompt matching this session's other panel-fix clips
(see _render31_fix.json / _render_new5_results.json for the proven prompt shape)."""
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

HERE = Path(__file__).resolve().parent
OUT = HERE / "v1" / "visual_16x9_inked"
PNG = OUT / "two_thieves_foreground.png"
CLIP = OUT / "clips" / "two_thieves_foreground.mp4"
SLUG = "04_The_Bronze_Serpent"
MODEL = "seedance1_5"

PROMPT = (
    "Graphic novel inked illustration, painted tableau, a frozen moment. Two "
    "condemned thieves hang bound with rope on rough wooden crosses in the "
    "foreground to either side, Christ crucified on the taller central cross "
    "rising behind and between them, wrists nailed to the wood, head bowed. "
    "The camera holds nearly still, an almost imperceptible settle, resting on "
    "the scene. Nothing moves -- every figure and element stays fixed as drawn, "
    "no blood grows, no blood drips, no blood spreads beyond what is painted at "
    "the wound. No invented motion, no morphing, no new elements, no camera "
    "shake. Painted tableau stays still; only the camera moves."
)

cli = str(config.HF_CLI_PATH)
cmd = [
    cli, "generate", "create", MODEL,
    "--start-image", str(PNG),
    "--prompt", PROMPT,
    "--duration", "4",
    "--aspect_ratio", "16:9",
    "--wait",
]
print(f"[clip] {MODEL} on {PNG.name} ...", flush=True)
result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
blob = (result.stdout or "") + "\n" + (result.stderr or "")
if "nsfw" in blob.lower():
    sys.exit(f"NSFW rejected:\n{blob[-800:]}")
if result.returncode != 0:
    sys.exit(f"FAILED ({result.returncode}):\n{blob[-800:]}")

import re
m = re.search(r"https://\S+?\.mp4", result.stdout, re.IGNORECASE)
if not m:
    sys.exit(f"no mp4 URL found:\n{blob[-800:]}")
url = m.group(0)
CLIP.parent.mkdir(parents=True, exist_ok=True)
req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible/1.0"})
with urllib.request.urlopen(req, timeout=300) as resp:
    CLIP.write_bytes(resp.read())
print(f"       ok -> {CLIP}")
try:
    cost.record_hf(SLUG, "long", "clip", MODEL, note="two_thieves_foreground (reuse fix)")
except Exception as e:
    print(f"[cost] ledger row failed (non-fatal): {e}")
