"""Real verse text for seats + judges: python kjv_pack.py <topic_dir> "Mark 5:1-20" "Luke 8:39" ...
Writes <topic_dir>/KJV_PACK.md from data/kjv_full, one numbered verse per line. A range stays inside one chapter."""
import re, sys
from pathlib import Path
from _kjv import verse
T = Path(sys.argv[1]).resolve()
out = ["# KJV text (from data/kjv_full, verbatim)", ""]
for ref in sys.argv[2:]:
    cv, v1, v2 = re.match(r"(.+:)(\d+)(?:-(\d+))?$", ref.strip()).groups()
    out += [f"## {ref}"] + [f"{cv}{v} {verse(f'{cv}{v}')}" for v in range(int(v1), int(v2 or v1) + 1)] + [""]
(T / "KJV_PACK.md").write_text("\n".join(out), encoding="utf-8")
print("wrote", T / "KJV_PACK.md", len(sys.argv) - 2, "refs")
