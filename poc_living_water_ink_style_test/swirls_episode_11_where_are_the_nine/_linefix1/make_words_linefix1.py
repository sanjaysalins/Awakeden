"""Words/timestamps file for the new cut, same schema as narration.alignment.json (ElevenLabs-style 'words'), so build_srt.build_from_cache works.
Old words kept where the old audio is kept (5.80..73.60 s, same times). New words = whisperx forced alignment of the two new takes, mapped to final time."""
import json, shutil
from pathlib import Path
H = Path(__file__).resolve().parent; EP = H.parent
old = json.loads((EP / "narration.alignment.json").read_text(encoding="utf-8"))
rel = json.loads((H / "new_lines_words_rel.json").read_text(encoding="utf-8"))
def fmap(t): return t + 0.08 if t < 2.95 else t + 0.08 - 0.40
words = []
for k, w in enumerate(rel["first_a"]["words"]):
    words.append({"text": w["w"], "start": round(fmap(w["start"]), 3), "end": round(fmap(w["end"]), 3), "loss": 0.0, "src": "linefix1_first_take_a"})
    words.append({"text": " ", "start": round(fmap(w["end"]), 3), "end": round(fmap(w["end"]), 3) + 0.001, "loss": 0.0})
keep = [x for x in old["words"] if 5.80 <= x["start"] < 73.60]
words += keep
OFF = 77.55 - 3.091
for w in rel["last_b"]["words"]:
    words.append({"text": " ", "start": round(w["start"] + OFF - 0.02, 3), "end": round(w["start"] + OFF, 3), "loss": 0.0})
    words.append({"text": w["w"], "start": round(w["start"] + OFF, 3), "end": round(w["end"] + OFF, 3), "loss": 0.0, "src": "linefix1_last_take_b"})
out = {"characters": old.get("characters", []), "words": words, "loss": old.get("loss"), "note": "linefix1: words only for srt; 'characters' is the OLD file's and is not valid for the new first/last lines"}
(H / "narration.alignment_linefix1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
d = H / "swirls_episode_11_where_are_the_nine_linefix1"; d.mkdir(exist_ok=True)
(d / "narration.alignment.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print(len(words))
