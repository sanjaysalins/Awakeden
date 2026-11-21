"""ep13 wordsfix1 picture re-cut: trim only, 1.0x from clip frame 0, hard cuts. Fails closed if any clip < slot+0.05 s.
Same clips as the pinned fix1 film (fix1 clips copied to _wordsfix1/clips), same encode as uplift/cut_uplift.py.
F04, F05, F08, F09B are dropped (their baked words are no longer spoken). Writes work/base.mp4 (video only)."""
import subprocess
from pathlib import Path
H = Path(__file__).resolve().parent; EP = H.parent
WORK = H / "work"; WORK.mkdir(exist_ok=True)
U = EP / "uplift" / "clips"; C = EP / "_wordsfix1" / "clips"; NEWC = H / "clips"
FPS, W, Hh = 30, 1080, 1920
N = "swirls_episode_13_the_cross_that_wasnt_his"
SHOTS = [  # id, page, f0, f1, src
    ("S01", "front", 0, 148, U / "cover_5s.mp4"),
    ("S02", "F01", 148, 387, EP / f"{N}_f01_9x16.mp4"),
    ("S03", "F01B", 387, 453, U / "f01b_3s.mp4"),
    ("S04", "F02", 453, 691, EP / f"{N}_f02_9x16.mp4"),
    ("S05", "F02B", 691, 783, U / "f02b_4s.mp4"),
    ("S06", "F03", 783, 1021, EP / f"{N}_f03_9x16.mp4"),
    ("S07", "F03B", 1021, 1140, C / "f03b_fix.mp4"),
    ("S08", "F05B", 1140, 1288, C / "f05b_fix.mp4"),
    ("S09", "F06", 1288, 1586, EP / f"{N}_f06_9x16.mp4"),
    ("S10", "F06B", 1586, 1669, C / "f06b_fix.mp4"),
    ("S11", "F07", 1669, 1847, EP / f"{N}_f07_9x16.mp4"),
    ("S12", "F07B", 1847, 1971, U / "f07b_5s.mp4"),
    ("S13", "F09", 1971, 2208, NEWC / "f09_new.mp4"),
    ("S14", "back", 2208, 2470, NEWC / "back_new.mp4"),
]
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit("FAIL " + " ".join(map(str, c))[:160] + r.stderr[-500:])
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
VF = f"fps={FPS},scale={W}:{Hh}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{Hh},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-r", str(FPS)]
segs = []
for sid, page, f0, f1, src in SHOTS:
    n = f1 - f0; out = WORK / f"final_{sid}.mp4"
    d = dur(src)
    if d < n / FPS + 0.05: raise SystemExit(f"FAIL SHORT {src.name}: {d:.3f} < {n/FPS+0.05:.3f}")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", VF, "-frames:v", str(n), *ENC, str(out)])
    segs.append(out); print(sid, page, n, "frames", f"clip {d:.2f}s slack {d - n/FPS:.2f}s")
lst = WORK / "concat_final.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
base = WORK / "base.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
print("BASE", base, run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip(), "expected", SHOTS[-1][3])
