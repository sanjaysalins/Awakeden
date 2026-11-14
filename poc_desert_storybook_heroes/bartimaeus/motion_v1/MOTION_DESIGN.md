# Blind Bartimaeus (Desert Storybook) - Motion layer v1 "THE ROAD STOPS" (design only, $0)

Owner ask: "a BOLDER and FULLER Remotion motion graphics to elevate this episode."
Build spec. The builder makes no creative choices. Where a number is given, use it.

- Comp: 1080x1920, 30 fps, **2375 frames** (79.17 s). Suggested comp `BartimaeusV1`.
- Base: `film/bartimaeus_final_v1.mp4`, 1.0x, never re-cut. Audio muxed from it after render.
- All frames are ABSOLUTE comp frames. Seconds = frame / 30.
- Cuts (from SHOT_PLAN; **measure the real cut frames first, +-1**):
  `CUT = [0,90,150,300,450,624,798,900,1011,1152,1254,1344,1470,1680,1830,1950,2070,2375]`
  = s01 s02 s03 s04 s14 s05 s06 s07 s08 s09 s10 s11 s12 s13 s15 s16 s17, end.
- **Word frames here are ESTIMATES** from line timings (`audio/timeline.json`), marked `~`. Step 1 of the build: force-align `audio/narration.mp3`, check the offset against the film, and replace every `~` frame.
- Positions were read off the 17 stills (one still per shot, scaled to 1080x1920, +-25 px). Clips move: re-read every box on the first / middle / last frame of its shot.
- No `Math.random`. Use `hash(i) = fract(sin(i*127.1+311.7)*43758.5453)`.

---

## 1. Spine, palette, type

**Spine, one line: a whole road is moving and a blind man sits in the dark; one cry makes the road STOP; the dark opens into light; the road moves again with him on it; and at the last line it stops once more, "for one man."**

Three parts, one story, all tied to the score:

| Part | What it is on screen | Story | Score |
|---|---|---|---|
| **THE ROAD** (D1) | A river of painted dust strokes that marches across the frame on the walking beat | The crowd that will not stop | Walking music. **Stops dead at f768 (25.6 s).** Returns f1680. Stops again ~f2205. |
| **THE DARK** (D3) | A brushed umber edge round the page + a slightly dull grade | His blindness | Lifts at f1470 (cello sings the whole tune) |
| **THE CRY** (D2) | Maroon brush rings from his mouth + his KJV words, growing | The one voice | Hook, then louder at f693 |

After f1470 the dust strokes come back as **gold light motes**. Same shapes, new colour: the road he sat beside is now the road he can see.

### Palette (hex, sampled from the art)

| Name | Hex | Use |
|---|---|---|
| PAPER | `#F6E9CC` | main lettering fill, page sweep |
| SAND | `#E3C48D` | dust strokes (before f1470) |
| UMBER | `#2E211A` | letter outline, the DARK edge, "be quiet" |
| MAROON | `#7A2E22` | Bartimaeus only: his cry, his rings, "ONE MAN" (his cloak colour) |
| SAGE | `#5E7F6C` | Jesus's words only (His mantle colour) |
| GOLD | `#E9B043` | light: motes, "SEE", "HE ROSE" - **never before f1470** |
| GLOW | `#FFF2C9` | light wash, mote highlights |

Colour rules: MAROON = him. SAGE = His words. GOLD only after sight. No GOLD ring, arc or glow round Jesus's head, ever.

### Type

- **Display: Fraunces 800** (Google Font; set `opsz` 144, `SOFT` 100). ALL CAPS, letter-spacing 2. Warm picture-book serif. Used for story words.
- **KJV lines: Fraunces 600 Italic**, sentence case, exact punctuation.
- **Notes / labels: Kalam Bold** (`public/Kalam-Bold.ttf`).
- No Bangers. No Permanent Marker.
- Every display letter: fill + UMBER stroke 10 px (`paintOrder: stroke`, round joins) + flat UMBER shadow copy offset (5,6) at opacity .45. Then filter `#gouache` (D4).
- Text safe box (Shorts UI): **x 60-1020, y 200-1540**.

