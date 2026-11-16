# Independent review — claude (OK, 270s)

I checked the owner page against the two reports, the panel files, the Bible verses and two video frames. I confirmed the rope (Today in Paradise, 0:06) and the hammer with fresh blood (Forsaken Cry, 0:28). The page has real errors, mainly in the Bible wording, one count, the cost of Step 1 and "My pick".

## Bible text errors on insights the page marks USE

1. **Little Girl, Get Up: "Jesus only spoke" is false.** Mark 5:41 says "he took the damsel by the hand, and said unto her, Talitha cumi". The film itself shows Him taking her hand (swirls_report.md:89). Peter also copied the hand (Acts 9:41) and sending everyone out (Mark 5:40 / Acts 9:40). The real difference is that Peter "kneeled down, and prayed" and Jesus did not. Fix: "Peter had to kneel and pray first. Jesus took her hand and spoke."

2. **The Bier He Touched: "Jesus just said Arise" leaves out the touch, which is the film's own title.** Luke 7:14 says "he came and touched the bier". "Elijah begged God 3 times" is the mix-up the Claude seat flagged ("split 'stretched three times' from 'cried'", claude.md:118). 1 Kings 17:21 says he stretched himself on the child three times and cried to the LORD.
   - The page quotes "delivered him to his mother" for both books. 1 Kings 17:23 actually says "delivered him **unto** his mother".
   - So a plain "USE" sits on wording the panel corrected.
   - Fix: "Elijah stretched himself on the boy three times and cried to the LORD. Jesus touched the bier and spoke." Quote each verse exactly as it reads.

3. **Forsaken Cry: the link that makes it Bible-based is gone.** The page has only "Psalm starts 'My God, my God'… Jesus said 'my God, and your God'". As written, that is a coincidence of words. The link the panel approved runs through Ps 22:22 "my brethren", Heb 2:12 and "go to my brethren" in John 20:17 (INSIGHTS_PANEL #5). Fix: add "the same psalm goes on: 'I will declare thy name unto my brethren'". Cite Heb 2:12.

4. **Sign of Jonah: the page rests on the very things the panel warned against.**
   - The cited verse, 2 Kings 14:25, says "Gath-hepher". It does not say Galilee. Claude asked for Joshua 19:13 (spelled "Gittah-hepher" there) and Isa 9:1 for "Galilee".
   - Claude said: "do not suggest Jesus answered John 7:52". The page line "They said no prophet comes from Galilee. Jonah did." does that.
   - Cursor flagged that this joins John 7 and Matthew 12, which the text never links.
   - Fix: cite Joshua 19:13 and Isa 9:1. Say it is our observation, not Jesus' reply.

## Labels that don't match the panel

5. **"USE" looks like a sign-off, but the panel was degraded.**
   - INDEX.md says: "healthy voices: 3/5 (quorum 4) — DEGRADED PANEL — do not lock on this run".
   - All 3 working seats voted REVISE. None voted PASS.
   - There was **no Fable seat**, which breaks the house rule that independent panels always include Fable.
   - "treat this as a first pass" is too soft for that. Fix: retitle as "Looks promising, not cleared yet". Re-run with Fable plus a full quorum before anything is marked USE.

6. **"Two Fable reviewers" is not supported.** BRIEF.md and both reports never name the model. Swirls even calls itself "one model's ideas" (swirls_report.md:479). Fix: say "two reviewers", or check the dispatch log first.

7. **"Drop" for It Is Finished throws away a fix the panel offered.** Claude said "near REJECT *as written*" and suggested swapping Gen 2:1 for 1 Kings 7:51 → 8:10-11, with Heb 10:20 for the veil (claude.md:67-68). Into Thy Hands is a plain wording error, not an over-reach: Luke 2:49 begins "How is it…". Claude gave safe wording ("about his Father… to his Father"). Fix: label both "Rework", with the fixed wording.

## Wrong numbers

8. **"6 of the Swirls films use freeze/boomerang fill" is wrong.** The report says "all seven page films" (swirls_report.md:457). The repo agrees:
   - Freeze/boomerang matches in episode.py: ep02 = 6, ep07 = 8, ep08 = 8, ep10 = 11, ep11 = 12, ep13 = 11.
   - Jacob's Ladder also uses freeze + boomerang (swirls_report.md:13). That makes 7.
   - Only ep06 (Talitha Cumi) has none.
   - "~$25" hides the report's range of $2.50–5 per film, which is about $17–35.
   - Fix: "7 of 8. About $17–35. Needs a real quote."

9. **The freshness list leaves one out.** "6 of the 9… It Is Finished and Empty Tomb are fairly fresh" names only 2 of the 3 left. Into Thy Hands is about 40% (comic_report.md:297), fresher than Empty Tomb at 50%. Fix: name all three.

## "My pick" problems

10. **Step 1 "($0): fix the mistakes" is not $0.**
    - Samaritan's new face (ep11 F10): new still + re-animation.
    - Nineveh pyramid: the report itself prices this at "$1-1.50" (comic_report.md:339).
    - "Same nails" over roped thieves: either new stills + new clips, or new words. New words need the words gate plus a re-voice.
    - Saw: paint-out + re-animation. Fixing a still does not fix the shipped mp4.
    - Calling this $0 sets up a spend without a quote. Fix: split into "$0 now" (clip swaps, grids, doodles, hammer crop) and "needs a quote" (face, Nineveh, nails, saw).

11. **"Hold these 17" quietly reverses the owner's call from today.** Today the owner lifted the hold ("if they are ready, start posting"), and the upload tracker lists these in Next up.
    - The page gives no reason to hold films the reports call already fine or fresh: ep13 "already fresh… would not change the spine", ep06 "most alive", Women Witnesses "only film with real panel variety".
    - Fix: say plainly it reverses the owner's call. Pick per film: post the clean ones, hold only the ones with defects.

12. **Step 2 skips required gates and its cost.**
    - New landing lines on a finished film mean a re-voice, re-timing and a re-cut.
    - They also need the 5 guardrail questions and the global-audience test, not just "the words gate".
    - Both picked insights (Bier, Forsaken Cry) still carry the text errors in points 2 and 3.
    - Fix: correct the wording first. List the gates by name.

13. **Numbers 19:11 is listed under "mistakes" but the page also says it was on purpose.** The repo confirms it was deliberate (episode.py:12, _DESIGN_BRIEF.md:994). That makes it a choice for the owner, not a mistake. Fix: move it to an "Your call" line.

## Wording a dyslexic reader may stumble on

- "Contrast only; call them prisoners"
- "lifts 8 of 9"
- "the words gate"

These need the reader to already know the jargon. Fix: one plain sentence each.

VERDICT: REVISE
TOP FIXES:
1. Fix the Bible wording on the USE items. Little Girl: Jesus took her hand. Bier: He touched the bier; Elijah stretched three times and cried; quote 1 Kings 17:23 as "unto". Forsaken Cry: add Ps 22:22 / Heb 2:12. Then mark every insight "not cleared yet". The panel was 3/5, all REVISE, no Fable seat; re-run with Fable and a full quorum.
2. Rewrite "My pick". Step 1 is not $0 (face, Nineveh, nails and saw need new stills, clips or voice), so split it into "$0 now" and "needs a quote". Don't blanket-hold all 17 against the owner's call from today; pick per film and post the clean ones.
3. Correct the numbers and labels. Swirls fill is 7 of 8 at about $17–35. Into Thy Hands is the third fresher comic. Relabel It Is Finished and Into Thy Hands "Rework", with the panel's fixes. Move Numbers 19:11 to "your call". Drop or check "Two Fable reviewers".
