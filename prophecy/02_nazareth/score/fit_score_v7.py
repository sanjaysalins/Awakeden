r"""$0 re-fit of the SAME paid parts (part1_raw.mp3 48 s, part2_raw.mp3 27 s from generate_score.py) to words v7 / narration_v7.mp3 (59.85 s).
Split moves to the cliff->cross pause 39.82-40.32 (centre 40.07). Gentle 2.6 s end fade (owner rule). -> score_v7.mp3"""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "poc_folk_print_style"))
from generate_score_piano import check_timeline_sweep  # noqa: E402
TOTAL, SPLIT, XF = 59.85, 40.07, 0.3
l2 = TOTAL - SPLIT + XF / 2
fc = (f"[0:a]atrim=0:{SPLIT + XF / 2:.3f}[a];[1:a]atrim=0:{l2:.3f},afade=t=out:st={l2 - 2.6:.2f}:d=2.6[b];"  # gentle end fade
      f"[a][b]acrossfade=d={XF}:c1=tri:c2=tri[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(H / "part1_raw.mp3"), "-i", str(H / "part2_raw.mp3"), "-filter_complex", fc,
                "-map", "[o]", "-t", f"{TOTAL:.3f}", str(H / "score_v7.mp3")], check=True)
check_timeline_sweep(H / "score_v7.mp3")
print("[done] score_v7.mp3")
