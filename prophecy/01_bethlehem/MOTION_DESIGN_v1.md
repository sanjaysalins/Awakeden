# Born in Bethlehem - MOTION DESIGN v1

Film: 1080x1920, 30 fps, 1779 frames (59.3 s). Voice timing is untouched. Frame = `Math.round(s*30)`.
Source of truth for cuts/words: `_remotion/public/bethlehem/film_v2_data.json`, `audio_v2/narration_v2.words.json`.

**Read first - what is measured and what is estimated**
- Word times, cut times and clip lengths are measured (clips: M1 5.04 s, M2 7.04 s, all others 10.04 s).
- Every picture-anchored position below (panel edges, town, galaxy core, tomb door) is an ESTIMATE read off 270 px check frames, about +/-40 px. Each is tagged **[MEASURE]**. The coder must measure them on real frames before building (method in section 5.1).
- I looked at stills, not at the moving clips. Pan speed of each clip is estimated the same way.
- Check frame `film/_chk2/f1030.jpg` shows the Herod page at 34.3 s, but the edl says P1 from 33.4 s. The check frames may be older than the edl. Trust the edl.

Colours: GOLD `#E8A81C`, INK `#141210`, CREAM `#FFEEBE`, PAPER `#FBF8F0`, SEPIA `#2A1A0E`, DAWN `#FFF3D6`.
Easing names: OUT = `Easing.out(Easing.cubic)`, IN = `Easing.in(Easing.cubic)`, INOUT = `Easing.inOut(Easing.cubic)`, SINE = `Easing.inOut(Easing.sin)`, BACK = `Easing.out(Easing.back(1.8))`.

---

## 1. The visual idea: "Hollow steps, gold steps, one gold line"

The film is about who WENT. So the motion has one small grammar, used only where the words are about going:

- **The star mark** (a small gold four-point star) = Bethlehem, the place everyone knew. It lands each time the place is pointed at: the hook ("where"), Micah naming it, and "close by".
- **Footstep dots** = a human journey. **Hollow** dot = a step not taken. **Gold** dot = a step taken.
  - The experts get 7 hollow dots to the star. A short road. The dots never fill. The first one blinks in the silence, waiting.
  - The wise men get 16 gold dots that stream in from the east (screen right), and later they fill the experts' own 7 hollow dots and reach the star. That last gold dot opens like an iris onto Mary and the child: they went, and found Him.
- **One unbroken gold line** = Jesus' journey. Not steps on a road: a single line that comes down out of the stars and stops at the panel edge right above the cross. It is the only solid line in the film.
- The same grammar lives in the lettering: "knew" gets a gold box, the experts' "went" gets an EMPTY box, the wise men's "went" gets the gold box, and "He came to us" gets the gold line as its underline. That line then comes to rest above the series mark.

Everything else (transitions, scroll, counter) is picked beat by beat and kept thin. Sacred shots get only soft fades.

**Sacred windows (machine-check these):** 22.7-25.0, 41.2-43.5 (Mary and child on screen), 46.0-59.3. Inside them: no shake, no scale-pop, no slam, no word pops, nothing drawn on Jesus, no glow on the baby.

---

## 2. Transitions - every cut in the edl

Rule for overlap: a transition window is [cut - a, cut + b] frames. The outgoing clip keeps playing to cut + b (needs spare footage). The incoming clip starts at cut - a (needs an in-point >= a, or it simply starts earlier at clip time 0). The table says which is used. M1 and P3 have NO spare footage, so their cuts use cover-type or pre-roll-only transitions.

