# Mary and Martha (Warm Storybook) — Motion layer v1 (design spec, build-ready)

Comp: 1080x1920, 30 fps, 2148 frames (71.61 s). Base = the 15 Kling clips of `MARY_MARTHA_SCORED_v2.mp4`, each at 1.0x from its frame 0.
Because 6 cuts now overlap, the builder lays the 15 clips as separate `OffthreadVideo` layers (not one flat base file). Audio = the v2 scored mix, untouched.
All frames below are absolute comp frames. Word frames come from `voice_v2/narration.alignment.json` (x30, rounded).
Positions were read off the gridded frames f01-f15 (one frame per shot; see risk R1).

---

## 1. The idea in 3 lines

1. **One pencil line.** A soft sepia pencil line gets tangled into a small **knot** (her worry, her "many things"). Same hand as the pictures: pencil on cream paper, a dab of gouache.
2. **Pencil is Martha's side. Terracotta is His.** Narrator words and the knot are warm graphite. Jesus's own words, and the "one thing", are painted in the rust of His mantle.
3. **Many becomes one.** At the end the knot comes loose into one calm terracotta line under "And He loved her."

---

## 2. The thread (first frame to last)

| Seen | Frame | What the line does |
|---|---|---|
| 1. Born | f20 | A small knot scribbles itself beside Martha's head ("everything for everyone"). |
| 2. Made of many things | f964 | One long line loops round pot, jar, figs, nuts, bread ("many things"). Same stroke, same colour. |
| 3. The answer | f1024 | One straight terracotta line under **one thing**. The first calm line in the film. |
| 4. Named | f1262 | The underline of the word "worry" runs off and ties itself into the knot. Now the viewer knows what the knot is. |
| 5. Pay-off | f2030 | The knot unties, turns terracotta, and becomes one calm line under **And He loved her.** Holds to the last frame. |

---

## 3. Cuts and beat table

Cut frames (round of s x 30): **0 · 179 · 261 · 329 · 464 · 668 · 837 · 954 · 1059 · 1208 · 1313 · 1512 · 1616 · 1844 · 1920 · end 2148.**
If `build_v2.py` rounds a cut 1 frame differently, use its number and shift that shot's beats by the same 1 frame.

Safe box for TEXT: x 60-950, y 160-1490. "Box" = outer edge of the carrier (x1-x2, y1-y2). Font = Kalam 700 unless noted.

