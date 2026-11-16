# Plan review (independent Fable seat) - COMIC_DESIGN.md, Prophecy 01 "Born in Bethlehem"

Reviewed: `F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem\COMIC_DESIGN.md`
Against: `narration.md` (locked words), `audio\narration.words.json` (129 words, last word ends 48.50 s),
`look\art\D_barabbas_micah.png`, `look\art\D_barabbas_manger.png` (both looked at).
No other review file was read. Nothing was run or spent.

Short take: the idea is strong (page, scroll, one gold word, sacred quiet). The word times are right.
But the plan is not yet buildable as written. The panel shapes fight the 9:16 art, the plan breaks its
own safe zone and its own sacred rule in a few spots, and the first real viewer test comes AFTER the money.

---

## What I checked and found right

- Every caption/landing time in section 2 matches `narration.words.json` (spot-checked all 30+ cues:
  0.00, 1.02, 2.16, 5.02, 7.18, 9.18, 9.86, 10.68, 12.72, 14.76, 15.46, 16.96, 19.86, 21.94, 23.54,
  25.04, 26.98, 27.72, 28.68, 29.14, 30.96, 33.30, 35.64, 37.78, 39.56, 41.54, 42.54, 43.66, 45.02, 46.46).
- Clip length vs screen time: all 14 clips are longer than their time on screen
  (tightest: C04 9.5 of 10 s, C08 4.52 of 5 s, C01 7.4 of 8 s). No freeze, loop, boomerang or slow-down planned.
- Landing hold: last word 48.50, film ends 51.5 = 3.0 s. Passes the 3.0 s rule on paper.
- All Bible words on screen are KJV word for word (Micah 5:2 parts, Matt 2:5 "In Bethlehem of Judaea").
  No "..." on screen. Scroll text is SVG type, not painted, not animated by a model. Good.
- No adult Jesus, no countable wise men, no round tomb stone, closed scroll in S08, scroll seen from behind in S01. Good guards.

---

## 1. Comic on a phone, or slideshow?  -> NOT PROVEN YET

1. **Panel shapes do not fit the art.** Every still and clip is 9:16, but no multi-panel slot is 9:16.
   Rough sizes on a 1080x1920 page: STACK2 / SCROLLPAGE top row is about 1024 x 1030 (square);
   bottom row about 1024 x 810; TRIPTYCH top rows about 1024 x 470 (a 2.2:1 strip).
   So 8A (baby) and 8B (crosses) show about a quarter of a paid 9:16 clip and never go full screen.
   The plan never says how a 9:16 picture is cropped into each slot.
2. **DIVE is not defined.** A square panel cannot "fill the screen" by scaling. Either it crops away
   about 45% of the width, or the border opens to show the rest of the 9:16 frame. Same problem in reverse
   for 1A (full screen shrinks to a square row). Each of 1A, 5B, 6A, 8C needs two safe compositions. Not specified.
3. **"Camera eases down" is unclear.** If the whole page fits on screen, there is no move. If the camera
   is pushed in on one panel, the other panel is off screen, and that is a slideshow with a pan.
4. **Only 4 of 8 pages are real multi-panel pages** (1 late, 4, 5, 8). Pages 2 and 6 are single pictures,
   3 and 7 are picture + text card. All panels are full-width rows of nearly the same shape. One balloon in the whole film.
   The comic feel rests on paper, borders and page turns. It may work. It needs to be seen moving first.
5. **Hook frame.** Second 0-2 is old men over a scroll with a slow push. It is calm for a first 2 seconds.

## 2. Picture matches words / Bible accuracy  -> MOSTLY GOOD, 6 POINTS

1. **Time slab drops a word.** Narration says "About seven hundred years earlier". Slab says `700 YEARS EARLIER`. Keep "ABOUT".
2. **S04: Micah's window town.** Nothing in Micah puts Bethlehem outside his window (he is from Moresheth, Micah 1:1).
   It is a nice picture idea, but it is invented. Keep it soft and never label that town.
3. **S06 riders "toward a bright star".** Matt 2:2 only says they saw his star. The star going before them is
   Matt 2:9, after Herod. Also no animals are named. Safer: travellers on a road, a star in the sky, no "following" pose.
4. **S09 star standing over the house** sits under "They knew the town", which is before the visitors leave Herod.
   Matt 2:9 is later. Small time squeeze. Acceptable, but say so on purpose.
5. **S05 manger.** The plan admits ox and donkey are tradition. But in the real D frame the ox is a large face
   at Mary's level and the donkey is at Joseph's shoulder. A square crop that holds Joseph's head and the baby
   must be full width, so both animals are fully in. "Crop them out" does not work in this panel shape.
   The straw also glows like a halo around the baby, and the plan says "No halos".
6. **C03 Micah "mouth open mid-word".** An animator will make him talk for 5 s while the narrator (not Micah) speaks. Close the mouth.

Not flagged: Herod's throne, the scribe's raised hand, the finger on the scroll, old white-bearded Micah. Fair picture choices.

## 3. Newcomer / second-language clarity  -> 4 POINTS

1. **No slab for the jump forward.** A newcomer sees old-man-with-scroll, then a baby. Add `ABOUT 700 YEARS LATER` (it is true to the narration).
2. **The gold word gets lost.** It "stays pinned", then becomes a label on 4A, then page 4 turns away at 26.9.
   The gold thread then "draws in from the page edge" at 31.06, from nothing. The proof device is the whole
   point of the series. Say exactly where the gold word sits from 26.9 to 31.0.