---

## 2. Layer stack (bottom to top)

1. `Base` - `OffthreadVideo`, inside a `Stage` div that takes D6 transforms (scale / shake) and the D3 grade filter.
2. `DARK` - D3 umber edge, `mix-blend-mode: multiply`. FaceGuard masked.
3. `ROAD` - D1 dust strokes / light motes. FaceGuard masked.
4. `MARKS` - D2 rings, D5 road line, cloak streaks, light wash. FaceGuard masked.
5. `TYPE` - D4 lettering. Not masked (placed by hand in free areas, section 5).
6. `TRANS` - D7 page sweeps and dust wipes.
7. `GRAIN` - static paper tooth: `feTurbulence baseFrequency 0.9, seed 7`, opacity .05, `multiply`. Whole film.

**FaceGuard:** one SVG `<mask>` per shot: white frame, black ellipses and boxes from section 5, feather 0. A `DEBUG` flag draws every guard in red.

---

## 3. Devices (7)

### D1. THE ROAD (dust river, then light motes)
- 46 strokes. Stroke i: a tapered brush dash = a lens-shaped path, length `70 + hash(i)*130`, thickness `8 + hash(i+9)*14`, fill SAND, opacity `.30 + hash(i+5)*.35`, with the `#gouache` edge.
- Lives in two places only: **ground band y 1500-1900** and **edge lanes x 0-110 and x 970-1080** (y 250-1500). Never in the centre of the frame.
- Motion: each stroke moves along direction `dir` at `speed * (0.7 + hash(i+2)*0.6)` px/frame and wraps. **Step bob:** all strokes hop `-10 * |sin(PI * f / STEP)|` px. `STEP` = frames per footstep of the score (measure it; default 16).
- Props per shot: `dir` (deg, 0 = right, -90 = up), `speed`, `gain` (opacity multiplier).
- `halt(f0)`: from f0 every stroke keeps its position. No ease. It just stops. Bob stops too.
- `MOTES` mode (after f1470): fill GOLD with a GLOW core, length x0.35 (short flecks), `dir` -90, speed 1.6, bob off, slow sway `x += 6*sin(f/40 + i)`. Allowed in the whole frame outside FaceGuard. 60 flecks.

### D2. THE CRY (rings)
- A ring = an arc, not a full circle: centre `M` (his mouth), span 110 deg centred on angle `a`, stroke MAROON width 30 with a PAPER stroke 8 on its outer side, `#gouache` edge, round caps.
- Life: radius `r0` to `r1` over 26 frames, `Easing.out(cubic)`; width 30 to 6 over the last 10 frames; then gone.
- `Cry(M, a, n, at, r0, r1)`: n rings, launched 5 frames apart from `at`.

### D3. THE DARK (edge + grade) and its opening
- Edge: full-frame UMBER rect with an **evenodd hole**. Hole = rounded rect inset by `T` px, corner radius 120, its outline wobbled: sample 120 points, offset point k by `22*sin(k*0.9) + 12*sin(k*2.3)` px. No blur. Opacity .58, multiply. A second copy inset by `T+60` at opacity .25 gives a brushed double edge.
- `T` per shot is in the beat table (60 = light, 150 = heavy). Changes between shots are instant on the cut.
- Grade on `Stage` while the DARK is on: `saturate(.86) brightness(.97)`.
- **OPEN (f1470-1520):** `T` goes 190 to -200, `Easing.out(cubic)`, 50 frames (the hole grows past the frame). At the same time one GLOW ring (stroke 26, opacity .8 to 0) grows from **r 300 to r 1500**, centred on his eyes (677,756), and the grade eases to `saturate(1.06) brightness(1.02)` and stays there to the end. The ring starts outside his face guard, so it never crosses his eyes.
- After f1520 the DARK never returns.

