# Mary and Martha (Warm Storybook) — Motion layer v2 (design spec, build-ready)

Comp: 1080x1920, 30 fps, 2148 frames. Same base, same audio, same **cut** and same **6 transitions** as v1
(`motion_v1/MOTION_DESIGN.md` section 3 cut list and section 4 table: use them unchanged, origins included).
All frames are absolute comp frames. Word frames = `voice_v2/narration.alignment.json` x30.
Positions were read off gridded frames f01-f15 (432x768 stills, x2.5; one frame per shot, see R1).

**Diagnosis check:** I agree with the brief. v1 drew a diagram ON the pictures (knot, lasso, cards).
The pictures already have their own doodles. Two finds the brief did not list:
- The clay lamp in shot 9 (Mary) and shot 12 (Martha, "did He care?") has a flame that is **pencil outline only, not coloured in.** In shots 4, 5 and 11 the same lamp's flame IS painted gold.
- Shot 3 shows an olive tree through the door. Shot 13's gold leaf sprigs are the same leaf.

So v2 adds nothing new to the world. It only **finishes what the illustrator left unfinished.**

---

## 1. The idea in 3 lines

1. **The illustrator keeps drawing.** No symbols. Only the pictures' own things: a clay lamp in pencil, its small gold flame, a pale gold olive sprig.
2. **A little flame gets coloured in** where His care is: at "one thing", over Mary, and then, after "did He care?", over Martha. A silent yes before the words say it.
3. **A gold sprig grows** when the Bible says He loved them: three leaves for three names, then one leaf for her under "And He loved her."

Words sit straight on the paper, in the same pencil. No cards.

---

## 2. The thread: the lamp flame

| Seen | Frame | What happens | Whose pencil |
|---|---|---|---|
| 1. Seeded | f333-464 | Mary listens. The two lamps beside her are lit. Their flames sway a little. | Art (we add sway only) |
| (free) | f464-668 | Martha asks "dost thou not care". A lit lamp is right beside her head. | Art. **We add nothing.** |
| 2. Drawn | f964-1000 | Kitchen, "many things". A small lamp on a shelf is sketched on the bare plaster. Flame outline only. | Ours, copying shot 12's lamp |
| 3. Lit | f1009-1022 | "**one thing**". The flame is painted gold. | Ours |
| 4. Mary's | f1110-1124 | "that **good part**". The art's own empty flame over Mary is coloured in. | Art outline + our colour |
| 5. Pay-off | f1584-1598 | Half a second after "did He care?". The art's own empty flame over Martha is coloured in. | Art outline + our colour |

Second, smaller motif (love, spoken): the gold olive sprig. f1664 (three leaves) and f2060 (one leaf). It holds on the last frame.

---

## 3. Beat table

Safe box for TEXT: x 60-950, y 160-1490. Font = Kalam 700 unless noted. "T" = text beat, "D" = doodle beat.

