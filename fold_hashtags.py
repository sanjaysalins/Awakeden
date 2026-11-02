"""Fold each publish/*.md's HASHTAGS into the main DESCRIPTION/CAPTION body (idempotent).
Matches pipeline/publish_pack.render_platform_md: body + blank line + space-joined hashtags.
Usage: fold_hashtags.py <pack_folder> [...]"""
import re, sys
from pathlib import Path
def fold(f: Path) -> bool:
    t = f.read_text(encoding="utf-8")
    m = re.search(r"## HASHTAGS\n(.+?)(\n##|\Z)", t, re.S)
    if not m: return False
    tags = m.group(1).split()
    if not tags: return False
    bm = re.search(r"## (DESCRIPTION|CAPTION)\n", t)
    if not bm: return False
    nxt = re.search(r"\n## ", t[bm.end():])
    end = bm.end() + (nxt.start() if nxt else len(t) - bm.end())
    body = t[bm.end():end]
    if all(h in body for h in tags): return False
    body = body.rstrip() + "\n\n" + " ".join(tags) + "\n"
    f.write_text(t[:bm.end()] + body + t[end:], encoding="utf-8")
    return True
if __name__ == "__main__":
    n = 0
    for d in sys.argv[1:]:
        for f in sorted((Path(d) / "publish").glob("*.md")):
            n += fold(f)
    print("folded", n, "files")
