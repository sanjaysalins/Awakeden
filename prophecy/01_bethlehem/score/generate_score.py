"""Score v1 for Prophecy 01 "Born in Bethlehem" (film v4c, 59.3 s). Owner yes 2026-11-15 (~$1.20, cap $2.50).
Blind panel: Fable seat (FABLE_EPISODE_DESIGN.md) + score_panel/panel_r1 (claude, codex, grok).
Convergence 4/4: felt piano + solo cello only, one hummable "promise tune" left UNFINISHED until the final hold,
no choir; 3/4 no drums (Fable's frame drum dropped); split 37.0 s inside the planned pause (3/4).
Silences / dips are done in the MIX, never asked of the generator (dead-air lesson)."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402

VIDEO = HERE.parent / "film" / "BETHLEHEM_FILM_v4c.mp4"
P1, P2, FIT = HERE / "part1_raw.mp3", HERE / "part2_raw.mp3", HERE / "score.mp3"
STOP, SPLIT = 36.3, 37.0

STYLE = ("Instrumental only, no vocals, no choir, no drums, no percussion, no synth, no orchestra. Intimate cinematic "
 "score: soft felt piano and one warm solo cello only, close and gentle. A clear, simple melody a person can hum after "
 "one listen. Not ambient, not a drone, not epic, not a trailer. Music is audible from the very first second, no silent "
 "lead-in, continuous sound throughout with no gaps. Keep the midrange light for a spoken voice-over. ")

TUNE = ("The promise tune: four slow rising notes D, E, F-sharp, A, then one step down to E, left hanging like an "
 "unfinished sentence. ")

PART1 = (STYLE + "D major with soft minor shading, 66 BPM, slow and tender. " + TUNE +
 "It opens with one low held cello note and a few quiet felt piano notes, old and hushed, like a room lit by torches. "
 "Around 6 seconds in, the cello plays long calm notes. Around 10 seconds in, the felt piano plays the promise tune "
 "once, slowly, and leaves it hanging on E. Around 18 seconds in, a gentle walking pattern in the piano left hand, like "
 "slow footsteps on a long road, with the cello humming underneath. Around 22 seconds in, the cello sings the promise "
 "tune warmly, still hanging on E, tender and quiet. Around 26 seconds in, the walking pattern returns, a little "
 "lighter. Around 29 seconds in, it turns darker and lower, one low cello note under soft minor piano chords. Around "
 "34 seconds in, the walking thins to single slow piano notes, and the piano plays the first four notes of the tune "
 "with no answer, holding softly to the end.")

PART2 = (STYLE + "D major, 66 BPM, warm and open. " + TUNE + "When it is finally played whole it comes home: D, E, "
 "F-sharp, A, then G, F-sharp, E, D. It opens very quietly with one soft held low cello note. Around 3 seconds in, the "
 "walking piano pattern returns, brighter, with the cello. Around 6 seconds in, a wide, open cello line, warm and "
 "hopeful. Around 9 seconds in, high piano notes step gently downward. Around 11 seconds in, cello alone, one long "
 "slow sincere note, reverent. Around 13 seconds in, a gentle warm swell of piano and cello, glowing, never loud. "
 "Around 16 seconds in, piano alone, soft and simple. Around 19 seconds in, the piano plays the promise tune whole for "
 "the first time and resolves home to D, the cello holds the last D, and it rings out softly to the end.")


def main() -> None:
    key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
    total = dur(VIDEO)
    l2 = total - SPLIT
    print(f"video {total:.2f}s split {SPLIT} -> part2 {l2:.2f}")
    if "--join-only" not in sys.argv:
        if not P1.exists():
            gen_music(PART1, SPLIT + 3.0, P1, key)
        if not P2.exists():
            gen_music(PART2, l2 + 3.5, P2, key)
    for p in (P1, P2):
        check_no_dead_intro(p)
    fc = (f"[0:a]atrim=0:{STOP},afade=t=out:st={STOP-0.5:.2f}:d=0.5,apad=whole_dur={SPLIT}[a];"
          f"[1:a]atrim=0:{l2:.3f},afade=t=in:d=0.5,afade=t=out:st={l2-0.8:.2f}:d=0.8[b];"
          "[a][b]concat=n=2:v=0:a=1[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc,
                    "-map", "[o]", "-t", f"{total:.3f}", str(FIT)], check=True)
    check_timeline_sweep(FIT)
    print(f"[done] {FIT} {dur(FIT):.2f}s")


if __name__ == "__main__":
    main()
