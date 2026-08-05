"""Day of Atonement LONG -- step 5b: turn `_spread_table.py`'s
plan-estimated 76 windows + `_alignment.json`'s real forced-aligned word
timings into the one file `_s6_assemble.py` actually reads:
`_spread_windows.json`.

Two corrections applied to the plan's estimated windows:
  1. SEAM SNAP -- every interior (sub-turn) spread boundary is an estimate
     (_PLAN.md sec 1c/2 says so explicitly; only turn-level boundaries are
     ffprobe-hard). Snap each boundary to the start of the nearest real word
     in `_alignment.json`, and print a drift report so anything that moved
     more than 1.5s gets a human look before assembly runs, not after.
  2. FINAL EXTENT -- spread 76 (the landing) is stretched from the last real
     word's end to LAST_WORD_END + LANDING_HOLD_S (INV-26, >=3.0s,
     audio=video). Spread 1 always starts at 0.00.

FILL MODE (how a clip shorter or longer than its window gets stretched to
fill it exactly), given each spread's live clip duration (ffprobe'd fresh,
not hardcoded):

  once_trim  -- clip is >= window: play from its start, trimmed to fit.
  once_hold  -- clip already AT (or extended to) the window duration (the
                deterministic-camera spreads, corrected by
                `_s5c_extend_deterministic.py` for the ones that needed a
                longer render): play as-is, pad any sub-frame remainder by
                holding the last frame.
  fwd_drift  -- clip < window: play the clip forward ONCE at native speed
                (the real licensed motion, exactly as generated -- never
                reversed), then fill the remainder with a $0 deterministic
                camera push/arc (panel_animator/dynamic_cam3d.py) over the
                clip's own LAST FRAME.

REDESIGNED 2026-08-05 after the user watched the first assembled cut and
flagged two real problems, both fixed by removing this project's OWN
pingpong/slow_pingpong/fwd_tail_bounce modes entirely:
  1. "Loads of backwards walking animation" -- any clip with directional
     motion (walking, carrying, leading an animal) read as walking
     BACKWARDS during a pingpong bounce's reverse half. The prior version
     only protected the 2 known "designed acting spread" cases (ONE_WAY);
     the user's report makes clear that was not enough spreads to protect
     -- rather than trying to enumerate every clip with directional motion
     (error-prone, exactly the kind of guessing this project's own
     standing rules warn against), reverse playback is now eliminated
     PROJECT-WIDE. Nothing in this film ever plays backward, full stop.
  2. "Stills that don't have any animation" -- a short clip pingponged many
     times to fill a long window reads as static/repetitive, not real
     motion. fwd_drift replaces that repetition with genuine forward motion
     once, then a real (if gentle) continuing camera move for the rest --
     more alive, and more "creative" than a mechanical bounce loop.

  .venv\\Scripts\\python.exe poc_living_sketchbook/day_of_atonement/_s5b_spread_windows.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _spread_table as ST

CLIPS = HERE / "clips"
STILLS = HERE / "stills"
ALIGNMENT = HERE / "_alignment.json"
OUT = HERE / "_spread_windows.json"

# The 18 spreads animated by the $0 deterministic camera (panel_animator/
# dynamic_cam3d.py push/arc over the untouched still, zero repaint) rather
# than a generative Kling/Seedance clip -- 12 from the original animate
# batch + 6 from the 2026-08-05 user-review fix pass. Never gets a drift
# tail of its own (it IS already a camera move); once_hold/once_trim only.
DETERMINISTIC = {
    "s05_walking_to_veil", "s25_slaying_stage1",
    "s51_jesus_pivot", "s52_jesus_entering_formal", "s53_the_cross",
    "spread54_thread_leaf", "spread55_isaiah536",
    "s56_the_answer", "s57_without_the_gate", "s60_seated_glory",
    "s66_high_priests_face", "s76_already_inside",
    "s26_through_veil_stage2", "s27_sprinkling", "s34_riddle_recap",
    "s45_sign_before_veil", "s50_the_shadow", "s63_torn_veil_card",
}

# Verse-card spreads (name carries "_card") keep the drift tail very gentle
# and push-only -- lettering needs to stay legible/stable, not swept by a
# yawing arc.
DRIFT_AMP_CARD, DRIFT_AMP_DEFAULT = 0.35, 0.5
DRIFT_FOCUS_DEFAULT = (0.50, 0.45)  # generic "slightly above center" bias;
# not hand-tuned per spread (76 of them) the way the 6 punch-list fixes
# were -- reasonable default, not a precision framing decision.


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def nearest_word_start(t: float, words: list) -> float:
    if not words:
        return t
    best = min(words, key=lambda w: abs(w["start"] - t))
    return best["start"] if abs(best["start"] - t) <= 3.0 else t


def _drift_choice(name: str) -> tuple:
    """(move, amp) for the fwd_drift tail. Cards stay push-only/gentle;
    everything else alternates push/arc (stable per-name, not random) for
    some visual variety across 76 spreads rather than the same move on
    every single one."""
    if "_card" in name:
        return "push", DRIFT_AMP_CARD
    move = "push" if sum(ord(c) for c in name) % 2 == 0 else "arc"
    return move, DRIFT_AMP_DEFAULT


def fill_mode(name: str, window_dur: float, clip_dur: float) -> dict:
    if name in DETERMINISTIC:
        drift = window_dur - clip_dur
        if abs(drift) > 0.5:
            print(f"[note] {name}: real aligned window ({window_dur:.2f}s) still differs from "
                  f"its clip's own duration ({clip_dur:.2f}s) by {drift:+.2f}s -- run "
                  f"_s5c_extend_deterministic.py if this is a positive drift not yet corrected.")
        if drift >= 0:
            return {"mode": "once_hold", "clip_dur": clip_dur}
        return {"mode": "once_trim", "clip_dur": clip_dur}
    if clip_dur >= window_dur:
        return {"mode": "once_trim", "clip_dur": clip_dur}
    remainder = window_dur - clip_dur
    if remainder <= 0.5:
        return {"mode": "once_hold", "clip_dur": clip_dur}
    move, amp = _drift_choice(name)
    return {"mode": "fwd_drift", "clip_dur": clip_dur, "tail_s": round(remainder, 3),
            "move": move, "focus": DRIFT_FOCUS_DEFAULT, "amp": amp}


def main():
    words = []
    if ALIGNMENT.exists():
        words = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
        print(f"[align] loaded {len(words)} words from {ALIGNMENT.name}")
    else:
        print(f"[align] WARNING: {ALIGNMENT.name} not found -- using plan-estimated "
              f"windows uncorrected. Re-run after _s5_align.py finishes for real timing.")

    # Snap only the START of each spread (spread 1 always 0.00). Each
    # spread's END is then set to the NEXT spread's start -- never snapped
    # independently -- so consecutive windows share the exact same boundary
    # value with zero gap and zero overlap.
    n = len(ST.SPREADS)
    starts = [0.00] * n
    for i, (num, name, beat, plan_start, plan_end) in enumerate(ST.SPREADS):
        starts[i] = 0.00 if num == 1 else (nearest_word_start(plan_start, words) if words else plan_start)
    last_word_end = max((w["end"] for w in words), default=ST.LAST_WORD_END_ESTIMATE)
    final_end = last_word_end + ST.LANDING_HOLD_S

    rows = []
    drift_report = []
    for i, (num, name, beat, plan_start, plan_end) in enumerate(ST.SPREADS):
        start = starts[i]
        end = starts[i + 1] if i + 1 < n else final_end

        drift = (start - plan_start, end - plan_end)
        if abs(drift[0]) > 1.5 or abs(drift[1]) > 1.5:
            drift_report.append((num, name, drift))

        clip_path = CLIPS / f"{name}.mp4"
        if name in ST.ALWAYS_STATIC_HOLD:
            fm = {"mode": "static_still", "clip_dur": None}
        elif clip_path.exists():
            clip_dur = ffprobe_dur(clip_path)
            fm = fill_mode(name, end - start, clip_dur)
        else:
            fm = {"mode": "MISSING_CLIP", "clip_dur": None}
            print(f"[MISSING] {name}: no clip at {clip_path}")

        rows.append({
            "num": num, "name": name, "beat": beat,
            "start": round(start, 3), "end": round(end, 3),
            "dur": round(end - start, 3),
            **fm,
        })

    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"[out] {len(rows)} spreads -> {OUT}")

    if drift_report:
        print(f"\n[drift] {len(drift_report)} spread(s) with >1.5s seam drift vs plan estimate:")
        for num, name, (ds, de) in drift_report:
            print(f"  #{num:02d} {name}: start {ds:+.2f}s, end {de:+.2f}s")
    else:
        print("\n[drift] none >1.5s" if words else "\n[drift] skipped (no alignment yet)")

    modes = {}
    for r in rows:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    print(f"\n[fill modes] {modes}")


if __name__ == "__main__":
    main()
