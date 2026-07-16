import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # 04_The_Bronze_Serpent
ALIGN = HERE / "v1" / "narration.alignment.json"

d = json.loads(ALIGN.read_text(encoding="utf-8"))
allwords = d["words"]
first_real = next(i for i, w in enumerate(allwords) if w["end"] > 0)
WORDS = allwords[first_real:]


def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9']", "", s)
    return s


NORMS = [norm(w["text"]) for w in WORDS]


class Cursor:
    """Monotonic forward scanner over the narration word-timing array."""

    def __init__(self):
        self.i = 0

    def find(self, phrase):
        """Match a short RUN of leading words (not just the first), so common openers
        like 'The'/'And'/'It' don't false-match the nearest unrelated occurrence."""
        words = [norm(w) for w in phrase.split()]
        run = words[:3] if len(words) >= 3 else words
        n = len(run)
        j = self.i
        while j <= len(NORMS) - n:
            ok = True
            for k in range(n):
                tok = run[k]
                if not (NORMS[j + k] == tok or (len(tok) > 3 and NORMS[j + k].startswith(tok))):
                    ok = False
                    break
            if ok:
                return j
            j += 1
        raise ValueError(f"not found: {phrase!r} from i={self.i} ({NORMS[self.i:self.i+8]})")

    def t0(self, phrase):
        """Time the phrase STARTS; advances the cursor past the matched word."""
        j = self.find(phrase)
        self.i = j + 1
        return WORDS[j]["start"]

    def peek(self, phrase):
        j = self.find(phrase)
        return WORDS[j]["start"]

    def last_end(self):
        return WORDS[self.i - 1]["end"] if self.i > 0 else 0.0

    def total_end(self):
        return WORDS[-1]["end"]
