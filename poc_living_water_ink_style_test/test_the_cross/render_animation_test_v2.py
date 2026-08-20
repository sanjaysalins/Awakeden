"""Animation bake-off v2 for "The Cross" -- INK_LIFE + FROZEN_v2 (2026-08-20
prompt-only redesign, see NORTH_STAR_ANIMATION_PROMPT.md's test plan).
Swirl + panels both get IN-PLACE tone motion only (never a displacement
verb) -- no python compositing. Kling3.0 pro vs veo3_1_lite, same still.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\test_the_cross\\render_animation_test_v2.py
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

ACTOR_NO_MOUTH = (
    "Jesus's expression stays calm, grave, and completely still throughout — his lips stay "
    "closed and completely still, he is not speaking and his mouth does not move at all. His "
    "eyes hold a steady, unwavering gaze toward the viewer, then close in one slow deliberate "
    "blink and open again fully, ending wide open, gaze steady on the viewer. "
)

FROZEN_V2 = (
    "The camera does not move. In the top row of the page — the title, the frame number, and "
    "all three small panels — every ink line, figure, letter, and number stays exactly as "
    "drawn for the entire clip: nothing is added, removed, redrawn, or moved anywhere in that "
    "row, and the row ends the clip looking identical to how it began. The only life in that "
    "row is in the paint itself: the watercolor tones inside the three panels breathe very "
    "gently, deepening and paling slightly in place, like paper under slowly changing light. "
    "Motion of figures happens ONLY inside the one large lower illustration. No new elements, "
    "no invented content, no new text anywhere on the page."
)


def ink_life(gold_verb: str) -> str:
    return (
        "The blue-and-gold ink motif already painted in the scene keeps its exact shape, "
        "length, position, and edges for the entire clip — every curl and thread stays "
        "precisely where it is drawn, and the motif ends the clip identical in outline to how "
        "it began. No new ink ever appears anywhere. Within that fixed outline the ink is "
        "quietly alive: its blue tone slowly deepens and pales again in place, and the small "
        f"gold accents slowly {gold_verb}, like drawn ink under a lamp that is gently passing "
        "over the page. The ink itself never travels, spreads, lengthens, widens, or flows. "
    )


def build_prompt(gold_verb: str) -> str:
    return ACTOR_NO_MOUTH + ink_life(gold_verb) + FROZEN_V2


def render(model: str, extra: list[str], out_name: str, gold_verb: str) -> None:
    out_path = HERE / out_name
    if out_path.exists():
        print(f"  [skip] {out_path.name} already exists")
        return
    prompt = build_prompt(gold_verb)
    cmd = [HF_CLI, "generate", "create", model, "--prompt", prompt,
           "--start-image", str(SRC_PNG), "--aspect_ratio", "9:16"] + extra + ["--wait"]
    print(f"  [{model}] rendering (gold_verb={gold_verb!r})...")
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
    render("kling3_0", ["--mode", "pro", "--duration", "5", "--sound", "off"],
            "the_cross_kling_inklife.mp4", gold_verb="glint softly and settle")
    render("veo3_1_lite", ["--duration", "4"],
            "the_cross_veo_inklife.mp4", gold_verb="warm and settle")
