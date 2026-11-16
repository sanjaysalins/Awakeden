# COMIC DESIGN v2 - Prophecy 01 "Born in Bethlehem" (Micah 5:2 -> Matthew 2)

Design only, $0. Replaces `COMIC_DESIGN.md` (v1 kept). Changed after 3 blind reviews (Fable, Claude, Gemini: all REVISE).
Film: 1080x1920, 30 fps, **1548 frames = 51.6 s** (voice ends 48.50 s, so the landing hold is 3.1 s).
Build: one Remotion comp `ProphecyBethlehem` in `_remotion/src/`. Clips are `OffthreadVideo`, 1.0x, trim only.
Audio: `prophecy/01_bethlehem/audio/narration.mp3` (locked). All times are from `narration.words.json`.

**What changed from v1 (short):** real pixel slots, only 2 picture shapes (9:16 and 16:9) so no paid clip is
cut to a strip; DIVE, gutter light, 3D page curl, wet ink, gold thread, camera pushes all dropped; lettering
is now the owner's ELEVATE look (see-through pills, Kalam, gold chips); the gold word lands on the birth;
Micah is 3 short shots, no 10 s clip; a new manger still; a $0 animatic comes before any spend.

---

## 1. THE GRAMMAR (series template)

### 1.1 Slots (exact pixels on the 1080x1920 page)

Only two picture shapes exist. Every still is drawn for its slot. Every clip is rendered in its slot shape.

| Slot | x | y | Size | Shape |
|---|---|---|---|---|
| `FULL` | 12-1068 | 12-1908 | 1056 x 1896 | 9:16 |
| `INSET` | 24-1056 | 1204-1784 | 1032 x 580 | 16:9 |
| `ROW-A` | 24-1056 | 200-780 | 1032 x 580 | 16:9 |
| `ROW-B` | 24-1056 | 800-1380 | 1032 x 580 | 16:9 |

Paper `#F1E6CF` shows in the margins. Every slot has a 7 px hand-wobbled ink border `#141210`.
The INSET also has a 10 px paper keyline, so it reads as a panel laid on the page.

Three page layouts:

| Layout | Slots | Use |
|---|---|---|
| `SPLASH` | FULL | one big moment |
| `SPLASH+INSET` | FULL, then INSET lands on top of its lower third | set-up, then pay-off (the main comic page) |
| `QUIET ROWS` | ROW-A + ROW-B on open paper | sacred two-beat page |

Inset-safe rule for stills: on a `SPLASH+INSET` page the FULL picture keeps every face and key object
**above y 960**. The lower third is floor, ground or shadow.

### 1.2 How a page is read (no camera moves)

The whole page is always on screen. Nothing zooms, pans or pushes. Reading is done by arrival:
1. The page arrives with its FULL picture alive.
2. The INSET is an empty ink frame, or not there yet. It lands on its word.
3. One text item at a time sits on the **reading line**, right where the two panels meet.
4. Then the page turns.
Every clip is longer than its time on screen by at least 0.4 s (numbers in section 3).

### 1.3 Lettering = the owner's ELEVATE look (2026-11-09)

Matched to `poc_comic_page/_ELEVATE/build_w3.py` (`pill_tabs`) and `build_tp.py` (`light_text`).
One change: the pill is 60 px narrower on the right, to clear the Shorts buttons.

