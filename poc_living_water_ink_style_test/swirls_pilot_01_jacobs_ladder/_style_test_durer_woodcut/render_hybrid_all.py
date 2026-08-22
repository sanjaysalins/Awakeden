"""Hybrid-style stills pass — F01 through F07 (F08 already validated in
render_hybrid_panels.py). Step 1 of the staged "book" plan: cheap stills
only, no animation yet, to see whether the woodcut-panels/locked-main-scene
split holds across every page's real content, not just F08's.

Reuses each page's REAL locked panel/main-scene content verbatim (imported
from render_jacobs_ladder.py), same style-split instruction validated on
F08: the 3 top panels render in the Durer-woodcut/cinematic look, the main
scene stays in the locked page's own ink-and-watercolor wash — motif dosage
untouched, main-scene-only (per the plan: swirls stay out of the panels).

F01 has no chained refs (it's the establishing page in the base pilot) —
rendered the same way here.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\render_hybrid_all.py
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

sys.path.insert(0, str(PILOT_DIR))
import render_jacobs_ladder as jl  # noqa: E402

WOODCUT_STYLE = (
    "16th-century Albrecht Durer woodcut linework blended with contemporary cinematic "
    "landscape photography — dense parallel hatching, hard black contours, ink-on-block "
    "texture, dramatic volumetric light rays, deep teal shadows, golden-hour glow, "
    "photographic tonality"
)

_IMG_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

PAGE_IDS = ["f01", "f02", "f03", "f04", "f05", "f06", "f07"]


def build_prompt(spec) -> str:
    p1, p2, p3 = spec.panels
    return (
        f'One single storyboard page of hand-drawn animation development art, laid out like a '
        f'real found piece of production art. Top-left title, handwrite: "SEQ: {spec.seq_title}". '
        f'Top-right frame number, handwrite: "{spec.frame_label}". Across the top, a row of '
        f'exactly three small storyboard panels, each with a circled number 1, 2, 3 as its ONLY '
        f'label — these three panels ONLY are rendered in a deliberately different, more intense '
        f'style from the rest of the page: {WOODCUT_STYLE}. '
        f'panel 1 (handwrite: "{p1.label}") {p1.content}, drawn in that woodcut-cinematic style; '
        f'panel 2 (handwrite: "{p2.label}") {p2.content}, drawn in that woodcut-cinematic style; '
        f'panel 3 (handwrite: "{p3.label}") {p3.content}, drawn in that woodcut-cinematic style. '
        f'Below them, ONE large full-scene illustration filling the lower half of the page — '
        f'returning fully to the page\'s OWN gentle hand-drawn style, delicate ink linework and '
        f'soft watercolor on aged cream paper, NOT the panels\' denser woodcut-cinematic '
        f'treatment — a {spec.still_shot_type}: {spec.main_scene_still.strip()} '
        f'Small handwritten production notes integrated naturally on the page: a caption '
        f'beneath the main scene, handwrite: "{spec.caption_lines[0]}", and a corner note, '
        f'handwrite: "{spec.corner_note}". No other text, letters, numbers, or words appear '
        f'anywhere on the page beyond the exact handwrite strings given above — no invented '
        f'captions, signs, inscriptions, or titulus, with no border, box, or speech bubble ever '
        f'appearing around any caption or note. Palette for the MAIN SCENE ONLY: black ink, '
        f'ochre, muted brown, olive green, clay-red, touches of soft gold wash on aged cream '
        f'paper with visible grain, not photorealistic, not anime, no polished graphic design, '
        f'no clean comic-book inking, no glowing spiritual VFX. {spec.material_closer.strip()} '
        f'The three top panels keep their own separate deep teal and gold cinematic woodcut '
        f'palette, described above, distinct from the main scene\'s palette — the contrast '
        f'between the two styles on one page is the point of this test.'
    )


def render(pid: str) -> bool:
    spec = jl.PAGES[pid]
    out = HERE / f"{pid}_hybrid_panels_test.png"
    if out.exists():
        print(f"[skip] {out.name} already exists")
        return True
    prompt = build_prompt(spec)
    cmd = [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt]
    for ref in spec.refs:
        cmd += ["--image", ref.path]
    cmd += ["--aspect_ratio", "9:16", "--resolution", "2k", "--wait"]
    print(f"[{pid}] rendering hybrid ...")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=600)
    if proc.returncode != 0:
        print(f"  FAILED: hf CLI exit {proc.returncode}: "
              f"{(proc.stderr or proc.stdout).strip()[-800:]}")
        return False
    match = _IMG_URL_RE.search(proc.stdout)
    if not match:
        print(f"  FAILED: no output URL in stdout: {proc.stdout.strip()[-800:]}")
        return False
    req = urllib.request.Request(match.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out.write_bytes(resp.read())
    print(f"  -> {out.name} ({out.stat().st_size:,} bytes)")
    return True


def main() -> None:
    args = sys.argv[1:] or PAGE_IDS
    for pid in args:
        if pid not in jl.PAGES:
            print(f"  skip unknown page id {pid!r}")
            continue
        render(pid)


if __name__ == "__main__":
    main()
