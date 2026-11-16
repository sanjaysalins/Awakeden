# Woman at the well (Pop Halftone) - Motion layer v2 "LIVING WATER TAKES THE PAGE" (design only, $0)

Owner note on v1: "great edit, but go bolder and fuller motion graphics, be as creative as your model allows."
This doc is the full build spec. The builder makes no creative choices. Where a number is given, use it.

- Comp: 1080x1920, 30 fps, **2636 frames**. New comp name `WomanWellV2` in `_remotion/src/WomanWellV2.tsx` (copy helpers from `WomanWellV1.tsx`).
- Base: `public/waw_base_v2.mp4`, 1.0x, never re-cut, audio muxed from it after render. Tails for two irises: `public/waw_c07.mp4`, `public/waw_c17.mp4` (as v1).
- All frames are ABSOLUTE comp frames. Seconds = frame / 30.
- Cuts (measured, from v1 code): `CUT = [0,132,240,348,434,568,683,801,981,1125,1341,1463,1569,1654,1738,1978,2128,2264,2445,2636]` (c01..c19, end).
- Word frames below are real, from `motion_v1/words_film.json` (field `f` = start frame).
- No `Math.random`. Use `hash(i) = fract(sin(i*127.1+311.7)*43758.5453)`.

---

## 1. The big idea

**The page itself gets thirsty, then the living water takes the page.**
In v1 the story was told by small drops. In v2 it is told by the whole sky: the loud burst rays behind the people are re-coloured live. They **drain to dry paper** on "thirst again", they **flood teal** on "shall never thirst", and teal then follows her to town. On top of that sky: comic panel gutters, big ink ticks, splash crowns, speech balloons with exact KJV words, and a graphic move on 10 of the 18 cuts.
The drop spine stays (white drop falls and is gone / teal springs up) but every part is 2-3x bigger, and the spring now fills the whole frame.

**The trick that makes "bold" safe: the INK KEY.** All people, faces, ground and stones in this art are pure black-and-white. Only the rays are coloured. So we put our big graphics UNDER a copy of the film that keeps only its grey pixels. Result: our sky graphics sit *behind* every figure and face automatically, on every frame, even when the camera moves. The art's own black ray lines and ink spatter stay on top, so our colours look printed, not pasted.

### Palette (hex)

| Name | Hex | Use |
|---|---|---|
| K ink | `#111111` | all outlines, speed lines, gutters |
| W white | `#FFFFFF` | sticker edge, well-water drops, balloons |
| PAPER | `#F4EFE4` | the "dry / thirsty" sky |
| TEAL | `#14B8C4` | living water (only after f866) |
| DEEP | `#0A7C8C` | water shade, type shadow on teal |
| AQUA | `#7FE3E8` | water highlight wedge |
| YEL | `#FFD60A` | noon, WHY?, ticks, Saviour slab |
| ORG | `#F55700` | wipes (act 1 only) |
| RED | `#EE0C00` | one wedge colour in "kept apart" only |
| GOLD | `#FFE89A` | tomb sunrise only |

Colour rule: **TEAL never appears before f866** ("gift"). Before that, water is white. Paper = thirst.

### Layer stack (bottom to top) - build exactly this

1. `Base` - `OffthreadVideo waw_base_v2.mp4`.
2. `BACK` - one full-frame SVG. Sky fields only (D2, D3, D5 fields, D6). Wrapped in FaceGuard mask.
3. `InkTop` - a second `OffthreadVideo` of the same file, same frame, wrapped in a div with `filter: url(#inkKey)`. Mount it only on frames where BACK draws something (see table) to save render time.
4. `FRONT` - one full-frame SVG. Objects: drops, ticks, splashes, gutters, balloons, type. Wrapped in FaceGuard mask.
5. `TRANS` - transitions (full-frame covers, irises with clip tails). Not masked.
6. `FRAME` - the comic page border (D9).

Safe zone for words (Shorts UI): all type inside **x 60-960, y 200-1540**.

---

## 2. The devices (10)

### D1. INK KEY (the matte) + FACE GUARD

```
<filter id="inkKey" color-interpolation-filters="sRGB" x="0" y="0" width="100%" height="100%">
  <feColorMatrix in="SourceGraphic" type="matrix" result="d"
    values="1 0 -1 0 0   -1 0 1 0 0   0 0 0 0 0   0 0 0 1 0"/>      <!-- R'=R-B (warm), G'=B-R (teal) -->
  <feColorMatrix in="d" type="matrix" result="m"
    values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0   -6 -6 0 0 1.5"/>       <!-- alpha = 1.5 - 6*(R'+G') -->
  <feComposite in="SourceGraphic" in2="m" operator="in"/>
</filter>
```
Grey/black/white pixels stay solid. Orange, red, yellow, teal pixels go clear. Tune only the two numbers `-6` and `1.5` (step 1 of build order).
**Fallback if the filter fails in headless Chrome:** clip BACK to the per-shot sky rectangle in the table ("sky y<...") instead, and skip InkTop.

