r"""Ep13 wordsfix1 audio. Old narration kept for 0..37.40 s and 54.20..74.20 s (the second block moved EARLIER by S1 = 341 frames = 11.3667 s),
new takes (mid, end) placed; score cut (2 crossfaded cuts) so its part-2 entry + final fade stay on the same words; sfx layers re-timed.
Then the film's own chain: narration -> aac -> mix_tail (score -6 dB, duck 0.12/2.5/250) -> aac -> sfxlib.build(LAYERS).
Usage: build_audio_wordsfix1.py null|new   (null = old narration + old score through the same chain, to prove the chain)"""
import subprocess, sys, json
import numpy as np
from pathlib import Path
H = Path(__file__).resolve().parent
EP = H.parent
ROOT = EP.parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(EP))
from pipeline import score_mix
import build_sfx
import sfxlib
SR = 44100
mode = sys.argv[1] if len(sys.argv) > 1 else "new"
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("FAIL " + " ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
def dec(p, ch):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(b, np.float32)
    return a if ch == 1 else a.reshape(-1, ch)
def wav(p, a):
    ch = 1 if a.ndim == 1 else a.shape[1]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-c:a", "pcm_f32le", str(p)], input=a.astype(np.float32).tobytes(), check=True)
def fade(a, n_in=0, n_out=0):
    a = a.copy()
    if n_in: a[:n_in] *= np.linspace(0, 1, n_in, dtype=np.float32)
    if n_out: a[-n_out:] *= np.linspace(1, 0, n_out, dtype=np.float32)
    return a
def sec(t): return int(round(t * SR))
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)

S1 = 341 / 30.0
FRAMES = 2470
TOTAL = FRAMES / 30.0
OLD_N = EP / "narration.mp3"; OLD_S = EP / "score_piano.mp3"

def tighten(take, cuts):
    """cuts = [(t0,t1)...] in take seconds (inside silent gaps). returns new array and a mapper take_t -> new_t"""
    out, pos = [], 0
    for t0, t1 in cuts:
        seg = take[sec(t0):sec(t1)]
        assert db(seg) < -48, f"cut window {t0}-{t1} not silent: {db(seg):.1f} dB"
        out.append(fade(take[pos:sec(t0)], 0, sec(0.01))); pos = sec(t1)
    out.append(take[pos:])
    def m(t):
        return t - sum(min(max(t - a, 0), b - a) for a, b in cuts)
    return np.concatenate(out), m
MID_CUTS = [(2.25, 2.45)]
END_CUTS = [(1.70, 2.00), (6.25, 6.65), (14.20, 14.40)]
if mode == "null":
    narr_arr = None; NARR_LEN = 103.431; TOT = NARR_LEN + 3.0; layers = build_sfx.LAYERS
