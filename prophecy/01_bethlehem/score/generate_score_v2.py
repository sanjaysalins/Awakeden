"""CINEMATIC score v2 for Prophecy 01 "Born in Bethlehem" (words v3, film 59.5 s). Owner: score should be cinematic
for this serious topic; film now a bold graphic comic. Owner yes ~$1.20 (cap $2.50), 2026-11-15.
Blind panel score_panel_v2: fable_score.md + panel_r1/{claude,codex,grok}_score.md. Convergence 4/4: full strings +
French horns + timpani (sparing), no choir/piano lead; horn 'promise tune' left unfinished, completed only in the final
hold; one warm swell at 'He rose'; still/sacred for heaven-cross-tomb; split inside the 1 s silence (38.0-39.0).
Prompts merged from the Fable seat (closest to the convergent cue sheet). Silences/dips are done in the MIX
(dead-air lesson): prompts ask for continuous sound."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402

P1, P2, FIT = HERE / "cine_part1_raw.mp3", HERE / "cine_part2_raw.mp3", HERE / "score_cine.mp3"
TOTAL, STOP, SPLIT = 59.5, 38.0, 38.6

STYLE = ("Cinematic orchestral film score, instrumental only. Full string section with deep cellos and basses, French "
 "horns, timpani used sparingly. No choir, no vocals, no piano, no synth, no rock drums, no trailer braams or hits, no "
 "Middle-Eastern scales. Serious, reverent, warm, grace not fear. Music is audible from the very first second, no "
 "silent lead-in, continuous sound throughout with no gaps. Keep the midrange light for a spoken voice-over. ")

PART1 = (STYLE + "D major with minor shading, slow 66 BPM. The promise tune: a solo French horn plays five slow "
 "rising notes that stop one step below home, left hanging. It starts at once with a low string tremolo and one held "
 "horn note, quiet and expectant. Around 4 seconds in, a soft timpani roll and deep slow cellos and basses, like time "
 "turning back. Around 12 seconds in, a solo French horn plays the promise tune over quiet strings, unfinished. Around "
 "16 seconds in, very thin: one high held string note. Around 18 seconds in, a gentle walking pulse of plucked low "
 "strings, like travellers on a road. Around 22 seconds in, warm strings and horn play the promise tune again, bigger "
 "and warmer, still unfinished. Around 27 seconds in, darker and heavier, slow low brass chords, weight not horror. "
 "Around 34 seconds in, very quiet, one low held bass note. Around 36 seconds in, one soft high string chord, thin and "
 "uneasy, holding to the end.")

PART2 = (STYLE + "D major, 66 BPM, reverent and hopeful. The same promise tune on French horn: five slow rising "
 "notes; when it is finally finished it adds two more notes stepping down to rest on home. It opens with quiet, "
 "waiting low strings. Around 3 seconds in, one timpani hit and a strong driving string rhythm with rising horns, "
 "people setting out on a journey. Around 7 seconds in, the drive melts into long warm chords. Around 9 seconds in, "
 "sacred and still: soft high strings and harp, no drums. Around 14 seconds in, one huge warm swell, full strings, "
 "horns and a timpani roll, glowing, not a trailer hit. Around 16 seconds in, it drops to one soft held string note. "
 "Around 18 seconds in, French horns and full strings play the promise tune whole and it resolves home on a warm D "
 "major chord that rings out softly to the end.")


def main() -> None:
    key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
    l2 = TOTAL - SPLIT
    if "--join-only" not in sys.argv:
        if not P1.exists():
            gen_music(PART1, SPLIT + 3.0, P1, key)
        if not P2.exists():
            gen_music(PART2, l2 + 3.0, P2, key)
    for p in (P1, P2):
        check_no_dead_intro(p)
    fc = (f"[0:a]atrim=0:{STOP},afade=t=out:st={STOP - 0.35:.2f}:d=0.35,apad=whole_dur={SPLIT}[a];"
          f"[1:a]atrim=0:{l2:.3f},afade=t=in:d=0.4,afade=t=out:st={l2 - 0.6:.2f}:d=0.6[b];"
          "[a][b]concat=n=2:v=0:a=1[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc,
                    "-map", "[o]", "-t", f"{TOTAL:.3f}", str(FIT)], check=True)
    check_timeline_sweep(FIT)
    print(f"[done] {FIT}")


if __name__ == "__main__":
    main()