| Item | Spec |
|---|---|
| **Pill** (narrator) | rounded box x 70-950, radius 46, fill grey `rgb(225,225,228)` at 59% (alpha 150), ink outline 4 px at 67%. Text Kalam Bold 54 px, ink `rgb(20,18,16)`, centred, line step 62 px |
| **Speech pill** (the scribe) | same pill + gold **speaker tab** top-left (`A SCRIBE`) + gold **verse chip** top-right (`MATTHEW 2:5`) + one small ink tail pointing down at the speaker in the INSET. No oval balloons (owner pick) |
| **Chips / tabs** | Kalam Bold 28 px on gold `rgb(232,168,28)`, ink outline 3 px, radius 16 |
| **Scroll card** (the prophet, any OT promise) | x 70-950, y 940-1190. Parchment `rgb(236,214,160)` at 92%, edge `rgb(92,58,24)`, two wooden rollers left and right (flat SVG). Text Kalam Bold 60 px in sepia `#2A1A0E`. Verse chip top-right. Real type, never painted, never animated by a model |
| **Time slab** | the look's hook-card style: Bangers 104 px, cream `rgb(255,238,190)`, 9 px dark brown stroke, top at y 400. Bangers is used here only |
| **Gold word** | the promised word in ink letters on a gold highlight block (same gold as the chips) |

Homes (all inside the safe zone x 60-960, y 200-1540):
- Reading line (pill): y 1000-1184. On `QUIET ROWS`: y 1400-1522 (one line only).
- Scroll card: y 940-1190. Time slab: y 400-630. Gold word HOME: x 70-400, y 210-282.

Word rules: max **7 words** and **28 letters** a line. Max 2 lines. **One text item at a time**
(a pill may carry its own small chips). Each item stays at least 1.2 s and about 0.3 s a word.
KJV word for word. No "..." on screen: a skipped part of a verse is a new scroll strip.
All fonts are bundled in `_remotion/public/` (Kalam-Bold.ttf, Bangers.ttf). No system fonts.

### 1.4 Transitions (all 2D)

| Name | Exactly | When |
|---|---|---|
| `PAGE SLIDE` | new page slides in from the right over the old one, 10 frames, ease-out; a 40 px soft shadow on its leading edge; old page moves 60 px left and darkens 15%; paper sound | normal page change |
| `SOFT TURN` | the same, 15 frames, ease in-out, no sound hit, score dips | **always** into a page that holds the child, the cross or the tomb |
| `RIFFLE` | 5 blank paper sheets slide across one after another, 5 frames each (24 frames total); each sheet is a little more yellow; time slab on top | a jump in time, never onto a sacred page |

### 1.5 The five signature effects (each one is a plain 2D build)

1. **PANEL LAND** - an INSET arrives on its word: slides up 80 px in 4 frames, its border draws
   (SVG stroke), page shake 6 px for 5 frames, low boom. On a page that holds the child: slide only, no shake, no boom.
2. **LIVING SCROLL** - the two rollers part (12 frames, mask reveal). Each KJV word fades in on its
   word time (6 frames, left-to-right mask). To change strip, the parchment slides up between the rollers (8 frames). Never shakes.
3. **GOLD WORD** - the promised word gets its gold block on the scroll, waits at HOME, then lands on
   the fulfilment picture. It moves once. Its home at every second is in section 2.2.
4. **RIFFLE THROUGH TIME** - the book flips back with the slab `ABOUT 700 YEARS EARLIER`.
5. **WAITING FRAME** - before a sacred inset, its empty ink frame draws slowly in silence. Then the
   picture arrives by **ink bloom** (14-frame fade from soft to sharp). The reader waits at an empty panel.

Dropped from v1 because they could not be pinned down or are 3D: DIVE, gutter light, page curl,
wet ink, gold thread, the red word, every zoom / push / tilt.

### 1.6 Sacred-stillness rule

A page that holds the child, the cross, the tomb, or a scroll card:
enters by SOFT TURN; no shake, no boom, no slab, no speed lines; pictures arrive by ink bloom;
pills fade in (6 frames); the clip itself is near-still (breath, flame, cloud, dawn light only).

---

## 2. THE PAGE PLAN (10 pages, 16 panels)

### 2.1 Pages

"On" = seconds the picture is on screen (including the turn). Text is shown exactly as written; `/` = line break.