| # | Frames (on-off) | Word it hits | What appears | Motion (easing) | Box (px) / size | Colours | Why |
|---|---|---|---|---|---|---|---|
| **1a** | 0-179 | hook ("Does anyone even care?" f98-133) | Cream swatch, text **Does anyone care?** | Fully there on frame 0. Settle: scale 1.05→1, f0-6, ease-out cubic. No fade: leaves on the hard cut at f179. | 70-730, 170-310. Text 76 px, centre (400, 240). | Swatch `#F8EFDD`, text `#3A322B` | First-frame hook. Sits on the stone wall above her head (hair top y≈320), left of the beam post (x≈730). |
| **1b** | 20-179 | "**everything** for **everyone**" (f20-58), tightens on "Does anyone even care?" (f98-122) | The **knot** (doodle), no carrier | First 60% of the path draws f20-58, linear. Last 40% (the tight inner loops) draws f98-122, linear. Then still. Leaves on the cut. | 70-250, 350-530 (knot scale 1.0, centre (160, 440)). Stroke 5 px. | `#6B4A32` | Births the thread. On bare stone wall left of her hair (hair edge x≥290 at this height). She is tugging her own hair in the picture: the knot says the same thing. |
| **2** | 186-261 | "**Martha**" (f190-200) | Cream swatch, name **Martha** | Swatch paints on f186-191 (L→R). Text writes f190-200. Leaves on the cut (curtain wipe starts f261). | 600-950, 1340-1470. Text 92 px, centre (775, 1405). | Swatch `#F8EFDD`, text `#3A322B` | Tells a newcomer who this is. On her tunic shoulder, like a storybook label. Clear of face (y≤1000) and neckline (x≤625). |
| — | 261-381 | quiet (4 s) | nothing | | | | "She had opened her home to Him" is said by the curtain and the open door. |
| **3** | 380-452 | "**Mary**" (f384-392) | Cream swatch, name **Mary**, one tiny pencil arrow down to her | Swatch paints on f380-385. Text writes f384-392. Arrow draws f393-400, ease-out cubic. Out: opacity f440-452. | Swatch 270-540, 375-492. Text 96 px, centre (405, 432). Arrow: `M 405 496 Q 392 522 384 544`, 4 px, 14 px open head. | Swatch `#F8EFDD`, text `#3A322B`, arrow `#6B4A32` | Names the sister. Between the shelf sketch and His head (His hair starts x≥690). Mary's hair top y≈555. His open hand is at y≥825. |
| — | 452-843 | quiet (13 s) | nothing | | | | Martha's whole complaint (KJV) and "His answer? Her name. Twice." play clean on the two faces. |
| **4** | 841-952 | "**Martha, Martha,**" (f843-857, f868-882) | Cream swatch, text **Martha, Martha,** (KJV, word for word) | Swatch paints on f841-846. First "Martha," writes f843-857. Second "Martha," writes f868-882 (it follows His voice; the gap is the point). Out: opacity f940-952. | 130-900, 190-390. Text 104 px, centre (515, 290). | Swatch `#F8EFDD`, text `#A84A24` | First terracotta in the film = His voice. Her name, twice, written over her head while her face answers. Hair top y≈437. |
| **5a** | 963-1008 | "**many things**" (f958-977) | Cream swatch, text **many things**; then the **lasso** (doodle): one line looping 5 things | Swatch paints on f963-967. Text writes f964-977. Lasso draws f964-994, linear (a steady hand), one loop about every 6 frames. Out: text, swatch and lasso opacity f998-1008. | Swatch 70-570, 220-390. Text 84 px, centre (320, 300). Lasso path: see 4.4. Stroke 5 px. | Swatch `#F8EFDD`, text `#3A322B`, lasso `#6B4A32` | KJV words. The still life has no people, so the line can roam. The viewer sees the knot is made of "many things". Text sits on bare plaster above the steam (steam top y≈600). |
| **5b** | 1009-1120 | "**one thing**" (f1009-1022) | Same spot: cream swatch, text **one thing**, one calm line under it | Swatch stays (fade it back up f1006-1010). Text writes f1009-1022. Line draws f1024-1034, ease-out cubic. **Holds across the cut at f1059** while the kitchen blooms into Mary (transition C8). Out: opacity f1108-1120 (on "good part"). | Same swatch 70-570, 220-390. Text 104 px, centre (320, 295). Line: `M 112 372 Q 320 380 530 364`, 7 px. | Text + line `#A84A24` | KJV words. Same place, bigger, His colour: many → one. Holding it over Mary shows what the one thing is before the narrator explains it. Mary's hair top y≈425. See R6, R9. |
| — | 1120-1210 | quiet (3 s) | nothing | | | | Mary's face carries "shall not be taken away from her". |
| **6** | 1208-1310 | "**Careful**" (cut f1208), "**full of worry**" (f1245-1266) | Cream swatch, three rows: **“careful”** / small **means** / **full of worry**. Then the underline of "worry" runs off and ties the **knot** | Swatch paints on f1208-1213. “careful” writes f1210-1226. "means" fades in f1236-1242. "full of worry" writes f1245-1266. Underline + knot: one stroke, draws f1262-1288, linear. Out: all opacity f1298-1310. | Swatch 440-950, 185-455. “careful” 88 px, centre (695, 250). "means" 42 px (Kalam 400), centre (695, 320). "full of worry" 74 px, centre (695, 392). Underline (772, 434)→(925, 428), then into knot at scale 0.8, centre (858, 522), box 790-926, 462-582. | Swatch `#F8EFDD`, text `#3A322B`, underline + knot `#6B4A32` | The one hard word, in plain English, for a second-language viewer. Top right is bare cream; hands are at y≥590, pot rim y≥610. Swatch covers ~100 px of sleeve only. |
| — | 1310-1549 | quiet (8 s) | nothing | | | | "The one thing needed was to hear Him" plays on the wide picture that shows it. |
| **7** | 1545-1612 | "**did He care?**" (f1549-1569) | Cream swatch, text **Did He care?** | Swatch paints on f1545-1550. Text writes f1549-1569 (tracks the voice). Out: opacity f1600-1612. | 90-700, 170-310. Text 92 px, centre (395, 240). | Swatch `#F8EFDD`; "Did", "care?" `#3A322B`; "**He**" `#A84A24` | Same box and hand as the hook, so the eye links the two questions. The music turns here. Her hair top y≈325; lamp is at x≥725. |
| **8** | 1665-1832 | "**Now** Jesus loved Martha" (f1662), music warms | One small tag **John 11:5** | Fade in f1665-1677. Hold. Fade out f1820-1832. Nothing else on this shot. | 70-330, 172-240. Text 40 px (Kalam 400), rotate -1.5°. | Swatch `#F8EFDD`, text `#3A322B` | The hero picture breathes. The tag only shows that the love line is the Bible's own. On the leaf pattern, top-left; nearest hair y≥312. |
| — | 1832-1968 | quiet (4.5 s) | nothing | | | | "He never called Martha's work wrong": her hand in His. No text near hands. |
| **9a** | 1968-2148 | "He **saw** her **worry**." (f1974-2002) | Cream swatch low on the robes; text **He saw her worry.**; a short underline under "worry" runs into a small **knot** | Swatch paints on f1968-1974. Text writes f1974-2002. Underline + knot draw f1996-2016, linear. | Swatch 110-930, 1235-1485. Text 64 px, left edge x 160, centre y 1292. Underline (540, 1327)→(690, 1323). Knot scale 0.6, centre (745, 1290), box 694-796, 1245-1335. | Swatch `#F8EFDD` at .92, text `#3A322B`, knot `#6B4A32` | Twin of beat 6 (same underline-into-knot), so the viewer reads it at once. On skirt and robe; her cup hands are at y≤1175, His hand on His knee y≤1212. |
| **9b** | 2030-2148 (end) | "And He **loved** her." (f2034-2057) | The knot **unties** into one calm line; text **And He loved her.** | Untie f2030-2054, ease in-out cubic (see 4.3). Underline under "worry" fades f2030-2040. Text writes f2034-2057. **No out.** Holds 3.0 s to the last frame. | Text 100 px, centre (520, 1392). Calm line ends as `M 150 1456 Q 520 1470 890 1448`, 7 px. | Text + line `#A84A24` | The thread pays off: the tangle of many becomes one line, in His colour. "He saw her worry." stays written above it: He saw it and He loved her. |

