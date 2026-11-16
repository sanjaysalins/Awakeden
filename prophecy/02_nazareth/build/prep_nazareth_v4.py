"""prep_nazareth_v4.py - $0 prep for film v4: new clips S15..S18 -> _remotion/public/comic_nazareth (1080x1920 30fps), v4 pills (words v6 / new voice) -> pills_v4 + pills_v4.json.
  .venv\Scripts\python.exe prophecy/02_nazareth/build/prep_nazareth_v4.py"""
import sys, json, subprocess, math
from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
import prep_nazareth as V1
from prep_nazareth import PUB, EP, T, W, BA, ImageDraw

# (f0 sec, f1 sec, text, who, ref, jesus)
PL = [(0.10, 2.40, "Jesus stopped reading in the middle of a sentence.", None, None, False),
      (2.88, 4.55, "In Nazareth, His home town,", None, None, False),
      (4.60, 8.20, "He read God's promise of someone sent with good news for the poor,", None, None, False),
      (8.28, 9.60, "freedom for prisoners,", None, None, False),
      (9.68, 11.34, "and a time of God's welcome.", None, None, False),
      (11.54, 13.68, "The prophet Isaiah's sentence goes on:", None, None, False),
      (14.00, 16.62, "and the day of vengeance of our God.", "ISAIAH", "ISAIAH 61:2", False),
      (16.94, 20.01, "He left the day of vengeance unread, and sat down.", None, None, False),
      (20.85, 25.14, "This day is this scripture fulfilled in your ears.", "JESUS", "LUKE 4:21", True),
      (25.56, 27.21, "He knew what His town would say:", None, None, False),
      (27.55, 29.88, "Physician, heal thyself.", "JESUS", "LUKE 4:23", True),
      (30.00, 35.30, "He reminded them God once sent help to foreigners, not to them.", None, None, False),
      (35.40, 38.20, "Furious, they led Him to a cliff to throw Him down.", None, None, False),
      (38.36, 39.87, "He walked right through them.", None, None, False),
      (40.48, 43.06, "Later, at the cross, leaders mocked:", None, None, False),
      (43.36, 45.82, "He saved others; let him save himself.", "LEADER", "LUKE 23:35", False),
      (46.12, 49.64, "This time, He stayed, and gave His life.", None, None, False),
      (50.28, 52.70, "He stopped reading at the welcome.", None, None, False),
      (52.88, 56.08, "It is still open, for you, today.", None, None, False)]


def clips():
    for n in ("S15", "S16", "S17", "S18"):
        o = PUB / (n + ".mp4")
        if o.exists(): continue
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-stream_loop", "1", "-i", str(EP / "clips" / (n + ".mp4")), "-vf", "scale=1080:1920:flags=lanczos,fps=30", "-t", "12", "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", str(o)], check=True)


def pills():
    d = PUB / "pills_v4"; d.mkdir(exist_ok=True); out = []
    f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j)
        lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
        out.append(dict(png="pills_v4/p%02d.png" % i, f0=int(math.ceil(a * 30 - 1e-6)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=bool(j), text=text, lines=len(lines)))
    T.light_text(d / "hook.png", "HE STOPPED READING", 600, size=130, maxw=900)
    return out


if __name__ == "__main__":
    clips(); P = pills(); (HERE / "pills_v4.json").write_text(json.dumps(P, indent=1)); print("v4 assets ok", len(P), [p["lines"] for p in P])
