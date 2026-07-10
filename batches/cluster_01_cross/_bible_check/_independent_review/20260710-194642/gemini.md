# Independent review — gemini (OK, 74s)

This is a strong baseline that successfully filters out common unbiblical tropes (like the lightning storm or replacing nails with ropes). However, you have violated your own bucket definitions by smuggling historical, botanical, and traditional inferences into the `[SPECIFIED]` bucket as if they were verbatim Scripture. There is also a major coverage gap for the journey to Golgotha.

Here are the specific findings:

**1. Citation Truth / No Invented Facts (Lots)**
*Phrase:* `[SPECIFIED] The garments were PARTED and LOTS CAST... lots = small unmarked objects.`
*Finding:* The cited verses (Psalm 22:18, John 19:23-24) simply state that they "cast lots." The Bible never describes the physical appearance of the lots. Claiming they are "small unmarked objects" is an archaeological inference, not an explicit biblical fact.

**2. Citation Truth / No Invented Facts (Hyssop)**
*Phrase:* `[SPECIFIED] The vinegar came on a SPONGE... Hyssop = a SMALL herb bunch bound to a reed — never a leafy branch...`
*Finding:* John 19:29 specifies "hyssop" and Matthew 27:48 specifies "a reed", but the text never defines hyssop botanically as a "SMALL herb bunch bound to a reed". This is a historical constraint dressed up as Scripture.

**3. Bucket Honesty / Tradition (Golgotha)**
*Phrase:* `[SPECIFIED] Golgotha, "that is to say, a place of a skull" (Matthew 27:33) — a bare rise outside the city (Hebrews 13:12 "suffered without the gate").`
*Finding:* The cited verses confirm "place of a skull" and "without the gate", but they *never* state that it was a "bare rise" or a hill. The hill of Calvary is pure tradition. This belongs in `[CONSTRAINED]` or `[FREE]`.

**4. Coverage Gap (The Road)**
*Phrase:* `The mocking and the road (Matt 27:27-33)`
*Finding:* Your scope includes verse 32, but you completely omit it. Matthew 27:32 states: "they found a man of Cyrene, Simon by name: him they compelled to bear his cross." For any depiction of "the road," Simon of Cyrene is a critical, checkable biblical fact that prevents the error of showing Jesus carrying the cross alone the entire way.

**5. Minor Over-reach (Gethsemane)**
*Phrase:* `watch_one_hour (Matthew 26:36-46): Gethsemane, NIGHT, an olive garden`
*Finding:* The cited text says "a place called Gethsemane." While it was on the Mount of Olives and John mentions a garden, the specific phrase "an olive garden" is a synthesis, not a verbatim KJV fact from the cited verses.

VERDICT: REVISE
TOP FIXES:
1. Scrub the `[SPECIFIED]` bucket of all historical/archaeological inferences (specifically: the physical appearance of the "lots" and the botanical definition of "hyssop"). Move these to `[CONSTRAINED]`.
2. Remove "a bare rise" from the `[SPECIFIED]` Golgotha fact. The Bible calls it a "place of a skull" outside the gate, but never explicitly calls it a hill or rise.
3. Add Simon of Cyrene (Matthew 27:32) to the `[SPECIFIED]` facts for the road to Golgotha, as he is a strictly textual, highly checkable detail for the journey.
