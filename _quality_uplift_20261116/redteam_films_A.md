# Red team A: films 1-4 (ep08, ep13, Jacob's Ladder, ep07) - 2026-11-16

Reviewer: independent, adversarial. Judged only from the old and new mp4s, the narration (JL: `LOCKED_WORDS_JL_2026-11-02.md`) and `SWIRLS_UPLIFT_SPEC.md`. No builder report, gate report or review page was read. Verdicts are advisory; the owner decides.

Frames: `C:\Users\sanjay\AppData\Local\Temp\redteam_A\` (called `%T%` below). New films sampled at 1 frame/second over the whole film, plus zooms. Old films sampled every 2 s.

## How far to trust this
- Seen with eyes: every second of all 4 new films (contact sheets), plus full-size zooms on suspects.
- NOT judged: playback feel, sound sync, sub-second glitches between samples. Freeze / slow-motion / landing hold are being measured by the coordinator; I only ran one coarse `freezedetect` (n=0.0015, d=0.5 s) which found nothing in any of the 4 new films.
- Old films: ep08, ep13 and ep07 old sheets were looked at; Jacob's Ladder old was judged from its cut list only (first cut at 10.0 s, 7 cuts), not from frames.
- "Pre-existing" = the same defect is in a clip that was already in the shipped film. I confirmed that by frame only for ep08 F02 and ep13 F05; the other "pre-existing" labels are inferred from the spec's EX (existing clip) list.
- Costs are rough, from the spec's rates ($0.063 per clip second, $0.08 per still), first take.

## Checks that passed on all 4
- Audio unchanged: audio stream md5 is identical old vs new (ep08 `2db1f1d3...`, ep13 `2de0f019...`, JL `1fdac746...`, ep07 `666bd070...`). Durations identical.
- No burned-in captions added. Storyboard-page look kept.
- Pencil marks: sparse, word-tied, none on Jesus' face, none covering a face or baked caption in any frame I saw. No mark adds words.
- Cuts roughly doubled (ep08 7 -> 13, ep13 10 -> 17, JL 7 -> 9), all hard cuts in the frames seen.

## Systemic finding (all 4 films): the blue/gold motif moves
Rule: "the motif must NEVER be animated". It moves in many clips, old and new. Worst cases:
- ep07 F06 (50.6-56.5 s): big blue ribbon takes a new shape every second. `%T%\ep07\sheets\new_06.jpg` (existing clip)
- ep13 back cover (96.5-106 s): blue/gold ribbon whips about. `%T%\ep13\sheets\d_05.jpg` (existing clip)
- JL F06 (32.3-37.3 s): sky ribbon goes curl -> wave -> streak. `%T%\jl\sheets\new_04.jpg` (existing clip)
- New clips also do it: ep07 F03A thread goes wavy -> ruler-straight and pokes above the panel (`%T%\ep07\z_f03a.jpg`); ep07 F04 cloud wisps reshape (`%T%\ep07\z_f04.jpg`); ep08 F05B thread wiggles (`%T%\ep08\z_f05b_balloon.jpg`); ep13 F05 doorway wisp grows into a big S (`%T%\ep13\sheets\d_02.jpg`).
The uplift did not fix this and added a few more. Owner call: accept as the series' look, or re-animate the worst ones (paid).

---

## 1. ep08 Can Any Good Thing
**VERDICT: NEEDS PAID FIX (one page, about $0.40-0.60). Otherwise lock.**
**Better than old? Yes.** Pages now arrive with their words (old cover sat until 7.5 s), the fig-tree "eye" doodle makes "I saw thee" clear, and the empty-mat page lands the ending.

Defects, worst first:
1. **39.7-44.7 s, new page F05B. Jesus looks like he is holding a balloon on a string.** A round blue/gold blot sits above his raised hand, joined by a thin thread. Also Nathanael is a different man here: brown wavy hair, red vest over cream (everywhere else: black curls, yellow robe, orange stole). Rules: reverent / same face and clothes. Fix: redraw the still without the blot-on-a-thread and with the right Nathanael, re-animate 5 s (paid, ~$0.40). CONFIRMED `%T%\ep08\z_f05b_balloon.jpg`, `%T%\ep08\sheets\d_01.jpg`
2. **~46-48 s, F06. An angel appears at ground level, bottom-left, reaching toward Jesus, then hovers beside him;** the angel in top panel 2 climbs out of its panel. Rule: no invented content / objects appearing. Existing clip (inferred pre-existing). Fix: re-animate F06, 8 s (paid, ~$0.50) or accept. CONFIRMED `%T%\ep08\sheets\d_02.jpg`
3. **16-19 s, F03 (new re-animation). The feet in top panel 2 "still he came" walk out of the panel,** leaving a dust cloud. Rule: people walking out of panels. Small on screen. Fix: accept, or re-animate (paid, ~$0.50). CONFIRMED `%T%\ep08\sheets\new_02.jpg`
4. **52-56 s, borrowed Jacob's Ladder page.** Header reads "SEQ: THE LADDER"; legs appear in the "first rung" panel and a cloud grows in panel 3. Works as a callback to "That is Jacob's ladder"; the header is a small oddity. Owner call. CONFIRMED `%T%\ep08\sheets\d_02.jpg`, `%T%\ep08\sheets\d_03.jpg`
5. **7.2-12.2 s, F02.** Baked label reads "(2) the open" (word "hand" missing) and the caption "any good thing" is jammed at the bottom-left page edge. Same in the old film, so not a regression. CONFIRMED `%T%\ep08\z_f02_new9_old16_old18.jpg`
6. **19.3-21.2 s, F03B and 30.3-32.7 s, F05A.** New pages are framed a little differently (F03B label sits above the SEQ line, filled black number dots; F05A shows the paper edge). Minor style drift. CONFIRMED `%T%\ep08\sheets\new_02.jpg`, `%T%\ep08\sheets\d_01.jpg`

---

## 2. ep13 The Cross That Wasn't His
**VERDICT: NEEDS PAID FIX (4 new shots, about $1.40-2.00).**
**Better than old? Yes, but with new errors.** The opening is now a real walking clip, and the new close shots (seized arm, bystanders pointing) break up the sameness. Four of the seven new shots have a visible fault.

Defects, worst first:
1. **~92 s, new page F09B "Only the shame". The offered hand deforms** - fingers curl into a clawed, mis-jointed shape mid-clip, then half recover. This is the call-to-action picture. Rule: no extra/deformed limbs. Fix: re-animate 7 s with a hand that only opens slightly (paid, ~$0.45). CONFIRMED `%T%\ep13\z_f09b_hand.jpg`
2. **64.2-67 s, new page F06B. The city gate is a pointed Gothic arch with crenellated battlements** - reads medieval, not 1st-century Jerusalem. Simon is also in a red robe here. Rule: era. Fix: redraw still + 3 s clip (paid, ~$0.27). CONFIRMED `%T%\ep13\sheets\d_03.jpg`
3. **50.2-54.3 s, new page F05B (the Old Testament page). The sin offering is shown as a bull standing/walking on its own legs under the carrying pole,** not a body being carried out to be burned. Words: "Its body went out, burned without the camp." Rule: picture must not contradict the text; newcomer clarity. Fix: redraw still + 5 s (paid, ~$0.40). CONFIRMED `%T%\ep13\sheets\d_03.jpg`
4. **~36 s, new page F03B. A large white dust cloud bursts at the sandal and spills outside the panel border onto the page margin.** Rule: no invented content; breaks the page. Fix: re-animate 4 s (paid, ~$0.25). CONFIRMED `%T%\ep13\sheets\d_02.jpg`
5. **42-45 s, F05. The baked caption appears twice** ("without the camp   without the camp"), then one copy fades. Same in the old film - not a regression. CONFIRMED `%T%\ep13\z_f05_caption_new43_old44_old50.jpg`
6. **Whole film. Simon's clothes change page to page** (white tunic / green shawl / brown robe / red robe), and the cross reads as an X on F02, F04, F06B. Mostly pre-existing; the new pages did not help. CONFIRMED `%T%\ep13\sheets\d_01.jpg`, `%T%\ep13\sheets\d_02.jpg`
7. **48 s and 52 s, camp-plan doodle** (small square + arrow). Clean, but cryptic for a newcomer. SUSPECTED weak, not a rule break. `%T%\ep13\sheets\d_03.jpg`
8. The spec's red circle on the baked word "without" (~40.9 s) was not seen in my samples. SUSPECTED missing or just between samples.

---

## 3. Jacob's Ladder
**VERDICT: NEEDS PAID FIX (about $0.50-1.00). Clearly the biggest gain of the four.**
**Better than old? Yes.** Old film held the cover for 10 s and never showed Jesus. New film has the flight page, 13 s of Jesus on screen, and a back cover whose title is the spoken last line.

Defects, worst first:
1. **43.6-50.2 s, borrowed ep08 page.** (a) Header reads "SEQ: CAN ANY GOOD THING" and a panel is labelled "your fig tree" - a different film's words, on screen for 6.6 s in a Jacob film. (b) At ~46 s an angel appears at ground level beside Jesus, reaching toward him. Rules: no invented content; newcomer clarity. Fix: the spec's paid option - a new JL F08 page with the ladder above Jesus (1 still + 7 s, ~$0.52). CONFIRMED `%T%\jl\z_borrow.jpg`, `%T%\jl\sheets\new_05.jpg`
2. **37.3-43.6 s, new page F07 (Jesus and a second man under a tree). By ~43 s both men's coats blow wide open as if in a sudden gust, and Jesus' mouth opens in a grin.** Reads slightly comic. The blue thread above his hand also drifts. Rules: reverent; motif still. Fix: re-animate 7 s with hems barely moving (paid, ~$0.44), or accept. CONFIRMED `%T%\jl\z_f07.jpg`
3. **Same page: the second man (Nathanael) is never named in these words.** A newcomer cannot tell who he is. Rule: who/what/why. Free option: none in picture; owner call.
4. **12.4-20.6 s, F03 (new re-animation). Angels walk up and down a lot;** their number changes (about 4 -> 6) and one drifts off the ladder into the air. Fits "ascending and descending", but figures appear. Rule: no invented content (mild). Accept or re-animate (~$0.57). CONFIRMED `%T%\jl\sheets\new_02.jpg`
5. **~23.9 s, underline on the baked caption "I am with thee".** The voice says "I will not leave thee" - the mark points at words that are not spoken. Rule: marks tied to the spoken word. Free fix: drop this mark. CONFIRMED `%T%\jl\sheets\new_03.jpg`
6. **50.2-56.5 s, new back cover.** Accurate (the pillar stone, Genesis 28:18) and the title is the spoken line. To the eye it looks almost still across 7 sampled frames. SUSPECTED low motion - coordinator's measurement decides. `%T%\jl\sheets\new_06.jpg`
7. **30-37 s, F05 and F06.** Motif swirls and the sky ribbon reshape every second (existing clips). See systemic note. CONFIRMED `%T%\jl\sheets\new_04.jpg`

---

## 4. ep07 The Bier He Touched
**VERDICT: NEEDS PAID FIX (2 new pages, about $0.90-1.00).**
**Better than old? Yes.** The old "touch" and "Arise" pages were slow zooms on a still (`%T%\ep07\sheets\old_02.jpg`); both are now real clips, the hand landing on the pole is a strong hero shot, and the reversed-arrow doodle explains the idea.

Defects, worst first:
1. **34-40.2 s, new page F03B "it didn't work that way". The bier is empty except for a wrapped, head-shaped bundle at one end.** It reads as a body missing or a wrapped head alone. The body is on the bier in the shots before and after. Also the sleeve grows and a tassel/second figure appears at the left edge by 40 s; the blue line slides across His hand. Rules: no contradiction, reverent, no objects appearing. Fix: redraw still (tight on hand + boards, no bundle) + 7 s (paid, ~$0.52). CONFIRMED `%T%\ep07\z_f03b.jpg`
2. **13-17 s, new page F01B "kept their distance". The bier stands on the ground on legs with no bearers,** and the widow is in a pitch-black robe (grey/brown in every other shot). In the shots either side the bier is carried on shoulders. Crowd figures also drift and one walks in. Rules: continuity, same clothes. Fix: redraw still + 5 s (paid, ~$0.40). CONFIRMED `%T%\ep07\z_f01b.jpg`
3. **25.5-30 s, new hero page F03A. Good shot, two faults:** the blue thread straightens into a ruler line and pokes above the panel border, and a dust puff appears bottom-left at ~29.7 s. Rules: motif still, no invented content. Fix: accept, or re-animate 5 s (paid, ~$0.32). CONFIRMED `%T%\ep07\z_f03a.jpg`
4. **40.2-44.6 s, hero page F04 "Arise" (new re-animation).** Real motion now, reverent. The blue cloud wisps reshape. Rule: motif still. CONFIRMED `%T%\ep07\z_f04.jpg`
5. **19.7-25.5 s, F02.** The feet in top panel 2 vanish, leaving an empty road. Existing clip. CONFIRMED `%T%\ep07\sheets\new_03.jpg`
6. **56.5-61.3 s, new page F06B.** Jesus full-face, hand out. Reverent. His face is more realistic/longer than on the other pages. Mild consistency note. `%T%\ep07\sheets\new_06.jpg`
7. **50.6-56.5 s, F06.** The mother has a blue veil and a younger face here (existing page). Pre-existing.
8. **66-72 s, back cover.** Looks almost still to the eye. SUSPECTED low motion - coordinator's measurement decides. "NUMBERS 19:11" is still unexplained for a newcomer (owner call, per spec). `%T%\ep07\sheets\new_07.jpg`
9. 17-19.7 s, F02A arrow doodle: checked, it passes beside the baked caption, not over it. No defect. `%T%\ep07\z_f02a_arrow.jpg`

---

## Top 5 across these four films
1. **ep13 ~92 s - the offered hand deforms** on the call-to-action page. Paid, ~$0.45. `%T%\ep13\z_f09b_hand.jpg`
2. **ep07 34-40 s - empty bier with a lone wrapped head-shaped bundle.** Paid, ~$0.52. `%T%\ep07\z_f03b.jpg`
3. **ep08 39.7-44.7 s - Jesus "holding a balloon", and the wrong Nathanael.** Paid, ~$0.40. `%T%\ep08\z_f05b_balloon.jpg`
4. **JL 43.6-50.2 s - another film's page (wrong header) with an angel popping in beside Jesus.** Paid, ~$0.52. `%T%\jl\z_borrow.jpg`
5. **The blue/gold motif moves in all four films,** in old clips and in several new ones. Owner call: accept as the look, or pay to re-animate the worst (ep07 F06, ep13 back cover, JL F06).

Next in line: ep13 Gothic gate (F06B), ep13 live bull on the Old Testament page (F05B), ep07 bier on the ground with a black-robed widow (F01B).

Rough total to clear every "paid" item above except the motif question: about $4-5 first take.
