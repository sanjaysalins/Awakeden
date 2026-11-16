# Graphic comic (9) - quality uplift + fresh insight report

Date: 2026-11-16. Read-only pass. Nothing was generated. Nothing was spent.

## How I looked

- Pulled 1 frame every 2 s from each final film (about 30-40 frames each) and looked at every one.
- Measured motion every 2 s (pixel change between frames) to find the still, flat parts.
- Read each `narration.md` and one `livingpage_short.spec.json`.
- Pulled every Bible quote below from the repo's own KJV (`F:\slk\PycharmProjects\JesusInTheBible\data\kjv_full\`), so the quotes are exact.
- Frames are in `C:\Users\sanjay\AppData\Local\Temp\qu_comic\` (scratch).

Limits, said plainly:
- Times are good to about 1 second (2 s sampling).
- I saw frames, not playback, and I did not hear the sound. Motion numbers tell "moving or flat", not "good or cheap looking".
- The fresh insights are model ideas. Each one still needs the AI panel and the doctrine check before use.
- "Odds" are my estimates for a typical churchgoer, about plus or minus 15 points.

## 4 things true for the whole group (read these first)

**1. The 3-panel grids are one clip, cut three ways.**
The spec uses `hero_band3` / `hero_frac3` with ONE clip. So David is on screen 3 times, the father 3 times, the child 3 times, the tomb 3 times. It looks like a comic page, but it is one picture repeated. This breaks the spirit of the panel-variety rule (2+ panels with the same subject). It is the biggest "seen it" feeling in the group.

**2. The six cross shorts share the same pictures.**
Same clips show up again and again:
- risen Christ reaching hand: in 5 of 6
- two people kneeling at the cross shadow: in 5 of 6
- three crosses, tall 3-band: in 5 of 6
- nail in the hand: in 4 of 6
- cross at dawn as the last shot: in 4 of 6
- David writing / scroll and lamp: in 3 of 6
Posted as a series, a viewer sees the same 6 pictures every time. This feeds the owner's own complaint: "does this not look like a lot we have already done".

**3. Endings go flat.** Forsaken Cry, I Thirst, It Is Finished and Into Thy Hands all end on the same cross-at-dawn shot, and it is the stillest part of each film (motion about 2 on a scale where a lively shot is 15+).

**4. There are no doodles yet.** All on-screen text is typed pills and yellow "X = Y" cards. No hand-drawn circle, arrow, margin note, map or measured line anywhere. Adding even 2-3 per film changes the feel a lot, for $0.

Cost note for new shots (not spent): about $1 to $1.50 per new shot (one still plus one real clip; Seedance for calm, Kling for action). Always re-check against the real invoice.

---

## 1. The Forsaken Cry (Psalm 22:1) - 58 s

Film: [forsaken_cry_ps221_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/forsaken_cry_ps221/visual/forsaken_cry_ps221_sfx_v5hook.mp4)

**What I saw.** Opens on the temple veil (strong, but the veil is never spoken of). David x3 grid. Three crosses held about 6 s. Scroll and lamp. Moon over Golgotha. The cry from a low angle. Then 8 s on the risen, glowing Christ while the voice says "bearing the forsaking our sin deserved".

**Weakest 10 s: 0:40-0:50.** The words are about being forsaken in the dark. The picture is a warm, risen, smiling Christ. Picture and words pull apart at the heart of the film.
Second flat spot: 0:06-0:10 (David x3) and 0:18-0:22 (scroll, motion about 3).

**Single biggest win.** Show the two cries as one. At 0:28-0:34 ("The very same words") put David's line and Jesus' line side by side, word for word, and let the words lock together.

**Plan**
- 0:18-0:22 "My God, my God..." (David). `keeper-hand`: the line is written by hand on the scroll as it is spoken. Why: we watch the words get made 1,000 years early.
- 0:28-0:32 the cry. `typography-panel` or Remotion (`_remotion/src/comic_kit`): the same hand-written line from 0:18 slides in and lands on top of the red quote. Why: "the very same words" becomes something you see.
- 0:32 "The very same words". `annotators-circle` on the two matching words "my God". Why: sets up the "still calls God my God" line 4 s later.
- 0:22-0:26 "a thousand years later". `measuring-reed` style time line: David ---- 1,000 years ---- the cross. One hand-ruled line. Why: makes the gap felt. (Use as a time line only. The skill's own rule is for real Bible lengths, so build this in Remotion with the same look.)
- 0:40-0:48 swap the risen-hand clip for the dark. Reuse `darkness_veil_torn` or `ninth_hour_darkness` (already paid for), then let light come in only on "so that you never will be" (0:48). `candle-only` can do the light closing and opening for $0.
- 0:06-0:10 David grid: replace 2 of the 3 crops with different existing clips (scroll close, lamp). $0.
- Check: at 0:28 a hammer and fresh blood show at the bottom of the frame. At the ninth hour the nailing was long over. Trim or crop that frame.

**Task B - how familiar?** About 85% have heard "He quoted Psalm 22, He was forsaken so we never are". Solid, but well worn.

**Fresh insight 1 (strongest). "My God" became ours.**
- Psalm 22:1: "My God, my God, why hast thou forsaken me?"
- Same psalm, 22:22: "I will declare thy name unto my brethren: in the midst of the congregation will I praise thee."
- Hebrews 2:11-12 says this is Jesus speaking: "he is not ashamed to call them brethren, Saying, I will declare thy name unto my brethren".
- John 20:17, the first morning: "go to my brethren, and say unto them, I ascend unto my Father, and your Father; and to my God, and your God."
- The point: the psalm that starts with "My God" alone in the dark turns, in verse 22, to "my brethren". On Easter morning Jesus uses both words in one breath. He cried "my God" alone so He could say "your God" to us.
- Why missed: people stop at verse 1. Few link Ps 22:22 to John 20:17.
- Odds heard: about 8%.
- Risk: low. Hebrews itself puts Ps 22:22 in Jesus' mouth. It does not need the disputed "He meant the whole psalm" claim, which this piece's panel already told us to avoid. Say "the same psalm goes on to say", not "He was hinting at".
- Size: small to medium. Replace the landing lines (about 2 sentences).

**Fresh insight 2. The one prayer with no "Father".**
- Luke 23:34: "Father, forgive them; for they know not what they do."
- Matthew 27:46: "My God, my God, why hast thou forsaken me?"
- Luke 23:46: "Father, into thy hands I commend my spirit"
- First word from the cross: Father. Last word: Father. In the dark middle: "My God". Then "Father" comes back.
- Odds heard: about 25%. Risk: low to medium. Must not say the Trinity broke or the Father stopped loving the Son. The current script already guards this well. Size: one added line.

**Fresh insight 3. The next verse has day and night in it.**
- Psalm 22:2: "O my God, I cry in the day time, but thou hearest not; and in the night season, and am not silent."
- Matthew 27:45: "Now from the sixth hour there was darkness over all the land unto the ninth hour."
- The cross had a day and a night inside one afternoon. The cry comes as that dark ends.
- Odds heard: about 10%. Risk: medium. It is a picture, not a stated prophecy. Say "look at the very next line", do not say "this predicted". Size: one line.

---

## 2. I Thirst (Psalm 22:15 / John 19:28) - 56 s

Film: [i_thirst_john1928_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/i_thirst_john1928/visual/i_thirst_john1928_sfx_v5hook.mp4)

**What I saw.** Great opening: the sea, then "I thirst". David x3 again. Broken pot on cracked ground with two decode cards (potsherd, cleaveth). Scroll. Low angle on the cross. The sponge on the hyssop reed (strong shot). Gethsemane x3. Waterfall. Risen hand. Cross at dawn.

**Weakest 10 s: 0:36-0:46.** "The Psalm does not foretell that cry, it paints the thirst behind it." This is the key idea, and the picture is Jesus praying in the garden, three crops, almost still (motion 4-5). The garden has nothing to do with the line.
Second flat spot: 0:22-0:26 (scroll, motion 3).

**Single biggest win.** One dry-to-wet turn. Let the cracked clay from 0:16 come back at 0:44 and have water run into the cracks as "living water" is said.

**Plan**
- 0:16-0:22 the potsherd verse. `focal-tour`: a soft light visits the pot, then the cracks, then the dust, in the order the verse names them. Replaces two stacked decode cards that fight the quote box.
- 0:16-0:20 `annotators-circle` on "potsherd" in the quote, then one hand note "a bit of broken pot" with `marginalia`. Why: a hand note is warmer than the yellow "=" card, and the meaning is still spoken.
- 0:32-0:36 "I thirst." Hold the hyssop shot in silence. The spec already stops the heartbeat here. Add nothing. Stillness is right here.
- 0:36-0:44 replace the garden grid. Best: split screen, Psalm line on the left in David's hand, the cross on the right (`infographic-panel` diptych, both stills already exist). Why: "paints the thirst behind it" becomes one picture.
- 0:44-0:50 "living water hung there dry". `ink-transition` (ink-bleed wipe) from the cracked clay to the stream. Why: dry to wet is the whole film in one move.
- 0:50-0:54 end: do not go back to the shared risen-hand shot. Stay on water. If budget allows, 1 new clip: cupped hands lifting water (about $1-1.50, calm, Seedance).
- Era check: fine. Nothing odd seen.

**Task B - how familiar?** About 70% have heard "the giver of living water was thirsty". The Psalm 22:15 link is a little fresher (about 40%).

**Fresh insight 1 (strongest). John shows Jesus thirsty twice. Both at the sixth hour.**
- John 4:6-7: "Jesus therefore, being wearied with his journey, sat thus on the well: and it was about the sixth hour. There cometh a woman of Samaria to draw water: Jesus saith unto her, Give me to drink."
- John 4:28: "The woman then left her waterpot"
- John 19:14: "And it was the preparation of the passover, and about the sixth hour"
- John 19:28: "saith, I thirst."
- The point: at the well He asks for water at the sixth hour and John never tells us He got any. She gets living water instead and leaves her pot. At the cross, the sixth hour comes again, and He says it out loud. He went thirsty at both ends so others could drink.
- Odds heard: about 12%.
- Risk: low to medium. "He never got the drink" is silence in the text, so say "John never says He drank". Sixth hour in John 19:14 is the trial, not the moment of the cry, so say "the same hour of the day", not "the same minute".
- Size: medium. Swaps the "made every ocean" hook for a well-to-cross frame. Could also be a new sister short.

**Fresh insight 2. The hyssop.**
- John 19:29: "they filled a spunge with vinegar, and put it upon hyssop, and put it to his mouth."
- Exodus 12:22: "And ye shall take a bunch of hyssop, and dip it in the blood that is in the bason, and strike the lintel and the two side posts with the blood"
- Psalm 51:7: "Purge me with hyssop, and I shall be clean"
- Only John names the plant. It is the Passover plant. On Passover day it is lifted to the Lamb.
- Odds heard: about 30%. Risk: low, widely held. Size: small. The hyssop reed is already drawn in the film. One line of narration adds it.

**Fresh insight 3. The other man who begged for a wet tongue.**
- Luke 16:24: "send Lazarus, that he may dip the tip of his finger in water, and cool my tongue; for I am tormented in this flame."
- Psalm 22:15: "my tongue cleaveth to my jaws"
- Jesus told that story. Then He took that thirst.
- Odds heard: about 20%. Risk: medium. It is a step of reasoning (He bore judgment's thirst), not a stated link. Needs the doctrine check and gentle wording, no fear framing. Size: one or two lines.

---

## 3. Today in Paradise (Luke 23:43) - 59 s

Film: [today_paradise_luke2343_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/today_paradise_luke2343/visual/today_paradise_luke2343_sfx_v5hook.mp4)

**What I saw.** Best character work in the cross set. Two clear thieves (angry dark-haired mocker, old bald thief with a tear). Strong faces. Good paradise garden at the end.

**Weakest 10 s: 0:24-0:34.** The thief's confession and "A confession. A verdict: innocent." Motion drops to 1-2 at 0:28-0:32, the lowest in the whole group. The picture is the mocker screaming again while the words are about the OTHER thief's confession.

**Single biggest win.** Make the two men a true side-by-side. Same frame, left and right, all the way through the two quotes. One taunts, one asks.

**Plan**
- 0:04-0:10 "Same nails. Same hill. Same distance." `grid-choreography`: rack attention left thief, right thief, then the gap between. Three beats, three moves. Why: the three "same" words each get a look.
- Fix: the voice says "Same nails" but both thieves are drawn tied with ROPE. Either change the word (the Bible does not say how they were fixed) or paint nails in. A sharp viewer will catch it.
- 0:16-0:20 the taunt. `impact-burst` (small, one hit) on "save thyself and us". Why: a taunt is a blow.
- 0:24-0:32 the confession. Use `penitent_thief_face` and `thief_looks_to_jesus` (already rendered) in place of the mocker. Then `annotators-circle` on "nothing amiss". Why: his verdict is the turn of the film.
- 0:28-0:32 "A verdict: innocent." Remotion stamp, hand-drawn, one word: INNOCENT, over Jesus. Spoken too, so dubbing is safe.
- 0:38-0:44 "To day". `annotators-circle` on "To day" in the red quote at the exact word. Why: the whole film hangs on that word.
- 0:46-0:48 "He asked for someday. Jesus gave him that same afternoon." Two-word doodle: "someday" struck through by hand, "today" written under (`keeper-hand` word-strike). Why: the correction is the joke and the grace.
- 0:54-0:59 paradise garden: fine. Keep as the one new picture of the ending. Drop the shared risen-hand shot at 0:44 for `answer_light_profile` held longer.

**Task B - how familiar?** About 90% have heard this exact telling. It is the most-told story in the group.

**Fresh insight 1 (strongest). Joseph, two prisoners, and "remember me".**
- Genesis 40:14, Joseph in prison to the butler: "But think on me when it shall be well with thee, and shew kindness, I pray thee, unto me"
- Genesis 40:20-22: "the third day ... he restored the chief butler ... But he hanged the chief baker"
- Genesis 40:23: "Yet did not the chief butler remember Joseph, but forgat him."
- Luke 23:42-43: "Lord, remember me when thou comest into thy kingdom. ... To day shalt thou be with me in paradise."
- The point: an innocent man between two condemned men. One is lifted up, one is hanged. Someone says "remember me". In Genesis the one who was asked forgot. On the cross the roles turn: the guilty man asks the innocent one, and Jesus does not forget. He does not even wait.
- Why missed: nobody reads Genesis 40 next to Luke 23.
- Odds heard: about 6%.
- Risk: medium. The New Testament never names Joseph as this picture. Present it as an echo ("the Bible has seen this scene before"), never as a prophecy. Sound as long as it stays an echo.
- Size: new script (new hook, new spine). Worth it. This is the one that best answers the owner's challenge.

**Fresh insight 2. He was a mocker an hour before.**
- Matthew 27:44: "The thieves also, which were crucified with him, cast the same in his teeth."
- Luke 23:34: "Father, forgive them; for they know not what they do."
- Both thieves mocked at first. One changed, on the cross, in a few hours. What did he hear in between? "Father, forgive them."
- Odds heard: about 25%. Risk: low to medium. This is the usual way the two accounts are read together. A few say Matthew speaks loosely. Say "Matthew tells us both began by mocking". Also it fixes a soft spot: the current script paints the two as opposite from the start.
- Size: small. Two lines.

**Fresh insight 3. The first man back in the garden.**
- Genesis 3:24: "So he drove out the man; and he placed at the east of the garden of Eden Cherubims, and a flaming sword which turned every way, to keep the way of the tree of life."
- Revelation 2:7: "the tree of life, which is in the midst of the paradise of God."
- A man was driven out of the garden for taking from a tree. The first man the Bible shows going back in is a thief, beside a tree.
- Odds heard: about 15%. Risk: low to medium. Old and orthodox reading. Keep "paradise" tied to Rev 2:7 so the garden link is from Scripture. Size: small. The ending garden clip already fits it.

---

## 4. Woman, Behold Thy Son (John 19:26) - 59 s

Film: [woman_behold_john1926_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/woman_behold_john1926/visual/woman_behold_john1926_sfx_v5hook.mp4)

**What I saw.** The best single image in the group: Mary holding the baby with a cross-shaped shadow on the wall behind her (0:04-0:08). Simeon in the temple. Mary and John looking up. John leading Mary to the city gate.

**Weakest 10 s: 0:28-0:38.** Jesus' two sayings. "Woman, behold thy son!" plays over two strangers kneeling at a cross shadow. "Behold thy mother!" plays over a nail in a hand. Neither picture shows Mary or John. The key words of the film have the wrong pictures.
Also flat: 0:40 (motion 1.8, a mostly blank page) and the last 6 s.

**Single biggest win.** Put Mary and John on screen for the two "Behold" lines, and draw the line between them.

**Plan**
- 0:28-0:32 "Woman, behold thy son!" Use `jesus_looks_down` then `mary_and_john` (both exist). `focal-tour`: light on Mary, then on John.
- 0:32-0:36 "Behold thy mother!" Same shot, light goes John back to Mary. Then one hand-drawn line joins the two (`marginalia` leader line, no text). Why: a new family is drawn in front of us.
- 0:08-0:12 "Thirty years later, the sword lands." `ink-transition` from the cross-shadow still to the real cross. Why: the shadow becomes the thing. This is the film's best idea and right now it is a hard cut.
- 0:04-0:08 Simeon's line. `raking-light` slowly crossing the wall so the cross shadow shifts. $0. Why: the shadow feels alive, like a warning.
- 0:36-0:40 "took her unto his own home". Good clip. Add one tiny `map`-style doodle path from the hill to the gate (optional).
- 0:40 "A son. A home." Fix the near-blank page. Bring both panels in at once.
- 0:52-0:59 end: the shared risen hand again. Better: return to the mother-and-shadow still, now with morning light (1 new clip, about $1-1.50) so the film closes on its own image.
- Remove the "BEHOLD = HERE IS" card from the kneeling-strangers shot, or move it onto the Mary and John shot.

**Task B - how familiar?** About 55%. "He cared for His mother while dying" is very common (about 85%). The Simeon sword link lifts it (about 35% have joined those two).

**Fresh insight 1 (strongest). "Woman" twice, and the hour.**
- John 2:3-4, the wedding: "They have no wine. Jesus saith unto her, Woman, what have I to do with thee? mine hour is not yet come."
- John 19:26-27: "Woman, behold thy son! ... And from that hour that disciple took her unto his own home."
- John 19:29: "they filled a spunge with vinegar" (sour wine)
- The point: Mary is in John's Gospel only twice. Both times He calls her "Woman". The first time the wine has run out and He says His hour is not here yet. The second time the hour has come, and the only wine left is sour, and it is for Him. He gave the good wine. He drank the bad.
- Odds heard: about 15%.
- Risk: low. Both scenes and the "hour" word are John's own framing. Keep the wine contrast as a picture, not a doctrine.
- Size: medium. A new middle. The Simeon open can stay.

**Fresh insight 2. Why John, and not His brothers?**
- John 7:5: "For neither did his brethren believe in him."
- John 19:27: "Then saith he to the disciple, Behold thy mother!"
- Acts 1:14: "with the women, and Mary the mother of Jesus, and with his brethren."
- He had brothers. They did not believe yet. So at the cross He starts a new kind of family, joined by Him and not by blood. Weeks later His own brothers are in the room, praying.
- Odds heard: about 20%. Risk: low to medium. "Brethren" is read differently across church traditions (brothers, or wider kin). The point holds either way, so do not lean on which. Size: small to medium, 2-3 lines. Gives a far better ending than the current one.

**Fresh insight 3. The seed of the woman.**
- Genesis 3:15 names "the woman" and "her seed" and a bruised heel. At the hour of the bruising He says "Woman".
- Odds heard: about 15%. Risk: MEDIUM-HIGH. This runs into different church teachings about Mary. I would not use it in a short. Listed for honesty, not recommended.

---

## 5. It Is Finished (John 19:30) - 59 s

Film: [it_is_finished_john1930_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/it_is_finished_john1930/visual/it_is_finished_john1930_sfx_v5hook.mp4)

**What I saw.** The most varied film of the cross set (17 clips). Garden valley, golden lake, a carpenter's bench, hands holding a sun (lovely), garden prayer, sponge, tomb, dawn, a man lifting his face.

**Weakest 10 s: 0:10-0:20.** "God rested. He does not leave work half done" over a workbench x3 (same picture three times), then "When sin wrecked that world" over the three crosses. The break of the world is never shown. We jump from "nothing was broken" to the cross with no break in between.

**Single biggest win.** One crack. At 0:14 let a real crack run across the perfect garden from the opening. Then the "mend it" line has something to mend.

**Plan**
- 0:14-0:18 "When sin wrecked that world". Bring back `eden_garden_finished` and run a hand-drawn ink crack across it (Remotion on top of the clip, or `ink-transition` with a jagged front). Why: we must see it break.
- 0:18-0:22 "All things were made by him." Keep the hands and sun. Add `line-boil` so the hand lines breathe. $0.
- 0:22-0:24 "The hands that finished creation came to finish redemption." Match cut: hands holding the sun to the nailed hand, same position on screen. `ink-transition`. Why: same hands. This is the film's thesis and it is currently just a cut.
- 0:44-0:48 "Two finished works. One Workman." `infographic-panel` diptych: garden left, cross right, hand-drawn brush arrow, the word FINISHED written under both by the same hand (`keeper-hand`). Spoken too.
- 0:48-0:52 "rested in the tomb through the sabbath". A 7-box week doodle: six ticks, a rest; then six ticks again, a rest, and box one lights. (Remotion, hand-drawn boxes.) Why: makes "sixth day, seventh day, first day" plain for a newcomer.
- Era check: the saw on the bench has a metal frame like a modern hacksaw. Zoom and check. Paint out or swap for a simple hand saw.
- Fact check: John 17:4 is shown as a prayer in the garden at night. John 18:1 says "When Jesus had spoken these words, he went forth ... over the brook Cedron, where was a garden". So He prayed it BEFORE the garden. Small, but a Bible reader may catch it. Either reframe the still (upper room / on the way) or accept and note.
- Tomb at 0:48: a round stone is in frame. Memory says Kling tends to roll it. Check the clip start to end.
- 0:56-0:59 end: flat (motion 2). Use `man_lifting_face_dawn` as the last picture, not the shared cross.

**Task B - how familiar?** Already the freshest script in the group. About 35% have heard "finished creation / finished redemption / rested". Most have only heard "paid in full". Say so to the owner: this one is not stale.

**Fresh insight 1 (strongest). Three "finished" works. Each time, God moves in.**
- Genesis 2:1: "Thus the heavens and the earth were finished"
- Exodus 40:33-34: "So Moses finished the work. Then a cloud covered the tent of the congregation, and the glory of the LORD filled the tabernacle."
- John 19:30: "It is finished"
- Matthew 27:51: "And, behold, the veil of the temple was rent in twain from the top to the bottom"
- The point: the script has two finishings. The Bible has a third in between. Each time a work is finished, God comes to live with people: the garden, the tent, and then the veil tears and the way in is open to all.
- Odds heard: about 10%.
- Risk: low. The Genesis and Exodus wording match is well known to Bible scholars and fully orthodox.
- Size: small to medium. Add one beat (about 12 words) and the veil. The veil clip already exists in the Forsaken Cry folder.

**Fresh insight 2. It was in a garden.**
- John 19:41: "Now in the place where he was crucified there was a garden"
- John 20:15: "She, supposing him to be the gardener"
- The first work was finished in a garden. So was the second. On the first morning He is taken for the gardener.
- Odds heard: about 20%. Risk: low. Size: small, one or two lines. Fits the opening garden clip and pays it off.

**Fresh insight 3. The sixth day, the sleep, the side.**
- Genesis 2:21-22: "caused a deep sleep to fall upon Adam ... and he took one of his ribs ... made he a woman"
- John 19:34: "one of the soldiers with a spear pierced his side, and forthwith came there out blood and water."
- Odds heard: about 15%. Risk: medium. Very old reading, but the Bible does not state it. Keep as "an echo". Probably too much for this short. Could be its own piece.

---

## 6. Father, Into Thy Hands (Luke 23:46) - 59 s

Film: [into_thy_hands_luke2346_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_01_cross/into_thy_hands_luke2346/visual/into_thy_hands_luke2346_sfx_v5hook.mp4)

**What I saw.** The warmest film. Sleeping child, a father's big hand over a small hand, hands of light opening in the clouds, father holding a sleeping child, child waking at dawn. The hands motif is strong and it is this film's own.

**Weakest 10 s: 0:28-0:38.** "He begins with a word the Psalm does not have. Father. Not judge. Not stranger. Father." This is the heart, and it is the stillest stretch (motion 3.6). The picture is the father at the door with a lamp, three crops of one image. The added word is never SHOWN being added.
Also flat: 0:10-0:14 (Psalm on the scroll, motion 2) and 0:44-0:48.

**Single biggest win.** Show the word being added. Psalm line on the scroll. Then one word, "Father", written in at the front by hand.

**Plan**
- 0:10-0:16 Psalm 31:5 on the scroll. `keeper-hand` writes the line on the scroll as spoken. Move the "REDEEMED = BOUGHT BACK" card off this beat (it lands before the idea is used).
- 0:28-0:32 "a word the Psalm does not have". Bring the scroll back. A caret mark, then "Father," written in before the line (`keeper-hand` or `marginalia`). `annotators-circle` on it. Why: this is the whole insight, in one gesture. Spoken too.
- 0:32-0:36 "Not judge. Not stranger. Father." Three beats. Two words written and struck through by hand, the third stays (`keeper-hand` word-strike). Then cut to the father at the door, ONE full panel, not three crops.
- 0:36-0:40 "he was buying that redemption". Now use the "bought back" decode here, as a hand note, where it belongs.
- 0:40-0:44 "like a child falling asleep in his father's arms". Good clip. Add `held-breath` so everything quiets. No new text.
- 0:44-0:50 "death loses its last word". Child waking x3: swap 2 crops for `first_day_morning` and `child_waking_dawn` full.
- 0:54-0:59 end: use `father_hand_childs_hand` or `hands_of_light_open` as the last image, not the shared cross. "He keeps the morning" should end on hands.
- Tomb at 0:42: round stone in frame again. Check the clip for a rolling stone.

**Task B - how familiar?** About 40%. "He quoted Psalm 31 and added Father" is known to keen readers. The child's-prayer frame is fresh in feel.
One honest flag: "Jewish tradition made these words an evening prayer" comes from later Jewish writings, not from the Bible, and we cannot prove children prayed it in Jesus' day. The script words it carefully. Keep it careful, or lean on the Bible points below.

**Fresh insight 1 (strongest). His first words and His last words in Luke are the same word.**
- Luke 2:49, age twelve, His first recorded words: "wist ye not that I must be about my Father's business?"
- Luke 23:46, His last before death: "Father, into thy hands I commend my spirit"
- The point: the boy in the temple says "my Father". The man on the cross says "Father". His whole life in Luke sits between those two. The child's-prayer idea is no longer only tradition. It is in the text.
- Odds heard: about 8%.
- Risk: low. It is simply what Luke records.
- Size: small. One or two lines. It also makes the child pictures fit even better (1 new shot of the boy in the temple, about $1-1.50, would seal it).

**Fresh insight 2. A day of hands.**
- Luke 9:44: "the Son of man shall be delivered into the hands of men."
- Luke 24:7: "The Son of man must be delivered into the hands of sinful men"
- John 10:18: "No man taketh it from me, but I lay it down of myself."
- Luke 23:46: "Father, into thy hands"
- John 10:29: "no man is able to pluck them out of my Father's hand."
- All day He was handed from one set of hands to the next. The last move was His own. He put Himself in the only hands nobody can take from.
- Odds heard: about 12%. Risk: low. Size: medium, a reworked middle. Fits the film's hands motif perfectly.

**Fresh insight 3. The first to die after Him prayed His prayer, to Him.**
- Acts 7:59-60: "Lord Jesus, receive my spirit. ... And when he had said this, he fell asleep."
- Stephen prays the same prayer, but to Jesus. And Luke says he "fell asleep".
- Odds heard: about 35%. Risk: low. Size: small. A strong, earned landing: someone already did what the film asks.

---

## 7. The Sign of Jonah (Matthew 12:40) - 70 s

Film: [sign_of_jonah_matt1240_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_02_resurrection/sign_of_jonah_matt1240/visual/sign_of_jonah_matt1240_sfx_v5hook.mp4)

**What I saw.** The best looking film of the nine. Thrown overboard, the great fish rising under a tiny man, ship in the wave, lots on the deck, sinking, praying inside the ribs, Jesus and the scribes, a wrapped body, a hand of light reaching into dark water. Every picture is its own.

**Weakest 10 s: 0:44-0:54.** "I went down guilty... He went down innocent... The grave no more held Him than the deep held me." The guilty/innocent contrast is the doctrine of the film, but the two pictures come one after the other, never together, and 0:50-0:54 is a near-blank page (motion 2.4).
Also flat: 0:36 (the Matthew 12:40 quote over one held shot).

**Single biggest win.** Match the two descents. Jonah sinking and the body laid in the tomb, side by side, same pose, same downward move. Then both rise.

**Plan**
- 0:34-0:42 Matthew 12:40. `infographic-panel` diptych: fish belly left, tomb right. On "three days and three nights" three small hand-drawn sun-and-moon marks tick under EACH side at the same time. Why: "as Jonas... so shall the Son of man" is a side-by-side sentence.
- 0:44-0:50 guilty / innocent. Same diptych. Hand-written word under each: "guilty" under Jonah, "innocent" under Christ (`keeper-hand`). Spoken too.
- 0:50-0:54 "The grave no more held Him". Fill the blank page. Both halves rise together: `jonah_on_shore` and the empty-tomb garden clip (both exist).
- 0:06-0:12 "He sent me to Nineveh". `map`: a small inked map. Arrow one way to Nineveh (east). Jonah's ship line the other way (west). Why: "I ran" becomes funny and clear in 3 seconds. Era check on the city: it is drawn as a stepped pyramid that reads Central American. Nineveh should read Assyrian (walls, gates, winged bulls). Worth 1 new still + clip (about $1-1.50).
- 0:14-0:18 "the lot fell on me". `impact-burst`, small, on the lot. `annotators-circle` on the one dark pebble.
- 0:54-0:60 hand of light into the deep: lovely. Leave alone.
- 0:02-0:04 the fish rising: the hero shot. Add a `parallax-panel` depth pass only if the clip is slow. Do not restyle.

**Task B - how familiar?** About 75% know "three days in the fish, three days in the grave". The first-person voice and guilty/innocent line are fresher (about 35%).

**Fresh insight 1 (strongest). Jonah was from Galilee.**
- 2 Kings 14:25: "his servant Jonah, the son of Amittai, the prophet, which was of Gathhepher."
- John 7:52, the Pharisees: "Search, and look: for out of Galilee ariseth no prophet."
- Matthew 12:41: "behold, a greater than Jonas is here."
- The point: the experts said no prophet comes from Galilee. Jonah did. His home town, Gath-hepher, is in the hill country of Zebulun (Joshua 19:13), in Galilee, a short walk from Nazareth. So the one sign Jesus gave them was a prophet from His own hills. They had forgotten their own Bible.
- Odds heard: about 5%.
- Risk: low for "Jonah was from Galilee" (Bible plus settled geography). "A short walk from Nazareth" rests on where the village is placed on the map, which is the usual view but comes from outside the Bible. Say "in the same hills".
- Size: small to medium. A new hook: "They said no prophet ever came from Galilee. They forgot one." Jonah can say it himself in his own voice.

**Fresh insight 2. The sailors and the crowd.**
- Jonah 1:14, pagan sailors about a guilty man: "let us not perish for this man's life, and lay not upon us innocent blood"
- Matthew 27:24, Pilate: "I am innocent of the blood of this just person"
- Matthew 27:25: "Then answered all the people, and said, His blood be on us, and on our children."
- Heathen sailors begged not to be charged with a guilty man's blood. At the cross people called for the blood of the innocent One. And He let it cover them in mercy.
- Odds heard: about 5%. Risk: MEDIUM. Matthew 27:25 has been badly misused against Jewish people. Must say "we", "people like us", all of us. Needs the panel and care. Size: medium.

**Fresh insight 3. "Salvation is of the LORD" - and the fish lets go.**
- Jonah 2:9-10: "Salvation is of the LORD. And the LORD spake unto the fish, and it vomited out Jonah upon the dry land."
- Matthew 1:21: "thou shalt call his name JESUS: for he shall save his people from their sins."
- The last word Jonah says in the dark is, in Hebrew, the word Jesus' name is built from. The very next line, the deep gives him up.
- Odds heard: about 10%. Risk: low to medium. This is a Hebrew point you cannot see in English. Say "the word behind Jesus' name", not "Jonah said Jesus". Size: small, 1-2 lines near the turn.

Also possible: Jonah asleep in the storm / Jesus asleep in the storm (Jonah 1:5-6, Mark 4:38). But the series already has "He Was Asleep in the Storm", so I leave it.

---

## 8. The Empty Tomb (John 20:8) - 79 s

Film: [empty_tomb_john208_sfx_v5hook.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_02_resurrection/empty_tomb_john208/visual/empty_tomb_john208_sfx_v5hook.mp4)

**What I saw.** A good mystery build. Stone in the dark, Mary running at us, two men running, the linen on the slab, the rolled head-cloth set apart, John kneeling in a shaft of light, Thomas, the risen Christ, the tomb door at dawn. Motion is the highest of the group (11 clips, none shared with the cross set).

**Weakest 10 s: 0:48-0:58.** "He did not yet know the scripture. The linen was enough." The picture is the outside of the tomb in three stacked crops, the same stone seen for the third time. The words say LINEN and we look at a rock.
Also flat: 1:08 (motion 1.0, the doorway shot as "You were not at the tomb" starts).

**Single biggest win.** Treat it like a detective scene. The cloth is the clue. Circle it. Note it. Keep the camera on it.

**Plan**
- 0:22-0:30 John 20:7. `focal-tour`: light on the linen, then travels to the rolled napkin "in a place by itself". Then `annotators-circle` around the napkin. Why: the verse walks the eye exactly this way.
- 0:28-0:32 "What thief wraps the face-cloth?" `margin-study`: one quick pencil study of the rolled cloth in the margin with a hand note and a question mark. Why: it turns the viewer into the detective. Spoken too.
- 0:10-0:20 the running. `map`-style doodle: two dotted paths to the tomb, one dot pulls ahead (John outran Peter, John 20:4). 3 seconds. Small smile, and true to the text.
- 0:48-0:58 "The linen was enough." Replace the outside-stone grid with `linen_left_lying` full frame and a slow `raking-light` pass across the cloth. $0. Why: stay on the evidence.
- 0:40-0:46 "and he saw, and believed." Good shot. Add `held-breath` quiet. No text beyond the quote.
- 0:58-1:02 Thomas: the hands are drawn very red and wet. Eight days after, the risen Lord shows marks, not fresh blood. Tone down by paint-out if the owner agrees.
- 1:08-1:14 "You were not at the tomb." `parallax-panel` on the doorway still so the view drifts as if we step toward it. Why: "you" are now the one walking in.
- The stone: a round stone is in many shots. Check each clip that it never rolls.

**Task B - how familiar?** About 50%. The napkin is semi-famous. "John believed from the linen, before he understood the Scripture" is fresher (about 25%). A decent script already.

**Fresh insight 1 (strongest). John has seen a napkin before. Lazarus was still wearing his.**
- John 11:44: "And he that was dead came forth, bound hand and foot with graveclothes: and his face was bound about with a napkin. Jesus saith unto them, Loose him, and let him go."
- John 20:7: "And the napkin, that was about his head, not lying with the linen clothes, but wrapped together in a place by itself."
- Romans 6:9: "Christ being raised from the dead dieth no more; death hath no more dominion over him."
- The point: John uses the word napkin for a grave only twice. Lazarus came out still wrapped. Others had to free him. He would need those cloths again one day. Jesus left His behind, set aside. He was not coming back for them. John stood at both tombs. That is why the cloth was enough.
- Odds heard: about 12%.
- Risk: low. Both verses are plain. "He would need them again" is a fair step (Lazarus died again). Say it as a thought, not a verse. Avoid the popular "folded napkin at a meal means I'm coming back" story. It has no Bible or history behind it.
- Size: small. 2-3 lines right after "What thief wraps the face-cloth?". One new shot of Lazarus in his wraps (about $1-1.50) would make it land.

**Fresh insight 2. Two angels, one at the head, one at the feet.**
- John 20:12: "two angels in white sitting, the one at the head, and the other at the feet, where the body of Jesus had lain."
- Exodus 25:18, 22: "two cherubims of gold ... in the two ends of the mercy seat. ... And there I will meet with thee"
- The empty slab, with an angel at each end, looks like the mercy seat, the one place where blood was brought and God met man.
- Odds heard: about 12%. Risk: medium. A loved reading, but John does not say it. Present as "a picture a Bible reader would know". Size: medium. It moves the scene from John to Mary (verses 11-12). Better as a new sister short.

**Fresh insight 3. A garden, and a gardener.**
- John 19:41 and 20:15 (quoted in episode 5 above). Odds heard: about 20%. Risk: low. Better used in "It Is Finished".

---

## 9. Women as First Witnesses (Luke 24:5-6) - 82 s

Film: [women_first_witnesses_luke245_sfx.mp4](file:///F:/slk/PycharmProjects/JesusInTheBible/batches/cluster_02_resurrection/women_first_witnesses_luke245/visual/women_first_witnesses_luke245_sfx.mp4)

**What I saw.** Different page design from the rest (tall text box top-left, real 4-panel grids with different shots). The apostles waving the women away. Three distinct women. Galilee hillside. Women watching the cross from far off. Dawn path. Two shining men. A tear close-up. Women running. This is the only film with real panel variety. It is also the longest.

**Weakest 10 s: 0:10-0:22.** The court argument. "A woman's word carried almost no weight in court. No one inventing a resurrection would open it there. Luke gains nothing..." About 12 s of reasoning over women's faces and two men thinking. It is a talk, not a story. Motion is fine. The idea is the slow part.
Also flat: 0:06-0:10 (the "idle tales" quote, motion 3).

**Single biggest win.** Draw the trail. The script's best thread is "they never left": Galilee, the cross, the burial, the dawn. Put it on screen as one hand-drawn path with four stops.

**Plan**
- 0:22-0:34 "Luke named these women long before... They watched Him die. They saw where He was buried. At dawn, they were back." `map`: one inked path, four stops that tick on as each is said (Galilee, the cross, the tomb at dusk, the tomb at dawn). The clips play inside each stop. Why: faithfulness becomes a line you can follow.
- 0:22-0:26 names. `marginalia`: hand-letter "Mary Magdalene" and "Joanna" with leader lines to two faces. Why: named people are harder to dismiss, and it sets up Joanna (see insight 1). Check the three women stay the same three in every shot (cloned-people rule).
- 0:06-0:10 "idle tales". `annotators-circle` on "idle tales". At 1:04 "The idle tale was true", bring the same circled words back and strike "idle" by hand (`keeper-hand` word-strike). Why: a clean set-up and pay-off, in a doodle.
- 0:10-0:22 court beat: cut to one line (see insight 2 for what to put there instead). If kept, use a simple hand-drawn balance scale that will not tip (Remotion). 3 seconds, not 12.
- 0:44-0:52 "remember how he spake unto you when he was yet in Galilee". `ink-transition` from the bright tomb back to the Galilee hillside. Why: "remember" is a flashback. Make it feel like one.
- Angels: Luke 24:4 says "two men ... in shining garments". They are drawn fine (no wings). Good.
- 1:08-1:22 end: 14 s on one risen-Christ shot is long. Split with the women running (`women_run_tell`) under "sends His word to the overlooked".
- No hook card on this one (file is `_sfx`, not `_v5hook`). The others have one. Decide on purpose.

**Task B - how familiar?** About 65%. "Women were the first witnesses and their word did not count in court, so nobody would make it up" is one of the most repeated Easter points. The "remember... Galilee" thread is fresher (about 20%).

**Fresh insight 1 (strongest). Joanna, from Herod's own house.**
- Luke 8:3: "And Joanna the wife of Chuza Herod's steward"
- Luke 9:9: "And Herod said ... who is this, of whom I hear such things? And he desired to see him."
- Luke 23:8-9: "he hoped to have seen some miracle done by him. Then he questioned with him in many words; but he answered him nothing."
- Luke 24:10: "It was Mary Magdalene, and Joanna, and Mary the mother of James ... which told these things unto the apostles."
- The point: King Herod wanted a miracle for years. When he finally met Jesus he got silence. But the wife of Herod's own steward stood at the empty tomb. The king got nothing. A woman from his staff got the resurrection.
- Why missed: Joanna is a name people read past. Only Luke names her, and only twice.
- Odds heard: about 4%.
- Risk: low. Every step is Luke's own words. Do not guess what Joanna told Herod's house. Stay with what is written.
- Size: small to medium. The script already names Joanna. Swap the 12 s court beat for this. It carries the same "overlooked" theme, but from the Bible itself and not from outside history.

**Fresh insight 2. Jesus took the women's side.**
- Luke 24:11: "And their words seemed to them as idle tales, and they believed them not."
- Luke 24:22-25, that same day on the road: "certain women also of our company made us astonished ... Then he said unto them, O fools, and slow of heart to believe"
- Mark 16:14: "upbraided them with their unbelief and hardness of heart, because they believed not them which had seen him after he was risen."
- The men called it idle tales. The first thing the risen Jesus does about it is tell them off for not believing.
- Odds heard: about 12%. Risk: low to medium. Luke 24:25 is about being slow to believe the prophets, and Mark 16:14 names the witnesses, so word it as "He rebuked their unbelief", and quote Mark for the direct link. (Mark 16:9-20 is the longer ending of Mark. It is in the KJV. Some will raise it.) Size: small, 2 lines.

**Fresh insight 3. God kept His own witness rule.**
- Deuteronomy 19:15: "at the mouth of two witnesses, or at the mouth of three witnesses, shall the matter be established."
- Luke 24:4: "two men stood by them in shining garments"
- Luke 24:10 names three women.
- The courts would not count them. God sent two and three anyway, just as His law asks.
- Odds heard: about 10%. Risk: low to medium. A neat pattern, not a stated claim. Say "notice the numbers". Size: one line.

---

## Top 5 quality wins for the group (ranked)

1. **Break up the one-clip grids.** Every `hero_band3` / `hero_frac3` grid that shows the same picture three times gets either one full panel or three different clips (most already exist in each folder). $0. Lifts all 8 older films at once.
2. **Stop sharing the same 6 pictures across the cross shorts.** Give each film its own ending image from its own clips (hands for "Into Thy Hands", water for "I Thirst", the lifted face for "It Is Finished", mother-and-shadow for "Behold Thy Son"). Mostly $0. About 2-4 new shots in total if wanted (about $3-6, not spent).
3. **Put the right picture on the key line.** Three films show the wrong thing at the heart: Forsaken Cry 0:40 (risen glow over "forsaken"), Behold Thy Son 0:28 (strangers and a nail over "behold thy son / thy mother"), Empty Tomb 0:48 (stone over "the linen was enough"). All fixable with clips that already exist.
4. **Add hand-drawn doodles, 2-3 per film, each tied to a spoken word.** Circle the key word (`annotators-circle`), write the word in (`keeper-hand`), strike the wrong word, draw the path (`map`). Best single ones: "Father" written into the Psalm (ep 6), "someday" struck for "today" (ep 3), the cloth circled as a clue (ep 8), the four-stop trail (ep 9).
5. **Side-by-side for every "as... so" line.** `infographic-panel` diptychs: David's line / Jesus' cry (ep 1), fish / tomb (ep 7), garden / cross (ep 5), two thieves (ep 3). The scripts are built on pairs. The screen should show pairs.

Small fixes to do in the same pass: "Same nails" over roped thieves (ep 3); hammer and fresh blood at the ninth hour (ep 1); modern-looking saw (ep 5); John 17 prayer shown in the garden (ep 5); pyramid-like Nineveh (ep 7); wet red hands eight days later (ep 8); round stones that may roll (ep 5, 6, 8).

## The 3 strongest fresh insights in the group

1. **Joanna of Herod's house (ep 9).** Luke 8:3, 9:9, 23:8-9, 24:10. The king who wanted a sign got silence. His steward's wife got the empty tomb. About 4% have heard it. Pure Luke. Low risk. Small script change.
2. **Jonah was from Galilee (ep 7).** 2 Kings 14:25 with John 7:52 and Matthew 12:41. "Out of Galilee ariseth no prophet", yet the one sign Jesus gave was a prophet from His own hills. About 5%. Low risk. New hook, small change.
3. **"Remember me": Joseph and the two prisoners (ep 3).** Genesis 40:14, 40:20-23 with Luke 23:42-43. The butler forgot Joseph. Jesus did not forget the thief, and did not make him wait. About 6%. Medium risk (an echo, not a stated prophecy, and it must be said that way). Needs a new script.

Close runners-up: first and last words in Luke are both "Father" (ep 6, Luke 2:49 / 23:46, about 8%, low risk, tiny change); "my God" becomes "your God" (ep 1, Ps 22:22 / Heb 2:12 / John 20:17, about 8%, low risk); Lazarus still wore his napkin (ep 8, John 11:44 / 20:7, about 12%, low risk, tiny change); three "finished" works and God moves in each time (ep 5, Gen 2:1 / Exod 40:33-34 / Matt 27:51, about 10%, low risk).

## My honest answer to the owner's challenge

Yes, the challenge is fair for most of this group. Six of the nine tell a point most churchgoers have heard (55-90%). Two are already fairly fresh (It Is Finished, Empty Tomb). The fresh material is there in the text, and most of it can go in with small changes, because the pictures already fit.

But one caution. These are ideas from one model. None of them has been through the blind panel or the doctrine check. Three carry real care points (Matthew 27:25 in ep 7, the Mary reading in ep 4, the mercy-seat picture in ep 8). Any narration change also re-opens the words-before-money gate and means new voice, which costs money and needs its own ask.

My pick: start with the three small-change ones that need no new pictures: Joanna (ep 9), first-and-last "Father" (ep 6), Lazarus' napkin (ep 8). Send those three to the panel first.
