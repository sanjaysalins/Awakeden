r"""$0 mix: narrator turns with internal pauses capped at CAP s and edge silence trimmed (natural speed unless ATEMPO set);
character lines from _takes (take a or b). 0.35 s before each character line, 1.0 s pause after Isaiah, 0.4 s before 'Still true.'.
Every line evened to -18 LUFS.  python build_mix.py a|b [atempo]  -> narration_<take>.mp3 + timeline_<take>.json"""
import re, sys, json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent; T = H / "_turns"; TK = H / "_takes"; W = H / "_work"; W.mkdir(exist_ok=True)
take = sys.argv[1]; ATEMPO = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0; CAP = 0.45
def run(*a): return subprocess.run(a, capture_output=True, text=True)
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)).stdout)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",str(f),"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
def clean(src, out, cap=True, tempo=1.0):
    d = dur(src); e = run("ffmpeg","-hide_banner","-i",str(src),"-af","silencedetect=n=-40dB:d=0.12","-f","null","-").stderr
    ss = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", e)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    se += [d] * (len(ss) - len(se))
    a0, a1 = 0.0, d
    keep, cur = [], None
    for a, b in zip(ss, se):
        if a <= 0.02: a0 = max(0.0, b - 0.05); continue        # leading silence
        if b >= d - 0.02: a1 = min(d, a + 0.12); continue      # trailing silence
        if cap and b - a > CAP: keep.append((a, b))
    segs, cur = [], a0
    for a, b in keep: segs.append((cur, a + CAP/2)); cur = b - CAP/2
    segs.append((cur, a1))
    sel = "+".join(f"between(t,{x:.3f},{y:.3f})" for x, y in segs)
    af = f"aselect='{sel}',asetpts=N/SR/TB" + (f",atempo={tempo}" if tempo != 1.0 else "")
    r = run("ffmpeg","-y","-v","error","-i",str(src),"-af",af,"-ar","44100","-ac","1",str(out)); assert r.returncode == 0, r.stderr
    return out
lines = re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H / "narration-tagged.md").read_text(encoding="utf-8"))
TAKES = {2: f"02_prophet_{take}.mp3", 5: f"05_angel_{take}.mp3", 8: f"08_jesus_{take}.mp3"}
PAUSE_AFTER = {2: 1.0}; PAUSE_BEFORE = {9: 0.4}
segs, tl, t = [], [], 0.0
for i, (who, text) in enumerate(lines):
    if i in TAKES: f = clean(TK / TAKES[i], W / f"{i:02d}_{take}.wav", cap=False)
    elif i == 6: f = clean(TK / "06_narrator_b.mp3", W / f"06_rb_n{ATEMPO}.wav", tempo=ATEMPO)  # retake: raw slurred "Jesus says"
    else: f = clean(T / f"{i:02d}_narrator.mp3", W / f"{i:02d}_n{ATEMPO}.wav", tempo=ATEMPO)
    pre = 0.35 if who != "narrator" else PAUSE_BEFORE.get(i, 0.0)
    if i and pre: segs.append(("SIL", pre)); t += pre
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": who, "start": round(t,3), "end": round(t+d,3), "text": text}); t += d
    if i in PAUSE_AFTER: segs.append(("SIL", PAUSE_AFTER[i])); t += PAUSE_AFTER[i]
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", str(f)]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
out = H / f"narration_{take}.mp3"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","128k",str(out)); assert r.returncode == 0, r.stderr
(H / f"timeline_{take}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print(take, "total", round(t, 2), "file", round(dur(out), 2))
