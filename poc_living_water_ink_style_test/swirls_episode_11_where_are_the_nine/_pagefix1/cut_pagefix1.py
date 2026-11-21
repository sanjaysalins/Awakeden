"""ep11 uplift: picture-only re-cut (trim only, 1.0x, hard cuts). Usage: python cut_uplift.py
Writes work/base_final.mp4 (video only). Fails closed if any clip < slot + 0.05 s. Never edits episode files."""
import json, subprocess, sys
from pathlib import Path
EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"; WORK = EP / "_pagefix1" / "work"
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
FPS, W, H = 30, 1080, 1920
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit("FAIL: " + " ".join(map(str, cmd))[:200] + "\n" + r.stderr[-800:])
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
VF = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-r", str(FPS)]
segs = []
for sh in SPEC["shots"]:
    n = sh["f1"] - sh["f0"]; src = (EP / "_pagefix1" / "clips" / "f10b_new.mp4") if sh["id"] == "S16" else EP / sh["src"]
    if not src.exists(): raise SystemExit(f"FAIL missing clip {src}")
    d = dur(src)
    if d < n / FPS + 0.05: raise SystemExit(f"FAIL SHORT CLIP {src.name}: {d:.3f}s < {n/FPS+0.05:.3f}s")
    out = WORK / f"final_{sh['id']}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", VF, "-frames:v", str(n), *ENC, str(out)])
    print(sh["id"], src.name, n, "frames"); segs.append(out)
lst = WORK / "concat_final.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
base = WORK / "base_final.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
print("BASE", base, run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip(), "expected", SPEC["total_frames"])
