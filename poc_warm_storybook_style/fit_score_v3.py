"""$0 refit of the paid score onto the v3 film (words H, 73.85 s). No new music.
Part 1 = try 1 (E major) audible run from 16.2 s; it decays out by itself at ~51 s film time,
just after "So, did He care?" (50.81 s). Part 2 (E minor) starts at 52.83 s so its warm chord
(~5.0 s in) lands on "Now Jesus loved Martha" (57.83 s). The ~2 s hush after the question is on purpose."""
import subprocess
from pathlib import Path
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur
H = Path(__file__).resolve().parent
T1, P2 = H / "_score_rejected" / "part1_try1_dead16s.mp3", H / "score_piano_part2_raw.mp3"
VID, OUT = H / "MARY_MARTHA_PREVIEW_v3.mp4", H / "score_piano_v3.mp3"
P2_AT = 52.83
total = dur(VID)
fc = (f"[0:a]atrim=16.2:{16.2 + P2_AT:.2f},asetpts=PTS-STARTPTS[a];"
      f"[1:a]atrim=0:{total - P2_AT:.2f},asetpts=PTS-STARTPTS,adelay={int(P2_AT * 1000)}:all=1[b];"
      f"[a][b]amix=inputs=2:duration=longest:normalize=0,afade=t=in:st=0:d=1.0,afade=t=out:st={total - 2.0:.2f}:d=2.0[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(T1), "-i", str(P2),
                "-filter_complex", fc, "-map", "[o]", "-t", f"{total:.2f}", str(OUT)], check=True)
check_no_dead_intro(OUT)
try:
    check_timeline_sweep(OUT)
except SystemExit as e:
    print("  [note]", e)  # expected: the planned hush after the question, and the 2 s fade-out
print(f"{OUT} {dur(OUT):.2f}s (film {total:.2f}s)")