| # | Cut (s / frame) | From -> To | Transition | Window (frames) | How it is drawn |
|---|---|---|---|---|---|
| 1 | 4.00 / 120 | P1 -> P2 | **Page riffle BACK** (time jump) | 116-134 (18 f) | 7 opaque paper leaves sweep LEFT -> RIGHT (turning back through a book). Leaf k (0-6) lives frames 116+2k to 122+2k, x from -1080 to +1080, linear. Leaf colours cycle `#F4EAD2 #F1E3C3 #EEDDB6 #EAD6A8 #E6CF9C #EAD6A8 #EEDDB6`, each with a 40 px soft shadow on its trailing edge (`rgba(0,0,0,.25)`) and 6 faint ruled lines (`rgba(90,58,24,.10)`, 3 px). Clip swap happens at frame 120 under the leaves (leaves 0+1 cover the full frame there). No overlap footage needed. |
| 2 | 9.10 / 273 | P2 -> M1 | **Panel zoom-through** | 265-282 (17 f) | Outgoing P2 scales 1.0 -> 1.9 over frames 265-272, IN, transform-origin = centre of P2's top panel (Micah at sunset) **[MEASURE ~ (540, 340)]**. Cream flash overlay `#FFEEBE`: opacity 0 -> 0.85 over 270-272, 0.85 -> 0 over 273-276. Incoming M1 scales 1.12 -> 1.0 over 273-282, OUT. We dive into the small picture of Micah and land in the big one. No overlap needed. |
| 3 | 14.10 / 423 | M1 -> P2 (in 5.55) | **Ink brush wipe, in the pointing direction** | 413-423 (10 f) | Incoming P2 starts at frame 413 (clip time 5.22) and is revealed left -> right behind a wobbly diagonal front. Front x at height y: `lerp(-300, 1500, INOUT(u)) + 0.21*(y-960) + 28*sin(y/90 + 1.7)`. An INK band 140 px wide rides the front (both edges wobbled, second edge uses phase 4.1). Micah points right; the ink follows his finger. Ends exactly on the cut (M1 has no spare footage). |
| 4 | 15.85 / 476 | P2 -> P2 (in 8.0) | **Lamp flare splice** | 472-480 (8 f) | Same page, small jump. 4-frame mix of the two takes over 474-478, under a warm overlay `rgb(255,196,110)`, blend `screen`, opacity 0 -> 0.35 -> 0 (peak at 476, SINE). It lands on the frame the scroll finishes opening and Micah's voice starts: the lamp flares as he speaks. |
| 5 | 17.80 / 534 | P2 -> P3 | **Page riffle FORWARD** (back to the story's "now") | 530-540 (10 f) | Mirror of #1 but short: 3 leaves sweep RIGHT -> LEFT (x +1080 -> -1080), leaf k lives 530+2k to 536+2k. Clip swap at 534 under the leaves. No overlap needed (P2 and P3 have none). The scroll card snaps shut under the first leaf (section 3.4). |
| 6 | 27.80 / 834 | P3 -> P4 | **Webtoon scroll-down** | 825-834 (9 f) | Both pages move up together like one long comic strip: outgoing P3 translateY 0 -> -1920, incoming P4 translateY +1920 -> 0, INOUT, PAPER colour behind. P4 starts at frame 825 from clip time 0 (so P4 runs 0.3 s "ahead" for its whole shot - fine, it has 10 s). P3's last panel is Herod; P4's first panel is Herod: the eye carries straight through. Ends on the cut. |
| 7 | 33.40 / 1002 | P4 -> P1 (in 5.6) | **Page turns BACK to page one** | 997-1007 (10 f) | Incoming P1 slides in from the LEFT, x -1080 -> 0, OUT, with a 40 px shadow on its right edge (`rgba(0,0,0,.35)`). Outgoing P4 drifts x 0 -> +60 and dims to brightness 0.85. P1 pre-rolls from clip time 5.43; P4 plays 0.17 s past its out-point. We flip back to the men from the hook. |
| 8 | 37.40 / 1122 | P1 -> P1 (in 1.5) | **Whip-pan up the page** | 1118-1126 (8 f) | Outgoing: translateY 0 -> +420 and scaleY 1 -> 1.06 over 1118-1121, IN. Swap at 1122. Incoming: translateY -420 -> 0, scaleY 1.06 -> 1 over 1122-1126, OUT. PAPER behind. The camera snaps from the empty road back up to the men who did not take it. No overlap needed. Comes straight after the 1 s silence, so it hits hard. |
| 9 | 40.50 / 1215 | P1 -> M2 | **Route iris** (calm) | 1215-1258; iris 1236-1258 (22 f) | P1 stays on screen past the cut (it has footage) while the wise men's gold fills the 7 dots (section 3.9). On the last dot the picture of Mary and the child opens from the star mark: circle mask centred on the star **[MEASURE ~ (930, 1490)]**, radius 0 -> 1800 px, INOUT, edge feathered 80 px. A thin gold ring (6 px, GOLD) rides the edge only while radius < 220 px, then fades over 4 frames - so no ring ever crosses the child. M2 runs from frame 1215 at clip time 0, hidden until the iris. No shake, no flash. |
| 10 | 43.50 / 1305 | M2 -> P5 | **Nightfall wipe, top to bottom** (calm) | 1299-1323 (24 f) | P5 starts at frame 1299 (clip time 0) and is revealed from the top down: mask `linear-gradient(to bottom, #000 (e-160)px, transparent e px)`, e from -160 to 2080, SINE. Stars first, then the hill, then the tomb. M2 plays on underneath to frame 1323 (it has footage). Heaven arrives from above, slowly. |
| 11 | 51.70 / 1551 | P5 -> M3 | **Dawn bloom from the tomb door** (calm) | 1539-1563 (24 f) | Frames 1539-1551: a DAWN-coloured radial bloom grows from the tomb doorway **[MEASURE ~ (540, 1480)]**: `radial-gradient(circle at cx cy, #FFF3D6 r%, transparent (r+25)%)`, r 0 -> 140, SINE, until the frame is full warm cream. Swap at 1551. Frames 1551-1563: the cream fades 1 -> 0, SINE, over M3. The light in the tomb becomes the morning. Whole-frame fade only - nothing is drawn on Him. No overlap needed. |

Pills, the slab and the scroll sit ABOVE all transitions and do not move with them.

---

## 3. Motion graphics, beat by beat

### 3.0 Shared parts

**Star mark** - four-point star, 52 px tip to tip, fill GOLD, 5 px INK outline, 2 px CREAM outer keyline. Lands: scale 0 -> 1.25 -> 1 over 8 frames (BACK), plus one ink ring (4 px INK stroke, radius 20 -> 70 px, opacity 1 -> 0, 10 frames). Then twinkles: scale 1 <-> 1.08, 40-frame sine loop. Never used in a sacred window.

**Footstep dot** - circle 26 px, 5 px INK stroke, 2 px CREAM outer keyline. Hollow fill `rgba(255,248,230,0.85)`. Gold fill GOLD. Pop-in: scale 0 -> 1.2 -> 1 over 5 frames (BACK). Fill change hollow -> gold: 3-frame colour blend with a scale tick 1 -> 1.25 -> 1.

**The experts' route (used in 3.1, 3.8, 3.9)** - 7 dots + the star on P1's bottom (night road) panel. Our own drawn route, NOT traced over the painted road (the painted road runs below y 1540, under the phone's own buttons). Dot centres, left to right **[MEASURE: slide the whole group in y so the star sits on the lit town]**:
`(170,1524) (275,1508) (380,1516) (485,1500) (590,1512) (695,1498) (800,1506)`, star at `(930,1490)`.
Because the town sits right under the normal pill line, **every pill on a P1 shot uses centre y = 1350 instead of 1440** (ids h1, cb, n1, n2a). It then sits in the night sky above the town. Check the 2-line pill (1268-1432) clears the panel's top border **[MEASURE ~ y 1280]**; if not, nudge to 1356.

### 3.1 Hook, 0.00-4.00 (P1)

| Time (s) | Frame | What |
|---|---|---|
| 0.00-2.46 | 0-74 | Pill h1 (cy 1350). Words POP IN one by one on their word times (hidden until spoken): scale 1.25 -> 1, 4 frames, OUT. Frame 0 already shows "The". |
| 0.88 | 26 | "knew" gets the **gold box** (the existing gold highlight span, alpha 0 -> 1 in 4 frames) plus two short ink tick marks above its top-right corner (2 lines, 18 px long, 5 px INK, 20 deg and 50 deg, draw-on 3 frames). |
| 1.28 | 38 | On "where": the **star mark** lands above the town at (930,1490). |
| 2.46-3.10 | 74-93 | Silence. Nothing new. The star twinkles. |
| 3.10 | 93 | Pill h1 fades out in 3 frames. |
| 3.22 / 3.38 / 3.56 | 97 / 101 / 107 | **"DID THEY GO?"** replaces the plain pill h2. Bangers 140 px, CREAM fill, 9 px `#4a2a12` stroke (same look as the 700 slab), one line, centred x 540, baseline box y 1290-1440 (the sky of the road panel). Each word slams in on its word time: scale 1.6 -> 1 in 4 frames (OUT), rotation -3 deg / +2 deg / -2 deg settling to 0. "GO?" is filled GOLD. |
| 3.56-4.00 | 107-120 | On "go?": the 7 **hollow dots** pop on left to right, one every 2 frames (107, 109 ... 119), walking toward the star. They stay hollow. |
| 3.87 | 116 | The riffle (cut 1) sweeps it all away. The question card, dots and star are removed at frame 120 under the leaves. The question is left open. |

### 3.2 The 700-years jump, 3.87-6.20 (cut 1 + slab)

- Riffle back as in the table (116-134).
- Slab s2 now starts at frame 119 (was 121), z-order above the leaves. Same style and place (Bangers 104 px, top 400). Line 1 is "ABOUT {N} YEARS", line 2 "EARLIER".
- **{N} counts the centuries as the leaves pass:** 100 at frame 119, then +100 every 2 frames, reaching **700 at frame 131** (4.37 s, on the word "hundred"). Each step: the number does a 2-frame scale tick 1.12 -> 1. Use tabular width (wrap the number in a fixed 190 px inline-block) so the line does not jiggle.
- Holds on "ABOUT 700 YEARS / EARLIER" to 6.20 as now (fade last 5 frames).

### 3.3 Micah names the town, 9.10-14.10 (M1)

- 11.34 (frame 340), on "Bethlehem": the **star mark** lands just above the distant town Micah is pointing at **[MEASURE ~ (890, 720)]**, tracked to the clip's camera move. Same frame: "Bethlehem" in pill m3 gets the gold box.
- Star fades out over frames 408-412, before the ink wipe (cut 3). Nothing else on this shot.

### 3.4 The scroll and Micah's own words, 15.50-17.80 (P2)

- 15.50-15.62 (465-469): the rolled scroll (two wooden rollers touching, 80 px wide) rises 60 px into place and fades in, centre (510, 1065).
- 15.62-15.90 (469-477): it unrolls sideways to 800 px, INOUT. It is fully open on the lamp flare (cut 4, frame 476).
- Parchment upgrade: top and bottom edges are a deckled SVG path (edge points every 40 px, +/-5 px from `hash`), fill `linear-gradient(#EFDDB0, #E4CC98)`, alpha 0.94, 3 px `#5C3A18` edge. Rollers get round end knobs (28 px circles, `#5a3a1c`).
- **Scripture face:** the quote is set in IM Fell English roman (`IMFeENrm28P.ttf`), 64 px, line height 74 px, SEPIA. Narrator stays in Kalam. So Bible words look like Bible words.
- Words ink in on the existing `wt` times: each word wipes on left to right in 6 frames (as now) and starts wet-black `#000`, drying to SEPIA over 10 frames.
- "MICAH 5:2" tag: when the scroll is open, slides in 30 px from the right and turns -6 deg -> 0 deg, 6 frames, OUT.
- 17.70 (531): the scroll rolls shut in 5 frames, under the first forward leaf of cut 5.

### 3.5 Mary and Joseph, the birth, 17.80-25.10 (P3)

- Pills only. "Bethlehem" in j2 gets the gold box at 21.62 (frame 649).
- 22.70-25.10 (the birth): pill j3 soft-fades in over 8 frames. **Nothing else. No mark, no glow.**

### 3.6 The wise men come, 25.18-27.80 (P3)

- 16 **gold dots** stream in from the EAST (screen right) along the bottom of the camel panel: centres x = 1010 - 58k (k 0-15), y = 40 px above that panel's bottom border **[MEASURE ~ y 930]**, with a gentle wobble `+/-10*sin(k*1.3)`. Tracked to the pan.
- Dot k pops on at frame `755 + round(2.8*k)` - first at 755 ("Wise"), last at 797 (the word "came" ends at 26.68). They arrive already gold: these men are walking.
- Hold. Fade all dots over frames 819-824, just before the scroll-down (cut 6).
- 16 long gold steps here against 7 short hollow ones later: that is the whole contrast, shown not said.

### 3.7 Herod asks, the scribe answers, 27.80-34.70 (P4)

- 31.16 (935), "where.": a wavy ink underline (5 px INK, 2 waves) draws under the word in 8 frames. Nothing else.
- 32.24 (967): the speech pill pops: scale 0.85 -> 1, 6 frames, BACK. Tags "A SCRIBE" and "MATTHEW 2:5" slide in 20 px from left and right, 6 frames.
- 32.48 (974): "Bethlehem" gets the gold box, and a tiny star (24 px, same drawing as the star mark) stamps on the box's top-right corner.
- 33.40 (1002): when the page turns back (cut 7), the speech tail fades out in 4 frames (the scribe is no longer on screen). The bubble stays to 34.70 so the answer hangs over the experts' page.

### 3.8 "Bethlehem was close by." + the silence, 34.80-37.40 (P1, bottom of page)

- 34.80 (1044), "Bethlehem": gold box on the word; the **star mark** lands on the town.
- 35.66 (1070), "close": the 7 **hollow dots** pop on, one every 2 frames (1070-1082), done as "by." is spoken. Seven steps. That is all it was.
- 36.32-37.40 (1090-1122), the 1 s silence: only the FIRST dot (far left) blinks, opacity 1 -> 0.35 -> 1, 20-frame sine loop. A cursor waiting for a first step. Nobody takes it.
- Optional, **needs the owner's yes because it adds a fact that is not in the script:** a small gold tag "ABOUT 9 KM" under the middle dot (Kalam 28 px chip style) from 35.94 to 37.30. Off by default.

### 3.9 "never ... went" against "went", 37.40-41.93 (P1 top of page, then M2)

- After the whip-pan (cut 8) the route and star are re-drawn at the road panel's new place **[MEASURE]**, already in their hollow state. No re-pop.
- 37.88 (1136), "never": DOUBLE ink underline (two strokes, 5 px INK, second one 9 px lower and 2 frames later, each draws on in 6 frames).
- 39.06 (1172), "went.": the word gets an **EMPTY box** - the same rounded shape as the gold box but outline only (4 px INK, hand-wobbled, no fill), drawn on in 6 frames. Same frame: the first hollow dot does one slow pulse (scale 1 -> 1.3 -> 1, 10 frames) and stays hollow.
- 40.52 (1216): pill n2a "The wise men went," (cy 1350, still on P1).
- Frames 1216, 1219, 1222, 1225, 1228, 1231, 1234: the 7 dots turn **gold**, one by one, left to right. The last lands on "went," (41.14).
- 41.14 (1234): "went," gets the **gold box**. Empty box above, gold box here: the contrast in one look.
- 41.20-41.93 (1236-1258): the route iris (cut 9) opens from the star onto Mary and the child. Dots, star and pill n2a fade out over 1236-1242.
- 41.93-43.40 (1258-1302): pill n2b "and found the child." (cy 1440, sacred style: 8-frame soft fade, no pops). Nothing else on this shot.

Data change: split item n2 into n2a (40.52-41.93, line "The wise men went,") and n2b (41.93-43.40, line "and found the child."). The long spoken "and" (41.52-42.42) covers the hand-over.

### 3.10 "much farther" and the descent, 43.30-48.00 (P5)

- 43.30-44.10: nightfall wipe (cut 10). Stars first.
- 43.52: pill l1, soft fade. 44.88-45.50 (1346-1365): the word "farther." slowly spreads, letter-spacing 0 -> 5 px, SINE. Gentle, and it means what it says.
- 46.04-47.24 (1381-1417), "He came down from heaven.": **the one gold line.** It starts at the galaxy's bright core and comes down through the star panel in a soft S-curve, ending 14 px above that panel's bottom ink border, directly above the middle cross. It never enters the cross panel.
  - Path in the star panel's own coordinates (panel about 1040 x 560 **[MEASURE]**): `M 545 150 C 600 260, 470 380, 525 546`.
  - Main stroke 5 px GOLD, round caps. Under it a 14 px GOLD stroke at 0.25 opacity (soft edge). Draw-on with `strokeDashoffset`, SINE, frames 1381-1417.
  - The tip carries a 14 px gold dot. No star at the tip (keep the star for Bethlehem only).
  - The whole group is tracked to the panel as the clip pans. Estimated panel bottom edge: y ~ 500 at frame 1381, ~ 420 at frame 1417 **[MEASURE]**. The top of the line will be in the top 200 px of the screen - that is fine, it is not text.
  - Fade the whole line out over frames 1420-1436. It is gone before "He died for our sins." (48.10 = frame 1443).
- 48.00-51.30: **nothing added.** Pills l3 and l4 soft-fade only. The crosses and the tomb are left alone.

### 3.11 The risen Jesus and the ending card, 51.30-59.30 (M3)

- 51.30-52.10: dawn bloom (cut 11).
- 52.50 (1575): pill p10 soft-fades in (10 frames) with line 1 only, "Before anyone went to Him,". The pill is already 2 lines tall; line 1 sits centred.
- 55.00-55.20 (1650-1656): line 1 eases up 31 px (SINE) and line 2 "He came to us." fades in (8 frames from 1653). Hidden until spoken, so the last line lands.
- 55.18-56.00 (1655-1680): **the gold line returns as the underline** of "He came to us." - 6 px GOLD with a 2 px INK shadow line under it, drawn left to right across the full width of line 2, SINE. Same line as the descent: it has arrived.
- 56.00-57.00: silent hold. Nothing moves except the clip.
- 57.00-57.40 (1710-1722): the pill shrinks to a small pill (600 x 84, same grey fill and edge, centre (510, 1440)), the two lines fade out, and the gold underline slides to rest as a 240 px rule centred at y 1418.
- 57.40-57.90 (1722-1737): **"PROMISED, THEN KEPT"** fades in inside the small pill: Fraunces, 36 px, uppercase, letter-spacing 7 px, INK, centred at y 1448.
- 57.90-59.30: full hold to the last frame. No call to action. No fade to black.
- Placement note: this is the same spot the pills already use on this shot (over the lower robe). There is no free space on M3 above y 1540 that is not on Him or His light, so the mark stays where the owner already accepted lettering, inside a pill, small.

---

## 4. Pills and lettering

Keep the translucent grey pill exactly as it is (the owner picked it in the earlier bake-off): 880 px wide, Kalam Bold 54 px, 62 px lines, INK. Changes:

1. **Read-along fill (all non-sacred pills).** All words are laid out in their final place from the first frame (no reflow). A word not yet spoken shows at 38% opacity. On its word time (1 frame early) it goes to 100% in 2 frames with a scale tick 1.07 -> 1 over 5 frames (OUT). No vertical movement, so the line stays easy to read. A non-native reader can still read ahead; the eye is led by the voice.
2. **Hook pill h1** is the one exception: words are hidden until spoken, then pop (3.1).
3. **Sacred pills** (j3, n2b, l1-l4, p10): no read-along, no pops. The whole pill soft-fades in over 8-10 frames, all words at full ink.
4. **Key-word marks** - one per pill at most:

| Pill | Word | Time (s) | Mark |
|---|---|---|---|
| h1 | knew | 0.88 | gold box + 2 ink ticks |
| (card) | GO? | 3.56 | gold Bangers word |
| s2 | 700 | 3.97-4.37 | century counter |
| m3 | Bethlehem | 11.34 | gold box |
| j2 | Bethlehem | 21.62 | gold box |
| w2 | where. | 31.16 | wavy ink underline |
| sp | Bethlehem | 32.48 | gold box + tiny star |
| cb | Bethlehem | 34.80 | gold box |
| n1 | never / went. | 37.88 / 39.06 | double underline / EMPTY box |
| n2a | went, | 41.14 | gold box |
| l1 | farther. | 44.88 | letters slowly spread 0 -> 5 px |
| p10 | He came to us. | 55.18 | gold line underline |

   Gold is kept for three things only: Bethlehem, "knew", and going. Nothing else turns gold.
5. **Pill y:** 1440 as now, except 1350 on every P1 shot (h1, cb, n1, n2a) so the town and route show.
6. **Minimum on-screen time:** no text block is up for less than 0.8 s; the shortest is "DID THEY GO?" (3.22 to about 3.97), three short words that appear as they are spoken.
7. Scroll quote in IM Fell English 64 px (3.4). Tags keep the existing gold chip style.

---

## 5. Remotion build notes

### 5.1 Measure first (30 minutes, $0)
Pull stills from the CURRENT v2 build at these film frames with ffmpeg and read off pixel positions: 38, 107, 265, 340, 476, 760, 800, 1044, 1090, 1130, 1234, 1381, 1417, 1545. Put them in a new `tracks` block in `film_v2_data.json`:
`"tracks": { "p1_road_a": [[38, y0],[119, y1]], ... }` = two keyframes per shot, linear between. Art-anchored groups read their offset from a track. If cut 6 or cut 10 pre-roll is built, re-measure P4 and P5 afterwards (they shift by 0.3 s / 0.2 s).

### 5.2 Components (one file `BethlehemMotion.tsx`, all pure functions of `f`)
- `useTrack(name, f)` -> `{dx, dy}` linear interpolate, clamped.
- `Transitions` - replaces the plain `Sequence` map. Each clip is a `Sequence` whose `from`/`durationInFrames` are widened by the a/b values in section 2 (`startFrom` reduced by a when the in-point allows). Each clip is wrapped in a div that takes `transform`, `filter`, `clipPath` or `maskImage` from a per-cut function. `OffthreadVideo` renders an `<img>`, so CSS `mask-image` and `clip-path` work on its wrapper.
- `Leaves({start, count, dir})` - cuts 1 and 5. Absolutely placed opaque divs.
- `InkWipe` - cut 3. Build one SVG polygon per frame from the front formula (sample y every 60 px); use it as `clipPath: path(...)` on the incoming wrapper, and draw the ink band as a filled SVG path on top.
- `Iris` - cut 9. `maskImage: radial-gradient(circle at Xpx Ypx, #000 (r-80)px, transparent r px)` on the M2 wrapper. Gold ring is a separate SVG circle.
- `NightWipe`, `DawnBloom`, `LampFlare` - plain overlay divs / mask gradients (cuts 10, 11, 4).
- `StarMark`, `RouteDots({pts, popAt[], goldAt[], blinkFirst})`, `DescentLine` - one SVG layer, 1080x1920, placed above transitions and below lettering. Draw-on = `pathLength={1}` + `strokeDasharray={1}` + `strokeDashoffset={1-p}` (already used for the underline in `BethlehemAnimatic.tsx`).
- `KPill` - copy of `Pill` with per-word spans (`display:inline-block`), word times from `narration_v2.words.json` matched in order to each pill's words, plus the mark types `gold`, `emptyBox`, `underline`, `underline2`, `wavy`, `track`. Reuse `measure()` for box and underline geometry and `wobblePath()` for the empty box.
- `QuestionCard`, `CounterSlab` (extends `Slab`), `ScrollCard2` (extends `ScrollCard`), `EndMark`.

### 5.3 Fonts
Add to the existing `FontFace` loader: `IMFeENrm28P.ttf` (scroll) and `Fraunces.ttf` (end mark). Keep the `delayRender` guard.

### 5.4 Layer order (bottom to top)
clips with transition wrappers -> full-frame transition overlays (leaves, flare, bloom, ink band) -> star / dots / gold line -> slab, question card, scroll -> pills -> hud.
Exception: during cuts 1 and 5 the star, dots and question card sit BELOW the leaves so the leaves wipe them away.

### 5.5 Rules for the coder
- No `Math.random`, no `Date`. Use the existing `hash(i)` for every wobble.
- Clamp every `interpolate`.
- Pre-mount the incoming clip (`premountFor={30}`) so there is no decode hitch at a transition.
- Two videos overlap only inside transition windows (max 24 frames), so render cost stays low.
- Add a `sacred` check to the machine checks: fail if any element with a pop / shake / scale > 1.02 is active inside 22.7-25.0, 41.2-43.5 or 46.0-59.3 (the gold line and its fade are allowed: draw-on only, no scale).
- Add a safe-zone check: all TEXT boxes inside x 60-1020, y 200-1540.
- Eye-check by rendering stills at frames 26, 38, 110, 119, 125, 131, 270, 273, 340, 418, 476, 534, 780, 830, 1002, 1082, 1100, 1122, 1172, 1234, 1246, 1258, 1311, 1400, 1417, 1545, 1551, 1670, 1740. Look at each one; do not trust the build passing.

### 5.6 If time is short, build in this order
1. Pills: read-along + key-word marks + hook card (biggest gain, lowest risk).
2. The 11 transitions.
3. Star mark + experts' route + route iris (the spine).
4. Wise men's 16 dots, gold line descent, ending card.

### 5.7 Three things for the owner to say yes or no to
1. The gold line at 46.0-47.9 is inside the cross-and-tomb window. It stays in the star panel and stops above the cross. Keep it? (My pick: yes.)
2. The series mark at the end sits where the pills sit, over the lower robe, inside a small pill. OK? (My pick: yes.)
3. "ABOUT 9 KM" tag on "close by" - a new fact on screen, not in the script. (My pick: leave it off.)
