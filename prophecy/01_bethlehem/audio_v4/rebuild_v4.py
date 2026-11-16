r"""v4.1 (2026-11-16): turn 01 = take3 ('About seven hundred years before...'), 'Later,' cut from raw turn 09 (2.074-2.58 s); turns 01+09 pauses capped 0.32 s, turn 01 tail 0.12 s, pause after 07 = 0.7 s. Run: python rebuild_v4.py 41
Words v4 mix, $0. python rebuild_v4.py 1|2  (which take of the 5 new turns).
Reused (from audio_v3, already approved): 00 hook, 02 prophet 'ruler in Israel.' (cut take), 06 scribe, 07 close by,
08 never says, 10 gospel, 11 landing. New turns 01 03 05 09 (narrator) get tighten (pauses capped 0.45 s, atempo 1.03,
same as v3); new 04 prophet 'from everlasting.' gets edge silence trimmed.
0.35 s before character lines; 1.0 s after turn 07 ('Bethlehem was close by.'); 0.3 s before the last line.
Every line evened to -18 LUFS. -> narration_v4_take<N>.mp3 + timeline_take<N>.json"""
import json, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
TAKE = sys.argv[1] if len(sys.argv) > 1 else "1"
W = H / "_work"; W.mkdir(exist_ok=True)
CAP, ATEMPO = 0.45, 1.03
def run(*a): return subprocess.run(a, capture_output=True, text=True, cwd=H)
dur = lambda f: float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)).stdout)
lufs = lambda f: float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run("ffmpeg", "-hide_banner", "-i", str(f), "-af", "ebur128=framelog=quiet", "-f", "null", "-").stderr)[-1])

def tighten(src, out, cap=None, tail=None):
    cap = cap or CAP
    d = dur(src)
    e = run("ffmpeg", "-hide_banner", "-i", str(src), "-af", "silencedetect=n=-38dB:d=0.2", "-f", "null", "-").stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", e)]; se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", e)]
    keep, cur = [], 0.0
    for a, b in zip(ss, se):
        if b - a > cap and b < d - 0.05:
            keep.append((cur, a + cap / 2)); cur = b - cap / 2
    end = d
    if tail is not None and ss and len(ss) > len(se) or (tail is not None and se and se[-1] >= d - 0.05):
        end = min(d, ss[-1] + tail)  # v4.1: trim the trailing silence of this turn to `tail` s
    keep.append((cur, end))
    sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
    r = run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", f"aselect='{sel}',asetpts=N/SR/TB,atempo={ATEMPO}", "-c:a", "libmp3lame", "-b:a", "128k", str(out))
    assert r.returncode == 0, r.stderr

def trim_edges(src, out):
    f = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.08"
    r = run("ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", f, "-c:a", "libmp3lame", "-b:a", "128k", str(out))
    assert r.returncode == 0, r.stderr

lines = re.findall(r'<speaker name="(\w+)">(.*?)</speaker>', (H / "narration-tagged.md").read_text(encoding="utf-8"))
SRC = {2: H / "_takes/02_prophet_ruler.wav", 6: H / "_takes/04_scribe_a.mp3"}
V41 = TAKE == "41"; TK = "1" if V41 else TAKE
if V41:  # cut 'Later,' from the RAW take-1 turn 09 (2.074-2.58 s, measured by silencedetect)
    rc = W / "raw41_09cut.mp3"
    r = run("ffmpeg", "-y", "-v", "error", "-i", str(H / "_takes/take1/09_narrator.mp3"), "-af", "aselect='not(between(t,2.074,2.58))',asetpts=N/SR/TB", "-c:a", "libmp3lame", "-b:a", "128k", str(rc)); assert r.returncode == 0, r.stderr
for i in (1, 3, 5, 9):
    src = H / f"_takes/take3/01_narrator.mp3" if (V41 and i == 1) else (W / "raw41_09cut.mp3" if (V41 and i == 9) else H / f"_takes/take{TK}/{i:02d}_narrator.mp3")
    o = W / f"t{TAKE}_{i:02d}.mp3"
    if V41 and i in (1, 9): tighten(src, o, cap=0.32, tail=0.12 if i == 1 else None)  # v4.1: fit under 60 s
    else: tighten(src, o)
    SRC[i] = o
o = W / f"t{TAKE}_04.mp3"; trim_edges(H / f"_takes/take{TK}/04_prophet.mp3", o); SRC[4] = o
PAUSE_AFTER = {7: 0.7 if V41 else 1.0}; PAUSE_BEFORE = {11: 0.3}
segs, tl, t = [], [], 0.0
for i, (who, text) in enumerate(lines):
    pre = 0.35 if who != "narrator" else PAUSE_BEFORE.get(i, 0.0)
    if i and pre: segs.append(("SIL", pre)); t += pre
    f = SRC.get(i, H / f"_turns/{i:02d}_narrator__atempo.mp3")
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": who, "start": round(t, 3), "end": round(t + d, 3), "text": text}); t += d
    if i in PAUSE_AFTER: segs.append(("SIL", PAUSE_AFTER[i])); t += PAUSE_AFTER[i]
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f", "lavfi", "-t", str(g), "-i", "anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", str(f)]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
out = H / f"narration_v4_take{TAKE}.mp3"
r = run("ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "128k", str(out))
assert r.returncode == 0, r.stderr
(H / f"timeline_take{TAKE}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print("take", TAKE, "total", round(t, 2))
for x in tl: print(f'{x["i"]:02d} {x["start"]:6.2f}-{x["end"]:6.2f} {x["who"]:8s} {x["text"][:60]}')
