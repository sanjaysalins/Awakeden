"""Extract ONLY the spoken narration from a long-form narration.md.

Keeps prose **only while inside a `## MOVEMENT ...` section** — so the trailing
non-spoken sections (`## DEPTH & SOURCING`, `## VOICE PLAN`, doctrine ledgers)
and the leading metadata block are dropped. Within a movement, drops heading
lines, `---` rules, and `**[narrator ...]**` / `**[the_LORD ...]**` stage tags,
keeping the spoken prose + KJV quotes verbatim. Writes <out>.
"""
import re
import sys
from pathlib import Path

src, out = sys.argv[1], sys.argv[2]
lines = Path(src).read_text(encoding="utf-8", errors="ignore").splitlines()

in_movement = False
kept = []
for ln in lines:
    s = ln.strip()
    if s.startswith("#"):                                  # any heading toggles section
        in_movement = bool(re.match(r"#+\s*MOVEMENT\b", s, re.I))
        continue
    if not in_movement:
        continue
    if not s or s.startswith("---"):
        continue
    if re.fullmatch(r"\*\*\[.*\]\*\*", s):                 # **[narrator — KJV, ...]** tags
        continue
    s = re.sub(r"[*_`>]", "", s)                           # drop md emphasis marks
    kept.append(s.strip())

spoken = re.sub(r"\s+", " ", " ".join(kept)).strip()
Path(out).write_text(spoken, encoding="utf-8")
print(f"{len(spoken)} chars, ~{len(spoken.split())} words -> {out}")
print("HEAD:", spoken[:240])
print("TAIL:", spoken[-240:])
