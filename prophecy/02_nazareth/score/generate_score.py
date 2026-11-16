r"""CINEMATIC score for Prophecy 02 "He stopped mid-sentence" (words v6, film v5 59.1 s). Owner yes ~$0.90 cap $2.00, 2026-11-16.
Blind panel score_panel_v6 (fable + claude/codex/grok) merged -> MERGED_PLAN.md. 2 parts split 40.2 s (cliff -> cross pause), 0.3 s crossfade.
  F:\slk\PycharmProjects\JesusInTheBible\.venv\Scripts\python.exe generate_score.py [--join-only]"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from pipeline.assembly_align import _resolve_key  # noqa: E402
from generate_score_piano import check_no_dead_intro, check_timeline_sweep  # noqa: E402
from generate_score_v2 import gen_music  # noqa: E402
P1, P2, FIT = HERE / "part1_raw.mp3", HERE / "part2_raw.mp3", HERE / "score.mp3"
TOTAL, SPLIT, XF = 59.1, 40.2, 0.3
PART1 = 'Cinematic orchestral film score, instrumental only, D major, slow 64 bpm, warm, tender and reverent, continuous sound with no silence or gaps anywhere. Solo cello leads, warm string orchestra, concert harp. No choir, no vocals, no piano, no brass, no drums, no percussion hits, no Middle Eastern scales, no trailer sounds. Begins at once with a solo cello playing four slow rising notes, D, E, F sharp, A, that stop unfinished on the A over a soft held string note. Around 3 seconds in, warm strings and gentle harp enter, hopeful and golden. Around 9 seconds in, a small warm lift. Around 12 seconds in, the melody stops and the strings thin to a hushed, solemn low chord, grave but never scary. Around 17 seconds in, the cello plays the same four rising notes again and stops unfinished on the A. Around 20 seconds in, only one very quiet, high, still string note continues for five seconds. Around 26 seconds in, low strings return with a quiet questioning feel. Around 30 seconds in, harp and cello play the four rising notes again, kind and warm, still unfinished. Around 35 seconds in, the strings move forward with a soft urgent pulse, lyrical, never dark. Around 38 seconds in, the pulse falls away to one calm, warm held D major string chord that sustains to the end.'
PART2 = 'Cinematic orchestral film score, instrumental only, D major, slow 60 bpm, reverent and full of grace, continuous sound with no silence or gaps anywhere. Solo cello, warm string orchestra, concert harp, one French horn near the end. No choir, no vocals, no piano, no drums, no percussion, no trailer hits, no horror stabs. Begins at once with low, bare, slow sustained strings on D, quiet and still. Around 6 seconds in, the solo cello plays four slow rising notes, D, E, F sharp, A, and stops unfinished. Around 10 seconds in, harp and cello begin the four rising notes again with a slow golden swell of strings. Around 16 seconds in, the cello finally plays the fifth note, the high D, home, and a French horn joins on a full warm D major chord, held and ringing to the very end with no fade.'
key = _resolve_key() or sys.exit("no ELEVENLABS_API_KEY")
l2 = TOTAL - SPLIT + XF / 2
if "--join-only" not in sys.argv:
    gen_music(PART1, 48.0, P1, key)  # +7 s: generator fades its own last ~5 s (take1 lesson)
    gen_music(PART2, 27.0, P2, key)  # +7 s spare
fc = (f"[0:a]atrim=0:{SPLIT + XF / 2:.3f}[a];[1:a]atrim=0:{l2:.3f},afade=t=out:st={l2 - 2.6:.2f}:d=2.6[b];"  # gentle 2.6 s end fade (owner: end felt abrupt)
      f"[a][b]acrossfade=d={XF}:c1=tri:c2=tri[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(P1), "-i", str(P2), "-filter_complex", fc, "-map", "[o]", "-t", f"{TOTAL:.3f}", str(FIT)], check=True)
check_timeline_sweep(FIT)
print("[done]", FIT)
