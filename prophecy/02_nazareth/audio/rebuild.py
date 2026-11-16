r"""Build the narration from picked takes. $0.  python rebuild.py a|b|02=a,04=b,06=a  -> narration_<tag>.mp3 + timeline_<tag>.json
0.5 s after the hook, 0.4 s before each character line, 0.9 s (pause) before Jesus, 3.0 s landing hold at the end; every line evened to -18 LUFS."""
import subprocess, re, json, sys
from pathlib import Path
H = Path(__file__).resolve().parent
SP = [("00","narrator"),("01","narrator"),("02","isaiah"),("03","narrator"),("04","jesus"),("05","narrator"),("06","townsman"),("07","narrator"),("08","narrator")]
arg = sys.argv[1]
pick = {n: arg for n, s in SP if s != "narrator"} if arg in ("a","b") else dict(kv.split("=") for kv in arg.split(","))
tag = arg if arg in ("a","b") else "pick"
run = lambda *a: subprocess.run(a, capture_output=True, text=True, cwd=H)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",f,"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)
segs, tl, t = [], [], 0.0
for i, (n, s) in enumerate(SP):
    gap = 0.9 if s == "jesus" else 0.4 if s != "narrator" else 0.5 if i == 1 else 0.7 if n == "08" else 0.0
    if gap: segs.append(("SIL", gap)); t += gap
    f = f"_takes/{n}_{s}_{'a' if s == 'narrator' else pick[n]}.mp3"
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": s, "file": f, "start": round(t,3), "end": round(t+d,3)}); t += d
segs.append(("SIL", 3.0)); t += 3.0
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", f]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error","-threads","2",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","160k",f"narration_{tag}.mp3")
assert r.returncode == 0, r.stderr
(H/f"timeline_{tag}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print(tag, "total", round(t,2), "s; Jesus starts", tl[4]["start"])