Count: **9 text beats** (1a, 2, 3, 4, 5, 6, 7, 8, 9). **5 doodle beats** (1b knot, 5a lasso, 5b one line, 6 worry-knot, 9b untie) plus one tiny name arrow. 6 quiet stretches. Terracotta appears 4 times only (4, 5b, the "He" in 7, 9b).

### Timing notes the builder must know
- The aligner stretched two words over a pause: "Careful" (f1195-1228, straddles the cut at f1208) and "Now" (f1662-1698). Trust the shot cut for beat 6 and check both by ear.
- Beat 5a's text is fully written for only ~0.7 s before it fades. That is on purpose (it is swept away by "one thing"), and it is 2 short words at 84 px.
- Beats 1a and 2 leave on a hard cut. All other exits are a 12-frame opacity fade.

---

## 4. Transitions (every cut)

Rule: the next shot always starts on its cut frame from its own frame 0. A transition only reveals it over the first N frames, with the outgoing clip playing on underneath from its tail.

| Cut | Frame | Shots | Type | Frames / easing | Tail used (max) | Why |
|---|---|---|---|---|---|---|
| C1 | 179 | 1→2 | **Hard** | — | 0 (2 f) | Hook pace. No tail anyway. |
| C2 | 261 | 2→3 | **Curtain wipe**, right → left | 12 f (261-273), ease-out cubic | 12 of 68 f | "She had opened her home." Shot 3 is Martha drawing a curtain aside. The cut itself opens like cloth. |
| C3 | 329 | 3→4 | **Hard** | — | — | Simple story step. |
| C4 | 464 | 4→5 | **Hard** | — | — | Martha breaks in on the quiet. The cut should break in too. |
| C5 | 668 | 5→6 | **Hard** | — | — | Straight to His face. No softening of her question. |
| C6 | 837 | 6→7 | **Hard** | — | — | He says her name, we are on her. |
| C7 | 954 | 7→8 | **Page slide**, new page comes in from the right | 9 f (954-963), ease in-out cubic | 9 of 94 f | Mid-sentence ("troubled about | many things"): the eye is led across to the kitchen. |
| C8 | 1059 | 8→9 | **Wet bloom**, with **one thing** held on top | 16 f (1059-1075), ease-out cubic. Bloom origin (320, 372) = the terracotta line | 16 of 76 f | The many things melt away under the words "one thing" and Mary is there. The best cut in the film. |
| C9 | 1208 | 9→10 | **Hard** | — | 0 (2 f) | No tail. Also a new thought. |
| C10 | 1313 | 10→11 | **Page slide**, new page comes in from the left | 9 f (1313-1322), ease in-out cubic | 9 of 106 f | Mirror of C7: we went out to the work, now we come back to the room where He is. |
| C11 | 1512 | 11→12 | **Hard** | — | — | The music turns on this frame. Let it hit. |
| C12 | 1616 | 12→13 | **Wet bloom**, slow | 20 f (1616-1636), ease in-out sine. Origin (540, 800) | 20 of 78 f | "Later…" = time passes. The only slow one. |
| C13 | 1844 | 13→14 | **Hard** | — | — | Only 13 f of tail, and the line is plain. |
| C14 | 1920 | 14→15 | **Wet bloom** | 16 f (1920-1936), ease-out cubic. Origin (600, 420) = the lit doorway | 16 of 105 f | The ending opens out of the light. Then 1.5 s of clean picture before any words. |

