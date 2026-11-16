"""Fetch exact KJV (bible-api.com) for Ep 02 Immanuel. $0."""
import json, urllib.request, urllib.parse
from pathlib import Path
REFS = ["Isaiah 7:1-16", "Isaiah 8:8-10", "Isaiah 9:6-7", "Matthew 1:18-25", "Luke 1:26-35", "John 1:14", "Matthew 28:20", "1 Corinthians 15:3-4"]
out = []
for r in REFS:
    u = "https://bible-api.com/" + urllib.parse.quote(r) + "?translation=kjv"
    d = json.load(urllib.request.urlopen(u, timeout=30))
    out.append(f"## {r}\n" + "\n".join(f"{v['book_name']} {v['chapter']}:{v['verse']} {' '.join(v['text'].split())}" for v in d["verses"]))
Path(__file__).with_name("KJV.txt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print("ok")
