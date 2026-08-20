"""North-star pattern-lock POC — final assembly, both aspect ratios (rev 5).

Concats the 8 pre-built {stem}__filled.mp4 clips from build_fills.py — each
already spans its own full slot duration (real AI motion + a devised fill,
see build_fills.py's own docstring for the per-shot device plan) — then mux
narration -> mux score under it via the shared score_mix tail (INV-26:
absolute apad, never relative) -> 3.0s landing hold, video and audio both.
Re-encodes the concat, never stream-copies (independently-encoded clips
don't share timestamps; "-c copy" leaves a visible glitch at every splice).

Score: the reused Robert-Miles/"Children"-direction dna_d cue from the
Look-and-Live score-swap POC (refit_miles_dna_d.py).

Run per ratio:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test/northstar_shortform/assemble.py --ratio 9:16
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test/northstar_shortform/assemble.py --ratio 16:9
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.score_mix import AFMT, mix_tail, output_args  # noqa: E402

HERE = Path(__file__).resolve().parent
NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\SwirlsOfLife_JohnFour_POC\v1\narration.mp3"
)
SCORE_MP3 = HERE / "score" / "score_miles_dna_d.mp3"
OUTRO_HOLD = 3.0

# Beat map scaled from the 60s short-form structure (JACOBS_WELL_STRUCTURE.html)
# onto this narration's ACTUAL length below (SCALE computed at runtime).
BEAT_SECONDS_AT_60S = [5, 7, 8, 10, 10, 8, 7, 5]  # shots 1..8, sums to 60
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


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratio", required=True, choices=["9:16", "16:9"])
    args = ap.parse_args()

    ratio_dir = HERE / args.ratio.replace(":", "x")
    w, h = (1080, 1920) if args.ratio == "9:16" else (1920, 1080)

    narration_len = dur(NARRATION_MP3)
    total = narration_len + OUTRO_HOLD
    scale = narration_len / sum(BEAT_SECONDS_AT_60S)
    slot_secs = [s * scale for s in BEAT_SECONDS_AT_60S]
    print(f"[plan] narration={narration_len:.2f}s scale={scale:.4f} "
          f"slots={[round(s,2) for s in slot_secs]}")

    work = ratio_dir / "_assembly"
    work.mkdir(exist_ok=True)

    # 1) each shot's pre-built filled clip (build_fills.py) already spans its
    # own full slot duration — just verify and collect.
    extended = []
    for stem, slot in zip(SHOT_STEMS, slot_secs):
        src = ratio_dir / f"{stem}__filled.mp4"
        if not src.exists():
            sys.exit(f"missing filled clip: {src} (run build_fills.py first)")
        cdur = dur(src)
        extended.append(src)
        print(f"  [{stem}] {cdur:.2f}s (slot target {slot:.2f}s)")

    # 2) concat — re-encode, not stream copy (see module docstring).
    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in extended), encoding="utf-8")
    silent_video = work / "silent_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-r", "30", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", str(silent_video)])
    print(f"[concat] {dur(silent_video):.2f}s silent video")

    # 3) mux narration onto the silent video (this becomes score_mix's input 0)
    with_narration = work / "with_narration.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(silent_video), "-i", str(NARRATION_MP3),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(with_narration)])

    # 4) score under narration via the shared, INV-26-hardened tail.
    out_final = ratio_dir.parent / f"THE_WELL_{args.ratio.replace(':','x')}.mp4"
    filt = f"[1:a]{AFMT},volume=-9dB[mus];" + mix_tail(total, OUTRO_HOLD, fmt_narration=True)
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(with_narration), "-i", str(SCORE_MP3),
         "-filter_complex", filt] + output_args(out_final, preset="medium", total=total))
    print(f"[done] {out_final}  ({dur(out_final):.2f}s)")


if __name__ == "__main__":
    main()
