# The Second Fire (Folk Print) — Motion layer v1 (design spec, build-ready)

Comp: 1080x1920, 30 fps, 2637 frames (87.9 s). Base = the 17 clips, 1.0x, audio untouched (mux from `SECOND_FIRE_SCORED_v2.mp4`).
All frames are ABSOLUTE comp frames, `f = round(seconds x 30)`. Word frames come from `score_sfx_panel/_timed_lines.txt`.

Cut frames (slot starts): s01 0 | s02 99 | s03 240 | s04 396 | s05 471 | s06 567 | s07 711 | s08 867 | s09 1023 | s10 1101 |
s11 1206 | s12 1434 | s13 1596 | s14 1806 | s15 2034 | s16 2256 | s17 2409 | end 2637.

**Where the positions come from.** Read off the full stills (`stills_full/sNN.png`, shown 1116x2000; comp = shown x 0.968,
y minus 8) for s02, s07, s10, s11, s12, s13, s16, s17. The other 9 shots were read off the small sheet (300 px cells), so
they are good to about +-25 px. The clips also move. Every position must be re-checked on real clip frames (Risk 1).

**Note on the brief.** s11 is split TOP (night) / BOTTOM (sunrise), not left / right. This spec follows the real still.

**What I took from the two earlier jobs.**
- Mary & Martha v2-v4 worked because every doodle was one of the picture's own things, in the picture's own colours, big,
  popping with a back-ease, then swaying. Same rule here.
- Zacchaeus read "sloppy" because: every mark re-wobbled every 3 frames (boil), cuts were hidden under black scribble that
  covered the whole frame, random jitter on everything, arrows and dashed sight-lines (a diagram on top of the art), caption
  slabs, hard 0/100 pops. **None of that here:** no boil, no random numbers, no arrows, no lines pointing at people, no
  words, nothing foreign ever covers the frame.

---

## 1. The idea in 3 lines

1. **The print keeps printing.** Only the art's own shapes are added, as flat ink with riso grain: sparks, stars, sun rays,
   waves, flowers, gulls, fish, steam. Big and full, in sky, sea, sand and edges.
2. **Night sparks go cold. Day sparks stay lit.** At the first fire every spark rises and cools into a teal star. At the
   second fire the sparks stay orange. The same "fire signature" plays 3 times, on the 3 fire sounds (3 s, 37 s, 80 s).
3. **Three coals count the story.** Three flames go out one by one for the three no's. Three cold coals wait by the second
   fire. They light one, two, three on "Three times, yes" and rest under the bread on the last frame.

---

## 2. Doodle vocabulary (10 motifs)

Start colours below are read by eye. **Eyedrop the real clip frames and replace them before building.**

| Name | Hex |
|---|---|
| ink (outline) | `#1E2A2E` |
| night teal / mid teal / sea teal | `#173F45` / `#2E6F73` / `#3F8F8C` |
| star teal (pale) | `#9FD3C7` |
| burnt orange / coral / mustard | `#D9542B` / `#EF6A4A` / `#EDAE3B` |
| cream | `#F7E7C4` |
| rust / coal dark | `#B5522B` / `#2A2320` |
| fish grey / steam tan | `#8FB3B0` / `#C9A98C` |

**Print look for every doodle (one shared SVG filter `riso`, STATIC, fixed seed):** `feTurbulence baseFrequency 0.9, seed 9`
-> colour matrix to make about 10% pin-holes -> `feComposite in`. Flat fills, opacity 1.0 (no see-through, no glow, no blur,
no shadow, no gradient). Outlined motifs: outline drawn 2 px right and 2 px up from the fill (riso mis-register).
**Motion rules:** pop = scale 0 -> 1 over 9 frames, `Easing.out(Easing.back(1.8))`. Sway = sine, period 70-90 frames,
phase = `x` position (deterministic). Nothing boils. Nothing uses `Math.random`. Doodles are children of their shot's clip
layer, so transitions mask them with the picture.

