"""python -I fetch.py <creation_list_json_file>: download completed jobs listed in jobs.json {historyId: relative_out_path}; print status of all."""
import json, sys, urllib.request
from pathlib import Path
UP = Path(__file__).resolve().parent
jobs = json.loads((UP / "jobs.json").read_text())
d = json.load(open(sys.argv[1], encoding="utf-8"))
seen = set()
for x in d["items"]:
    h = x.get("historyId")
    if h in jobs and h not in seen:
        seen.add(h)
        out = UP / jobs[h]
        st = x.get("status")
        print(jobs[h], st, "exists" if out.exists() else "")
        if st == "completed" and x.get("url") and not out.exists():
            req = urllib.request.Request(x["url"], headers={"User-Agent": "Mozilla/5.0"})
            out.write_bytes(urllib.request.urlopen(req, timeout=300).read())
            print("  saved", out.name, out.stat().st_size)
for h in jobs:
    if h not in seen:
        print(jobs[h], "NOT IN LIST")
