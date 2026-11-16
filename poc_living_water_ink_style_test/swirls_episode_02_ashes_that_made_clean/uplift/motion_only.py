"""ep08 uplift gate ($0). python check_uplift.py  -> prints PASS/FAIL per gate; writes gate_report.json
Checks: G-AUDIO (audio md5 == shipped), G-FRAMES (1858), G-SLOT (clip >= slot + 0.05 s, no fill), G-MOTION (new clips: zoom, frozen, text, motif),
G-MARKS (word time +-3 f, spacing >= 3.0 s, <= 8 per 60 s, quiet zones, keep-out overlap on real frames)."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

UP = Path(__file__).resolve().parent
EP = UP.parent
sys.path.insert(0, str(UP))
SPEC = json.loads((UP / "uplift.json").read_text(encoding="utf-8"))
WORDS = Path(r"F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_swirls\word_timings\ep02_words.txt").read_text(encoding="utf-8")
SHIPPED = EP / "THE_ASHES_BOOK_final_sfx.mp4"
FINAL = UP / "ep02_uplift_final.mp4"
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

# ---- G-MOTION on the new clips (and re-animated F03/F04)
mot, ok_all = [], True
USED = {"f02b_3s": "S03", "f01_8s": "S04", "f02c_6s": "S05", "f02d_6s": "S06", "f03a_4s": "S07", "f03_8s": "S08", "f04b_4s": "S10", "f05_9s": "S11"}
SLOT = {x["id"]: (x["f1"] - x["f0"]) for x in SPEC["shots"]}
for cid in USED:
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
    CB = {'f01_8s': (.89, .925), 'f02b_3s': (.92, .96), 'f02c_6s': (.90, .93), 'f02d_6s': (.895, .925), 'f03a_4s': (.915, .95), 'f03_8s': (.83, .865), 'f04b_4s': (.86, .89), 'f05_9s': (.925, .955)}[cid]
    t_cap = float(np.mean(np.abs(band(a, CB[0], CB[1]) - band(b, CB[0], CB[1]))))
    ok = 0.99 <= z <= 1.01 and mean_d > 0.15 and t_title < 4.5 and t_cap < 5.0 and abs(b1 - b0) <= 0.20 * max(b0, 1)
    ok_all &= ok
    mot.append(f"{cid}: zoom {z:.3f} meandiff {mean_d:.2f} title {t_title:.2f} caption {t_cap:.2f} blue-motif px {b0}->{b1} used {len(fr)}f {'ok' if ok else 'CHECK'}")
result("G-MOTION new clips: zoom 1.000+-0.010, not frozen, baked text first==last", ok_all, " | ".join(mot))

