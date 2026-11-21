"""$0: readable captions for the Nazareth film (cues >= 1.0 s, lines <= 42 chars, <= ~20 chars/s,
quote marks on the KJV / spoken-quote lines). Text = words/FINAL_WORDS_v7.md ("home town" as scripted).
Times from visual/nazareth_final_linefix1.words.json (v7 per-turn whisper, 'hometown' split in two). -> captions_locked.srt
(cli_publish --index copies it to captions.srt instead of rebuilding from words)."""
import json, re
from pathlib import Path
H = Path(__file__).resolve().parent
W = json.loads((H.parent / "visual" / "nazareth_final_linefix1.words.json").read_text(encoding="utf-8"))
CUES = [
 ["Afraid God is angry with you?"],
 ["Watch where Jesus stopped reading."],
 ["In Nazareth, His home town,", "He read God's promise"],
 ["of someone sent with good news", "for the poor,"],
 ["and a time of God's welcome."],
 ["The prophet Isaiah's sentence goes on:"],
 ['"and the day of vengeance of our God."'],
 ["He left the day of vengeance unread,", "and sat down."],
 ['"This day is this scripture fulfilled."'],
 ["It was about Him."],
 ["They would want miracles, and say:"],
 ['"Physician, heal thyself."'],
 ["He reminded them God once sent help", "to foreigners, not to their own."],
 ["Furious, they took Him to a cliff", "to throw Him down."],
 ["He walked right through them."],
 ["Later, at the cross, the same dare:"],
 ['"He saved others; let him save himself."'],
 ["This time, He stayed."],
 ["He died, and rose again."],
 ["He stopped reading at the welcome."],
 ["It is still open, for you, today."],
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
END = 59.5
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
