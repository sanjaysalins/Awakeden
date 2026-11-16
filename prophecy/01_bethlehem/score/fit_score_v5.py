"""Fit the locked score (score.mp3, made for the words-v2 timing) to the words-v3 voice ($0, no re-generation).
The score's own split (37.0 s, inside the planned silence) maps through the warp; each part gets one gentle atempo.
-> score_v5.mp3 (59.5 s)."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parent / "motion_v5"))
from warp import o2n
SRC, OUT, T = H / "score.mp3", H / "score_v5.mp3", 59.5
SPLIT_OLD, END_OLD = 37.0, 59.31
s_new = o2n(SPLIT_OLD)
t1 = SPLIT_OLD / s_new                      # atempo for part 1
t2 = (END_OLD - SPLIT_OLD) / (T - s_new)    # atempo for part 2
print(f"split old {SPLIT_OLD} -> new {s_new:.2f}; atempo part1 {t1:.3f}, part2 {t2:.3f}")
assert 0.85 < t1 < 1.15 and 0.85 < t2 < 1.15, "tempo change too big"
fc = (f"[0:a]atrim=0:{SPLIT_OLD},asetpts=N/SR/TB,atempo={t1:.4f}[a];"
      f"[0:a]atrim={SPLIT_OLD}:{END_OLD},asetpts=N/SR/TB,atempo={t2:.4f}[b];"
      "[a][b]concat=n=2:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-filter_complex", fc, "-map", "[o]", "-t", f"{T}", str(OUT)], check=True)
print(OUT)
