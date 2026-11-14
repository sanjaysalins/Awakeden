r"""Rebuild narration from picked takes. $0. Usage: python rebuild_narration.py a|b|00=a,04=b,...  -> narration_<tag>.mp3 + timeline_<tag>.json
Narrator turns natural 1.0x; 0.4 s before each character line; 1.0 s (pause) after turns 05 and 15 (v4 words); every line evened to -18 LUFS."""
import subprocess, re, json, sys
from pathlib import Path
H = Path(__file__).resolve().parent
spk = ["bartimaeus","narrator","narrator","narrator","narrator","bartimaeus","narrator","narrator","jesus","bartimaeus","jesus","narrator","narrator","narrator","narrator","narrator","narrator"]
arg = sys.argv[1]
pick = {f"{i:02d}": arg for i, s in enumerate(spk) if s != "narrator"} if arg in ("a","b") else dict(kv.split("=") for kv in arg.split(","))
tag = arg if arg in ("a","b") else "pick"
lines = re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H/"narration-tagged.md").read_text(encoding="utf-8"))
def run(*a): return subprocess.run(a, capture_output=True, text=True, cwd=H)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",f,"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)
segs, tl, t = [], [], 0.0
for i, s in enumerate(spk):
    n = f"{i:02d}"
    if s == "narrator": f = f"_turns/{n}_narrator__atempo.mp3"
    else:
        if i: segs.append(("SIL", 0.4)); t += 0.4
        f = f"_takes/{n}_{s}_{pick[n]}.mp3"
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": s, "start": round(t,3), "end": round(t+d,3), "text": lines[i][1]}); t += d
    if i in (5, 15): segs.append(("SIL", 1.0)); t += 1.0
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", f]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","128k",f"narration_{tag}.mp3")
assert r.returncode == 0, r.stderr
(H/f"timeline_{tag}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print(tag, "total", round(t,2))
