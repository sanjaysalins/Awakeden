# COMIC DESIGN - Prophecy 01 "Born in Bethlehem" (Micah 5:2 -> Matthew 2)

Design only, $0. Series template + this episode's build plan.
Film: 1080x1920, 30 fps, 51.5 s = 1545 frames (voice 48.5 s + 3.0 s landing hold).
Build: one Remotion comp `ProphecyBethlehem` in `_remotion/src/`, clips as `OffthreadVideo` at 1.0x, trim only.
Audio: `prophecy/01_bethlehem/audio/narration.mp3` (locked). All times below are from `narration.words.json`.

Big idea: **you are reading a comic book about a promise.** The page turns. Panels land on the
spoken word. The old promise is real lettering on an old scroll. One word on that scroll turns
gold, and that same gold word comes back 700 years later in another man's mouth.

---

## 1. THE GRAMMAR (reusable for every prophecy episode)

### 1.1 The page

- Every screen is a **comic page**: cream paper `#F1E6CF` with soft halftone grain, 28 px page margin,
  22 px white gutters, panels with hand-wobbled black ink borders 7 px (`#141210`), soft drop shadow.
- Panels are **stacked rows only** (9:16 rule: never side-by-side columns). Four layouts:

| Layout | Rows (top to bottom) | Use |
|---|---|---|
| `SPLASH` | one full-page panel | hook open, the prophet, a dive target |
| `STACK2` | 56% / 44% | set-up then pay-off |
| `SCROLLPAGE` | picture 56% / scroll card 44% | every Old Testament promise |
| `TRIPTYCH` | 26% / 26% / 48% | the gospel landing (last page) |

- Frame 1 is always real moving art (a `SPLASH`), never empty paper.
- A panel not yet read is an empty ink frame on paper. Its picture arrives on its word.

### 1.2 How the camera reads a page

1. The page arrives (page turn). The camera sits on the first panel, pushed in 4%.
2. On the next panel's word, that panel **lands** and the camera eases down to it (10 frames,
   ease-out). The eye is moved in reading order, top to bottom. Always.
3. Read panels stay alive (their clip keeps playing) until the page turns.
4. **DIVE**: when someone speaks, or the story steps inside a place, the camera pushes into that
   one panel until it fills the screen (14 frames). The other panels leave the screen.
5. Clip rule (binding): every clip is longer than its time on screen. Numbers are in section 3.

### 1.3 Words on the page

Fonts (already in `_remotion/public/`, plus Windows system fonts):

| Element | Font | Look | Where |
|---|---|---|---|
| **Caption box** (narrator) | Kalam Bold, 52 px, ink `#141210` | cream box `#FFF6DC`, 6 px ink border, square corners, 8 px hard ink shadow, tilted -1 or +1 degree | top-left or bottom-left corner of its own panel, overlapping the border by 20 px |
| **Speech balloon** (people in the New Testament scene) | Kalam Bold, 60 px | white `#FFFFFF` oval, 7 px ink border, curved tail to the mouth | upper half of the panel, never over a face |
| **Scroll card** (the prophet / any OT promise) | Palatino Linotype Bold, 58 px, sepia ink `#2A1A0E` (Windows font) | parchment `#E2C993`, darker edge `#8A5A2B`, two wooden rollers, paper fibre grain. Built in SVG, $0. Never painted by the image model | bottom row of a `SCROLLPAGE` |
| **Verse tag** | Bangers, 34 px | yellow chip `#F5B921`, 4 px ink border, e.g. `MICAH 5:2` | top-right corner of the scroll or balloon |
| **Name tag** | Bangers, 64 px | ink slab, cream letters | under a new character, once |
| **Time slab** | Bangers, 120 px | yellow slab, ink letters | time jumps only |

Word rules: max 7 words a line, max 2 lines a box. Bible quotes are KJV word for word. No
"..." ever: a skipped part of a verse becomes **two separate scroll strips**. All words stay
inside x 60-960, y 200-1540 (Shorts buttons).
Colour rule: **gold `#E9B23C` is only the promised word. Red `#C8281E` is only one stressed
narrator word per episode.**

