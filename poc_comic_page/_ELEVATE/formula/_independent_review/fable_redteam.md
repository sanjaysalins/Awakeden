# Red team (independent Fable seat, blind) — FORMULA_PLAN.md

## 1. VERDICT: REVISE

Right instinct (prove on a $0 pilot before wiring the engine). But it copies a film nobody has measured, and its main fix may remove what viewers liked.

Checked myself: film is 38.0 s, audio = video, last word ends 34.66 s (hold 3.3 s, OK). Six frames looked at.

## 2. Top flaws (ranked)

1. **Formula from n=1, no numbers.** "Loved" is the owner's report only. Analytics is a footnote ("Also: read...").
   Fix: make it step 0, blocking. Compare this short with its sibling cluster shorts on 3-second hold, retention curve, shares. Only what differs is DNA.
2. **The "DNA" cannot be told apart from the passage.** Luke 23 is short, famous, has 3 speakers and a ready-made someday/today twist. Length, look, hook, or story: which one won? Unknown.
   Fix: list 15-20 passages that truly fit BEFORE building. If fewer than ~10 fit, it is a mini-series, not a formula.
3. **"Word-free master" may delete the loved look and hurts muted viewers.** The pills + speaker tabs are the comic identity, and they carry the film with sound off. Platform captions are often off, and TikTok/Instagram do not take an SRT upload the way YouTube does. Word-free + no captions = a silent film with no words.
   Fix: word-free master as the SOURCE only; always ship a lettered render per language. Decide early: one video + SRT tracks, or one upload per language. Different products.
4. **Wrong fact on placement.** In the frames the pill sits mid-frame (about 52-60% height), across chests and faces, not in the bottom subtitle band. So "keep bottom 25% clear" does not solve the collision the plan names; the real problem is pill over art and two text sets.
   Fix: measure pill box and platform UI safe zones (right rail, bottom caption/handle block) per platform; gate on those.
5. **Word count wrong.** Plan says ~85 words; the locked lines are 73 (about 1.9 words/s over 38 s, with big pauses). A template tuned to 85 will be rushed.
6. **The existing SRT is already broken for translation.** Cues split mid-phrase ("...beside" / "Him.", "...into thy" / "kingdom."), some cues 0.3 s. The plan's own "min 1.2 s" rule fails on its own source.
   Fix: phrase-level cues first, then translate.
7. **Pilot proves nothing.** "Owner compares old vs new" is one opinion, and a re-upload of the same story cannot be A/B read.
   Fix: blind newcomer panel on old vs new, sound-off and sound-on; then the real test is the new story.
8. **Cost line is thin.** Source was $0 because clips came from a parent film. New stories need stills, clips and 3 voices, every time. Quote the true per-episode cost with a range.

## 3. Missing

- Sound: score, SFX, voice casting. Likely part of "feel". Not mentioned.
- The cover/title pair and the title pattern.
- A kill rule: what number says the formula failed.
- Doctrine check per language (both ways, as house rule).
- Who checks a language nobody on the team reads.
- English audio is archaic KJV; non-English viewers hear "thou comest". Subtitles must carry the meaning alone.
- Voice vs subtitle mismatch when a PD Bible words the verse differently in length/order.

## 4. What I would do instead

**"Two Answers" format**, defined by story shape, not by look:
- Pick passages where two people meet Jesus and answer differently (thief/mocker, Pharisee/publican, Mary/Martha, nine/one leper, rich ruler/Zacchaeus).
- Fixed skeleton: question hook (<=3 s) -> two voices in contrast -> Jesus' own words -> one-word flip -> invitation taken from the passage's own verb.
- Three layers, built separately: (1) picture, zero text; (2) doodles, zero text; (3) lettering from a per-language JSON (line, speaker, verse ref, direction, font).
- Ship 3 languages only at first (English, Spanish, Portuguese), each a fully lettered render. Add more when numbers justify.
- Make 3 episodes, then read numbers, then lock. Not lock after one.

## 5. Staleness risk: HIGH

Same hook shape ("X for a Y?"), same flip ("Not X. Y."), same close-face push-ins, same dawn ending = viewers predict it by episode 4.
Prevent: fix the skeleton, rotate the skin. A small menu of 4-5 hook shapes and 4-5 landing shapes; a gate that fails if the last 3 episodes share one. Doodle ledger: no doodle idea reused within 5 episodes. Landing word must come from that passage's own text.

## 6. Language pitfalls not covered

- **RTL (Arabic, Hebrew, Urdu):** pills, speaker tabs, verse chips must mirror; arrows and "left to right" reveals read backwards; needs proper shaping (ffmpeg drawtext breaks Arabic joins).
- **Expansion:** German/Russian/Tamil can run 30-40% longer, not 25%. A 2.2 s hook card and a 0.4 s "Today." cue will not fit. Pills need auto-size + a max-lines gate.
- **CJK/Thai:** no spaces, so line-break by rule; 32 chars is far too many for CJK (about 14-16); needs its own fonts; the comic hand font has no glyphs for most scripts.
- **Burned-in text left over:** hook card, speaker tabs, "LUKE 23:43" chip, any text inside the generated art itself.
- **"23:43" numbers only** drops the book; needs localised book names. Verse numbers differ between traditions (Psalms especially). Some locales use other digits.
- **PD Bibles:** RV1909 and Segond 1910 are archaic too; check PD status per country; many languages have no PD text at all (then no quote, or licence). Text families differ (TR vs critical), so a KJV clause may be missing.
- **The one-word flip may not survive:** "To day"/"someday" echo depends on English. Each language needs the flip re-found from its own Bible wording, by a reader.
- **Luke 23:43 comma** is disputed in some traditions; a translator can change doctrine with punctuation.
- **Dubs:** timing drifts; doodles synced to English words will miss.

## 7. Doodle pitfalls

- A calendar page is modern and culture-bound (and often has text/numerals). Use sun position or shadow length.
- Ink circle on a dying man's face can read as "target". Arrow cross-to-Jesus reads as a diagram, lowers reverence.
- Never doodle over Christ's face or wounds; set a sacred no-draw zone.
- Doodles on top of pills on top of art = clutter. One overlay class per shot.
- Sync to word timestamps per language, not fixed frames.
- Flat vector doodles over inked comic look pasted-on; match line weight and wobble of the art.
- "3-5 per film" is a count, not a reason. Rule should be: a doodle only where it shows something the picture cannot.
