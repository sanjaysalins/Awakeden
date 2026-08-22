"""Hybrid-style TEST #2 — NOT part of the locked pilot.

User's ask: keep the locked page format's own distinctions (title, frame
number, the 3-panel-plus-main-scene layout, handwritten captions, the
Swirls-of-Life motif) intact, but see whether the Durer-woodcut/cinematic
look from render_test.py's experiment can sit ALONGSIDE it as a variant —
specifically, applied to just the 3 small top panels, while the main scene
stays in the locked page's own gentle ink-and-watercolor wash style.

Reuses F08's REAL locked panel/main-scene content verbatim (imported from
render_jacobs_ladder.py, not retyped) so this is a fair one-variable test —
only the PANELS' rendering style changes, nothing about F08's actual
content does. One hand-assembled prompt (not swirls_page.assemble_still_
prompt(), which has no style-split parameter — this is a one-off test, not
a module change).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_hybrid_panels.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE.parent
REFS = PILOT_DIR / "refs"
OUT = HERE / "f08_hybrid_panels_test.png"

sys.path.insert(0, str(PILOT_DIR))
import render_jacobs_ladder as jl  # noqa: E402

F08 = jl.PAGES["f08"]
p1, p2, p3 = F08.panels

WOODCUT_STYLE = (
    "16th-century Albrecht Durer woodcut linework blended with contemporary cinematic "
    "landscape photography — dense parallel hatching, hard black contours, ink-on-block "
    "texture, dramatic volumetric light rays, deep teal shadows, golden-hour glow, "
    "photographic tonality"
)

PROMPT = (
    'One single storyboard page of hand-drawn animation development art, laid out like a real '
    'found piece of production art. Top-left title, handwrite: "SEQ: THE LADDER". Top-right '
    'frame number, handwrite: "F08". Across the top, a row of exactly three small storyboard '
    f'panels, each with a circled number 1, 2, 3 as its ONLY label — these three panels ONLY '
    f'are rendered in a deliberately different, more intense style from the rest of the page: '
    f'{WOODCUT_STYLE}. '
    f'panel 1 (handwrite: "{p1.label}") {p1.content}, drawn in that woodcut-cinematic style; '
    f'panel 2 (handwrite: "{p2.label}") {p2.content}, drawn in that woodcut-cinematic style; '
    f'panel 3 (handwrite: "{p3.label}") {p3.content}, drawn in that woodcut-cinematic style. '
    'Below them, ONE large full-scene illustration filling the lower half of the page — '
    'returning fully to the page\'s OWN gentle hand-drawn style, delicate ink linework and '
    'soft watercolor on aged cream paper, NOT the panels\' denser woodcut-cinematic treatment — '
    'a ' + F08.still_shot_type + ': ' + F08.main_scene_still.strip() + ' '
    'Small handwritten production notes integrated naturally on the page: a caption beneath '
    f'the main scene, handwrite: "{F08.caption_lines[0]}", and a corner note, handwrite: '
    f'"{F08.corner_note}". No other text, letters, numbers, or words appear anywhere on the '
    'page beyond the exact handwrite strings given above — no invented captions, signs, '
    'inscriptions, or titulus, with no border, box, or speech bubble ever appearing around any '
    'caption or note. Palette for the MAIN SCENE ONLY: black ink, ochre, muted brown, olive '
    'green, clay-red, touches of soft gold wash on aged cream paper with visible grain, not '
    'photorealistic, not anime, no polished graphic design, no clean comic-book inking, no '
    'glowing spiritual VFX. ' + F08.material_closer.strip() + ' The three top panels keep their '
    'own separate deep teal and gold cinematic woodcut palette, described above, distinct from '
    'the main scene\'s palette — the contrast between the two styles on one page is the point '
    'of this test.'
)

REF_IMAGES = [REFS / "jacob_ref.png", REFS / "stone_ref.png", REFS / "staff_ref.png",
              REFS / "ladder_ref.png", REFS / "bethel_ref.png"]

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def main() -> None:
    if "--print" in sys.argv:
        print(PROMPT)
        return
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", PROMPT]
    for ref in REF_IMAGES:
        cmd += ["--image", str(ref)]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print("[nano_banana_pro] rendering hybrid-panel test ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        raise SystemExit(f"FAILED: hf CLI exit {proc.returncode}: "
                          f"{(proc.stderr or proc.stdout).strip()[-800:]}")
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        raise SystemExit(f"FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        OUT.write_bytes(resp.read())
    print(f"-> {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
