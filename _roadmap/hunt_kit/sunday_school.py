"""Gate 2: python sunday_school.py <topic_dir> "Luke 8:22-39" [claude,codex]
Asks 2 CLI seats for the most common sermons on the passage; merges both lists into <topic_dir>/SUNDAY_SCHOOL.md
(the KILL LIST that run_seats.py appends to BRIEF.md). Edit it by hand if you like."""
import re, sys
from pathlib import Path
from _cli import read, run_panel
T = Path(sys.argv[1]).resolve()
passage = sys.argv[2]
seats = (sys.argv[3] if len(sys.argv) > 3 else "claude,codex")
P = read(Path(__file__).with_name("SUNDAY_SCHOOL_TEMPLATE.md")).replace("{PASSAGE}", passage)
run_panel(P, T, "sunday", ["", "", seats])
seen, lines = set(), []
for s in seats.split(","):
    f = T / f"sunday_{s}.md"
    for ln in (f.read_text(encoding="utf-8") if f.exists() else "").splitlines():
        ln = ln.strip()
        if ln.startswith(("-", "*")) and (key := re.sub(r"\W+", " ", ln.lower()).strip()) not in seen:
            seen.add(key); lines.append("- " + ln.lstrip("-* ").strip())
if not lines: sys.exit("sunday_school: no list came back; SUNDAY_SCHOOL.md NOT written")
(T / "SUNDAY_SCHOOL.md").write_text(
    f"## KILL LIST - the common sermons on {passage}. DO NOT give any of these as your angle, "
    "and do not give a re-worded copy of one.\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
print("wrote", T / "SUNDAY_SCHOOL.md", len(lines), "lines")
