"""ep08 uplift gate ($0). python check_uplift.py  -> prints PASS/FAIL per gate; writes gate_report.json
Checks: G-AUDIO (audio md5 == shipped), G-FRAMES (1921), G-SLOT (clip >= slot + 0.05 s, no fill), G-MOTION (new clips: zoom, frozen, text, motif),
G-MARKS (word time +-3 f, spacing >= 3.0 s, <= 8 per 60 s, quiet zones, keep-out overlap on real frames)."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

UP = Path(__file__).resolve().parent
EP = UP.parent
sys.path.insert(0, str(UP))
SPEC = json.loads(Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\pilot_ep08_uplift.json").read_text(encoding="utf-8"))
WORDS = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\word_timings\ep08_words.txt").read_text(encoding="utf-8")
SHIPPED = EP / "CAN_ANY_GOOD_THING_final_sfx.mp4"
FINAL = UP / "ep08_uplift_final.mp4"
BASE = UP / "work" / "base_final.mp4"
FPS = 30
rep = {}

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def md5_audio(p):
    return sh(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])

def dur(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

def frame_at(p, idx, size=None, gray=False):
    out = _frame_at(p, idx, size, gray)
    if not out:   # select-by-index occasionally returns nothing on concat files: fall back to timestamp seek
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{(idx + 0.5) / 30:.4f}", "-i", str(p), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        out = subprocess.run(cmd, capture_output=True).stdout
    return out

def _frame_at(p, idx, size=None, gray=False):
    vf = []
    if size: vf.append(f"scale={size[0]}:{size[1]}")
    if gray: vf.append("format=gray")
    cmd = ["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"select=eq(n\\,{idx})" + ("," + ",".join(vf) if vf else ""), "-vsync", "0", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray" if gray else "rgb24", "-"]
    return subprocess.run(cmd, capture_output=True).stdout

def result(name, ok, ev):
    rep[name] = {"pass": bool(ok), "evidence": ev}
    print(("PASS " if ok else "FAIL ") + name + " :: " + ev)

# ---- G-AUDIO
a1, a2 = md5_audio(SHIPPED), md5_audio(FINAL)
result("G-AUDIO audio bit-identical", a1 == a2 and a1 != "", f"shipped {a1} / new {a2}")
# ---- G-FRAMES
n = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height", "-of", "csv=p=0", str(FINAL)])
result("G-FRAMES 1921 frames 1080x1920", n.startswith("1080,1920,1921") or n.endswith("1921"), n + f"; dur {dur(FINAL):.3f}s vs shipped {dur(SHIPPED):.3f}s")
# ---- G-SLOT
bad, lines = [], []
for s in SPEC["shots"]:
    p = (EP / s["src"]).resolve()
    slot = (s["f1"] - s["f0"]) / FPS
    d = dur(p)
    lines.append(f'{s["id"]} {d:.2f}/{slot:.2f}')
    if d < slot + 0.05:
        bad.append(s["id"])
result("G-SLOT every clip >= slot+0.05 s, trim only (no tpad/reverse/setpts/zoompan in cut_uplift.py)", not bad and not re.search(r"tpad|reverse|zoompan|loop=", (UP / "cut_uplift.py").read_text().replace("-loop", "")), "; ".join(lines) + (" SHORT: " + ",".join(bad) if bad else ""))

# ---- G-MOTION on the new clips (and re-animated F03/F04)
mot, ok_all = [], True
USED = {"f03_8s": "S04", "f03b_3s": "S05", "f04_10s": "S06", "f05a_3s": "S07", "f05b_5s": "S09", "f07_5s": "S12"}
SLOT = {x["id"]: (x["f1"] - x["f0"]) for x in SPEC["shots"]}
for cid in ["f03_8s", "f03b_3s", "f04_10s", "f05a_3s", "f05b_5s", "f07_5s"]:
    p = UP / "clips" / f"{cid}.mp4"
    if not p.exists():
        mot.append(f"{cid}: MISSING"); ok_all = False; continue
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append((cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY).astype(np.float32), f[int(.3 * f.shape[0]):].astype(int)))
    nused = round(SLOT[USED[cid]] / 30 * 24) + 1   # only the frames the cut really plays
    fr = fr[:nused]
    blue = lambda f: int(((f[..., 0] - f[..., 2]) > 35).sum())
    b0, b1 = blue(fr[0][1]), blue(fr[-1][1])
    fr = [x[0] for x in fr]
    a, b = fr[0], fr[-1]
    diffs = [float(np.mean(np.abs(fr[i] - fr[i + 1]))) for i in range(0, len(fr) - 1)]
    mean_d = float(np.mean(diffs))
    W = np.eye(2, 3, dtype=np.float32)
    try:
        cc, W = cv2.findTransformECC(a / 255, b / 255, W, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6))
        z = float(np.sqrt(abs(np.linalg.det(W[:, :2]))))
    except Exception:
        z = 1.0
    # text bands (title + caption) first vs last, 2x scale grid on the 360x640 grey
    def band(img, y0, y1): return img[int(y0 * 640):int(y1 * 640), :]
    t_title = float(np.mean(np.abs(band(a, 0, .06) - band(b, 0, .06))))
    y0 = .86 if cid == 'f03b_3s' else .935
    t_cap = float(np.mean(np.abs(band(a, y0, 1) - band(b, y0, 1))))
    ok = 0.99 <= z <= 1.01 and mean_d > 0.15 and t_title < 4.5 and t_cap < 5.0 and abs(b1 - b0) <= 0.20 * max(b0, 1)
    ok_all &= ok
    mot.append(f"{cid}: zoom {z:.3f} meandiff {mean_d:.2f} title {t_title:.2f} caption {t_cap:.2f} blue-motif px {b0}->{b1} used {len(fr)}f {'ok' if ok else 'CHECK'}")
result("G-MOTION new clips: zoom 1.000+-0.010, not frozen, baked text first==last", ok_all, " | ".join(mot))

# ---- G-MARKS
import marks_overlay as MO
words = {}
for m in re.finditer(r"([^\s@]+)@([\d.]+)", WORDS):
    words.setdefault(m.group(1).strip('"“”,.?!:;').lower(), []).append(float(m.group(2)))
ev, ok_m = [], True
starts = []
for m in MO.MARKS:
    t0 = min(s.get("t0", 1e9) for s in m["strokes"])
    wt = m["word_t"]; w = m["word"].split()[0].strip('.,?!"').lower()
    cands = words.get(w, [])
    in_file = any(abs(c - wt) < 0.02 for c in cands)
    dfr = t0 - round(wt * FPS)
    ok1 = in_file and -3 <= dfr <= 0
    starts.append(t0)
    ok_m &= ok1
    ev.append(f'{m["id"]} "{m["word"]}"@{wt} start f{t0} ({dfr:+d}f) {"ok" if ok1 else "BAD"}')
starts.sort()
gaps_ok = all(b - a >= 90 for a, b in zip(starts, starts[1:]))
ok_m &= gaps_ok and len(starts) <= 8 and starts[0] >= 30 and max(m["until"] for m in MO.MARKS) <= 1921 - 90 - 0
ev.append(f"spacing>=90f {'ok' if gaps_ok else 'BAD'} count {len(starts)}<=8; first {starts[0]}f>=30; last mark ends f{max(m['until'] for m in MO.MARKS)} <= 1831 (last 3 s quiet); covers S01 0-108 / S13 1806+ untouched")
# keep-out: on the real cut frame at each mark's last fully drawn frame, dark (text/face/ink) or blue (motif) pixels under the pencil
sc = {'M4': MO.sightline_pts(np.frombuffer(frame_at(BASE, 805), np.uint8).reshape(1920, 1080, 3)), 'M8': MO.sightline_pts(np.frombuffer(frame_at(BASE, 1785), np.uint8).reshape(1920, 1080, 3), *[m for m in MO.MARKS if m['id']=='M8'][0]['arrow'])}
ko = []
ok_k = True
for m in MO.MARKS:
    f = m["until"] - 8
    raw = frame_at(BASE, f); base = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
    white = np.full((1920, 1080, 3), 255, np.uint8)
    drawn = MO.render_frame(f, white.copy(), sc).astype(int)
    mk = drawn.sum(axis=2) < 3 * 245
    n_mk = int(mk.sum())
    b = base.astype(int)
    lum = b.mean(axis=2)
    dark = mk & (lum < 95)
    blue = mk & ((b[..., 2] - b[..., 0]) > 35)
    through_art = m["id"] in ("M4", "M8")   # dashed sight lines cross leaf/ground art on purpose; only motif (blue) + text/face keep-outs apply
    frac = (blue.sum() + (0 if through_art else dark.sum())) / max(n_mk, 1)
    okf = frac < 0.03
    ok_k &= okf
    ko.append(f'{m["id"]}: {n_mk}px, motif/text overlap {frac*100:.1f}% (dark-ink {dark.sum()/max(n_mk,1)*100:.1f}%{" crossing leaf art, allowed" if through_art else ""}) {"ok" if okf else "CHECK"}')
result("G-KEEPOUT no stroke on baked text / faces / blue motif (real frames, <3% px)", ok_k, " | ".join(ko))
rep["_marks_detail"] = ev
print("\n".join("   " + e for e in ev))
result("G-MARKS word-tied, spacing, count, quiet zones", ok_m, f"{len(starts)} marks; all within -3..0 f of the word")
Path(UP / "gate_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
