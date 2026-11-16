"""ep13 uplift picture re-cut: trim only, 1.0x from clip frame 0, hard cuts. Fails closed if any clip < slot+0.05 s.
python cut_uplift.py [--animatic]  (animatic: grey slug where a new clip is missing). Writes work/base_<mode>.mp4 (video only)."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
EP = Path(__file__).resolve().parent.parent
WORK = EP / "uplift" / "work"; WORK.mkdir(exist_ok=True)
SPEC = json.loads((EP / "uplift" / "uplift.json").read_text())
FPS, W, H = 30, 1080, 1920
MODE = "animatic" if "--animatic" in sys.argv else "final"
def run(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit("FAIL " + " ".join(map(str, c))[:160] + r.stderr[-500:])
    return r.stdout
def dur(p): return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
VF = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-r", str(FPS)]
segs = []
for s in SPEC["shots"]:
    n = s["f1"] - s["f0"]; src = EP / s["src"]; out = WORK / f"{MODE}_{s['id']}.mp4"
    if src.exists():
        d = dur(src)
        if d < n / FPS + 0.05: raise SystemExit(f"FAIL SHORT {src.name}: {d:.3f} < {n/FPS+0.05:.3f}")
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", VF, "-frames:v", str(n), *ENC, str(out)])
    elif MODE == "animatic":
        png = WORK / "slug.png"; im = Image.new("RGB", (W, H), (150, 150, 150)); ImageDraw.Draw(im).text((300, 900), "NEW SHOT " + s["page"], fill=(30, 30, 30)); im.save(png)
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-frames:v", str(n), *ENC, str(out)])
    else: raise SystemExit(f"FAIL missing {src}")
    segs.append(out); print(s["id"], s["page"], n, "frames", "clip" if src.exists() else "SLUG")
lst = WORK / f"concat_{MODE}.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
base = WORK / f"base_{MODE}.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
print("BASE", base, run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip(), "expected", SPEC["total_frames"])
