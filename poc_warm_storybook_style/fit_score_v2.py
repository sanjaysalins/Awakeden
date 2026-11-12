"""$0 refit of the paid score onto the tighter v2 film (words G, 71.61 s). No new music.
Part 1 = try 1 (E major) audible run from 16.2 s, no repeated opening phrase (v1 needed it, v2 is shorter),
ends on its open questioning phrase at 50.4 s ("So, did He care?"). Part 2 = the paid part 2 (E minor),
whose warm chord lands ~4.9 s in = ~55.3 s ("Now Jesus loved Martha" 55.41 s). 0.4 s crossfade."""
import subprocess
from pathlib import Path
from generate_score_piano import check_no_dead_intro, check_timeline_sweep, dur
H = Path(__file__).resolve().parent
T1, P2 = H / "_score_rejected" / "part1_try1_dead16s.mp3", H / "score_piano_part2_raw.mp3"
VID, OUT = H / "MARY_MARTHA_PREVIEW_v2.mp4", H / "score_piano_v2.mp3"
SPLIT, XF = 50.40, 0.4
total = dur(VID)
fc = (f"[0:a]atrim=16.2:{16.2 + SPLIT + XF:.2f},asetpts=PTS-STARTPTS[a];"
      f"[1:a]atrim=0:{total - SPLIT:.2f},asetpts=PTS-STARTPTS[b];"
      f"[a][b]acrossfade=d={XF}:c1=tri:c2=tri,afade=t=in:st=0:d=1.0,afade=t=out:st={total - 2.0:.2f}:d=2.0[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "3", "-i", str(T1), "-i", str(P2),
                "-filter_complex", fc, "-map", "[o]", "-t", f"{total:.2f}", str(OUT)], check=True)
check_no_dead_intro(OUT)
try:
    check_timeline_sweep(OUT)
except SystemExit as e:
    print("  [note]", e)  # last window = the planned 2 s fade-out
print(f"{OUT} {dur(OUT):.2f}s (film {total:.2f}s)")
