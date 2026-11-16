"""prep_nazareth.py - $0 prep: clips -> 1080x1920 30fps in _remotion/public/comic_nazareth (S13 gets a sepia memory tint), pill + hook PNGs, pills.json.
  .venv\Scripts\python.exe prophecy/02_nazareth/build/prep_nazareth.py [--force S13]"""
import sys, json, subprocess
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); EL = ROOT / "poc_comic_page/_ELEVATE"
sys.path.insert(0, str(EL))
import build_tp as T, build_w3 as W, build_arms as BA
from PIL import ImageDraw
EP = ROOT / "prophecy/02_nazareth"; PUB = ROOT / "_remotion/public/comic_nazareth"
SEPIA = "colorchannelmixer=.50:.55:.12:0:.40:.52:.12:0:.30:.42:.10,eq=brightness=0.02:contrast=1.05,"
# (f0 sec, f1 sec, text, who, ref, jesus)
PL = [(0.10, 2.6, "Jesus stopped reading in the middle of a sentence.", None, None, False),
      (2.96, 4.5, "In Nazareth, His home town,", None, None, False),
      (4.9, 8.3, "He stood to read from the prophet Isaiah, written long before.", None, None, False),
      (9.44, 12.9, "He read God's promise of someone sent with good news for the poor,", None, None, False),
      (13.18, 14.3, "freedom for prisoners,", None, None, False),
      (14.5, 16.1, "and a time of God's welcome.", None, None, False),
      (16.82, 18.2, "Then He rolled up the scroll.", None, None, False),
      (18.96, 20.4, "Isaiah's sentence goes on:", None, None, False),
      (20.9, 23.3, "and the day of vengeance of our God.", "ISAIAH", "ISAIAH 61:2", False),
      (23.5, 26.4, "He left the day of vengeance unread, and sat down.", None, None, False),
      (27.28, 29.0, "Every eye was on Him.", None, None, False),
      (29.62, 34.2, "This day is this scripture fulfilled in your ears.", "JESUS", "LUKE 4:21", True),
      (34.44, 36.6, "The people were amazed at His kind words.", None, None, False),
      (37.14, 38.6, "They knew Him as a local boy.", None, None, False),
      (39.56, 42.3, "Is not this Joseph's son?", "A TOWNSMAN", "LUKE 4:22", False),
      (42.34, 45.7, "That local boy was saying Isaiah's promise was about Him.", None, None, False),
      (46.76, 49.6, "He stopped reading at God's welcome, and said:", None, None, False),
      (49.7, 51.5, "This day.", None, None, False)]


def clips(force=()):
    PUB.mkdir(parents=True, exist_ok=True)
    for i in range(1, 15):
        n = "S%02d" % i; o = PUB / (n + ".mp4")
        if o.exists() and n not in force: continue
        vf = (SEPIA if n == "S13" else "") + "scale=1080:1920:flags=lanczos,fps=30"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-threads", "2", "-stream_loop", "1", "-i", str(EP / "clips" / (n + ".mp4")), "-vf", vf, "-t", "12", "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-g", "15", "-pix_fmt", "yuv420p", str(o)], check=True)


def pills():
    d = PUB / "pills"; d.mkdir(exist_ok=True); out = []
    f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j)
        lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
        out.append(dict(png="pills/p%02d.png" % i, f0=int(-(-a * 30 // 1)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=bool(j), text=text, lines=len(lines)))
    T.light_text(d / "hook.png", "HE STOPPED READING", 600, size=130, maxw=900)
    return out


if __name__ == "__main__":
    force = set(sys.argv[sys.argv.index("--force") + 1:]) if "--force" in sys.argv else set()
    clips(force); P = pills(); (Path(__file__).parent / "pills.json").write_text(json.dumps(P, indent=1)); print("assets ok", len(P))