### 1.4 Transitions

| Name | What | When |
|---|---|---|
| `PAGE TURN` | the page lifts from the right edge and curls left (CSS 3D rotateY, paper back face, moving shadow), 12 frames, paper sound | normal change of page |
| `RIFFLE` | 5-6 pages flip very fast; the paper gets older (back) or newer (forward); a time slab rides on top | jumps in time only |
| `INK WIPE` | fast black ink bars, 6 frames | a hard, tense cut |
| `SOFT TURN` | slow page turn, 20 frames, no sound hit | into a sacred page |

### 1.5 The five signature effects

1. **PANEL LAND** - a panel arrives on its exact word: 4-frame slide, border ink draws, small
   page shake (6 px, 5 frames), low boom. Speed lines and one impact burst allowed on action.
2. **LIVING SCROLL** - the scroll card unrolls (rollers part, 14 frames). The KJV words ink in
   one by one on the prophet's voice, each word a little wet, then dry. Gentle. Never shakes.
3. **GOLD WORD** - the one promised word (here: `Bethlehem`) turns gold on the scroll. It stays
   pinned on screen through the time jump. It lands again, same gold, same size, in the
   fulfilment balloon. A thin gold thread draws between them. This is the series' proof device.
4. **RIFFLE THROUGH TIME** - the book flips back 700 years and forward again (see 1.4).
5. **DIVE + GUTTER LIGHT** - the camera dives into a panel to step inside the place. On the last
   page, warm light from the risen panel spills softly over the gutters onto the other panels.

Small spice (use thin): halftone dots in shadows, speed lines, one red word.

### 1.6 The sacred-stillness rule

On any panel with the child Jesus, the cross, the empty tomb, or God's own words on the scroll:
- no PANEL LAND, no shake, no boom, no speed lines, no burst, no comic sound words, no red;
- the panel arrives by **ink bloom**: 14-frame fade from soft to sharp, score dips 4 dB;
- captions fade in, they do not pop; the camera moves slowly or not at all;
- the clip itself is near-still (breath, lamp flame, dawn light only).
The loud pages make the quiet pages feel holy. That contrast is the style.

---

## 2. THE PAGE PLAN (8 pages, 14 panels)

`s` = seconds. "Lands" = when the picture arrives. Captions are shown exactly as written.

### Page 1 - HOOK - 0.00 to 6.95 - `SPLASH` then splits to `STACK2`

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 1A | 0.00-7.4 | "The religious experts knew the exact town where God's promised King would be born." | Chief priests and scribes in Herod's hall bend over an open scroll; one finger rests on a line. Seen from behind the scroll, so no writing shows (Matt 2:4-6) | C01 veo 8 s | box 0.00 `The religious experts knew the exact town`; box 2.16 `where God's promised King would be born.` | full-bleed open, slow push. `knew` (1.02) bumps 115% | at 5.02 shrinks to the top row |
| 1B | 5.02-7.4 | "The Bible never says they went to look." | The night road to Bethlehem, empty; small town lights far off. No people | C02 veo 4 s | box 5.02 `The Bible never says they went to look.` (`never` in red) | PANEL LAND from below, shake, boom, speed lines to the far town | RIFFLE back at 6.95 |

### Page 2 - THE PROPHET - 6.95 to 12.6 - `SPLASH`

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| (riffle) | 6.95-8.3 | "About seven hundred years earlier," | pages flipping, paper ageing | none ($0) | time slab 7.18 `700 YEARS EARLIER` | RIFFLE THROUGH TIME, slab holds to 9.0 | lands on 2A |
| 2A | 7.9-13.0 | "Micah, a prophet, a man who spoke God's message," | Micah, old, white beard, stands on a Judean hillside at dusk, cloak moving in the wind, mouth open mid-word, one hand raised (Micah 1:1) | C03 Seedance 6 s | name tag 9.18 `MICAH`; chip 9.86 `a prophet`; box 10.68 `a man who spoke God's message` | name tag PANEL LAND (small boom); slow push to his face | PAGE TURN at 12.6 |