Count: **6 non-hard** (1 curtain, 2 slides, 3 blooms). **8 hard.** No overlay is on screen during C2, C7, C10, C12, C14. Only C8 has a held overlay, on purpose.

---

## 5. Device build notes (Remotion)

New file `_remotion/src/MaryMarthaV1.tsx`. Reuse from `Ep16ChildrenV2.tsx`: `Swatch`, `WriteOn`, `PencilLine`, `PaperGrain`, the `deckle`, `graphite`, `pencil` filters, `boilSeed`, `clamp`, `OUT`, `IN`. Do not bring the blue `Wash` or the `Slip`.
Layers, bottom to top: 15 clip layers (with transition masks) → `<Defs/>` → beats → `<PaperGrain/>`.

### 5.1 Swatch and text
- Swatch = ep16 `Swatch` (deckle edge, dry-brush tail, warm lower shade `#E8D6B4`), fill `#F8EFDD`, opacity .94 (.92 on beat 9). It should read as a dab of cream gouache on the page. No drop shadow anywhere in this film.
- Text = ep16 `WriteOn` (clip-path reveal, linear, never faster than 1 frame per letter). Graphite text gets `#graphite`. Terracotta text gets **no** grain filter (solid gouache) and `textShadow: "0 2px 0 rgba(120,50,20,.25)"`.
- No letter bounce, no boil on text.

### 5.2 The knot (ONE component, three uses: 1b, 6, 9a)
- Props: `cx, cy, scale, from, to` (plus an optional lead-in point for the underline in beats 6 and 9a).
- Path = 120 points, t from 0 to 1:
  `θ = 2π · 5.5 · t`
  `r = 26 + 46 · |sin(2π · 1.7 · t + 0.6)|`
  `x = cx + scale · (1.15 · r · cos θ + 10 · sin(2π · 3.1 · t))`
  `y = cy + scale · (0.90 · r · sin θ + 8 · cos(2π · 2.3 · t))`
  then a loose tail: 12 more points curving 60 px down and right (× scale). Join with a smooth curve (Catmull-Rom). Size at scale 1.0 is about 170 x 150.
