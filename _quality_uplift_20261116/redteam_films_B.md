# Red team B: films 5, 6, 7 (2026-11-16)

Reviewer: independent, blind. I looked only at the old and new mp4 files, the narration.md files and the two design specs. No builder notes, gate files or review pages were read.

Method: 2 frames/second pulled from all 6 files, old and new put side by side at 1 frame/second (21 contact sheets), then full-size strips and 1:1 crops of every suspect shot. Per-frame motion measured on every shot (cut detection + freeze count). Audio checked with `ffmpeg -map 0:a -c copy -f md5`.

All evidence frames are in `C:\Users\sanjay\AppData\Local\Temp\redteamB\` (called `TEMP\` below).

## What passed on all three

| Check | ep10 | ep11 | Woman Behold |
|---|---|---|---|
| Audio md5, old = new | 856871eb... same | 5ea10c3a... same | ec440b1d... same |
| Length, old = new | 106.17 s | 83.57 s | 59.07 s |
| Size | 1080x1920 (old 720x1280) | 1080x1920 (old 720x1280) | 1080x1920 |
| Frozen shots in new | none (old: back cover dead still for its last 3 s) | none (old F03 was a fully frozen picture, 179 of 181 frames identical) | none |
| Old zoom-fill that cut off words | gone (old back cover ended on "...HIS PEAC") | gone (old F07 zoomed until "where are the nine?" was cut) | n/a |
| Burned captions added to Swirls | none | none | n/a |

Limits: I judged from frames, not playback with sound. I did not run a reverse-play (boomerang) test; I saw no backwards motion in the frame sequences. Costs are rough, from the spec's own rates ($0.063 per clip second, $0.08 per still).

---

## Film 5. Swirls ep10 She Loved Much

**VERDICT: NEEDS PAID FIX** (about $1.00 first take, $1.50 with redos)

**Clearly better than old? Yes.** The feet are now three real shots (tear, hair, oil) instead of one zoomed still, the hook words now sit on the page that shows them, the end card is no longer cropped, and nothing freezes. But three of the new clips break the "blue ink never moves" rule, and one has her walk out of the picture.

Defects, most severe first:

1. **91.9-98.4 s, new page F09B ("Thy faith").** The blue-gold ribbon slides across the whole page and leaves the frame. The woman walks out of the panel; by 98.3 s the doorway is empty. Top panel 1 ("the door") also swings shut by itself. Rules: motif never animated; no people walking out of panels; no invented content. Fix: paid, re-animate about 7 s (~$0.45), brief = she takes one step and holds, ribbon exactly as drawn. CONFIRMED: `TEMP\e10_f09b.jpg`.
2. **78.0-83.9 s, new page F08B ("the receipt, not the price").** The blue flower motif drifts down onto her hand and then vanishes; it is gone by 83.8 s. Rule: motif never animated. Fix: paid, re-animate about 6 s (~$0.38). CONFIRMED: `TEMP\e10_f08b.jpg`.
3. **40.5-43.4 s, new page F04B ("answered anyway").** The blue wisp above Jesus' hand changes shape (straight line at 40.55, curled at 43.3). Also Jesus lies back with His head propped on His fist: a casual, lounging pose at the moment He answers Simon. Rules: motif never animated; reverent. Fix: paid, new still + 3 s (~$0.27), or re-animate only (~$0.19) if the owner accepts the pose. CONFIRMED: `TEMP\e10_f04b_f06b.jpg` (left two frames).
4. **58.3 s, cut from F06 to new F06B.** Simon is bald on F06 and wears a striped head-cloth with a full grey beard one frame later; on F07 he is bare-headed and grey again. The new close-up makes the old mismatch more visible. Rule: recurring people keep the same face and clothes. Fix: paid, redraw F06 (the spec's own optional item, ~$0.52), or accept. CONFIRMED: `TEMP\sheet_e10_048.jpg` (58 s and 59 s tiles).
5. **21.9-32.5 s, feet pages.** The foot rests on a bare wooden bench under a white robe on F03A and F03B, then on a cushion under an olive robe on F03C. F02 just before shows a cushioned couch. Small continuity slip. Fix: accept, or redo F03C still. CONFIRMED: `TEMP\e10_f03abc.jpg`.
6. **25.0-28.6 s.** The voice says "and kissed his feet" while the page shows hair wiping (caption "her hair"). The old film showed the kiss on this line. Small picture/word mismatch. Fix: free, move the cut, or accept. CONFIRMED: `TEMP\sheet_e10_024.jpg`.
7. **91.9-93.5 s, underline on "Thy faith".** It draws on the next page after the word has been spoken (word at about 91.6 s, line finishes about 93 s). Rule: marks tied to the spoken word. Fix: free. CONFIRMED: `TEMP\e10_f09b.jpg`, `TEMP\e10_misc.jpg`.
8. Kept from the old film, not a regression: the blue wisp on F05 and the blue cloud on F08 change shape inside their existing clips. SUSPECTED as a rule break the owner may want fixed later: `TEMP\sheet_e10_036.jpg`, `TEMP\sheet_e10_072.jpg`.

Marks that are fine: two panel rings on F01, tally on F05, red circle on "forgiven", tick on F08B. None touch a face, the motif or baked words. `TEMP\e10_misc.jpg`.

---

## Film 6. Swirls ep11 Where Are the Nine

**VERDICT: NEEDS PAID FIX** (about $2.10 first take, $3.20 with redos)

**Clearly better than old? Yes, but not ready.** The old film had a frozen key page, three clips that zoomed into the page, red-roofed farmhouses and a glow. Those are gone. But four of the re-made clips bring new faults, two of them on Jesus Himself, and the face fix did not land.

Defects, most severe first:

1. **21.5 s, page F03 ("Go shew yourselves unto the priests").** Jesus reaches out and puts His hand on a leper's arm. The story turns on the men standing far off, and the narration has just said "They'd stood at a distance, as their disease required". The blue wisp above His hand also drifts and is gone by 24.4 s. Rules: picture must not contradict the text; no invented content; motif never animated. Fix: paid, re-animate 6 s (~$0.38). CONFIRMED: `TEMP\e11_f03_touch.jpg`, `TEMP\e11_f01b_f03.jpg`.
2. **39-41.7 s, page F06 ("fell down on his face at his feet").** Jesus breaks into a stride with His robe flying open and a dust cloud behind Him, as if walking off past the man who is worshipping at His feet. In top panel 1 the feet walk out and leave an empty panel. Rules: reverent; no invented motion; people walking out of panels. Fix: paid, re-animate 7 s (~$0.44). CONFIRMED: `TEMP\e11_f06_f07.jpg` (first three frames).
3. **66.6-74.5 s, page F10 redraw (the face fix).** The Samaritan is now an elderly, grey, white-bearded man. On F06, F08 and F09 just before he is middle-aged with dark hair and a dark beard. It is closer than the old F10 (young, full head of hair) but still a different man. The blue-gold ribbon also grows and swings down behind his head during the clip. Rules: recurring people keep the same face; motif never animated. Fix: paid, new still + 8 s (~$0.59). CONFIRMED: `TEMP\e11_sam.jpg`, `TEMP\e11_f10.jpg`.
4. **41.7-47.2 s, page F07 ("Were there not ten cleansed?").** The blue wisp above Jesus' hand changes shape through the whole shot. Everything else on the page is still. Rule: motif never animated. Fix: paid, re-animate 6 s (~$0.38). CONFIRMED: `TEMP\e11_f06_f07.jpg` (last three frames).
5. **9.1-12.6 s, new page F01B ("at a distance").** I count 8 men, not ten. Rule: right number of people. Fix: paid, new still + 4 s (~$0.33). CONFIRMED: `TEMP\e11_counts.jpg`.
6. **55.2-62.1 s, page F09 (existing clip, kept).** A white ribbon sweeps through the three round top panels at 57-60 s. Present in the old film too. Rules: motif never animated; no invented content. Fix: paid, re-animate 7 s (~$0.44). CONFIRMED: `TEMP\sheet_e11_048.jpg` (57-59 s tiles).
7. **50.6-55.2 s, page F08 (existing clip, kept).** The man lifts himself to hands and knees and the blue cloud fades to wisps, then the voice says "To the one still on his face". Present in the old film too. Fix: paid (~$0.32), or accept. CONFIRMED: `TEMP\sheet_e11_048.jpg`, `TEMP\e11_f07b_f09b.jpg`.
8. **26.6-29.7 s, new page F04B ("they were cleansed").** The healed man is a new face (grey hair, no beard) that matches none of the ten and not the Samaritan; his fingers are a little malformed. A newcomer may take him for the hero. Fix: accept, or redo with the Samaritan's look. CONFIRMED: `TEMP\e11_f04b.jpg`.
9. **74.5-77.7 s, new page F10B.** The blue-gold ring shifts shape slightly. Small. CONFIRMED: `TEMP\e11_f10.jpg` (last two frames).

Good: new page F09B shows exactly nine men walking away (`TEMP\e11_f09b_count.jpg`). F05's top panels now hold still. Marks are clean: distance dashes, footprints under "One turned back", red circle on "stranger", underline on "faith". None touch a face or the motif.

---

## Film 7. Graphic comic Woman, Behold Thy Son

**VERDICT: LOCK AFTER FREE FIX**

**Clearly better than old? Yes.** Jesus' two sayings now play over Mary, John and His own face instead of two strangers and a nail. No page shows one clip cut three ways. The ending is no longer slowed. But three marks or cards sit on faces, including His.

Defects, most severe first:

1. **29.8-32.2 s, "Woman, behold thy son!".** The BEHOLD = HERE IS card covers John's whole face in the top panel. Rule: never cover faces. Fix: free, move the card or re-crop the panel. CONFIRMED: `TEMP\wb_a.jpg` (30.5 frame).
2. **28.8-31.9 s, same page.** The quote box lies across Jesus' mouth and beard while He speaks. The spec said it must sit on His chest. Rule: nothing on Jesus' face. Fix: free, shift the crop up or the box down. CONFIRMED: `TEMP\wb_a.jpg` (30.5 frame).
3. **20.0-22.1 s, gaze line.** The dashed line starts on Jesus' face, at His nose and beard, not below His chin outside the panel. Rule: marks never on Jesus' face. Fix: free, start it at the panel edge. CONFIRMED: `TEMP\wb_a.jpg` (21.0 frame).
4. **42.1-43.6 s, "A son. A home."** The gold thread runs over John's throat and knots on his neck. The crops also cut faces: the left panel shows John with no head, the right panel shows John's cheek and beard with his eyes cut off. Rules: marks never cover faces; crop on the face. Fix: free, re-crop both panels and run the thread shoulder to shoulder. CONFIRMED: `TEMP\wb_b.jpg` (40.5 and 43.4 frames).
5. **31.9-33.9 s.** Half the page is an empty pale box for 2 s under "Then saith he to the disciple". The old film had a full picture here. Same again at 18.7-19.7 s and 39.9-41.5 s. It reads as a missing picture. Fix: free, bring both panels in together. CONFIRMED: `TEMP\wb_a.jpg` (33.0 frame), `TEMP\sheet_wb_024.jpg`.
6. **22.1 s vs 24.3 s, John.** He is a dark-haired man in grey with a brown mantle on a blue sky, then a lighter-haired man in a cream cloak on a tan sky. The two shots sit back to back. Rule: recurring people keep the same face and clothes. Fix: free, use the first clip cropped on John, as the spec's own fallback says. CONFIRMED: `TEMP\wb_c.jpg`.
7. **8.5-13.1 s.** The bottom panel shows only two feet hanging into the frame; the gold thread passes close beside them and knots on the wood just below. Not on Him, but tight. Fix: free, lower the crop a little. CONFIRMED: `TEMP\wb_a.jpg` (12.6 frame).
8. **53.4-55.2 s, mourners page.** Graded dark, not warm as designed, and the caption box sits over the middle mourners. Small. CONFIRMED: `TEMP\wb_b.jpg` (54.5 frame).
9. Kept from the old film: the last caption reads "LET HIM BEHOLD YOU, AND BIND WHAT THE SWORD TORE", while narration.md says "The Son who saw her will behold you, and bind what the sword tore". I could not listen, so I cannot say which matches the voice. SUSPECTED: `TEMP\sheet_wb_048.jpg`.

Good: the route dots on "took her unto his own home" stay on open sand. The landing on the risen hand has no marks. The hook card is unchanged.

---

## Top 5 across the three films

1. **ep11, 21.5 s: Jesus touches a leper** in a story about men who stood far off. Paid re-animate. `TEMP\e11_f03_touch.jpg`
2. **ep11, 39-41.7 s: Jesus strides off with His robe flying** while the healed man worships at His feet. Paid re-animate. `TEMP\e11_f06_f07.jpg`
3. **ep10, 91.9-98.4 s: the woman walks out of the picture and the blue ribbon flies off the page.** Paid re-animate. `TEMP\e10_f09b.jpg`
4. **The blue ink moves in 7 new or re-made clips** (ep10 F04B, F08B, F09B; ep11 F03, F07, F10, F10B). The one rule the Swirls uplift was told never to break. Every new clip needs a motif pixel check before it enters a cut.
5. **Woman Behold, 20-32 s: a mark, a caption and a card sit on faces**, two of them on Jesus' face while He speaks. All free to fix. `TEMP\wb_a.jpg`

Also worth the owner's eye: ep11's face fix made the Samaritan an old man (`TEMP\e11_sam.jpg`), and ep11's "ten men" page shows eight (`TEMP\e11_counts.jpg`).
