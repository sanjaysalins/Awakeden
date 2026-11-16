"""Read-only $0 audit of finished videos: colour cast, voice start, trailing hold, still stretches.
  .venv\Scripts\python.exe poc_comic_page/_audit/audit.py"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; (H / "frames").mkdir(exist_ok=True)
vids = json.load(open(H / "videos.json", encoding="utf8"))
def sh(c): return subprocess.run(c, capture_output=True)
def probe(p, sel):
    r = sh(["ffprobe","-v","error","-select_streams",sel,"-show_entries","stream=duration","-of","csv=p=0",p]).stdout.decode().strip().split("\n")[0]
    try: return float(r)
    except: return None
rows = []
for i, v in enumerate(vids):
    if i < 3 or v["id"].startswith("swirls") or not v["video"]: continue
    p = v["video"]
    if not Path(p).exists(): rows.append({**v, "err": "missing file"}); continue
    r = {"id": v["id"], "title": v["title"], "video": p}
    r["vdur"] = probe(p, "v:0"); r["adur"] = probe(p, "a:0")
    # silence: start + trailing
    sd = sh(["ffmpeg","-v","info","-i",p,"-af","silencedetect=n=-45dB:d=0.4","-vn","-f","null","-"]).stderr.decode()
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sd)]; ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sd)]
    r["voice_start"] = ends[0] if starts and starts[0] < 0.05 and ends else 0.0
    tail = 0.0
    if starts and (len(starts) > len(ends)): tail = (r["adur"] or r["vdur"]) - starts[-1]
    r["tail_silence"] = round(tail, 2)
    # frames: 2fps gray 48x84 + colour means
    W, Hh = 48, 84
    raw = sh(["ffmpeg","-v","error","-i",p,"-vf",f"fps=2,scale={W}:{Hh}","-f","rawvideo","-pix_fmt","rgb24","-"]).stdout
    n = len(raw) // (W*Hh*3)
    if n < 4: r["err"] = "few frames"; rows.append(r); continue
    a = np.frombuffer(raw[:n*W*Hh*3], np.uint8).reshape(n, Hh, W, 3).astype(float)
    m = a.mean((0,1,2)); r["rgb"] = [round(x) for x in m]; r["g_excess"] = round(m[1] - (m[0]+m[2])/2, 1)
    g = a.mean(3); d = np.abs(np.diff(g, axis=0)).mean((1,2))
    thr = 1.2; win = 8; still = 0; worst = 0
    for k in range(0, len(d) - win + 1):
        if d[k:k+win].max() < thr: still += 1
    r["still_windows_4s"] = still; r["median_motion"] = round(float(np.median(d)), 2)
    # longest run of near-still (d<thr) in seconds
    run = best = 0
    for x in d:
        run = run + 1 if x < thr else 0; best = max(best, run)
    r["longest_still_s"] = best / 2
    for t in (0.3, 1.2): sh(["ffmpeg","-y","-v","error","-ss",str(t),"-i",p,"-frames:v","1","-vf","scale=270:-1",str(H/"frames"/f"{v['id']}_{t}.png")])
    rows.append(r); print(r["id"], r["g_excess"], r["voice_start"], r["tail_silence"], r["longest_still_s"], flush=True)
json.dump(rows, open(H / "audit.json", "w", encoding="utf8"), indent=1)
print("DONE", len(rows))
