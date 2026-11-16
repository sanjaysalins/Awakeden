"""ep02 uplift: picture-only re-cut (trim only, 1.0x, hard cuts, one page turn).
Usage: python cut_uplift.py [--animatic]   (animatic = grey NEW SHOT slugs where a new clip is missing)
Writes uplift/work/base_{animatic|final}.mp4 (video only, 1921 frames). Audio is added in marks_overlay.py.
Fails closed if any clip is shorter than its slot + 0.05 s. Never edits episode files."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"
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

def trim(src, out, start_frame, n):
    """play src from its frame `start_frame` at 1.0x for n frames. Closed if clip too short."""
    d = dur(src)
    need = (start_frame + n) / FPS + 0.05
    if d < need:
        raise SystemExit(f"FAIL SHORT CLIP {src.name}: {d:.3f}s < need {need:.3f}s")

    # clips can be 24 fps: do the offset in source time for the page-turn tail only
    if start_frame:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", f"fps={FPS},trim=start_frame={start_frame},setpts=PTS-STARTPTS,{VF.split(',', 1)[1]}",
             "-frames:v", str(n), *ENC, str(out)])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", VF, "-frames:v", str(n), *ENC, str(out)])

HOLD = {}   # animatic only: the approved still held static (marks can be judged on it)

def slug(out, n, label, hold=None):
    png = WORK / "slug.png"
    if hold:
        Image.open(EP / f"swirls_episode_08_can_any_good_thing_{hold}_9x16.png").convert("RGB").resize((W, 1936), Image.LANCZOS).crop((0, 8, W, 1928)).save(png)
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-frames:v", str(n), *ENC, str(out)])
        return
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

def resolve(shot):
    s = shot["src"]
    p = (EP / s).resolve() if not Path(s).is_absolute() else Path(s)
    if s.startswith("uplift/clips/"):
        p = EP / s
    return p

segs = []
for sh in SPEC["shots"]:
    f0, f1 = sh["f0"], sh["f1"]
    n = f1 - f0
    out = WORK / f"{mode}_{sh['id']}.mp4"
    src = resolve(sh)
    if src.exists():
        trim(src, out, 0, n)
        print(sh["id"], "clip", src.name, n, "frames")
    elif ANIM:
        slug(out, n, f"{sh['id']} {sh['page']}", None)
        print(sh["id"], "SLUG", n, "frames")
    else:
        raise SystemExit(f"FAIL missing clip for {sh['id']}: {src}")
    segs.append(out)

lst = WORK / f"concat_{mode}.txt"
lst.write_text("".join("file '" + p.as_posix() + "'\n" for p in segs), encoding="utf-8")
base = WORK / f"base_{mode}.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
n = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip()
print("BASE", base, "frames", n, "expected", SPEC["total_frames"])
