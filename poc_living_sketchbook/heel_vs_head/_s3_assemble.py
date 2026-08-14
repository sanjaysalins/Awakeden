"""Heel vs Head (Seed of the Woman short #3) -- step 3: assemble the CORE
cut (visual + real narration audio only -- score/sfx/captions/watermark
are separate follow-up stages). Real word-timed spread windows from
`_alignment.json` (forced WhisperX alignment against the locked
narration.mp3, 162/162 words matched).

Architecture ported directly from the sibling shorts' own _s3_assemble.py
(same episode family, same style): ffmpeg extracts every clip to its own
frame sequence once, a ping-pong helper holds/bounces each clip's frames
across its real window. Hard cuts throughout.

  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s3_assemble.py --test-window 15 19
  .venv\\Scripts\\python.exe poc_living_sketchbook/heel_vs_head/_s3_assemble.py
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT  # noqa: E402 -- reuse, don't duplicate

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
SRC_AUDIO = (Path(__file__).resolve().parents[3] / "PythonProject1" / "jesus" /
             "narration" / "43_Not_a_Tie" / "v1" / "narration.mp3")
OUT = HERE / "HEELVSHEAD_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
LAST_WORD_END = 61.711  # "forever." real offset, _alignment.json
HOLD = 3.289             # >= INV-26's 3.0s minimum hold, lands TOTAL on a clean number
TOTAL = 65.0              # LAST_WORD_END + HOLD, frame-exact at 30fps (1950 frames)

# (name, t0, t1) -- real word-timed windows, midpoint of each inter-spread
# silence gap in _alignment.json, matching _PLAN.md's spread table.
SHOTS = [
    ("s01_duel_motif", 0.00, 3.79),
    ("s02_bruise_vs_crush_split", 3.79, 11.11),
    ("s03_serpent_judged", 11.11, 23.21),
    ("s04_serpent_pronouncement", 23.21, 34.78),
    ("s05_heel_and_head_insert", 34.78, 43.79),
    ("s06_own_blow_straining", 43.79, 53.52),
    ("s07_landing_christ", 53.52, TOTAL),
]


def extract_clip_frames(work: Path) -> dict:
    frames = {}
    for name, _t0, _t1 in SHOTS:
        src = CLIPS / f"{name}.mp4"
        if not src.exists():
            raise SystemExit(f"missing clip: {src}")
        d = work / f"_{name}"
        d.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(src),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
             "-r", str(FPS), "-start_number", "0", str(d / "f%05d.png")],
            check=True,
        )
        seq = sorted(d.glob("f*.png"))
        if not seq:
            raise SystemExit(f"no frames extracted from {src}")
        frames[name] = seq
    return frames


def _ppindex(li: int, n: int) -> int:
    cyc = 2 * n - 2 if n > 1 else 1
    j = li % cyc
    if j >= n:
        j = cyc - j
    return max(0, min(n - 1, j))


def shot_frame(frames: dict, name: str, t: float, t0: float) -> Image.Image:
    seq = frames[name]
    li = int((t - t0) * FPS)
    j = _ppindex(li, len(seq))
    path = seq[j]
    if not path.exists():
        fresh = sorted(path.parent.glob("f*.png"))
        if not fresh:
            raise FileNotFoundError(f"{name}: no frames in {path.parent} (fresh reglob also empty)")
        frames[name] = fresh
        j = _ppindex(li, len(fresh))
        path = fresh[j]
    return Image.open(path).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-window", nargs=2, type=float, default=None,
                     help="render only [start end] seconds, for fast iteration (video only, no audio)")
    args = ap.parse_args()

    work = HERE / "_frames"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    print("[extract] pulling frame sequences from all 7 real clips ...")
    frames = extract_clip_frames(work)
    for name, seq in frames.items():
        print(f"    {name}: {len(seq)} frames")

    n_frames = int(round(TOTAL * FPS))
    outdir = work / "grid"
    outdir.mkdir()

    if args.test_window:
        frame_range = range(int(args.test_window[0] * FPS), min(n_frames, int(args.test_window[1] * FPS)))
    else:
        frame_range = range(n_frames)

    for i in frame_range:
        t = i / FPS
        shot = next((s for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1])
        name, t0, t1 = shot
        frame = shot_frame(frames, name, t, t0).convert("RGB")
        frame.save(outdir / f"g{i:05d}.png")

    if args.test_window:
        test_out = HERE / f"_test_{args.test_window[0]:.1f}_{args.test_window[1]:.1f}.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
             "-start_number", str(frame_range.start),
             "-i", str(outdir / "g%05d.png"),
             "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
             str(test_out)],
            check=True,
        )
        print(f"[test] {test_out}")
        shutil.rmtree(work)
        return

    silent = HERE / "_silent.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
         "-i", str(outdir / "g%05d.png"),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", str(FPS), str(silent)],
        check=True,
    )

    if not SRC_AUDIO.exists():
        raise SystemExit(f"missing narration audio: {SRC_AUDIO}")

    filt = f"[1:a]{AFMT},apad=whole_dur={TOTAL}[aout]"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(silent), "-i", str(SRC_AUDIO),
         "-filter_complex", filt,
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-t", f"{TOTAL}",
         str(OUT)],
        check=True,
    )
    shutil.rmtree(work)
    print(f"[ok] {OUT}")


if __name__ == "__main__":
    main()
