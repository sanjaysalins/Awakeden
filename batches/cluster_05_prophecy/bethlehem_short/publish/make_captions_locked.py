"""$0: readable captions for film v6 (red team r3/r4): cues >= 1.0 s, lines <= 42 chars, <= ~20 chars/s,
quote marks on the prophet/scribe lines. Times from visual/bethlehem_final.words.json. -> captions_locked.srt
(cli_publish --index copies it to captions.srt instead of rebuilding from words)."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent
W = json.loads((H.parent / "visual" / "bethlehem_final.words.json").read_text(encoding="utf-8"))
CUES = [
 ["The Bible experts knew where the King", "would be born. Did they go?"],
 ["About seven hundred years before,", "the prophet Micah named a small town:"],
 ["Bethlehem. God promised a King", 'from there: "ruler in Israel."'],
 ['It goes on: "from everlasting."'],
 ["Bethlehem would be His birthplace,", "not His beginning."],
 ["There, God's promise came true:", "Jesus, the King, was born."],
 ["Wise men came asking for this King.", "King Herod asked the experts."],
 ['"In Bethlehem of Judaea."'],
 ["Bethlehem was close by."],
 ["The Bible never says the experts went."],
 ["The wise men went,", "and found the child."],
 ["Jesus grew up in Galilee."],
 ["People argued:", "can the King come from Galilee?"],
 ["The promise said Bethlehem.", "He was born there."],
 ["But Jesus came much farther.", "He came down from heaven."],
 ["He died for our sins."],
 ["On the third day,", "He rose from the dead."],
 ["Before anyone went to Him,", "He came to us."],
]
key = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
k, spans = 0, []
for c in CUES:
    toks = " ".join(c).split()
    first = None
    for tok in toks:
        assert key(W[k]["w"]) == key(tok), (k, W[k]["w"], tok)
        first = W[k]["start"] if first is None else first; last = W[k]["end"]; k += 1
    spans.append([first, last])
assert k == len(W), (k, len(W))
END = 59.3
for i, s in enumerate(spans):
    nxt = spans[i + 1][0] - 0.04 if i + 1 < len(spans) else END
    s[1] = min(nxt, max(s[1] + 0.6, s[0] + 1.0))
fmt = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
out, bad = [], []
for i, (c, (a, b)) in enumerate(zip(CUES, spans), 1):
    d, n = b - a, len(" ".join(c))
    if d < 1.0 or n / d > 20 or max(map(len, c)) > 42: bad.append((i, round(d, 2), round(n / d, 1), c))
    out.append(f"{i}\n{fmt(a)} --> {fmt(b)}\n" + "\n".join(c) + "\n")
(H / "captions_locked.srt").write_text("\n".join(out), encoding="utf-8")
print(len(CUES), "cues; over limits:", bad or "none")
