"""Comic Page Pipeline POC -- Rung 1 Phase 2, Step 4: draft freeze-lint (CP-G8).

$0, deterministic: decode a clip at 8fps, downscale to 128px wide, gaussian
blur, take the mean abs pixel diff between consecutive frames, and flag any
run of low-diff frames lasting more than 0.8s as a "frozen" (static) stretch.
This is a DRAFT gate -- it reports, it does not block -- but a >2s static run
on an extended (loop-mode) clip should be escalated per the brief.

Threshold is tuned so a KNOWN-GOOD (genuinely, gently animated) clip PASSES
and a STATIC PNG-as-video control clip FAILS. Report both results + the
threshold landed on.

  .venv\\Scripts\\python.exe poc_comic_page/rung1/_freeze_lint_draft.py <clip.mp4> [<clip2.mp4> ...]
"""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

PROBE_FPS = 8
PROBE_W = 128
# tuned below by the calibration run (main()); exposed as a module default so
# other callers can import it once trusted.
DEFAULT_THRESHOLD = 2.0  # mean abs diff (0-255 scale) below this = "frozen" frame-pair
MIN_STATIC_RUN_S = 0.8   # report any run of low-diff frame-pairs >= this long


def _extract_probe_frames(clip: Path, tmpdir: Path) -> list[Path]:
    out_pattern = tmpdir / "p%05d.png"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(clip),
         "-vf", f"fps={PROBE_FPS},scale={PROBE_W}:-1,gblur=sigma=1.2",
         str(out_pattern)],
        check=True, capture_output=True,
    )
    return sorted(tmpdir.glob("p*.png"))


def _mean_abs_diffs(frames: list[Path]) -> list[float]:
    diffs = []
    prev = None
    for fp in frames:
        arr = np.asarray(Image.open(fp).convert("L"), dtype=np.float32)
        if prev is not None:
            diffs.append(float(np.abs(arr - prev).mean()))
        prev = arr
    return diffs


def lint_clip(clip: Path, threshold: float = DEFAULT_THRESHOLD,
              min_static_s: float = MIN_STATIC_RUN_S) -> dict:
    with tempfile.TemporaryDirectory() as td:
        frames = _extract_probe_frames(clip, Path(td))
        if len(frames) < 2:
            return {"clip": str(clip), "result": "ERROR", "detail": "too few frames decoded"}
        diffs = _mean_abs_diffs(frames)

    # find runs of consecutive low-diff frame-pairs
    frame_dt = 1.0 / PROBE_FPS
    runs = []
    run_start = None
    for i, d in enumerate(diffs):
        low = d < threshold
        if low and run_start is None:
            run_start = i
        elif not low and run_start is not None:
            runs.append((run_start, i))
            run_start = None
    if run_start is not None:
        runs.append((run_start, len(diffs)))

    worst_run_s = max(((b - a) * frame_dt for a, b in runs), default=0.0)
    flagged = [(a * frame_dt, b * frame_dt) for a, b in runs if (b - a) * frame_dt >= min_static_s]

    return {
        "clip": str(clip),
        "n_frame_pairs": len(diffs),
        "mean_diff": round(float(np.mean(diffs)), 3),
        "min_diff": round(float(np.min(diffs)), 3),
        "max_diff": round(float(np.max(diffs)), 3),
        "worst_static_run_s": round(worst_run_s, 2),
        "flagged_static_runs": [(round(a, 2), round(b, 2)) for a, b in flagged],
        "result": "FAIL-static" if worst_run_s > 2.0 else ("WARN" if flagged else "PASS"),
    }


def _make_static_control(src_still: Path, out_mp4: Path, seconds: float = 3.0) -> None:
    """3s video made from a single still -- the known-bad control clip."""
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(src_still),
         "-t", str(seconds), "-vf", "scale=540:-2", "-r", "24",
         "-pix_fmt", "yuv420p", str(out_mp4)],
        check=True, capture_output=True,
    )


def calibrate(known_good: Path, still_for_control: Path, workdir: Path) -> float:
    """Try a small set of candidate thresholds; pick the smallest that still
    PASSes the known-good clip AND FAILs (flags a run) the static control."""
    control = workdir / "_static_control.mp4"
    _make_static_control(still_for_control, control)
    print(f"[calib] static control clip -> {control}")

    candidates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    chosen = None
    for th in candidates:
        good = lint_clip(known_good, threshold=th)
        bad = lint_clip(control, threshold=th)
        good_pass = good["result"] in ("PASS", "WARN")
        bad_fail = bad["result"] == "FAIL-static" or bool(bad["flagged_static_runs"])
        print(f"  th={th:>4}  known-good={good['result']:<11} static-control={bad['result']:<11}"
              f"  (good worst_run={good['worst_static_run_s']}s, control worst_run={bad['worst_static_run_s']}s)")
        if good_pass and bad_fail and chosen is None:
            chosen = th
    return chosen if chosen is not None else DEFAULT_THRESHOLD


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    clips = [Path(a) for a in sys.argv[1:]]
    workdir = clips[0].parent
    still = Path("poc_comic_page/rung1/stills/panel_a_jesus.png")

    # calibrate against the first clip as "known-good" + a fresh static control
    threshold = calibrate(clips[0], still, workdir)
    print(f"\n[threshold landed on] {threshold}\n")

    print(f"{'clip':40} {'result':10} {'mean_diff':>10} {'worst_static_run_s':>20} flagged_runs")
    for c in clips:
        r = lint_clip(c, threshold=threshold)
        print(f"{Path(r['clip']).name:40} {r['result']:10} {r.get('mean_diff', ''):>10} "
              f"{r.get('worst_static_run_s', ''):>20} {r.get('flagged_static_runs', [])}")


if __name__ == "__main__":
    main()