| # | Frames (on-off) | Word it hits | What appears | Motion (easing) | Position / size (px) | Colours | Why it fits THIS picture |
|---|---|---|---|---|---|---|---|
| **T1** | 0-179 | hook (f0; "Does anyone even care?" f98-133) | Words **Does anyone care?** written on the stone wall. Under them a **lift** (4.1), no card. | Fully there on frame 0. Settle scale 1.04→1, f0-6, ease-out cubic. Leaves on the hard cut f179. | Text 76 px, centre (400, 240). Lift ellipse centre (400, 240), rx 370, ry 95. | Text `#3A322B`. Lift `#F8EFDD`. | First-frame hook. Same spot as v1 (hair top y≈320, post x≈730). The wall is pale stone, so paper showing through looks like the page, not a label. No doodle: her hand in her hair already says it. |
| **T2** | 190-261 | "**Martha**" (f190-200) | Name **Martha**, pencil, straight on the cream paper | Writes f190-200, linear. Leaves on the cut (curtain wipe f261). | 72 px, centre (565, 208). Fits the gap between the jar sketches, above the shelf line (shelf y≈375). | `#3A322B` + `#graphite` | Reads like the illustrator's own note beside the shelf sketch. Hair top y≈270. No swatch needed: clean cream. |
| — | 261-333 | quiet | nothing | | | | Curtain and open door say it. |
| **D1** | 333-464 | "her sister **Mary** sat at His feet and **listened**" | The two painted lamp flames **sway**. A flame dab (4.3) sits on each art flame. | Opacity 0→.85, f333-345. Sway (4.3) to the hard cut f464. | Flame A base (280, 250), 26 w x 62 h. Flame B base (175, 562), 20 w x 50 h. | 4.3 flame colours | The lamps are already drawn and lit in this picture. We only let them breathe. It seeds the thread where she **listens**. Skip this beat if R2 fails. |
| **T3** | 384-452 | "**Mary**" (f384-392) | Name **Mary**, pencil, on cream | Writes f384-392, linear. Out: opacity f440-452. | 88 px, centre (420, 440). No arrow. | `#3A322B` + `#graphite` | Bare cream between the shelf sketch and His head, just above her hair (top y≈555). His open hand is at y≥825. |
| — | 464-843 | quiet (12.6 s) | nothing | | | | Her whole KJV complaint and "His answer? Her name. Twice." play clean. The art's lit lamp beside her does the work. |
| **T4** | 843-952 | "**Martha, Martha,**" (f843-857, f868-882) | **Martha, Martha,** (KJV) straight on the cream above her head | First "Martha," writes f843-857. Second writes f868-882 (the gap is His pause). Out: opacity f940-952. | 104 px, centre (515, 290). | `#A84A24`, solid, no grain | His voice = His mantle colour. Top of this picture is empty cream (hair top y≈430). Best v1 beat, now with no card. |
| **D2** | 964-1071 | "**many things**" (f958-977) | A small **clay lamp on a bracket shelf**, sketched in pale pencil on the bare plaster, top-left. Flame is **outline only**. | Shelf f964-972. Lamp body f972-990. Rim, handle, foot f986-996. Flame outline f994-1000. All linear (a steady hand). After f1000 still (`pencilStill`). | Paths in 4.2. Box x 90-350, y 258-470. Stroke 3 px. | Line `#A8876A` at .9. Body wash `#EAD9BF` at .35. | Same lamp, same bracket shelf as shots 9 and 12, same pale pencil as every shelf sketch. The kitchen is full of painted things. The one unfinished pencil thing is the lamp. Plaster here is the only bare "paper" in the shot. |
| **D3 + T5** | 1009-1071 | "**one thing**" (f1009-1022) | The flame is **painted in**. Under the shelf, the words **one thing** (KJV). A lift under the words. | Flame colour paints bottom → top f1009-1020, ease-out cubic, then sways (4.3). Words write f1009-1022, linear. Lift fades in f1004-1010. Out: whole group opacity f1059-1071, under the C8 bloom (it leaves with the kitchen). | Flame base (118, 336), tip (120, 262). Text 88 px, centre (300, 520). Lift centre (300, 520), rx 250, ry 80. | Flame 4.3. Text `#A84A24`. | Many painted things, one small flame. The viewer's eye goes to the only thing that just changed. Words sit on plaster above the pot steam (steam top y≈580; steam may drift through, that is fine). |
| **D4** | 1110-1208 | "that **good part**" (f1110-1128) | The art's own empty flame above Mary is **coloured in** | Paints bottom → top f1110-1124, ease-out cubic. Sways to the hard cut f1208. | Flame base (654, 180), tip (656, 100), 22 w. Path 4.3. | 4.3 | This flame is drawn but not painted in the picture. We finish it on the word that says what she chose. No text: her face carries the line. His head is at x≥925. |
| **T6** | 1210-1310 | "**Careful**" (cut f1208), "**full of worry**" (f1245-1266) | Three short rows in pencil on the cream: **“careful”** / small **means** / **full of worry** | “careful” writes f1210-1226. "means" fades in f1236-1242. "full of worry" writes f1245-1266. Out: opacity f1298-1310. | “careful” 84 px, centre (755, 235). "means" 40 px (Kalam 400), centre (755, 305). "full of worry" 64 px, centre (755, 375). | `#3A322B` + `#graphite` | The one hard word. Top-right is bare cream. Her arm is below y≈470, hands y≥590. No doodle here on purpose: her working hands are the picture of "careful". |
| — | 1310-1584 | quiet (9 s) | nothing | | | | "The one thing needed was to hear Him" plays on the wide room. Its niche lamp is lit in the art. |
| **D5** | 1584-1616 | half a second after "did He **care?**" (f1560-1569) | The art's own empty flame above Martha is **coloured in** | Paints bottom → top f1584-1598, ease-out cubic. Sways. Goes with the slow bloom C12 (f1616-1636) on the outgoing picture. | Flame base (750, 298), tip (748, 215), 28 w. Path 4.3. | 4.3 | The pay-off. She asks. The music turns. No words on screen. A small light comes on over her head. The Bible's words answer next. |
| **D6** | 1664-1842 | "Now **Jesus loved**" (f1662-1722), then "**Martha**" f1725, "**sister**" f1758, "**Lazarus**" f1791 | One new **gold olive sprig** grows out of the art's leaf pattern, top-left. Three leaves open, one on each name. | Stem draws f1664-1712, ease in-out sine. Leaf 1 opens f1725-1735, leaf 2 f1758-1768, leaf 3 f1791-1801, each ease-out cubic (grow from its base). Then leaves sway ±2° (sine, 70 f, staggered). Out: opacity f1830-1842. | Path and leaves in 4.4. Box x 215-565, y 140-240. | Stem `#D8BF88`. Leaf fill `#EAD7A6` at .7. | The picture already has these sprigs in this gold. One more grows while the love line is read. Three names, three leaves. It stays low and to the left: not an arch, not over His head (hair top y≈312). |
| — | 1842-2034 | quiet (6.4 s) | nothing | | | | "He never called Martha's work wrong. Under all her work, He saw her worry." Hands, then the clean last picture. The cup in her hands steams by itself. |
| **T7** | 2034-2148 (end) | "**And He loved her.**" (f2034-2057) | Last words, two rows, written in the bright doorway above them | "And He" writes f2034-2042. "loved her." writes f2043-2057. **No out.** | 60 px. Row 1 centre (628, 256). Row 2 centre (628, 318). Light patch is x 455-795, y 210-370. | `#A84A24`, solid | The doorway is the picture's own blank paper: warm, bright, above the two of them. No card over their robes. His hair top y≈380. |
| **D7** | 2060-2148 (end) | after "her." | A short gold sprig grows under the last row and opens **one leaf** | Stem draws f2060-2078, ease-out cubic. Leaf opens f2078-2090. Then fully still to the last frame. | Stem `M 640 350 Q 720 358 782 334`. Leaf (4.4) base (782, 334), rotate -42°, scale 0.85. | Stem `#C9A65E` (one step deeper, the sky is yellow). Leaf fill `#E6CC8E` at .8. | Three leaves for the family. One leaf for her. Same olive that stands outside this door in shot 3. |