**FaceGuard** (belt and braces, always on, both BACK and FRONT): an SVG `<mask>`: white full-frame rect, black ellipses from the "face guard" column of the shot table. Hard edge, no feather. Ellipse = (cx, cy, rx, ry). Builder re-reads every ellipse on first / middle / last frame of the shot and grows it if the face leaves it.

### D2. RAY SWAP (BACK) - re-colour the sky

A fan of 16 flat wedges from an origin `O`, radius 2600 (reuse v1 `wedgePath`). Wedge widths in degrees, fixed list: `[26,18,30,20,14,28,22,24,16,30,20,26,18,22,28,18]` (sum 360). Colours from a named palette, cycled.
Props: `O`, `pal`, `rot0`, `spin` (deg/frame), `reveal`:
- `snap` - on in 1 frame.
- `sweep(a,b)` - clock wipe: a `clipPath` pie from angle 180 deg growing clockwise to 360 deg (upper half) then on to full, over frames a..b, `Easing.out(cubic)`.
- `iris(a,b,R)` - circle clip from `O`, r 0 to R, `Easing.inOut(sin)`.
- `front(a,b,dir)` - straight edge wipe (dir = "down" or "up"), edge is a row of Ben-Day dots (D3) 2 rows deep.
- `pulse(at)` - on for 4 frames only (`at..at+3`), then off. A beat flash.
Palettes:
- `NOON` = [YEL, W, YEL, "#FFF3A0"]
- `DRY` = [PAPER, W] plus black Ben-Day dots r 7, pitch 34, over the PAPER wedges only
- `WATER` = [TEAL, DEEP, TEAL, AQUA, TEAL, W]
- `LEFT` = [YEL, ORG, W] / `RIGHT` = [RED, K, ORG] (c06 only)
- `DAWN` = [GOLD, W, YEL]
Opacity 1.0 unless the table says otherwise.

### D3. DOT FIELD (BACK or TRANS) - Ben-Day dots

Hex grid, pitch `p` (default 54), row offset p/2, dot radius from a function. Build as plain `<circle>`s (about 800 per frame is fine).
- `wipe(a,b,ang,col)` (TRANS, the cut wipe): `d` = position of the dot along direction `ang`, normalised 0..1 across the frame diagonal. `front = lerp(f,a,b,-0.25,1.25)`. `r = 40 * clamp((front - d)/0.22, 0, 1)`. At `front >= 1.25` the frame is solid (also draw a full rect of `col` when front > 1.0 so no gaps). To reveal, run the same with `r = 40 * clamp((d - front)/0.22,0,1)`.
- `radialHole(a,b,C,R,col)`: solid `col` everywhere outside a growing hole at `C`; `hole = lerp(f,a,b,0,R, Easing.out(cubic))`; dot r = 40 * clamp((dist - hole)/240, 0, 1); solid rect with an evenodd circle hole of radius hole+240 behind the dots.
- `crawl(col, r, speedY, opacity)`: dots of fixed radius `r`, pitch 64, whole field offset by `speedY * f` px (wrap by pitch). Calm texture.
- `sun(O, R)`: dots only where dist to O < R; r = 22 * (1 - dist/R) * (0.8 + 0.2*sin(2*PI*f/40)).

### D4. PANEL GUTTER + SHUTTERS (FRONT / TRANS)

- `Gutter(x)`: white vertical bar 44 px wide (x-22..x+22) with a 10 px K line on each side, full height. Slam: its y-offset goes -1920 to 0 in 5 frames (`Easing.in(quad)`), then 2 frames squash (scaleY 0.985 at bottom anchor), then still. On the landing frame draw 6 impact ticks at the foot (D8 ticks, len 150, fan -160..-20 deg at (x,1900)), 8 frames.
- `Shutters(a, cut, b, x)`: two K rectangles with a 12 px white inner edge. Left one slides in from x=-1080 to cover 0..x, right one from x=1080 to cover x..1080, over a..cut (`Easing.in(cubic)`); at `cut` they are closed; they open again cut..b (`Easing.out(cubic)`).
- `Shards`: when the gutter breaks, the segment y 200-560 is replaced by 6 white quads with K outline (split the 44x360 bar into 6 x 60 px slices). Each flies: velocity `((hash(i)-0.5)*38, -10 - hash(i+9)*14)` px/frame, gravity +2.2 px/frame^2, spin `(hash(i+3)-0.5)*40` deg/frame, removed after 14 frames.

### D5. LIVING WATER kit (the spine)

