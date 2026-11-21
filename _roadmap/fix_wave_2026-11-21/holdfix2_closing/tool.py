r"""holdfix1 closing-beat tool (ps22-04/06/07). usage: tool.py <piece> prep|audio|compose
Film = last beat extended to its clip's REAL end (no stretch) + one caption-less CLOSING beat from the film's own pool
(trim only, t_in chosen) so the film ends >= 3.0 s after the last spoken word; audio = old final kept, film's own score tail,
+5 dB lift, 2.5 s cos^2 fade to zero."""
import json, shutil, subprocess, sys
from pathlib import Path
import numpy as np, scipy.io.wavfile as wf
from scipy.signal import fftconvolve

ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); CL = ROOT / "batches/cluster_01_cross"
CFG = {
    "declared_brethren_ps2222": dict(final="declared_brethren_ps2222_sfx.mp4", out="declared_brethren_ps2222_sfx_holdfix1.mp4",
                                     last=16, clip="risen_mercy_hand", close="cross_at_dawn", t_in=3.54, close_frames=45),
    "ends_of_earth_ps2227": dict(final="ends_of_earth_ps2227_sfx.mp4", out="ends_of_earth_ps2227_sfx_holdfix1.mp4",
                                 last=18, clip="risen_christ_wounds", close="stone_rolled_dawn", t_in=2.5, close_frames=75),
    "body_foretold_ps2214": dict(final="body_foretold_ps2214_sfx_v3fix.mp4", out="body_foretold_ps2214_sfx_v3fix_holdfix1.mp4",
                                 last=17, clip="risen_mercy_hand", close="cross_at_dawn", t_in=3.54, close_frames=45),
}
name = sys.argv[1]; stage = sys.argv[2]; c = CFG[name]
P = CL / name; V = P / "visual"; POOL = V / "_holdfix1_pool"; A = P / "audio" / "_holdfix1"; SR = 44100
FINAL = V / c["final"]; OUT = V / c["out"]
spec = json.loads((V / "livingpage_short.spec.json").read_text(encoding="utf-8"))
al = json.loads((P / "audio/alignment.json").read_text())
B = spec["beats"]; lb = B[c["last"] - 1]; f0 = round(lb["t"][0] * 30); LASTEND = al[-1]["end"]
CLIPFR = 151                       # real clip length 5.0417 s = 151.25 frames at 30 fps -> 151 (no stretch)
f1 = f0 + CLIPFR; f2 = f1 + c["close_frames"]; T = f2 / 30

if stage == "prep":
    POOL.mkdir(exist_ok=True); (POOL / "clips").mkdir(exist_ok=True)
    for s in (c["clip"], c["close"]):
        for fn in (f"{s}.png", f"{s}.anchor.json", f"{s}.audit.json", f"{s}.quality.json"):
            if (V / fn).exists():
                shutil.copy(V / fn, POOL / fn)
        shutil.copy(V / "clips" / f"{s}.mp4", POOL / "clips" / f"{s}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "90",
                    str(POOL / "silence.wav")], check=True)
    b = json.loads(json.dumps(lb)); b["t"] = [lb["t"][0], round(f1 / 30, 6)]
    t0 = lb["t"][0]; ws = [w for w in al if w["start"] >= t0 - 0.05]
    nwords = len(b["cap"]["text"].split())
    assert len(ws) == nwords, (len(ws), nwords, [w["w"] for w in ws])
    b["cap"]["word_t"] = [max(0.0, round(w["start"] - t0, 3)) for w in ws]
    assert 5.0417 - c["t_in"] >= c["close_frames"] / 30
    cb = {"t": [round(f1 / 30, 6), round(f2 / 30, 6)], "tpl": "full",
          "clips": [{"slug": c["close"], "motion": "pushin", "t_in": c["t_in"]}], "fx": {"temp": 5000}}
    sp = {"audio": "silence.wav", "total": round(f2 / 30, 6), "cut_ticks": False, "motion": "smooth", "beats": [b, cb]}
    (POOL / "tail.spec.json").write_text(json.dumps(sp, indent=1), encoding="utf-8")
    print("prep ok; last beat frames", f0, f1, "close to", f2, "T", round(T, 3), "hold", round(T - LASTEND, 3))

