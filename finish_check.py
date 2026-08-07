#!/usr/bin/env python
"""finish_check.py -- the $0 "definition of done" gate for a living-sketchbook
LONG episode. Born from the Day of Atonement retrospective: the film was
declared "locked" while it still had no score/SFX/captions/watermark at all
-- an entire standard finishing chain silently missing, despite Bronze
Serpent LONG having already established that exact chain days earlier
(memory `day-of-atonement-retro-learnings` fix #5). This script asserts the
full artifact chain actually exists, IN ORDER, and refuses to pass on the
first missing/wrong stage -- run it before ever telling the user an episode
is done.

Chain checked, in order:
  1. <STEM>.mp4                    -- the base (silent-narration-only) cut
  2. <STEM>_scored.mp4              -- music added, has audio, duration >= base
  3. <STEM>_scored_sfx.mp4          -- SFX bed added, duration matches scored
  4. <STEM>_cc.mp4                  -- captions added, duration matches sfx
  5. watermark                      -- <STEM>_cc.prewm.bak.mp4 exists (the
                                        pre-watermark original add_watermark.py
                                        keeps) and is not newer than _cc.mp4
  6. INV-26 landing hold            -- final video/audio duration within 0.3s;
                                        if --alignment is given, both also
                                        >= last spoken word + 3.0s
  7. motion_lint clean              -- _motion_lint_report.md exists, states
                                        0 FAIL, and is newer than every
                                        _segments/*.mp4 (not stale)

Usage:
    python finish_check.py --episode-dir <dir> --stem <STEM> [--alignment <alignment.json>]

Exit code 1 naming the first failing stage; 0 (silent chain, one summary
line) if every stage passes.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

DUR_TOLERANCE = 0.05
INV26_AV_TOLERANCE = 0.3
INV26_MIN_HOLD = 3.0


def ffprobe_streams(path: Path) -> dict | None:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
         "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def duration(path: Path, stream_type: str | None = None) -> float | None:
    j = ffprobe_streams(path)
    if j is None:
        return None
    if stream_type is None:
        try:
            return float(j["format"]["duration"])
        except (KeyError, ValueError):
            return None
    for s in j.get("streams", []):
        if s.get("codec_type") == stream_type:
            try:
                return float(s["duration"])
            except (KeyError, ValueError, TypeError):
                continue
    return None


def fail(stage: str, detail: str) -> None:
    print(f"[finish_check] FAIL at stage {stage}: {detail}")
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode-dir", required=True, type=Path)
    ap.add_argument("--stem", required=True, help="e.g. DAYOFATONEMENT_LONG_living_sketchbook")
    ap.add_argument("--alignment", default=None, type=Path,
                     help="path to _alignment.json, for the last-word +3.0s hold check")
    args = ap.parse_args()
    ep = args.episode_dir
    stem = args.stem

    base = ep / f"{stem}.mp4"
    scored = ep / f"{stem}_scored.mp4"
    sfx = ep / f"{stem}_scored_sfx.mp4"
    cc = ep / f"{stem}_cc.mp4"
    bak = ep / f"{stem}_cc.prewm.bak.mp4"

    # 1. base cut
    if not base.exists():
        fail("1-base", f"missing {base} -- run the assembly stage")
    base_dur = duration(base)
    if base_dur is None:
        fail("1-base", f"{base} exists but is unreadable")
    print(f"  [ok] 1-base       {base.name} ({base_dur:.1f}s)")

    # 2. scored
    if not scored.exists():
        fail("2-scored", f"missing {scored} -- run the score stage")
    scored_dur = duration(scored)
    scored_audio = duration(scored, "audio")
    if scored_dur is None or scored_audio is None:
        fail("2-scored", f"{scored} missing a readable audio stream")
    if scored_dur < base_dur - DUR_TOLERANCE:
        fail("2-scored", f"{scored_dur:.2f}s is shorter than base {base_dur:.2f}s")
    print(f"  [ok] 2-scored     {scored.name} ({scored_dur:.1f}s)")

    # 3. sfx
    if not sfx.exists():
        fail("3-sfx", f"missing {sfx} -- run the SFX stage")
    sfx_dur = duration(sfx)
    if sfx_dur is None:
        fail("3-sfx", f"{sfx} exists but is unreadable")
    if abs(sfx_dur - scored_dur) > DUR_TOLERANCE:
        fail("3-sfx", f"{sfx_dur:.2f}s != scored {scored_dur:.2f}s (tolerance {DUR_TOLERANCE}s)")
    print(f"  [ok] 3-sfx        {sfx.name} ({sfx_dur:.1f}s)")

    # 4. captions
    if not cc.exists():
        fail("4-captions", f"missing {cc} -- run the captions stage")
    cc_dur = duration(cc)
    if cc_dur is None:
        fail("4-captions", f"{cc} exists but is unreadable")
    if abs(cc_dur - sfx_dur) > DUR_TOLERANCE:
        fail("4-captions", f"{cc_dur:.2f}s != sfx {sfx_dur:.2f}s (tolerance {DUR_TOLERANCE}s)")
    print(f"  [ok] 4-captions   {cc.name} ({cc_dur:.1f}s)")

    # 5. watermark
    if not bak.exists():
        fail("5-watermark", f"missing {bak} -- run add_watermark.py on {cc}")
    if cc.stat().st_mtime < bak.stat().st_mtime:
        fail("5-watermark", f"{cc.name} is OLDER than its own backup {bak.name} "
                             "-- looks like the backup exists but watermarking didn't complete")
    print(f"  [ok] 5-watermark  {bak.name} present, {cc.name} is newer")

    # 6. INV-26 landing hold
    cc_v = duration(cc, "video")
    cc_a = duration(cc, "audio")
    if cc_v is None or cc_a is None:
        fail("6-inv26", f"{cc} missing a readable video or audio stream")
    if abs(cc_v - cc_a) > INV26_AV_TOLERANCE:
        fail("6-inv26", f"video {cc_v:.2f}s vs audio {cc_a:.2f}s differ by "
                         f">{INV26_AV_TOLERANCE}s")
    if args.alignment:
        if not args.alignment.exists():
            fail("6-inv26", f"--alignment given but not found: {args.alignment}")
        words = json.loads(args.alignment.read_text(encoding="utf-8"))
        last_word_end = max(w["end"] for w in words)
        min_total = last_word_end + INV26_MIN_HOLD
        if cc_v < min_total - DUR_TOLERANCE or cc_a < min_total - DUR_TOLERANCE:
            fail("6-inv26", f"hold after last word ({last_word_end:.2f}s) is "
                             f"{min(cc_v, cc_a) - last_word_end:.2f}s < required {INV26_MIN_HOLD}s")
    print(f"  [ok] 6-inv26      video {cc_v:.2f}s / audio {cc_a:.2f}s "
          f"(diff {abs(cc_v - cc_a):.3f}s)")

    # 7. motion_lint clean and fresh
    lint_report = ep / "_motion_lint_report.md"
    if not lint_report.exists():
        fail("7-motion_lint", f"missing {lint_report} -- run panel_animator/motion_lint.py")
    segments_dir = ep / "_segments"
    if segments_dir.is_dir():
        newest_seg_mtime = max((f.stat().st_mtime for f in segments_dir.glob("*.mp4")), default=0.0)
        if lint_report.stat().st_mtime < newest_seg_mtime:
            fail("7-motion_lint", f"{lint_report.name} is STALE -- older than the newest "
                                   f"segment in {segments_dir}; re-run motion_lint.py")
    report_text = lint_report.read_text(encoding="utf-8")
    if "**0 FAIL" not in report_text:
        first_line = next((ln for ln in report_text.splitlines() if ln.startswith("**")), "")
        fail("7-motion_lint", f"report does not state 0 FAIL: {first_line or '(no summary line found)'}")
    print(f"  [ok] 7-motion_lint {lint_report.name} is fresh and states 0 FAIL")

    print(f"[finish_check] ALL 7 STAGES PASS -- {stem} is genuinely finished.")


if __name__ == "__main__":
    main()
