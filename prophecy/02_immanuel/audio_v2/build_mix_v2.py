r"""$0 mix for words v2: new lines from audio_v2/_takes, reused lines from audio/ (v1 Mix B takes).
Same rules as v1 build_mix.py: narrator pauses capped 0.45 s, edges trimmed, every line -18 LUFS,
0.35 s before character lines, 1.0 s after Isaiah, 0.4 s before the last line.
  python build_mix_v2.py <angel_take a|b>  -> narration_v2.mp3 + timeline_v2.json"""
import re, sys, json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent; V1 = H.parent / "audio"; W = H / "_work"; W.mkdir(exist_ok=True)
ANG = sys.argv[1] if len(sys.argv) > 1 else "a"
sys.argv = [sys.argv[0], "b"]   # reuse v1 helpers without running v1's mix
src = (V1 / "build_mix.py").read_text(encoding="utf-8").split("lines = re.findall")[0]
exec(src.replace('H = Path(__file__).resolve().parent', 'H = Path(r"%s")' % V1))
H = Path(__file__).resolve().parent; W = H / "_work"; W.mkdir(exist_ok=True)   # exec above reset H/W to v1
TK2 = H / "_takes"
import os
CAP = float(os.getenv("CAP", "0.45")); TEMPO = float(os.getenv("TEMPO", "1.0")); GAP = float(os.getenv("GAP", "0.35")); POSTP = float(os.getenv("POSTP", "1.0"))
# cut "With us as a baby." off the v1 cross line (speech resumes at 1.85 s)
cross = W / "08_cross_cut.mp3"
r = run("ffmpeg","-y","-v","error","-i",str(V1 / "_turns" / "07_narrator.mp3"),"-ss","1.80","-c:a","libmp3lame","-b:a","128k",str(cross)); assert r.returncode == 0 and cross.exists(), r.stderr
L = [  # (who, file, is_char, text)
 ("narrator", TK2 / "00_narrator_a.mp3", False, "A frightened king told God no. God answered anyway."),
 ("narrator", TK2 / os.getenv("L01", "01_narrator_a.mp3"), False, os.getenv("L01T", "King Ahaz, from King David's family, was afraid of war. God said, \"fear not,\" and offered any sign, as proof. Ahaz refused, and begged a foreign king: \"save me.\" God chose the sign:")),
 ("prophet",  V1 / "_takes" / "02_prophet_b.mp3", True, "Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel."),
 ("narrator", TK2 / os.getenv("L03", "03_narrator_a.mp3"), False, os.getenv("L03T", "Seven hundred years later, Mary, a virgin, was pregnant by God's Holy Spirit.")),
 ("narrator", TK2 / "04_narrator_a.mp3", False, "An angel told Joseph:"),
 ("angel",    TK2 / f"05_angel_{ANG}.mp3", True, "Joseph, thou son of David, fear not to take unto thee Mary thy wife:"),
 ("angel",    V1 / "_takes" / "05_angel_b.mp3", True, "thou shalt call his name JESUS: for he shall save his people from their sins."),
 ("narrator", TK2 / "07_narrator_a.mp3", False, "Joseph obeyed. Ahaz begged a king to save him. This child saves. Immanuel means: God with us."),
 ("narrator", cross, False, "With us at the cross, where He died for our sins. On the third day, He rose from the dead. He promised:"),
 ("jesus",    V1 / "_takes" / "08_jesus_b.mp3", True, "I am with you alway."),
 ("narrator", TK2 / "10_narrator_a.mp3", False, "That was God's answer."),
]
PRE = {6: min(0.25, GAP), 10: 0.4}; POST = {2: POSTP}
segs, tl, t = [], [], 0.0
for i, (who, f0, ch, text) in enumerate(L):
    f = clean(f0, W / f"{i:02d}.wav", cap=not ch, tempo=(TEMPO if (not ch and i != 8) else 1.0))
    pre = PRE.get(i, GAP if ch else 0.0)
    if i and pre: segs.append(("SIL", pre)); t += pre
    d = dur(f); segs.append((f, -18.0 - lufs(f))); tl.append({"i": i, "who": who, "start": round(t,3), "end": round(t+d,3), "text": text}); t += d
    if i in POST: segs.append(("SIL", POST[i])); t += POST[i]
inputs, filt = [], []
for k, (f, g) in enumerate(segs):
    if f == "SIL": inputs += ["-f","lavfi","-t",str(g),"-i","anullsrc=r=44100:cl=mono"]; filt.append(f"[{k}:a]anull[a{k}]")
    else: inputs += ["-i", str(f)]; filt.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,volume={g:.2f}dB[a{k}]")
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[out]"
out = H / f"narration_v2_{ANG}{os.getenv('TAG', '')}.mp3"
r = run("ffmpeg","-y","-hide_banner","-loglevel","error",*inputs,"-filter_complex",fc,"-map","[out]","-c:a","libmp3lame","-b:a","128k",str(out)); assert r.returncode == 0, r.stderr
(H / f"timeline_v2_{ANG}{os.getenv('TAG', '')}.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
print(ANG, "total", round(t, 2), "file", round(dur(out), 2))
for x in tl: print(f'{x["i"]:2} {x["who"]:8} {x["start"]:6.2f}-{x["end"]:6.2f}  {x["text"][:50]}')