### Page 3 - THE PROMISE - 12.6 to 21.85 - `SCROLLPAGE`

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 3A | 12.6-22.1 | "named one small town." | Micah at his table with pen and blank scroll, lamp lit; through the window, one small hill town at dusk (the chosen "D" picture) | C04 Kling 10 s (cued: he lifts his eyes from the scroll to the window, then holds; the pen never touches the scroll) | box 12.72 `named one small town.` | camera eases toward the window town on "one small town" | stays |
| 3B | 14.4-21.85 | PROPHET: "But thou, Bethlehem" / "out of thee shall he come forth unto me that is to be ruler in Israel." | scroll card (type, $0), two strips | none ($0) | strip 1 at 14.76 `But thou, Bethlehem`; strip 2 at 16.96 `out of thee shall he come forth unto me` and at 19.86 `that is to be ruler in Israel.`; tag `MICAH 5:2`; small ink tail from the scroll up to Micah | LIVING SCROLL, words ink in on the word times. `Bethlehem` turns gold at 15.46 (GOLD WORD). Sacred: no shake | RIFFLE forward at 21.6, the gold word stays pinned |

### Page 4 - BORN THERE - 21.85 to 26.9 - `STACK2`

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 4A | 21.6-27.3 | "When Jesus was born there," | Mary and Joseph over the baby in the manger, lamp light (the chosen "D" picture, cropped to the three of them) (Luke 2:7) | C05 veo 8 s (flame and breath only) | box 21.94 `When Jesus was born there,`; the gold word settles as a small label `BETHLEHEM` | SACRED: ink bloom, no hit. Gold word lands softly | stays |
| 4B | 23.54-27.3 | "visitors from the east came looking for a newborn King." | Travellers from the east ride by night toward a bright star; far silhouettes, number not countable (Matt 2:1-2) | C06 Kling 5 s (riders move forward) | box 23.54 `visitors from the east came looking`; box 25.04 `for a newborn King.` | PANEL LAND, light shake; star glints once | PAGE TURN at 26.9 |

### Page 5 - THE QUESTION - 26.9 to 33.1 - `STACK2` then DIVE

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 5A | 26.9-30.9 | "So King Herod asked the experts" | King Herod on his throne leans forward, hard face, hand gripping the throne arm (Matt 2:3-4) | C07 Kling 5 s (cued: he leans forward once, holds) | box 26.98 `So King Herod asked the experts` | name-size bump on `Herod` (27.72), speed lines behind him | leaves screen in the dive |
| 5B | 28.68-33.2 | "where He would be born." then SCRIBE: "In Bethlehem of Judaea." | The same experts stand before the throne; the lead scribe in front holds a rolled, closed scroll and lifts one open hand to answer (Matt 2:5) | C08 Kling 5 s (cued: he raises his hand once, holds) | box 29.14 `where He would be born.`; balloon 30.96 `In Bethlehem of Judaea.` with tag `MATTHEW 2:5` | PANEL LAND on `experts`. DIVE into 5B at 30.7. In the balloon `Bethlehem` is the same GOLD WORD; a gold thread draws in from the page edge. One impact burst behind the balloon | INK WIPE at 33.0 |

### Page 6 - ALREADY THERE - 33.1 to 37.65 - `SPLASH` with DIVE

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 6A | 33.0-35.7 | "They knew the town." (then 1.4 s of silence) | Bethlehem at night, close: flat-roofed stone houses, one window lit, the star standing above it (Matt 2:9) | C09 veo 4 s | box 33.30 `They knew the town.` | in the silence (34.2-35.6) the camera DIVES slowly at the lit window. No sound hit. Score thins | dive becomes 6B |
| 6B | 35.5-38.05 | "And Jesus was already there." | Inside the house: the young child in the arms of Mary his mother, lamp light (Matt 2:11) | C10 Seedance 5 s (breath only) | box 35.64 `And Jesus was already there.` | SACRED: ink bloom, held still | SOFT TURN at 37.65 |

