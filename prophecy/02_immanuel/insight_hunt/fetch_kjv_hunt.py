"""Fetch exact KJV for every verse the hunt seats quoted. $0."""
import json, urllib.request, urllib.parse, time
from pathlib import Path
REFS = ["Isaiah 7:2-4", "Isaiah 7:11-15", "Isaiah 7:22", "Isaiah 8:6-18", "Isaiah 9:1-2", "Isaiah 36:2", "Isaiah 37:6",
        "2 Kings 15:29", "2 Kings 16:5-8", "2 Kings 18:17", "2 Chronicles 28:20-21",
        "Matthew 1:9", "Matthew 1:20-24", "Matthew 4:13-16", "Matthew 18:20", "Matthew 28:20",
        "Luke 2:11-12", "Luke 2:34", "Hebrews 2:11-14", "1 Peter 2:7-8", "John 7:37", "John 9:7"]
out = []
for r in REFS:
    u = "https://bible-api.com/" + urllib.parse.quote(r) + "?translation=kjv"
    d = json.load(urllib.request.urlopen(u, timeout=30))
    out.append(f"## {r}\n" + "\n".join(f"{v['book_name']} {v['chapter']}:{v['verse']} {' '.join(v['text'].split())}" for v in d["verses"]))
    time.sleep(0.5)
Path(__file__).with_name("KJV_HUNT.txt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print("ok")
