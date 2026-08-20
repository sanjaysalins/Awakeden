"""Animation prompt v3 -- multi-shot generalization test (2026-08-20), directly
adopting the user's own validated Kling prompt structure: short, mostly
positive, per-panel BOUNDED content motion (not vague tone-breathing), and
swirl/halo motion described as staying within its own fixed area (rotate/
flow/drift) rather than growing/spreading from a source point -- that
distinction, not "motion vs no motion," is what actually caused shot 6's
2026-08-19 escalation.

3 shots from the existing John 4 sequence (stills reused, $0), Kling3.0 pro
only, 9:16 only. See NORTH_STAR_ANIMATION_PROMPT.md for the doc this feeds.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_prompt_v3_multishot.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
SRC_DIR = HERE.parent / "northstar_shortform" / "9x16"
_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

SHOTS = [
    {
        "stem": "shot04_closeup_jesus_five_husbands",
        "out": "shot04_v3.mp4",
        "prompt": (
            "Stationary camera, locked close-up shot of the 2D storyboard layout, frame "
            "borders and all baked text stay static. Animate isolated motion inside each "
            "panel: panel 1 the woman's eyes widen slightly in realization; panel 2 her hands "
            "tighten almost imperceptibly on the waterpot rope; panel 3 heat shimmer drifts "
            "faintly over the well mouth. Large bottom panel: Jesus's lips stay closed, not "
            "speaking; his eyes hold steady on the viewer, one slow blink; the soft blue "
            "threads near him drift gently within their own small area, never spreading "
            "further."
        ),
    },
    {
        "stem": "shot07_wide_moving_she_runs",
        "out": "shot07_v4.mp4",
        "prompt": (
            "Stationary camera, locked wide shot of the 2D storyboard layout, frame borders "
            "and all baked text stay static. Animate isolated motion inside each panel: panel "
            "1 the abandoned waterpot sits still, a faint shimmer of heat over the ground "
            "beside it; panel 2 the woman's face shows urgent joy, hair catching motion; panel "
            "3 dust drifts faintly over the distant town gate. Large bottom panel: the woman "
            "runs steadily along the path AWAY from the well and TOWARD the distant town the "
            "whole time, moving forward only, never turning back and never approaching the "
            "well; her robes and head covering stream behind her with her stride; her arms "
            "swing empty and free. The clay waterpot remains completely still on the well's "
            "stone edge for the entire clip — it never moves, tips, or falls. The thin "
            "blue-gold ink thread already trailing from the well stays exactly the same size, "
            "length, and position for the whole clip; only its color tone breathes gently, "
            "deepening and lightening in place — it never widens, lengthens, or flows "
            "anywhere."
        ),
    },
    {
        "stem": "shot08_wide_landing_town_arrives",
        "out": "shot08_v4.mp4",
        "prompt": (
            "Stationary camera, locked wide shot of the 2D storyboard layout, frame borders "
            "and all baked text stay static. Animate isolated motion inside each panel: panel "
            "1 the crowd streams gently through the town gate; panel 2 the woman turns back, "
            "gesturing the crowd onward; panel 3 Jesus's robe shifts faintly in a light "
            "breeze. Large bottom panel: the woman walks forward and arrives at Jesus, "
            "stopping close beside him and turning to face him; the rest of the crowd "
            "continues walking forward behind her at an even pace, gathering around the well; "
            "Jesus's open arms hold their welcoming gesture toward all of them. The diffused "
            "blue-and-gold ink threads drift smoothly through the air of the scene, within "
            "their own fixed band, never growing beyond it."
        ),
    },
]


def render(shot: dict) -> None:
    out_path = HERE / shot["out"]
    if out_path.exists():
        print(f"  [skip] {out_path.name} already exists")
        return
    src_png = SRC_DIR / f"{shot['stem']}.png"
    cmd = [HF_CLI, "generate", "create", "kling3_0", "--prompt", shot["prompt"],
           "--start-image", str(src_png), "--aspect_ratio", "9:16",
           "--mode", "pro", "--duration", "5", "--sound", "off", "--wait"]
    print(f"  [{shot['stem']}] rendering...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900)
    if proc.returncode != 0:
        print(f"        FAILED: hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-800:]}")
        return
    match = _URL_RE.search(proc.stdout)
    if not match:
        print(f"        FAILED: no video URL in stdout: {proc.stdout.strip()[-800:]}")
        return
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    for shot in SHOTS:
        render(shot)