- `Drop` - reuse v1 `Drop` (3 states: empty / white / teal, `lv` fill). **Sizes now h 170-420.** Outline 12 px K + 6 px W edge when h > 250.
- `Crown(x,y,w,col)` - splash crown: 5 lobes (drops, h = 0.42w, rotated -60,-30,0,30,60 deg) rise from (x,y) to radius 0.5w and shrink, 12 frames, plus a flat ellipse ring (rx 0.5w, ry 0.12w, K stroke 10, W fill) for frames 0-6. Default w 300.
- `Ripple(C, at, r0, r1, col)` - ring: stroke `col` 16 px between two K strokes 6 px, r0 to r1 in 24 frames `Easing.out(cubic)`, stroke width goes to 0 over the last 6 frames.
- `Flood(C, a, b)` - a filled TEAL circle from `C`, r from 330 to 2300 over a..b (`Easing.in(quad)`). Edge is scalloped: 18 lobes, path = circle with radius `r*(1+0.045*sin(18*theta + f*0.5))` (sample 144 points). K outline 14 px. Inside: one AQUA ring stroke 22 px at 0.9r, DEEP dots (D3 fixed r 9, pitch 46) clipped to r < 0.7r.
- `WaveBody(yTop, col)` - full-width teal body from `yTop` down to 1920+. Top edge path: `y = yTop + 34*sin(x/170 + f*0.16) + 16*sin(x/61 - f*0.23)`, sampled every 30 px. K outline 12 px on the top edge, a W line 8 px thick following the edge 30 px lower, DEEP dots (r 8, pitch 46) in the lowest 40% of the body.
- `Stream(lane, a)` - rising drops that never stop: teal drops h 190, one launched every 12 frames from f=a, each rises at 13 px/frame along x = lane + 22*sin(y/140 + i), from y 2040 to y -140, then is removed.

### D6. SPEED LINES (BACK, so they are always behind people)

`SpeedLines(F, n, r0)`: n black tapered triangles pointing at focus `F`. Line i: angle `360*i/n + (hash(i)-0.5)*8`, base on a circle r 2400 (base width `10 + hash(i+50)*30` px), tip at radius `r0 + hash(i+20)*160`. **Boil on threes:** use `i` seed offset `floor(f/3)%2 * 1000` so two line sets swap every 3 frames. n = 46 unless stated.

### D7. INK BARS (TRANS) - the fast wipe

`Bars(a, cut, b, cols)`: 5 horizontal bars, each 384 px tall, bar k covers y 384k..384k+384. Each bar slides in from the left: its right edge goes from -100 to 1180 over `a + 2k .. cut` (so all are closed at `cut`), then its left edge goes from -100 to 1180 over `cut .. cut + 4 + 2k`. Colours from `cols` cycled; 8 px K line top and bottom of each bar.

### D8. STICKERS (FRONT) - v1 kit, bigger

Reuse v1 `Tick`, `JarTicks`, `Puff`, `Flower`, `WhyStar`, `pop`, `well`. New sizes:
- Ticks: len **200-240**, strokes W 46 / K 36 / YEL 20. `JarTicks` = **7** ticks, radius-in 80.
- Ticks boil: each tick length multiplied by `1 + 0.06 * (floor(f/3)%2 ? 1 : -1)` while shown.
- Puffs r 70 / 55 / 40. Flowers r 60.
- Loud half (c01-c09, c14, c16, c17): `pop` (8 frames, back ease). Quiet shots (c03, c10, c12, c13, c15, c18, c19): `well` only (sine, 30-40 frames), no back ease.

### D9. PAGE FRAME (top layer, whole film)

A comic page border: K rectangle stroke 20 px inset 10 px (so it covers the outer 20 px), plus a W line 6 px at inset 26 px.
`thump(at)`: border scale 1.018 to 1 over 6 frames (`Easing.out(cubic)`), about frame centre. Thump list: 10, 22, 34, 112, 348, 436, 607, 771, 866, 952, 958, 967, 1341, 2092, 2119, 2128. **No thump in c03, c10, c12, c13, c15, c18, c19.**

### D10. KINETIC TYPE (FRONT)

Font Bangers (`public/Bangers.ttf`, load as in v1). ALL CAPS. Letter-spacing 4.
- `Slam` (loud): word appears at its frame, scale 1.7 to 1 in 5 frames (`Easing.out(back(1.6))`), rotate from `(hash(i)-0.5)*10` deg to its rest angle. Fill + K stroke 14 (`paintOrder: stroke`) + a flat shadow copy offset (8,8).
- `Step` (calm): word is simply on from its frame. No scale, no rotate, no shadow.
- `Balloon(x0,y0,x1,y1,tip)`: W rounded rect rx 60, K stroke 12, plus a triangle tail (base 90 px wide on the bottom edge, to `tip`), tail drawn in the same path so there is no seam.
- `Slab`: W (or YEL) rect rx 22, K stroke 10, flat K shadow offset (10,10).
The 8 word items are listed in section 5. **Type the strings by copy-paste from section 5.**

---

## 3. Shot by shot (all 19)

"L" = loudness 1 (still) to 5 (full takeover). "Sky y<N" = fallback clip for BACK if the ink key is not used. Positions come from the v1 QC frames (mid-shot, +-30 px): re-read on first / middle / last frame.

