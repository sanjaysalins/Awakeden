"""Jacob's Ladder pilot — quick assembly for a first look.

Concats the 8 locked clips, one per page, each extended to a slot duration
proportional to that page's share of the narration's word count
(word-count proportional, NOT forced alignment — there is no per-scene
timeline for this ad-hoc POC the way the main cli_visual pipeline has one;
see WORD_COUNTS below for the mapping and its rationale).

Two extension modes, picked per page (locked 2026-08-22 per user feedback —
"do the reverse boomerang animation... just ensure it's not for anything
that has forward animation like walking or pouring or falling"):
  - FREEZE (ffmpeg tpad, last frame held): for pages built around a body
    performing a directional, completing physical action — reversing it
    would visibly undo the action (Jacob un-walking, un-rising, un-turning
    his head). F01 (walk), F03 (angels climbing/traveling), F05 (rise),
    F06 (head-turn), F08 (head-lift).
  - BOOMERANG (ping-pong forward/reverse, seamless): for pages that are a
    pure atmospheric hold with no completing action — sleep-breathing,
    a presence-hold, a wide quiet field. F02, F04, F07.

Mux narration over the concatenated video, then apply the INV-26 landing
hold (`pipeline/score_mix.py`'s pattern, reused, not duplicated) — video
holds its last frame and narration audio pads to the same absolute length
for a 3.0s hold. No score/SFX layer yet (that's /sfx's job, deliberately
out of scope for this quick look).

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\assemble_pilot.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
NARRATION = HERE / "narration.mp3"
OUT = HERE / "THE_LADDER_pilot_cut.mp4"
OUTRO_HOLD = 3.0

BOOMERANG_PAGES = {"f02", "f04", "f07"}  # atmospheric holds, no completing action

# word counts per page, split from narration.md's own paragraphs against each
# page's caption (each caption IS a verbatim fragment of that paragraph, so
# the mapping is grounded in the text, not guessed) — see module docstring.
WORD_COUNTS = {
    "f01": 10,   # "A man fled his own brother's threat to kill him"
    "f02": 38,   # "...slept on open ground..." + "God does not wait..."
    "f03": 22,   # "Scripture says he dreamed of a ladder..."
    "f04": 37,   # "I am with thee..." + "Some would call it just a guilty man's dream..."
    "f05": 11,   # "Jacob woke and said: Surely the LORD is in this place;"
    "f06": 10,   # "...and I knew it not... How dreadful is this place!"
    "f07": 20,   # "You may be lying in your own version of that field..."
    "f08": 26,   # "Jacob saw a ladder to heaven..." + the CTA
}
PAGES = list(WORD_COUNTS)


def dur(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def encode(cmd_tail: list[str], out: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error"] + cmd_tail +
        ["-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-an", str(out)])


def make_freeze(src: Path, out: Path, slot: float, cdur: float) -> None:
    encode(["-i", str(src), "-vf",
            f"tpad=stop_mode=clone:stop_duration={max(slot - cdur, 0):.3f}"], out)


def make_boomerang(src: Path, out: Path, slot: float, cdur: float, work: Path, pid: str) -> None:
    """Seamless ping-pong: forward, reverse, forward, reverse... trimmed to `slot`.
    No freeze anywhere — the clip never stops moving until the hard cut to the
    next page (a page-flip is expected to be a hard cut in this style)."""
    if slot <= cdur:
        encode(["-i", str(src), "-t", f"{slot:.3f}"], out)
        return
    rev = work / f"{pid}__rev.mp4"
    encode(["-i", str(src), "-vf", "reverse"], rev)
    reps = int(slot // cdur) + 2
    parts = [src if i % 2 == 0 else rev for i in range(reps)]
    concat_list = work / f"{pid}__pingpong.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-t", f"{slot:.3f}",
         "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-an", str(out)])


def main() -> None:
    narration_len = dur(NARRATION)
    total_words = sum(WORD_COUNTS.values())
    total = narration_len + OUTRO_HOLD
    print(f"[plan] narration={narration_len:.2f}s total(+{OUTRO_HOLD}s hold)={total:.2f}s")

    work = HERE / "_assembly"
    work.mkdir(exist_ok=True)

    held = []
    for pid in PAGES:
        src = HERE / f"the_ladder_{pid}_9x16.mp4"
        slot = narration_len * WORD_COUNTS[pid] / total_words
        cdur = dur(src)
        out = work / f"{pid}__held.mp4"
        mode = "boomerang" if pid in BOOMERANG_PAGES else "freeze"
        if mode == "boomerang":
            make_boomerang(src, out, slot, cdur, work, pid)
        else:
            make_freeze(src, out, slot, cdur)
        print(f"  [{pid}] native={cdur:.2f}s -> slot={slot:.2f}s ({mode})")
        held.append(out)

    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in held), encoding="utf-8")
    silent_video = work / "silent_concat.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-r", "30", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", str(silent_video)])
    print(f"[concat] {dur(silent_video):.2f}s silent video")

    # narration over the concat, then the INV-26 landing hold: video holds its
    # last frame, narration audio pads to the same absolute `total` length.
    filt = (
        f"[0:v]tpad=stop_mode=clone:stop_duration={OUTRO_HOLD}[vout];"
        f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo:sample_rates=44100,"
        f"apad=whole_dur={total}[aout]"
    )
    run(["ffmpeg", "-y", "-v", "error",
         "-i", str(silent_video), "-i", str(NARRATION),
         "-filter_complex", filt,
         "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k",
         "-t", f"{total:.3f}", str(OUT)])
    print(f"[done] {OUT}  ({dur(OUT):.2f}s)")


if __name__ == "__main__":
    main()
