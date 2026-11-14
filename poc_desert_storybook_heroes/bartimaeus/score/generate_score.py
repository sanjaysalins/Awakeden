"""Score v1 for Blind Bartimaeus, merged from blind panel score_panel/panel_r1 (fable, claude, codex, grok).
Convergence (4/4): walking pulse = the moving crowd, STOPS at "And Jesus stood still"; an unanswered
4-note cry motif that resolves home in D major when he sees (~49 s); pulse returns as he follows; low and
solemn at the cross; warm lift at "rose"; resolved motif in the 3 s hold. Instruments (3/4): oud, finger
frame drum, ney, one cello. Split 26.1 s inside the planned silence 25.6-26.6 (3/4 seats). No silence asked
of the model (dead-air risk); the hard stop is made in the join. music_v1 free text, never composition_plan.
Owner yes ~$1.35 capped $2.50, 2026-11-14."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402

VIDEO = HERE.parent / "film" / "bartimaeus_draft_v2.mp4"
P1, P2, FIT = HERE / "part1_raw.mp3", HERE / "part2_raw.mp3", HERE / "score.mp3"
STOP, SPLIT = 25.6, 26.1

STYLE = ("Instrumental only, no vocals, no choir. Intimate ancient Middle Eastern folk underscore for a warm painted "
 "storybook film. Only four instruments: plucked oud, soft finger-played frame drum, breathy ney reed flute, one "
 "warm cello. Dry, warm, hand-played, small room. Never epic, not a trailer, no synths, no big drums, no brass. "
 "Music is audible from the very first second, no silent lead-in, continuous sound throughout. Keep the midrange "
 "light for a spoken voice-over. ")

PART1 = (STYLE + "Slow walking tempo, 76 BPM, D minor. Signature motif, the cry: four notes on the ney, a step up, "
 "a leap up, a held note, then falling back without landing home, like a question with no answer. It starts with "
 "a very quiet low cello drone alone. Around 3 seconds in, the ney plays the cry motif once, unanswered. Around 5 "
 "seconds in, a gentle plucked oud walking pattern and soft frame drum begin, like footsteps of a crowd on a dusty "
 "road. Around 13 seconds in, the cello adds a low, sorrowful line under the walking pattern, darker. Around 21 "
 "seconds in, the walking pattern grows a little more urgent and the ney plays the cry motif again, higher and "
 "pleading, and it keeps going to the end.")

PART2 = (STYLE + "D minor moving to D major, 76 BPM. Signature motif: four notes, a step up, a leap up, a held "
 "note, then landing home. It starts with one single soft held cello note, alone, no rhythm, no drum, very still "
 "and tender. Around 8 seconds in, a few bright plucked oud notes, then stillness again. Around 12 seconds in, "
 "very sparse and quiet: soft cello and occasional single oud plucks, no drum. Around 20 seconds in, the cello "
 "plays the four-note motif slowly and it resolves home. Around 23 seconds in, a warm lift in D major: ney and "
 "cello play the motif together over gentle full oud chords, joyful but small. Around 29 seconds in, a soft "
 "oud walking pattern and frame drum return, like footsteps following, warm. Around 35 seconds in, it thins to a "
 "soft drum and a low mournful cello, minor and solemn. Around 40 seconds in, the cello rises and the oud opens "
 "into a warm major chord that rings. Around 43 seconds in, settled and peaceful, the walking pattern slows and "
 "stops, cello holding. Around 50 seconds in, the ney plays the four-note motif once, resolved, and the last note "
 "rings softly to the very end.")


def main() -> None:
    key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
    total = dur(VIDEO)
    l2 = total - SPLIT
    print(f"video {total:.2f}s split {SPLIT} -> part2 {l2:.2f}")
    if "--join-only" not in sys.argv:
        if not P1.exists():
            gen_music(PART1, SPLIT + 3.0, P1, key)
        if not P2.exists():
            gen_music(PART2, l2 + 4.0, P2, key)
    for p in (P1, P2):
        check_no_dead_intro(p)  # part2 raw tail past the used 53.07 s may be silent; sweep the joined FIT instead
    fc = (f"[0:a]atrim=0:{STOP},afade=t=out:st={STOP-0.45:.2f}:d=0.45,apad=whole_dur={SPLIT}[a];"
          f"[1:a]atrim=0:{l2:.3f},afade=t=in:d=0.5,afade=t=out:st={l2-1.2:.2f}:d=1.2[b];"
          "[a][b]concat=n=2:v=0:a=1[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc,
                    "-map", "[o]", "-t", f"{total:.3f}", str(FIT)], check=True)
    check_timeline_sweep(FIT)
    print(f"[done] {FIT} {dur(FIT):.2f}s")


if __name__ == "__main__":
    main()
