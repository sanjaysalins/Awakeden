"""Her Seed (Seed of the Woman short #2) -- step 3: assemble the CORE cut
(visual + real narration audio only -- score/sfx/captions/watermark are
separate follow-up stages). Real word-timed spread windows from
`_alignment.json` (166/166 words matched), snapped to the mid-point of
each inter-spread silence gap -- these landed within a few hundredths of
a second of `_PLAN.md`'s own approximate windows, confirming the plan was
already built against real timing.

Architecture ported directly from the sibling short's own _s3_assemble.py
(same episode family, same style): ffmpeg extracts every clip to its own
frame sequence once, a ping-pong helper holds/bounces each clip's frames
across its real window (every raw clip is 4-5s, shorter than most
windows).

  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s3_assemble.py --test-window 15 19
  .venv\\Scripts\\python.exe poc_living_sketchbook/her_seed/_s3_assemble.py
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
             "narration" / "45_Not_Plan_B" / "v1" / "narration.mp3")
OUT = HERE / "HERSEED_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
LAST_WORD_END = 58.819   # "you." real offset, _alignment.json
HOLD = 3.181              # >= INV-26's 3.0s minimum hold, lands TOTAL on a clean number
TOTAL = 62.0              # LAST_WORD_END + HOLD, frame-exact at 30fps (1860 frames)

# (name, t0, t1) -- real word-timed windows, midpoint of each inter-spread
# silence gap in _alignment.json, matching _PLAN.md's spread table.
SHOTS = [
    ("s01_eden_coming_apart", 0.00, 8.294),
    ("s02_promise_spoken_over_eve", 8.294, 13.250),
    ("s03_already_written_page", 13.250, 20.390),
    ("s04_mary_annunciation", 20.390, 27.877),
    ("s05_line_of_fathers_vertical", 27.877, 34.663),
    ("s06_mary_close", 34.663, 41.214),
    ("s07_hands_reaching", 41.214, 51.259),
    ("s08_landing_christ", 51.259, TOTAL),
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

    print("[extract] pulling frame sequences from all 8 real clips ...")
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