| # | Motif | Shape | Colours / stroke | How it moves |
|---|---|---|---|---|
| M1 | **Spark** | Teardrop flame dab, 3 flat layers (copy s02's own flame). 22-60 px tall. | burnt orange / mustard / cream core. No outline. | Rises on a fixed S path, tilts +-8 deg with the path. |
| M2 | **Count coal** | Dark oval coal 70x34 px with a flame 90 px tall on it. Three states: LIT (flame), OUT (no flame, teal ash dot 20 px + one small smoke curl), COLD (coal only, teal cracks). | coal `#2A2320`, ink outline 3 px; flame as M1; ash `#2E6F73`; cracks orange (lit) or `#2E6F73` (cold). | Light: flame grows bottom -> top in 8 frames, back-ease, then sways. Go out: flame shrinks to 0 in 6 frames, smoke curl draws 12 frames and drifts up 0.4 px/frame for 30 frames, then gone. |
| M3 | **Folk star** | 4-point star like the art's own. 30-70 px. | star teal, or cream. No outline. | Twinkle: scale 0.85-1, period 60. Night shots only. |
| M4 | **Ray stitches** | Dotted lines running out from the shot's sun. Dot r 7, gap 34 px. | cream on orange skies; mustard on cream. | Draw outward (dots pop in order, 1 dot per frame), then crawl outward 12 px/s (dash offset). Day shots only. |
| M5 | **Wave scallops** | A row of joined half-circle arcs, 60 px wide each. | stroke 5 px, cream by day, star teal by night. | Scroll sideways 20 px/s, rows alternate direction. Clip each row to its sea box. |
| M6 | **Woven band** | Strip 44 px tall: mid-teal band, mustard zigzag (period 44 px), one coral dot in each V. Copied from Jesus's mantle hem. | mid teal / mustard / coral, ink edge lines 3 px. | Draws on left -> right with a clip rect. Used once (s11). |
| M7 | **Folk flower + spike** | 6-petal daisy (r 26-40) on a thin stem with 2 leaves; spiky agave fan (5-7 blades, 160-260 px). Copy the art's bottom-edge plants. | petals coral / mustard / cream, centre mid teal, stem mid teal, ink outline 3 px. Spikes `#1C3B40`, mustard or coral. | Stem draws 8 frames, flower pops 9 frames, sways +-4 deg. Day shots. Night shots: dark teal spikes only, no flowers. |
| M8 | **Gull** | Two shapes from the art: small "v" tick (ink stroke 4 px, 34 px wide) and white gull (cream body, ink wing tips, 70 px). | ink / cream. | Flies a fixed arc, wings flap (scaleY 0.4-1, 10-frame cycle), bobs 6 px. |
| M9 | **Fish** | The art's fish: almond body 110 px, forked tail, 4 scale ticks, dot eye. | fish grey, ink outline 3 px, cream belly line. | Leaps one arc out of the sea (140 px high, 24 frames), rotates along the arc, with 3 cream drop dabs. |
| M10 | **Steam curl** | The art's own curl (s10, s13): a wavy line ending in a spiral. 180-260 px tall. | steam tan, stroke 7 px, round caps. | Draws upward 20 frames, then drifts up 0.35 px/frame and thins to 50%. |

**Fire signature (used 3 times, section 5):** ember-iris transition in + **tongue ring** (12 M1 dabs set around the fire's
rim, pulse scale 1 -> 1.15 -> 1 over 12 frames) + a **spark column** rising from the flame.

**Keep-out rule (hard):** before placing anything, draw a box round every face (+40 px) and round all of Jesus (+30 px).
No doodle pixel may enter. Boxes for the 8 closely read shots are given below. For the other shots, make them from the clip.

---

## 3. Per shot

"Spark flight" = one M1 flies once from A to B over the frames given, no looping. "Low sparks" = 6 small M1 (22 px)
looping inside a box above the flame, life 30 frames, staggered 5 frames (deterministic phase `i/6`).

### s01 — f0-99 — "Is there one night you can't stop thinking about?" (Peter close, night)
Keep-out: face x 330-750, y 560-1090.
- **Sparks, already flying on frame 0** (hook). 8 flights from below the bottom edge. Left lane x 40-250, right lane x 830-1040.
  Launch frames -40, -28, -16, -4, 8, 20, 32, 44 (alternate left/right). Each flight 70 frames, from y 1960 to its star spot.
  Below y 1350 keep them at x < 80 or x > 1000 (his arms). Size 30 -> 46 px.
- **They cool into stars.** In the last 20 frames of each flight the colour goes burnt orange -> star teal and the shape
  cross-fades M1 -> M3. Star spots: (130,110) (420,200) (610,80) (950,340) (300,330) (700,260) (60,470) (1010,520).
  The moon is near (864,160); keep 90 px away.
- Bottom corners: 2 dark teal spikes (M7, night), 200 px, at (40,1920) and (1040,1920), already there on frame 0, sway only.

### s02 — f99-240 — "The night Jesus was arrested, His friend Peter stood by a fire." (courtyard)
Brazier centre (537,1318), flame top y 1230. Keep-out: all six faces; Peter's face is near (620,978).
- Fire signature #1 (section 5): tongue ring rx 150, ry 62 round the brazier, pulse f99-111.
- **Spark column, 8 flights**, launch f112 + 12i, each 50 frames. Path: (537,1235) straight up the gap between the two
  men (x 525-550, size 22 px while y > 930), then fan out and grow to 44 px. Cool to stars at:
  (120,120) (420,150) (610,90) (760,200) (480,330) (930,110) (140,420) (680,420). Art moon near (252,300): keep 90 px away.
- Low sparks in box x 490-590, y 1150-1240.
- **Three count coals appear LIT** on "by a fire" at f198, f205, f212: (420,1500) (537,1530) (654,1500), on the flagstones
  in front of the brazier, between the two front men's feet.
- Bottom-left: 2 dark teal spikes at (60,1920) and (230,1920), 220 px, grow f104-116.

### s03 — f240-396 — "People asked if he was one of His followers. / I am not."
Brazier near (540,1369). Girl's face near (144,907), Peter's near (774,889) (sheet read; re-check).
- Low sparks over the brazier. 4 spark flights up to stars at (200,110) (470,230) (660,90) (380,400), launch f250 + 20i.
- Count coals LIT from frame 240 at (430,1560) (540,1590) (650,1560).
- **"I am not." (f350-367): coal 1 (left) goes OUT at f367.** Flame shrinks, teal ash, smoke curl.
- Nothing else. The pointing girl and his turned face carry the shot.

### s04 — f396-471 — "Three times, he said no." (rooster, Peter walking away)
Brazier near (540,1369), rooster near (342,1565).
- Count coals at (560,1640) (670,1660) (780,1640), right of the rooster. Coal 1 already OUT. **Coal 2 OUT at f418,
  coal 3 OUT at f440** (on "no").
- From f443: low sparks stop. The last sparks in the air cool to stars at (150,140) (520,90) (820,260). The yard is cold.
- 3 stars (M3, cream, 40 px) step DOWN the sky, popping at f401, f412, f423: (700,120) (760,230) (820,340). Three falling
  notes, drawn once. They stay.

### s05 — f471-567 — "Jesus died. / He rose from the dead." (empty tomb, first light)
Sun near (342,640), tomb door near (790,1067).
- **f479-511: nothing moves.** "Jesus died" gets a still picture.
- "He rose" (f512): **ray stitches** from the sun, 9 rays, angles 190-350 deg (up and sideways), r 170 -> 760, drawn f512-540.
- 2 gulls (M8 tick) lift off from near (600,560) to top-right, f520-567.
- Flowers pop along the path and bottom, on "from the dead": f526 (160,1700), f531 (360,1790), f536 (560,1740),
  f541 (760,1810), f546 (930,1720). Nothing in or round the doorway (keep-out x 680-900, y 930-1200).

### s06 — f567-711 — "Peter went back to fishing. / All night, nothing." (night sea)
Boat near (648,1173). Men's faces x 530-1010, y 850-1070.
- Wave scallops, star teal: rows at y 1580, 1690, 1800 (full width); short rows x 0-470 at y 860, 980, 1100, 1220, 1340.
- 6 stars twinkle: (110,90) (400,250) (560,110) (90,420) (330,470) (640,360). Art moon near (252,178): keep 90 px away.
- **"All night, nothing." (f638-686): NO fish, on purpose.** Three ripple rings where the net meets the water (700,1500):
  ellipses growing rx 30 -> 150, ry 10 -> 50 over 24 frames, stroke 4 px star teal, fading. Start f650, f662, f674.

### s07 — f711-867 — "At sunrise, Jesus stands on the shore. / He tells them where to throw the net."
Sun (542,408), r about 190. **Keep-out (Jesus): x 100-590, y 700-1600.** Boat near (598,765).
- **Ray stitches:** 11 rays, angles 200-340 deg, r 230 -> 900, cream. Draw f717-745 (straight out of the ray wipe).
- 3 gulls (M8 white) cross on one arc (-40,560) -> (540,300) -> (1120,470): f730-800, f750-820, f775-845.
- Wave scallops, cream: y 660 (x 620-900), y 880 (x 640-900), y 940 (x 620-940). Nothing left of x 600.
- Flowers along the bottom: f722 (170,1760), f728 (330,1830), f734 (520,1790), f740 (700,1850), f746 (880,1770), f752 (1010,1840).
- "where to throw the net" (f804-849): three ripple rings on the far (right) side of the boat at (720,800), cream,
  start f822, f832, f842. No line or arrow from His hand.

### s08 — f867-1023 — "It fills with fish. / A friend cries, 'It is the Lord.'"
Net near (900,1670). Sun near (576,640). Faces: friend near (504,889), Peter near (252,1067), others on the boat.
- **Fish burst** on "It fills with fish": 7 M9 leaps from the water round the net, box x 700-1060, y 1350-1850.
  Start f876, 882, 888, 894, 900, 906, 912 at x 720, 980, 800, 1040, 880, 760, 940. After the first arc each fish repeats
  a smaller arc (70 px) every 45 frames.
- Wave scallops, cream, x 700-1060 at y 980, 1080, 1180.
- 4 gulls (M8 white) circle top-right on one ellipse, centre (850,330), rx 170, ry 80, 90-frame loop.
- "It is the Lord" (f935-999): ray stitches from the sun, 9 rays, 190-350 deg, r 200 -> 800, draw f960-985.

### s09 — f1023-1101 — "Peter jumps into the sea to reach Him."
Peter's face near (468,658). Splash near (540,1173). **Keep-out circle r 130 at (774,587): tiny Jesus on the shore.**
- **Splash crown** at (540,1230): 3 scalloped arcs, r 140 / 220 / 300, cream, stroke 8 px, pop f1030, f1034, f1038
  (back-ease); 8 cream drop dabs fly out 160 px and fall, f1032-1060.
- 2 fish leap: (120,1320) at f1040, (930,1400) at f1052.
- Wave scallops, cream: y 1430, y 1530.
- **First sight of the second fire:** one tiny spark (22 px) flickering on the art's tiny shore fire near (864,625),
  outside the keep-out circle. Scale 0.8-1.1, period 14. Nothing else near the shore.

### s10 — f1101-1206 — "On the beach: 'a fire of coals.'" (fire close-up)
Fire ring centre (542,1125), about rx 475, ry 245. See section 5 (fire signature #2).
- 3 extra steam curls (M10) beside the art's own: start f1112 (430,880), f1124 (640,860), f1136 (540,820). Each 220 px tall.
- Wave scallops, cream, top-left sea: y 130 (x 250-700), y 250 (x 300-560). Keep 80 px off the heron (145,312).
- Flowers at the bottom: f1108 (140,1790), f1114 (400,1850), f1120 (700,1800), f1126 (940,1860).

### s11 — f1206-1434 — "In the whole Bible, those exact words appear only twice. / Here, and the night Peter said no."
Top fire (537,757). Bottom fire (542,1560), ring rx 280, ry 135. Split line y 960. See section 5.

### s12 — f1434-1596 — "Come and dine. / Come and eat. / Jesus hands them bread and fish."
Sun (542,505). **Keep-out (Jesus + bread arm): x 230-700, y 990-1720.** Disciples' faces x 530-1080, y 900-1300.
Fire (581,1638), flame top y 1512.
- Ray stitches on "Come and dine" (f1441-1463): 8 rays laid along the sky's own stripe edges, r 180 -> 760,
  draw f1441-1466, cream. (Lay them on real stripe edges, measured from the clip.)
- Gulls: 2 M8 ticks cross the sky left -> right, y 300-420, f1450-1560.
- Wave scallops, cream, in the sea left of Him: y 870 (x 180-420), y 1110 (x 60-300), y 1175 (x 20-280). Heron near (58,940): keep 70 px off.
- Flowers on "Come and eat" (f1480-1495): f1480 (90,1860), f1485 (250,1890), f1490 (560,1870), f1495 (900,1830), f1500 (1010,1890).
- Low sparks only inside x 530-640, y 1480-1620 (the flame's own space). **No spark column here:** it would cross His robe.

### s13 — f1596-1806 — "After the meal, He asks Peter three times: / Lovest thou me? / Do you love me?"
**Keep-out (Jesus): x 150-580, y 960-1640.** Peter's face near (774,1094). Fire (542,1636), ring x 358-726, y 1510-1694.
- **Three count coals appear COLD** on "three times" at f1660, f1667, f1674: (400,1790) (542,1815) (684,1790), on the sand
  below the ring. They do not light in this shot. The question is still open.
- One new steam curl per ask, next to the art's own curl at (532,1452): f1712 at (470,1500), f1759 at (600,1490).
  Height 180 px. They stay in the gap x 440-640 between the two men.
- Ray stitches from the low sun (223,620): 7 rays, 250-350 deg, r 200 -> 700, draw f1602-1630, then crawl.
- 2 gulls drift, top sky. Wave scallops: y 760 (x 60-380), y 900 (x 160-400).
- Quiet shot. No pops after f1759 except the steam.

### s14 — f1806-2034 — "The third time, Peter is sad. / Lord, thou knowest all things; thou knowest that I love thee."
Peter close, day. **This shot mirrors s01.** Keep-out: face and hand, x 250-830, y 520-1500.
- f1806-1973: only 2 small gull ticks in the top sky and 2 side spikes swaying at (30,1920) and (1050,1920) (mustard, coral).
  Leave his face alone while he is sad.
- **"thou knowest that I love thee" (f1974-2023): 8 sparks rise up the same two side lanes as s01** (left x 40-200, right
  x 880-1040; below y 1350 keep x < 80 or x > 1000). Launch f1974 + 8i, flight 70 frames. **They do NOT cool.** They stay
  orange and settle, swaying, in the sky at: (120,140) (400,90) (640,180) (940,120) (250,330) (830,360) (60,480) (1000,500).
  Same lanes, same count as the cold night: now they stay lit.

### s15 — f2034-2256 — "You know everything. You know I love you. / Feed my sheep. / Take care of my people."
**Keep-out (Jesus, Peter, the hand on the shoulder): x 80-640, y 930-1560.** Sheep on the hill x 612-1044, y 1030-1316.
- Ray stitches from the sun near (468,462): 9 rays, 200-340 deg, draw f2040-2068.
- **"Feed my sheep" (f2149-2181): the hill blooms.** 7 flowers pop under the sheep, never on a sheep:
  f2150 (640,1360), f2155 (730,1400), f2160 (820,1370), f2165 (910,1410), f2170 (1000,1380), f2175 (780,1460), f2180 (960,1470).
- "Take care of my people" (f2200-2230): 5 more along the bottom: f2202 (120,1800), f2208 (330,1860), f2214 (560,1820),
  f2220 (790,1870), f2226 (980,1810).
- 2 gulls, top sky. No sparks (no fire in the shot).

### s16 — f2256-2409 — "Three times, no, that night. / Three times, yes, at the second fire."
**Keep-out (Jesus + arm): x 230-720, y 990-1720.** Peter's face near (745,1140). Fire (581,1638), flame top y 1512.
- **The count pays off.** Three count coals on the sand under the fire ring: (455,1800) (581,1822) (707,1800).
  - "Three times, no" (f2260-2310): they pop in COLD, teal cracks, at f2262, f2272, f2282.
  - "Three times, yes" (f2322-2384): they LIGHT left to right at **f2330, f2344, f2358**. If the score's three rising
    notes sit within 10 frames of these, snap each light to its note.
  - "at the second fire" (f2360-2384): tongue ring (rx 135, ry 60) round the fire pulses once, f2366-2378.
- Small art flowers sit near (430,1812) and (726,1745): nudge the coals up to 30 px if they collide.
- Ray stitches along the sky's stripe edges from (542,505), already drawn on frame 2256, crawling. 2 gulls.
- Low sparks only inside x 530-640, y 1480-1620.

### s17 — f2409-2637 — "And before Jesus asked Peter to feed anyone, Jesus fed Peter." (+3 s hold)
**Keep-out: Jesus x 540-1080, y 0-1330. Peter's face x 60-560, y 250-800. All four hands and the bread x 250-830, y 820-1300.**
Fire ring centre (542,1640), rx 455, ry 215. See section 5 (fire signature #3).

---

## 4. The 16 transitions

Three types + hard cuts. A transition is a MASK on the incoming clip (as `bloomMask` / `curtainMask` in `MaryMarthaV4.tsx`),
plus a thin printed edge drawn on top. Window = `[cut - a, cut + b]`. The outgoing clip plays `b` frames past its slot
(it must be that much longer). The incoming clip starts at `cut - a`. Both clips keep playing. No freeze, no speed change.

**A. Ray wipe (into daylight).** 16 wedges of 22.5 deg round the incoming shot's sun point. With `p` (0 -> 1,
`Easing.inOut(Easing.sin)`), every wedge opens from its clockwise edge to `22.5 x p` deg, like a paper pinwheel. Just ahead
of each opening sits a flat colour wedge spanning `22.5 x p` to `22.5 x min(1, p + 0.35)`, colours cycling coral / mustard /
mid teal (the s12 sky), with the `riso` grain. The whole wheel turns +6 deg during the move. Wedge radius 2400.

**B. Wave wipe (into the sea).** A front rises from the bottom: `y(x) = Y + 28 sin(2 pi x / 270 + ph)`, `Y` from 1980 to
-120, `Easing.inOut(Easing.cubic)`. Above the front: a cream scallop line (M5, stroke 10 px). Below it: a 70 px band, then
a 50 px band, then the new picture. Each band has its own `ph` and slides sideways 8 px/frame. Night colours for 5->6
(band `#2E6F73`, band `#173F45`, foam star teal). Day colours for 8->9 (band `#3F8F8C`, band `#2E6F73`, foam cream).

**C. Ember iris (fire to fire; only on the 3 fire sounds).** A circle opens from the incoming shot's fire, R 0 -> 2100,
14 frames, `Easing.out(Easing.cubic)`. Edge shape `r = R (1 + 0.07 sin(16 theta))` (16 flame lobes, turning 0.5 deg/frame).
Three flat edge strokes: burnt orange 26 px at R, mustard 14 px at R-20, cream 6 px at R-34. Ten M1 sparks ride 40 px
ahead of the edge. Edge strokes fade out once R > 1100.

| Cut | Type | Window (frames) | Origin / what moves | Why |
|---|---|---|---|---|
| 1->2 (f99) | **C ember iris** | 93-107 | From the brazier (537,1318). | Fire sound no. 1. "The night" starts f102, the yard is open by then. |
| 2->3 (f240) | HARD | - | - | A question is thrown at him. It should feel sudden. |
| 3->4 (f396) | HARD | - | - | Denial is a slammed door. The dying coals carry over the cut. |
| 4->5 (f471) | **A ray wipe** | 465-479 | Sun of s05 (342,640). | Night breaks into day: He rose. Done before "He rose"; the picture then holds still under "Jesus died". |
| 5->6 (f567) | **B wave wipe**, night | 560-574 | Front rises bottom -> top. | Back to the sea, back to the dark. "Peter went" starts f571. |
| 6->7 (f711) | **A ray wipe** | 703-717 | Sun of s07 (542,408). | "At sunrise" (f716). The rays keep going as ray stitches. |
| 7->8 (f867) | HARD | - | - | "It fills with fish" is a surprise. The fish burst is the punch. |
| 8->9 (f1023) | **B wave wipe**, day | 1016-1030 | Front rises bottom -> top, into the splash crown. | He jumps in; the sea comes up to meet the cut. "Peter jumps" starts f1027. |
| 9->10 (f1101) | **C ember iris** | 1095-1109 | From the coal fire (542,1125). | Fire sound no. 2. Same move as 1->2, so the eye links the two fires. |
| 10->11 (f1206) | HARD | - | - | The split picture IS the reveal. A wipe would blur it. |
| 11->12 (f1434) | **A ray wipe** | 1424-1438 | Sun of s12 (542,505). | Out of the memory, back to Him: "Come and dine" (f1441). |
| 12->13 (f1596) | HARD | - | - | One quiet talk from here on. |
| 13->14 (f1806) | HARD | - | - | Straight onto Peter's face on "The third time". |
| 14->15 (f2034) | HARD | - | - | Nothing may sit across his answer or the hand on his shoulder. |
| 15->16 (f2256) | HARD | - | - | A clean beat before the count. |
| 16->17 (f2409) | **C ember iris**, low arc only | 2401-2415 | From the fire of s17 (542,1640). | Fire sound no. 3. Draw the edge strokes and riding sparks ONLY on the lower half of the circle (below y 1640) so no printed edge crosses Jesus. The bare mask edge passes Him in about 3 frames. |

Totals: ember iris x3 (the three fire sounds), ray wipe x3, wave wipe x2, hard x8. No dissolves anywhere.

---

## 5. The showpiece: the two fires (s02 / s10 / s11 / s17)

One signature, three times, on the three fire sounds: **ember iris in -> tongue ring pulses -> sparks rise.**
What changes is what the sparks do. That change is the story.

**s02, first fire (f99).** Iris opens from the brazier, f93-107. Ring of 12 tongues round the rim (rx 150, ry 62) pulses
f99-111, colours dull: rust + mustard. Sparks rise through the gap and **cool into teal stars**. The three count coals
appear LIT on "by a fire" (f198-212). By s04 all three are out.

**s10, second fire (f1101).** The same iris, same 14 frames, f1095-1109. Ring of 12 tongues round the stone ring
(rx 480, ry 250, on the stones, not on the fish), pulse f1101-1113, colours bright: burnt orange + mustard + cream core.
- "a fire of coals" (f1121-1181): the 12 tongues flare one after another, clockwise from the top, 5 frames each
  (scale 1 -> 1.3 -> 1). One full turn lands exactly as the phrase ends.
- Spark column: 8 flights, launch f1110 + 10i, from (542,1040) up an S path (amplitude 60 px) to y 560-820 over the sand
  between x 330 and x 700. **They stay orange** and hang there, swaying. Keep 60 px off the jug (x 690-840, y 560-830).
- Plus the steam, waves and flowers listed under s10.

**s11, both fires in one picture (f1206-1434).** Hard cut in.
- f1212-1242: the **woven band (M6)** draws left -> right along the split, centre y 960, 44 px tall. His hem pattern joins
  the two halves.
- From f1206: the top fire has a dull ring (rx 120, ry 52, rust) and 5 spark flights that cool into stars at (150,90)
  (420,60) (640,150) (880,70) (300,230), launch f1215 + 14i. The bottom fire has a bright ring (rx 290, ry 140) and low
  sparks in x 440-640, y 1330-1430.
- "only twice" (f1295-1322): the two rings pulse **one, two**: top at f1298, bottom at f1312.
- "Here" (f1340-1352): bottom ring pulses at f1342. "the night Peter said no" (f1362-1411): top ring pulses at f1372.
- **The link, f1375-1428:** 9 sparks leave the bottom fire in a chain, 5 frames apart, each flying 30 frames on one path:
  (542,1420) -> (700,1250) -> (400,1050) -> (537,800). They cross the woven band, **stay orange inside the night half**,
  and land in the cold brazier. As each lands, the top ring warms one step from rust to burnt orange; fully bright at f1428.
  Without a word, the second fire answers the first. Sparks ride OVER the band.

**s17, the landing (f2409-2637).**
- Iris opens from the fire, f2401-2415, lower arc only. Tongue ring (rx 455, ry 215, bright) pulses f2409-2421.
- Low sparks only, in x 380-700, y 1470-1560. **No spark column:** the hands and bread are above the fire.
- "to feed anyone" (f2455-2480): the three count coals pop in, **already LIT**, at the foot of the art's three steam wisps
  on the back of the ring: (416,1500) (542,1490) (697,1500), flame 80 px. Pop f2456, f2464, f2472.
- "Jesus fed Peter" (f2500-2541): each flame swells once (scale 1 -> 1.25 -> 1, 10 frames) at f2502, f2516, f2530, left to
  right. Three yes's, resting right under the bread.
- Hold f2541-2637: only the three flames sway (+-3 deg, period 80) and 2 gull ticks drift in the sea gap between the two
  heads (x 430-760, y 470-700; keep 60 px from both faces). Nothing new appears after f2530. Do not fade anything.

---

## 6. Three risks and how to check each

**R1. Positions are from stills, and the clips move.** 9 shots were read from a 300 px sheet. A doodle could drift onto a
face, onto Jesus, or float off its fire.
*Check:* for every shot export the first, middle and last clip frame with the doodle layer AND the keep-out boxes drawn in
red. Zero overlap allowed. Check each fire centre on all three frames; if it drifts more than 8 px, track it with a 2-point
linear move. Zoom 2x on every frame that has Jesus in it. Do s01, s03, s04, s05, s06, s08, s09, s14, s15 first.

**R2. "Fuller" tips into "forced" or "sloppy".** This is a lot of ink: about 15-40 marks per shot. It may fight the art or
hide the subject, as Mary & Martha v1 did.
*Check:* build ONE 20 s test first (s07 through the start of s11, f711-1300) with a single `DENSITY` knob that drops every
second flower, gull, wave row and star spot. Render it at 1.0 and 0.6, side by side, for the owner. On 6 stills squint:
is the subject still the first thing seen? Put each motif next to the art's own version (flame, star, flower, fish, curl):
same hue, same line weight, same grain. If a doodle looks cleaner or brighter than the print, fix the colour and grain
before adding any more.

**R3. Transitions need clip tail and must not step on words; the count must read.** Each window needs up to 8 spare frames
on the outgoing clip and up to 10 frames early start on the incoming one. And a newcomer has to read the coals as "three".
*Check:* `ffprobe` all 17 clips: length >= slot + 0.3 s. If one is short, slide that window to start at the cut (a = 0),
or make that cut hard. Step every transition frame by frame against the word frames above: the new picture must be at
least 80% open by the first word. Watch the iris 16->17 at 2x for anything printed across Jesus. Then show s03-s04 and s16
to one fresh viewer with no sound: can they say "three went out, three came back on"? If not, make the coals 1.3x bigger
before touching anything else. Finish with `check_landing_hold.py` (audio length = video length, last 3 s calm).
