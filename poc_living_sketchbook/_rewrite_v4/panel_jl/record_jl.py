"""Record LOCKED Jacob's Ladder words (2026-11-02). One ElevenLabs pass. Output audio/{lN.mp3,timing.json,narration.mp3}."""
import json, subprocess, sys, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import config  # loads env
spec = importlib.util.spec_from_file_location("_a2", ROOT / "poc_castbible_look" / "_02_audio.py")
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
H = Path(__file__).resolve().parent
V = json.loads((ROOT / "poc_living_water_ink_style_test/swirls_pilot_01_jacobs_ladder/voices.json").read_text())
N, G, J = (V[k]["voice_id"] for k in ("narrator", "god", "jacob"))
GAP = 0.32
# (voice, text, gap_after)
L = [
 (N, "Jacob tricked his blind father and took his brother's blessing. Now Esau wanted him dead. He ran. What would God say to a man like that?", GAP),
 (N, "He lay down in the open, with a stone for his pillow.", GAP),
 (N, 'In a dream he saw "a ladder set up on the earth," with "the angels of God ascending and descending on it."', GAP),
 (N, "The LORD stood above it and promised:", GAP),
 (G, "I will not leave thee.", GAP),
 (N, "Before Jacob did anything to make things right, God promised to stay.", GAP),
 (N, "Jacob woke afraid:", GAP),
 (J, "Surely the LORD is in this place; and I knew it not.", 1.5),
 (N, 'Centuries later, Jesus used that same picture about himself, calling himself the Son of man: "ye shall see heaven open, and the angels of God ascending and descending upon the Son of man."', GAP),
 (N, "Jacob never climbed that ladder. God came to him first.", 0.0),
]
d = H / "audio"; d.mkdir(exist_ok=True); A.AUD = d
inputs, timing, t = [], [], 0.0
for i, (v, text, gap) in enumerate(L, 1):
    mp3 = d / f"l{i}.mp3"
    if not mp3.exists():
        print(f"[tts] l{i} {len(text)}ch", flush=True); A.synth(v, text, mp3)
    du = A.dur(mp3)
    timing.append(dict(name=f"l{i}", start=round(t, 3), end=round(t + du, 3), text=text, voice=("narrator" if v == N else "god" if v == G else "jacob")))
    t += du + gap; inputs.append((mp3, gap))
(d / "timing.json").write_text(json.dumps(dict(total=round(t - L[-1][2], 3), chars=sum(len(x[1]) for x in L), lines=timing), indent=1))
n = len(inputs)
f = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}];" for i in range(n)); ch = ""
for i, (_, gap) in enumerate(inputs):
    ch += f"[a{i}]"
    if i < n - 1: f += f"aevalsrc=0:d={gap}:s=44100,aformat=channel_layouts=stereo[g{i}];"; ch += f"[g{i}]"
f += ch + f"concat=n={2*n-1}:v=0:a=1[out]"
cmd = ["ffmpeg", "-y", "-v", "error", "-threads", "3"]
for p, _ in inputs: cmd += ["-i", str(p)]
subprocess.run(cmd + ["-filter_complex", f, "-map", "[out]", str(d / "narration.mp3")], check=True)
print(f"[ok] {n} lines, {A.dur(d/'narration.mp3'):.1f}s, {sum(len(x[1]) for x in L)} chars")
