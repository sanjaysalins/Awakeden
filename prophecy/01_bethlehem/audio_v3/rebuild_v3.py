r"""Words v3 mix (new turns 01 03 07 tightened by tighten.py). $0. Narrator turns from per_turn_synth (natural 1.0x); prophet = Mix-A take cut to 'that is to be ruler in Israel';
scribe = Mix-A take reused. 0.4 s before character lines; 1.0 s pause after turn 05 ('Bethlehem was close by.'); 0.5 s before the last line.
Every line evened to -18 LUFS. -> narration.mp3 (overwrites synth concat) + timeline.json"""
import subprocess, re, json
from pathlib import Path
H = Path(__file__).resolve().parent
lines = re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H/"narration-tagged.md").read_text(encoding="utf-8"))
SRC = {2: "_takes/02_prophet_ruler.wav", 4: "_takes/04_scribe_a.mp3"}
PAUSE_AFTER = {5: 1.0}; PAUSE_BEFORE = {8: 0.3}
def run(*a): return subprocess.run(a, capture_output=True, text=True, cwd=H)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg","-hide_banner","-i",f,"-af","ebur128=framelog=quiet","-f","null","-").stderr)[-1])
dur = lambda f: float(run("ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f).stdout)
segs, tl, t = [], [], 0.0
for i, (who, text) in enumerate(lines):
    pre = 0.35 if who != "narrator" else PAUSE_BEFORE.get(i, 0.0)
    if i and pre: segs.append(("SIL", pre)); t += pre
    f = SRC.get(i, f"_turns/{i:02d}_narrator__atempo.mp3")
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": who, "start": round(t,3), "end": round(t+d,3), "text": text}); t += d
    if i in PAUSE_AFTER: segs.append(("SIL", PAUSE_AFTER[i])); t += PAUSE_AFTER[i]
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", f]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","128k","narration_v3.mp3")
assert r.returncode == 0, r.stderr
(H/"timeline.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print("total", round(t,2))
