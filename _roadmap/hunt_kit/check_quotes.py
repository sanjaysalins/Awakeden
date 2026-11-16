"""$0 quote check: python check_quotes.py <file.md> [more.md ...]
Finds every  Book C:V "quote"  and checks it against data/kjv_full (words + order; case/punctuation ignored).
A quote with ... is checked piece by piece. Prints MISMATCH lines, then TOTAL / OK / MISMATCH."""
import re, sys
from pathlib import Path
from _kjv import check
PAT = re.compile(r'((?:[1-3] )?[A-Z][a-z]+(?: of [A-Z][a-z]+)? \d+:\d+(?:-\d+)?)[ \t*_:,—-]{1,6}"([^"\n]+)"')
ok = bad = 0
for f in sys.argv[1:]:
    md = Path(f).read_text(encoding="utf-8", errors="replace")
    md = re.sub("[“”]", '"', md).replace("–", "-").replace("…", "...")
    n = b = 0
    for ref, q in PAT.findall(md):
        try:
            parts = [p for p in re.split(r"\.{3,}", q) if re.search("[A-Za-z]", p)]
            res = [check(ref, p) for p in parts]
            good, text = all(g for g, _ in res), res[0][1]
        except Exception as e:  # unknown book / chapter / verse
            good, text = False, f"(bad reference: {type(e).__name__})"
        n += 1; b += not good
        if not good: print("MISMATCH", Path(f).name, "|", ref, "|", q, "\n   real:", text[:250])
    print(f"{Path(f).name}: {n} quotes, {b} mismatch"); ok += n - b; bad += b
print(f"TOTAL {ok+bad}  OK {ok}  MISMATCH {bad}")
