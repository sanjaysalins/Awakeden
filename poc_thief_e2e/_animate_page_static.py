"""Animate the FULL comic-strip page as ONE clip with a STATIC camera --
no scroll, no pan, no zoom -- but each of the 3 panels gets its OWN distinct
atmospheric motion within its frame, so the whole page reads as "alive"
simultaneously rather than the camera moving through it.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_page_static.py
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
PNG = HERE / "stills" / "_comic_strip_native" / "strip2_promise_ref.png"
OUT = HERE / "clips" / "_comic_strip_native" / "strip2_static_page.mp4"

PROMPT = (
    "A finished comic-strip page with three panels stacked vertically, filmed with the camera "
    "held completely still -- the whole page and every panel border stay perfectly fixed in "
    "frame the entire time, no camera movement, no zoom, no pan, no scroll. Every figure in "
    "every panel stays perfectly frozen the entire time -- no limbs move, no heads turn, no "
    "faces change, no morphing, and no new figures, hands or objects appear. INVENT NOTHING: "
    "show only what is already drawn in this exact image. Only the light and the air are alive, "
    "and each panel breathes independently and differently from the others: in the TOP panel, "
    "storm clouds drift faintly behind the figure; in the MIDDLE panel, the dark background "
    "breathes gently with faint shifting shadow; in the BOTTOM panel, the golden light rays "
    "shift and glow softly, brighter and dimmer."
)


def main():
    dur = _hf_duration("kling3_0", 5)
    cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(PNG), "--prompt", PROMPT,
           "--duration", str(dur), "--aspect_ratio", "9:16", "--mode", "pro", "--sound", "off", "--wait"]
    print(f"[clip] strip2_static_page kling3_0 {dur}s -> {OUT.name} ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-300:]}"); return
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(OUT)], check=True)
    if OUT.exists() and OUT.stat().st_size > 0:
        cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note="[static-page]", params={"duration": dur})
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")


if __name__ == "__main__":
    main()
