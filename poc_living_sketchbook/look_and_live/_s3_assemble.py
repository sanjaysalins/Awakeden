"""Look and Live (Bronze Serpent short #1) -- step 3: assemble the CORE cut
(visual + real narration audio only -- score/sfx/captions/watermark are
separate follow-up stages, matching this project's staged short-form
pipeline). Real word-timed spread windows from `_alignment.json` (forced
WhisperX alignment against the locked narration.mp3, 157/157 words).

Architecture ported directly from poc_living_sketchbook/bronze_serpent/
_s4_assemble.py (same episode family, same style): ffmpeg extracts every
clip to its own frame sequence once, a ping-pong helper holds/bounces each
clip's frames across its real window (shorter or longer than the clip's own
rendered length). No runtime transition classes needed -- unlike Bronze
Serpent's landing (a runtime TornOutPage reveal), this episode's torn-page
landing is already baked into the s12a/s12b stills themselves, so straight
hard cuts throughout (SKILL.md's own stated default) is correct. All verse
lettering lives in the separate _s3b_titlecards.py pass, on the locked
yellow/black/red/white/red-cream card standard -- no Scribed-Ink calligraphy
here, so the episode uses one consistent lettering language throughout.

  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s3_assemble.py --test-window 15 19
  .venv\\Scripts\\python.exe poc_living_sketchbook/look_and_live/_s3_assemble.py
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
             "narration" / "41_The_Cure_Looked_Like_the_Curse" / "v1" / "narration.mp3")
OUT = HERE / "LOOKANDLIVE_living_sketchbook.mp4"

W, H, FPS = 1080, 1920, 30
# Rebuilt 2026-08-16 after 41_The_Cure_Looked_Like_the_Curse's narration.mp3
# was re-synthesized to add a real "god" voice on the Numbers 21:8-9 quote
# (previously narrator-only) -- old timing below is STALE, kept only as a
# comment for reference. Every boundary recomputed fresh from the new
# _alignment.json as the midpoint of each real inter-word silence gap, same
# methodology as this cluster's own serpent_crusher_promised piece.
LAST_WORD_END = 58.854   # "live." real offset, _alignment.json (was 59.271)
HOLD = 3.046              # >= INV-26's 3.0s minimum hold, small safety margin
TOTAL = 61.900            # LAST_WORD_END + HOLD, frame-exact at 30fps (1857 frames)

# (name, t0, t1) -- real word-timed windows built against _alignment.json,
# matching _PLAN.md's spread table.
SHOTS = [
    ("s01_hook", 0.00, 3.859),
    ("s02_object_reveal", 3.859, 7.692),
    ("s03_unused_remedy", 7.692, 9.817),
    ("s04_bitten_arm", 9.817, 12.337),
    ("s05_eye_reflection", 12.337, 16.129),
    ("s06_verse_backdrop", 16.129, 20.451),
    ("s07_look_and_live_acting", 20.451, 26.237),
    ("s08_crowd_healing", 26.237, 31.458),
    ("s09_atmosphere_dawn", 31.458, 38.530),
    ("s10_own_cure", 38.530, 43.070),
    ("s11_plain_sight", 43.070, 48.274),
    ("s12a_torn_to_gold", 48.274, 55.202),
    ("s12b_landing_gold", 55.202, TOTAL),
]

# No baked-in verse card here anymore -- deprecated in favor of the
# yellow/black/red/white/red-cream card system (_s3b_titlecards.py), so the
# whole episode uses ONE consistent lettering language instead of mixing
# Scribed Ink hand-calligraphy with the locked card standard.


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