| Shot | Frames (s) | Faces + face guard (cx,cy,rx,ry) | BACK (behind people, keyed) | FRONT (on top, safe regions) | L |
|---|---|---|---|---|---|
| **c01** jar alone, hook | 0-132 (0.00-4.40) | No faces. Jar x 27-365, y 1160-1840. Well mouth ~(610,1372). Sky y<620. | `RaySwap pulse` NOON, O=(540,640), at 10, 22, 34 (one per drop landing). f112-132: `SpeedLines` F=(600,420), n 46, r0 380. | **f0:** 3 white drops h 300 already falling, x 612 / 628 / 598, y = 1372 - 46*(land - f), land = 10 / 22 / 34. Each lands with `Crown` w 300, W. **f45 "She (left)":** empty drop h 420 at (800,360): outline draws on in 12 frames (stroke-dashoffset), then bobs. **f69 "her":** `JarTicks` x7, cx 205, cy 1140, out 104. **f112 "Why?":** empty drop removed (shrink 4 frames from 108); `WhyStar` at (600,420), R 330 / r 210, text `WHY?` 230 px, rock 2 deg once; swell 126-132 floods YEL. | 5 |
| **c02** she walks | 132-240 (4.40-8.00) | Her face (535,810,105,120). Jar on shoulder x 325-500, y 675-920. Sky y<610. | **f139 "noon":** `RaySwap sweep(139,157)` NOON, O=(510,560), then spin 0.15. Stays to the cut. `DotField sun` O=(510,560), R 430, ORG dots, from f150. | Nothing on her. FRAME only. (The sky is the show.) | 4 |
| **c03** Jesus tired | 240-348 (8.00-11.59) | Jesus face (390,810,130,150). Sky y<600. | `DotField crawl` W, r 6, speedY -0.6, opacity 0.6, **clipped to y < 260 only** (His hair top is y ~690: 430 px clear). Nothing else. No ray swap: the art's sun is over His head, any new ray there reads as a halo. | Nothing. | 1 |
| **c04** "Give me to drink" | 348-434 (11.59-14.47) | Jesus (205,800,135,150). Woman (850,775,120,135). His hand ~(580,1040). Sky y<640. | `RaySwap pulse` NOON, O=(560,700), at 351, 360, 376. | `Balloon` (90,205)-(900,600), tail tip (300,640). Pops at f348 (`pop`). Words `Slam`, K fill, no shadow: `GIVE` f351, `ME` f360 (row 1, baseline y 370, 150 px), `TO` f369, `DRINK.` f376 (row 2, baseline y 530, 150 px), left edge x 150. **f380:** empty drop h 170 pops inside the balloon at (800,440), tips +-12 deg once (f392-410). Balloon and all leave on the cut. | 4 |
| **c05** her surprise | 434-568 (14.47-18.95) | Her face (620,715,190,235). Shawl x 245-755, y 400-1080. Jar x 650-1050, y 1130-1750. Whole background is rays. | **f436-470:** `SpeedLines` F=(600,720), n 54, r0 560 (boil). **f470-562:** same lines, no boil, n 28. | **f436, 440, 444:** 3 ticks, len 220, at (150,330) ang -132, (260,205) ang -112, (420,135) ang -92. Out 500. **f540 "drink (of me)":** empty drop h 300 pops at (910,330); tips +-12 deg twice f549-566 (a question). | 4 |
| **c06** kept apart | 568-683 (18.95-22.78) | Jesus (325,1040,90,100). Woman (880,945,90,100). Well + lid x 380-760. Sky y<600. | **f607 (gutter lands) to f665:** two `RaySwap snap`: `LEFT` clipped to x<578, `RIGHT` clipped to x>622, both O=(540,640), spin 0. **f665-678:** both removed by `iris` closing (r 2600 to 0) centred (760,380). | **f602 "kept":** `Gutter(600)` slams, lands f607 (+ foot ticks). FRAME thump 607. **f640:** empty drop h 200 pops at (430,380). **f658 "asks":** it hops (430,380) to (760,380) in 14 frames, arc top y 180, rot -15 to +15. At f664 (crossing x=600) the gutter segment y 200-560 breaks into `Shards`. **f665 "anyway":** upper gutter piece (y 0-200) slides up out, lower piece (y 560-1920) drops out, 8 frames `Easing.in(quad)`. Drop lands f672 with 3 ticks len 110 at (690,520) -150, (760,510) -90, (830,520) -30. | 4 |
| **c07** "thirst again" | 683-801 (22.78-26.70) | Jesus (355,760,165,190). His hand ~(890,1350). Free: x 540-1080, y 0-850. | **f771 "thirst":** `RaySwap front(771,797,"down")` DRY, O=(700,900): the colour drains out of the sky, top to bottom. Holds to the iris. | **"this water":** 3 white drops h 220 fall in, launch 739 / 747 / 755, 12 frames each, to (640,250) (815,205) (975,265). **f771 / 778 / 785:** each empties top to bottom in 7 frames (`lv` 1 to 0). **Type `Slam`:** `THIRST` f771, centre (765,520), 150 px; `AGAIN` f781, centre (765,680), 150 px. Fill W, K stroke 14, K shadow. Rest angle -4 deg. | 4 |
| **c08** down the well | 801-981 (26.70-32.70) | No faces. Art's colour disc centre (540,1080), r ~230. Almost all B&W: **everything here is FRONT.** | None. | **f829 / 836 / 843 "different water":** 3 `Ripple` C=(540,1080), r 240 to 700, W. **f866 "gift":** FIRST TEAL. 8 teal drops h 240 jump out of the disc toward us: v1 `SPRING` logic, ring radius 560 x / 700 y, launch 866 + 4i, flight 16 frames, grow 0.12 to 1; 3 `Ripple` TEAL at 866, 874, 882 (r 240 to 900). **f920 "Drink":** 12 more teal drops h 170, ring radius 380 / 480, launch 920 + 2i. All bob. **f940-956:** `Flood` C=(540,1080) swallows everything. **Type `Slam` on the flood:** `SHALL` f952, centre (540,620), 200 px; `NEVER` f958, centre (540,880), 250 px; `THIRST` f967, centre (540,1150), 250 px. Fill W, K stroke 16, DEEP shadow. Rest angles -3, +2, -2 deg. Type holds to f981. | 5 |
| **c09** her face | 981-1125 (32.70-37.49) | Her face (665,975,235,325). Head + shawl x 30-920, y 500-1680. Free: y<450, and x>930. | **From f981:** `RaySwap snap` WATER, O=(560,760), spin 0.2. The rays behind her are now water. Holds to the cut. | **f1001 "Life":** `Stream(1010, 1001)` up the right edge (never stops). **f1001 + 9i:** 7 teal drops h 190 rise up the right lane and settle over her head line, v1 `Rise` paths, ends (1005,640) (960,400) (820,215) (600,150) (300,165) (120,300) (75,450). **f1069 "spring":** `Crown` w 260 TEAL at (600,150) and (300,165). | 4 |
| **c10** truth about her life | 1125-1341 (37.49-44.68) | Woman (195,895,135,150). Jesus (765,935,140,160). Sky y<700. | `DotField crawl` W, r 6, speedY -0.5, opacity 0.5, clipped y<620. | 3 teal drops h 190 already hanging when the wave drains: (180,270) (560,215) (900,300). Bob only. Nothing pops. **No count of five. Nothing at "five husbands".** | 2 |
| **c11** "the Christ will come" | 1341-1463 (44.68-48.75) | Her face (285,1010,115,125). Arm up to ~(580,865). Sky y<720. | **f1432 "will":** `RaySwap sweep(1432,1456)` NOON, O=(560,655), spin 0. **Everything is still from f1456.** | FRAME thump 1341. `Rays` (v1 dot rays), o=(560,655), 9 rays, dot stroke 36 / 24, r 210 to 900, a 1400 ("promised"), b 1432. | 3 |
| **c12** "I that speak unto thee am he" | 1463-1569 (48.75-52.27) | Jesus face (540,640,210,310). Hair x 160-930, y 150-1080. | **None. InkTop off.** | One calm caption `Slab` W, (90,1290)-(990,1510), wipes on left to right f1466-1478 (`SINE`). Words `Step`, K, 96 px: row 1 baseline y 1385, centred: `I` 1470, `THAT` 1479, `SPEAK` 1489, `UNTO` 1499, `THEE` 1511. Row 2 baseline y 1480, centred: `AM` 1540, `HE.` 1544. No motion after 1544. Slab is 380 px below His beard. | 1 |
| **c13** her tears + silence | 1569-1654 (52.27-55.10) | Her face (510,1080,190,250). Shawl x 30-840, y 510-1920. Free: y<480. | **Slow well-up:** `WaveBody` TEAL at opacity 0.55, `yTop` from 1150 to -80 over f1580-1640 (`SINE`), wave speed halved (use f*0.08 / f*0.11). Behind her only. Still water from 1640. **If any teal fringe shows on her face or tear at 2x zoom: delete this and leave c13 plain.** | **Nothing.** | 1 |
| **c14** she leaves the jar | 1654-1738 (55.10-57.90) | Back view, no face. Her figure box x 470-610, y 690-900 (guard (540,790,90,125)). Jar x 325-675, y 1190-1840. Sky y<280. | **f1700 ("back to town"):** `RaySwap sweep(1700,1725)` WATER, O=(540,330), spin 0.1. The water is going to town. | **f1665 "her (jar)":** 5 ticks len 200 left of the jar, cx 335, cy 1290, angles -200, -178, -156, -134, -112 (v1 place). **Puffs** r 70 / 55 / 40 at (250,1215) f1668, (330,1150) f1680, (420,1080) f1692. Check she is past each spot. | 3 |
| **c15** "Come, see a man" | 1738-1978 (57.90-65.90) | Woman (580,945,100,105). Others (95,1065,80,90) (285,960,80,90) (930,1065,80,90). Sky y<300. | `RaySwap` WATER continues, O=(540,330), spin 0.1. | `Balloon` (110,210)-(970,450), tail tip (590,800). Wells up f1738-1750 (`SINE`, no back ease). Words `Step`, K, 120 px, one row, baseline y 375: `COME,` 1739, `SEE` 1772, `A` 1789, `MAN` 1793. **f1905:** those 4 words go off (cut, no fade). Same balloon: `IS` 1915, `NOT` 1951, `THIS` 1958 (row 1, baseline y 320, 100 px), `THE` 1977, `CHRIST?` 1979 (row 2, baseline y 420, 100 px). **f1739 and f1749:** 2 `Ripple` TEAL from (580,945), r 130 to 900, 40 frames (masked by FaceGuard). | 3 |
| **c16** many come | 1978-2128 (65.90-70.90) | Crowd faces: guard = full-width rect y 1130-1460. Sky y<650. | `RaySwap` WATER, O=(540,675), spin 0.15. **f2073-2128:** `SpeedLines` F=(540,380), n 40, r0 520. | Balloon from c15 stays, **tail removed at f1978**, leaves at f1998 (shrink 6 frames). **f2004 "Many":** 14 teal drops h 170 `well` (24 frames), 4 frames apart, left to right along an arc: x = 70 + 72i, y = 560 - 330*sin(PI*i/13), i = 0..13. They bob in place. **f2068:** drops i=2..11 shrink out (6 frames) to clear the slab. **f2073 "call":** YEL `Slab` (80,215)-(1000,585) `pop`. Words `Slam`, K fill, no stroke: `THE` 2086, `SAVIOUR` 2092 (row 1, baseline y 375, 150 px), `OF` 2102, `THE` 2114, `WORLD` 2119 (row 2, baseline y 530, 150 px). Slab holds across the cut. | 4 |
| **c17** the jar stayed | 2128-2264 (70.90-75.44) | No faces. Jar ~x 55-380, y 1150-1840 (drifts). Sky y<650. | **f2255-2264:** `SpeedLines` F=(600,380), n 46, r0 300. | Slab from c16 holds to f2150, then slides up off frame in 6 frames. **f2140 "jar":** `JarTicks` x7, cx 215, cy 1130, out 2186. **f2200 "She":** empty drop h 420 pops at (600,380), screen-fixed (not pinned to the jar). **f2255 "found":** it fills TEAL bottom to top, 2255-2263. | 4 |
| **c18** Jesus with the people | 2264-2445 (75.44-81.48) | Jesus (370,935,130,145). Others (80,970,80,90) (650,1080,80,90) (810,1080,85,95) (1010,945,80,90). Sky y<700. Bottom rays y>1700. | `DotField crawl` TEAL, r 7, speedY -0.6, opacity 0.7, clipped y<620. `WaveBody` TEAL `yTop` 1790, opacity 1, slow wave (f*0.08 / f*0.11): water at the people's feet, keyed behind the rug. | 5 teal drops h 170 already hanging when the iris opens: (140,260) (330,470) (620,200) (850,420) (950,215). Bob only. **Not in an arc. Nothing within 300 px of His head.** | 2 |
| **c19** empty tomb + hold | 2445-2636 (81.48-87.87) | No faces. Door keep-out x 480-840, y 1150-1650. Sunrise ~(550,860). Olive branch x 675-1080, y 620-1270. | **f2445-2510: nothing.** **f2510 "rose":** `RaySwap iris(2510,2570,1500)` DAWN at opacity 0.6, O=(550,860), spin 0.05, clipped y<860. | **f2510 + 6i:** 7 `Flower` r 60, `well` 36 frames, at x 150, 290, 420, 560, 700, 830, 950, y 1840 +- 20. Sway only. **f2522-2560:** `Rays` (v1), o=(550,860), 7 rays, upward, r 250 to 900. **Nothing new after f2575. Nothing in or near the door. Last frame = tomb, flowers, sunrise. No fade.** | 1 |

