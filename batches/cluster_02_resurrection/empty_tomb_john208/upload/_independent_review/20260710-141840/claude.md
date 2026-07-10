# Independent review — claude (OK, 65s)

This kit ships its own failure report and then tells you to paste anyway. Findings, most serious first:

**1. The kit is not actually done — it contradicts itself.**
- Header: `Gates: FAILURES ❌` and `❌ UK-G2 KJV-strict — could not resolve KJV text for ` (the Anchor field is **empty** — the kit has no verse anchor at all, so the KJV gate never ran on anything).
- Yet the intro says "pre-checked, red-teamed and panel-reviewed" and "Copy each block straight into the platform's upload form." That's a false claim of readiness. There is also no panel evidence in the artifact — only the in-engine red-team.

**2. The red-team's REVISE findings were never applied.** The hostile auditor (quoted inside the kit itself) flagged five fixes; **all five are still in the copy**:
- Chosen YouTube-short title still reads **"What Thief Folds the Face-Cloth?"** — KJV John 20:7 says *"wrapped together"*, the video's own narration says *"wraps"*, and "folds" is the vocabulary of the debunked folded-napkin/dinner-table legend. On a channel whose premise is text-accuracy, the CHOSEN title uses a verb that is in neither the text nor the video.
- TikTok caption still says "What thief **folds** the face-cloth?"
- Tags still include **"folded napkin"** (YT short) and **"folded napkin meaning"** (YT long) — SEO-baiting the myth the video never teaches. Off-thread promise.
- Facebook title still **"No Angel. No Risen Lord. Only the Linen."** — standalone it flatly denies the angels (Matt 28:2-5; Luke 24:4; and John 20:12, where Mary sees two angels *in this same chapter*). The scope ("what Peter and John saw") lives only in the description a scroller never reads.
- YT long description still quotes John 20:2 verbatim but unmarked/unreferenced, while 20:29 gets quotes + (KJV).

**3. UK-G7 "plain ASCII" is marked ✅ but every description contains "✝"** (non-ASCII). Either the gate didn't run on the final copy or it's broken — same credibility problem as UK-G2.

**4. Instagram caption doctrine wobble:** "You were not at the tomb. **Jesus called your faith blessed** (John 20:29)." John 20:29 blesses *"they that have not seen, and yet **have believed**"* — the caption drops the condition and declares an unbelieving scroller's faith already blessed. The YT/FB versions get this right ("Believe what John believed"); IG should match.

**5. Minor:** a full YouTube long-form 16:9 block is emitted for a piece whose Format is `short` and whose only listed video is the 9:16 `_sfx.mp4`. If there is no long-form render, this block is metadata for a video that doesn't exist and shouldn't be in a paste-ready kit.

What's genuinely good: John 20:29 is verbatim KJV everywhere it appears; footers/links intact; hashtag counts sane on all four platforms; the "He Believed Before He Ever Saw Jesus Alive" title option is honest and hooky — arguably the better CHOSEN.

VERDICT: FAIL
TOP FIXES:
1. Apply the red-team fixes it already lists: retitle to "What Thief Wraps the Face-Cloth? The Empty Tomb" (YT short + TikTok), drop/replace the "folded napkin" tags, scope the Facebook title to John ("John Saw No Angel — Only the Linen. And He Believed."), and add "(John 20:2, KJV)" to the long description quote.
2. Fix the empty Anchor field, re-run UK-G2 (and UK-G7, which false-passed on "✝") until the gate block is genuinely all-green — never ship a kit whose own header says FAILURES.
3. Instagram caption: restore the condition — "Believe what John believed — Jesus calls that faith blessed (John 20:29)" — and drop or clearly mark the long-form 16:9 block if no 16:9 render exists.
