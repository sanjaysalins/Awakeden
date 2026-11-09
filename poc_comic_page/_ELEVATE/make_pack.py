"""Blind pack for bake-off 1. Shuffles arms to codes, builds frame sheets + $0 measurements. Key file is NOT given to seats.
  .venv\\Scripts\\python.exe poc_comic_page/_ELEVATE/make_pack.py"""
import json, random, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; ARMS = HERE / "arms"; OUT = HERE / "pack_tp"; OUT.mkdir(exist_ok=True)
names = [p.stem.replace("TP_", "") for p in sorted(ARMS.glob("TP_*.mp4"))]
names = [n for n in names if n != "B0" or True]
rnd = random.Random(20261108); codes = list("ABCDEFGH")[:len(names)]; rnd.shuffle(names)
key = dict(zip(codes, names)); (HERE / "KEY_tp_PRIVATE.json").write_text(json.dumps(key, indent=1))


def sh(c): return subprocess.run(c, capture_output=True, text=True)


rows = []
for code, n in key.items():
    f = ARMS / ("TP_%s.mp4" % n); dur = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).stdout)
    r = sh(["ffmpeg", "-hide_banner", "-i", str(f), "-vf", "select='gt(scene,0.22)',showinfo", "-an", "-f", "null", "-"]).stderr
    ts = [0.0] + [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r)] + [dur]; gaps = [b - a for a, b in zip(ts, ts[1:])]
    rows.append((code, len(ts) - 2, max(gaps), (len(ts) - 2) / dur * 60))
    sheet = OUT / ("film_%s.png" % code)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "fps=1/2.46,scale=200:-1,tile=6x4:padding=4:color=black", "-frames:v", "1", str(sheet)])
(OUT / "measures.md").write_text("# Measured, $0 (hard cuts found by scene detection)\n| film | cuts | longest gap between cuts (s) | cuts per minute |\n|---|---|---|---|\n" +
                                 "".join("| %s | %d | %.1f | %.0f |\n" % r for r in sorted(rows)))
print(key); print((OUT / "measures.md").read_text())
