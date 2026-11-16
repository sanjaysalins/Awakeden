"""Build _remotion/public/bethlehem/film_v5_data.json for words v3 ($0).
Pills carry the NEW words; every time is stored in OLD film coordinates (n2o) so the v4 graphics, which are keyed to
old frames, stay in sync. The TSX maps the real frame -> old frame with the same anchor table ("warp")."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from warp import A, n2o, NEW

R = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("\u2019", "'")).replace("judaea", "judea")
# id, mode, lines, cy, marks  (cy is overridden for some ids inside the TSX, same as v4)
P = [
 ("h1", "pop", ["The Bible experts knew", "where the King would be born."], 1350, {"knew": ["gold", "ticks"]}),
 ("m1", "read", ["a prophet called Micah,"], 1440, {}),
 ("m2", "read", ["a man who spoke", "God's message,"], 1440, {}),
 ("m3", "read", ["named a small town:", "Bethlehem."], 1440, {"Bethlehem.": ["gold"]}),
 ("m4", "read", ["God promised a King", "from there."], 1440, {"promised": ["gold"]}),
 ("m5", "read", ["Micah called Him"], 1440, {}),
 ("j1", "read", ["Mary and Joseph", "lived far away."], 1440, {}),
 ("j2", "read", ["A tax order sent them", "to Bethlehem."], 1440, {"Bethlehem.": ["gold"]}),
 ("j3", "sacred", ["There, God's promise", "came true:"], 1440, {"true:": ["gold"]}),
 ("j4", "sacred", ["Jesus, the King,", "was born."], 1440, {}),
 ("w1", "read", ["Wise men reached Jerusalem,", "asking where this King was."], 1440, {}),
 ("w2", "read", ["Herod, the king there,", "asked the experts."], 1440, {}),
 ("sp", "speech", ["In Bethlehem of Judaea."], 1440, {"Bethlehem": ["gold", "star"]}),
 ("cb", "read", ["Bethlehem was close by."], 1350, {"Bethlehem": ["gold"]}),
 ("n1", "read", ["The Bible never says", "the experts went."], 1350, {"never": ["under2"], "went.": ["empty"]}),
 ("n2a", "read", ["The wise men went,"], 1350, {"went,": ["gold"]}),
 ("n2b", "sacred", ["and found the child."], 1440, {}),
 ("l1", "sacred", ["But Jesus came", "much farther."], 1440, {"farther.": ["spread"]}),
 ("l2", "sacred", ["He came down", "from heaven."], 1440, {}),
 ("l3", "sacred", ["He died for our sins."], 1440, {}),
 ("l4", "sacred", ["On the third day,", "He rose from the dead."], 1440, {}),
 ("p10", "final", ["Before anyone went to Him,", "He came to us."], 1440, {}),
]
W = [w for w in NEW]
k = 0
built = []
for pid, mode, lines, cy, marks in P:
    rows, first, last = [], None, None
    for ln in lines:
        row = []
        for tok in ln.split(" "):
            while k < len(W) and norm(W[k]["w"]) != norm(tok):
                k += 1
            if k >= len(W):
                sys.exit(f"no time for {pid}:{tok}")
            t = W[k]["start"]; last = W[k]["end"]; first = t if first is None else first; k += 1
            row.append({"t": tok, "at": t, "m": marks.get(tok, [])})
        rows.append(row)
    built.append([pid, mode, cy, rows, first, last])
items = []
for i, (pid, mode, cy, rows, first, last) in enumerate(built):
    nxt = built[i + 1][4] if i + 1 < len(built) else last + 1.0
    s_new, e_new = first - 0.06, min(nxt - 0.04, last + 1.2)
    if pid == "h1": s_new = 0.0
    for r in rows:
        for w in r:
            w["at"] = round(n2o(w["at"]), 3)
    items.append({"id": pid, "mode": mode, "start": round(n2o(s_new), 3), "end": round(n2o(e_new), 3), "cy": cy, "lines": rows})
pr = [w for w in W if norm(w["w"]) in ("ruler", "in", "israel") and 15.5 < w["start"] < 17.5][:3]
true_t = next(w["start"] for w in W if norm(w["w"]) == "true" and w["start"] > 20)
born_end = next(w["end"] for w in W if norm(w["w"]) == "born" and w["start"] > 24)
old = json.loads((R / "_remotion/public/bethlehem/film_v3_data.json").read_text(encoding="utf-8"))
out = {"frames": old["frames"], "edl": old["edl"], "pills": items,
       "scroll": {"lines": [["ruler", "in", "Israel."]], "wt": [[round(n2o(w["start"]), 3) for w in pr]]},
       "marks": {"came_true": round(n2o(true_t), 3), "came_true_end": round(n2o(born_end + 0.5), 3)},
       "warp": [[round(a, 3), round(b, 3)] for a, b in A]}
(R / "_remotion/public/bethlehem/film_v5_data.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for it in items:
    print(it["id"], it["start"], it["end"], " ".join(w["t"] for r in it["lines"] for w in r))
print("scroll", out["scroll"]["wt"], "marks", out["marks"])
