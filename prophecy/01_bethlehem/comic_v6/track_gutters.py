"""Find the white gutter rows of a comic-page clip every 0.25 s (rows whose mean brightness over x 200-880 > 225). $0."""
import json, subprocess, sys
import numpy as np
from pathlib import Path
CL = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_remotion\public\bethlehem\clips")
def frame(clip, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", str(CL / f"{clip}.mp4"), "-frames:v", "1",
                          "-vf", "scale=1080:1920,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080)
def gutters(img):
    m = img[:, 200:880].mean(1) > 225
    runs, y = [], 0
    while y < 1920:
        if m[y]:
            y0 = y
            while y < 1920 and m[y]: y += 1
            if y - y0 >= 6 and 60 < y0 < 1860: runs.append([y0, y - 1])
        y += 1
    return runs
def box(img):
    rows = img[:, 100:980].mean(1); cols = img[200:1700, :].mean(0)
    top = next((y for y in range(0, 300) if rows[y] < 225), 0); bot = next((y for y in range(1919, 1500, -1) if rows[y] < 225), 1919)
    l = next((x for x in range(0, 200) if cols[x] < 225), 0); r = next((x for x in range(1079, 880, -1) if cols[x] < 225), 1079)
    return [top, bot, l, r]
out = {}; boxes = {}
for clip, a, b in [("P1", 0.0, 9.8), ("P2", 0.0, 10.0), ("P3", 0.0, 10.0), ("P4", 0.0, 10.0), ("P5", 0.0, 10.0)]:
    out[clip] = []; boxes[clip + "_box"] = []
    for t in np.arange(a, b, 0.25):
        im = frame(clip, t); out[clip].append([round(float(t), 2), gutters(im)]); boxes[clip + "_box"].append([round(float(t), 2), box(im)])
    print(clip, [(k, g) for k, g in out[clip][::4]])
Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\comic_v6\panel_rects.json").write_text(json.dumps(out))

# ---- clean pass: keep exactly the 2 real gutters per key (continuity-tracked), fill gaps by interpolation ----
def clean(keys):
    A = B = None; rows = []
    for t, runs in keys:
        if A is None:
            runs2 = sorted(runs)[:2]
            if len(runs2) < 2: continue
            A, B = runs2
        a = min(runs, key=lambda r: abs(r[0] - A[0]), default=None); b = min(runs, key=lambda r: abs(r[0] - B[0]), default=None)
        a = a if a and abs(a[0] - A[0]) < 60 else None
        b = b if b and abs(b[0] - B[0]) < 60 and b != a else None
        if a: A = a
        if b: B = b
        rows.append([t, a, b])
    for idx in (1, 2):
        known = [i for i, r in enumerate(rows) if r[idx]]
        for i, r in enumerate(rows):
            if r[idx]: continue
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            if lo is not None and hi is not None:
                u = (i - lo) / (hi - lo); r[idx] = [round(rows[lo][idx][j] + (rows[hi][idx][j] - rows[lo][idx][j]) * u) for j in (0, 1)]
            else:
                r[idx] = rows[lo if lo is not None else hi][idx]
    return [[r[0], [r[1], r[2]]] for r in rows]
cleaned = {c: clean(v) for c, v in out.items()}
cleaned.update(boxes)
Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\comic_v6\panel_rects.json").write_text(json.dumps(cleaned))
print("cleaned", {c: len(v) for c, v in cleaned.items()})
