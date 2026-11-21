r"""holdfix1 (fix wave 2026-11-21): landing hold >= 3.0 s from real clip frames + score tail fade 2.5 s + unspoken gloss cards / hook removed.
usage: ..\.venv\Scripts\python.exe holdfix1.py <film> <stage>   film in {thy,fin,forsaken}; stage in {prep,engine,video,audio,mux}
Video = pinned final stream-copied between keyframes; spans with burned cards are re-encoded from the clean engine preview (livingpage_short.spec_preview.mp4,
PSNR ~41-50 dB vs the pinned film outside overlays); tail beats rebuilt with the stock engine (clips at <=1x, trim only, no freeze/loop)."""
import json, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); CL = ROOT / "batches/cluster_01_cross"; HERE = Path(__file__).resolve().parent
FPS = 30
ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-r", "30", "-an", "-threads", "2"]
CFG = {
 "thy": dict(dir="into_thy_hands_luke2346", pinned="into_thy_hands_luke2346_sfx_v5hook_linefix1.mp4", new="into_thy_hands_luke2346_sfx_v5hook_linefix1_holdfix1",
   last_end=58.949, total_f=1863,
   # keyframe-bounded spans re-cut from the clean preview (frames): card1 12.3-14.1, card2 23.9-25.7
   spans=[(279, 438), (638, 882)],
   # tail: keep pinned up to frame 1771 (end of film), append ONE new beat (unseen frames of first_day_morning clip)
   keep_to=1771, tail_from=1771, slugs=["first_day_morning"],
   beats=[dict(src_idx=10, t=[1771, 1863], clips=[{"slug": "first_day_morning", "motion": "pushin", "t_in": 1.78}], cap=None)]),
 "fin": dict(dir="it_is_finished_john1930", pinned="it_is_finished_john1930_sfx_v5hook.mp4", new="it_is_finished_john1930_sfx_v5hook_holdfix1",
   last_end=59.034, total_f=1863, spans=[(1106, 1292)], keep_to=1634, tail_from=1634, slugs=["man_lifting_face_dawn", "cross_at_dawn"],
   beats=[dict(src_idx=15, t=[1634, 1713], wt=[54.533, 54.653, 54.873, 54.993, 55.493, 55.613, 55.733, 55.873, 56.073]),
          dict(src_idx=16, t=[1713, 1863], wt=[57.1, 57.22, 57.34, 57.46, 58.314, 58.614, 58.774])]),
 "forsaken": dict(dir="forsaken_cry_ps221", pinned="forsaken_cry_ps221_sfx_v5hook.mp4", new="forsaken_cry_ps221_sfx_v5hook_holdfix1",
   last_end=58.084, total_f=1835, spans=[(535, 814)], hook=(0, 148), keep_to=1551, tail_from=1551, slugs=["father_lamp_doorway", "cross_at_dawn"],
   beats=[dict(src_idx=11, t=[1551, 1685], wt=[52.262, 52.682, 52.902, 53.05, 53.202, 54.003, 54.163, 54.403, 54.703, 54.903]),
          dict(src_idx=12, t=[1685, 1835], wt=[56.404, 56.744, 57.064, 57.444, 57.624, 57.744])]),
}
def run(c):
    r = subprocess.run([str(x) for x in c], capture_output=True, text=True)
    if r.returncode: sys.exit("FAIL " + " ".join(map(str, c))[:250] + "\n" + r.stderr[-1500:])
def paths(f):
    c = CFG[f]; V = CL / c["dir"] / "visual"; P = V / "_holdfix1_pool"
    return c, V, P

def prep(f):
    c, V, P = paths(f); P.mkdir(exist_ok=True); (P / "clips").mkdir(exist_ok=True)
    for s in c["slugs"]:
        for ext in (".png", ".anchor.json", ".audit.json", ".quality.json"):
            if (V / (s + ext)).exists(): shutil.copy2(V / (s + ext), P / (s + ext))
        shutil.copy2(V / "clips" / (s + ".mp4"), P / "clips" / (s + ".mp4"))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "70", str(P / "silence70.wav")])
    old = json.loads((V / "livingpage_short.spec.json").read_text(encoding="utf-8"))["beats"]
    beats = []
    for b in c["beats"]:
        nb = json.loads(json.dumps(old[b["src_idx"]])); t0, t1 = b["t"][0] / FPS, b["t"][1] / FPS
        nb["t"] = [round(t0, 4), round(t1, 4)]
        if "clips" in b: nb["clips"] = b["clips"]
        if b.get("cap", 1) is None: nb.pop("cap", None)
        for k in ("sfx", "whip", "punch", "ramp", "inserts", "border_break"): nb.pop(k, None)
        if "panel_at" in nb: nb["panel_at"] = [round(t0 + 0.0, 4), round(t0 + 0.35, 4), round(t0 + 0.7, 4)]
        if "wt" in b:
            nb["cap"]["word_t"] = [max(0.0, round(w - t0, 3)) for w in b["wt"]]
        beats.append(nb)
    spec = {"audio": "silence70.wav", "total": round(c["total_f"] / FPS, 4), "cut_ticks": False, "motion": "smooth", "beats": beats}
    (P / "holdfix1.spec.json").write_text(json.dumps(spec, indent=1), encoding="utf-8"); print("prep ok", P)

