"""Animation bake-off for "The Cross" -- Kling3.0 pro vs veo3_1_lite, same
still, same motion prompt, 9:16 only. See DESIGN.md for the design rationale.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_animation_test.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
SRC_PNG = HERE / "the_cross_v2_9x16.png"
_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

MOTION = (
    "Jesus's expression stays calm, grave, and completely still throughout — his lips stay "
    "closed and completely still, he is not speaking and his mouth does not move at all. His "
    "eyes hold a steady, unwavering gaze toward the viewer, then close in one slow deliberate "
    "blink and open again fully, ending wide open, gaze steady on the viewer. The blue-and-gold "
    "ink motif already painted in the lower illustration — wherever it appears — also stays "
    "completely still and unchanging for the entire clip: no new curl, thread, bloom, or trail "
    "of ink ever appears, spreads, grows, lengthens, or moves anywhere in the frame. The camera "
    "does not move. The top row of the page — the title, the frame number, and all three small "
    "panels with everything drawn inside them — is a completely static, unchanging picture for "
    "the entire clip: not one new mark, line, color, or letter ever appears anywhere in that "
    "row, and nothing already there ever fades, moves, or changes. Motion happens ONLY inside "
    "the one large lower illustration. No new elements, no invented content, no new text "
    "anywhere on the page."
)


def render(model: str, extra: list[str], out_name: str) -> None:
    out_path = HERE / out_name
    if out_path.exists():
        print(f"  [skip] {out_path.name} already exists")
        return
    cmd = [HF_CLI, "generate", "create", model, "--prompt", MOTION,
           "--start-image", str(SRC_PNG), "--aspect_ratio", "9:16"] + extra + ["--wait"]
    print(f"  [{model}] rendering...")
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
    render("kling3_0", ["--mode", "pro", "--duration", "5", "--sound", "off"], "the_cross_kling.mp4")
    render("veo3_1_lite", ["--duration", "4"], "the_cross_veo.mp4")