### Page 7 - FROM EVERLASTING - 37.65 to 43.3 - `SCROLLPAGE`

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 7A | 37.65-43.7 | "Micah also said this ruler is" ... "He did not begin in Bethlehem." | A vast night sky thick with stars over dark hills; tiny town lights low on the horizon. No people | C11 veo 8 s | box 37.78 `Micah also said this ruler is`; box 41.54 `He did not begin in Bethlehem.` | slow tilt: stars first, then down to the tiny town on "Bethlehem" (42.54) | stays |
| 7B | 39.3-43.3 | "from everlasting." | the same scroll card as page 3 (type, $0) | none ($0) | scroll 39.56 `from everlasting.` with tag `MICAH 5:2` | LIVING SCROLL, two words ink in large. Sacred: no shake | SOFT TURN at 43.3 |

### Page 8 - THE GOSPEL - 43.3 to 51.5 - `TRIPTYCH` (all sacred)

| Panel | Lands-leaves | Narration | Picture | Clip | Words on screen | Effect | Out |
|---|---|---|---|---|---|---|---|
| 8A | 43.3-49.8 | "He came as a baby," | Close on the swaddled baby asleep in the manger straw. No other faces (Luke 2:7) | C12 Seedance 8 s (breath only) | box 43.66 `He came as a baby,` | ink bloom | stays |
| 8B | 45.02-49.8 | "died for our sins," | Three crosses far off on a hill, small dark shapes against a heavy sky. Distant, no close body (Luke 23:33) | C13 veo 6 s (clouds only) | box 45.02 `died for our sins,` | ink bloom | stays |
| 8C | 46.46-51.5 | "and rose from the dead on the third day." | Inside the empty rock tomb looking out: a low square doorway full of dawn light, garden beyond, linen cloths lying flat and folded on the stone shelf. **No round stone anywhere. No body shape** (John 20:5-7) | C14 veo 6 s (dawn light only, positive wording) | box 46.46 `and rose from the dead` / `on the third day.` | ink bloom. GUTTER LIGHT: warm light spills up over the gutters onto 8B and 8A (47.0-48.6). Then a slow DIVE into 8C (48.6-49.8) | hold full-bleed on the open tomb to 51.5. Video and audio both run to the end |

Pacing check: 14 panels in 51.5 s, about 3.7 s each. Sacred panels: 4A, 6B, 8A, 8B, 8C + both scroll cards.

---

## 3. STILLS + CLIPS LIST

Every still is 9:16, in the "D" look. Every prompt attaches the two D frames as the look reference.
No writing in any still. No halos.

