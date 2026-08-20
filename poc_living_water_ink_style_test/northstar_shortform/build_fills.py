"""Build each shot's full slot-duration clip: raw AI clip + a devised fill
for the remaining gap (never a dead freeze, never a whole-frame zoom, never
a hard-cut gallery tour — see NORTH_STAR_PROMPT.md for why those were tried
and reverted). Devices are the project's own existing $0 toolkit
(panel_animator/) plus a small new one (ink_bloom.py) for this session.

Per-shot device assignment (adapted from Fable's original 8-part plan after
real testing — see build notes below each entry):
  1 wide (Stage 0, no blue allowed)      -> Lamplight (line_boil + raking_light)
  2 medium 2-shot (Stage 1)              -> Live Ink Hold + line_boil
  3 2-shot breaking (Stage 1->2)         -> Live Ink Hold + line_boil
  4 closeup five husbands (Stage 2)      -> Halo Tour (focal_tour) + line_boil
  5 compressed 2-shot (Stage 2)          -> Lamplight (line_boil + raking_light)
  6 held single "I am he" (Stage 2->3)   -> Live Ink Hold + line_boil
  7 wide moving she runs (Stage 3-begin) -> Lamplight only (ADAPTED: this
        shot's 16:9 clip took 3 regens to get clean on Kling after veo kept
        inventing a pot in her hands; not spending further processing on a
        clip that fragile — keep its fill simple and low-risk)
  8 wide landing (Stage 3)               -> line_boil only (short 1.49s fill,
        doesn't need more)

held_breath's energy(t) (from real forced-alignment word timing, see
narration.alignment.json) modulates every device's amplitude throughout, so
motion quiets during the narration's own real silences.

Run: .venv\\Scripts\\python.exe build_fills.py --shots 6 --ratios 9:16   # test one first
     .venv\\Scripts\\python.exe build_fills.py --shots 1,2,3,4,5,6,7,8 --ratios 9:16,16:9
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "panel_animator"))

import ink_bloom  # noqa: E402
import held_breath  # noqa: E402
import line_boil  # noqa: E402
import raking_light  # noqa: E402
import focal_tour  # noqa: E402

ROOT = HERE.parents[1]
NARRATION_MP3 = Path(
    r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration"
    r"\SwirlsOfLife_JohnFour_POC\v1\narration.mp3"
)
ALIGN_JSON = HERE / "narration.alignment.json"
OUTRO_HOLD = 3.0
BEAT_SECONDS_AT_60S = [5, 7, 8, 10, 10, 8, 7, 5]

SHOT_STEMS = [
    "shot01_wide_the_ask",
    "shot02_medium_2shot_living_water",
    "shot03_2shot_breaking_to_singles",
    "shot04_closeup_jesus_five_husbands",
    "shot05_compressed_2shot_spirit_truth",
    "shot06_held_single_jesus_i_am_he",
    "shot07_wide_moving_she_runs",
    "shot08_wide_landing_town_arrives",
]
DEVICE = {1: "lamplight", 2: "ink", 3: "ink", 4: "halo", 5: "lamplight",
          6: "ink", 7: "lamplight", 8: "boil_only"}

# manually-verified swirl points (cx_frac, cy_frac), eyeballed per shot per
# ratio, well clear of the robe/figures — see session notes on why an HSV
# color mask was rejected.
INK_POINT = {
    "9:16": {2: (0.35, 0.48), 3: (0.47, 0.62), 6: (0.62, 0.86)},
    "16:9": {2: (0.45, 0.40), 3: (0.50, 0.50), 6: (0.72, 0.45)},
}
INK_RADIUS_FRAC = {2: 0.05, 3: 0.06, 6: 0.07}
INK_MAX_STRENGTH = {2: 0.22, 3: 0.22, 6: 0.28}

PANEL_BOXES = {
    "9:16": [
        (0.0423, 0.1112, 0.2832, 0.2264),
        (0.3594, 0.1112, 0.2826, 0.2264),
        (0.6745, 0.1112, 0.2839, 0.2264),
    ],
    "16:9": [
        (0.1170, 0.1191, 0.2300, 0.2324),
        (0.3812, 0.1191, 0.2398, 0.2324),
        (0.6549, 0.1191, 0.2329, 0.2324),
    ],
}


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def build_shot(n: int, stem: str, ratio: str, ratio_dir: Path, w: int, h: int,
                slot: float, t0_global: float, energy_fn, work: Path) -> Path:
    src = ratio_dir / f"{stem}.mp4"
    cdur = dur(src)
    extend = max(0.0, slot - cdur)
    base_vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
               f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1")

    natural = work / f"{stem}__natural.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", base_vf,
         "-an", "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(natural)])

    device = DEVICE[n]
    parts = [natural]

    if extend > 0.05:
        last_frame = work / f"{stem}__last.png"
        run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.1", "-i", str(natural),
             "-vframes", "1", str(last_frame)])
        tail = work / f"{stem}__tail.mp4"

        if device == "ink":
            cx, cy = INK_POINT[ratio][n]
            ink_bloom.render_hold(
                last_frame, tail, extend, cx, cy, INK_RADIUS_FRAC[n], INK_MAX_STRENGTH[n],
                energy_fn, t0_global + cdur, w, h)
        elif device == "halo":
            regions = [{"bbox": [x * 100, y * 100, bw * 100, bh * 100]}
                       for x, y, bw, bh in PANEL_BOXES[ratio]]
            focal_tour.render_clip(last_frame, regions, "dramatic_spotlight",
                                    extend, w, h, tail)
        else:  # lamplight or boil_only fill -> just hold, boil+raking applied after concat
            run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(last_frame),
                 "-t", f"{extend:.3f}", "-r", "30", "-c:v", "libx264", "-crf", "18",
                 "-preset", "medium", "-pix_fmt", "yuv420p", str(tail)])
        parts.append(tail)

    slotted = work / f"{stem}__slotted.mp4"
    if len(parts) == 1:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(parts[0]), "-t", f"{slot:.3f}",
             "-c", "copy", str(slotted)])
    else:
        part_list = work / f"{stem}__parts.txt"
        part_list.write_text("\n".join(f"file '{p.name}'" for p in parts), encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
             "-i", str(part_list), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-pix_fmt", "yuv420p", str(slotted)])

    # universal base layer: line_boil on every shot, full duration.
    boiled = ratio_dir / f"{stem}__filled.mp4"
    line_boil.render(slotted, boiled, amount=0.7)

    if device == "lamplight":
        lit = work / f"{stem}__lit.mp4"
        raking_light.render_clip(boiled, lit, flare=False, k=0.025, intensity=1.0,
                                  band_width_px=max(w, h) * 0.5, angle_deg=15.0)
        run(["ffmpeg", "-y", "-v", "error", "-i", str(lit), "-c", "copy", str(boiled)])

    print(f"  [{stem}] device={device} natural={cdur:.2f}s fill={extend:.2f}s -> {slot:.2f}s slot")
    return boiled


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", default="1,2,3,4,5,6,7,8")
    ap.add_argument("--ratios", default="9:16,16:9")
    args = ap.parse_args()
    wanted = {int(x) for x in args.shots.split(",")}
    ratios = args.ratios.split(",")

    words = json.loads(ALIGN_JSON.read_text(encoding="utf-8"))
    narration_len = dur(NARRATION_MP3)
    energy_fn = held_breath.energy_envelope(words, narration_len)
    scale = narration_len / sum(BEAT_SECONDS_AT_60S)
    slot_secs = [s * scale for s in BEAT_SECONDS_AT_60S]
    slot_starts = [0.0]
    for s in slot_secs[:-1]:
        slot_starts.append(slot_starts[-1] + s)

    for ratio in ratios:
        ratio_dir = HERE / ratio.replace(":", "x")
        w, h = (1080, 1920) if ratio == "9:16" else (1920, 1080)
        work = ratio_dir / "_fillwork"
        work.mkdir(exist_ok=True)
        for i, stem in enumerate(SHOT_STEMS, start=1):
            if i not in wanted:
                continue
            build_shot(i, stem, ratio, ratio_dir, w, h, slot_secs[i - 1],
                       slot_starts[i - 1], energy_fn, work)


if __name__ == "__main__":
    main()
