#!/usr/bin/env python
"""Motion Lint -- the standing $0 QC gate for a long-form episode's finishing
pass (Fable Round 10, `poc_living_sketchbook/_FABLE_ROUND10_MOTION_FRESHNESS_
PIPELINE.md`). Built after the Day of Atonement rollout shipped with 21 of 76
spreads on Raking Light (28%) -- a systematic "frozen still" problem only the
user watching all 10 minutes caught. This gate measures every finished
segment BEFORE a human has to.

Metric: sample each segment at 3fps via ffmpeg, compute mean absolute
luminance difference between consecutive samples, report per-segment MEAN
(the energy signal) and P95 (the freshness/arrival-event signal -- a verse
card whose only motion is three big text presses scores near-zero on a naive
mean but its p95 catches the press events).

No LLM, no spend -- ffmpeg + numpy only. Fail-closed: an unreadable segment
is a suspect segment, never silently skipped.

Usage:
    python motion_lint.py --episode-dir <dir> [--calibrate] [--windows <path>]
        [--devices-module <path>] [--out <report.md>]

  --calibrate  prints the raw score distribution (with device labels where
               available) instead of running checks -- use this FIRST on a
               new episode to set T_frozen per class, then hardcode the
               thresholds into DEFAULT_THRESHOLDS below (or pass --thresholds
               <json>) for the real run. Every real report states which
               thresholds it used, so lineage is never silently stale.

Exit code 1 on any FAIL (never on WARN-only).
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
import io

FPS_SAMPLE = 3
# GOTCHA (found 2026-08-08, Seed of the Woman s26 tuning): at 3fps, sample
# points are 0.333s apart. A device whose real motion window is SHORTER
# than ~1s can land well or badly on this sparse grid almost by chance --
# tuning stroke_width/duration against a p95 that swung 0.069 -> 0.102 ->
# 0.048 as changes got "bigger" turned out to be sampling aliasing, not a
# real signal. If a device isn't clearing threshold and small parameter
# bumps produce non-monotonic p95, suspect this FIRST: widen the device's
# own active-motion window to >=1s (several sample points reliably land
# inside it) before spending more time on stroke/amplitude tuning.
STATIC_RUN_LEN = 2  # 2+ consecutive spreads at/below WARN level -> FAIL
FROZEN_MIN_DUR = 5.0  # dur >= this -> FROZEN-SPREAD (FAIL); below -> FROZEN-SHORT (WARN)
QUOTA_WARN, QUOTA_FAIL = 0.10, 0.15
QUOTA_FULLSCOPE_FAIL = 0.08

# RES-MISMATCH: catches a device wrapper silently rendering at its still's own
# native resolution instead of the film's frame (the real parallax_25d bug
# that survived 10 spreads in Day of Atonement before anyone noticed -- see
# memory `day-of-atonement-retro-learnings` fix #3). Checked per-segment
# alongside the freshness score, not a separate pass.
DEFAULT_EXPECT_RES = (1920, 1080, 30.0)
FPS_TOLERANCE = 0.5

# Calibrated 2026-08-06 against the Day of Atonement 76-segment set, PRE-FIX
# (see _FABLE_ROUND10...md sec 3d). The real distribution shows a clean,
# isolated cluster of 11 segments at p95<=0.036 (exactly the spreads
# independently flagged as truly frozen in the round-10 disposition table --
# s52/s51/s60/s53/s05/s63/s25/s27/s50/s26), then a sharp jump to 0.259 for
# the next entry (a real Kling clip, correctly NOT frozen) and everything
# else. Thresholds set strictly between the two clusters, per class --
# "narrative" = ordinary NS/MV spreads; "card" = verse-card spreads.
# Deliberately loose (this gate catches the WORST systemic offenders, not
# every quality nit -- see the disposition table for spreads like s34/s57
# that score fine here but still get a glue-fix for a different reason; the
# lint is the floor, not the ceiling). Values are P95 of per-frame
# mean-abs-luminance-diff (0..255 scale).
DEFAULT_THRESHOLDS = {
    "narrative": 0.15,
    "card": 0.10,
}


def _lookup_entry(name: str, devices_mod):
    """A spread's device entry may live in DEVICE_ASSIGNMENTS or, for a
    bespoke non-combo card (verse-mask/settle/etc.), SPECIAL_CARDS -- check
    both so stillness_authored and other flags are honored regardless of
    which table actually holds the spread."""
    if devices_mod is None:
        return None
    entry = getattr(devices_mod, "DEVICE_ASSIGNMENTS", {}).get(name)
    if entry is not None:
        return entry
    return getattr(devices_mod, "SPECIAL_CARDS", {}).get(name)


def _class_of(name: str, devices_mod) -> str:
    if devices_mod is not None and name in getattr(devices_mod, "VERSE_CARDS", {}):
        return "card"
    if "_card" in name:
        return "card"
    return "narrative"


def sample_luminance_series(seg_path: Path, fps: int = FPS_SAMPLE) -> np.ndarray | None:
    """Returns an array of per-frame mean luminance (0..255), sampled at
    `fps`. None on extraction failure (caller must treat as FAIL, not skip)."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(seg_path), "-vf", f"fps={fps},format=gray",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "csv=s=x:p=0", str(seg_path)],
        capture_output=True, text=True)
    if probe.returncode != 0 or not probe.stdout.strip():
        return None
    try:
        w, h = (int(x) for x in probe.stdout.strip().split("x"))
    except ValueError:
        return None
    frame_bytes = w * h
    if frame_bytes == 0 or len(r.stdout) % frame_bytes != 0:
        return None
    n = len(r.stdout) // frame_bytes
    if n < 2:
        return None
    arr = np.frombuffer(r.stdout, dtype=np.uint8).reshape(n, h, w).astype(np.float32)
    return arr.mean(axis=(1, 2))  # per-frame mean luminance


