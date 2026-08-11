"""THROWAWAY EPISODE BUILD -- normalize + concat the 8 picture pieces, then mux
the real narration.mp3 with correct >=3.0s landing-hold padding
(apad=whole_dur=<total>, never pad_dur -- INV-26 / pipeline/score_mix.py)."""
from __future__ import annotations
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEG = HERE / "segments"
INS = HERE / "inserts"
NORM = HERE / "normalized"
NORM.mkdir(exist_ok=True)

NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\29 The Race He Could Never Win\v1\narration.mp3"
)
LAST_WORD_END = 58.88
OUTRO_HOLD = 3.0

PIECES = [
    SEG / "s1.mp4",
    INS / "insert_a_water_stirs.mp4",
    SEG / "s3.mp4",
    SEG / "s4.mp4",
    SEG / "s5.mp4",
    INS / "insert_b_man_rises.mp4",
    SEG / "s7.mp4",
    SEG / "s8.mp4",
]

FFMPEG_ENCODE = [
    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.0",
    "-r", "30", "-fps_mode", "cfr", "-g", "30", "-keyint_min", "30",
]


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def normalize(src: Path, dst: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-an", *FFMPEG_ENCODE, str(dst)],
        check=True, capture_output=True,
    )
    print(f"  [ok] {dst.name}  dur={ffprobe_duration(dst):.3f}s")


def concat(paths: list[Path], out: Path) -> None:
    list_file = NORM / "_concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.as_posix()}'" for p in paths), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(out)],
        check=True, capture_output=True,
    )
    print(f"[ok] concat -> {out.name}  dur={ffprobe_duration(out):.3f}s")


def mux_with_hold(picture_mp4: Path, narration_mp3: Path, out: Path,
                   last_word_end: float, outro_hold: float) -> None:
    picture_dur = ffprobe_duration(picture_mp4)
    total = last_word_end + outro_hold
    video_pad = max(0.0, total - picture_dur)
    print(f"  picture track: {picture_dur:.3f}s | target total: {total:.3f}s | video tpad: {video_pad:.3f}s")
    vf = f"tpad=stop_mode=clone:stop_duration={video_pad:.3f}" if video_pad > 0.01 else "null"
    af = (
        "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
        f"apad=whole_dur={total:.3f}"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(picture_mp4), "-i", str(narration_mp3),
         "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]",
         "-map", "[v]", "-map", "[a]",
         *FFMPEG_ENCODE, "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(out)],
        check=True, capture_output=True,
    )
    print(f"[ok] muxed -> {out.name}  dur={ffprobe_duration(out):.3f}s")


if __name__ == "__main__":
    print("normalizing 8 pieces...")
    norm_paths = []
    for p in PIECES:
        dst = NORM / p.name
        normalize(p, dst)
        norm_paths.append(dst)

    picture = HERE / "picture_track.mp4"
    concat(norm_paths, picture)

    final = HERE / "cut_v1_no_score.mp4"
    mux_with_hold(picture, NARRATION_MP3, final, LAST_WORD_END, OUTRO_HOLD)
