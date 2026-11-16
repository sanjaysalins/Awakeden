"""Old film time (words v2 voice) <-> new film time (words v3 voice), piecewise-linear from shared-word anchors. $0."""
import json, re
from pathlib import Path
B = Path(__file__).resolve().parents[1]
OLD = json.loads((B / "audio_v2/narration_v2.words.json").read_text(encoding="utf-8"))
NEW = json.loads((B / "audio_v3/narration_v3.words.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower().replace("’", "'")).replace("judaea", "judea")
# anchor = (phrase start word in OLD, occurrence index, same in NEW). Sentence starts present in both voices.
KEYS = [("the", 0), ("did", 0), ("about", 0), ("named", 0), ("mary", 0), ("a", "tax"), ("wise", 0), ("in", "bethlehem"),
        ("bethlehem", "was"), ("the", "bible2"), ("the", "wise"), ("but", 0), ("he", "came"), ("he", "died"), ("before", 0)]
def find(W, word, nxt, after):
    for i in range(after, len(W) - 1):
        if norm(W[i]["w"]) == word:
            if nxt in (0,) or nxt == "bible2" and norm(W[i + 1]["w"]) == "bible" or norm(W[i + 1]["w"]) == nxt:
                return i
    raise KeyError((word, nxt))
def anchors():
    out, io, inn = [(0.0, 0.0)], 0, 0
    for w, nx in KEYS:
        io = find(OLD, w, nx, io); inn = find(NEW, w, nx, inn)
        out.append((OLD[io]["start"], NEW[inn]["start"])); io += 1; inn += 1
    def first(W, word, after_t):
        return next(x["start"] for x in W if norm(x["w"]) == word and x["start"] > after_t)
    out += [(first(OLD, "out", 10), first(NEW, "god", 10)),          # Micah's promise line
            (first(OLD, "that", 15), first(NEW, "ruler", 15.5)),     # prophet voice
            (first(OLD, "there", 22), first(NEW, "there", 21)),      # birth
            (first(OLD, "king", 29), first(NEW, "herod", 30))]       # Herod
    out.append((OLD[-1]["end"], NEW[-1]["end"]))
    return sorted(set(out))
A = anchors()
def _lerp(x, pts):
    for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
        if x <= a1: return b0 + (x - a0) * (b1 - b0) / (a1 - a0)
    (a0, b0), (a1, b1) = pts[-2], pts[-1]; return b1 + (x - a1)
def o2n(t): return _lerp(t, A)
def n2o(t): return _lerp(t, [(b, a) for a, b in A])
if __name__ == "__main__":
    for a, b in A: print(f"old {a:6.2f} -> new {b:6.2f}  (+{b - a:5.2f})")
