"""Compose -- static-composite devices + the ffmpeg normalize/concat/mux chain.

`tear_vertical()` is new: models the torn curtain (Matthew 27:51) as a static
AFTER-state composite -- a paid animated version of the actual tearing motion
is a separate, later concern (see the Two Goats commission's Insert B).

`normalize_and_concat()` and `mux_with_landing_hold()` promote the ffmpeg
subprocess pipeline from
`poc_bethesda_style_test/far_corner_episode/assemble.py`'s `normalize()` +
`concat()` + `mux_with_hold()`. `mux_with_landing_hold()` is promoted EXACTLY
as-is -- it is the INV-26 landing-hold logic (`apad=whole_dur=<total>`, never
`apad=pad_dur=` -- that was a real historical bug in this project) and must
not be changed.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FFMPEG_ENCODE = [
    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.0",
]


# --------------------------------------------------------------------------
# static composite: the torn curtain
# --------------------------------------------------------------------------
def _seam_x_for_row(t: float, tear_x_px: float, jag_amplitude_px: int) -> float:
    """Full-height jagged wobble, same sum-of-sines spirit as
    path_draw.draw_wobbled_path's hand-wobble (low-frequency, not per-pixel
    noise), evaluated at row-fraction t in [0,1]."""
    wobble = (
        math.sin(t * 5.3 + 1.7) * jag_amplitude_px
        + math.sin(t * 11.0 + 0.4) * jag_amplitude_px * 0.35
        + math.sin(t * 23.0) * jag_amplitude_px * 0.15
    )
    return tear_x_px + wobble


def tear_vertical(
    img: Image.Image,
    tear_x_frac: float,
    jag_amplitude_px: int = 18,
    gap_px: int = 14,
    light_color=(255, 244, 214),
) -> Image.Image:
    """Split `img` along a jagged vertical seam near `tear_x_frac`, displace
    the left half left and the right half right by gap_px//2 each, and fill
    the revealed gap with `light_color` (light spilling through a torn
    curtain). Returns one composited image, same size as input."""
    arr = np.asarray(img.convert("RGB"))
    h, w, _ = arr.shape
    half_gap = max(0, gap_px // 2)
    tear_x_px = tear_x_frac * w

    out = np.empty((h, w, 3), dtype=np.uint8)
    out[:, :] = light_color
    xs = np.arange(w)

    for y in range(h):
        t = y / max(1, h - 1)
        seam = _seam_x_for_row(t, tear_x_px, jag_amplitude_px)
        seam = min(max(seam, 0.0), float(w))

        left_mask = (xs + half_gap) < seam
        right_mask = (xs - half_gap) >= seam

        if left_mask.any():
            src_left = np.clip(xs[left_mask] + half_gap, 0, w - 1)
            out[y, left_mask] = arr[y, src_left]
        if right_mask.any():
            src_right = np.clip(xs[right_mask] - half_gap, 0, w - 1)
            out[y, right_mask] = arr[y, src_right]

    return Image.fromarray(out, "RGB")


# --------------------------------------------------------------------------
# ffmpeg chain
# --------------------------------------------------------------------------
def _ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def normalize_and_concat(
    pieces: list[Path],
    out: Path,
    canvas_w: int = 1080,
    canvas_h: int = 1920,
    fps: int = 30,
) -> Path:
    """Re-encode every piece to matching codec params (video-only), then
    concat via the ffmpeg concat demuxer with `-c copy`. Promotes
    assemble.py's normalize() + concat()."""
    out.parent.mkdir(parents=True, exist_ok=True)
    norm_dir = out.parent / "_normalize_and_concat_work"
    norm_dir.mkdir(parents=True, exist_ok=True)

    norm_paths = []
    for p in pieces:
        dst = norm_dir / p.name
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(p), "-an",
             *FFMPEG_ENCODE,
             "-r", str(fps), "-fps_mode", "cfr", "-g", str(fps), "-keyint_min", str(fps),
             "-vf", f"scale={canvas_w}:{canvas_h}",
             str(dst)],
            check=True, capture_output=True,
        )
        norm_paths.append(dst)

    list_file = norm_dir / "_concat_list.txt"
    list_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in norm_paths), encoding="utf-8"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(out)],
        check=True, capture_output=True,
    )
    return out


def mux_with_landing_hold(
    picture_mp4: Path,
    narration_mp3: Path,
    out: Path,
    last_word_end_s: float,
    outro_hold_s: float = 3.0,
) -> Path:
    """INV-26 landing-hold mux: audio padded to an ABSOLUTE total length via
    `apad=whole_dur=<total>` (never `apad=pad_dur=`, a real historical bug in
    this project); video cloned-hold via `tpad=stop_mode=clone` if the
    picture track is shorter than the target total. Promoted EXACTLY as-is
    from assemble.py's mux_with_hold() -- do not change the padding formula."""
    picture_dur = _ffprobe_duration(picture_mp4)
    total = last_word_end_s + outro_hold_s
    video_pad = max(0.0, total - picture_dur)
    vf = f"tpad=stop_mode=clone:stop_duration={video_pad:.3f}" if video_pad > 0.01 else "null"
    af = (
        "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
        f"apad=whole_dur={total:.3f}"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(picture_mp4), "-i", str(narration_mp3),
         "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]",
         "-map", "[v]", "-map", "[a]",
         *FFMPEG_ENCODE, "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(out)],
        check=True, capture_output=True,
    )
    return out
