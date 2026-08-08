"""Seed of the Woman LONG -- step 5b: write the real `_spread_windows.json`
that panel_animator/motion_lint.py actually reads (SKILL.md sec.8b gate #3).
The prior file was a leftover from the 5-spread POC30 promotion (stale
durations, a generic "device" mode string that collided with motion_lint's
device-quota tally) -- this regenerates it from the CURRENT `_spread_table.py`
+ whatever segments actually exist in `_segments/`, covering every spread
built so far (not just spreads 1-N contiguous -- s51 is out of table order).

Mode per spread:
  - a real Kling/Seedance clip (has clips/<name>.mp4): once_trim if the clip
    is >= its window, once_hold if the remainder is tiny, fwd_drift otherwise
    (mirrors day_of_atonement/_s5b_spread_windows.py's fill_mode(), no
    DETERMINISTIC set here -- this episode has none yet).
  - a $0 device spread: the literal device name from _devices.py's
    DEVICE_ASSIGNMENTS if present, else "verse_card" (VERSE_CARDS
    membership) or "bespoke" (neither table has an entry -- s01/s05, whose
    hold is hand-built without a DEVICE_ASSIGNMENTS row).

  .venv\\Scripts\\python.exe poc_living_sketchbook/seed_of_the_woman/_s5b_spread_windows.py
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _spread_table as ST  # noqa: E402
import _devices as DV  # noqa: E402

CLIPS = HERE / "clips"
SEG_DIR = HERE / "_segments"
OUT = HERE / "_spread_windows.json"


def ffprobe_dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def fill_mode(window_dur: float, clip_dur: float) -> tuple[str, float]:
    if clip_dur >= window_dur:
        return "once_trim", clip_dur
    remainder = window_dur - clip_dur
    if remainder <= 0.5:
        return "once_hold", clip_dur
    return "fwd_drift", clip_dur


def device_mode(name: str) -> str:
    entry = DV.DEVICE_ASSIGNMENTS.get(name)
    if entry is not None:
        return entry["device"]
    if name in DV.VERSE_CARDS:
        return "verse_card"
    return "bespoke"


def main():
    rows = []
    for num, name, beat, start, end in ST.SPREADS:
        seg = SEG_DIR / f"seg_{name}.mp4"
        if not seg.exists():
            continue  # not built yet -- omit rather than fake a row
        dur = round(end - start, 3)
        clip = CLIPS / f"{name}.mp4"
        if clip.exists():
            clip_dur = ffprobe_dur(clip)
            mode, clip_dur = fill_mode(dur, clip_dur)
        else:
            mode, clip_dur = device_mode(name), None
        rows.append({"num": num, "name": name, "beat": beat,
                      "start": round(start, 3), "end": round(end, 3),
                      "dur": dur, "mode": mode, "clip_dur": clip_dur})

    OUT.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(f"[out] {len(rows)} built spreads -> {OUT}")
    modes = {}
    for r in rows:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    print(f"[modes] {modes}")


if __name__ == "__main__":
    main()
