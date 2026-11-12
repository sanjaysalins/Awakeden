"""$0 rescue of score part 1 (2026-11-12). Try 1 = E major (matches part 2, E minor) but silent 0-16.2 s;
try 2 = F major (clashes) and silent after 42.9 s. So: try 1's audible 16.2-31.0 s phrase, then try 1
again from 16.2 s to 67.2 s, 1.0 s crossfade at a quiet dip (31 s) -> ~64.8 s part 1."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
T1 = H / "_score_rejected" / "part1_try1_dead16s.mp3"
OUT = H / "score_piano_part1_raw.mp3"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(T1), "-i", str(T1), "-filter_complex",
                "[0:a]atrim=16.2:31.0,asetpts=PTS-STARTPTS[a];[1:a]atrim=16.2:67.2,asetpts=PTS-STARTPTS[b];"
                "[a][b]acrossfade=d=1.0:c1=tri:c2=tri", "-threads", "3", str(OUT)], check=True)
print(OUT)
