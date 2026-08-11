"""Drawing Office -- The Father Who Ran. Final assembly: 13 real animated
clips (0 static holds), each trimmed to its exact word-timed beat window,
concatenated, muxed with the real narration.mp3. No score/SFX/captions --
explicitly out of scope for this pass (narration + animated visuals only).
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIPS = HERE / "clips"
TRIMMED = HERE / "trimmed"
TRIMMED.mkdir(exist_ok=True)

sys.path.insert(0, str(HERE.parents[1] / "primitives"))
from compose import normalize_and_concat, mux_with_landing_hold  # noqa: E402

NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\09 The Father Who Ran\v1\narration.mp3"
)
LAST_WORD_END = 59.84
OUTRO_HOLD = 3.0

# (clip filename, duration to trim to -- real word-timed beat windows)
SEGMENTS = [
    ("slot1_walk.mp4", 5.30),
    ("slot2_run_flash.mp4", 2.94),
    ("slot3_watching.mp4", 4.56),
    ("slot4_feet_pound.mp4", 6.20),
    ("slot5_rehearsing.mp4", 4.30),
    ("slot6_great_way_off.mp4", 6.06),
    ("slot7_the_run.mp4", 4.14),
    ("slot8_arrival.mp4", 4.00),
    ("slot9_fists_unclench.mp4", 5.50),
    ("slot10_open_hand.mp4", 5.00),
    ("slot11_watcher_becomes_runner.mp4", 3.50),
    ("slot12_christ_walking.mp4", 5.50),
    ("slot13_landing.mp4", 5.84),
]


def trim_clip(src: Path, dur: float, out: Path) -> Path:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-t", f"{dur:.3f}",
         "-c", "copy", "-avoid_negative_ts", "make_zero", str(out)],
        check=True, capture_output=True,
    )
    return out


if __name__ == "__main__":
    print("trimming 13 clips to their exact beat windows...")
    trimmed_paths = []
    total = 0.0
    for name, dur in SEGMENTS:
        src = CLIPS / name
        out = TRIMMED / name
        if not out.exists():
            trim_clip(src, dur, out)
        trimmed_paths.append(out)
        total += dur
        print(f"  [ok] {name} -> {dur:.2f}s")
    print(f"total picture duration (target): {total:.2f}s")

    picture = HERE / "picture_track.mp4"
    print("normalizing + concatenating...")
    normalize_and_concat(trimmed_paths, picture)
    print(f"[ok] {picture.name}")

    final = HERE / "cut_v1_narration_only.mp4"
    print("muxing narration with landing hold...")
    mux_with_landing_hold(picture, NARRATION_MP3, final, LAST_WORD_END, OUTRO_HOLD)
    print(f"[ok] {final.name}")