### D4. LETTERING
- `#gouache` filter (dry-brush edge): `feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"` into `feDisplacementMap scale="7"`. Fixed seed: letters do not boil.
- `Stamp` (loud): on at its frame, scale 1.28 to 1 in 6 frames `Easing.out(back(1.4))`, rotate from `(hash(i)-.5)*6` deg to rest.
- `Set` (calm): opacity 0 to 1 in 8 frames, y +10 to 0, `Easing.out(cubic)`. No scale.
- `Still` (sacred): on at its frame. Nothing else.
- `Ribbon(x0,y0,x1,y1,col)`: a painted band behind KJV speech: rect with `#gouache` edge, fill `col` at .88, each end cut with 2 brush notches. Wipes on left to right in 10 frames.
- `Swash`: a brushed underline, tapered path 14 px thick, draws left to right in 8 frames.
- Exits: on the cut unless the table says otherwise.

### D5. THE ROAD LINE
- A dashed painted path: dashes 34 long, 12 thick, gap 26, PAPER fill, UMBER stroke 4. Dashes appear in order: one per 2 frames, or one per `STEP/2` frames when the table says "in step". Follows the polyline in the table (Catmull-Rom through the points).

### D6. STAGE moves (on the live clip)
- `Punch(at, s)`: scale 1 to `s` in 4 frames, back to 1 over 22 frames `Easing.out(cubic)`. Origin given per use.
- `Shake(at, amp, n)`: for k = 0..n, offset = `amp * (1 - k/n) * (sin(k*2.9), cos(k*3.7))`.
- `Drift(s0, s1)`: slow scale across a whole shot, linear. Max 1.04.
- Stage scale is exactly 1.0 on the sacred shots (s06, s15, s16).

### D7. TRANSITIONS
- `DustWipe(cut, dir, col)`: a band 700 px wide (default SAND) with ragged `#gouache` edges and 20 D1 strokes riding in it, opacity .92. It crosses the frame in 12 frames (cut-6 to cut+6); its centre is on the frame centre at `cut`.
- `PageSweep(cut, n)`: a PAPER sheet (1300 wide, full height) slides right to left over n frames, centred on `cut`. Leading edge: curved (quadratic bulge 60 px) with a 90 px shadow gradient UMBER .35 to 0. Trailing edge the same, mirrored. GRAIN shows on it.
- `Press(cut)`: DARK `T` jumps to 260 at `cut` and eases to the new shot's `T` in 8 frames.

---

## 4. Beat table (whole film)

`T` = DARK thickness. ROAD = `dir / speed / gain`. All text strings are exact: copy-paste them.

