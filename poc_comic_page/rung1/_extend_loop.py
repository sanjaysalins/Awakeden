"""Comic Page Pipeline POC -- Rung 1 Phase 2, Step 3: loop-mode + no-freeze
extension (CP-4). $0, deterministic ffmpeg. Extends a short generative clip
to the full page dwell (default 12.10s), 24fps CFR, via one of:

  boomerang     forward + reversed concatenated into one ping-pong unit,
                looped and trimmed to the exact target length. Use when the
                clip's real motion reads correctly played backwards (drift,
                breathing, flicker -- symmetric/non-directional motion).
  forward       forward-only, repeated with a `--crossfade` (default 0.5s)
                xfade dissolve at each seam, trimmed to the exact target
                length. Use when the motion has a one-way directional read
                that would look wrong reversed.

Usage:
  .venv\\Scripts\\python.exe poc_comic_page/rung1/_extend_loop.py <src.mp4> <out.mp4> \\
      --mode boomerang|forward [--target 12.10] [--crossfade 0.5] [--fps 24]
"""
from __future__ import annotations
import argparse
import math
import subprocess
import tempfile
from pathlib import Path


def probe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(r.stdout.strip())


def _normalize(src: Path, out: Path, fps: int) -> None:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an",
                    "-r", str(fps), "-pix_fmt", "yuv420p", str(out)], check=True)


def extend_boomerang(src: Path, out: Path, target: float, fps: int) -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        norm = td / "norm.mp4"
        _normalize(src, norm, fps)
        rev = td / "rev.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(norm), "-vf", "reverse",
                        "-an", "-r", str(fps), "-pix_fmt", "yuv420p", str(rev)], check=True)
        pingpong = td / "pingpong.mp4"
        listfile = td / "list.txt"
        listfile.write_text(f"file '{norm.as_posix()}'\nfile '{rev.as_posix()}'\n")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(listfile), "-c", "copy", str(pingpong)], check=True)
        pp_dur = probe_duration(pingpong)
        loops = max(1, math.ceil(target / pp_dur))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", str(loops - 1),
                        "-i", str(pingpong), "-t", f"{target:.3f}", "-r", str(fps),
                        "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18",
                        str(out)], check=True)


def extend_forward_crossfade(src: Path, out: Path, target: float, fps: int, crossfade: float) -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        norm = td / "norm.mp4"
        _normalize(src, norm, fps)
        seg_dur = probe_duration(norm)
        if crossfade >= seg_dur:
            crossfade = seg_dur * 0.2
        step = seg_dur - crossfade
        n = 2
        L = seg_dur + step
        while L < target:
            n += 1
            L += step

        inputs = []
        for _ in range(n):
            inputs += ["-i", str(norm)]

        parts = []
        prev = "0:v"
        cur_L = seg_dur
        for i in range(1, n):
            offset = cur_L - crossfade
            label = f"v{i}"
            parts.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={crossfade:.3f}:"
                         f"offset={offset:.3f}[{label}]")
            prev = label
            cur_L = cur_L + step
        filter_complex = ";".join(parts)

        cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + [
            "-filter_complex", filter_complex, "-map", f"[{prev}]",
            "-t", f"{target:.3f}", "-r", str(fps), "-pix_fmt", "yuv420p",
            "-c:v", "libx264", "-crf", "18", str(out),
        ]
        subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--mode", choices=["boomerang", "forward"], required=True)
    ap.add_argument("--target", type=float, default=12.10)
    ap.add_argument("--crossfade", type=float, default=0.5)
    ap.add_argument("--fps", type=int, default=24)
    a = ap.parse_args()

    src, out = Path(a.src), Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    src_dur = probe_duration(src)
    print(f"[extend] {src.name} ({src_dur:.2f}s) -> {a.mode} -> {a.target:.2f}s @ {a.fps}fps")
    if a.mode == "boomerang":
        extend_boomerang(src, out, a.target, a.fps)
    else:
        extend_forward_crossfade(src, out, a.target, a.fps, a.crossfade)
    out_dur = probe_duration(out)
    print(f"[ok] {out} -> {out_dur:.2f}s (target {a.target:.2f}s, delta {out_dur - a.target:+.2f}s)")


if __name__ == "__main__":
    main()
