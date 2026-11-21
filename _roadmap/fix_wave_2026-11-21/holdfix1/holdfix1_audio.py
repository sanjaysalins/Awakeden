r"""holdfix1 audio: pinned audio kept untouched up to the last spoken word, then the film's OWN score (run_piece.score_cmd, outro_hold 6 s, same music/dips/cta_dip)
continues: +5 dB lift (1.2 s smooth) through the landing hold, then a 2.5 s cos^2 fade to exactly zero on the last frame.
usage: holdfix1_audio.py <film>   (film keys as in holdfix1.CFG)"""
import json, subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent)); import holdfix1 as H
ROOT = H.ROOT; sys.path.insert(0, str(ROOT)); import run_piece
f = sys.argv[1]; c, V, P = H.paths(f); PIECE = V.parent
A = PIECE / "audio" / "_holdfix1"; A.mkdir(exist_ok=True); SR = 44100
T = c["total_f"] / 30.0; N = int(round(T * SR)); LE = c["last_end"]
pj = json.loads((PIECE / "piece.json").read_text(encoding="utf-8"))
sc = pj["score"]; sc["outro_hold"] = 6.0; sc["tpad"] = "6.0"; sc["fade_out"] = 0.05  # tpad only pads a throw-away video; only the audio of scored_ext is used
sc["src"] = str(V / "livingpage_short.spec_preview.mp4"); sc["out"] = str(A / "scored_ext.mp4")
r = subprocess.run(run_piece.score_cmd(PIECE, pj), capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
def dec(src):
    out = A / "_tmp_dec.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)], check=True)
    return wf.read(out)[1].astype(np.float64) / 32768
L = dec(V / c["pinned"]); X = dec(A / "scored_ext.mp4")
a, b = int((LE - 14) * SR), int(LE * SR)
best = None
for d in range(150, 300):   # lag search (pinned later than scored by ~219 samples)
    x = L[a:b]; y = X[a - d:b - d]
    cc = float((x * y).sum() / np.sqrt((x ** 2).sum() * (y ** 2).sum()))
    if best is None or cc > best[0]: best = (cc, d)
cc, lag = best; y = X[a - lag:b - lag]; g = float((L[a:b] * y).sum() / (y * y).sum())
print("align corr %.4f lag %d gain %.4f" % (cc, lag, g))
t = np.arange(N) / SR
# ext[t] = g * X[t - lag]  (X delayed by lag samples)
ext = np.zeros((N, 2)); ext[lag:] = g * X[:N - lag]
x_ = np.clip((t - (LE + 0.05)) / 1.2, 0, 1); ext *= (10 ** ((5 * (x_ * x_ * (3 - 2 * x_))) / 20))[:, None]
base = np.zeros((N, 2)); m = min(N, len(L)); base[:m] = L[:m]
xs = int((LE + 0.02) * SR); xf = int(0.05 * SR); w = np.zeros(N); w[xs:xs + xf] = np.linspace(0, 1, xf); w[xs + xf:] = 1
out = base * (1 - w[:, None]) + ext * w[:, None]
y2 = np.clip((t - (T - 2.5)) / 2.5, 0, 1); out *= (0.5 * (1 + np.cos(np.pi * y2)))[:, None]; out[-1] = 0
out = np.clip(out, -0.97, 0.97)
wf.write(A / "narration_holdfix1_mix.wav", SR, (out * 32767).astype(np.int16)); print("ok", N / SR)
