"""Deterministic safety net for the title/frame-number/3-panel row.

Diagnostic finding (2026-08-19, contact-sheet review): the video model does
NOT reliably honor "stay frozen" for that region — shot 2 hallucinated new
baked text ("Jesus") into panel 1 mid-clip, and let the swirl bleed into
panel 2. Rather than trust prompting alone, this composites the SOURCE
STILL's own panel row back onto every frame of the rendered clip — the
region becomes pixel-guaranteed static, sourced from the real approved art,
regardless of what the video model actually did there.

Freeze boundary measured per-ratio from the panel row's bottom border
(darkest horizontal band in the upper half of the page): 9:16 -> 43% of
frame height, 16:9 -> 40%.

Run: .venv\\Scripts\\python.exe lock_panels.py --shots 1,2,3,4,5,6,7,8 --ratios 9:16,16:9
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FREEZE_FRAC = {"9:16": 0.43, "16:9": 0.40}
SHOT_STEMS = [
    "shot01_wide_the_ask",
    "shot02_medium_2shot_living_water",
    "shot03_2shot_breaking_to_singles",
    "shot04_closeup_jesus_five_husbands",
    "shot05_compressed_2shot_spirit_truth",
    "shot06_held_single_jesus_i_am_he",
    "shot07_wide_moving_she_runs",
    "shot08_wide_landing_town_arrives",
]


def probe_size(p: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=s=x:p=0", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def lock_one(stem: str, ratio: str, ratio_dir: Path) -> None:
    src_png = ratio_dir / f"{stem}.png"
    src_mp4 = ratio_dir / f"{stem}.mp4"
    out_mp4 = ratio_dir / f"{stem}__locked.mp4"
    if not src_png.exists() or not src_mp4.exists():
        print(f"  [skip] missing input for {ratio}/{stem}")
        return

    cw, ch = probe_size(src_mp4)
    band_h = int(round(ch * FREEZE_FRAC[ratio]))
    # crop the top band from the SOURCE STILL at the clip's own resolution,
    # then overlay it at (0,0) on every frame of the clip.
    filt = (
        f"[1:v]scale={cw}:{ch},crop={cw}:{band_h}:0:0[band];"
        f"[0:v][band]overlay=0:0:shortest=1[v]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src_mp4), "-loop", "1", "-i", str(src_png),
         "-filter_complex", filt, "-map", "[v]", "-an",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         str(out_mp4)],
        check=True,
    )
    print(f"  [locked] {ratio}/{stem} (top {FREEZE_FRAC[ratio]*100:.0f}% = {band_h}px pinned to source still)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", default="1,2,3,4,5,6,7,8")
    ap.add_argument("--ratios", default="9:16,16:9")
    args = ap.parse_args()
    wanted = {int(x) for x in args.shots.split(",")}
    for ratio in args.ratios.split(","):
        ratio_dir = HERE / ratio.replace(":", "x")
        for i, stem in enumerate(SHOT_STEMS, start=1):
            if i in wanted:
                lock_one(stem, ratio, ratio_dir)
