# Independent review — claude (OK, 195s)

# Independent review: TWO DRIVERS ROADMAP (plan)

I worked only from the text you gave me and my own knowledge of the KJV. I opened no repo files. The checker already confirms the 86 quotes match the KJV. My concerns are the claims made around those quotes, the label rules, and the week plan.

## A. Doctrine and fact problems in the 24 angles

1. **T8 says "grandson". That is wrong.** "Why would a king call his own grandson 'my Lord'?" The Messiah is David's distant *descendant*, not his grandson. The riddle in Matthew 22:45 is about a son or descendant. This is a plain fact error in the hook. Fix: "his own descendant" or "his own son, many generations later".

2. **E9 says "three people ask Jesus". Not true.** The three requests in Mark 5:10–18 come from the demons (5:12), the townspeople (5:17) and the man (5:18). Demons are not people. "The man who loves Him" is also not in the text; it is a guess. Fix: "Three requests. Two get a yes. The one who wants to stay with Him gets a no."

3. **T12 gives the wrong time.** "700 years later" is wrong. Isaiah 6 is about 740 BC and John wrote about AD 90, so the gap is about 800 years. T12's label is also wrong. John 12:41 says Isaiah saw *His glory*. That names who Isaiah saw. It is not a *type*. The label table has no slot for "the New Testament names who this was", so add one (for example **IDENTITY**). Otherwise the label spoken in the film is wrong.

4. **The label rules contradict each other.** Row A says "NT says fulfilled → **PROPHECY**". But the ban list says never call a type a prediction. Hosea 11:1 (T2) and Psalm 41:9 (T7) are the classic cases: the New Testament says "fulfilled", yet the Old Testament verse looks back and was not a forecast. T2 is labelled TYPE, which breaks row A. T7 is labelled PROPHECY, which breaks the ban. Fix: split row A in two:
   - **A1 PREDICTION**: the text itself looks forward (Micah 5:2, Psalm 16:10 per Acts 2:30–31).
   - **A2 FULFILLED PATTERN**: the New Testament says "fulfilled" of an Old Testament verse that looks back.

   T2, T7 and possibly T6 go in A2.

5. **E2's take-away goes further than the text, and E2 is a ★ "lowest risk" pick.** "He took your place outside so you could come in" turns Mark 1:45 into a statement about the cross. In Mark, Jesus stays outside because of the crowds and the publicity. Hebrews 13:12 is about His death "without the gate", not this episode. Also, the healed man was sent to the priest (1:44). Mark does not show him going into the city. The plan's own fix ("show both verses, let the viewer see it") still lands on the cross claim. Fix: tone the line down to "He went outside to reach the one who was outside", or move E2 out of the ★ slot.

6. **T9 has two shaky claims.**
   - "Silent all night" is too strong. Jesus answers Annas in John 18:20–23. Matthew 26:63 only says "held his peace" at one point.
   - "The 'coming' part is still ahead, and we say so" takes a side on a debated point. Many sound readers take Daniel 7:13 as the Son *coming to the Ancient of Days* (ascension and enthronement). Both views are orthodox. Saying one out loud invites push-back. Drop the line or leave it open.

7. **E3 mixes up being ritually unclean with being morally ashamed.** Leviticus 15 is about ritual uncleanness, not sin. "Your shame does not stain Him" is fine as a feeling but needs one plain bridge, or a Bible-reader seat will flag it.

8. **Smaller stretches:**
   - E11 "the first meal in the Bible": Genesis 3:6 is the first *eating* told, not a meal. Say "the first eating that went wrong".
   - T3 "the first land to fall into the dark": 1 Kings 15:20 has Naphtali struck earlier. Say "the first carried away to Assyria".
   - T7 "He leaves out 'in whom I trusted'": the omission is real. Any *why* is our reading, so say "notice what is missing", not why.
   - E1 "love comes before work": that moves the Father's delight in the Son onto the viewer with no bridge. It needs an adoption verse, or it is a stretch.

