import json, re
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); D = ROOT / "poc_comic_page" / "_words_mockers_r1"
corpus = json.load(open(ROOT / "data" / "kjv_corpus.json", encoding="utf-8-sig"))
def verse(book, ch, v):
    for b in corpus:
        if b["name"] == book: return b["chapters"][ch - 1][v - 1]
V = [("Psalms", 22, 6, 9), ("Psalms", 22, 27, 28), ("Matthew", 27, 39, 44), ("Matthew", 26, 53, 53), ("John", 10, 17, 18), ("Luke", 23, 34, 34)]
def norm(s): return re.sub(r"[^a-z' ]", " ", s.lower().replace("\u2019", "'")).split()
kjv_words = []
for bk, ch, a, b in V:
    for v in range(a, b + 1): kjv_words += norm(verse(bk, ch, v)) + ["|"]
def in_kjv(frag):
    f = norm(frag)
    if not f: return True
    n = len(f)
    return any(kjv_words[i:i + n] == f for i in range(len(kjv_words) - n + 1))
files = {"claude_faith": "claude_w_faith.md", "codex_hook": "codex_w_hook.md", "fable_free": "fable_free.md", "grok_plain": "grok_w_plain.md", "sonnet_story": "sonnet_story.md"}
checks = {"script": r"\bscript", "unwilling": r"unwilling", "scorn": r"\bscorn", "ends of world": r"ends of the world", "Messiah": r"messiah", "nearly line": r"line for line", "whole song": r"whole song"}
out = []
for k, fn in files.items():
    t = (D / "panel_r1" / fn).read_text(encoding="utf-8")
    body = t.split("(b)")[0].split("Word count")[0].split("WORD COUNT")[0]
    body = re.sub(r"\*\*\(a\) Narration\*\*", "", body)
    refs = re.findall(r"\[((?:Psalms?|Matthew|John|Luke) [\d:]+)\]", body)
    clean = re.sub(r"\[(?:Psalms?|Matthew|John|Luke) [\d:]+\]", "", body)
    clean = re.sub(r"\[(narrator|david|mocker)\]", "", clean)
    words = len(clean.split())
    quotes = re.findall(r"[\"\u201c]([^\"\u201d]+)[\"\u201d]", clean)
    bad = [q for q in quotes if not in_kjv(q)]
    # unquoted quote lines (grok style): [david]/[mocker] paragraphs
    for m in re.finditer(r"\[(david|mocker)\]\s*([^\[]+?)\s*\[(?:Psalms?|Matthew) [\d:]+\]", body):
        q = m.group(2).strip().strip("\"\u201c\u201d")
        if q and not in_kjv(q) and q not in bad: bad.append(q)
    flags = [n for n, rx in checks.items() if re.search(rx, clean, re.I)]
    out.append(dict(seat=k, words=words, secs_at_2_75wps=round(words / 2.75, 1), quotes=len(quotes), refs=refs, non_verbatim=bad, avoid_words_used=flags,
                    names_david="David" in clean, says_who_jesus=bool(re.search(r"Son of God", clean)), answers_who_wrote=bool(re.search(r"David", clean[:260])),
                    ends=clean.strip().split(chr(10))[-1][:160]))
for o in out: print(json.dumps(o, ensure_ascii=False))
json.dump(out, open(D / "judge_table.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
