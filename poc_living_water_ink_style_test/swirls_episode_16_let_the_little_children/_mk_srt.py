"""$0 captions (upload-alongside .srt, not burned) from narration.alignment.json (whisperx on the
locked voice; film timing = voice timing, the landing hold is after the last word).
Two whisperx starts are stretched over a pause and are corrected by ear/shot cuts:
"Suffer" 31.29 -> 32.64 (Jesus voice starts, f979) and the quote-opening "He" 54.88 -> 56.10.
Cards break at phrase ends (. ? : !), max 9 words."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
words = json.loads((HERE / "narration.alignment.json").read_text(encoding="utf-8"))
FIX = {70: 32.64, 126: 56.10}
for i, s in FIX.items():
    words[i]["start"] = s


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


cards, cur = [], []
for w in words:
    cur.append(w)
    if w["w"].rstrip('"”').endswith((".", "?", ":", "!")) or len(cur) >= 9:
        cards.append(cur)
        cur = []
if cur:
    cards.append(cur)
out = []
for n, c in enumerate(cards, 1):
    end = min(c[-1]["end"] + 0.15, cards[n][0]["start"] if n < len(cards) else 99)
    out += [str(n), f"{ts(c[0]['start'])} --> {ts(end)}", " ".join(w["w"] for w in c), ""]
p = HERE / "swirls_episode_16_let_the_little_children.srt"
p.write_text("\n".join(out), encoding="utf-8")
print(p, len(cards), "cards")
