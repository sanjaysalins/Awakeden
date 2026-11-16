"""Blind X/Y test pack for Ep 02 words. X/Y key kept out of the pack. $0."""
from pathlib import Path
H = Path(__file__).resolve().parent
def body(f): return "\n".join(l for l in (H / f).read_text(encoding="utf-8").splitlines() if not l.startswith("<!--"))
KEY = {"X": "CAND_B.md", "Y": "CAND_A.md"}
kjv = (H.parent / "KJV.txt").read_text(encoding="utf-8")
P = f"""You are ONE independent reviewer. You have not seen any other review. Be honest and specific. Do not flatter.

Below are TWO versions (X and Y) of the spoken words for a 59-second vertical video, episode 2 of a series "Promised, then kept" (an Old Testament promise and how it came true in Jesus). Audience: worldwide; many viewers have English as a second language, many know nothing about the Bible, many watch on a phone with captions. Look: bold comic-book art with orchestral music. Released before Christmas.

Voices: [narrator], [prophet] (Isaiah, KJV), [ahaz] (KJV), [angel] (KJV), [jesus] (KJV). (pause) = 1 second of silence. The voice must end by 56 seconds (about 2.6 words a second).

=== X ===
{body(KEY['X'])}

=== Y ===
{body(KEY['Y'])}

=== KJV (the only authority) ===
{kjv}
=== Answer, in this format (max ~450 words, plain English) ===
For EACH of X and Y:
1. NEWCOMER: as someone with no Bible knowledge, say in your own words who / what / why. Any line you would not understand? Quote it.
2. HOOK: would the first line make you keep watching? Is the question answered by the end? 0-10.
3. PROMISE: who promised what, how long before, and what came true? Is the promise HEARD, not just read? 0-10.
4. HARD WORDS: words that fail for a second-language listener or for auto-captions. Quote them.
5. BIBLE: any claim WRONG / OVERCLAIMED against the KJV above (remember Isaiah 7:15-16 also points to Ahaz's own day)? Quote it.
6. LANDING: does the end land on Jesus, earned, with grace and no pressure? 0-10.
7. Overall 0-10.
Then: PICK X or Y, in one line why, and ONE small change to the one you picked (exact wording).
"""
for bad in ("CAND_", "fable", "codex", "gemini", "grok", "Spine"):
    assert bad not in P, bad
(H / "TEST_PACK.md").write_text(P, encoding="utf-8")
(H / "_KEY_do_not_give.txt").write_text(str(KEY), encoding="utf-8")
print("ok", len(P.split()))