| Time (frames) | Shot | Motion layer | Words on screen (exact) | Why |
|---|---|---|---|---|
| **0.0-3.0** (0-90) | s01 he shouts | T 150. ROAD 180 / 5 / .8, ground band only (the crowd passing). `Drift` 1.04 to 1.0 over f0-20, so frame 0 is alive. **f8:** `Cry(M=(518,610), a=-90, n=3, r0 140, r1 520)`; again at **~f52** ("mercy"). FaceGuard cuts the rings. | Kalam 40 PAPER, centre (540,215), on from f6: `Jesus, thou Son of David,` Row 1 `HAVE MERCY` Fraunces 112 MAROON, centre (540,302). Row 2 `ON ME` 112, centre (540,400). `Stamp`: HAVE ~f50, MERCY ~f56, ON ~f68, ME ~f74. | First-frame hook: a voice you can see. Words sit on the crowd's robes above his hair (hair top y~420). |
| **3.0-5.0** (90-150) | s02 crowd hushes | Cut = `Press(90)`. T 150. **f96 (hush SFX):** ROAD gain drops to .3 in 6 frames. One maroon ring at M=(350,1010), r 260, a=-60, is **pressed flat**: scaleY 1 to 0 over f96-104. | `BE QUIET!` Fraunces 118, UMBER fill, PAPER stroke 10, rotate -3 deg, centre (790,1010) (on the robes, below all faces). `Stamp` ~f120. | The crowd's answer presses his cry flat. |
| **5.0-10.0** (150-300) | s03 Jericho road | Cut = `DustWipe(150, 0)`. T 60. ROAD 160 / 4 / 1.0, ground band + right lane (crowd walks toward us). `Drift` 1.0 to 1.03. | `BARTIMAEUS` Fraunces 104 PAPER, centre (720,1420), `Stamp` ~f165. MAROON `Swash` under it f172-180. Kalam 46 PAPER `a blind beggar by the road`, centre (720,1505), `Set` ~f195. **~f255 ("Jericho"):** `JERICHO` Fraunces 84, letter-spacing 10, PAPER, centre (700,300), `Set`. | Who and where, for a newcomer. The name sits on the empty road, right of him. |
| **10.0-15.0** (300-450) | s04 Jesus in the crowd | Hard cut + `Punch(300, 1.04)` origin (585,760). T 60. ROAD 90 / 5 / 1.0, both lanes + ground band (the crowd comes toward us). | Row 1 Fraunces Italic 64 MAROON `"Son of David"` centre (540,260), `Set` f303. Row 2 Kalam 44 PAPER `means` centre (540,330), ~f330. Row 3 Fraunces 96 PAPER `GOD'S PROMISED KING` centre (540,440), `Stamp` by word ~f340 / 352 / 366. All out by opacity f378-388. **No words after f388.** | The one hard phrase, in plain words. Text sits on sky and buildings, 240 px above His hair. It is a flat row, not an arch. |
| **15.0-20.8** (450-624) | s14 road to Jerusalem | Cut = `DustWipe(450, -90)` (we go up the road). T 60. ROAD bands off. **D5 road line** climbs the painted road from f456: (538,1680) (672,1363) (662,1277) (538,1162) (614,1037) (614,902) (480,826). **~f520 ("killed"):** a small UMBER cross mark (two brush strokes 12 px; 56 wide, 84 tall) draws in 10 frames at (480,740), where the line ends. `Drift` 1.0 to 1.03. | `JERUSALEM` Fraunces 96, letter-spacing 10, PAPER, centre (540,300), `Set` ~f468. **~f565:** `WOULD HE STOP` Fraunces 112 PAPER, centre (540,1240). **~f590:** `FOR A BEGGAR?` 112, `BEGGAR?` in MAROON, centre (540,1380). `Stamp` by row. | Where He is going, what waits there, and the question of the film. The cross mark is the only drawn symbol; it pays off at s15. |
| **20.8-26.6** (624-798) | s05 louder | Cut = `PageSweep(624, 12)`. T 150. ROAD 0 / 6 / 1.0, ground band + lanes. **~f640 ("louder"):** `Punch(640, 1.05)` origin (560,520). **Cry 2, f693 (23.1 s):** `Cry(M=(610,515), a=-50, n=5, r0 180, r1 1500)` + `Shake(693, 7, 14)`. A passing ring pushes ROAD strokes: any stroke within 80 px of a ring moves +14 px along the ring's normal for 6 frames. **f768 (25.6 s): `ROAD.halt`. Everything of ours stops.** f768-798: nothing moves. | Kalam 40 PAPER `Thou Son of David,` centre (535,215), on ~f695. Row 1 `HAVE MERCY` Fraunces 124 MAROON, x 240-830, baseline 300. Row 2 `ON ME.` 124, right-aligned to x 830, baseline 405. `Stamp`: HAVE ~f730, MERCY ~f738, ON ~f752, ME. ~f758. Words hold still f768-798. | Bigger than the hook: he will not be pressed flat. Then the road stops with the music. |
| **26.6-30.0** (798-900) | **s06 Jesus stood still (SACRED)** | **Hard cut. Stage 1.0, no drift.** T 60, not moving. ROAD: the same strokes, halted, hanging in the bands at gain .6. **Nothing of ours moves for 3 s** while the clip's crowd blurs past Him. **f888 (29.6 s, music back):** ROAD starts again, speed 0 to 3 over 12 frames. | Row 1 `AND JESUS` Fraunces 104 PAPER, centre (540,1420). Row 2 `STOOD STILL` 104, centre (540,1525). `Still`: AND ~f800, JESUS ~f810, STOOD ~f824, STILL ~f836. Kalam 38 PAPER `Mark 10:49`, right-aligned x 1010, y 1310. | One idea: the whole motion layer holds its breath. The moving crowd in the clip does the rest. Words sit on the blurred foreground robes, below His feet. |
| **30.0-33.7** (900-1011) | s07 He calls | Hard cut. T 60. ROAD 180 / 3 / .7 ground band. **~f985 ("called"):** 2 SAGE arcs (D2 shape, stroke 22, PAPER edge 6) from (1000,430), a=0, r 80 to 700. They run on across the cut. | Row 1 `HE STOPPED` Fraunces 92 PAPER, x 60-540, baseline 280, `Stamp` ~f925. Row 2 `FOR ONE MAN` 92, `ONE MAN` in MAROON, baseline 380, `Stamp` ~f945. | The point of the film in five plain words. The top-left sky is empty. |
| **33.7-38.4** (1011-1152) | s08 cloak off | Cut: the SAGE arcs keep growing f1003-1020 (no cover). T 150. ROAD off. **f1077 (whoosh, 35.9 s):** 5 MAROON brush streaks (tapered, 300-520 long, 18 thick) fan out from (300,560) at -150, -165, 180, 165, 150 deg over 10 frames + `Punch(1077, 1.06)` origin (620,560) + `Shake(1077, 6, 10)`. T 150 to 100 at f1077. | `HE CAME` Fraunces 100 PAPER, centre (600,262), `Stamp` ~f1085. Out by opacity f1125-1135. | The cloak was all he had. The hit lands on the SFX. The dark thins: he has left something behind. |
| **38.4-41.8** (1152-1254) | s09 Jesus asks | Hard cut. T 100. ROAD off. `Drift` 1.0 to 1.02. Nothing else. | `Ribbon` (80,1300)-(1000,1525) SAGE, on f1158-1168. Fraunces Italic 66 PAPER, no outline, `Set` by word from ~f1164. Row 1 `What wilt thou that I` baseline 1395. Row 2 `should do unto thee?` baseline 1485. | His words, exact KJV, in His colour. Quiet. The ribbon sits on robe hems, below every hand. |
| **41.8-44.8** (1254-1344) | s10 "my sight" | Hard cut. T 150 (the dark at its closest, just before it breaks). `Drift` 1.0 to 1.03 origin (530,600). | A word stack down the right wall, right-aligned x 1030, Fraunces Italic 62 MAROON, PAPER stroke 8, `Set` one per spoken word from ~f1262: `Lord,` y 330 / `that I` y 420 / `might` y 510 / `receive` y 600 / `my` y 690 / `sight.` y 800 at 84 px. | His whole request, one word at a time, beside his closed eyes. Column is x 790-1030; his nose tip is x~700. |
| **44.8-49.0** (1344-1470) | s11 "thy faith" | Hard cut. T 100. Only the words move. **f1464-1470:** T 100 to 190 (the dark closes one last time). | `Ribbon` (80,1300)-(1000,1525) SAGE, on f1350-1360. Fraunces Italic 66 PAPER, `Set` by word from ~f1356. Row 1 `Go thy way; thy faith` baseline 1395. Row 2 `hath made thee whole.` baseline 1485. | Jesus heals by His word, so His word is the only thing on screen. |
| **49.0-56.0** (1470-1680) | **s12 eyes open (HERO)** | Cut = **THE DARK OPENS** (D3 OPEN, f1470-1520). ROAD returns as `MOTES` from f1500, gain 0 to .8 over 30 frames. `Drift` 1.0 to 1.03 origin (677,756). **No ring, streak, mote or word in the eye box, ever.** | Nothing f1470-1590 but light. **~f1590 ("At once"):** row 1 `AT ONCE HE` Fraunces 72 PAPER, centre (800,265). Row 2 `COULD SEE.` 96, `SEE.` in GOLD, centre (800,365), ~f1612. `Set` by row. | The hero. The first 4 s are his eyes and the light only. Words wait for the narrator. First GOLD in the film. |
| **56.0-61.0** (1680-1830) | s13 he follows | Cut = `DustWipe(1680, -90, GOLD)`. T 0. MOTES off. ROAD dust strokes back, now **GOLD**, lanes + ground band, -90 / 4 / .9, bobbing in step with the footsteps SFX. **~f1795 ("Up the road"):** D5 road line "in step" from his feet: (317,1580) (470,1330) (590,1080) (615,820). All out by f1824. | `HE FOLLOWED JESUS` Fraunces 88 PAPER, centre (540,285), `Stamp` by word ~f1740 / 1752 / 1768. Out by opacity f1790-1800. Then Kalam 48 PAPER `up the road to Jerusalem`, centre (540,285), `Set` ~f1798. | Jesus said go; he followed. The road line from s14 is back, and now he is on it. |
| **61.0-65.0** (1830-1950) | **s15 the cross (SACRED)** | **Hard cut. Everything off:** no ROAD, no motes, no drift, no edge. | Row 1 `HE DIED` Fraunces 84 PAPER, centre (790,560). Row 2 `FOR OUR SINS` 84, centre (790,660). `Still`: rows on at ~f1868 and ~f1890. | One idea: still words in the open sky, right of the cross. The small mark at s14 was the promise. |
| **65.0-69.0** (1950-2070) | **s16 the tomb (SACRED)** | **Hard cut.** f1950-2000: nothing. **~f2000 ("rose", the warm lift):** a GLOW wash rises: linear gradient GLOW .28 to 0, top edge y 1920 to 700 over 60 frames, `Easing.inOut(sin)`, clipped out of the door box. 24 MOTES rise outside the door from f2010. | `HE ROSE TO LIFE` Fraunces 96 GOLD, centre (540,1440), `Set` (14 frames) ~f2005. Holds to the sweep. | Stillness, then one warm lift with the music. Nothing in or near the door. |
| **69.0-79.17** (2070-2375) | **s17 bookend + hold** | Cut = `PageSweep(2070, 16)` (the last page turns, in the pause). ROAD GOLD dust, right lane + ground band, 0 / 3 / .7 (the far crowd still walking). **~f2205 ("stood still"): `ROAD.halt`** - the second stop. 30 MOTES drift on slowly to the end. | Row 1 `JESUS STOOD STILL` Fraunces 84 PAPER, centre (540,255), `Still` by word ~f2190 / 2205 / 2218. Row 2 `FOR ONE MAN.` 84, `ONE MAN.` in MAROON, centre (540,350), ~f2240 / 2252. Kalam 40 PAPER `Mark 10:46-52`, centre (540,1500), `Set` f2300. **No fade. Nothing new after f2315.** | Same lettering as s06: the answer to the hook's cry. The road stops for him a second time. Last frame: both men, the sun, the words. |

