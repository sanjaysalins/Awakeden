"""$0 KJV check: reads every `Ref "quote"` in TWO_DRIVERS_ROADMAP.md and checks it against data/kjv_full.
Checks words + order only (ignores case/punctuation). v1 (hard-coded list) kept as kjv_check_roadmap.v1.py."""
import re, sys
from pathlib import Path
sys.path.insert(0, r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\fresh_hunt")
from kjv_check import check
md = Path(__file__).with_name("TWO_DRIVERS_ROADMAP.md").read_text(encoding="utf-8")
pat = re.compile(r'((?:[1-3] )?[A-Z][a-z]+(?: of [A-Z][a-z]+)? \d+:\d+(?:-\d+)?) "([^"]+)"')
ok = bad = 0
for ref, q in pat.findall(md):
    good, text = check(ref, q)
    ok += good; bad += not good
    if not good: print("MISMATCH", ref, "|", q, "\n   real:", text[:250])
print(f"TOTAL {ok+bad}  OK {ok}  MISMATCH {bad}")
