"""Words json for the srt: old narration.alignment.json words, cut words dropped, later words shifted (-4.6 s after cut1, -7.4 s after cut2). Same schema."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent; EP = H.parent
old = json.loads((EP / "narration.alignment.json").read_text(encoding="utf-8"))
def mp(t):
    if t < 12.40: return t
    if 17.00 <= t < 25.50: return t - 4.6
    if t >= 28.30: return t - 7.4
    return None
words = []
for w in old["words"]:
    a = mp(w["start"]); 
    if a is None: continue
    d = a - w["start"]
    n = dict(w); n["start"] = round(w["start"] + d, 3); n["end"] = round(w["end"] + d, 3); words.append(n)
out = {"characters": old.get("characters", []), "words": words, "loss": old.get("loss"),
       "note": "cutfix1: words only for srt; 'characters' is the OLD file's and not valid for the cut film"}
d = H / "swirls_episode_07_the_bier_he_touched_cutfix1"; d.mkdir(exist_ok=True)
(H / "narration.alignment_cutfix1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(d / "narration.alignment.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print(len(words), len(old["words"]))