else:
    old = dec(OLD_N, 1)
    mid, mmap = tighten(dec(H / "mid_narrator_a.mp3", 1), MID_CUTS)
    end, emap = tighten(dec(H / "end_narrator_a.mp3", 1), END_CUTS)
    rel = json.loads((H / "new_words_rel.json").read_text())
    K1, K2, K3 = 37.40, 54.20, 74.20           # old keep points (all inside old silences)
    P_MID = 37.40
    P_END = 75.08 - S1 - 0.12                  # 'Reproach' lands where the old 'Reproach' was, shifted
    last_end = P_END + emap(rel["end_a"]["words"][-1]["end"])
    NARR_LEN = last_end + 0.05
    TOT = TOTAL
    n = sec(TOT)
    buf = np.zeros(n + sec(30), np.float32)
    def put(a, t):
        i = sec(t); buf[i:i + len(a)] += a
    put(fade(old[:sec(K1)], 0, sec(0.05)), 0.0)
    put(fade(mid, sec(0.02), sec(0.02)), P_MID)
    put(fade(old[sec(K2):sec(K3)], sec(0.03), sec(0.05)), K2 - S1)
    put(fade(end, sec(0.02), sec(0.05)), P_END)
    narr_arr = buf[:sec(NARR_LEN)]
    # ---- score: cut 1 (part-1 decay shortened by S1) and cut 2 (part 2 shortened by S2), equal-power crossfades
    sc = dec(OLD_S, 2); S2 = len(sc) / SR - S1 - TOT
    def splice(a, b, x):
        nn = sec(x); w = np.linspace(0, 1, nn, dtype=np.float32).reshape(-1, 1)
        return np.concatenate([a[:-nn], a[-nn:] * np.cos(w * np.pi / 2) + b[:nn] * np.sin(w * np.pi / 2), b[nn:]])
    A, X = 40.0, 2.0
    best = None
    for c2 in np.arange(78.0, 86.0, 0.25):
        d = abs(db(sc[sec(c2 - 2):sec(c2)]) - db(sc[sec(c2 + S2):sec(c2 + S2 + 2)]))
        if best is None or d < best[0]: best = (d, c2)
    c2 = float(best[1]); print("score cuts: A", A, "S1", round(S1, 3), "S2", round(S2, 3), "c2", c2, "level diff dB", round(float(best[0]), 2))
    p1 = splice(sc[:sec(A + X / 2)], sc[sec(A + S1 - X / 2):], X)    # after this, old t sits at new t - S1
    t_cut = c2 - S1
    p2 = splice(p1[:sec(t_cut + X / 2)], p1[sec(t_cut + S2 - X / 2):], X)
    print("score len", len(p2) / SR, "target", TOT)
    score = p2[:sec(TOT)]
    wav(H / "score_wordsfix1.wav", score)
    layers = [sfxlib.layer("wind_compelled", "wind_desert_bleak", "loop", 0.000, round(54.479 - S1, 3), -46.0, fin=2.0, fout=3.0),
              sfxlib.layer("gate_creak", "door_gate_creak", "oneshot", 5.699, 5.000, -30.0, fin=0.0, fout=1.0),
              sfxlib.layer("soldiers", "soldiers_march_armor", "loop", 5.699, 19.360, -42.0, fin=1.0, fout=2.0),
              sfxlib.layer("simon_turns", "footsteps_dirt_approach", "oneshot", 25.059, 4.000, -38.0, fin=0.0, fout=1.5),
              sfxlib.layer("wind_return", "wind_desert_bleak", "loop", round(67.180 - S1, 3), round(TOT - (67.180 - S1), 3), -46.0, fin=3.0, fout=4.0,
                           filt="volume='if(lt(t,19),1,pow(10,-(t-19)*0.22))':eval=frame")]  # tames the loop's 3 s gust that would land in the landing hold
    old_w = json.loads((EP / "narration.alignment.json").read_text(encoding="utf-8"))
    words = []
    def add(text, s, e, src):
        words.append({"text": text, "start": round(s, 3), "end": round(e, 3), "loss": 0.0, "src": src})
        words.append({"text": " ", "start": round(e, 3), "end": round(e + 0.001, 3), "loss": 0.0})
    for w in old_w["words"]:
        if w["text"].strip() and w["end"] <= K1: words += [w, {"text": " ", "start": w["end"], "end": w["end"] + 0.001, "loss": 0.0}]
    for w in rel["mid_a"]["words"]:
        add(w["w"], P_MID + mmap(w["start"]), P_MID + mmap(w["end"]), "wordsfix1_mid_take_a")
    for w in old_w["words"]:
        if w["text"].strip() and K2 <= w["start"] and w["end"] <= K3:
            words += [{**w, "start": round(w["start"] - S1, 3), "end": round(w["end"] - S1, 3)}, {"text": " ", "start": round(w["end"] - S1, 3), "end": round(w["end"] - S1 + 0.001, 3), "loss": 0.0}]
    for w in rel["end_a"]["words"]:
        add(w["w"], P_END + emap(w["start"]), P_END + emap(w["end"]), "wordsfix1_end_take_a")
    out = {"characters": old_w.get("characters", []), "words": words, "loss": old_w.get("loss"),
           "note": "wordsfix1: 'words' only (for srt); 'characters' is the OLD file's and is not valid for the new text"}
    (H / "narration.alignment_wordsfix1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    json.dump({"NARR_LEN": NARR_LEN, "TOTAL": TOT, "P_END": P_END, "S1": S1}, open(H / "audio_params.json", "w"))
    print("NARR_LEN", NARR_LEN, "TOTAL", TOT, "last word end", last_end)
tag = mode
if mode == "null": narr = OLD_N
else:
    narr = H / "narration_wordsfix1.wav"; wav(narr, narr_arr)
wn = H / f"_{tag}_with_narration.m4a"
run(["ffmpeg", "-y", "-v", "error", "-i", str(narr), "-c:a", "aac", "-b:a", "192k", "-t", f"{TOT:.3f}", str(wn)])
scorefile = OLD_S if mode == "null" else H / "score_wordsfix1.wav"
filt = f"[1:a]{score_mix.AFMT},volume=-6dB[mus];" + "[0:a]" + score_mix.AFMT + f",apad=whole_dur={TOT},asplit=2[main][key];" \
    + "[mus][key]sidechaincompress=threshold=0.12:ratio=2.5:attack=20:release=250[musd];[main][musd]amix=inputs=2:normalize=0,alimiter=limit=0.97,aresample=44100[mix]"
mix_aac = H / f"_{tag}_mix_stage1.m4a"
run(["ffmpeg", "-y", "-v", "error", "-i", str(wn), "-i", str(scorefile), "-filter_complex", filt, "-map", "[mix]", "-c:a", "aac", "-b:a", "192k", "-t", f"{TOT:.3f}", str(mix_aac)])
VID = EP / "uplift" / "ep13_uplift_fix1.mp4"
s1 = H / f"_{tag}_stage1.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", str(VID), "-i", str(mix_aac), "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", str(s1)])
out = H / f"_{tag}_sfx.mp4"
sfxlib.build(s1, out, layers)
print("ok", out)
