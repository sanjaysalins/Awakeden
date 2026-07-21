# Independent review — claude (OK, 98s)

**Verdict up front: REVISE.** The copy itself is mostly honest and doctrinally sound, but this pack is presented as paste-ready while its own gates are red, and the red-team's findings sit unapplied in the same document.

## Findings

**1. Failing pack sold as paste-ready (worst problem).** Header line 2 says `Gates: FAILURES ❌` and the in-engine red-team says `VERDICT: REVISE` — yet the blockquote right under it says "Copy each block straight into the platform's upload form… pre-checked, red-teamed and panel-reviewed." That is false in this state. A kit with a FAILING UK-G7 must not carry the paste-ready instruction. Fix the gates, then re-issue.

**2. UK-G7 anchor front-load is a real failure, not lint noise.** The YouTube long description's first verse ref `(Isaiah 52:13-53:12)` lands at roughly character 220 — well past the ~157-char "…more" fold. The YouTube **Short** block already does this right (`(Isaiah 53)` at ~128 chars). Reuse that opening shape on the long: e.g. "…wrote down the death of a man he had never met (Isaiah 53): the wounds, the silence, the grave…"

**3. Unmarked KJV fragments in the long description — red-team flagged them and this draft still hasn't fixed them.** "of whom speaketh the prophet this" (Acts 8:34) and "all we like sheep have gone astray" (Isaiah 53:6) are woven into prose unquoted. And the red-team **missed one**: "that it pleased the LORD to bruise him" is Isaiah 53:10 near-verbatim, also unquoted in the same paragraph. Quote-mark all three at point of use, and loosen or exactly quote the tense-shifted Acts 8:35 paraphrase ("beginning at the same scripture, preaches unto him Jesus").

**4. Long-unit completeness: no CHAPTERS, no PINNED_COMMENT.** The red-team states the publish gate fails a long unit without timed chapters (the seven movements) and a pinned comment in youtube_long.md. Neither exists in this artifact. The pack cannot be called done without them.

**5. The 'clean yourself' grace flag is a false positive — but adjudicate it, don't ship red.** "You do not have to clean yourself up before you come" *negates* works-framing; it's grace-anchored, the film's own landing line. Either whitelist the negated form in the linter or reword — but the gate must go green explicitly, not be left failing.

**6. TikTok is the only platform with no CTA-to-Jesus.** YouTube/FB/IG all close "Come to the One it names." TikTok ends on "Subscribe to Awakeden" — a brand CTA, not a Christ CTA. One sentence fixes it.

**7. Short and long carry the identical YouTube title** ("Isaiah 53: The Death Described 700 Years Before It Happened"), presumably on the same channel. UK-G6 checks sibling collisions but not this internal one. Differentiate the short's title (e.g. lead with the hook question) or confirm the duplication is intended.

**What holds up:** Isaiah 53:5 is verbatim KJV everywhere it's quoted, marked and attributed (including Instagram's partial). "700 years" matches the narration's own claim and is honest rounding. Titles are specific and not clickbait — "the wounds, the silence, the grave, the rich man in his death" are all genuinely in the chapter. Tags are real search phrases, no stuffing; hashtag counts are sane; TikTok/IG first lines are strong.

VERDICT: REVISE
TOP FIXES:
1. Clear UK-G7 before re-issuing: front-load the Isaiah ref inside the first 157 chars of the youtube_long description (copy the Short's opening shape), and adjudicate the 'clean yourself' lint (whitelist the negated grace form or reword) — then drop the "paste-ready" claim until gates are green.
2. Quote-mark every KJV fragment in the long description — Acts 8:34, Isaiah 53:6, and the missed Isaiah 53:10 "it pleased the LORD to bruise him" — and fix or loosen the tense-shifted Acts 8:35 paraphrase.
3. Author the missing long-unit pieces: timed CHAPTERS for the seven movements and the PINNED_COMMENT (and add a one-line Come-to-Jesus CTA to the TikTok caption while in there).
