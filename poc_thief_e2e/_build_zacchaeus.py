"""Zacchaeus assembly build -- Stage 3, first real test (2026-07-25).

Proposed shape from E2E_WORKFLOW_PROPOSAL.md / COMIC_STRIP_NATIVE_SPEC.md
"Path A": place each panel clip at its narration beat's start time, fill the
gap between the clip's animated duration and the beat's actual duration with
a held last frame, extended. Timings below are computed from per_turn_synth's
own logged per-turn durations (7 turns, atempo 1.2830 on narrator turns only,
0.4s pre-quote pause on each of the 3 quotes).

Panel assignment (3 panels, 4 narration segments -- panel B reused for the
bookend, matching the hero-bookend discipline: open AND close on the
gospel-pivot moment, here Jesus's two direct quotes):
  Panel A (wide: crowd+tree+Jesus arriving) -> T0  narrator hook+climb   0.00-17.08
  Panel B (Jesus close-up, calling)          -> T1+T2 jesus quote1 + narrator contrast  17.08-31.41
  Panel C (Zacchaeus close-up, joy)          -> T3+T4 zacchaeus quote + narrator bridge  31.41-48.42
  Panel B again (Jesus close-up, landing)    -> T5+T6 jesus quote2 + narrator CTA  48.42-59.00

Each clip is scaled+padded to a common 1080x1920 canvas (aged-paper cream
bars for non-9:16 source clips), held on its last frame to fill its segment
duration, concatenated, muxed with narration.mp3, then given a 3.5s landing
hold per INV-26 (video holds the final frame, audio gets matching silence).

  .venv\\Scripts\\python.exe poc_thief_e2e/_build_zacchaeus.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIPS = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus"
AUDIO = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\jesus\narration\Zacchaeus_Luke19\v1\narration.mp3")
OUT = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus" / "_build"
OUT.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1080, 1920, 30
PAPER = "0xEDE0C8"

SEGMENTS = [
    ("panel_a_wide.mp4", 5.04, 17.08),
    ("panel_b_jesus.mp4", 5.875, 14.33),
    ("panel_c_zacchaeus.mp4", 5.875, 17.01),
    ("panel_b_jesus.mp4", 5.875, 10.58),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAILED:", " ".join(cmd))
        print(r.stderr[-2000:])
        raise SystemExit(1)


def fit_and_hold(src: Path, src_dur: float, target_dur: float, out: Path):
    """Scale+pad src to WxH (paper bars), then hold last frame to reach target_dur."""
    stop_duration = max(target_dur - src_dur, 0.1)
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={PAPER},"
        f"fps={FPS},"
        f"tpad=stop_mode=clone:stop_duration={stop_duration:.2f}"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error", "-i", str(src),
        "-vf", vf,
        "-t", f"{target_dur:.2f}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out),
    ]
    run(cmd)


def main():
    seg_paths = []
    for i, (name, src_dur, dur) in enumerate(SEGMENTS):
        src = CLIPS / name
        out = OUT / f"seg{i:02d}.mp4"
        print(f"[seg {i}] {name} -> {dur:.2f}s held")
        fit_and_hold(src, src_dur, dur, out)
        seg_paths.append(out)

    # concat
    listfile = OUT / "concat_list.txt"
    listfile.write_text("\n".join(f"file '{p.name}'" for p in seg_paths), encoding="utf-8")
    concat_out = OUT / "video_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-c", "copy", str(concat_out)])

    # landing hold: extend video by holding final frame +3.5s, extend audio with 3.5s silence
    HOLD = 3.5
    video_held = OUT / "video_held.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(concat_out),
         "-vf", f"tpad=stop_mode=clone:stop_duration={HOLD}",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video_held)])

    audio_held = OUT / "audio_held.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(AUDIO),
         "-af", f"apad=pad_dur={HOLD}", str(audio_held)])

    final = ROOT / "poc_thief_e2e" / "clips" / "_zacchaeus" / "ZACCHAEUS_FINAL.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video_held), "-i", str(audio_held),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)])

    print(f"\n[done] {final}")


if __name__ == "__main__":
    main()
