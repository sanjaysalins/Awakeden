"""POC (2026-08-05, round 5): the top 2 techniques adapted from ArkAIology's
motion-design toolkit (a sibling project, different visual style) into this
project's own hand-inked/no-camera-movement/letterpress-verse vocabulary.
New modules: panel_animator/verse_mask_reveal.py (from ArkAIology's
text_mask_reveal), panel_animator/through_object_cut.py (from ArkAIology's
radial_iris, re-skinned through this project's own ink_transition noise
field instead of a clean lens iris).

Built as [~2s context on A] + [device] + [~2s context on B] so each can be
judged in situ, matching every prior transition POC in this folder.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_arkaiology_adapt.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import verse_mask_reveal  # noqa: E402
import through_object_cut  # noqa: E402

HERE = Path(__file__).resolve().parent
STILLS = HERE / "stills"
OUT = HERE / "_poc_arkaiology_adapt"
OUT.mkdir(exist_ok=True)
WORK = OUT / "_work"
WORK.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30
SCALE_CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
VCODEC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]
CONTEXT_S = 2.0


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def still_hold(still: Path, dest: Path, dur: float):
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still),
         "-t", f"{dur:.3f}", "-vf", SCALE_CROP, *VCODEC, str(dest)])


def concat(parts: list, dest: Path):
    listfile = WORK / f"{dest.stem}_concat.txt"
    listfile.write_text("\n".join(f"file '{p.resolve()}'" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         *VCODEC, str(dest)])


if __name__ == "__main__":
    # 1. Verse-Mask Reveal -- "BLOOD" pressed on the altar card, s21's goat
    # face grows outward from inside its letterforms.
    a_still, b_still = STILLS / "s20_blood_atonement_card.png", STILLS / "s21_goat_innocent.png"
    a_head = WORK / "vmr_a_head.mp4"
    still_hold(a_still, a_head, CONTEXT_S)
    trans = WORK / "vmr_trans.mp4"
    verse_mask_reveal.render(a_still, b_still, trans, "BLOOD", 0.06, 0.06, hold=1.4, grow=1.8)
    b_tail = WORK / "vmr_b_tail.mp4"
    still_hold(b_still, b_tail, CONTEXT_S)
    concat([a_head, trans, b_tail], OUT / "s20_to_s21_verse_mask_reveal.mp4")

    # 2. Through-the-Object Cut -- iris opens on the smoke tendril in s44,
    # the veil scene (s45) arrives through that exact point.
    a_still, b_still = STILLS / "s44_pointing_smoke.png", STILLS / "s45_sign_before_veil.png"
    a_head = WORK / "toc_a_head.mp4"
    still_hold(a_still, a_head, CONTEXT_S)
    trans = WORK / "toc_trans.mp4"
    through_object_cut.render(a_still, b_still, trans, (0.62, 0.30), duration=1.6)
    b_tail = WORK / "toc_b_tail.mp4"
    still_hold(b_still, b_tail, CONTEXT_S)
    concat([a_head, trans, b_tail], OUT / "s44_to_s45_through_object_cut.mp4")
