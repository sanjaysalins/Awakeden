"""Fresh blind retest of CAND_A2 (single version). $0."""
from pathlib import Path
H = Path(__file__).resolve().parent
body = "\n".join(l for l in (H / "CAND_A2.md").read_text(encoding="utf-8").splitlines() if not l.startswith("<!--"))
kjv = (H.parent / "KJV.txt").read_text(encoding="utf-8")
P = f"""You are ONE independent reviewer. You have not seen any other review or any earlier version. Be honest and specific. Do not flatter.

Below are the spoken words for a 59-second vertical video, episode 2 of a series "Promised, then kept" (an Old Testament promise and how it came true in Jesus). Audience: worldwide; many viewers have English as a second language, many know nothing about the Bible, many watch on a phone with captions. Look: bold comic-book art with orchestral music. Released before Christmas.

Voices: [narrator], [prophet] (Isaiah, KJV), [angel] (KJV), [jesus] (KJV). (pause) = 1 second of silence. The voice must end by 56 seconds (about 2.6 words a second).

=== THE WORDS ===
{body}

=== KJV (the only authority) ===
{kjv}
=== Answer, in this format (max ~350 words, plain English) ===
1. NEWCOMER: as someone with no Bible knowledge, say in your own words who / what / why. Any line you would not understand? Quote it.
2. HOOK: would the first line make you keep watching? Is it answered by the end? 0-10.
3. PROMISE: who promised what, how long before, and what came true? Is it HEARD, not just read? 0-10.
4. HARD WORDS: words that fail for a second-language listener or for auto-captions. Quote them.
5. BIBLE: any claim WRONG / OVERCLAIMED against the KJV above (remember Isaiah 7:15-16 also points to King Ahaz's own day)? Quote it.
6. LANDING: does the end land on Jesus, earned, with grace and no pressure? 0-10.
7. Overall 0-10.
8. ONE small change, if any (exact wording).
"""
for bad in ("CAND_", "fable", "codex", "gemini", "grok", "X ", "Y "):
    assert bad not in P, bad
(H / "RETEST_PACK.md").write_text(P, encoding="utf-8"); print("ok", len(P.split()))
