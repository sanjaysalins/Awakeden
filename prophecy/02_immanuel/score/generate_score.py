"""Score for Prophecy 02 "Immanuel" (words v2, film 63.80 s). Owner yes ~$0.90, 2026-11-16.
Blind panel ../score_panel: fable/claude/codex/grok_score.md. Convergence 4/4: rising 4-note tune left unfinished until
the final hold; dark (minor) -> warm (major) turn at 'Joseph obeyed' (~43.7); sacred/still at the cross; one swell on
'He rose' (55.1). Split 43.5 (fable+claude) so the key change is certain. Prompts = Fable seat (closest to convergence).
Dips under the KJV lines are done in the MIX (dead-air lesson): prompts ask for continuous sound."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402
P1, P2, FIT = HERE / "part1_raw.mp3", HERE / "part2b_raw.mp3", HERE / "score.mp3"
# v2 fix (owner yes ~$0.45): part1 starts 4.0 s in (quiet intro); part1 is live only to ~40.5 s so the film uses part1 4.0-40.5
# (film 0-36.5), then a NEW longer part 2 (32 s asked, ~27 s live) from film 36.5, cues shifted so the warm turn lands at
# "Joseph obeyed" (43.65 = 7.1 s in) and the tune resolves on "That was God's answer." (~60 = 23.5 s in), ringing to 63.8.
TOTAL, OFF1, SPLIT, XF = 65.44, 2.5, 38.0, 0.6  # v2.2: film 65.44; part1 from 2.5 s so it stays live to the split; turn ~45 s
PART1 = ("Cinematic orchestral film underscore, instrumental only, 60 BPM, D minor. Quiet, tense, uneasy but never horror. "
 "Starts at once with a low sustained cello and bass note and a solo cello playing a slow four-note rising phrase that does "
 "not resolve. Around 4 seconds in, a slow soft low string pulse begins with violas holding a tight unsure chord. Around 12 "
 "seconds in, the pulse grows slightly more urgent, with one single soft timpani hit around 14 seconds in. Around 17 seconds "
 "in, everything thins to very soft high sustained violins and a gentle harp, calm and open. Around 24 seconds in, gentle "
 "harp steps and warm violas, tender, still minor. Around 31 seconds in, a soft glowing sustained string pad, no pulse, no "
 "melody, peaceful. Around 41 seconds in, strings rise gently, unresolved. Continuous sound, no silence, no choir, no "
 "vocals, no drums, no brass hits, no ethnic scales.")
PART2 = ("Cinematic orchestral film underscore, instrumental only, 60 BPM, D major. Warm, hopeful, sacred. Starts at once "
 "very quiet: soft held high strings and a gentle harp, still and reverent, under a spoken voice. Around 7 seconds in, warm "
 "full soft strings enter and a French horn plays a slow four-note rising melody, hopeful. Around 15 seconds in, drops to "
 "low sustained strings alone, very still and reverent, with one soft low timpani beat. Around 18 seconds in, one warm "
 "swell: full strings and French horns rise together on the melody. Around 21 seconds in, the swell falls back to a soft "
 "held unresolved chord. Around 23 seconds in, the melody completes and resolves home to a full warm final major chord. "
 "The final chord keeps ringing, held by strings and horns, still clearly sounding at 30 seconds. Continuous sound, no "
 "silence, no choir, no vocals, no drums, no trailer hits, no ethnic scales.")
def main() -> None:
    key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
    l2 = TOTAL - SPLIT
    if "--join-only" not in sys.argv:
        gen_music(PART1, 46.0, P1, key)
        gen_music(PART2, 32.0, P2, key)
    for p in (P1, P2): check_no_dead_intro(p)
    fc = (f"[0:a]atrim={OFF1}:{OFF1 + SPLIT + XF:.3f},asetpts=PTS-STARTPTS[a];[1:a]atrim=0:{l2:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={l2 - 2.6:.2f}:d=2.6[b];"
          f"[a][b]acrossfade=d={XF}:c1=qsin:c2=qsin[o]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc,
                    "-map", "[o]", "-t", f"{TOTAL:.3f}", str(FIT)], check=True)
    check_timeline_sweep(FIT)
    print(f"[done] {FIT}")
if __name__ == "__main__":
    main()
