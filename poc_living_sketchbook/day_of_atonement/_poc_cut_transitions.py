"""POC (2026-08-05, round 2): user rejected any effect applied to a single
held still (camera push/arc, and the raking-light replacement) and asked for
transitions AT THE CUT between two clips instead -- plain still holds within
a scene, a real transition device carrying the visual interest at each cut.

Uses this project's own existing `panel_animator/ink_transition.py` (the
"/ink-transition" skill -- organic ink-bleed "blot" or brush-stroke "wipe"
reveal edge between two clips, $0 deterministic noise-field + maskedmerge,
already built, not new code). Tests BOTH modes on 3 real, varied cut pairs
from this episode so they can be compared in context (not just the bare
transition in isolation): a plain narrative-to-narrative cut, a cut into a
verse card, and a beat-turn cut.

Builds [~2s tail of A] + [transition] + [~2s head of B] per pair/mode, plus
a comparison gallery. Writes to _poc_transitions/, touches nothing else.

Run:
    .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_poc_cut_transitions.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
import ink_transition  # noqa: E402

HERE = Path(__file__).resolve().parent
SEGMENTS = HERE / "_segments"
OUT = HERE / "_poc_transitions"
OUT.mkdir(exist_ok=True)
WORK = OUT / "_work"
WORK.mkdir(exist_ok=True)

W, H, FPS = 1920, 1080, 30
SCALE_CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
VCODEC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]
TRANS_DUR = 0.9
CONTEXT_S = 2.0  # how much clean A / clean B to show around the transition

# (label, spread A name, spread B name) -- varied cut types
PAIRS = [
    ("narrative_to_narrative", "s01_cold_open", "s02_tabernacle_wide"),
    ("narrative_to_versecard", "s19_altar_ministry", "s20_blood_atonement_card"),
    ("beat_turn", "s45_sign_before_veil", "s46_aged_unchanged_veil"),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def build_pair(label: str, a_name: str, b_name: str, mode: str):
    a_clip = SEGMENTS / f"seg_{a_name}.mp4"
    b_clip = SEGMENTS / f"seg_{b_name}.mp4"
    dest = OUT / f"{label}_{mode}.mp4"

    a_head = WORK / f"{label}_{mode}_a_head.mp4"  # A minus its final TRANS_DUR
    run(["ffmpeg", "-y", "-v", "error", "-sseof", f"-{CONTEXT_S:.3f}", "-i", str(a_clip),
         "-t", f"{(CONTEXT_S - TRANS_DUR):.3f}", "-vf", SCALE_CROP, *VCODEC, str(a_head)])

    trans = WORK / f"{label}_{mode}_trans.mp4"
    ink_transition.render(a_clip, b_clip, trans, TRANS_DUR, mode, (0.5, 0.55), FPS)

    b_tail = WORK / f"{label}_{mode}_b_tail.mp4"  # B, from TRANS_DUR to CONTEXT_S
    run(["ffmpeg", "-y", "-v", "error", "-i", str(b_clip), "-ss", f"{TRANS_DUR:.3f}",
         "-t", f"{(CONTEXT_S - TRANS_DUR):.3f}", "-vf", SCALE_CROP, *VCODEC, str(b_tail)])

    listfile = WORK / f"{label}_{mode}_concat.txt"
    listfile.write_text(
        f"file '{a_head.resolve()}'\nfile '{trans.resolve()}'\nfile '{b_tail.resolve()}'\n",
        encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         *VCODEC, str(dest)])
    print(f"[ok] {label} ({mode}) -> {dest}")


if __name__ == "__main__":
    for label, a_name, b_name in PAIRS:
        for mode in ("blot", "wipe"):
            build_pair(label, a_name, b_name, mode)