Count: **7 text beats** (T1-T7). **6 doodle beats** (D1 sway, D2+D3 the kitchen lamp, D4, D5, D6, D7). Terracotta 3 times only (T4, T5, T7).

Cut from v1: the knot (x3), the lasso, the untie, the arrow, every cream card, "many things", "Did He care?", the John 11:5 tag, "He saw her worry."

---

## 4. Shape recipes

### 4.1 Lift (replaces the swatch; used in T1 and T5 only)
- One ellipse, fill = radial gradient of `#F8EFDD`: opacity .62 at centre, .45 at 60%, 0 at 100%. **No edge, no outline, no deckle, no shadow.**
- It must read as paint thinned back to paper, like the cream fade at the bottom of shots 8 and 13. If you can see its shape, lower the centre to .5.
- Not used on cream shots (T2, T3, T4, T6) and not on the doorway (T7).

### 4.2 Kitchen lamp (D2), 1080x1920 px, stroke 3, round caps, no fill unless said
- Shelf: `M 92 416 L 348 414 L 349 434 L 93 436 Z`
- Brackets: `M 132 436 Q 134 462 150 468 L 158 436` and `M 296 436 Q 298 462 284 468 L 276 436`
- Body: `M 112 340 Q 150 348 182 344 Q 200 332 245 330 Q 290 332 304 352 Q 312 380 284 396 Q 235 410 190 400 Q 150 386 128 358 Q 116 352 112 340` (fill `#EAD9BF` at .35, fades in f986-996)
- Rim: `M 200 336 Q 245 344 290 338`
- Handle: `M 304 350 Q 340 336 344 362 Q 344 388 300 384`
- Foot: `M 196 402 L 192 412 L 268 412 L 264 402`
- Flame outline (pencil, 2 px): same path as the 4.3 flame at base (118, 336).
- Three or four light hatch strokes under the shelf, 2 px at .5, like shot 9's shelf. Optional.
- Put it side by side with shot 12's lamp before render. It should look like the same hand drew both.

