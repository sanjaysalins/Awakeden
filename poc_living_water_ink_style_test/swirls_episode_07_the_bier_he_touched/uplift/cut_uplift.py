"""ep07 uplift: picture-only re-cut (trim only from each clip's frame 0, 1.0x, hard cuts, no fill).
Usage: python cut_uplift.py [--animatic]   (animatic = grey NEW SHOT slugs where a new clip is missing)
Writes uplift/work/base_{animatic|final}.mp4 (video only). Fails closed if any clip < slot + 0.05 s."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

UP = Path(__file__).resolve().parent
EP = UP.parent
WORK = UP / "work"
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
FPS, W, H = 30, 1080, 1920
ANIM = "--animatic" in sys.argv
mode = "animatic" if ANIM else "final"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("FAIL: " + " ".join(map(str, cmd))[:200] + "\n" + r.stderr[-800:])
    return r.stdout

def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

VF = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-r", str(FPS)]

def trim(src, out, n):
    d = dur(src)
    if d < n / FPS + 0.05:
        raise SystemExit(f"FAIL SHORT CLIP {src.name}: {d:.3f}s < need {n / FPS + 0.05:.3f}s")
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", VF, "-frames:v", str(n), *ENC, str(out)])

def slug(out, n, label):
    png = WORK / "slug.png"
    im = Image.new("RGB", (W, H), (150, 150, 150))
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("arial.ttf", 90)
    except Exception:
        f = ImageFont.load_default()
    d.text((W // 2, H // 2 - 60), "NEW SHOT", fill=(40, 40, 40), font=f, anchor="mm")
    d.text((W // 2, H // 2 + 60), label, fill=(40, 40, 40), font=f, anchor="mm")
    im.save(png)
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-frames:v", str(n), *ENC, str(out)])

segs = []
for sh in SPEC["shots"]:
    n = sh["f1"] - sh["f0"]
    src = EP / sh["src"]
    out = WORK / f"{mode}_{sh['id']}.mp4"
    if src.exists():
        trim(src, out, n)
        print(sh["id"], "clip", src.name, n, "frames")
    elif ANIM:
        slug(out, n, f"{sh['id']} {sh['page']}")
        print(sh["id"], "SLUG", n, "frames")
    else:
        raise SystemExit(f"FAIL missing clip for {sh['id']}: {src}")
    segs.append(out)
lst = WORK / f"concat_{mode}.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
base = WORK / f"base_{mode}.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
n = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip()
print("BASE", base, "frames", n, "expected", SPEC["total_frames"])
