"""Build _remotion/public/bethlehem/film_v3_data.json: pills with per-word times (from audio_v2/narration_v2.words.json) + marks. $0."""
import json, re
from pathlib import Path
R = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
W = json.loads((R / "prophecy/01_bethlehem/audio_v2/narration_v2.words.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("\u2019", "'"))
# id, mode(pop|read|sacred|card), start, end, lines, cy, marks {word: [type, ...]}
P = [
 ("h1", "pop", 0.0, 3.1, ["The Bible experts knew", "where the King would be born."], 1350, {"knew": ["gold", "ticks"]}),
 ("m1", "read", 5.86, 7.4, ["a prophet called Micah,"], 1440, {}),
 ("m2", "read", 7.42, 9.6, ["a man who spoke", "God's message,"], 1440, {}),
 ("m3", "read", 9.62, 12.6, ["named a small town:", "Bethlehem."], 1440, {"Bethlehem.": ["gold"]}),
 ("m4", "read", 12.64, 15.6, ["Out of it, he said,", "a ruler would come,"], 1440, {}),
 ("j1", "read", 17.86, 20.5, ["Mary and Joseph", "lived far away."], 1440, {}),
 ("j2", "read", 20.52, 22.7, ["A tax order sent them", "to Bethlehem."], 1440, {"Bethlehem.": ["gold"]}),
 ("j3", "sacred", 22.76, 25.1, ["There, Jesus was born."], 1440, {}),
 ("w1", "read", 25.18, 29.2, ["Wise men from the east came", "asking for the one born King."], 1440, {}),
 ("w2", "read", 29.32, 32.2, ["King Herod asked", "the experts where."], 1440, {"where.": ["wavy"]}),
 ("sp", "speech", 32.24, 34.7, ["In Bethlehem of Judaea."], 1440, {"Bethlehem": ["gold", "star"]}),
 ("cb", "read", 34.8, 37.3, ["Bethlehem was close by."], 1350, {"Bethlehem": ["gold"]}),
 ("n1", "read", 37.44, 40.4, ["The Bible never says", "the experts went."], 1350, {"never": ["under2"], "went.": ["empty"]}),
 ("n2a", "read", 40.52, 41.93, ["The wise men went,"], 1350, {"went,": ["gold"]}),
 ("n2b", "sacred", 41.93, 43.4, ["and found the child."], 1440, {}),
 ("l1", "sacred", 43.52, 45.9, ["But Jesus had come", "much farther."], 1440, {"farther.": ["spread"]}),
 ("l2", "sacred", 46.04, 48.0, ["He came down", "from heaven."], 1440, {}),
 ("l3", "sacred", 48.1, 50.4, ["He died for our sins."], 1440, {}),
 ("l4", "sacred", 50.52, 52.4, ["He rose again", "the third day."], 1440, {}),
 ("p10", "final", 52.5, 57.2, ["Before anyone went to Him,", "He came to us."], 1440, {}),
]
items = []
for pid, mode, a, b, lines, cy, marks in P:
    pool = [w for w in W if a - 0.25 <= w["start"] < b + 0.05]
    wl, k = [], 0
    for ln in lines:
        row = []
        for tok in ln.split(" "):
            t = None
            while k < len(pool) and norm(pool[k]["w"]) != norm(tok): k += 1
            if k < len(pool): t = pool[k]["start"]; k += 1
            row.append({"t": tok, "at": t if t is not None else a, "m": marks.get(tok, [])})
        wl.append(row)
    miss = [x["t"] for r in wl for x in r if x["at"] == a and x["t"] != lines[0].split(" ")[0]]
    if miss: print("WARN no time", pid, miss)
    items.append({"id": pid, "mode": mode, "start": a, "end": b, "cy": cy, "lines": wl})
d = json.loads((R / "_remotion/public/bethlehem/film_v2_data.json").read_text(encoding="utf-8"))
out = {"frames": d["frames"], "edl": d["edl"], "pills": items,
       "scroll": {"lines": [["that", "is", "to", "be"], ["ruler", "in", "Israel."]], "wt": [[15.82, 15.9, 16.04, 16.24], [16.4, 16.7, 17.22]]}}
(R / "_remotion/public/bethlehem/film_v3_data.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("pills", len(items)); print([(i["id"], [[round(x["at"],2) for x in r] for r in i["lines"]]) for i in items[:3]])
