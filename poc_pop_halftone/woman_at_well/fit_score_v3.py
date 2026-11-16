"""Fit the locked score to the v3 film (91.04 s) for $0, no new generation.
Part 1: repeat one whole bar (41.30-43.71 s, downbeat to downbeat, 100 BPM) in the soft section, so the hush
lands on "I that speak" (+2.09 s in the film; +2.41 s bar, the extra 0.32 s falls in the pause).
Part 2 then starts at 56.71 s and runs to the end (34.33 s of the 39.6 s take). Same crossfade/fade as v1."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; S = H / "score"
sys.path.insert(0, str(H.parents[1] / "poc_folk_print_style")); sys.path.insert(0, str(H.parents[1]))
from generate_score_piano import check_timeline_sweep, dur  # noqa: E402
END, XF, A, B = 91.04, 0.5, 41.30, 43.71
SPLIT = 54.3 + (B - A)
run = lambda *a: subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
fc = (f"[0:a]atrim=0:{B},asetpts=PTS-STARTPTS[x];[0:a]atrim={A},asetpts=PTS-STARTPTS[y];"
      f"[x][y]acrossfade=d=0.03:c1=tri:c2=tri,atrim=0:{SPLIT + XF:.2f}[p1];"
      f"[1:a]atrim=0:{END - SPLIT:.2f},asetpts=PTS-STARTPTS[p2];[p1][p2]acrossfade=d={XF}:c1=tri:c2=tri,"
      f"apad=whole_dur={END},afade=t=out:st={END - 1.2:.2f}:d=1.2,atrim=0:{END}[o]")
run("-i", str(S / "part1_raw.mp3"), "-i", str(S / "part2_raw.mp3"), "-filter_complex", fc, "-map", "[o]", str(S / "score_v3.mp3"))
print("score_v3", round(dur(S / "score_v3.mp3"), 2), "split", SPLIT)
check_timeline_sweep(S / "score_v3.mp3")
