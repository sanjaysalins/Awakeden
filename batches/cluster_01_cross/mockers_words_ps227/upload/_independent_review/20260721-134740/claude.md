# Independent review — claude (OK, 96s)

## Findings

**1. The kit ships with its own red-team's REVISE unapplied — every flagged item is still in the copy.**
The header says "RED-TEAMED" and the auditor's verdict is REVISE, but not one fix was made:
- **YouTube Short:** "the wagging heads, the sneer, the very words" still sits under "(Psalm 22:8; Matthew 27:43)". The head-shaking is **Psalm 22:7** ("they shake the head"); v8 is only the spoken taunt. Still wrong.
- **YouTube Long:** "the gestures, the sneer, nearly line for line (Psalm 22:8)" — same error, still wrong.
- **Facebook:** "the wagging heads, the sneer, the very words (Psalm 22:8)" — same error, still wrong.
- **TikTok:** "Matthew heard them repeated word for word" — still overclaims. Matthew 27:43 ("He trusted in God") is not verbally identical to Psalm 22:8 KJV ("He trusted on the LORD"), and the video itself only claims "nearly line for line". Metadata promises more than the video delivers — that's the bait-and-switch rule.
- **TikTok:** "#fyp" is still in the hashtag block.

**2. The kit is in a FAILING gate state but presents itself as verified.**
"UK-G2 KJV-strict — ❌ could not resolve KJV text for " (blank), because the **Anchor field is empty**. The one deterministic verse check never ran. Yet the preamble says "Title, description, tags and hashtags are pre-checked, red-teamed and panel-reviewed" — and the header claims panel review that appears nowhere in the artifact. A kit with a red ❌ must not carry a "copy straight into the upload form" instruction. (The Matthew 27:43 quote does happen to be verbatim KJV — I checked it myself — but that's luck, not verification.)

**3. Gate-integrity contradiction on UK-G7.** It reports "plain ASCII" ✅, but every caption contains the non-ASCII "✝" glyph. Either the gate is lying or its description is; both undermine trust in the green checks.

**4. TikTok and Instagram captions have no CTA-to-Jesus.** "Subscribe to Awakeden" is a brand CTA, not the turn-to-Jesus invitation the charter requires. Both captions are far under their limits (311 and 378 chars) — there is room for the "Turn, and come to the One who would not come down" line that YT/FB carry. UK-G4's ✅ is over-generous here.

**5. Title option 3 overclaims:** "Why the Taunts at the Cross Match Psalm 22 **Line for Line**" drops the "nearly" the rest of the kit is careful about. It isn't the chosen title, but it's offered as a live option — tighten or cut it.

Minor: the long-form line "all the ends of the world shall remember and turn unto the LORD" is verbatim KJV (Psalm 22:27) but uncited — a reference would match the kit's own precision standard.

What's genuinely good: the chosen title is specific and honest, the Matthew 27:43 quote is exact KJV, tags are real search terms with no stuffing, hashtag counts are sane, and "He stayed… for the very people throwing it" is grace-anchored with no fear or gain-loss framing.

VERDICT: FAIL
TOP FIXES:
1. Fix the blank Anchor and re-run UK-G2 so the KJV check actually executes — a kit with a red ❌ gate must never say "pre-checked, copy straight into the upload form."
2. Apply the red-team's own fixes: cite Psalm 22:7-8 wherever the wagging heads are described (YouTube Short, YouTube Long, Facebook), change TikTok's "word for word" to "nearly line for line", and drop "#fyp".
3. Add the explicit turn-to-Jesus CTA line to the TikTok and Instagram captions, and reconcile UK-G7's "plain ASCII" pass with the "✝" glyph in every caption.
