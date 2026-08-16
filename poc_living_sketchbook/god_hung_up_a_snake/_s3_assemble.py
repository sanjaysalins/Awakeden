"""God Hung Up a Snake (Bronze Serpent short #2) -- step 3: assemble the
CORE cut (visual + real narration audio only -- score/sfx/captions/watermark
are separate follow-up stages). Real word-timed spread windows from
`_alignment.json` (forced WhisperX alignment, 148/148 words). Architecture
ported directly from look_and_live/_s3_assemble.py -- straight hard cuts
throughout, no runtime transition classes (the torn-page landing is baked
into the s12a/s12b stills themselves), no baked-in verse card (lettering
lives in the separate _s3b_titlecards.py pass, same locked card standard).

  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s3_assemble.py --test-window 0 5
  .venv\\Scripts\\python.exe poc_living_sketchbook/god_hung_up_a_snake/_s3_assemble.py
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
             "narration" / "42_God_Hung_Up_a_Snake" / "v1" / "narration.mp3")
OUT = HERE / "GODHUNGUPASNAKE_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
# RE-ALIGNED 2026-08-16: source narration.mp3 was re-synthesized to add the
# missing "scripture" voice on the Numbers 21:9 quote (memory
# living-sketchbook-subject-variety-gap's sibling fix, same recipe as Romans
# 16:20's own re-synth). Every timestamp below was recomputed from the fresh
# _alignment.json via the SAME gap-midpoint methodology the original build
# used (midpoint of each inter-beat silence gap), not a linear rescale --
# old values kept in comments for the record.
LAST_WORD_END = 58.9      # "too." real offset, _alignment.json (was 57.607)
HOLD = 3.1                 # >= INV-26's 3.0s minimum hold, small safety margin (was 3.193)
TOTAL = 62.0               # LAST_WORD_END + HOLD, frame-exact at 30fps (1860 frames) (was 60.8)

# (name, t0, t1) -- real word-timed windows built against _alignment.json,
# matching _PLAN.md's spread table. (old values in comments)
SHOTS = [
    ("s01_hook", 0.00, 5.448),               # was 0.00, 4.60
    ("s02_pole_reveal", 5.448, 8.072),        # was 4.60, 7.30
    ("s03_texture_insert", 8.072, 10.291),    # was 7.30, 9.50
    ("s04_camp_gathered", 10.291, 15.745),    # was 9.50, 15.00
    ("s05_forge_acting", 15.745, 20.659),     # was 15.00, 19.00
    ("s06_mother_child_look", 20.659, 28.322),  # was 19.00, 26.80
    ("s07_moses_face", 28.322, 30.443),       # was 26.80, 29.50
    ("s08_raw_bronze_insert", 30.443, 36.521),  # was 29.50, 35.80
    ("s09_reaching_soft", 36.521, 42.510),    # was 35.80, 41.60
    ("s10_heavy_sky", 42.510, 48.204),        # was 41.60, 47.30
    ("s11_pole_night", 48.204, 51.657),       # was 47.30, 51.00
    ("s12a_torn_to_gold", 51.657, 54.853),    # was 51.00, 54.00
    ("s12b_landing_christ", 54.853, TOTAL),   # was 54.00, TOTAL(60.8)
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

    print("[extract] pulling frame sequences from all 13 real clips ...")
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
