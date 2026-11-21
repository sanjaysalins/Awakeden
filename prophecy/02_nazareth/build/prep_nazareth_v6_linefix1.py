"""prep_nazareth_v6_linefix1.py - $0: new pills for the new first line -> _remotion/public/comic_nazareth/pills_v6_lf1/ + pills_v6_lf1.json (3 entries: 2 caption pills + hook card).
  .venv\Scripts\python.exe prophecy/02_nazareth/build/prep_nazareth_v6_linefix1.py"""
import sys, json, math
from pathlib import Path
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
from prep_nazareth import PUB, T, W, BA, ImageDraw
PL = [(0.10, 1.55, "Afraid God is angry with you?"), (2.13, 3.65, "Watch where Jesus stopped reading.")]
d = PUB / "pills_v6_lf1"; d.mkdir(exist_ok=True); out = []
f = BA.KAL(54); dd = ImageDraw.Draw(T.canvas())
for i, (a, b, text) in enumerate(PL):
    p = d / ("p%02d.png" % i); W.pill_tabs(p, text, None, None, jesus=False)
    lines = BA.wrap(dd, text.split(), f, 820)[:3]; h = 60 + 62 * len(lines)
    out.append(dict(png="pills_v6_lf1/p%02d.png" % i, f0=int(math.ceil(a * 30 - 1e-6)), f1=int(round(b * 30)), box=[70, 1000, 940, h], radius=46, jesus=False, text=text, lines=len(lines)))
T.light_text(d / "hook.png", "AFRAID GOD IS ANGRY WITH YOU?", 600, size=110, maxw=900)
(HERE / "pills_v6_lf1.json").write_text(json.dumps(out, indent=1)); print(out)
