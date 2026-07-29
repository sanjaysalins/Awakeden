"""Isolate why the dynamic-camera pass reads as Ken Burns (2026-07-25): test two
prompt techniques on the SAME source page (david_goliath.png) to see whether
Kling can genuinely activate all four panels at once when (a) there is no
camera move competing for its attention, and (b) per-panel motion is
described first and in equal weight to any camera instruction, with the
figure-freeze rule and the environment-must-move rule given equal force.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_panel_technique_test.py
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
STILLS = HERE / "stills" / "_comic_strip_template_test"
OUT = HERE / "clips" / "_comic_strip_template_test"
OUT.mkdir(parents=True, exist_ok=True)
SRC = STILLS / "david_goliath.png"

FIGURE_FREEZE = (
    "Every human figure in every panel stays perfectly frozen the entire time -- no limbs move, "
    "no heads turn, no faces change, no expressions change, no skin changes, no new marks or "
    "liquid appear anywhere on any body or face, and no new figures, hands or objects appear. "
    "INVENT NOTHING on any face or body -- every face stays pixel-for-pixel identical to this "
    "exact image throughout. All caption text stays exactly as drawn, unchanged. "
)
ENV_MANDATE = (
    "But the environment in every panel is NOT frozen and must show bold, clearly visible "
    "motion the entire time, with equal force to the freeze rule above -- clouds, dust, wind, "
    "light and cloth are fully alive and move as much as real weather and light would. "
)
PANEL_MOTION = (
    "In the TOP panel: the storm clouds visibly roll and churn across the sky, and lightning "
    "repeatedly flashes and cracks between them, lighting up the armies on the ridges. "
    "In the MIDDLE-LEFT panel: dust and grit blow across the frame in gusts, and loose threads "
    "at his shoulder flutter in the wind. "
    "In the MIDDLE-RIGHT panel: his hair and the loose threads of his tunic stir in the wind, "
    "and dust motes drift visibly through the light beam behind him. "
    "In the BOTTOM panel: dust and debris visibly burst and swirl upward around the point of "
    "impact, and the light rays shifting through the clouds sweep visibly across the ground. "
    "ALL FOUR panels must show clearly visible motion at the same time, continuously, for the "
    "whole clip -- no panel is allowed to remain a still, static frame. "
)

VARIANT_1 = (
    "A finished comic-strip page with four panels, 9:16. The camera does not move at all -- it "
    "stays perfectly still, filming the whole page fixed in frame, no pan, no zoom, no push, no "
    "rack. " + PANEL_MOTION + FIGURE_FREEZE + ENV_MANDATE
)
VARIANT_2 = (
    "A finished comic-strip page with four panels, 9:16. " + PANEL_MOTION + FIGURE_FREEZE +
    ENV_MANDATE +
    "Only after all four panels are already visibly alive, the camera performs one simple "
    "move: it racks briefly from the top panel down to the bottom panel and holds there, "
    "without slowing or erasing the ongoing motion in every panel."
)

JOBS = [("technique_v1_static_amped", VARIANT_1), ("technique_v2_panelfirst_camera", VARIANT_2)]


def main():
    dur = _hf_duration("kling3_0", 5)
    for name, prompt in JOBS:
        out = OUT / f"{name}.mp4"
        cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(SRC), "--prompt", prompt,
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
            cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[panel-technique-test] {name}", params={"duration": dur})
            print(f"   ok ({time.time()-t:.0f}s)")
        else:
            print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
