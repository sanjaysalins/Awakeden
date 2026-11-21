r"""into_thy_hands linefix1 audio (v2: chain rebuild, no subtraction).
Finding: pinned final audio F = 0.705 x scored.mp4 audio (the sfx stage is a pure ~-3 dB gain, residual -30..-35 dB).
scored.mp4 = run_piece score stage over the engine preview (narration + engine sfx).
So: head 0..CUT = 0.705 x score-stage(new engine head: new narration + engine sfx) ; CUT.. = the pinned film's audio untouched
(25 ms crossfade inside the old 4.06..4.26 silence). Writes narration_linefix1_mix.wav (stereo 44.1k, full length).
Env: needs visual/_linefix1_pool/livingpage_short.linefix1.spec_preview.mp4 (engine run with sfx). JesusInTheBible .venv python."""
import json, subprocess, sys
import numpy as np, scipy.io.wavfile as wf
from pathlib import Path
H = Path(__file__).resolve().parent
PIECE = H.parents[1]
ROOT = PIECE.parents[2]
sys.path.insert(0, str(ROOT))
import run_piece
pj = json.loads((PIECE / "piece.json").read_text(encoding="utf-8"))
HEADMP4 = PIECE / "visual" / "_linefix1_pool" / "livingpage_short.linefix1.spec_preview.mp4"
pj["score"]["src"] = str(HEADMP4)
tmp = H / "_score_head_new.mp4"
pj["score"]["out"] = str(tmp)
cmd = run_piece.score_cmd(PIECE, pj)
cmd = cmd[:-1] + ["-t", "5.0", cmd[-1]]          # only need the head
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
SR = 44100
def dec(src):
    out = H / "_tmp_dec.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)], check=True)
    return wf.read(out)[1].astype(np.float64) / 32768
F = dec(PIECE / "visual" / "into_thy_hands_luke2346_sfx_v5hook.mp4")
SC = dec(tmp)
SCOLD = dec(PIECE / "visual" / "into_thy_hands_luke2346_scored.mp4")
# fit the sfx-stage gain on the OLD head (F vs old scored), lag 219 samples (F later than scored)
LAG = 219
a, b = int(0.3 * SR), int(4.0 * SR)
x = F[a + LAG:b + LAG]; y = SCOLD[a:b]
g = float((x * y).sum() / (y * y).sum()); print("sfx-stage gain", g)
CUT = 4.17; ci = int(CUT * SR); xf = int(0.025 * SR)
head = np.zeros((ci, 2)); n = min(ci, len(SC) - 0)
head[:n] = g * SC[:n]
# new scored head has its own aac delay equal to old scored (same chain) -> shift by the same LAG so it lines up with F
shifted = np.zeros((ci, 2)); shifted[LAG:] = head[:ci - LAG]; shifted[:LAG] = F[:LAG]
out = F.copy()
out[:ci - xf] = shifted[:ci - xf]
t = np.linspace(0, 1, xf)[:, None]
out[ci - xf:ci] = shifted[ci - xf:ci] * (1 - t) + F[ci - xf:ci] * t
out = np.clip(out, -0.99, 0.99)
wf.write(H / "narration_linefix1_mix.wav", SR, (out * 32767).astype(np.int16))
print("ok", len(out) / SR)