Counts: 17 of 17 shots carry the spine. 14 word items. 7 graphic cuts, 9 hard cuts.

### Cut list (all 16)

| Cut | Frame | Type |
|---|---|---|
| s01>s02 | 90 | `Press` (hard cut + the dark squeezes in) |
| s02>s03 | 150 | `DustWipe` left to right |
| s03>s04 | 300 | HARD + `Punch` |
| s04>s14 | 450 | `DustWipe` upward |
| s14>s05 | 624 | `PageSweep` 12 f ("But...") |
| s05>s06 | 798 | **HARD, in silence. Nothing of ours moves.** |
| s06>s07 | 900 | HARD |
| s07>s08 | 1011 | SAGE call arcs cross the cut (no cover) |
| s08>s09 | 1152 | HARD |
| s09>s10 | 1254 | HARD |
| s10>s11 | 1344 | HARD |
| s11>s12 | 1470 | **THE DARK OPENS** (D3) |
| s12>s13 | 1680 | `DustWipe` upward, GOLD |
| s13>s15 | 1830 | HARD (sacred) |
| s15>s16 | 1950 | HARD (sacred) |
| s16>s17 | 2070 | `PageSweep` 16 f (last page) |

---

## 5. Face / eye safe zones (px, 1080x1920; ellipse = cx,cy,rx,ry)