## B. Freshness: the 30–40% fail estimate looks too hopeful

At least nine angles are standard study-Bible cross-references or common sermon points, so they are likely to score under 7:

- **Driver 1:** T1 (Gabriel and 2 Samuel 7), T2 (Jesus re-living Israel's story), T4 (Deuteronomy 18 and the Transfiguration), T6, T11.
- **Driver 2:** E3, E4 (garden and gardener), E5, E6 (the blind man's growing faith).

My guess is that 50–65% fail the FRESH 7.0 bar. That is a guess with wide error bars, the same kind as yours. Plan for that, and pre-run the kill list on these 9 now, at $0, before the order table is trusted.

## C. Are the two drivers clear?

- **The line between them blurs.** Eight of the 12 Driver 2 rows (E1, E2, E3, E4, E5, E7, E11, E12) also rest on an Old Testament to New Testament echo. The real difference is what the headline claims:
  - **Driver 1:** the headline link must be one the New Testament itself states, labelled PREDICTION, FULFILLED PATTERN or TYPE.
  - **Driver 2:** the headline is the event plus a take-away. Any Old Testament link is only a side ECHO.

  Write that down. Without it, E11 and T7 could swap drivers.
- **Q5 clashes with S2.** Q5 says the last spoken beat is about Jesus. S2 says "what Jesus is like or did, *then* what that means for you". The E2, E8 and E12 take-aways end on "you". Decide which rule wins.
- **The freshness bar is set in three places and they don't match:**
  - Q4 makes FRESH ≥ 7.0 a hard test.
  - Section 2c allows 6.0–6.9 in 1 of every 4 films.
  - Section 9 adds a FILM FRESH bar of 6.5.

  Make one rule.

## D. The daily rhythm is not realistic

- **Tuesday is overloaded.** It runs the full words-before-money pipeline for two films in one day: 4–5 blind writers, a judge table, combining, the global-audience test with its fix and re-test loop, and the guardrail panel. The 5-CLI `independent_review.py` panel required at every LOCK isn't in the week at all. One film's words is a day or more. Words for 2 films need Mon–Wed.
- **The order of steps is wrong.** Thursday has the voice ear-check and the clips page on the same day. The pipeline needs the voice approved *before* stills (clip timing comes from line timing), and stills approved before clips.
- **Missing steps:**
  - the "enhance before upload" pass,
  - packaging that uses real search autocomplete,
  - the blind panel on the finished film,
  - OpenArt bridge servicing, which needs a live session and cannot run unattended.
- **Seat budget.** 12 seats every day for hunt and judges, plus writer and guardrail panels, on CLI subscriptions risks hitting rate limits. The plan doesn't count seats.
- **Cost.** The $8–14 figure predates two rules: hero images always get a real animated clip, and every clip must be at least as long as its slot. Both push cost up. The pilot in section 9 is the right fix. Make it a hard gate before the 24-episode order table means anything.

VERDICT: REVISE
TOP FIXES:
1. Fix the factual and label errors: T8 "grandson" → descendant; E9 "three people" → three requests (one from demons); T12 "700 years" → ~800 and add a new IDENTITY label instead of TYPE; T9 drop "silent all night" and the claim that the "coming" is still ahead.
2. Split label A into PREDICTION and FULFILLED PATTERN so Hosea 11:1 and Psalm 41:9 are never said out loud as "prophecy". Tone down E2's take-away ("took your place") or drop it from the ★ first-3. Settle Q5 vs S2 (last beat about Him or about you) and use one freshness bar instead of three (Q4, 2c, section 9).
3. Rebuild the week after the pilot: words for 2 films spread over Mon–Wed, voice approved before stills before clips, and the LOCK panel, enhance pass and finished-film panel added. Pre-run the kill list now on the 9 likely-classic angles (T1, T2, T4, T6, T11, E3, E4, E5, E6) and expect a 50–65% fail rate.