- Round, loopy, soft. **No sharp zig-zags** (a jagged scribble reads as comic-book anger; this is worry).
- Stroke 5 px at scale 1.0 (min 4 px), round caps, `#6B4A32`, `filter="url(#pencil)"` (3-pose boil, changes every 5 frames, absolute frame).
- Draw-on: `pathLength=1` + `strokeDashoffset`, linear.
- Beats 6 and 9a: the path starts with the underline (two points from the table) and then enters the knot, so it is one unbroken stroke.

### 5.3 The untie (beat 9b)
- Target = 132 points evenly spaced along the calm line `M 150 1456 Q 520 1470 890 1448`.
- Each knot point i moves to target point i. Progress for point i: `p_i = ease(clamp((frame − 2030 − 6·(1 − i/131)) / 18))`, ease in-out cubic. So the tail end leads and the line pulls out smoothly over f2030-2054.
- Colour lerps `#6B4A32` → `#A84A24`, stroke 3 px → 7 px, over the same frames. Keep the `#pencil` filter on until f2054, then swap to a static seed (the last line must be still for the 3 s hold).

### 5.4 The lasso (beat 5a)
- One open path, 5 loose loops joined by short strokes, in this order. Each loop is about 1.15 turns of an ellipse (it does not close neatly), started at its top-left:

| Thing | Centre | rx, ry |
|---|---|---|
| Cooking pot | (200, 1050) | 170, 125 |
| Tall jar | (600, 930) | 140, 225 |
| Fig basket | (841, 915) | 135, 105 |
| Nut basket | (870, 1185) | 115, 92 |
| Bread stack | (627, 1238) | 150, 125 |

- Ends with a 120 px tail trailing off to lower-left, toward (400, 1400).
- Stroke 5 px, `#6B4A32`, opacity .85, `#pencil` filter. Draw f964-994, linear.
- It must look like the same line as the knot. If any loop cuts through the fire glow badly, nudge that loop, do not thicken the stroke.

### 5.5 Curtain wipe (C2)
- Mask on the incoming clip. The reveal front travels from x 1100 to x −80 over f261-273, ease-out cubic.
- Front shape: a vertical edge with three soft folds: `x_front(y) = X + 26 · sin(2π · y / 640)`, then `deckle` filter.
- On the outgoing side of the front: a 16 px cream rim `#F8EFDD`, then a 40 px soft band of `#E8D6B4` at .5 (a cloth fold, not a shadow box). No blur, no bounce.

### 5.6 Page slide (C7, C10)
- Both clips move together 1080 px over 9 frames, ease in-out cubic. C7: outgoing exits left, incoming enters from right. C10: the reverse.
- Between them a 14 px strip of `#F8EFDD` with one 2 px `#6B4A32` line at .5 (the paper edge). No motion blur, no zoom.

### 5.7 Wet bloom (C8, C12, C14)
- Mask on the incoming clip: a white ellipse at the origin in the table, growing rx 0→1500, ry 0→2300, displaced by the ep16 `wash` turbulence (baseFrequency `0.009 0.016`, scale 34) and then blurred 28 px so the wet front is soft and uneven.
- No coloured rim. Nothing but the two pictures and the paper. On cream-to-cream shots the figures seem to soak into the page.
- C8: the `one thing` swatch, text and line sit above the mask and do not move at all.

### 5.8 Paper grain
- ep16 `PaperGrain`, multiply, opacity .05, static. Top layer, over everything, so the marks and the film share one sheet.

---

## 6. Fonts and palette

**Font:** Kalam (bundled: `_remotion/public/Kalam-Bold.ttf`, `Kalam-Regular.ttf`). 700 for all lines; 400 for "means" and the John 11:5 tag. One hand for the whole film.

| Role | Hex |
|---|---|
| Cream gouache (swatches, rims) | `#F8EFDD` |
| Paper shade (swatch lower edge, cloth fold) | `#E8D6B4` |
| Warm graphite (narrator text) | `#3A322B` |
| Sepia pencil (knot, lasso, arrow, underline) | `#6B4A32` |
| Terracotta = His mantle (His words, one thing, last line) | `#A84A24` |