def engine(f):
    c, V, P = paths(f)
    r = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"), str(HERE / "holdfix1_engine.py"), str(P), "holdfix1.spec.json"], capture_output=True, text=True)
    (P / "engine_run.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    if r.returncode: sys.exit("engine FAIL\n" + (r.stdout + r.stderr)[-2500:])
    print("engine ok")

def video(f):
    c, V, P = paths(f); W = P / "_compose"; W.mkdir(exist_ok=True)
    OLD = V / c["pinned"]; PREV = V / "livingpage_short.spec_preview.mp4"; TAILV = P / "holdfix1.spec_preview.mp4"
    # keyframe pts of the pinned file
    kf = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-skip_frame", "nokey", "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(OLD)], capture_output=True, text=True).stdout.split()
    kfd = {round(float(x.strip(",")) * FPS): float(x.strip(",")) for x in kf}
    names, cur = [], 0
    def cp(name, a, b):
        assert a in kfd, f"frame {a} is not a keyframe"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{kfd[a] + 0.01:.4f}", "-i", OLD, "-frames:v", b - a, "-an", "-c:v", "copy", "-avoid_negative_ts", "make_zero", W / f"{name}.mp4"])
    def reenc(name, src, a, b, extra=None):
        vf = f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS"
        if extra: run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-loop", "1", "-t", "6", "-i", extra[0], "-filter_complex", f"[0:v]{vf}[v0];[v0][1:v]overlay=0:0:enable='between(t,{extra[1]},{extra[2]})'[v]", "-map", "[v]", "-frames:v", b - a] + ENC + [W / f"{name}.mp4"])
        else: run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf] + ENC + [W / f"{name}.mp4"])
    edits = []  # (a, b, kind)
    if c.get("hook"): edits.append((c["hook"][0], c["hook"][1], "hook"))
    for a, b in c["spans"]: edits.append((a, b, "span"))
    edits.sort()
    for i, (a, b, kind) in enumerate(edits):
        if a > cur: cp(f"c{i}", cur, a); names.append(f"c{i}")
        if kind == "hook": reenc(f"e{i}", PREV, a, b, (str(P / "hookcard.png"), 0.0, 2.0))
        else: reenc(f"e{i}", PREV, a, b)
        names.append(f"e{i}"); cur = b
    if c["keep_to"] > cur:
        cp("ckeep", cur, c["keep_to"]); names.append("ckeep")
    n_tail = c["total_f"] - c["tail_from"]
    reenc("tail", TAILV, 0, n_tail); names.append("tail")
    (W / "list.txt").write_text("".join(f"file '{n}.mp4'\n" for n in names))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", W / "list.txt", "-c", "copy", W / "video_only.mp4"])
    print("video ok", names)


def mux(f):
    c, V, P = paths(f); A = V.parent / "audio" / "_holdfix1"; out = V / (c["new"] + ".mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "2", "-i", P / "_compose/video_only.mp4", "-i", A / "narration_holdfix1_mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", out])
    al = json.loads((V.parent / "audio/alignment.json").read_text(encoding="utf-8"))
    words = [{"w": w["w"], "start": w["start"], "end": w["end"]} for w in al if any(ch.isalnum() for ch in w["w"])]
    (V / (c["new"] + ".words.json")).write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8"); print("mux ok", out)

def verify(f):
    import numpy as np, scipy.io.wavfile as wf
    c, V, P = paths(f); out = V / (c["new"] + ".mp4")
    def dur(s):
        return float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries", "stream=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.split()[0])
    dv, da = dur("v"), dur("a"); words = json.loads((V / (c["new"] + ".words.json")).read_text(encoding="utf-8")); le = words[-1]["end"]
    tmp = P / "_ver.wav"; run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", tmp])
    a = wf.read(tmp)[1].astype(float) / 32768
    seg = a[-5 * 44100:]; rms = [20 * np.log10(np.sqrt((seg[i:i + 11025] ** 2).mean()) + 1e-9) for i in range(0, len(seg) - 11025 + 1, 11025)]
    last = a[-441:]; print(f"video {dv:.3f} audio {da:.3f} diff {abs(dv-da):.3f} | last word {le:.3f} hold(video) {dv-le:.3f}")
    print("RMS dB per 0.25s last 5s:", " ".join(f"{r:.0f}" for r in rms)); print("last 10ms peak", float(np.abs(last).max()))
    if len(sys.argv) > 3:
        for t in sys.argv[3].split(","):
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", out, "-frames:v", 1, "-vf", "scale=540:-1", P / f"_chk_{t}.png"])

if __name__ == "__main__":
    globals()[sys.argv[2]](sys.argv[1])