| Still | Content (one line) | References | Clip | Model | Length | On screen |
|---|---|---|---|---|---|---|
| S01 | experts over the open scroll, seen from behind it | D look, R3 experts | C01 | veo3_1_lite | 8 s | 7.4 s |
| S02 | empty night road, Bethlehem lights far off | D look, R5 town | C02 | veo3_1_lite | 4 s | 2.4 s |
| S03 | Micah speaking on a hillside at dusk | D look, R1 Micah | C03 | Seedance | 6 s | 5.1 s |
| S04 | Micah at the table, blank scroll, town in window | **reuse `D_barabbas_micah.png`**, one edit: remove the white speed lines in the four corners | C04 | Kling | 10 s | 9.5 s |
| S05 | Mary, Joseph, baby in the manger | **reuse `D_barabbas_manger.png` as is**, panel crop on the three people | C05 | veo3_1_lite | 8 s | 5.7 s |
| S06 | travellers from the east under the star, far silhouettes | D look | C06 | Kling | 5 s | 3.8 s |
| S07 | King Herod leaning forward on his throne | D look, R4 hall | C07 | Kling | 5 s | 4.0 s |
| S08 | lead scribe answers, closed scroll in hand, experts behind | D look, R3 experts, R4 hall | C08 | Kling | 5 s | 4.5 s |
| S09 | Bethlehem houses at night, one lit window, star above | D look, R5 town | C09 | veo3_1_lite | 4 s | 2.7 s |
| S10 | the young child in Mary's arms, in the house | D look, R2 Mary + baby | C10 | Seedance | 5 s | 2.6 s |
| S11 | huge starry sky, tiny town on the horizon | D look, R5 town | C11 | veo3_1_lite | 8 s | 6.1 s |
| S12 | close on the sleeping swaddled baby | D look, R2 baby | C12 | Seedance | 8 s | 6.5 s |
| S13 | three far crosses on a hill, heavy sky | D look | C13 | veo3_1_lite | 6 s | 4.8 s |
| S14 | empty tomb from inside, square doorway, dawn, folded cloths | D look | C14 | veo3_1_lite | 6 s | 5.0 s |

Totals: **14 stills = 12 new + 2 reused D frames. 14 clips = 7 veo (8,4,8,4,8,6,6 s) + 4 Kling (10,5,5,5 s) + 3 Seedance (6,5,8 s).**
$0 graphics (no clip): scroll card x2, the riffle pages, all boxes, balloons, tags, gold word, gutter light.

What the two D test frames do:
- `look/art/D_barabbas_micah.png` - becomes S04, is the Micah character reference (R1), the town look
  reference (R5, crop of the window), and the look reference on every prompt.
- `look/art/D_barabbas_manger.png` - becomes S05, is the Mary + baby reference (R2), and the look reference.
  Note: the ox and donkey are tradition, not in Luke 2. The panel crop keeps them at the edge or out.

No price is quoted here. Stills and clips each need their own quote and their own yes before any spend.

---

## 4. CHARACTER REFS NEEDED

| Ref | Who / what | How | Used by |
|---|---|---|---|
| R1 | Micah | crop from `D_barabbas_micah.png`, $0 | S03, S04 |
| R2 | Mary + the baby | crop from `D_barabbas_manger.png`, $0 | S05, S10, S12 |
| R3 | The experts: one lead scribe + two chief priests, front and three-quarter view | **1 new sheet** | S01, S08 |
| R4 | Herod's hall (stone, pillars, throne) | no new sheet: S01, once approved, is chained into S07 and S08 | S07, S08 |
| R5 | Bethlehem (small hill town, flat roofs, lit windows) | crop of the window in `D_barabbas_micah.png`, $0 | S02, S09, S11 |

Not needed: Joseph (one still), Herod (one still), the wise men (far silhouettes, one still),
adult Jesus (the last line is told by three crosses far off and the empty tomb).
So: **1 new reference sheet.** Check every still for a cloned person before it is animated.

---

## 5. RISKS (3)

1. **Clips must outlast a live page.** Panels stay alive until the page turns, so two clips are
   tight: C04 (9.5 s of a 10 s clip) and C08 (4.5 s of 5 s). Fix if a render comes back short:
   land that panel 0.4 s later. Never slow, freeze or loop it.
2. **The model invents motion or writing.** The pen may scribble on the blank scroll (C04), the
   experts' scroll may grow fake letters (C01), a sacred clip may move too much (C05, C10, C12),
   a tomb may grow a stone (C14). Guard: pen held off the scroll, scroll seen from behind,
   "breath and flame only" wording, check the true first and last frame of every clip.
3. **Too much to read.** 8 pages in 51 s is fast for a second-language viewer. Guard: one box at a
   time, max 7 words a line, the box leaves when the next one lands, and the blind
   global-audience panel must run on the first assembled cut.

Before any spend: this design goes to the blind panel (Fable seat + AI panel) as a significant plan.
