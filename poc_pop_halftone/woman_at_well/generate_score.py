"""Score v1 for "Woman at the well" (pop halftone), merged from the blind score panel
(score_panel/panel_r1: fable, claude, codex, grok). Convergence: oud + frame drum + claps + round bass
+ one watery voice (handpan), ~100 BPM, D minor -> D major; unfinished 'drip' motif (thirst) that gains
its home note at "never thirst"; drain at 23 s, flood lift at 30 s, near-out 48.5-54 s, joy groove to
town, lift at "Saviour of the world", drop at "The jar stayed", felt piano + strings at the tomb.
Split 54.3 s (3/4 seats: inside the pause after "He is the Christ"). Free-text music_v1, never
composition_plan. Owner yes up to $2.50, 2026-11-13."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402

VIDEO = HERE / "motion_v2" / "WOMAN_AT_WELL_MOTION_v2.mp4"
OUT = HERE / "score"
P1, P2, RAW, FIT = OUT / "part1_raw.mp3", OUT / "part2_raw.mp3", OUT / "score_raw.mp3", OUT / "score.mp3"
SPLIT, XF = 54.3, 0.5

PART1 = ("Instrumental only, no vocals, no choir. 100 BPM, key of D minor turning to D major. Bright modern pop "
 "groove with Middle Eastern colour: dry plucked oud, frame drum, tight handclaps, round warm bass, a soft watery "
 "handpan, soft warm strings. Playful, bold, warm, clean, never epic, not a trailer, no big drum hits. Music is "
 "audible from the very first second, no silent lead-in, continuous sound throughout. Signature motif, the drip: "
 "two short notes on the same pitch then one step up, left hanging like a question. It starts with solo dry oud "
 "playing the drip motif twice. Around 4 seconds in, one handclap, then a light frame drum and clap groove with "
 "bass and an oud riff. Around 11 seconds in, it thins to soft bass and drum only. Around 14 seconds in, the groove "
 "returns, tighter and slightly tense. Around 23 seconds in, all drums and bass stop; only a lone dry oud plays the "
 "unfinished drip motif, slow and thirsty. Around 27 seconds in, a soft rising swell and the handpan is heard for "
 "the first time. Around 30 seconds in, a joyful full lift in D major: the handpan plays the drip motif with a "
 "fourth note that resolves home, flowing plucks, strings, claps and bass, the fullest moment of the piece. Around "
 "37 seconds in, it pulls back to a gentle bass pulse and soft handpan, kind and warm. Around 48 seconds in, "
 "drums and bass stop and it drops to one quiet sustained warm string note that keeps sounding softly to the very "
 "end, no fade-out to silence. Keep the midrange light for a spoken voice-over.")

PART2 = ("Instrumental only, no vocals, no choir. 100 BPM, D major. Dry plucked oud, frame drum, tight handclaps, "
 "round warm bass, a soft watery handpan, soft warm strings, felt piano. Joyful, running, bright and warm, never "
 "epic, not a trailer. Music is audible from the very first second, no silent lead-in. It starts at once with a "
 "bright clap and frame drum groove, strummed oud and the handpan playing a four-note motif: two short notes on "
 "the same pitch, one step up, then a fourth note that lands home. Around 12 seconds in, a bigger warm lift with "
 "strings joining the groove. Around 17 seconds in, the drums stop suddenly and the handpan plays alone. Around "
 "19 seconds in, warm gentle strings and handpan, no drums, tender. Around 27 seconds in, only felt piano and soft "
 "strings, very quiet and reverent. Around 30 seconds in, the felt piano plays the four-note motif once, slowly, "
 "and the last note rings out softly to the end. Keep the midrange light for a spoken voice-over.")


def main() -> None:
    key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
    OUT.mkdir(exist_ok=True)
    total = dur(VIDEO)
    l1, l2 = SPLIT, total - SPLIT
    print(f"video {total:.2f}s split {SPLIT} -> {l1:.2f} / {l2:.2f}")
    gen_music(PART1, l1 + 3.0, P1, key)
    gen_music(PART2, l2 + 6.0, P2, key)
    a, b = OUT / "_a.mp3", OUT / "_b.mp3"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-t", f"{l1 + XF:.2f}", str(a)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P2), "-t", f"{l2:.2f}", str(b)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(a), "-i", str(b), "-filter_complex",
                    f"acrossfade=d={XF}:c1=tri:c2=tri", str(RAW)], check=True)
    a.unlink(); b.unlink()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(RAW), "-af",
                    f"apad=whole_dur={total:.2f},afade=t=out:st={total - 1.2:.2f}:d=1.2", "-t", f"{total:.2f}", str(FIT)], check=True)
    check_timeline_sweep(FIT)
    print(f"[done] {FIT} {dur(FIT):.2f}s")


if __name__ == "__main__":
    main()