3. **Text does not fit its own rules.**
   - Scroll strip `out of thee shall he come forth unto me` is 9 words (rule: max 7) and about 1,100 px wide at 58 px Palatino Bold (room: 900 px). It needs 2 lines, so strip 2 becomes 3 lines (rule: max 2).
   - Caption `The religious experts knew the exact town` is 41 letters, about 1,060 px at 52 px Kalam. It will wrap. Set a letter limit (about 26 a line), not a word limit.
4. **Safe zone clash.** Words must stay in y 200-1540. But captions sit "top-left or bottom-left of their panel":
   top-left of a top panel is about y 30-150 (unsafe), bottom-left of a bottom panel is about y 1800 (unsafe).
   The scroll row runs y 1076-1892, so only the top 57% of the scroll is safe. The bottom-row box on 8C has the same problem.

## 4. Cost vs quality  -> ONE BIG MISS

1. **The first viewer test is after the spend.** Risk 3 says the global-audience panel runs "on the first assembled cut".
   That is after 12 stills + 14 clips are paid. A $0 animatic (locked audio + grey panels + the 2 D frames + all the
   $0 type, scroll, turns) can be built now and tested first. House rule: words and tests before money.
2. **C04 is the only 10 s Kling clip** and it is one eye-lift then a 7 s hold. If the camera dives into the scroll
   for strip 2 (16.96-21.6), 3A needs about 4.5 s, so a 5 s clip does it, and the scroll gets full-screen safe room for bigger text.
3. **Paying for 9:16 where a strip is shown** (8A, 8B). Compose stills for the slot they live in.
4. C02 (2.4 s, empty road) and C09 (2.7 s, houses) are low-headroom shots. Keep as real clips (owner rule), but they are the first to cut if the budget is tight.
5. No price is quoted and each spend needs its own yes. Correct.

## 5. House rules  -> 3 BREAKS OF THE PLAN'S OWN SACRED RULE, 1 WRITING RISK

1. **Riffle cuts into God's words.** RIFFLE forward starts 21.6. "Israel." is spoken 21.32-21.74 and is still inking in.
   The loud riffle lands on the scroll (rule 1.6: never) and 4A lands at 21.6 over it.
2. **Loud entry into the manger.** Rule 1.4: a sacred page is entered by SOFT TURN. Page 4 (baby) is entered by RIFFLE.
3. **Page shake with the baby on screen.** 4B does PANEL LAND with shake while 4A (the child) is on the same page. A page shake moves every panel.
4. **Writing scene.** In the real `D_barabbas_micah.png` the pen tip is already on the scroll. The plan says "the pen never
   touches the scroll". A 10 s animated clip of pen-on-paper is the classic invented-writing case. Lift the pen in the still, or crop the panel above the hands.
5. **Look reference carries a defect.** The raw micah frame has white speed lines in all four corners. If it is the
   look reference on every prompt, the lines can spread to every still. Use the cleaned S04 as the reference.
6. **Veo on glowing content.** C05 is the glowing manger on veo. Only C14 is marked "positive wording". C05 needs it too
   (known glitter risk), or move C05 to Seedance (three faces, calm).
7. Clip >= screen time, no freeze, no boomerang: pass. Check first and last frame of each clip: planned. Good.

---

## Small fixes list

- Slab: `ABOUT 700 YEARS EARLIER`. Add `ABOUT 700 YEARS LATER`.
- Move the forward jump to after 21.74. Gap to "When" (21.94) is only 0.2 s, so use a SOFT TURN, not a riffle, and let the slab ride over 4A's bloom.
- 4B arrives without page shake (panel-only move).
- Captions: top row boxes sit at the panel's bottom-left, bottom row boxes at its top-left. Scroll text in the top half of the scroll row.
- Scroll strip 2 on 3 lines; update the "max 2 lines" rule for scroll cards.
- C03 mouth closed. S06 no "following the star" pose. S05 redrawn for its square slot (no animals, no halo glow), keep the D frame as the look/character ref only.
- If C04 comes back short: let it leave earlier, do not land it later ("named" at 12.72 must stay in sync).

---

VERDICT: REVISE

TOP 3 FIXES

1. **Build a $0 animatic first, and pin the layout.** Locked audio + grey panels + the 2 D frames + all the $0 type.
   Fix in it: crop of each 9:16 picture into its real slot (square rows, 2.2:1 strips), what a DIVE does, caption
   places that obey y 200-1540, scroll lines that fit. Run the blind global-audience panel on the animatic BEFORE any still or clip is paid.
2. **Fix the page 3 -> 4 seam and the sacred breaks.** No riffle over "Israel." (ends 21.74), soft entry to the manger,
   no page shake while the child is on screen, add `ABOUT` to the slab plus an `ABOUT 700 YEARS LATER` slab, and say
   where the gold word lives from 26.9 to 31.0 so the thread joins something the eye can see.
3. **Fix three stills before spend.** S04: pen is on the scroll (writing risk) and its speed lines poison the look
   reference; lift the pen or crop above the hands, use the cleaned frame as the ref, and dive to the scroll so C04 is 5 s not 10 s.
   S05: the square crop cannot lose the ox and donkey and the straw glows like a halo; draw a new S05 for its slot.
   S03: close Micah's mouth.
