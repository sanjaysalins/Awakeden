"""$0 captions from short_g5/narration.alignment.json (local faster-whisper, aligned to the
locked G5 words). Cards break at phrase ends (. ? : and closing quotes), max 10 words."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
words = json.loads((HERE / "short_g5" / "narration.alignment.json").read_text(encoding="utf-8"))["words"]

def ts(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

cards, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    t = w["text"].rstrip('"')
    nxt_gap = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 9
    if t.endswith((".", "?", ":", "!")) or (t.endswith(",") and nxt_gap > 0.45) or len(cur) >= 10:
        cards.append(cur); cur = []
if cur: cards.append(cur)
out = []
for n, c in enumerate(cards, 1):
    out += [str(n), f"{ts(c[0]['start'])} --> {ts(min(c[-1]["end"] + 0.15, cards[n][0]["start"] if n < len(cards) else 99))}", " ".join(w["text"] for w in c), ""]
p = HERE / "swirls_episode_06_talitha_cumi.srt"
p.write_text("\n".join(out), encoding="utf-8")
print(p, len(cards))
