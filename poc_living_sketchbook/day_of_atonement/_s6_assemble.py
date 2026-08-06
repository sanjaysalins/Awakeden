"""Day of Atonement LONG -- step 6: SIMPLE FIRST CUT. Turns
`_spread_windows.json` (76 spreads, each with a resolved fill mode) into one
silent 1920x1080@30fps video, then muxes the real locked narration on top
with the INV-26 landing hold. Hard cuts between spreads (no crossfade/
page-turn devices) -- those are a deliberate polish-pass-2 layer added AFTER
this base cut is seen and approved. Nothing here is generative -- every
segment is built by ffmpeg trim/pad/concat over already-approved clips plus
$0 deterministic camera moves (panel_animator/dynamic_cam3d.py) over a
clip's own last frame; nothing is ever regenerated or played in reverse.

This hard-cut-only concat also satisfies _PLAN.md's own "multi-stage
hard-cut PAIRS" requirement (10/11 strange fire, 25/26/27 slaying through
the veil, 61/62 whole-veil->torn) for free -- there is no dissolve/blend
mode in this recipe at all, so every seam in the film is already a hard cut.

Fill modes (resolved per-spread in `_spread_windows.json` by
`_s5b_spread_windows.py`):
  once_trim -- clip is >= window: play from its start, trimmed to fit.
  once_hold -- clip already AT (or extended to, by
               `_s5c_extend_deterministic.py`) the window duration: play as
               -is, pad any sub-frame remainder by holding the last frame.
  fwd_drift -- clip < window: play the clip forward ONCE at native speed
               (the real motion, exactly as generated, NEVER reversed),
               then fill the remainder with a $0 deterministic camera
               push/arc over the clip's own last frame -- real continuing
               motion instead of a repeated bounce loop.
  static_still -- unused this episode (every spread has a real clip) --
               kept for interface parity in case a future rebuild needs it.

REDESIGNED 2026-08-05: this file used to also implement pingpong/
slow_pingpong/fwd_tail_bounce (forward+reverse bounce loops). Removed
entirely after the user watched the first cut and reported "loads of
backwards walking animation" -- any clip with directional motion (walking,
carrying, leading an animal) read as walking BACKWARDS during a bounce's
reverse half. Nothing in this recipe plays a clip backward anymore, full
stop -- see _s5b_spread_windows.py's own docstring for the fuller reasoning.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py                 # full 76-spread build
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py --only s01_cold_open,s76_already_inside   # test gate
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py --concat-only   # (re)join existing segments + mux audio
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "panel_animator"))
from dynamic_cam3d import render_move  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _devices as DEV  # noqa: E402
CLIPS = HERE / "clips"
STILLS = HERE / "stills"
SEGMENTS = HERE / "_segments"
SEGMENTS.mkdir(exist_ok=True)
WORK = HERE / "_assemble_work"
WORK.mkdir(exist_ok=True)

WINDOWS = HERE / "_spread_windows.json"
NARRATION = HERE.parents[1] / "longform" / "EW01_Two_Goats" / "v1" / "narration.mp3"

W, H, FPS = 1920, 1080, 30
SCALE_CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
VCODEC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS)]

OUT_SILENT = HERE / "_DAYOFATONEMENT_LONG_silent.mp4"
OUT_CUT = HERE / "DAYOFATONEMENT_LONG_living_sketchbook.mp4"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stderr[-3000:]}")


def build_segment(row: dict, seg_path: Path):
    name = row["name"]
    dur = row["dur"]
    mode = row["mode"]
    clip = CLIPS / f"{name}.mp4"

    if name in DEV.VERSE_CARDS:
        DEV.render_verse_card(name, STILLS / f"{name}.png", seg_path, dur, row["start"])
        return

    if name in DEV.SPECIAL_CARDS:
        DEV.render_special_card(name, STILLS / f"{name}.png", seg_path, dur, row["start"])
        return

    device_info = DEV.DEVICE_ASSIGNMENTS.get(name)
    if device_info and device_info["scope"] == "full":
        params = dict(device_info["params"])
        params.setdefault("abs_start", row["start"])
        DEV.render_device(device_info["device"], STILLS / f"{name}.png", seg_path, dur, **params)
        return

    if mode == "static_still":
        still = STILLS / f"{name}.png"
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still),
             "-t", f"{dur:.3f}", "-vf", SCALE_CROP, *VCODEC, str(seg_path)])
        return

    if mode == "once_trim":
        run(["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-t", f"{dur:.3f}",
             "-vf", SCALE_CROP, *VCODEC, str(seg_path)])
        return

    if mode == "once_hold":
        clip_dur = row["clip_dur"]
        remainder = max(0.0, dur - clip_dur)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(clip),
             "-vf", f"{SCALE_CROP},tpad=stop_mode=clone:stop_duration={remainder:.3f}",
             "-t", f"{dur:.3f}", *VCODEC, str(seg_path)])
        return

    if mode == "fwd_drift":
        clip_dur = row["clip_dur"]
        tail_s = row["tail_s"]
        move = row["move"]
        focus = tuple(row["focus"])
        amp = row["amp"]

        fwd = WORK / f"{name}_fwd.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-vf", SCALE_CROP,
             *VCODEC, str(fwd)])

        last_frame = WORK / f"{name}_lastframe.png"
        run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.15", "-i", str(clip),
             "-frames:v", "1", str(last_frame)])
        drift = WORK / f"{name}_drift.mp4"
        if device_info and device_info["scope"] == "tail":
            params = dict(device_info["params"])
            params.setdefault("abs_start", row["start"] + clip_dur)
            DEV.render_device(device_info["device"], last_frame, drift, tail_s, **params)
        else:
            render_move(last_frame, move, tail_s, focus, drift, amp=amp)

        listfile = WORK / f"{name}_concat.txt"
        listfile.write_text(f"file '{fwd.resolve()}'\nfile '{drift.resolve()}'\n", encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
             *VCODEC, str(seg_path)])
        return

    raise ValueError(f"{name}: unknown/unresolved fill mode {mode!r}")


def _transition_for(seam: tuple) -> dict | None:
    if seam in DEV.NO_TRANSITION_SEAMS:
        return None
    return DEV.TRANSITION_OVERRIDES.get(seam, DEV.DEFAULT_TRANSITION)


def _trim_piece(seg: Path, start_trim: float, full_dur: float, end_trim: float, dest: Path):
    if dest.exists():
        return
    piece_dur = max(0.3, full_dur - start_trim - end_trim)
    if piece_dur < full_dur - start_trim - end_trim - 0.001:
        print(f"[warn] {dest.name}: transition trims exceeded segment duration, clamped to {piece_dur:.2f}s")
    tmp = dest.with_suffix(".partial.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(seg), "-ss", f"{start_trim:.3f}",
         "-t", f"{piece_dur:.3f}", *VCODEC, str(tmp)])
    tmp.replace(dest)  # atomic -- dest only ever appears once fully written (crash-safe cache)


def concat_segments(rows: list, out_path: Path):
    """Splices the ~75 transitions in between the hard cuts (RESUME.md
    section 5): each 2-clip/2-still transition device produces a standalone
    `duration`-length clip built from the real tail of A + real head of B (or
    A/B's own stills), inserted in place of half that duration trimmed off
    each side's segment -- total film duration (and every later seam's
    narration-sync timing) is exactly unchanged, only redistributed within
    the trimmed segments' own tails/heads."""
    listfile = WORK / "_concat_all.txt"
    lines = []
    n = len(rows)
    for i, row in enumerate(rows):
        name = row["name"]
        seg = SEGMENTS / f"seg_{name}.mp4"
        if not seg.exists():
            raise RuntimeError(f"missing segment for {name} -- build it first")

        prev_t = _transition_for((rows[i - 1]["name"], name)) if i > 0 else None
        next_t = _transition_for((name, rows[i + 1]["name"])) if i + 1 < n else None
        start_trim = prev_t["duration"] / 2.0 if prev_t else 0.0
        end_trim = next_t["duration"] / 2.0 if next_t else 0.0

        if start_trim > 0 or end_trim > 0:
            piece = SEGMENTS / f"seg_{name}_trimmed.mp4"
            _trim_piece(seg, start_trim, row["dur"], end_trim, piece)
        else:
            piece = seg
        lines.append(f"file '{piece.resolve()}'")

        if next_t:
            nxt_name = rows[i + 1]["name"]
            trans_path = SEGMENTS / f"trans_{name}_{nxt_name}.mp4"
            if not trans_path.exists():
                if next_t["device"] in ("verse_mask_reveal", "through_object_cut"):
                    a_src, b_src = STILLS / f"{name}.png", STILLS / f"{nxt_name}.png"
                else:
                    a_src, b_src = seg, SEGMENTS / f"seg_{nxt_name}.mp4"
                print(f"[transition] {name} -> {nxt_name}: {next_t['device']} ({next_t['duration']:.2f}s) ...",
                      flush=True)
                tmp = trans_path.with_suffix(".partial.mp4")
                DEV.render_transition(next_t["device"], a_src, b_src, tmp, next_t["duration"],
                                       **next_t["params"])
                tmp.replace(trans_path)  # atomic -- crash-safe cache, same as _trim_piece
            lines.append(f"file '{trans_path.resolve()}'")

    listfile.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-c", "copy", str(out_path)])


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def mux_narration(video_path: Path, out_path: Path, total_dur: float):
    # Each segment builder can land up to ~1 frame short of its target dur
    # (frame-count truncation, e.g. dynamic_cam3d's int(duration*FPS)) --
    # individually negligible, but summed across 76 segments this can drift
    # the concatenated silent video noticeably short of total_dur. -c:v copy
    # can't stretch video to compensate, so INV-26 (video=audio duration)
    # would silently fail. Pad the video with cloned last-frame tpad to
    # close that gap explicitly rather than trusting per-segment precision.
    video_dur = ffprobe_dur(video_path)
    video_deficit = max(0.0, total_dur - video_dur)
    vf = f"tpad=stop_mode=clone:stop_duration={video_deficit:.3f}" if video_deficit > 0.001 else "null"
    tmp = out_path.with_suffix(".partial.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video_path), "-i", str(NARRATION),
         "-filter_complex",
         f"[0:v]{vf}[vout];"
         f"[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
         f"apad=whole_dur={total_dur:.3f}[aout]",
         "-map", "[vout]", "-map", "[aout]", *VCODEC, "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total_dur:.3f}", str(tmp)])
    tmp.replace(out_path)  # atomic -- OUT_CUT only ever appears fully written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="comma-separated spread names to build/rebuild")
    ap.add_argument("--rebuild", action="store_true", help="rebuild segments even if they exist")
    ap.add_argument("--concat-only", action="store_true", help="skip segment build, just join + mux")
    args = ap.parse_args()

    if not WINDOWS.exists():
        print(f"[FATAL] {WINDOWS} not found -- run _s5b_spread_windows.py first")
        sys.exit(1)
    rows = json.loads(WINDOWS.read_text(encoding="utf-8"))
    only = set(args.only.split(",")) if args.only else None

    if not args.concat_only:
        for row in rows:
            if only and row["name"] not in only:
                continue
            seg_path = SEGMENTS / f"seg_{row['name']}.mp4"
            if seg_path.exists() and not args.rebuild:
                print(f"[skip] {row['name']} segment exists")
                continue
            print(f"[build] #{row['num']:02d} {row['name']} mode={row['mode']} dur={row['dur']:.2f}s ...", flush=True)
            build_segment(row, seg_path)
            print(f"   ok -> {seg_path.name}")

    if only:
        print("[done] --only build finished, not concatenating (partial set)")
        return

    total_dur = rows[-1]["end"]
    print(f"[concat] joining {len(rows)} segments, total {total_dur:.2f}s ...")
    concat_segments(rows, OUT_SILENT)
    print(f"[mux] adding narration, padding to {total_dur:.2f}s ...")
    mux_narration(OUT_SILENT, OUT_CUT, total_dur)
    print(f"[done] {OUT_CUT}")


if __name__ == "__main__":
    main()
