"""Low-level ffmpeg/ffprobe primitives for the assembly stage.

Mirrors the subprocess idioms validated in PythonProject1's concat_events.py
(stream-copy concat, forward-slashed paths) and mux_final.py (ffprobe_duration,
tpad+map mux). All commands are built as Python lists — no shell strings, so
Windows path/quoting issues never arise.

ffmpeg/ffprobe must be on PATH (the repo's convention; see concat_events.py).
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import config


def require_ffmpeg() -> None:
    """Raise a clear error if ffmpeg/ffprobe are missing."""
    missing = [b for b in ("ffmpeg", "ffprobe") if not shutil.which(b)]
    if missing:
        raise SystemExit(
            f"{', '.join(missing)} not found on PATH. Install ffmpeg and ensure "
            "ffmpeg/ffprobe are callable (the assembly stage shells out to them)."
        )


def ffprobe_duration(path: Path) -> float:
    """Seconds of media at `path`. Mirrors mux_final.py / per_turn_synth.py."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


# --------------------------------------------------------------------------
# Per-segment render + concat + mux (Phase 2 — appended below in build order)
# --------------------------------------------------------------------------
def render_segment(
    src: Path,
    out: Path,
    source_in_s: float,
    source_out_s: float,
    speed_factor: float,
    slot_duration_s: float,
    canvas_w: int | None = None,
    canvas_h: int | None = None,
    fps: int | None = None,
    log=print,
) -> Path:
    """Render one timeline slot to its own MP4 with uniform codec/params so the
    siblings concat stream-copy cleanly.

    Order of operations (validated): input-seek the trim (`-ss`/`-to`, resets
    PTS origin), then `setpts=PTS/S` to speed UP by S, then `fps` to resample to
    constant fps, then scale/pad/setsar/format. `-t slot` hard-trims the output
    so the slot length is exact (absorbs setpts rounding). Audio dropped (`-an`)
    — the narration is muxed at the very end."""
    w = canvas_w or config.ASSEMBLY_CANVAS_W
    h = canvas_h or config.ASSEMBLY_CANVAS_H
    r = fps or config.ASSEMBLY_FPS
    vf = (
        f"setpts=PTS/{speed_factor:.6f},"
        f"fps={r},"
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,format=yuv420p"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{source_in_s:.6f}", "-to", f"{source_out_s:.6f}",
        "-i", str(src),
        "-an",
        "-vf", vf,
        "-t", f"{slot_duration_s:.6f}",
        "-r", str(r), "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
        "-x264-params", f"keyint={r}:min-keyint={r}:scenecut=0",
        "-movflags", "+faststart",
        str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg render_segment failed for {src.name} -> {out.name}:\n"
            f"  {(result.stderr or '').strip()[-600:]}"
        )
    return out


def render_still(
    image_src: Path,
    out: Path,
    duration_s: float,
    canvas_w: int | None = None,
    canvas_h: int | None = None,
    fps: int | None = None,
    log=print,
) -> Path:
    """Render a FROZEN still image to an MP4 of `duration_s` with the exact same
    codec/canvas params as render_segment, so it concat stream-copies cleanly
    alongside the animated body segments. Used for the hero still bookend — the
    same still rendered for head and tail gives an identical first & last frame."""
    w = canvas_w or config.ASSEMBLY_CANVAS_W
    h = canvas_h or config.ASSEMBLY_CANVAS_H
    r = fps or config.ASSEMBLY_FPS
    vf = (
        f"fps={r},"
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,format=yuv420p"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(image_src),
        "-an",
        "-vf", vf,
        "-t", f"{duration_s:.6f}",
        "-r", str(r), "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
        "-x264-params", f"keyint={r}:min-keyint={r}:scenecut=0",
        "-movflags", "+faststart",
        str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg render_still failed for {image_src.name} -> {out.name}:\n"
            f"  {(result.stderr or '').strip()[-600:]}"
        )
    return out


def extract_frame(video: Path, out_png: Path, t: float = 0.0) -> Path:
    """Grab one frame from a video as a PNG (frame-accurate output-seek). Fallback
    source for the still bookend when the hero PNG is unavailable."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
         "-ss", f"{t:.3f}", "-vframes", "1", str(out_png)],
        capture_output=True, text=True, check=True,
    )
    return out_png


def _concat_list_file(mp4_paths: list[Path], list_path: Path) -> None:
    """Write an ffmpeg concat-demuxer list (forward slashes, escaped quotes).
    Mirrors concat_events.py:build_concat_list_file."""
    lines = []
    for p in mp4_paths:
        s = str(p.resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{s}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="ascii")


def concat_copy(mp4_paths: list[Path], out_path: Path, log=print) -> Path:
    """Stream-copy concat of byte-compatible segments. No re-encode."""
    list_path = out_path.with_name(out_path.stem + ".concat.txt")
    _concat_list_file(mp4_paths, list_path)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(list_path),
        "-c", "copy", str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg concat failed:\n  {(result.stderr or '').strip()[-600:]}"
        )
    return out_path


def mux_narration(
    video: Path, narration_mp3: Path, out_path: Path, log=print
) -> Path:
    """Lay the narration MP3 over the (silent) video. Clones the last frame for
    any sub-frame shortfall so the tail can't go black. Mirrors mux_final.py."""
    video_dur = ffprobe_duration(video)
    audio_dur = ffprobe_duration(narration_mp3)
    pad = max(0.0, audio_dur - video_dur)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(narration_mp3)]
    if pad > 0.02:
        cmd += [
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={pad:.3f}[v]",
            "-map", "[v]", "-map", "1:a",
        ]
    else:
        cmd += ["-map", "0:v", "-map", "1:a"]
    cmd += [
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg mux failed:\n  {(result.stderr or '').strip()[-600:]}"
        )
    return out_path