def probe_resolution_fps(seg_path: Path) -> tuple[int, int, float] | None:
    """(width, height, fps) of a segment's video stream, or None if unreadable."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,avg_frame_rate", "-of", "csv=s=x:p=0", str(seg_path)],
        capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        w_s, h_s, fps_s = r.stdout.strip().split("x")
        num, den = fps_s.split("/")
        fps = float(num) / float(den) if float(den) != 0 else 0.0
        return int(w_s), int(h_s), fps
    except (ValueError, ZeroDivisionError):
        return None


def score_segment(seg_path: Path) -> dict | None:
    """Returns {"mean": float, "p95": float, "n_frames": int} of the
    frame-to-frame luminance-diff series, or None on extraction failure."""
    series = sample_luminance_series(seg_path)
    if series is None:
        return None
    diffs = np.abs(np.diff(series))
    if len(diffs) == 0:
        return {"mean": 0.0, "p95": 0.0, "n_frames": len(series)}
    return {"mean": float(diffs.mean()), "p95": float(np.percentile(diffs, 95)),
            "n_frames": len(series)}


def load_devices_module(path: Path):
    if path is None:
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location("_episode_devices", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(mod)
    return mod


def device_share_table(rows: list, devices_mod) -> dict:
    """signature -> {"count": int, "full_count": int, "names": [...]}"""
    shares = {}
    for row in rows:
        name = row["name"]
        entry = None
        if devices_mod is not None:
            entry = getattr(devices_mod, "DEVICE_ASSIGNMENTS", {}).get(name)
        sig = entry["device"] if entry else ("verse_card" if devices_mod and name in
                                              getattr(devices_mod, "VERSE_CARDS", {}) else row.get("mode", "unknown"))
        d = shares.setdefault(sig, {"count": 0, "full_count": 0, "names": []})
        d["count"] += 1
        d["names"].append(name)
        if entry and entry.get("scope") == "full":
            d["full_count"] += 1
    return shares


def find_transitions_table(devices_mod):
    if devices_mod is None:
        return {}, set()
    return getattr(devices_mod, "TRANSITION_OVERRIDES", {}), getattr(devices_mod, "NO_TRANSITION_SEAMS", set())


def run_calibrate(rows: list, segments_dir: Path, devices_mod):
    print(f"[calibrate] sampling {len(rows)} segments at {FPS_SAMPLE}fps ...\n")
    out = []
    for row in rows:
        name = row["name"]
        seg = segments_dir / f"seg_{name}.mp4"
        if not seg.exists():
            print(f"  {name:35s}  MISSING SEGMENT")
            continue
        s = score_segment(seg)
        cls = _class_of(name, devices_mod)
        entry = getattr(devices_mod, "DEVICE_ASSIGNMENTS", {}).get(name) if devices_mod else None
        sig = entry["device"] if entry else "-"
        if s is None:
            print(f"  {name:35s}  EXTRACT-ERROR  class={cls:10s} device={sig}")
            continue
        out.append((s["p95"], name, cls, sig, s["mean"]))
    out.sort()
    print(f"\n{'p95':>7}  {'mean':>7}  {'class':10s}  {'device':22s}  name")
    for p95, name, cls, sig, mean in out:
        print(f"{p95:7.3f}  {mean:7.3f}  {cls:10s}  {sig:22s}  {name}")
    print("\n[calibrate] Set DEFAULT_THRESHOLDS in motion_lint.py per class from this "
          "distribution -- pick T_frozen just above the known-frozen cluster and below "
          "the known-alive cluster, then re-run without --calibrate.")


def run_lint(rows: list, segments_dir: Path, devices_mod, thresholds: dict, out_path: Path,
             expect_res: tuple[int, int, float] = DEFAULT_EXPECT_RES) -> int:
    findings = []
    scores = {}
    exp_w, exp_h, exp_fps = expect_res
    for row in rows:
        name = row["name"]
        seg = segments_dir / f"seg_{name}.mp4"
        cls = _class_of(name, devices_mod)
        entry = _lookup_entry(name, devices_mod)
        whitelisted = bool(entry and entry.get("stillness_authored"))  # explicit key, never inferred
        if not seg.exists():
            findings.append(("FAIL", "MISSING-SEGMENT", name, f"no segment file at {seg}"))
            continue
        s = score_segment(seg)
        if s is None:
            findings.append(("FAIL", "EXTRACT-ERROR", name,
                              "ffmpeg/ffprobe could not read this segment -- fail-closed, not skipped"))
            continue
        scores[name] = s
        res = probe_resolution_fps(seg)
        if res is None:
            findings.append(("FAIL", "RES-MISMATCH", name, "could not read resolution/fps"))
        else:
            w, h, fps = res
            if w != exp_w or h != exp_h or abs(fps - exp_fps) > FPS_TOLERANCE:
                findings.append(("FAIL", "RES-MISMATCH", name,
                                  f"{w}x{h}@{fps:.2f} != expected {exp_w}x{exp_h}@{exp_fps:.0f}"))
        if entry and entry.get("placeholder"):
            findings.append(("FAIL", "PLACEHOLDER", name,
                              f"device table still has placeholder:True for {name}"))
        if whitelisted:
            continue
        t = thresholds.get(cls, thresholds.get("narrative"))
        dur = row.get("dur", 0.0)
        if s["p95"] < t:
            if dur >= FROZEN_MIN_DUR:
                findings.append(("FAIL", "FROZEN-SPREAD", name,
                                  f"p95={s['p95']:.3f} < T_frozen({cls})={t}, dur={dur:.1f}s"))
            else:
                findings.append(("WARN", "FROZEN-SHORT", name,
                                  f"p95={s['p95']:.3f} < T_frozen({cls})={t}, dur={dur:.1f}s (short, WARN only)"))

    # STATIC-RUN: 2+ consecutive spreads both at/below WARN-level (p95 < threshold), non-whitelisted
    below = []
    for row in rows:
        name = row["name"]
        entry = _lookup_entry(name, devices_mod)
        if entry and entry.get("stillness_authored"):
            below.append(False)
            continue
        s = scores.get(name)
        cls = _class_of(name, devices_mod)
        t = thresholds.get(cls, thresholds.get("narrative"))
        below.append(bool(s and s["p95"] < t))
    run_start = None
    for i, b in enumerate(below + [False]):
        if b and run_start is None:
            run_start = i
        elif not b and run_start is not None:
            if i - run_start >= STATIC_RUN_LEN:
                names = [rows[j]["name"] for j in range(run_start, i)]
                findings.append(("FAIL", "STATIC-RUN", "/".join(names),
                                  f"{len(names)} consecutive low-motion spreads with no relief"))
            run_start = None

    # DEVICE-QUOTA
    shares = device_share_table(rows, devices_mod)
    n = len(rows)
    for sig, d in shares.items():
        share = d["count"] / n
        full_share = d["full_count"] / n
        if share > QUOTA_FAIL:
            findings.append(("FAIL", "DEVICE-QUOTA", sig,
                              f"{d['count']}/{n} = {share:.1%} > 15% FAIL threshold"))
        elif share > QUOTA_WARN:
            findings.append(("WARN", "DEVICE-QUOTA", sig,
                              f"{d['count']}/{n} = {share:.1%} > 10% WARN threshold"))
        if full_share > QUOTA_FULLSCOPE_FAIL:
            findings.append(("FAIL", "DEVICE-QUOTA-FULLSCOPE", sig,
                              f"{d['full_count']}/{n} = {full_share:.1%} full-scope > 8% FAIL threshold"))

    # MOTION-CLIFF: outgoing tail high-motion, incoming head low-motion, transition == unseen_hand
    trans_overrides, no_trans = find_transitions_table(devices_mod)
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        seam = (a["name"], b["name"])
        if seam in no_trans:
            continue
        t_entry = trans_overrides.get(seam)
        device = t_entry["device"] if t_entry else "unseen_hand"
        if device != "unseen_hand":
            continue
        sa, sb = scores.get(a["name"]), scores.get(b["name"])
        if not sa or not sb:
            continue
        cls_b = _class_of(b["name"], devices_mod)
        t_b = thresholds.get(cls_b, thresholds.get("narrative"))
        if sa["p95"] >= 2 * t_b and sb["p95"] < t_b:
            findings.append(("WARN", "MOTION-CLIFF", f"{a['name']} -> {b['name']}",
                              f"outgoing p95={sa['p95']:.2f} vs incoming p95={sb['p95']:.2f} "
                              f"(T={t_b}), unseen_hand transition -- consider escalating"))

    lines = ["# Motion Lint Report", "",
             f"Thresholds used: {json.dumps(thresholds)}",
             f"Segments analyzed: {len(rows)}", ""]
    fails = [f for f in findings if f[0] == "FAIL"]
    warns = [f for f in findings if f[0] == "WARN"]
    lines.append(f"**{len(fails)} FAIL, {len(warns)} WARN**")
    lines.append("")
    for sev, check, subject, detail in sorted(findings, key=lambda f: (f[0] != "FAIL", f[1])):
        lines.append(f"- **[{sev}] {check}** `{subject}` -- {detail}")
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"[motion_lint] {len(fails)} FAIL, {len(warns)} WARN -> {out_path}")
    for sev, check, subject, detail in findings:
        print(f"  [{sev}] {check:22s} {subject:40s} {detail}")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode-dir", required=True, type=Path)
    ap.add_argument("--windows", default=None, help="defaults to <episode-dir>/_spread_windows.json")
    ap.add_argument("--devices-module", default=None, help="defaults to <episode-dir>/_devices.py")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--out", default=None, help="defaults to <episode-dir>/_motion_lint_report.md")
    ap.add_argument("--thresholds", default=None, help="JSON string overriding DEFAULT_THRESHOLDS")
    ap.add_argument("--expect", default="1920x1080@30",
                     help="expected WxH@FPS for every segment (RES-MISMATCH check)")
    args = ap.parse_args()

    ep = args.episode_dir
    windows_path = Path(args.windows) if args.windows else ep / "_spread_windows.json"
    devices_path = Path(args.devices_module) if args.devices_module else ep / "_devices.py"
    segments_dir = ep / "_segments"
    out_path = Path(args.out) if args.out else ep / "_motion_lint_report.md"

    if not windows_path.exists():
        print(f"[FATAL] {windows_path} not found"); sys.exit(1)
    rows = json.loads(windows_path.read_text(encoding="utf-8"))
    devices_mod = load_devices_module(devices_path) if devices_path.exists() else None
    if devices_mod is None:
        print(f"[warn] no devices module at {devices_path} -- quota/placeholder/cliff checks limited")

    if args.calibrate:
        run_calibrate(rows, segments_dir, devices_mod)
        return

    thresholds = json.loads(args.thresholds) if args.thresholds else DEFAULT_THRESHOLDS
    res_part, fps_part = args.expect.split("@")
    exp_w, exp_h = (int(x) for x in res_part.split("x"))
    expect_res = (exp_w, exp_h, float(fps_part))
    code = run_lint(rows, segments_dir, devices_mod, thresholds, out_path, expect_res)
    sys.exit(code)


if __name__ == "__main__":
    main()
