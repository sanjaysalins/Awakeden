"""$0 KJV check: python kjv_check.py "Genesis 35:18" "quote words" ... (pairs). Prints OK / MISMATCH + real text."""
import json, re, sys
from pathlib import Path
K = Path(r"F:\slk\PycharmProjects\JesusInTheBible\data\kjv_full")
def verse(ref):
    m = re.match(r"(.+?)\s+(\d+):(\d+)(?:-(\d+))?$", ref.strip())
    b, c, v1, v2 = m.group(1).replace(" ", ""), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
    b = {"Psalm": "Psalms", "SongofSolomon": "SongofSolomon"}.get(b, b)
    d = json.loads((K / f"{b}.json").read_text(encoding="utf-8-sig"))
    ch = next(x for x in d["chapters"] if x["chapter"] == c)
    return " ".join(x["text"] for x in ch["verses"] if v1 <= int(x["verse"]) <= v2)
norm = lambda s: re.sub(r"[^a-z ]", "", s.lower().replace("\u2019", "'")).split()
def check(ref, q):
    t = verse(ref); tn, qn = " ".join(norm(t)), " ".join(norm(q))
    return qn in tn, t
if __name__ == "__main__":
    a = sys.argv[1:]
    for ref, q in zip(a[::2], a[1::2]):
        ok, t = check(ref, q); print(("OK      " if ok else "MISMATCH"), ref, "|", q, "\n         ", t[:300])