| Page | Time | Layout | Panel (slot) | On | Picture (grounded) | Clip | Text on screen, one at a time | Effect | Out |
|---|---|---|---|---|---|---|---|---|---|
| **1 HOOK** | 0.00-6.95 | SPLASH+INSET | 1A FULL | 0.00-7.2 | Chief priests and scribes bend over an open scroll in a stone hall; one finger pressed on a line; lamp light from below. Camera is behind the scroll: we see their faces and the back of the parchment, no writing (Matt 2:4-6) | C01 veo 8 s | 0.00 pill `The religious experts knew` / `the exact town`; 2.16 pill `where God's promised King` / `would be born.` | frame 1 is live art | stays |
| | | | 1B INSET | 5.02-7.2 | The night road to a far small town; empty; no people | C02 veo 4 s | 5.02 pill `The Bible never says` / `they went to look.` (ink underline draws under `never`) | PANEL LAND with shake and boom | RIFFLE 6.95-7.75 |
| **2 MICAH** | 6.95-12.62 | SPLASH | 2A FULL | 7.6-12.95 | Micah, old, white beard, head cloth, stands among terraced Judean hills at dusk, staff in hand, **mouth closed**, eyes lifted, cloak moving a little (Micah 1:1) | C03 veo 6 s | 7.18-9.0 slab `ABOUT 700 YEARS` / `EARLIER`; 9.18 pill `Micah, a prophet,`; 10.68 pill `a man who spoke` / `God's message,` | RIFFLE THROUGH TIME | PAGE SLIDE 12.62 |
| **3 ONE TOWN** | 12.62-16.85 | SPLASH+INSET | 3A FULL | 12.62-17.18 | Micah close, chest up, at a lamp, eyes down. **No hands, no pen, no scroll in frame.** A plain dusk sky in a window, no town | C04 Kling 5 s (cued: he lifts his eyes once, holds) | 12.72 pill `named one small town.` | - | stays |
| | | | 3B INSET | 13.68-17.18 | A far small town on a hill, seen across a valley at dusk; no people, no label | C05 veo 4 s | 14.55 scroll strip 1 `But thou, Bethlehem` + chip `MICAH 5:2` (rollers part 14.40) | PANEL LAND on `town.` (shake ends 13.9, before the scroll). LIVING SCROLL. `Bethlehem` gets its gold block at 15.46 | PAGE SLIDE 16.85 under the scroll; scroll rolls to strip 2 |
| **4 THE PROMISE** | 16.85-21.76 | SPLASH | 4A FULL | 16.85-22.26 | Micah from behind, three-quarter, on a flat roof at dusk, one arm stretched toward the far southern hills. Face not seen | C06 veo 6 s | 16.96 scroll strip 2 `out of thee shall he` / `come forth unto me`; 19.86 strip 3 `that is to be` / `ruler in Israel.` | LIVING SCROLL. Gold word waits at HOME | SOFT TURN starts 21.76, after `Israel.` is fully inked (word ends 21.74) |
| **5 BORN THERE** (sacred) | 21.76-26.9 | SPLASH+INSET | 5A FULL | 21.76-27.23 | **New still.** Mary kneels and Joseph stands over the baby in a wooden manger; one clay lamp; plain straw, **no glow around the baby**; no ox or donkey in frame (Luke 2:7) | C07 veo 6 s (flame and breath only) | 21.94 pill `When Jesus was born there,` + chip `ABOUT 700 YEARS LATER` | ink bloom. **GOLD WORD lands** at 22.92 (`there,`) as this pill's gold tab | stays |
| | | | 5B INSET | 23.54-27.23 | Travellers from the east on a night road, far dark shapes, cannot be counted; many stars; **no single bright star ahead of them** (Matt 2:1) | C08 Kling 5 s (they walk on) | 23.54 pill `visitors from the east` / `came looking`; 25.30 pill `for a newborn King.` | PANEL LAND slide only (the child is on the page) | PAGE SLIDE 26.9 |
| **6 THE QUESTION** | 26.9-32.7 | SPLASH+INSET | 6A FULL | 26.9-33.2 | King Herod on his throne, already leaning forward, hard face, one hand gripping the throne arm; torches (Matt 2:3-4) | C09 veo 8 s (torch flames, he holds) | 26.98 pill `So King Herod` / `asked the experts`; 29.14 pill `where He would be born.` | - | stays |
| | | | 6B INSET | 28.68-33.2 | The same experts from page 1 stand in the hall; the lead scribe in front holds a closed, rolled scroll and lifts one open hand (Matt 2:5) | C10 Kling 5 s (cued: he lifts his hand once, holds) | 30.96 speech pill `In Bethlehem of Judaea.` + tab `A SCRIBE` + chip `MATTHEW 2:5` + tail to the scribe | PANEL LAND on `experts`, shake and boom | SOFT TURN 32.7 |
| **7 ALREADY THERE** (sacred) | 32.7-37.62 | SPLASH+INSET | 7A FULL | 32.7-38.12 | Bethlehem close at night: flat-roofed stone houses, one lit window, ordinary starry sky (no star standing over a house) | C11 veo 6 s | 33.30-35.5 pill `They knew the town.` | 34.3-35.6 silence: WAITING FRAME draws | stays |
| | | | 7B INSET | 35.64-38.12 | Inside a house: the young child in the arms of Mary his mother, lamp light (Matt 2:11) | C12 veo 4 s (breath only) | 35.64 pill `And Jesus was already there.` | ink bloom, no hit | SOFT TURN 37.62 |
| **8 FROM EVERLASTING** | 37.62-43.3 | SPLASH | 8A FULL | 37.62-43.8 | A huge night sky thick with stars over dark hills; tiny town lights low on the horizon; no people | C13 veo 8 s | 37.78 pill `Micah also said` / `this ruler is`; 39.56 scroll card `from everlasting.` + chip `MICAH 5:2` (rollers part 39.30); 41.54 pill `He did not begin` / `in Bethlehem.` | LIVING SCROLL | SOFT TURN 43.3 |
| **9 HE CAME, HE DIED** (sacred) | 43.3-46.3 | QUIET ROWS | 9A ROW-A | 43.3-46.8 | Close on the swaddled baby asleep in the manger straw; no other faces (Luke 2:7) | C14 veo 4 s (breath only) | 43.66 pill `He came as a baby,` | in place when the page arrives | stays |
| | | | 9B ROW-B | 45.02-46.8 | Three crosses far off on a hill, small dark shapes, heavy sky. No close body (Luke 23:33) | C15 veo 4 s (clouds only) | 45.02 pill `died for our sins,` | ink bloom | SOFT TURN 46.3 |
| **10 HE ROSE** (sacred) | 46.3-51.6 | SPLASH | 10A FULL | 46.3-51.6 | Inside the empty rock tomb looking out: a low square doorway full of dawn light, garden beyond; linen cloths lying flat and folded on the stone shelf. **No round stone. No body shape** (John 20:5-7) | C16 veo 6 s (dawn light only, positive wording) | 46.46-49.6 pill `and rose from the dead` / `on the third day.` | pill fades at 49.6; picture alone to the last frame; video and audio both run to 51.6 | end |

