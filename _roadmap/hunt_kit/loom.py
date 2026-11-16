"""Gate 1: python loom.py <topic_dir> "Luke 8:22-39"
Runs pipeline/concordance.py (the $0 concordance loom) and writes <topic_dir>/loom.md:
cross-book verbatim matches first (outside the Gospels), then thematic word overlaps, then Gospel parallels.
Ours only - run_seats.py checks it exists, but it is NEVER sent to a seat."""
import re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from pipeline import concordance as cc
GOSPELS = ("Matthew", "Mark", "Luke", "John")
TOP = 25

T = Path(sys.argv[1]).resolve()
passage = sys.argv[2]
m = re.match(r"(.+?) (\d+):(\d+)(?:-(\d+))?$", passage.strip())
if not m: sys.exit('loom: passage must look like "Luke 8:22-39"')
book, ch, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
idx = cc.get_index()
verb = cc.find_echoes(idx, book, ch, v1, v2)
them = cc.find_thematic_echoes(idx, book, ch, v1, v2)
gos = lambda c: c.match_ref.startswith(GOSPELS) and c.passage_ref.startswith(GOSPELS)
out = [f"# LOOM - {passage}", "", "OURS ONLY. Never sent to seats or judges. A match is shared WORDS, not a proven link.",
       "Look for matches in a book that is NOT a Gospel parallel: that is where a two-book angle comes from.", "",
       f"## Verbatim phrase matches outside the Gospel parallels (top {TOP})", ""]
for c in [c for c in verb if not gos(c)][:TOP]:
    out += [f"- {c.passage_ref}  <->  {c.match_ref}   score {c.score:.2f}, {c.shared_word_count} words shared",
            f'  shared: "{c.shared_phrase}"', f"  {c.match_ref}: {c.match_text}"]
out += ["", f"## Thematic word overlap (weaker; top {TOP})", ""]
for c in [c for c in them if not gos(c)][:TOP]:
    out += [f"- {c.match_ref}   score {c.score:.2f}", f"  shared words: {', '.join(c.shared_words)}", f"  {c.match_text}"]
par = [c for c in verb if gos(c)]
out += ["", "## Gospel parallels (same story told again; not a second book of the Bible's view)", ""]
out += [f"- {c.passage_ref} <-> {c.match_ref}: \"{c.shared_phrase}\"" for c in par[:10]]
(T / "loom.md").parent.mkdir(parents=True, exist_ok=True)
(T / "loom.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote", T / "loom.md", f"({len(verb)} verbatim, {len(them)} thematic)")
