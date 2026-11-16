r"""Rebuild narration.mp3 from picked takes: narrator turns + chosen character takes, 0.4 s before each quote,
every line evened to -18 LUFS. Writes narration.mp3 + timeline.json. $0."""
import subprocess, re, json
from pathlib import Path
H = Path(__file__).resolve().parent
PICK = {"02": "_takes/02_jesus_b.mp3", "03": "_takes/03_woman_b.mp3", "05": "_takes/05_jesus_b.mp3",
        "09": "_takes/09_jesus_b.mp3", "12": "_takes/12_woman_d.mp3"}   # 12: reflective take d (owner 2026-11-13)
# film-panel fixes (owner yes 2026-11-13): lines 07/14/15 re-recorded, takes a/a/b(trimmed trailing silence)
NFIX = {"07": "_takes/07_narrator_fix_a.mp3", "14": "_takes/14_narrator_fix_a.mp3", "15": "_takes/15_narrator_fix_b_trim.mp3"}
spk = ["narrator","narrator","jesus","woman","narrator","jesus","narrator","narrator","narrator","jesus","narrator","narrator","woman","narrator","narrator","narrator"]
lines = re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H/"narration-tagged.md").read_text(encoding="utf-8"))
def run(*a): return subprocess.run(a, capture_output=True, text=True, cwd=H)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",f,"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)
segs, tl, t = [], [], 0.0
for i, s in enumerate(spk):
    n = f"{i:02d}"
    if s == "narrator": f = NFIX.get(n, f"_turns/{n}_narrator__atempo.mp3")
    else: segs.append(("SIL", 0.0)); t += 0.4; f = PICK[n]
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": s, "start": round(t,3), "end": round(t+d,3), "text": lines[i][1]}); t += d
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    inputs += (["-f","lavfi","-t","0.4","-i","anullsrc=r=44100:cl=mono"] if f == "SIL" else ["-i", f])
    filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","128k","narration.mp3")
assert r.returncode == 0, r.stderr
(H/"timeline.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
for o in tl: print(f'{o["i"]:02d} {o["start"]:6.2f}-{o["end"]:6.2f} {o["who"]}')
print("total", round(t,2))