### 2.2 Where the gold word lives (every second it is on screen)

| Time | Home |
|---|---|
| 15.46-16.70 | on scroll strip 1, on the word `Bethlehem` |
| 16.70-16.95 | slides (8 frames) to HOME, top-left, x 70-400, y 210-282 |
| 16.95-22.92 | at HOME, above pages 4 and 5 (it rides over the soft turn) |
| 22.92-23.30 | drops (12 frames, slow, no hit) into the gold tab of the pill `When Jesus was born there,` = **the fulfilment** |
| 23.30-23.54 | sits as that tab |
| 23.54-26.9 | back at HOME as the place label on the manger picture; it leaves with page 5 |
| 31.06-32.7 | a still gold block on the word inside the scribe's pill (no motion, no effect) |
| 42.54-43.25 | a still gold block on the word inside `in Bethlehem.` (no motion) |

Rule: the promised word always wears gold where it is written. It travels once, to the birth.

---

## 3. STILLS + CLIPS (recomputed, OpenArt credits)

Prices checked on OpenArt 2026-11-14: gpt-image-2 image-to-image 42 cr; Veo 3.1 lite 720p, audio off = 20 cr/s
(4 s 80, 6 s 120, 8 s 160; 9:16 and 16:9 only); Kling 3.0 pro, sound off = 35 cr/s (5 s 175). $0.002 a credit.

