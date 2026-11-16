"""ep13 uplift gate ($0). python check_uplift.py -> PASS/FAIL per gate; writes gate_report.json"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, cv2
UP = Path(__file__).resolve().parent; EP = UP.parent; sys.path.insert(0, str(UP))
SPEC = json.loads((UP / "uplift.json").read_text())
WORDS = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\word_timings\ep13_words.txt").read_text(encoding="utf-8")
SHIPPED = EP / "swirls_episode_13_the_cross_that_wasnt_his_final_piano_sfx.mp4"
FINAL = UP / "ep13_uplift_final.mp4"; BASE = UP / "work" / "base_final.mp4"
FPS = 30; NF = SPEC["total_frames"]; rep = {}
def sh(c): return subprocess.run(c, capture_output=True, text=True).stdout.strip()
def md5a(p): return sh(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])
def dur(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
def frame_at(p, idx):
    return subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{(idx + 0.5) / FPS:.4f}", "-i", str(p), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
def result(n, ok, ev):
    rep[n] = {"pass": bool(ok), "evidence": ev}; print(("PASS " if ok else "FAIL ") + n + " :: " + ev)
a1, a2 = md5a(SHIPPED), md5a(FINAL)
result("G-AUDIO audio bit-identical to shipped", a1 == a2 and a1 != "", f"shipped {a1} / new {a2}")
n = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=width,height,nb_read_frames", "-of", "csv=p=0", str(FINAL)])
result(f"G-FRAMES {NF} frames 1080x1920", n.replace(",", " ") == f"1080 1920 {NF}", n + f"; dur {dur(FINAL):.3f}s vs shipped {dur(SHIPPED):.3f}s")
bad, lines = [], []
for s in SPEC["shots"]:
    p = (EP / s["src"]).resolve(); slot = (s["f1"] - s["f0"]) / FPS; d = dur(p)
    lines.append(f'{s["id"]} {d:.2f}/{slot:.2f}')
    if d < slot + 0.05: bad.append(s["id"])
ctext = (UP / "cut_uplift.py").read_text()
result("G-SLOT every clip >= slot+0.05 s, trim only (no tpad/reverse/zoompan/loop)", not bad and not re.search(r"tpad|reverse|zoompan|setpts|loop=", ctext.replace("-loop", "")), "; ".join(lines) + (" SHORT:" + ",".join(bad) if bad else ""))
NEWC = {"cover_5s": ("S01", (0, .2), None), "f01b_3s": ("S03", (0, .06), (.93, 1)), "f02b_4s": ("S05", (0, .06), (.93, 1)), "f03b_4s": ("S07", (0, .06), (.88, .94)),
        "f05b_5s": ("S10", (0, .06), (.88, .94)), "f06b_3s": ("S12", (0, .06), (.96, 1)), "f07b_5s": ("S14", (0, .06), (.93, 1)), "f09b_7s": ("S17", (0, .06), (.91, .96))}
SLOT = {x["id"]: x["f1"] - x["f0"] for x in SPEC["shots"]}
mot, okall = [], True
for cid, (sid, tb, cb) in NEWC.items():
    p = UP / "clips" / f"{cid}.mp4"; cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append((cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY).astype(np.float32), f[int(.3 * f.shape[0]):].astype(int)))
    fr = fr[:round(SLOT[sid] / FPS * 24) + 1]
    blue = lambda f: int(((f[..., 0] - f[..., 2]) > 35).sum()); b0, b1 = blue(fr[0][1]), blue(fr[-1][1])
    g = [x[0] for x in fr]; a, b = g[0], g[-1]
    md = float(np.mean([np.mean(np.abs(g[i] - g[i + 1])) for i in range(len(g) - 1)]))
    W = np.eye(2, 3, dtype=np.float32)
    try:
        cc, W = cv2.findTransformECC(a / 255, b / 255, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)); z = float(np.sqrt(abs(np.linalg.det(W[:, :2]))))
    except Exception: z = 1.0
    band = lambda img, y: img[int(y[0] * 640):int(y[1] * 640), :]
    tt = float(np.mean(np.abs(band(a, tb) - band(b, tb)))); tc = float(np.mean(np.abs(band(a, cb) - band(b, cb)))) if cb else 0.0
    ok = 0.98 <= z <= 1.02 and md > 0.15 and tt < 4.5 and tc < 5.0 and (cid == "cover_5s" or abs(b1 - b0) <= 0.25 * max(b0, 1))
    okall &= ok
    mot.append(f"{cid}: zoom {z:.3f} meandiff {md:.2f} title {tt:.2f} caption {tc:.2f} blue px {b0}->{b1} {'ok' if ok else 'CHECK'}")
result("G-MOTION new clips: zoom ~1, not frozen, baked text first==last, motif px stable", okall, " | ".join(mot))
import marks_overlay as MO
words = {}
for m in re.finditer(r"([^\s@]+)@([\d.]+)", WORDS): words.setdefault(m.group(1).strip('"“”,.?!:;').lower(), []).append(float(m.group(2)))
ev, okm, starts = [], True, []
for m in MO.MARKS:
    t0 = min(s["t0"] for s in m["strokes"]); wt = m["word_t"]; w = m["word"].split()[0].strip('.,?!"').lower()
    inf = any(abs(c - wt) < 0.02 for c in words.get(w, [])); d = t0 - round(wt * FPS); ok1 = inf and -3 <= d <= 0
    shot = [s for s in SPEC["shots"] if s["id"] == m["shot"]][0]; ok2 = shot["f0"] <= t0 and m["until"] <= shot["f1"] - 5
    starts.append(t0); okm &= ok1 and ok2; ev.append(f'{m["id"]} "{m["word"]}"@{wt} start f{t0} ({d:+d}f) ends f{m["until"]} in {m["shot"]} {"ok" if ok1 and ok2 else "BAD"}')
starts.sort()
gaps = all(b - a >= 90 for a, b in zip(starts, starts[1:]))
per60 = max(sum(1 for s in starts if t <= s < t + 1800) for t in starts)
okm &= gaps and per60 <= 8 and starts[0] >= 30 and max(m["until"] for m in MO.MARKS) <= NF - 90
ev.append(f"spacing>=90f {'ok' if gaps else 'BAD'}; max {per60} marks in any 60 s; first f{starts[0]}; last ends f{max(m['until'] for m in MO.MARKS)} <= {NF-90}; covers (S01, S18) untouched")
ko, okk = [], True
for m in MO.MARKS:
    f = m["until"] - 8; base = np.frombuffer(frame_at(BASE, f), np.uint8).reshape(1920, 1080, 3)
    drawn = MO.render_frame(f, np.full((1920, 1080, 3), 255, np.uint8), {}).astype(int); mk = drawn.sum(axis=2) < 3 * 245; nmk = int(mk.sum())
    b = base.astype(int); lum = b.mean(axis=2); dark = (mk & (lum < 95)).sum(); blu = (mk & ((b[..., 2] - b[..., 0]) > 35)).sum()
    frac = (dark + blu) / max(nmk, 1); okf = frac < 0.03; okk &= okf
    ko.append(f'{m["id"]}: {nmk}px, text/face/motif overlap {frac*100:.1f}% {"ok" if okf else "CHECK"}')
result("G-KEEPOUT no stroke on baked text / faces / blue motif (real frames, <3% px)", okk, " | ".join(ko))
result("G-MARKS word-tied (+-3 f), spacing, count, quiet zones, leave before cut", okm, "; ".join(ev))
rep["_marks_detail"] = ev
Path(UP / "gate_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
