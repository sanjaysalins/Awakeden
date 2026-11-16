"""ep08 uplift: picture-only re-cut (trim only, 1.0x, hard cuts, one page turn).
Usage: python cut_uplift.py [--animatic]   (animatic = grey NEW SHOT slugs where a new clip is missing)
Writes uplift/work/base_{animatic|final}.mp4 (video only, 1921 frames). Audio is added in marks_overlay.py.
Fails closed if any clip is shorter than its slot + 0.05 s. Never edits episode files."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

EP = Path(__file__).resolve().parent.parent
UP = EP / "uplift"
WORK = UP / "work"
SPEC = json.loads(Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\pilot_ep08_uplift.json").read_text(encoding="utf-8"))
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

HOLD = {"S04": "f03", "S06": "f04"}   # animatic only: the approved still held static (marks can be judged on it)

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
shots = SPEC["shots"]
turn = SPEC["transitions"][0]
for sh in shots:
    f0, f1 = sh["f0"], sh["f1"]
    n = f1 - f0
    start = 0
    if sh["id"] == "S10":      # ends at the page-turn start
        n = turn["at"] - f0
    if sh["id"] == "S11":      # begins after the turn (clip plays continuously from frame 8)
        f0 = turn["at"] + turn["frames"]
        n = f1 - f0
        start = turn["frames"]
    out = WORK / f"{mode}_{sh['id']}.mp4"
    src = resolve(sh)
    if src.exists():
        trim(src, out, start, n)
        print(sh["id"], "clip", src.name, n, "frames")
    elif ANIM:
        slug(out, n, f"{sh['id']} {sh['page']}", HOLD.get(sh["id"]))
        print(sh["id"], "SLUG", n, "frames")
    else:
        raise SystemExit(f"FAIL missing clip for {sh['id']}: {src}")
    segs.append(out)
    if sh["id"] == "S10":
        # page turn segment: 8 frames built in marks_overlay via turn_{mode}.mp4 (outgoing S10 tail, incoming S11 head)
        turn_out = WORK / f"{mode}_TURN.mp4"
        s10, s11 = resolve(shots[9]), resolve(shots[10])
        o_src = s10 if s10.exists() else None
        # outgoing frames: S10 clip frames [turn.at - f0 .. +8)
        o_start = turn["at"] - shots[9]["f0"]
        o_png = WORK / f"{mode}_turn_out"; i_png = WORK / f"{mode}_turn_in"
        for d in (o_png, i_png):
            d.mkdir(exist_ok=True)
            for old in d.glob("*.png"):
                old.unlink()
        if o_src:
            run(["ffmpeg", "-y", "-v", "error", "-i", str(o_src), "-vf", f"fps={FPS},trim=start_frame={o_start}:end_frame={o_start + 8},setpts=PTS-STARTPTS,{VF.split(',', 1)[1]}", "-frames:v", "8", str(o_png / "%02d.png")])
        else:
            for k in range(8):
                Image.new("RGB", (W, H), (150, 150, 150)).save(o_png / f"{k + 1:02d}.png")
        if s11.exists():
            run(["ffmpeg", "-y", "-v", "error", "-i", str(s11), "-vf", VF, "-frames:v", "8", str(i_png / "%02d.png")])
        else:
            for k in range(8):
                Image.new("RGB", (W, H), (150, 150, 150)).save(i_png / f"{k + 1:02d}.png")
        # S7: outgoing page slides left 104% with 3 degree tilt + soft shadow over the incoming page
        from PIL import ImageFilter
        for k in range(8):
            t = (k + 1) / 8.0
            e = t * t * (3 - 2 * t)
            inc = Image.open(i_png / f"{k + 1:02d}.png").convert("RGBA")
            outp = Image.open(o_png / f"{k + 1:02d}.png").convert("RGBA")
            ang = 3 * e
            rot = outp.rotate(ang, resample=Image.BICUBIC, expand=False, center=(0, H), fillcolor=(0, 0, 0, 0))
            dx = -int(1.04 * W * e)          # page left edge x; its right edge is at W + dx
            canvas = inc.copy()
            edge = W + dx
            if edge > 0:
                sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(sh2).rectangle([edge, 0, edge + 30, H], fill=(0, 0, 0, 120))
                canvas.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(18)))
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                layer.paste(rot.crop((-dx, 0, W, H)), (0, 0))
                canvas.alpha_composite(layer)
            canvas.convert("RGB").save(WORK / f"{mode}_turn_{k:02d}.png")
        run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(WORK / f"{mode}_turn_%02d.png"), *ENC, str(turn_out)])
        segs.append(turn_out)

lst = WORK / f"concat_{mode}.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
base = WORK / f"base_{mode}.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
n = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip()
print("BASE", base, "frames", n, "expected", SPEC["total_frames"])
