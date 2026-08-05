"""Day of Atonement LONG -- step 6: SIMPLE FIRST CUT. Turns
`_spread_windows.json` (76 spreads, each with a resolved fill mode) into one
silent 1920x1080@30fps video, then muxes the real locked narration on top
with the INV-26 landing hold. Hard cuts between spreads (no crossfade/
page-turn devices) -- those are a deliberate polish-pass-2 layer added AFTER
this base cut is seen and approved, exactly mirroring
`bronze_serpent_long/_s7_assemble.py`'s own "simple first, polish after"
discipline. Nothing here is generative -- every segment is built by ffmpeg
trim/loop/reverse/concat over already-approved clips.

This hard-cut-only concat also satisfies _PLAN.md's own "multi-stage
hard-cut PAIRS" requirement (10/11 strange fire, 25/26/27 slaying through
the veil, 61/62 whole-veil->torn) for free -- there is no dissolve/blend
mode in this recipe at all, so every seam in the film is already a hard cut.

Fill modes (resolved per-spread in `_spread_windows.json` by
`_s5b_spread_windows.py`):
  once_trim    -- clip is >= window: play from its start, trimmed to fit.
  once_hold    -- clip already AT (or held to) the window duration (the 18
                  deterministic-camera spreads): play as-is, pad any
                  sub-frame remainder by holding the last frame (ffmpeg tpad).
  pingpong     -- clip < window <= 15s: native-speed forward+reverse bounce,
                  looped to fill exactly.
  slow_pingpong-- clip < window, window > 15s: same bounce, slowed so ONE
                  cycle spans (most of) the window -- a single reverent
                  drift, not a fast flicker.
  fwd_tail_bounce -- directional completing motion (the 2 acting spreads,
                  see _s5b's ONE_WAY set): play the clip forward ONCE at
                  native speed (so the real gesture is seen the right way
                  round), then fill the remainder by bouncing only a short
                  CALM TAIL -- never a full-clip reverse.
  static_still -- unused this episode (ST.ALWAYS_STATIC_HOLD is empty; every
                  spread has a real clip) -- kept for interface parity with
                  bronze_serpent_long in case a future rebuild needs it.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py                 # full 76-spread build
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py --only s01_cold_open,s76_already_inside   # test gate
  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s6_assemble.py --concat-only   # (re)join existing segments + mux audio
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
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


def build_bounce_cycle(src: Path, out: Path, speed_factor: float = 1.0):
    """One forward+reverse cycle of `src`, optionally slowed by speed_factor
    (>1 = slower). Native speed when speed_factor==1.0."""
    if speed_factor and speed_factor != 1.0:
        vf_pre = f"setpts={speed_factor}*PTS,"
    else:
        vf_pre = ""
    filt = (f"[0:v]{vf_pre}split[a][b];[b]reverse[r];"
            f"[a][r]concat=n=2:v=1:a=0,{SCALE_CROP}[out]")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
         "-filter_complex", filt, "-map", "[out]", *VCODEC, str(out)])


def loop_to_duration(src: Path, out: Path, target_dur: float):
    cycle_dur = ffprobe_dur(src)
    n_loops = max(1, int((target_dur // cycle_dur) + 2))
    run(["ffmpeg", "-y", "-v", "error", "-stream_loop", str(n_loops), "-i", str(src),
         "-t", f"{target_dur:.3f}", *VCODEC, str(out)])


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def build_segment(row: dict, seg_path: Path):
    name = row["name"]
    dur = row["dur"]
    mode = row["mode"]
    clip = CLIPS / f"{name}.mp4"

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

    if mode == "pingpong":
        cyc = WORK / f"{name}_cycle.mp4"
        build_bounce_cycle(clip, cyc)
        loop_to_duration(cyc, seg_path, dur)
        return

    if mode == "slow_pingpong":
        cyc = WORK / f"{name}_cycle.mp4"
        build_bounce_cycle(clip, cyc, speed_factor=row["factor"])
        loop_to_duration(cyc, seg_path, dur)
        return

    if mode == "fwd_tail_bounce":
        clip_dur = row["clip_dur"]
        tail_s = row["tail_s"]
        remainder = max(0.0, dur - clip_dur)
        fwd = WORK / f"{name}_fwd.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(clip), "-vf", SCALE_CROP,
             *VCODEC, str(fwd)])
        if remainder <= 0.05:
            seg_path.write_bytes(fwd.read_bytes())
            return
        tail_src = WORK / f"{name}_tailsrc.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-sseof", f"-{tail_s:.3f}", "-i", str(clip),
             "-vf", SCALE_CROP, *VCODEC, str(tail_src)])
        cyc = WORK / f"{name}_tailcycle.mp4"
        build_bounce_cycle(tail_src, cyc)
        tail_filled = WORK / f"{name}_tailfilled.mp4"
        loop_to_duration(cyc, tail_filled, remainder)
        # concat fwd + tail_filled
        listfile = WORK / f"{name}_concat.txt"
        listfile.write_text(f"file '{fwd.resolve()}'\nfile '{tail_filled.resolve()}'\n", encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
             *VCODEC, str(seg_path)])
        return

    raise ValueError(f"{name}: unknown/unresolved fill mode {mode!r}")


def concat_segments(rows: list, out_path: Path):
    listfile = WORK / "_concat_all.txt"
    lines = []
    for row in rows:
        seg = SEGMENTS / f"seg_{row['name']}.mp4"
        if not seg.exists():
            raise RuntimeError(f"missing segment for {row['name']} -- build it first")
        lines.append(f"file '{seg.resolve()}'")
    listfile.write_text("\n".join(lines) + "\n", encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-c", "copy", str(out_path)])


def mux_narration(video_path: Path, out_path: Path, total_dur: float):
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video_path), "-i", str(NARRATION),
         "-filter_complex", f"[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
                             f"apad=whole_dur={total_dur:.3f}[aout]",
         "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total_dur:.3f}", str(out_path)])


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