elif stage == "audio":
    pj = json.loads((P / "piece.json").read_text(encoding="utf-8")); sys.path.insert(0, str(ROOT)); import run_piece
    A.mkdir(exist_ok=True); sc = pj["score"]; sc["outro_hold"] = 9.0; sc["fade_out"] = 0.05
    sc["src"] = str(V / "livingpage_short.spec_preview.mp4"); sc["out"] = str(A / "scored_ext.mp4")
    r = subprocess.run(run_piece.score_cmd(P, pj), capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-1500:])
    def dec(src, n):
        o = A / n
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", str(o)], check=True)
        return wf.read(o)[1].astype(np.float64) / 32768
    L = dec(FINAL, "_cur.wav"); X = dec(A / "scored_ext.mp4", "_ext.wav"); N = int(round(T * SR)); Lend = len(L) / SR
    a, b = int(20 * SR), int(min(Lend - 6, 40) * SR)
    x = L[a:b].mean(1); y = X[a - 3000:b + 3000].mean(1); cc = fftconvolve(y, x[::-1], mode="valid"); d = int(np.argmax(cc)) - 3000
    xs = X[a + d:b + d].mean(1)
    print("align delta", d, "corr", float((x * xs).sum() / np.sqrt((x * x).sum() * (xs * xs).sum())))
    ext = np.zeros((N, 2)); i0 = max(0, -d); seg = X[i0 + d:i0 + d + N - i0]; ext[i0:i0 + len(seg)] = seg
    t = np.arange(N) / SR; base = np.zeros((N, 2)); m = min(N, len(L)); base[:m] = L[:m]
    x0 = int((Lend - 0.35) * SR); xf = int(0.35 * SR); w = np.zeros(N); w[x0:x0 + xf] = np.linspace(0, 1, xf); w[x0 + xf:] = 1
    xx = np.clip((t - Lend) / 1.2, 0, 1); ext *= (10 ** ((5 * (xx * xx * (3 - 2 * xx))) / 20))[:, None]
    out = base * (1 - w[:, None]) + ext * w[:, None]
    yy = np.clip((t - (T - 2.5)) / 2.5, 0, 1); out *= (0.5 * (1 + np.cos(np.pi * yy)))[:, None]; out[-1] = 0
    wf.write(A / "mix.wav", SR, (np.clip(out, -0.97, 0.97) * 32767).astype(np.int16)); print("audio ok", round(T, 3), "Lend", round(Lend, 3))

elif stage == "compose":
    W = POOL / "_compose"; W.mkdir(exist_ok=True); TAIL = POOL / "tail.spec_preview.mp4"
    def run(cmd):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            sys.exit("FAIL " + r.stderr[-1500:])
    ntail = f2 - f0
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(FINAL), "-frames:v", str(f0), "-an", "-c:v", "copy", "-avoid_negative_ts", "make_zero", str(W / "s1.mp4")])
    run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "3", "-i", str(TAIL), "-vf", f"trim=start_frame=0:end_frame={ntail},setpts=PTS-STARTPTS",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(W / "tail.mp4")])
    (W / "list.txt").write_text("file 's1.mp4'\nfile 'tail.mp4'\n")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(W / "list.txt"), "-c", "copy", str(W / "v.mp4")])
    run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "3", "-i", str(W / "v.mp4"), "-i", str(A / "mix.wav"), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-movflags", "+faststart", "-shortest", str(OUT)])
    shutil.copy(P / "audio/alignment.json", OUT.with_suffix(".words.json")); print("compose ok", OUT)