| Still | Slot shape | Clip | Model | Length | On screen | Spare | Credits (still + clip) |
|---|---|---|---|---|---|---|---|
| S01 experts over the scroll | 9:16 | C01 | veo lite | 8 s | 7.2 | 0.8 | 42 + 160 |
| S02 empty night road | 16:9 | C02 | veo lite | 4 s | 2.2 | 1.8 | 42 + 80 |
| S03 Micah on the hills | 9:16 | C03 | veo lite | 6 s | 5.35 | 0.65 | 42 + 120 |
| S04 Micah close at the lamp | 9:16 | C04 | Kling pro | 5 s | 4.56 | 0.44 | 42 + 175 |
| S05 far small town | 16:9 | C05 | veo lite | 4 s | 3.5 | 0.5 | 42 + 80 |
| S06 Micah from behind, arm out | 9:16 | C06 | veo lite | 6 s | 5.41 | 0.59 | 42 + 120 |
| S07 manger (new) | 9:16 | C07 | veo lite | 6 s | 5.47 | 0.53 | 42 + 120 |
| S08 travellers from the east | 16:9 | C08 | Kling pro | 5 s | 3.69 | 1.31 | 42 + 175 |
| S09 Herod | 9:16 | C09 | veo lite | 8 s | 6.3 | 1.7 | 42 + 160 |
| S10 the scribe answers | 16:9 | C10 | Kling pro | 5 s | 4.52 | 0.48 | 42 + 175 |
| S11 Bethlehem at night | 9:16 | C11 | veo lite | 6 s | 5.42 | 0.58 | 42 + 120 |
| S12 the child with Mary | 16:9 | C12 | veo lite | 4 s | 2.5 | 1.5 | 42 + 80 |
| S13 sky of stars | 9:16 | C13 | veo lite | 8 s | 6.18 | 1.82 | 42 + 160 |
| S14 baby close | 16:9 | C14 | veo lite | 4 s | 3.5 | 0.5 | 42 + 80 |
| S15 three far crosses | 16:9 | C15 | veo lite | 4 s | 1.8 | 2.2 | 42 + 80 |
| S16 empty tomb | 9:16 | C16 | veo lite | 6 s | 5.3 | 0.7 | 42 + 120 |

- **Stills: 16 new x 42 = 672 cr.**
- **Clips: 16 = 13 veo lite (3 x 8 s, 5 x 6 s, 5 x 4 s = 1,480 cr) + 3 Kling pro 5 s (525 cr) = 2,005 cr.**
- **Total 2,677 cr = $5.35.** Cap $6.50 = 3,250 cr, so 573 cr is left for re-rolls.
- OpenArt balance when checked: 2,749 cr. The plan fits (72 cr spare). Re-rolls beyond that need a top-up.
- No Seedance (dearer than veo on OpenArt, and not needed). No 10 s clip anywhere.

The two D test frames are **not** used as film stills any more (wrong slot shape; pen on the scroll; ox,
donkey and glowing straw). They are references only:
- `look/art/D_barabbas_micah.png`, **centre crop 70%** (cuts off the corner speed lines), $0 = look ref + Micah ref.
- `look/art/D_barabbas_manger.png` = look ref + Mary / Joseph / baby ref.

