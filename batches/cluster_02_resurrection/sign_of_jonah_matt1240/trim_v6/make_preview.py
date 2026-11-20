"""$0 audio preview of a cut-only trim: removes sentences from the locked narration.mp3 at gap midpoints.
Usage: make_preview.py <name> <ids...>   (id 'p2' = delete 'The first day of the week, while it was still dark,'; 'r:a-b' = delete a time range)"""
import json, subprocess, sys
from pathlib import Path
H = Path(__file__).parent
S = json.load(open(H / "sentences.json", encoding="utf-8"))
SRC = H.parent / "audio" / "narration.mp3"
name, ids = sys.argv[1], sys.argv[2:]
def mid(a, b): return (a + b) / 2
cuts = []
for x in ids:
    if x.startswith("r:"):  # explicit in-sentence range r:a-b (seconds)
        a, b = map(float, x[2:].split("-")); cuts.append((a, b)); continue
    if x == "p2_DISABLED":
        cuts.append((mid(S[1]["end"], S[2]["start"]), 7.20)); continue
    i = int(x.lstrip("S"))
    a = mid(S[i - 1]["end"], S[i]["start"]) if i else 0
    b = mid(S[i]["end"], S[i + 1]["start"]) if i + 1 < len(S) else S[i]["end"] + 0.05
    cuts.append((a, b))
cuts.sort()
keep, t = [], 0.0
for a, b in cuts:
    if a > t: keep.append((t, a))
    t = max(t, b)
keep.append((t, S[-1]["end"] + 0.08))
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.015:.3f}:d=0.015[k{n}];" for n, (a, b) in enumerate(keep))
f += "".join(f"[k{n}]" for n in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,apad=pad_dur=3.0[o]"
out = H / f"preview_{name}.mp3"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(SRC), "-filter_complex", f, "-map", "[o]", "-b:a", "192k", str(out)], check=True)
kept = [s for s in S if not any(a <= mid(s["start"], s["end"]) <= b for a, b in cuts)]
txt = " ".join(s["text"] for s in kept).replace("The first day of the week, while it was still dark, Mary", "Mary") if "p2" in ids else " ".join(s["text"] for s in kept)
(H / f"preview_{name}.txt").write_text(txt, encoding="utf-8")
print(name, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip(), "s")