### 4.3 Flame (D1, D3, D4, D5): ONE component, props `bx, by, h, w`
- Outer, for base (bx, by), height h, half-width w/2 = a:
  `M bx by C bx-a by-0.25h, bx-0.6a by-0.62h, bx+2 by-h C bx+a by-0.62h, bx+1.3a by-0.25h, bx by Z`
  - D3: `M 118 336 C 100 318 108 290 120 262 C 134 290 138 318 118 336 Z`
  - D4: `M 654 180 C 640 160 646 128 656 100 C 666 128 668 160 654 180 Z`
  - D5: `M 750 298 C 735 278 740 245 748 215 C 760 245 764 278 750 298 Z`
- Inner: same shape at 55% size, sharing the base point.
- Colours (sampled to match the painted flames in shots 5 and 11): outer `#F2B544`, inner `#FBE3A0`, a touch of `#E58A2B` in the bottom fifth. Flat gouache, opacity .9. `deckle` at scale 3 on the edge.
- Behind it, one damp wash: ellipse rx 1.5w, ry 0.75h, centred on the flame, `#F6DFA6` at .22, soft deckled edge, **no blur**. The art has this wash round its own flames. See R4.
- Paint-in: clip reveal bottom → top, plus opacity 0→.9, over the frames in the table.
- Sway, about the base point: rotate = 3°·sin(2πf/46) + 1.5°·sin(2πf/17). scaleY = 1 + 0.05·sin(2πf/23). Nothing faster. No flicker in brightness.
- D4 and D5: do **not** draw a new outline. The art's own pencil outline stays visible round the colour.

### 4.4 Sprig and leaf (D6, D7)
- D6 stem (3 px, round caps): `M 215 235 C 280 180 360 165 430 185 C 470 200 500 195 522 176`
- Leaf (local, base at 0,0, 46 long): fill `M 0 0 Q 23 -14 46 0 Q 23 14 0 0 Z`, midrib `M 0 0 L 40 0` (2 px).
  - Leaf 1 (Martha): base (321, 182), rotate -65°.
  - Leaf 2 (sister): base (430, 185), rotate 50°.
  - Leaf 3 (Lazarus): base (522, 176), rotate -25°.
- Open = scale 0→1 from the base along its length. No bounce.
- Start point: nudge up to 30 px so the stem leaves from a real stem of the art's pattern (R5).
- Line weight, colour and leaf shape must match the art's sprigs. No `graphite` grain (the art's gold is ink-smooth). Use `pencilStill` wobble only.

### 4.5 Text
- v1 `Write`, with two changes: **remove both `textShadow`s** (the cream glow and the terracotta shadow) and no swatch.
- Graphite text keeps `#graphite`. Terracotta is solid.
- No boil on any text. No boil on doodles once drawn (`pencilStill`), so they sit as still as the art's own sketches.

### 4.6 Layers
15 clip layers with v1 masks → doodles and text **inside the layer of their own shot** (so D3/T5 and D5 leave under the blooms with their picture) → `PaperGrain` on top.

---

## 5. Palette

| Role | Hex |
|---|---|
| Paper (lift only) | `#F8EFDD` |
| Warm graphite (narrator words, names) | `#3A322B` |
| Pale sketch pencil (kitchen lamp) | `#A8876A` |
| Lamp body wash | `#EAD9BF` |
| Flame outer / inner / base | `#F2B544` / `#FBE3A0` / `#E58A2B` |
| Flame damp wash | `#F6DFA6` |
| Sprig stem / leaf (shot 13) | `#D8BF88` / `#EAD7A6` |
| Sprig stem / leaf (shot 15) | `#C9A65E` / `#E6CC8E` |
| Terracotta = His mantle (His words, one thing, last line) | `#A84A24` |

v1's dark sepia `#6B4A32` is gone. It was darker than any sketch line in the pictures.

---

## 6. Three KEY FRAMES (judge these stills first)

| Frame | Shot | Shows |
|---|---|---|
| **f1030** | 8, kitchen | The pencil lamp on the plaster, its flame just painted, **one thing** under it. The new look in one still. |
| **f1604** | 12, Martha kneeling | No words. The little flame now lit over her, after "did He care?". The pay-off. |
| **f2110** | 15, last | **And He loved her.** in the doorway light, the one-leaf sprig under it. The last frame. |