| Shot | Keep clear |
|---|---|
| s01 | Face (518,560,135,165). Hands: x 150-460, y 650-900 and x 640-940, y 730-960. Bowl x 105-350, y 1350-1640. |
| s02 | Tall man (385,225,95,115). Woman (615,335,75,95). Shushing man (765,265,90,110) + his hand down to y 440. Right woman (1000,290,75,95). Left man (45,375,55,75). Small faces (370,455,48,58) (480,470,48,58) (435,540,32,38). Bartimaeus (335,975,135,135). Raised palm (530,575,55,75). Bowl + hand x 480-690, y 1070-1200. |
| s03 | Bartimaeus (262,1070,75,90). Crowd faces: band x 320-1080, y 830-1010. |
| s04 | Jesus (585,760,75,100). Crowd faces: full-width band y 800-1060. |
| s14 | No faces. Do not cover the temple block x 280-830, y 420-620. |
| s05 | Face + cupped hands (560,505,155,135). Left man (58,205,85,115). Woman (322,460,65,80). Far man (655,430,42,52). |
| s06 | Jesus (538,345,90,115); keep His whole figure clear: x 360-700, y 250-1350. Crowd faces: x 0-230 and x 650-1080, y 470-620. Foreground faces (60,740,75,95) (990,890,85,105). |
| s07 | Jesus (662,403,85,110). His raised hand (960,440,65,75). Man (370,520,75,90) + hand to x 470. Woman (206,600,65,80) + hand to x 290. |
| s08 | Face (653,545,80,90). Hands (990,455,60,60) (350,930,60,50). Crowd faces: y 960-1080, x 0-450 and x 620-1080. |
| s09 | Jesus (538,280,105,125). Bartimaeus (768,500,90,105). Jesus's open hand x 370-530, y 870-980. Crowd faces y 660-830. Bartimaeus's hands y 1150-1260. |
| s10 | Whole head x 160-705, y 220-870 (tear at (505,630)). Praying hands x 560-790, y 1000-1650. |
| s11 | Jesus (480,270,95,120). Bartimaeus (700,460,85,100). Hand on shoulder (640,700,50,50). Crowd faces (100,600) (52,770) (215,640) (865,680) (985,590), each r 60. |
| s12 | **Eye box x 580-770, y 715-800: sacred.** Whole face (720,770,195,235). Jesus's hair x 0-500, y 40-1100: nothing bright on it, no ring round it. |
| s13 | Bartimaeus's profile (317,655,65,75). Jesus's head (625,440,60,70). |
| s15 | No faces. Cross x 215-515, y 710-1545. Sun (705,1460,40,40). |
| s16 | No faces. Door x 178-615, y 566-1240 (grave cloth inside). |
| s17 | Jesus (413,460,85,105). Bartimaeus (722,690,80,95). The look between them: box x 440-700, y 430-700. Sun (710,558,50,50). |

