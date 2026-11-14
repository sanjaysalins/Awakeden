"""Score v2 (melody) for Blind Bartimaeus. Owner: "I think we can do a better score" -> picked "More melody + feeling"
(~$1.20, cap $2.50). Blind panel score_panel/panel_r2 (fable, claude, codex, grok). Convergence 4/4: felt piano leads one
hummable tune, warm strings, solo cello sings the WHOLE tune at sight (~49 s), light oud/ney only, no drums/drone/trailer.
Tune (claude seat, matches fable/grok shape): rise D-F-G-A, fall A-G-F-E, hangs on E; whole = ...F-E-D home.
Split 26.1 in the planned silence (3/4). v1 (oud/drum walking score) kept as score_v1_* files."""
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
P1, P2, FIT = HERE / "v2_part1_raw.mp3", HERE / "v2_part2_raw.mp3", HERE / "score_v2.mp3"
STOP, SPLIT = 25.6, 26.1

STYLE = ("Instrumental only, no vocals, no choir, no drums, no percussion. Gentle, warm cinematic score for a painted "
 "storybook film. Felt piano leads, warm soft string section, one solo cello, and only a light touch of Middle-Eastern "
 "colour from a few soft oud plucks and a breathy ney. Tender, intimate, clear hummable melody. Not ambient, not a "
 "drone, not epic, not a trailer. Music is audible from the very first second, no silent lead-in, continuous sound "
 "throughout with no gaps. Keep the midrange light for a spoken voice-over. ")

PART1 = (STYLE + "D minor, 66 BPM, slow and singing. The melody: four rising notes D F G A, then falling A G F E, "
 "ending unresolved on E, like a question with no answer. It opens with one low felt piano note and a soft ney "
 "breath. Around 3 seconds in, the felt piano plays the melody once, slowly, ending unresolved on E. Around 13 "
 "seconds in, warm low strings enter under the piano with a slow gentle pulse and a low solo cello note, and the "
 "piano plays the melody again, a little higher, still unresolved. Around 21 seconds in, the strings swell gently "
 "and the piano plays the melody a third time, higher and pleading, ending on E and holding it to the end.")

PART2 = (STYLE + "D minor turning to D major, 66 BPM. The same melody: D F G A, then A G F E, and when it is sung "
 "whole it comes home: F E D. It opens with one soft held felt piano note, very still, then sparse single piano "
 "notes. Around 8 seconds in, a short rising piano phrase and a small soft oud flourish. Around 12 seconds in, soft "
 "held piano chords and a quiet string pad, very quiet and sparse. Around 23 seconds in, the emotional peak: a warm "
 "solo cello sings the full melody and resolves home to D, the strings bloom, tender and joyful. Around 29 seconds "
 "in, a gentle walking piano pattern carries the melody forward, cello and violin sharing it. Around 35 seconds in, "
 "it thins to a low, slow solo cello, sorrowful. Around 40 seconds in, it turns to D major and the strings rise with "
 "quiet hope. Around 43 seconds in, piano and cello play the full melody once more, gently, resolving home. Around "
 "50 seconds in, a final soft D major chord on piano and strings with one oud note, ringing softly to the very end.")


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