Counts: 19 of 19 shots have something living. Loud (L4-5): 10 shots. Calm (L1-2): 6 shots. 8 word items.

---

## 4. Transitions (all 18 cuts)

10 graphic, 8 hard. Rule for every cover/reveal: the reveal opens **from the face outward**, so the face is the first thing clear.

| # | Cut (frame) | Type | Exact build | Why |
|---|---|---|---|---|
| 1 | c01>c02 (132) | **GRAPHIC: question flood** | v1 T4, bigger. `WhyStar` swell 126-132 to full YEL. f132-142: `DotField wipe` reveal, YEL, ang 45 deg, pitch 54. | The question throws us into the story. |
| 2 | c02>c03 (240) | HARD | - | First sight of Jesus. Plain. |
| 3 | c03>c04 (348) | HARD + thump | FRAME thump 348; balloon pops on the cut. | His first words carry the cut. |
| 4 | c04>c05 (434) | **GRAPHIC: dot wipe** | `DotField wipe` ORG, ang 0 deg (left to right): cover f426-434, reveal f434-442 (reveal also left to right; her face x 620 is clear by f439). | Her reaction snaps in. |
| 5 | c05>c06 (568) | **GRAPHIC: shutters** | `Shutters(562, 568, 574, 600)`. | "Kept apart": the page closes into two halves. The gutter then lands on the same x. |
| 6 | c06>c07 (683) | **GRAPHIC: dot wipe** | `DotField wipe` YEL, cover f677-683 right to left (ang 180), reveal f683-690 left to right (His face x 355 clear by f686). | "He asks anyway": the wall is gone, we go to Him. |
| 7 | c07>c08 (801) | **GRAPHIC: well iris** | v1 T1 unchanged: circle from (1000,1590), f801-813, c07 tail from `waw_c07.mp4` (startFrom 118), ring K 14 + **W** 10 (was teal; teal is not allowed yet). The c07 BACK/FRONT layers ride inside the outgoing mask. | He points at the well. We go in. |
| 8 | c08>c09 (981) | **GRAPHIC: the flood** | Flood is solid TEAL from f956. f981-995: `DotField radialHole(981,995,(650,1000),1500,TEAL)`; the 3 type lines are in the same layer and are cut by the same hole. Her face is clear by f984. **No vector copy of the art's disc anywhere (that was the v1 colour pop at f965).** | "Shall never thirst": the water fills the page, and she is in it. |
| 9 | c09>c10 (1125) | **GRAPHIC: wave** | `WaveBody` TEAL (TRANS layer, opacity 1): `yTop` 1980 to -80 over f1109-1125 (`Easing.in(quad)`); then the same body's **top edge** goes -80 to 1990 over f1125-1141 (`Easing.out(quad)`), so it drains down and faces (y ~900) are clear by f1132. | "A spring that never runs dry." |
| 10 | c10>c11 (1341) | HARD + thump | FRAME thump 1341. | Heavy line before it. Keep it plain. |
| 11 | c11>c12 (1463) | HARD | Nothing moves from f1456. | The cut IS the answer. |
| 12 | c12>c13 (1569) | HARD | - | Sacred. |
| 13 | c13>c14 (1654) | HARD | - | After the silence. |
| 14 | c14>c15 (1738) | **GRAPHIC: ink bars** | `Bars(1730, 1738, 1748, [TEAL, W, TEAL, W, TEAL])`. | She goes to town, and the water goes with her. |
| 15 | c15>c16 (1978) | **GRAPHIC: ripple (no cover)** | 3 `Ripple` TEAL from (580,945): launch 1964, 1970, 1976; r 130 to 1500 in 30 frames; they keep growing across the cut. Balloon also crosses the cut. Nothing covers a face (rings are masked by FaceGuard of the shot on screen). | Her call goes out. Many come. |
| 16 | c16>c17 (2128) | HARD + thump | FRAME thump 2128. Saviour slab crosses the cut. | "The jar stayed." lands flat. |
| 17 | c17>c18 (2264) | **GRAPHIC: drop iris** | v1 T3, new origin `T3_O = (600,380)`, start half-height 210 (the drop's own size), to 2600 over f2264-2278, `INOUT`. c17 tail from `waw_c17.mp4` (startFrom 136). Edge = K line 12. | "Better water: Jesus." The better water is Him. |
| 18 | c18>c19 (2445) | HARD | - | The tomb arrives in quiet. |

---

## 5. Kinetic type list (8 items, exact strings)

All from `words/FINAL_WORDS_v1.md`. Items 2-8 are KJV quotes in the narration. Copy-paste these strings.

| # | String on screen | Frames (word starts) | Out | Where | Style |
|---|---|---|---|---|---|
| 1 | `WHY?` | 112 | swells 126-132 | c01 star, centre (600,420) | Bangers 230, K fill, W stroke 10, in YEL burst star. (Kept from v1.) |
| 2 | `GIVE ME` / `TO DRINK.` | GIVE 351, ME 360, TO 369, DRINK. 376 | cut 434 | c04 balloon, rows y 370 / 530, left x 150 | `Slam`, 150, K fill, in W balloon with tail to Jesus. |
| 3 | `THIRST` / `AGAIN` | 771, 781 | iris 801-813 | c07 right sky, centres (765,520) (765,680) | `Slam`, 150, W fill, K stroke 14, K shadow, -4 deg. |
| 4 | `SHALL` / `NEVER` / `THIRST` | 952, 958, 967 | hole 981-995 | c08 on the teal flood, centres y 620 / 880 / 1150, x 540 | `Slam`, 200 / 250 / 250, W fill, K stroke 16, DEEP shadow. |
| 5 | `I THAT SPEAK UNTO THEE` / `AM HE.` | I 1470, THAT 1479, SPEAK 1489, UNTO 1499, THEE 1511, AM 1540, HE. 1544 | cut 1569 | c12 W slab (90,1290)-(990,1510) | **`Step` (calm)**, 96, K fill, no stroke, no motion. |
| 6 | `COME, SEE A MAN` | COME, 1739, SEE 1772, A 1789, MAN 1793 | 1905 | c15 balloon, baseline y 375 | **`Step`**, 120, K fill. |
| 7 | `IS NOT THIS` / `THE CHRIST?` | IS 1915, NOT 1951, THIS 1958, THE 1977, CHRIST? 1979 | 1998 | same balloon, baselines y 320 / 420; crosses the cut | **`Step`**, 100, K fill. |
| 8 | `THE SAVIOUR` / `OF THE WORLD` | THE 2086, SAVIOUR 2092, OF 2102, THE 2114, WORLD 2119 | slides up 2150-2156 | c16 YEL slab (80,215)-(1000,585); crosses the cut | `Slam`, 150, K fill. **Spelling is SAVIOUR (KJV).** |

Not on screen, on purpose: no count of "five", no "JESUS" title, nothing at the tomb. Width check: if any row is wider than its box minus 60 px, lower that row's font size in steps of 6 px until it fits. Never squeeze letters.

---

## 6. Build order

1. **Prove the ink key first (30 min).** Stills at f500 (c05), f1050 (c09), f1500 (c12), f1610 (c13), f2350 (c18) with BACK = a flat magenta full-frame rect. Pass = magenta only where rays were; every face, hand, robe, stone is clean at 2x zoom. Tune `-6` / `1.5`. If it cannot pass on c09 and c13, use the sky-rect fallback for those shots.
2. FaceGuard masks + a `DEBUG` flag that draws all guard ellipses and keep-out boxes in red.
3. D9 frame, D2 RaySwap, D3 DotField, D6 SpeedLines (the BACK set).
4. **Showpiece test: f683-1141 (c07 to c10 start).** Render it. Stop and show the owner this 15 s before building the rest.
5. D5 water kit rest, D8 stickers, D4 gutter/shutters, D7 bars.
6. D10 type (all 8 items) - paste strings from section 5.
7. All 10 graphic transitions.
8. Calm shots last: c03, c10, c12, c13, c18, c19.
9. Full render (no audio), mux audio from `waw_base_v2.mp4`, run `check_landing_hold.py`.

Output: `poc_pop_halftone/woman_at_well/motion_v2/WOMAN_AT_WELL_MOTION_v2.mp4` + a QC page `motion_v2/_QC_v2.html` (frame grabs, big, click to zoom). Do not auto-open anything.

---

## 7. Self-QC checklist (builder ticks every line)

**Frame grabs to make and look at (at 2x zoom on every face):**
f5, f22, f80, f120, f134, f150, f230 | f300 | f380, f430, f436, f445, f550, f565, f570, f607, f664, f672, f680, f686 | f760, f790, f806 | f845, f880, f935, f950, f970, f983, f990 | f1060, f1118, f1128, f1135 | f1250 | f1440, f1460 | f1480, f1550 | f1575, f1610, f1650 | f1670, f1720, f1736, f1742 | f1800, f1960, f1976, f1980, f1995 | f2030, f2100, f2125, f2135, f2152 | f2210, f2260, f2268, f2275 | f2350, f2440 | f2450, f2500, f2540, f2580, f2635.

- [ ] **Faces:** no graphic pixel on any face of Jesus or the woman on any grab, except inside the 10 transition windows. In those windows a face is covered for 8 frames or less, and never distorted.
- [ ] Jesus: nothing forms a ring, arc or glow round His head (c03, c04, c07, c10, c12, c18).
- [ ] Ink key: no colour fringe on skin, tears, beard, hands. Black ray lines of the art sit on top of our colours.
- [ ] **Words:** each of the 8 strings matches section 5 letter for letter (SAVIOUR, UNTO, THEE). Each word appears on its own frame +-1. All type inside x 60-960, y 200-1540.
- [ ] **Sacred beats calm:** c12 = slab + stepped words only, no thump, no slam. c13 = slow teal rise only (or plain). c19 = nothing before f2510, nothing new after f2575, last frame is the tomb.
- [ ] No TEAL anywhere before f866.
- [ ] No vector copy of the art's colour disc in c08. No colour pop near f965.
- [ ] No zigzag "crack" in c06 (it is a straight panel gutter now).
- [ ] Base film untouched: same cuts, 1.0x, no zoom, no freeze, no reverse. Diff a clean frame (f300 top-left 200x200 px outside the border) against the base.
- [ ] No object is pinned to a moving thing (jar ticks sit above the jar's mid-shot spot; check first and last frame of c01, c14, c17 that ticks do not touch the jar).
- [ ] Every shot has something moving (c03: top dots; c12: words; c13: water or leave plain and say so).
- [ ] Audio = base audio, same length. Landing hold >= 3.0 s after "day." (ends f2542; file ends f2636).
- [ ] $0: no image or video model was called.

## 8. Risks, in order

1. **Ink key edge on faces** (c09, c12, c13). Guarded by step 1 + FaceGuard + the "delete it" rule on c13.
2. **Too loud for the story.** The loud part ends at f1141. After that only c16 goes to L4. If the owner finds it too much, the first things to drop are: c05 speed lines, the c14>c15 bars, c16 speed lines.
3. **Type covers the hill/town** in c15-c17 (not faces). Accepted. If it bothers, shrink the balloon to y 210-400.
