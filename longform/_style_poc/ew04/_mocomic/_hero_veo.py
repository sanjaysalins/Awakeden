#!/usr/bin/env python
"""veo the 16:9 hero still -> an 8s wide motion clip (veo3_1_lite via HF). ~8 cr.

Frozen inked-GN tableau, very slow reverent push-in toward the lifted serpent;
only faint dust + cloth stir. Idempotent (skips if the mp4 exists).

  .venv\\Scripts\\python.exe longform/_style_poc/ew04/_mocomic/_hero_veo.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
import config
from pipeline import video_render

config.VIDEO_HF_MODEL = "veo3_1_lite"
config.VIDEO_HF_ASPECT = "16:9"

HERE = Path(__file__).resolve().parent
PNG = HERE / "_landscape" / "hero_serpent_wide.png"
MP4 = HERE / "_landscape" / "hero_serpent_wide.mp4"

PROMPT = (
    "Cinematic very slow reverent push-in toward the bronze serpent lifted high on the pole. "
    "Keep it a FROZEN inked graphic-novel tableau — preserve the exact serpent, pole, faces, "
    "hands and composition, NO morphing of faces or hands, NO new elements, NO invented body "
    "motion, the people stay still and looking up. Only faint drifting desert dust and a gentle "
    "stir of cloth and tent fabric. NO sparkles, NO glitter, NO floating particles, NO light-bloom "
    "or lens flare — steady pale daylight only."
)


def main():
    if MP4.exists() and MP4.stat().st_size > 0:
        print(f"[skip] {MP4.name} exists"); return
    vp = video_render.HFVideoProvider()
    print(f"[veo] {PNG.name} -> {MP4.name} (veo3_1_lite, 16:9, 8s) ...", flush=True)
    vp.animate(PNG, MP4, PROMPT, 8)
    print(f"[ok] {MP4} ({MP4.stat().st_size:,} b)")


if __name__ == "__main__":
    main()
