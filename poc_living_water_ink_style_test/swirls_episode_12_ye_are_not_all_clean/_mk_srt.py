"""$0 captions from narration.alignment.json (local whisper on the raw v2b voice).
The film adds a 0.5 s pause after the Jesus line (v3_retro/build_v3.py), so every word
after it is shifted +0.5 s. Cards break at phrase ends (. ? : !), max 10 words; one hand break before "was not the one who left"."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
words = json.loads((HERE / "narration.alignment.json").read_text(encoding="utf-8"))["words"]
JESUS_END_RAW = 40.95  # end of _turns/00 + 01 (39.19 + 1.76)
PAUSE = 0.5
for w in words:
    if w["start"] >= JESUS_END_RAW:
        w["start"] += PAUSE; w["end"] += PAUSE

def ts(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

cards, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    t = w["text"].rstrip('"')
    nxt_gap = words[i + 1]["start"] - w["end"] if i + 1 < len(words) else 9
    nxt = words[i + 1]["text"] if i + 1 < len(words) else ""
    if (t == "them" and nxt == "was") or t.endswith((".", "?", ":", "!")) or (t.endswith(",") and nxt_gap > 0.45) or len(cur) >= 10:
        cards.append(cur); cur = []
if cur: cards.append(cur)
out = []
for n, c in enumerate(cards, 1):
    end = min(c[-1]["end"] + 0.15, cards[n][0]["start"] if n < len(cards) else 99)
    out += [str(n), f"{ts(c[0]['start'])} --> {ts(end)}", " ".join(w["text"] for w in c), ""]
p = HERE / "swirls_episode_12_ye_are_not_all_clean.srt"
p.write_text("\n".join(out), encoding="utf-8")
print(p, len(cards))
