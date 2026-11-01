"""Record the LOCKED v3 words (ElevenLabs, per-line, narrator + quote voices).
Output: _rewrite_v3/audio/<piece>/lN.mp3 + timing.json + narration.mp3. Old audio untouched."""
import json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config
import importlib.util
spec = importlib.util.spec_from_file_location("_a2", ROOT / "poc_castbible_look" / "_02_audio.py")
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
H = Path(__file__).resolve().parent
NARR = config.VOICE_MAP["narrator"]; JES = config.VOICE_MAP["jesus"]; DIS = config.VOICE_MAP["disciples"]
GAP = 0.32
txt = (H / "LOCKED_WORDS_2026-11-01.md").read_text(encoding="utf8")
pieces = {}
for s in txt.split("## ")[1:]:
    n, b = s.split("\n", 1); pieces[n.strip()] = b.strip()
QV = {"jericho": {"thou shalt bind": DIS}, "bronze_serpent": {"And as Moses lifted": JES}}
def lines(name, body):
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z"])', body)
    out, buf = [], ""
    for s in sents:
        voice = next((v for k, v in QV.get(name, {}).items() if k in s), None)
        if voice:
            m = re.search(r'"([^"]+)"', s)
            q = m.group(0)
            pre, post = s[:m.start()].strip(), s[m.end():].strip()
            if buf or pre: out.append((NARR, (buf + " " + pre).strip())); buf = ""
            out.append((voice, q.replace('"', '“', 1)[:-1] + '”'))
            if post: buf = post.lstrip(".,;: ")
        else:
            buf = (buf + " " + s).strip()
            if len(buf) > 170: out.append((NARR, buf)); buf = ""
    if buf: out.append((NARR, buf))
    return out
def main():
    for name, body in pieces.items():
        d = H / "audio" / name; d.mkdir(parents=True, exist_ok=True); A.AUD = d
        L = lines(name, body); inputs, timing, t = [], [], 0.0
        for i, (v, text) in enumerate(L, 1):
            mp3 = d / f"l{i}.mp3"
            if not mp3.exists():
                print(f"[tts] {name} l{i} {len(text)}ch"); A.synth(v, text, mp3)
            du = A.dur(mp3); timing.append(dict(name=f"l{i}", start=round(t, 3), end=round(t + du, 3), text=text)); t += du + GAP; inputs.append(mp3)
        (d / "timing.json").write_text(json.dumps(dict(total=round(t - GAP, 3), lines=timing), indent=1))
        n = len(inputs); f = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}];" for i in range(n)); ch = ""
        for i in range(n):
            ch += f"[a{i}]"
            if i < n - 1: f += f"aevalsrc=0:d={GAP}:s=44100,aformat=channel_layouts=stereo[g{i}];"; ch += f"[g{i}]"
        f += ch + f"concat=n={2*n-1}:v=0:a=1[out]"
        cmd = ["ffmpeg", "-y", "-v", "error"]
        for p in inputs: cmd += ["-i", str(p)]
        subprocess.run(cmd + ["-filter_complex", f, "-map", "[out]", str(d / "narration.mp3")], check=True)
        print(f"[ok] {name}: {n} lines, {A.dur(d/'narration.mp3'):.1f}s, {sum(len(x[1]) for x in L)} chars")
main()
