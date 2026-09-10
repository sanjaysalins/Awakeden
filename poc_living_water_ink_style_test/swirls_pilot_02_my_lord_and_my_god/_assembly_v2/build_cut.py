"""Second first-look assembly -- v5 Flow delivery (fresh project, fully
self-contained prompts). Same real durations as _assembly/build_cut.py
(from ASSEMBLY_PLAN.md), applied to the new clips. Known issues kept as
delivered per the user's own pattern -- see the door-opens-on-Front-Cover
and F04-caption-cutoff defects flagged in chat before this was built.
"""
from __future__ import annotations
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
NARRATION = EP / "narration.mp3"
OUT = EP / "_first_look_cut_v2.mp4"

SHOTS = [
    ("01_front_cover.mp4", 10.005, 7.10),
    ("02_f01.mp4", 10.005, 16.90),
    ("03_f02.mp4", 10.005, 7.30),
    ("04_f03.mp4", 10.005, 12.80),
    ("05_f04.mp4", 10.005, 4.90),
    ("06_back_cover.mp4", 10.005, 15.30),
]

W, H, FPS = 1080, 1920, 30


def process_shot(name: str, native: float, target: float) -> Path:
    src = HERE / name
    out = HERE / f"proc_{name}"
    if out.exists():
        return out
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
    if target <= native:
        vf = f"{scale},trim=duration={target:.3f},setpts=PTS-STARTPTS"
    else:
        pad = target - native
        vf = f"{scale},tpad=stop_mode=clone:stop_duration={pad:.3f}"
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-i", str(src),
        "-vf", vf, "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        str(out),
    ]
    print(f"  [{name}] native={native:.2f}s -> target={target:.2f}s")
    subprocess.run(cmd, check=True)
    return out


def main() -> None:
    processed = [process_shot(name, native, target) for name, native, target in SHOTS]

    concat_list = HERE / "concat_list.txt"
    concat_list.write_text("".join(f"file '{p.name}'\n" for p in processed), encoding="utf-8")

    silent_video = HERE / "_silent_concat.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-c", "copy", str(silent_video)],
        check=True, cwd=HERE,
    )

    subprocess.run(
        ["ffmpeg", "-y", "-v", "error",
         "-i", str(silent_video), "-i", str(NARRATION),
         "-filter_complex", "[1:a]apad=whole_dur=64.3[a]",
         "-map", "0:v", "-map", "[a]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest",
         str(OUT)],
        check=True,
    )
    print(f"\n[done] {OUT}")


if __name__ == "__main__":
    main()