---

## 6. Risks

1. **Positions come from stills, not the clips.** Every clip moves. Tightest fits: s01 words vs hair top (y~420); s05 `ON ME.` vs hair and hands; s10 word stack vs nose (x~700); s17 row 2 vs Jesus's hair (y~385). If a face comes within 30 px, shrink the type 8 px at a time or move it away. Never squeeze letters.
2. **Estimated word frames.** Nothing ships on `~` frames.
3. **Too many words?** 14 items in 79 s. First to drop if it feels busy: `HE CAME`, `JERICHO`, `up the road to Jerusalem`. Never drop: the two cries, `AND JESUS STOOD STILL`, both Jesus lines, `COULD SEE.`, the last line.
4. **The D3 grade touches the approved look.** It is small (-14% saturation before sight). If the owner sees dull colour, remove the grade and keep the edge.
5. **The cross mark on s14** is the one drawn symbol. If it reads as a map pin, or as forced, delete it; `JERUSALEM` + the question still work.
6. **D5 road line on a moving shot** (s14, s13) can slide off the painted road. Drift over 30 px: track with a 2-point linear move. If it wobbles: drop the line, keep the labels.
7. **`ROAD.halt` could look like a render bug.** It reads as meant only because the music stops on the same frame. Check f768 against the real audio and move the halt to the measured silence.
8. **Light must not read as the healer.** The dark opens at the cut, after His words are complete (~f1467). No beam, ray or glow comes from Jesus's hand or head. He heals by His word.
9. **Fraunces** must be loaded before render (`delayRender`). Fallback: Kalam Bold everywhere.
10. **Simulated judgement only.** No real viewer has seen this. Show the two showpiece tests (below) before the full build.