Rule: terracotta is only ever Jesus's own words, the "one thing", the "He" in beat 7, and the last line. Nothing else gets a colour. No honey or yellow in the overlays (it would fight the tunics).

---

## 7. Do not

- Do not cross out, shake, or scribble over anything Martha does. The lasso only goes **round** things. Her work is never marked wrong.
- Do not put any mark over a face, the cup hands, His hand on her shoulder, or the joined hands in shot 14.
- Do not put any text on shots 3, 5, 6, 11 or 14. Shot 13 gets the small tag only.
- Do not write Martha's KJV line on screen, and do not write a plain-English version of it as if she said it.
- Do not add a heart, a halo, light rays, sparkle, glow, or a speech bubble.
- Do not use pills, rounded UI boxes, drop shadows, lower-thirds, or progress marks.
- Do not use sound-wave arcs, tick boxes, arrows between people, or icons. (One tiny name arrow in beat 3 is the only arrow.)
- Do not add motion blur, zoom punches, flashes or whip effects to transitions.
- Do not fade the last line. It holds, still, for the full 3 s.
- Do not add a transition to any cut marked Hard.

---

## 8. Risks

- **R1 (all beats).** Every box was checked on ONE frame per shot. The clips move. Before showing the owner, export first / middle / last frame of each beat and re-check faces and hands. Most at risk: beat 5b over Mary's hair (30 px clear), beat 6 knot above the working hands (8 px above the pot rim), beat 9 swatch under the hands (23 px clear), beat 1a above her hair (10 px).
- **R2 (knot).** A scribble can read as "angry" in comic language. Keep it round, small and sepia. If a blind viewer says "she is angry", lighten it (opacity .8) and slow the draw-on by 6 frames.
- **R3 (lasso).** Could look like an app annotation or like "these things are the problem". Keep it loose and hand-slow. If the panel reads it as blame, drop the loops and keep the two word cards; the thread still works through beats 1b, 6 and 9.
- **R4 (untie).** The words say He saw her worry and He loved her. They do not say her worry ended. The knot becoming His line is a picture of love, not a promise that worry vanishes. "He saw her worry." stays written for that reason. If the doctrine panel objects, keep the knot in place and draw the calm line fresh under the last words.
- **R5 (hook words).** "Does anyone care?" drops the word "even" to fit at a readable size. It is the narrator's line, not Bible text. If the owner wants it exact, use two rows at 64 px and move the knot down 40 px.
- **R6 (C8 held words).** If Mary's hair rises into the box during the bloom, fade "one thing" at f1090-1102 instead of f1108-1120.
- **R9 (meaning of 5b).** Holding "one thing" over Mary could be read as "Mary is the one thing". The narrator fixes this 10 s later ("to hear Him, as Mary did"). If a blind seat still misreads it, end beat 5b at f1052 and let C8 run clean.
- **R7 (terracotta contrast).** `#A84A24` on cream is fine at 100 px. Check "He" in beat 7 (92 px) on a phone; if weak, darken to `#963F1D` everywhere.
- **R8 (names on tunics).** "Martha" sits on her shoulder like a label. If it reads as a badge, move it to 400-720, 165-270 (above her hair, tighter).
- **R10 (count).** 9 text beats is one more than ep16. First to cut if it feels busy: beat 8 (the tag), then beat 3's arrow.

## 9. QC before showing the owner (all $0)

1. Stills at f0, 60, 200, 268, 395, 875, 990, 1040, 1066, 1280, 1318, 1570, 1626, 1700, 2010, 2045, 2147. No mark on a face or hands; all text inside x 60-950, y 160-1490.
2. Frame 0 shows the hook words fully written.
3. Each transition: step through frame by frame. The incoming shot's first frame is on the cut frame. No black, no flash.
4. Zoom 2x on the knot, the lasso and the last line: same pencil, same weight, no jagged corners.
5. Last frame: both lines and the calm terracotta line fully drawn and still. Audio and video same length (`check_landing_hold.py`).
