"""prep_nazareth_v6.py - $0 prep for film v6: v6 pills (words v7 / new voice) -> _remotion/public/comic_nazareth/pills_v6 + pills_v6.json.
  .venv\Scripts\python.exe prophecy/02_nazareth/build/prep_nazareth_v6.py"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
from prep_nazareth import PUB, T, W, BA, ImageDraw

# (f0 sec, f1 sec, text, who, ref, jesus)
PL = [(0.10, 2.40, "Jesus stopped reading in the middle of a sentence.", None, None, False),
      (2.88, 4.45, "In Nazareth, His home town,", None, None, False),
      (4.62, 7.80, "He read God's promise of someone sent with good news for the poor,", None, None, False),
      (7.90, 9.80, "and a time of God's welcome.", None, None, False),
      (10.15, 12.15, "The prophet Isaiah's sentence goes on:", None, None, False),
      (12.50, 15.10, "and the day of vengeance of our God.", "ISAIAH", "ISAIAH 61:2", False),
      (15.45, 18.49, "He left the day of vengeance unread, and sat down.", None, None, False),
      (19.22, 22.19, "This day is this scripture fulfilled.", "JESUS", "LUKE 4:21", True),
      (22.63, 23.75, "It was about Him.", None, None, False),
      (24.65, 26.66, "They would want miracles, and say:", None, None, False),
      (27.00, 29.20, "Physician, heal thyself.", "TOWNSMAN", "LUKE 4:23", False),
      (29.55, 34.10, "He reminded them God once sent help to foreigners, not to their own.", None, None, False),
      (35.28, 37.95, "Furious, they took Him to a cliff to throw Him down.", None, None, False),
      (38.44, 39.95, "He walked right through them.", None, None, False),
      (40.36, 42.94, "Later, at the cross, the same dare:", None, None, False),
      (43.28, 45.70, "He saved others; let him save himself.", "LEADER", "LUKE 23:35", False),
      (46.04, 49.00, "This time, He stayed. He died,", None, None, False),
      (49.90, 50.55, "and rose again.", None, None, False),
      (51.05, 53.00, "He stopped reading at the welcome.", None, None, False),
      (53.62, 56.70, "It is still open, for you, today.", None, None, False)]


def pills():
    d = PUB / "pills_v6"; d.mkdir(exist_ok=True); out = []
    f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
    for i, (a, b, text, who, ref, j) in enumerate(PL):
        p = d / ("p%02d.png" % i); W.pill_tabs(p, text, who, ref, jesus=j)
        lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
        out.append(dict(png="pills_v6/p%02d.png" % i, f0=int(math.ceil(a * 30 - 1e-6)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=bool(j), text=text, lines=len(lines)))
    T.light_text(d / "hook.png", "HE STOPPED READING", 600, size=130, maxw=900)
    return out


if __name__ == "__main__":
    P = pills(); (HERE / "pills_v6.json").write_text(json.dumps(P, indent=1)); print("v6 pills ok", len(P), [p["lines"] for p in P])