Spare if wanted: f1810 (shot 13, the three-leaf sprig among the art's own).

---

## 7. Do not

- Do not bring back the knot, the lasso, any arrow, any card, swatch, pill, box or underline.
- Do not add a heart, halo, light rays, sparkle, glow, blur, emoji or drop shadow. The flame is flat paint.
- Do not let the shot 13 sprig arch over His head or meet another sprig (it would read as a crown).
- Do not put any mark on a face, the cup hands, His hand on her shoulder, or the joined hands in shot 14.
- Do not add anything to shots 3, 5, 6, 11 or 14. Shot 5's lit lamp beside Martha is the art's; leave it alone.
- Do not write "lamp", "light" or Psalm 119 on screen. The flame is never explained.
- Do not write Martha's KJV line, or any words KJV does not have as if they were Bible text.
- Do not mark Martha's work as wrong. Nothing in the kitchen is circled, crossed or dimmed.
- Do not make the flame flicker fast or grow. It never gets bigger than the art's own flames.
- Do not boil the lines. Once drawn, a doodle is as still as the picture (flame sway and leaf sway only).
- Do not change the cut or any of the 14 cut types, frames, easings or origins from v1.
- Do not fade the last words or the last sprig.

---

## 8. Risks

- **R1 (all).** Positions come from ONE small frame per shot (432 px wide, so ±5 px). The clips move. Export first / middle / last frame of every beat and re-check.
- **R2 (D1, D4, D5: colour on the art's flames).** If the lamp drifts more than about 6 px during a shot, the colour slides off its pencil outline. Check the lamp's position at the shot's first and last frame. If it drifts, track it with a 2-point linear move. If it wobbles, skip D1; D4 and D5 are worth tracking by hand.
- **R3 (the flame's meaning).** A newcomer may read "the one thing is a lamp". The words **one thing** sit right there and the narrator explains it 10 s later ("to hear Him"). If a blind seat still says "lamp", keep D4 and D5 and drop the kitchen lamp (D2, D3), leaving T5 alone on the plaster.
- **R4 (damp wash vs "no glow").** The wash is copied from the art's own lamps, but it is the nearest thing here to a glow. If it reads as glow, delete it. The flame works without it.
- **R5 (D6 sprig).** It must touch a real stem of the art's pattern or it floats. It must also be the art's gold: if it looks brighter than its neighbours, drop opacity to .8.
- **R6 (T7 size).** The doorway patch is only 340 px wide, so the last line is 60 px (v1 was 100 px). His head is 30 px under it and may move. Check on a phone. Fallback: v1's place (centre (520, 1392), 92 px, one row) with a 4.1 lift, rx 430, ry 90, and the D7 stem moved to `M 560 1452 Q 720 1464 860 1436`.
- **R7 (T2 fit).** "Martha" has 13 px above her hair. If the clip lifts her head, drop to 64 px or use v1's fallback place (400-720, 165-270).
- **R8 (D4 height).** Mary's flame is at y 100-180, above the text safe line. It is a doodle, not text, but check it is not under the Shorts top bar on a phone.
- **R9 (hook words).** Still "Does anyone care?" without "even", as v1, to stay readable at 76 px. Narrator line, not Bible text.
- **R10 (quiet first half).** The first drawn doodle arrives at f964 (32 s). Before that there are only words and swaying flames. That is on purpose (her complaint plays clean), but if the owner wants more early life, add ONE thing only: a 2-curl pencil steam wisp joining the art's steam in shot 2 (right edge, x 900-1040, y 1100-1500).

## 9. QC before showing the owner (all $0)

1. Stills at f0, 200, 400, 875, 1000, **1030**, 1066, 1150, 1280, **1604**, 1626, 1810, 2045, **2110**, 2147.
2. No mark on a face or hands. All text inside x 60-950, y 160-1490.
3. Zoom 2x on each coloured flame: colour sits inside the pencil outline at first, middle and last frame.
4. Kitchen lamp next to shot 12's lamp: same hand, same weight, same paleness.
5. Shot 13 sprig next to the art's sprigs: same gold, same weight.
6. No card, box or visible lift shape anywhere. No shadow on any letter.
7. Transitions frame by frame, as v1. Last frame fully still. Audio = video length (`check_landing_hold.py`).
