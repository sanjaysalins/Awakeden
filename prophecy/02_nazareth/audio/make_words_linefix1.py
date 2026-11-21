"""linefix1 words json: new first line (aligned take a, pause cut 1.82..2.52 -> -0.70 s after) + every old word (from the pack words json, 'home'+'town' split kept) shifted +1.2 s."""
import json
from pathlib import Path
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
old = json.load(open(R / r"batches\cluster_05_prophecy\nazareth_short\visual\nazareth_final.words.json"))
a = json.load(open(R / r"prophecy\02_nazareth\audio\_linefix1\words_a.json"))
CUT = 0.70
new = [{"w": x["w"], "start": round(x["start"] - (CUT if x["start"] >= 2.5 else 0), 3), "end": round(x["end"] - (CUT if x["start"] >= 2.5 else 0), 3)} for x in a]
rest = [dict(w=x["w"], start=round(x["start"] + 1.2, 3), end=round(x["end"] + 1.2, 3)) for x in old if x["start"] >= 2.8]
assert len(old) - len(rest) == 9, (len(old), len(rest))
out = new + rest
for p in (R / r"prophecy\02_nazareth\audio\narration_v7_lf1.words.json", R / r"batches\cluster_05_prophecy\nazareth_short\visual\nazareth_final_linefix1.words.json"):
    p.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(len(out), out[:12], out[-2:])
