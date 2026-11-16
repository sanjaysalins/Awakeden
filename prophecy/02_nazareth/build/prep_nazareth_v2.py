"""prep_nazareth_v2.py - $0 prep for film v2: warm S13 (no grey/sepia tint, light warm vignette) as S13w.mp4, v2 pills (new audio times + new last line)
into _remotion/public/comic_nazareth/pills_v2, pills_v2.json. Clips S01..S14 (and the new S02/S13 art) are shared with v1.
  .venv\\Scripts\\python.exe prophecy/02_nazareth/build/prep_nazareth_v2.py"""
import sys, json, subprocess
from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
import prep_nazareth as V1
from prep_nazareth import PUB, EP, T, W, BA, ImageDraw

PL = list(V1.PL)
PL[11] = (29.60, 34.2, PL[11][2], "JESUS", "LUKE 4:21", True)
PL[13] = (37.06, 38.6) + PL[13][2:]
PL[14] = (39.54, 42.3) + PL[14][2:]
PL[16] = (46.76, 49.8) + PL[16][2:]
PL[17] = (49.92, 51.64, "This day.", None, None, False)
PL.append((52.34, 56.1, "His welcome is still open, for you, today.", None, None, False))


def clip():
    o = PUB / "S13w.mp4"
    if o.exists(): return
    vf = "colorchannelmixer=rr=1.05:gg=1.0:bb=0.92,eq=saturation=1.08:brightness=0.01,vignette=angle=PI/5,scale=1080:1920:flags=lanczos,fps=30"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-stream_loop", "1", "-i", str(EP / "clips/S13.mp4"), "-vf", vf, "-t", "12", "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", str(o)], check=True)


def pills():
    d = PUB / "pills_v2"; d.mkdir(exist_ok=True); out = []
    f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j)
        lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
        out.append(dict(png="pills_v2/p%02d.png" % i, f0=int(-(-a * 30 // 1)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=bool(j), text=text, lines=len(lines)))
    T.light_text(d / "hook.png", "HE STOPPED READING", 600, size=130, maxw=900)
    return out


if __name__ == "__main__":
    clip(); P = pills(); (HERE / "pills_v2.json").write_text(json.dumps(P, indent=1)); print("v2 assets ok", len(P))
