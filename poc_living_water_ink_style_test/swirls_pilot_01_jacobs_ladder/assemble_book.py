"""Final book assembly: front cover -> locked interior (unchanged) -> back
cover. Covers play silent (a deliberate cold-open/closing-credits
convention) -- the interior's own narration+score mix is untouched.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\assemble_book.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
COVERS = HERE / "_style_test_durer_woodcut"
FRONT = COVERS / "front_cover_woodcut.mp4"
BACK = COVERS / "back_cover_woodcut.mp4"
INTERIOR = HERE / "THE_LADDER_pilot_cut_scored.mp4"
OUT = HERE / "THE_LADDER_BOOK_final.mp4"

W, H, FPS = 720, 1280, 30


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def normalize_with_silence(src: Path, out: Path) -> None:
    """Re-encode to the target W/H/FPS and attach a silent audio track
    matching the video's own duration."""
    d = dur(src)
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(src),
         "-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
         "-map", "0:v", "-map", "1:a",
         "-vf", f"scale={W}:{H}:flags=lanczos,setsar=1", "-r", str(FPS),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)])


def main() -> None:
    work = HERE / "_assembly"
    work.mkdir(exist_ok=True)

    front_norm = work / "front_norm.mp4"
    back_norm = work / "back_norm.mp4"
    interior_norm = work / "interior_norm.mp4"

    normalize_with_silence(FRONT, front_norm)
    normalize_with_silence(BACK, back_norm)
    # interior already has real audio -- just normalize video params, keep its own audio
    run(["ffmpeg", "-y", "-v", "error", "-i", str(INTERIOR),
         "-vf", f"scale={W}:{H}:flags=lanczos,setsar=1", "-r", str(FPS),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", str(interior_norm)])

    with_narration = work / "with_narration.mp4"  # unused, placeholder guard
    concat_list = work / "book_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in [front_norm, interior_norm, back_norm]),
        encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)])
    print(f"[done] {OUT}  ({dur(OUT):.2f}s = {dur(front_norm):.2f} + {dur(interior_norm):.2f} + {dur(back_norm):.2f})")


if __name__ == "__main__":
    main()
