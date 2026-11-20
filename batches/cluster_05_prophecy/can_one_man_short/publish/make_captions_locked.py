"""$0: readable captions for the Can One Man film (cues >= 1.0 s, lines <= 42 chars, <= ~20 chars/s, quote marks on KJV / spoken-quote lines). Text = narration.md. Times from visual/can_one_man_final.words.json (whisper on the voice track, corrected to the script). -> captions_locked.srt"""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent
W = json.loads((H.parent / "visual" / "can_one_man_final.words.json").read_text(encoding="utf-8"))
CUES = [
 ['One warning in the Bible', 'ends with "healed."'],
 ['In Mark, when Jesus gives it,', 'it ends "forgiven."'],
 ["Can one man give both?"],
 ["Through Isaiah, God warns:", "people will hear, but not understand,"],
 ["or else they would turn back, and"],
 ['"be healed."'],
 ["Jesus repeats it.", "What they would miss:"],
 ['"their sins should be forgiven them."'],
 ["In Matthew, Jesus says", "they closed their own eyes."],
 ["A man who cannot walk is brought."],
 ["Jesus first says:"],
 ['"Son, thy sins be forgiven thee."'],
 ["Some sit thinking:", "only God can forgive sins."],
 ["So Jesus heals him,"],
 ['"that ye may know that the Son of man'],
 ['hath power on earth to forgive sins."'],
 ["He means Himself.", "The man stands up and walks out."],
 ["Forgiven, and healed.", "Jesus has power to give both."],
 ["Turn back to God, and trust Jesus."],
 ["He forgives your sins,", "and heals your heart."],
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
END = 69.4
for i, s in enumerate(spans):
    nxt = spans[i + 1][0] - 0.04 if i + 1 < len(spans) else END
    s[1] = min(nxt, max(s[1] + 0.8, s[0] + 1.0))
fmt = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
out, bad = [], []
for i, (c, (a, b)) in enumerate(zip(CUES, spans), 1):
    d, n = b - a, len(" ".join(c))
    if d < 1.0 or n / d > 20 or max(map(len, c)) > 42: bad.append((i, round(d, 2), round(n / d, 1), c))
    out.append(f"{i}\n{fmt(a)} --> {fmt(b)}\n" + "\n".join(c) + "\n")
(H / "captions_locked.srt").write_text("\n".join(out), encoding="utf-8")
print(len(CUES), "cues; over limits:", bad or "none")
