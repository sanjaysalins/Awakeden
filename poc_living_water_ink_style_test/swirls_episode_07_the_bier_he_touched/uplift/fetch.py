"""fetch.py <list_json> <historyId>:<outfile> ...  -> downloads completed results (from an openart_creation_list dump)."""
import json, sys, subprocess
d = json.load(open(sys.argv[1], encoding="utf-8"))
want = dict(a.split(":", 1) for a in sys.argv[2:])
seen = set()
for it in d["items"]:
    h = it.get("historyId")
    if h in want:
        seen.add(h)
        print(h, it.get("status"), it.get("url", "")[:90])
        if it.get("status") == "completed" and it.get("url"):
            subprocess.run(["curl", "-sL", "-o", want[h], it["url"]])
for h in want:
    if h not in seen:
        print(h, "NOT IN LIST")
