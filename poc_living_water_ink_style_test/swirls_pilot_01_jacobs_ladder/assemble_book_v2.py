"""Book assembly v2 — narration+score start at second one.

The old THE_LADDER_BOOK_final.mp4 bolted 4s of SILENT front cover before
narration began and 4s of silent back cover after it (70.08s total, dead
air at both ends). This version folds the covers INTO the narrated timeline
instead: the front cover takes over F01's exact word-count slot (both show
the same beat — fleeing at dusk — the cover is just the more dramatic
rendition of it), and the back cover takes over F08's slot (both show
standing at dawn). F01 and F08 are dropped from the interior so the same
beat is never shown twice. Total runtime returns to 62.04s (narration +
3.0s landing hold) — same length as the original interior-only cut, just
opening/closing on the woodcut covers instead of the ink-wash pages.

Word counts and freeze/boomerang classification for F02-F07 are UNCHANGED
from assemble_pilot.py; front takes F01's old values (10 words, freeze —
directional walk), back takes F08's old values (26 words, boomerang —
atmospheric standing hold, no completing gesture, same category as F04/F07).

Score reused as-is (score_final.mp3, the already-approved single-lead-voice
fix, already fitted to the same 62.04s total) — no regeneration needed,
just remixed onto the new visual sequence. Mixing uses the same looser
duck as mix_score.py (a rhythmic groove needs to stay felt under speech,
not the shared pipeline/score_mix.py duck tuned for ambient pads).

All held clips are explicitly scaled to 720x1280 before concat (mixed
kling/veo native resolutions otherwise risk a bad concat).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\assemble_book_v2.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
COVERS = HERE / "_style_test_durer_woodcut"
NARRATION = HERE / "narration.mp3"
SCORE = HERE / "score_final.mp3"
OUT = HERE / "THE_LADDER_BOOK_v2.mp4"
OUTRO_HOLD = 3.0
W, H, FPS = 720, 1280, 30

# same values as mix_score.py -- a rhythmic groove needs a much looser duck
# than pipeline/score_mix.py's shared ambient-pad-tuned SIDECHAIN
AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
MUSIC_GAIN_DB = -8
DUCK_THRESHOLD = 0.45
DUCK_RATIO = 1.3
DUCK_RELEASE = 500

# (source path, word count, mode) -- F02-F07 unchanged from assemble_pilot.py;
# front takes F01's slot/mode, back takes F08's slot/mode.
UNITS = [
    ("front", COVERS / "front_cover_woodcut.mp4", 10, "freeze"),
    ("f02", HERE / "the_ladder_f02_9x16.mp4", 38, "boomerang"),
    ("f03", HERE / "the_ladder_f03_9x16.mp4", 22, "freeze"),
    ("f04", HERE / "the_ladder_f04_9x16.mp4", 37, "boomerang"),
    ("f05", HERE / "the_ladder_f05_9x16.mp4", 11, "freeze"),
    ("f06", HERE / "the_ladder_f06_9x16.mp4", 10, "freeze"),
    ("f07", HERE / "the_ladder_f07_9x16.mp4", 20, "boomerang"),
    ("back", COVERS / "back_cover_woodcut.mp4", 26, "boomerang"),
]


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def encode(cmd_tail: list[str], out: Path, prefilter: str = "") -> None:
    # BUG FIX (2026-08-22): a caller-supplied "-vf tpad=..." used to be
    # followed by THIS function's own "-vf scale=...", and ffmpeg silently
    # honors only the LAST -vf flag -- the tpad extension was being dropped
    # every time, so freeze-mode clips never actually extended past their
    # native length. Confirmed this shipped silently in the locked cut: F03
    # stayed at 5.03s instead of its intended 7.46s slot (a ~2.4s pacing
    # drift on every page from F04 onward, harmlessly absorbed by the final
    # -t truncation, but real). Fix: chain any prefilter into ONE -vf arg.
    vf = f"{prefilter + ',' if prefilter else ''}scale={W}:{H}:flags=lanczos,setsar=1"
    run(["ffmpeg", "-y", "-v", "error"] + cmd_tail +
        ["-vf", vf, "-r", str(FPS),
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-an", str(out)])


def make_freeze(src: Path, out: Path, slot: float, cdur: float) -> None:
    encode(["-i", str(src)], out,
           prefilter=f"tpad=stop_mode=clone:stop_duration={max(slot - cdur, 0):.3f}")


def make_boomerang(src: Path, out: Path, slot: float, cdur: float, work: Path, tag: str) -> None:
    if slot <= cdur:
        encode(["-i", str(src), "-t", f"{slot:.3f}"], out)
        return
    # BUG FIX (2026-08-22): the concat DEMUXER (-f concat, a text file list)
    # combined with an output "-t" trim was silently truncating at whole-
    # segment boundaries only (e.g. landing on 12.0s = 3 whole 4.0s clips
    # instead of the intended 13.15s mid-4th-clip) regardless of where -t
    # was placed in the command. Confirmed by direct A/B test on episode 2's
    # build. Switched to the concat FILTER (each segment as its own -i,
    # joined via filter_complex) instead, which trims at the exact frame.
    rev = work / f"{tag}__rev.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf",
         f"reverse,scale={W}:{H}:flags=lanczos,setsar=1",
         "-r", str(FPS), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(rev)])
    reps = int(slot // cdur) + 2
    parts = [src if i % 2 == 0 else rev for i in range(reps)]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in parts:
        cmd += ["-i", str(p)]
    labels = "".join(f"[{i}:v]" for i in range(len(parts)))
    filt = (f"{labels}concat=n={len(parts)}:v=1:a=0[c];"
            f"[c]scale={W}:{H}:flags=lanczos,setsar=1[v]")
    cmd += ["-filter_complex", filt, "-map", "[v]", "-t", f"{slot:.3f}",
            "-r", str(FPS), "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an", str(out)]
    run(cmd)


def main() -> None:
    narration_len = dur(NARRATION)
    total_words = sum(u[2] for u in UNITS)
    total = narration_len + OUTRO_HOLD
    print(f"[plan] narration={narration_len:.2f}s total(+{OUTRO_HOLD}s hold)={total:.2f}s")

    work = HERE / "_assembly_v2"
    work.mkdir(exist_ok=True)

    held = []
    for tag, src, words, mode in UNITS:
        slot = narration_len * words / total_words
        cdur = dur(src)
        out = work / f"{tag}__held.mp4"
        if mode == "boomerang":
            make_boomerang(src, out, slot, cdur, work, tag)
        else:
            make_freeze(src, out, slot, cdur)
        print(f"  [{tag}] native={cdur:.2f}s -> slot={slot:.2f}s ({mode})")
        held.append(out)

    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in held), encoding="utf-8")
    silent_video = work / "silent_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-r", str(FPS), "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", str(silent_video)])
    print(f"[concat] {dur(silent_video):.2f}s silent video")

    with_narration = work / "with_narration.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(silent_video), "-i", str(NARRATION),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(with_narration)])

    filt = (
        f"[1:a]{AFMT},volume={MUSIC_GAIN_DB}dB[mus];"
        f"[0:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[mus][key]sidechaincompress=threshold={DUCK_THRESHOLD}:ratio={DUCK_RATIO}:"
        f"attack=20:release={DUCK_RELEASE}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO_HOLD}[vout]"
    )
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(with_narration), "-i", str(SCORE),
         "-filter_complex", filt,
         "-map", "[vout]", "-map", "[mix]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", str(OUT)])
    print(f"[done] {OUT}  ({dur(OUT):.2f}s)")


if __name__ == "__main__":
    main()
