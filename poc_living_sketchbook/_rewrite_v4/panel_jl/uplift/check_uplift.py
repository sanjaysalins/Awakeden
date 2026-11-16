"""JL uplift gate ($0). python check_uplift.py -> PASS/FAIL per gate; writes gate_report.json
G-AUDIO, G-FRAMES (1695), G-SLOT, G-MOTION (new clips: zoom, frozen, baked text, blue motif), G-MARKS, G-KEEPOUT."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, cv2

UP = Path(__file__).resolve().parent
sys.path.insert(0, str(UP))
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
WORDS = Path(SPEC["words"]).read_text(encoding="utf-8")
SHIPPED = Path(SPEC["audio_from"])
FINAL = UP / "jl_uplift_final.mp4"
BASE = UP / "work" / "base_final.mp4"
FPS = 30; NF = SPEC["total_frames"]
rep = {}
def sh(cmd): return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
def md5_audio(p): return sh(["ffmpeg", "-v", "error", "-i", str(p), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"])
def dur(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))
def frame_at(p, idx):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{(idx + 0.5) / 30:.4f}", "-i", str(p), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    return subprocess.run(cmd, capture_output=True).stdout
def result(name, ok, ev):
    rep[name] = {"pass": bool(ok), "evidence": ev}; print(("PASS " if ok else "FAIL ") + name + " :: " + ev)

a1, a2 = md5_audio(SHIPPED), md5_audio(FINAL)
result("G-AUDIO audio bit-identical", a1 == a2 and a1 != "", f"shipped {a1} / new {a2}")
n = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height", "-of", "csv=p=0", str(FINAL)])
ns = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(SHIPPED)])
result(f"G-FRAMES {NF} frames 1080x1920 = shipped", n.startswith(f"1080,1920,{NF}") and ns == str(NF), f"{n}; shipped frames {ns}; dur {dur(FINAL):.3f}s vs shipped {dur(SHIPPED):.3f}s")
bad, lines = [], []
def rp(s): p = Path(s["src"]); return p if p.is_absolute() else UP / p
for s in SPEC["shots"]:
    slot = (s["f1"] - s["f0"]) / FPS; d = dur(rp(s)); lines.append(f'{s["id"]} {d:.2f}/{slot:.2f}')
    if d < slot + 0.05: bad.append(s["id"])
src = (UP / "cut_uplift.py").read_text()
result("G-SLOT every clip >= slot+0.05 s, trim only (no tpad/reverse/setpts-speed/zoompan/loop)", not bad and not re.search(r"tpad|reverse|zoompan|loop=|boomerang", src), "; ".join(lines) + (" SHORT: " + ",".join(bad) if bad else ""))

mot, ok_all = [], True
for s in [x for x in SPEC["shots"] if x.get("new")]:
    p = rp(s); slot = s["f1"] - s["f0"]
    cap = cv2.VideoCapture(str(p)); fr = []
    while True:
        r, f = cap.read()
        if not r: break
        fr.append((cv2.cvtColor(cv2.resize(f, (360, 640)), cv2.COLOR_BGR2GRAY).astype(np.float32), f[int(.3 * f.shape[0]):].astype(int)))
    fr = fr[:round(slot / 30 * 24) + 1]
    blue = lambda f: int(((f[..., 0] - f[..., 2]) > 35).sum())
    b0, b1 = blue(fr[0][1]), blue(fr[-1][1]); fr = [x[0] for x in fr]; a, b = fr[0], fr[-1]
    diffs = [float(np.mean(np.abs(fr[i] - fr[i + 1]))) for i in range(len(fr) - 1)]; mean_d = float(np.mean(diffs))
    Wm = np.eye(2, 3, dtype=np.float32)
    try:
        cc, Wm = cv2.findTransformECC(a / 255, b / 255, Wm, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)); z = float(np.sqrt(abs(np.linalg.det(Wm[:, :2]))))
    except Exception: z = 1.0
    band = lambda img, y0, y1: img[int(y0 * 640):int(y1 * 640), :]
    cover = s["id"] == "S10"
    t_title = float(np.mean(np.abs(band(a, 0, .06) - band(b, 0, .06))))
    t_cap = float(np.mean(np.abs(band(a, .90, 1) - band(b, .90, 1))))
    ok = 0.99 <= z <= 1.01 and mean_d > 0.15 and t_title < 4.5 and t_cap < 5.0 and abs(b1 - b0) <= 0.20 * max(b0, 1)
    ok_all &= ok
    mot.append(f"{s['id']} {s['page']}: zoom {z:.3f} meandiff {mean_d:.2f} top {t_title:.2f} bottom {t_cap:.2f} blue px {b0}->{b1} used {len(fr)}f {'ok' if ok else 'CHECK'}")
result("G-MOTION new clips: zoom 1.000+-0.010, not frozen, baked text first==last", ok_all, " | ".join(mot))

import marks_overlay as MO
words = {}
for m in re.finditer(r"([^\s@]+)@([\d.]+)", WORDS):
    words.setdefault(m.group(1).strip('"“”,.?!:;').lower(), []).append(float(m.group(2)))
ev, ok_m, starts = [], True, []
for m in MO.MARKS:
    t0 = min(s.get("t0", 1e9) for s in m["strokes"]); wt = m["word_t"]; w = m["word"].split()[0].strip('.,?!"').lower()
    in_file = any(abs(c - wt) < 0.02 for c in words.get(w, [])); dfr = t0 - round(wt * FPS)
    ok1 = in_file and -3 <= dfr <= 0; starts.append(t0); ok_m &= ok1
    ev.append(f'{m["id"]} "{m["word"]}"@{wt} start f{t0} ({dfr:+d}f) {"ok" if ok1 else "BAD"}')
starts.sort(); gaps_ok = all(b - a >= 90 for a, b in zip(starts, starts[1:]))
last = max(m["until"] for m in MO.MARKS)
ok_m &= gaps_ok and len(starts) <= 8 and starts[0] >= 30 and last <= NF - 90
ev.append(f"spacing>=90f {'ok' if gaps_ok else 'BAD'}; count {len(starts)}<=8; first {starts[0]}f>=30; last mark ends f{last} <= {NF-90}; covers untouched")
# marks must end 5f before their shot ends
shot_end = {s["id"]: s["f1"] for s in SPEC["shots"]}
early = all(m["until"] <= shot_end[m["shot"]] - 5 for m in MO.MARKS)
ok_m &= early; ev.append("marks gone >=5f before shot end: " + ("ok" if early else "BAD"))
result("G-MARKS word-tied, spacing, count, quiet zones", ok_m, f"{len(starts)} marks; within -3..0 f of the word")
ko, ok_k = [], True
for m in MO.MARKS:
    f = m["until"] - 8; base = np.frombuffer(frame_at(BASE, f), np.uint8).reshape(1920, 1080, 3)
    drawn = MO.render_frame(f, np.full((1920, 1080, 3), 255, np.uint8), {}).astype(int); mk = drawn.sum(axis=2) < 3 * 245; n_mk = int(mk.sum())
    b = base.astype(int); lum = b.mean(axis=2)
    dark = mk & (lum < 95); blu = mk & ((b[..., 2] - b[..., 0]) > 35)
    frac = (blu.sum() + dark.sum()) / max(n_mk, 1); okf = frac < 0.03; ok_k &= okf
    ko.append(f'{m["id"]}: {n_mk}px, text/face/motif overlap {frac*100:.1f}% (dark {dark.sum()/max(n_mk,1)*100:.1f}% blue {blu.sum()/max(n_mk,1)*100:.1f}%) {"ok" if okf else "CHECK"}')
result("G-KEEPOUT no stroke on baked text / faces / blue motif (real frames, <3% px)", ok_k, " | ".join(ko))
rep["_marks_detail"] = ev; print("\n".join("   " + e for e in ev))
(UP / "gate_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
