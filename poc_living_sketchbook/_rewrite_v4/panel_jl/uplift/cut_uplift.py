"""JL uplift: picture-only re-cut (trim only, 1.0x, hard cuts, one page turn S08->S09).
Writes work/base_final.mp4 (video only, 1695 frames). Audio added in marks_overlay.py (stream copy).
Fails closed if any clip is shorter than its slot + 0.05 s."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

UP = Path(__file__).resolve().parent
WORK = UP / "work"
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
FPS, W, H = 30, 1080, 1920

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("FAIL: " + " ".join(map(str, cmd))[:200] + "\n" + r.stderr[-800:])
    return r.stdout

def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

TAIL = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", "-r", str(FPS)]

def resolve(s):
    p = Path(s["src"])
    return p if p.is_absolute() else UP / p

def trim(src, out, start_frame, n):
    need = (start_frame + n) / FPS + 0.05
    d = dur(src)
    if d < need:
        raise SystemExit(f"FAIL SHORT CLIP {src.name}: {d:.3f}s < need {need:.3f}s")
    vf = f"fps={FPS}," + (f"trim=start_frame={start_frame},setpts=PTS-STARTPTS," if start_frame else "") + TAIL
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-frames:v", str(n), *ENC, str(out)])

def frames_png(src, start, count, folder):
    folder.mkdir(exist_ok=True)
    for old in folder.glob("*.png"): old.unlink()
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", f"fps={FPS},trim=start_frame={start}:end_frame={start + count},setpts=PTS-STARTPTS,{TAIL}",
         "-frames:v", str(count), str(folder / "%02d.png")])

segs = []
shots = SPEC["shots"]; T = SPEC["transition"]; TF = T["frames"]
for sh in shots:
    f0, f1 = sh["f0"], sh["f1"]; n = f1 - f0; start = 0
    if sh["id"] == T["from"]: n = T["at"] - f0
    if sh["id"] == T["to"]: f0 = T["at"] + TF; n = f1 - f0; start = TF
    src = resolve(sh)
    if not src.exists(): raise SystemExit(f"FAIL missing clip for {sh['id']}: {src}")
    out = WORK / f"final_{sh['id']}.mp4"
    trim(src, out, start, n)
    print(sh["id"], src.name, n, "frames"); segs.append(out)
    if sh["id"] == T["from"]:
        s_to = resolve(next(x for x in shots if x["id"] == T["to"]))
        o_start = T["at"] - sh["f0"]
        need = (o_start + TF) / FPS + 0.05
        if dur(src) < need: raise SystemExit(f"FAIL SHORT for turn {src.name}")
        o_png, i_png = WORK / "final_turn_out", WORK / "final_turn_in"
        frames_png(src, o_start, TF, o_png); frames_png(s_to, 0, TF, i_png)
        for k in range(TF):
            t = (k + 1) / TF; e = t * t * (3 - 2 * t)
            inc = Image.open(i_png / f"{k + 1:02d}.png").convert("RGBA")
            outp = Image.open(o_png / f"{k + 1:02d}.png").convert("RGBA")
            rot = outp.rotate(3 * e, resample=Image.BICUBIC, expand=False, center=(0, H), fillcolor=(0, 0, 0, 0))
            dx = -int(1.04 * W * e); canvas = inc.copy(); edge = W + dx
            if edge > 0:
                sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(sh2).rectangle([edge, 0, edge + 30, H], fill=(0, 0, 0, 120))
                canvas.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(18)))
                layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layer.paste(rot.crop((-dx, 0, W, H)), (0, 0))
                canvas.alpha_composite(layer)
            canvas.convert("RGB").save(WORK / f"final_turn_{k:02d}.png")
        t_out = WORK / "final_TURN.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(WORK / "final_turn_%02d.png"), *ENC, str(t_out)])
        segs.append(t_out)

lst = WORK / "concat_final.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
base = WORK / "base_final.mp4"
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(base)])
n = run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(base)]).strip()
print("BASE", base, "frames", n, "expected", SPEC["total_frames"])
