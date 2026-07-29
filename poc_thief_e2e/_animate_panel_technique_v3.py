"""Technique test v3 (2026-07-25): same source page and static-camera strategy
as v1, but with every reference to hair, cloth, or held objects stripped out
-- motion is described strictly in sky/clouds/distant ground, never anything
touching or worn by a figure. v1 and v2 showed that motion described near a
figure's body gave Kling license to move the figure and invent content; this
tests whether pure open-environment motion gets all four panels genuinely
alive with zero figure drift.

  .venv\\Scripts\\python.exe poc_thief_e2e/_animate_panel_technique_v3.py
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
SRC = STILLS / "david_goliath.png"

FIGURE_FREEZE_V3 = (
    "Every human figure in every panel stays perfectly frozen the entire time -- no limbs move, "
    "no heads turn, no faces change, no expressions change, no skin changes, no hair moves, no "
    "clothing or cloth moves, no held objects (weapons, shields, slings, stones) move or change "
    "position, and no new figures, hands or objects appear. INVENT NOTHING on any face, body, "
    "clothing or held object -- every figure stays pixel-for-pixel identical to this exact "
    "image throughout, every panel, the whole time. All caption text stays exactly as drawn, "
    "unchanged. "
)
ENV_MANDATE_V3 = (
    "The environment in every panel -- meaning only the sky, clouds, weather, open ground, "
    "distant background and ambient light, NEVER anything touching, worn by, or held by a "
    "figure -- is NOT frozen and must show bold, clearly visible motion the entire time, with "
    "equal force to the freeze rule above. "
)
PANEL_MOTION_V3 = (
    "In the TOP panel: the storm clouds visibly roll and churn across the sky, and lightning "
    "repeatedly flashes and cracks between them, lighting up the distant ridges. "
    "In the MIDDLE-LEFT panel: the storm clouds behind him continue to roll and churn, and a "
    "fine mist drifts slowly across the background behind his silhouette. "
    "In the MIDDLE-RIGHT panel: the clouds behind him continue to shift and churn, and dust "
    "motes drift visibly through the light beam in the background behind him. "
    "In the BOTTOM panel: in the open ground and sky behind the two figures, dust devils swirl "
    "across the distant ground, and the light rays shifting through the clouds sweep visibly "
    "across the distant hillside. "
    "ALL FOUR panels must show clearly visible background motion at the same time, continuously, "
    "for the whole clip -- no panel is allowed to remain a still, static frame. "
)
VARIANT_3 = (
    "A finished comic-strip page with four panels, 9:16. The camera does not move at all -- it "
    "stays perfectly still, filming the whole page fixed in frame, no pan, no zoom, no push, no "
    "rack. " + PANEL_MOTION_V3 + FIGURE_FREEZE_V3 + ENV_MANDATE_V3
)


def main():
    dur = _hf_duration("kling3_0", 5)
    name = "technique_v3_env_only"
    out = OUT / f"{name}.mp4"
    cmd = [HF, "generate", "create", "kling3_0", "--start-image", str(SRC), "--prompt", VARIANT_3,
           "--duration", str(dur), "--aspect_ratio", "9:16", "--mode", "pro", "--sound", "off", "--wait"]
    print(f"[clip] {name} kling3_0 {dur}s -> {out.name} ...", flush=True)
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    if re.search(r"nsfw", blob, re.IGNORECASE):
        print("   NSFW-REJECTED"); return
    m = re.search(r'https?://\S+?\.mp4', blob)
    if not m:
        print(f"   no mp4 url: {blob.strip()[-300:]}"); return
    subprocess.run(["curl", "-s", "-L", m.group(0), "-o", str(out)], check=True)
    if out.exists() and out.stat().st_size > 0:
        cost.record_hf("EW_Thief_POC", "short", "animate", "kling3_0", note=f"[panel-technique-test] {name}", params={"duration": dur})
        print(f"   ok ({time.time()-t:.0f}s)")
    else:
        print("   FAILED")
    print(f"\n[out] {OUT}")


if __name__ == "__main__":
    main()
