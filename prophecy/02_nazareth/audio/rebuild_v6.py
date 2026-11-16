r"""Build v6 narration from takes. $0.  python rebuild_v6.py a|b  (a/b = take for jesus 07 + leader 10) -> narration_v6<tag>.mp3 + timeline_v6<tag>.json
Gaps (tightened to fit 60 s): 0.4 after hook, 0.3 before character lines, 0.8 (pause) before Jesus 'This day', 0.6 at the other (pause) marks; takes from _trim/, 3.0 s hold; every line -18 LUFS."""
import subprocess, re, json, sys
from pathlib import Path
H = Path(__file__).resolve().parent
tag = sys.argv[1]
SP = [("00_narrator_a","narrator",0), ("v6_01_narrator_a","narrator",.4), ("v6_02_narrator_a","narrator",.25), ("02_isaiah_b","isaiah",.3),
      ("v6_03t_narrator_a","narrator",.3), ("04_jesus_b","jesus",.8), ("v6_06_narrator_a","narrator",.4), (f"v6_07_jesus_{tag}","jesus",.3),
      ("v6_08_narrator_a","narrator",.3), ("v6_09_narrator_a","narrator",.6), (f"v6_10_leader_{tag}","leader",.3),
      ("v6_11_narrator_a","narrator",.3), ("v6_12_narrator_a","narrator",.6)]
run = lambda *a: subprocess.run(a, capture_output=True, text=True, cwd=H)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",f,"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)
segs, tl, t = [], [], 0.0
for i, (n, s, gap) in enumerate(SP):
    if gap: segs.append(("SIL", gap)); t += gap
    f = f"_trim/{n}.mp3"; d = dur(f)  # silence-trimmed copies of _takes
    segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": s, "file": f, "start": round(t,3), "end": round(t+d,3)}); t += d
segs.append(("SIL", 3.0)); t += 3.0
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", f]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error","-threads","2",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","160k",f"narration_v6{tag}.mp3")
assert r.returncode == 0, r.stderr
(H/f"timeline_v6{tag}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print(tag, "total", round(t,2), "s")
for x in tl: print(" %6.2f-%6.2f %s %s" % (x["start"], x["end"], x["who"], x["file"]))