## 7. QC checklist (builder ticks every line; all $0)

Frame grabs to make and view at 2x on every face:
f2, 12, 60, 80 | 92, 100, 125 | 152, 185, 270 | 302, 370, 420 | 452, 500, 530, 600 | 626, 645, 700, 745, 767, 769, 790 | 800, 840, 887, 895 | 930, 990 | 1012, 1078, 1090 | 1175, 1240 | 1300 | 1400, 1468 | **1471, 1485, 1500, 1520, 1560, 1620, 1675** | 1682, 1750, 1810 | 1832, 1900 | 1955, 2010, 2060 | 2068, 2076, 2150, 2206, 2260, 2320, 2374.

- [ ] **Faces:** no graphic pixel on any face, eye or hand listed in section 5, on any grab. Inside a `DustWipe` / `PageSweep` a face is covered for 6 frames or less.
- [ ] **s12 eye box** is clean on every frame f1470-1680. Both open eyes read clearly at phone size by f1485.
- [ ] **Jesus:** nothing forms a ring, arc, crown or glow round His head in s04, s06, s07, s09, s11, s12, s13, s17.
- [ ] **Sacred beats calm:** s06 = halted strokes + 4 still words, zero motion of ours f798-888. s15 = two still rows only. s16 = nothing before ~f2000. No punch, shake, stamp or wipe in any of them.
- [ ] **KJV exact**, letter for letter and mark for mark: `Jesus, thou Son of David,` / `HAVE MERCY ON ME` / `Thou Son of David,` / `AND JESUS STOOD STILL` / `What wilt thou that I should do unto thee?` / `Lord, that I might receive my sight.` / `Go thy way; thy faith hath made thee whole.`
- [ ] Each word lands on its spoken frame +-2. All type inside x 60-1020, y 200-1540.
- [ ] **No GOLD before f1470.** MAROON only on his words and `ONE MAN` / `BEGGAR?`. SAGE only on Jesus's two lines and the call arcs.
- [ ] The road stops on the frame the music stops (f768), and again at "stood still" (~f2205).
- [ ] Type reads on a phone at arm's length on s04, s14, s05 (busiest backgrounds).
- [ ] Base film untouched: same cuts, 1.0x, no freeze, no reverse. Stage scale never above 1.06; punches back to 1.0 within 26 frames; drifts max 1.04.
- [ ] Last 60 frames: no new element, no fade. Audio = base audio, same length; run `check_landing_hold.py`.
- [ ] Review page `motion_v1/_QC_v1.html`: big grabs, click to zoom. **Do not auto-open anything.**

**Build order:** 1) align words + measure cuts. 2) FaceGuard + DEBUG. 3) D1, D3, D4. 4) **Two showpiece tests: f624-900 (second cry, the stop, "And Jesus stood still") and f1344-1680 (the dark opens). Show the owner these before building the rest.** 5) Everything else.
