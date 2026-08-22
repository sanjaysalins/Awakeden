"""The Ashes That Made Clean — final book assembly. Same "north star"
pattern validated on Jacob's Ladder v2 (swirls_pilot_01_jacobs_ladder/
assemble_book_v2.py): front cover takes the opening beat's word-count slot,
back cover takes the landing beat's slot, narration+score run continuously
from second one — no silent bookends.

Word-count mapping (content-fit, not 1:1 with which narration paragraph
literally supplied each page's baked caption — see module docstring in
render_ashes.py and the session notes for the one honest mismatch: F02's
caption text came from Para1's phrase rather than the Numbers 19 KJV quote
originally planned for that slot):
  FRONT=Para1(21w) F01=Para2(24w) F02=Para3(35w) F03=Para4(27w)
  F04=Para5(27w) BACK=Para6+7(23w)  =>  157 words total, matches the full
  narration exactly.

Freeze vs boomerang: F01 (small discrete hand motion, feeding the fire) and
F04 (the rinsing/hyssop-tip motion explicitly completes and must not
reverse) are FREEZE. FRONT, F02, F03, BACK are pure atmospheric holds with
no completing gesture -> BOOMERANG.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_episode_02_ashes_that_made_clean\\assemble_ashes.py
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
COVERS = HERE
NARRATION = HERE / "narration.mp3"
OUTRO_HOLD = 3.0
W, H, FPS = 720, 1280, 30

AFMT = "aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100"
# NOTE (2026-08-22): Jacob's Ladder's validated duck (-8dB/0.45/1.3/500ms)
# made THIS episode's original score nearly inaudible (measured delta ~0dB
# against narration-alone at 13 points -- the exact "I did not hear the
# score" symptom again). Diagnosed empirically, not assumed: this episode's
# raw score_final.mp3 render happens to sit close to narration's own natural
# level even with ZERO attenuation (measured -21.8dB score vs -20.3dB
# narration) -- so the SAME negative attenuation that worked for Jacob's
# Ladder's louder-mastered score just buries this one.
#
# The "somber" score (generate_score_somber.py, added after a red-team of
# the original dream-trance direction flagged a tonal mismatch against this
# episode's ceremonial-uncleanness content) needed its OWN independent A/B
# sweep -- it is a deliberately sparse, silence-between-phrases piece, so
# unlike the driving-groove original, some sample points are SUPPOSED to sit
# below narration (that's the composition's own written rests, confirmed by
# checking those exact timestamps against the raw unattenuated score level:
# -30dB to -80dB raw at t=1/20/25/50/55/58, vs -14 to -18dB raw at its actual
# musical passages). Target for a sparse score is "healthy presence when the
# music is actually playing," not "never dips" -- forcing the rests above 0dB
# would just blow out the played passages to compensate for silence that was
# written on purpose.
#
# Lesson either way: don't assume a duck (or an audibility target) tuned for
# one score generation transfers to another -- ElevenLabs Music's mastering
# level AND a piece's own dynamic character both vary per generation, verify
# every time.
SCORE_VARIANTS = {
    "original": dict(
        score=HERE / "score_final.mp3",
        gain=3, threshold=0.7, ratio=1.15, release=500,
        out=HERE / "THE_ASHES_BOOK_final.mp4",
    ),
    "somber": dict(
        score=HERE / "score_somber.mp3",
        gain=2, threshold=0.55, ratio=1.25, release=400,
        out=HERE / "THE_ASHES_BOOK_final_somber.mp4",
    ),
}

UNITS = [
    ("front", HERE / "front_cover_woodcut.mp4", 21, "boomerang"),
    ("f01", HERE / "the_ashes_f01_9x16.mp4", 24, "freeze"),
    ("f02", HERE / "the_ashes_f02_9x16.mp4", 35, "boomerang"),
    ("f03", HERE / "the_ashes_f03_9x16.mp4", 27, "boomerang"),
    ("f04", HERE / "the_ashes_f04_9x16.mp4", 27, "freeze"),
    ("back", HERE / "back_cover_woodcut.mp4", 23, "boomerang"),
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
    # BUG FIX (2026-08-22): a caller-supplied "-vf tpad=..." here used to be
    # followed by THIS function's own "-vf scale=...", and ffmpeg silently
    # honors only the LAST -vf flag -- the tpad extension was being dropped
    # every time, so freeze-mode clips never actually extended past their
    # native length. Confirmed this had already shipped silently in Jacob's
    # Ladder's own assemble_book_v2.py (F03 stayed at 5.03s instead of its
    # intended 7.46s slot). Fix: chain any prefilter into ONE -vf argument.
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
    # was placed in the command. Confirmed by direct A/B test. Switched to
    # the concat FILTER (each segment as its own -i, joined via
    # filter_complex) instead, which trims correctly at the exact frame.
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--score", choices=sorted(SCORE_VARIANTS), default="original")
    args = parser.parse_args()
    variant = SCORE_VARIANTS[args.score]
    score, music_gain_db, duck_threshold, duck_ratio, duck_release, final_out = (
        variant["score"], variant["gain"], variant["threshold"],
        variant["ratio"], variant["release"], variant["out"],
    )
    print(f"[variant] {args.score} -> {score.name}")

    narration_len = dur(NARRATION)
    total_words = sum(u[2] for u in UNITS)
    total = narration_len + OUTRO_HOLD
    print(f"[plan] narration={narration_len:.2f}s total(+{OUTRO_HOLD}s hold)={total:.2f}s")

    work = HERE / "_assembly"
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
        f"[1:a]{AFMT},volume={music_gain_db}dB[mus];"
        f"[0:a]{AFMT},apad=whole_dur={total},asplit=2[main][key];"
        f"[mus][key]sidechaincompress=threshold={duck_threshold}:ratio={duck_ratio}:"
        f"attack=20:release={duck_release}[musd];"
        f"[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix];"
        f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO_HOLD}[vout]"
    )
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(with_narration), "-i", str(score),
         "-filter_complex", filt,
         "-map", "[vout]", "-map", "[mix]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", str(final_out)])
    print(f"[done] {final_out}  ({dur(final_out):.2f}s)")


if __name__ == "__main__":
    main()