Still order (so references chain): S01 first (it is the experts + hall ref) -> S10, S09. S03 -> S04, S06. S07 -> S12, S14. S05 -> S11, S13, S02.

---

## 4. CHARACTER REFS

| Ref | Source | Cost | Used by |
|---|---|---|---|
| Look | the two D frames (Micah one centre-cropped) | $0 | every still |
| Micah | centre crop of `D_barabbas_micah.png` | $0 | S03, S04, S06 |
| Mary, Joseph, baby | `D_barabbas_manger.png` | $0 | S07, S12, S14 |
| Experts + Herod's hall | approved S01 (faces are toward the camera) | $0 | S10, S09 |
| Small hill town | approved S05 | $0 | S11, S13, S02 |

No new reference sheets. Not needed: Herod (one still), travellers (far shapes), adult Jesus.
Check every still for a cloned person, any writing, and any halo before it is animated.

---

## 5. $0 ANIMATIC (build and blind-test this before any spend)

Comp `ProphecyBethlehemAnimatic`, 1548 frames, locked `narration.mp3`. It is the real comp with placeholder art.

Must show, exactly as in sections 1 and 2:
1. All 10 pages with the real slot pixels, borders, paper, and the three transitions at their real frames.
2. Every slot as a **grey panel with a label**: still id, the one-line picture, clip model and length.
   Two slots carry real art, static and marked PLACEHOLDER: the centre-cropped D Micah frame in S04, the D manger frame in S07.
3. **All** text at final size, font, place and time: every pill, chip, tab, scroll strip, both scroll cards, the time slab.
4. The gold word on its full path (table 2.2).
5. PANEL LAND (with and without shake), LIVING SCROLL, RIFFLE, WAITING FRAME, ink bloom (as a fade on the grey panel).
6. A safe-zone overlay toggle (x 60-960, y 200-1540) and a burnt-in page number + timecode for reviewers.

Machine checks the animatic script prints (all must pass):
- every text item inside the safe zone; max 7 words and 28 letters a line; max 2 lines;
- never two text items at once; each item at least 1.2 s and at least 0.28 s a word;
- every on-screen KJV string equals `words/KJV.txt` byte for byte, and its chip names the right verse;
- every clip length minus its on-screen time is at least 0.4 s;
- no shake, boom or slab event inside a sacred page; film is 1548 frames and audio runs to the end.

Blind test on the animatic (Fable seat + AI panel, film only, same questions):
who / what / why; could you read every line in time; where did your eye go on each page; did you see
the gold word and what did it mean; curiosity gap 0-10; the 5 guardrail questions. Fix by convergence, re-test once.
A pass locks the layout only. It does not approve any spend.

Then, in order, each with its own quote and yes: stills -> clips -> score and sound -> film panel -> packaging card.
Gates carried over from the Living Page standard: clip first / last frame check, `check_landing_hold.py`,
a tag per still in `visual_tags.json` (no two panels on one page share a tag), DoD numbers saved as json.

---

## 6. RISKS (3)

1. **The page may still read as a slideshow.** 4 of 10 pages are single splashes. Only the animatic
   test can answer this, at $0. If it fails, add an INSET to page 2 or 8 before buying anything.
2. **The model invents things.** Writing on the experts' scroll (C01), too much motion on sacred clips
   (C07, C12, C14), a stone at the tomb (C16), glitter on lamp light (veo: positive wording only).
   Guard: check the true first and last frame of every clip; re-roll budget is small (72 cr without a top-up).
3. **Thin spare time on two clips.** C04 (0.44 s) and C10 (0.48 s). If one comes back short, the page
   turns 0.2 s earlier. Never slow, freeze or loop, and never move a word-timed landing.

Also note: veo lite is 720p, shown at full screen on 8 pages. Check one FULL veo clip by eye before buying the rest.
