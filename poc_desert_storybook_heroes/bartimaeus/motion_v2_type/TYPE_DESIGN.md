# Blind Bartimaeus - TYPE v2 "THREE HANDS" (design only, $0)

Replaces **D4 LETTERING** (and the `Ribbon`) of `motion_v1/MOTION_DESIGN.md`. Nothing else changes.
KEEP as built in `_remotion/src/BartimaeusV1.tsx`: Stage (punch / shake / drift / grade), DARK, ROAD + motes, cry rings, road line, cross mark, cloak streaks, Bloom, glow wash, DustWipe, PageSweep, grain, all guards, all cut frames.
Build as a copy (`BartimaeusV2.tsx`); swap only the `Type` component, `Row`, `Ribbon`, and the `Swash` colour. Do not edit V1.

Comp 1080x1920, 30 fps, 2375 frames. All frames absolute. Word frames come from `motion_v1/words.json` (already aligned). No `Math.random`; use v1 `hash(i)`.

---

## 1. The direction (one, committed)

**Colour says WHO is speaking. The hand says HOW. And the words go blind-to-sight with him.**

There are three hands on the page, the way a real painted storybook has them:

| Hand | Who | Looks like | Moves like |
|---|---|---|---|
| **THE SHOUT** | Bartimaeus crying out | Rough dry-brush paint, red earth, caps | Thrown from his mouth. Each word bigger than the last. |
| **THE TELLER** | The narrator | A soft brush hand, sentence case, ink painted straight on the wall / sky / road | Written on, left to right, as the word is spoken. Blown off as dust. |
| **THE WORD** | Scripture and the gospel facts (Jesus's lines, "And Jesus stood still", the cross, the tomb) | Old Bible type, inked | **Never moves.** It is pressed on and stays. |

The arc inside the lettering:

1. **Blind (f0-1469):** earth pigments only (ink, red earth, sage). No gold. No shine. One word is left **hollow**: `sight.`
2. **The stop (f798):** every hand stops. Jesus stands **inside** the sentence: `And Jesus | stood still`.
3. **Sight (f1470+):** the first line comes **into focus** like new eyes, and `see.` is the first gold word, filled where `sight.` was empty. After that, the Teller's lines catch one glint of sun.
4. **Cross and tomb:** only THE WORD. Still. No effects.
5. **Last frame:** THE WORD and his colour meet: `Jesus stood still` (Bible type) + `for one man.` (his red).

### Why this is more creative than v1

- v1 had **one voice**: the same fat serif caps, same cream fill, same thick outline + drop shadow, for a beggar's scream, for Jesus, for the cross. It read as a sticker laid on top of the painting.
- v1 put **light letters on light paint**, so it needed the heavy outline. v2 does what a picture book does: **dark ink on the light wall**, no outline, blended into the paint (`multiply`), so the brush grain of the art shows through the letters.
- In v1 the type only labelled the story. In v2 the type **acts** it: the cry grows and breaks out of the dark frame; the crowd's words press down; Scripture alone holds still; a hollow word is answered by a gold one; a line comes into focus when his eyes do.
- Sentence case and bigger sizes (v1 notes were 38-48 px; v2 body is 72-132 px): easier for a dyslexic or second-language reader, and readable with the sound off.

---

## 2. Fonts (3 new, all free, OFL). Do not use Fraunces, Kalam, Bangers, Permanent Marker.

Download to `_remotion/public/` (I did not download them; the 4 URLs were checked, HTTP 200):

| Hand | Family | File | Raw path |
|---|---|---|---|
| SHOUT | Protest Revolution | `ProtestRevolution-Regular.ttf` | `https://raw.githubusercontent.com/google/fonts/main/ofl/protestrevolution/ProtestRevolution-Regular.ttf` |
| TELLER | Caveat Brush | `CaveatBrush-Regular.ttf` | `https://raw.githubusercontent.com/google/fonts/main/ofl/caveatbrush/CaveatBrush-Regular.ttf` |
| WORD | IM Fell English (roman) | `IMFeENrm28P.ttf` | `https://raw.githubusercontent.com/google/fonts/main/ofl/imfellenglish/IMFeENrm28P.ttf` |
| WORD (refs only) | IM Fell English Italic | `IMFeENit28P.ttf` | `https://raw.githubusercontent.com/google/fonts/main/ofl/imfellenglish/IMFeENit28P.ttf` |

- Load with `FontFace` + `delayRender`, same pattern as v1 `useFonts`.
- **SHOUT strings are typed in CAPS** (do not rely on the font's lowercase).
- **IM Fell is a light face.** Always add ink spread: `WebkitTextStroke: 1.4px currentColor`. Never below 70 px except the two verse refs.
- Why IM Fell: it is the type family of the old printed English Bible. Scripture looks printed; the story looks painted.
- All widths below are estimates. Builder measures each row with the real font and shrinks to `maxW` (as v1 `Row` does). Never squeeze letters.

---

## 3. Palette (pigments)

| Name | Hex | Use |
|---|---|---|
| INK | `#2B1D14` | Teller and Word on light ground |
| BONE | `#FBF1DA` | light paint on dark ground; under-coat of the Shout; the bare page |
| RED EARTH | `#B23A22` | Bartimaeus only: his cry, his prayer, `beggar?`, `one man.` (brighter than v1 MAROON `#7A2E22`, so it no longer sinks into his cloak; rings stay MAROON) |
| SAGE INK | `#2F5347` | Jesus's spoken words only (His mantle, at ink strength) |
| GOLD | `#E9B043` | `see.` and the glints. **Never before f1470.** |
| GLINT | `#FFF2C9` | the sun pass on letters, after f1470 only |
| DUSK | `#14302E` | soft dark lift under BONE letters on the cross sky |

Rules: RED EARTH = him. SAGE INK = His words. GOLD only after sight. No gold, ring or glow near Jesus's head.

---

## 4. Paint recipes (how a letter is made)

No recipe uses a drop shadow. No recipe uses an even all-round outline.

- **R1 INK (default, light ground).** Fill only. Container `mixBlendMode: "multiply"`. Filter `#gouache` (v1 filter; `scale` 5 for sizes under 90, 7 above). The wall's brush grain shows through.
- **R2 LIGHT PAINT (mid / dark ground).** Top coat BONE. Under-coat = the same text, colour INK (or RED EARTH where the table says), `WebkitTextStroke 8px` same colour, offset **(+3,+4)**, run through `#gouache2` (same filter, `seed 9`) so its edge wobbles differently from the top coat. Reads as a second coat of paint, not a sticker edge. No blend mode.
- **R3 SHOUT.** Top coat RED EARTH through `#drybrush` then `#gouache`. Under-coat BONE, `WebkitTextStroke 10px`, offset **(-3,-4)** (up-left, where the sun is), `#gouache2`.
- **R4 WORD.** IM Fell, fill + 1.4 px ink spread. Light ground: INK, `multiply`, plus a **lift** = a blurred BONE copy under it (`blur 10px`, opacity .55). Dark ground: BONE, plus a blurred DUSK copy (`blur 12px`, opacity .5). **No displacement filter** (keep the type crisp).
- **R5 BARE PAGE (Jesus speaks).** A patch of bare paper, then SAGE INK type on it. Patch = one closed path, fill BONE opacity .92, `#ragged`-style edge (v1 filter, `scale 26`), GRAIN at .08 on top:
  `M70,1322 C300,1284 800,1280 1010,1300 L1002,1502 C760,1548 320,1542 84,1526 Z`. No notches, no banner ends.
- **HOLLOW.** Top coat missing: only the BONE under-coat of R3 is drawn, opacity .9. Used once (`sight.`).
- **GILT.** Top coat GOLD, under-coat INK `WebkitTextStroke 7px`, offset (+3,+4). Used once (`see.`).

New filter:

```
<filter id="drybrush" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012 0.55" numOctaves="2" seed="5" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -7 0 0 0 4.7" result="m"/>
  <feComposite in="SourceGraphic" in2="m" operator="in"/>
</filter>
```
Target: about 8-10 % of each letter missing, in thin sideways streaks. If a letter loses a whole stroke, raise `4.7`. Fixed seed: no boil.

Hand wobble (TELLER and SHOUT only): word `i` gets a fixed tilt `(hash(i+at)-.5)*3` deg and a fixed baseline shift `(hash(i+at+7)-.5)*8` px. Fixed for the life of the word.

---

## 5. Moves (how words come and go)

| Name | Hand | What happens |
|---|---|---|
| `Shout` | SHOUT | On the spoken frame: opacity 0 to 1 in 2 f; scale .4 to 1 and travel 70 px **from the direction of his mouth** in 6 f, `Easing.out(Easing.back(1.6))`. At landing, 5 RED EARTH flecks (v1 `lens`, 20-46 px long) fly 30-90 px on along the same line in 8 f and stay. The word never crosses his face guard: start point is clamped outside it. |
| `Write` | TELLER | Per word, on the spoken frame: `clip-path: inset(0 X% 0 0)`, X 100 to 0 over `clamp(chars, 4, 8)` frames, linear. Soft leading edge: mask gradient 24 px. No scale, no bounce. |
| `Drop` | crowd only | opacity 0 to 1 in 2 f; y -26 to 0 in 5 f `Easing.out(cubic)`. No bounce. |
| `Press` | WORD | opacity 0 to 1 in 3 f (6 f on the cross, 14 f on the tomb). **No transform, ever.** After that the pixels do not change until the cut. |
| `Focus` | s12 only | `filter: blur()` 14 px to 0, `Easing.out(cubic)`. |
| `Glint` | TELLER after f1470 | One GLINT band, 120 px wide, leaning 20 deg, crosses the line's box left to right in 14 f, clipped to the letter shapes (`background-clip: text` on a copy), `screen` blend. Once per line. |
| `DustOff` | TELLER exits | opacity 1 to 0 and move 24 px along the shot's ROAD direction over the listed frames; 8 SAND strokes (v1 `lens`) start inside the line box and ride on 40 px. Before f1470 SAND, after it GOLD. |

Exits are on the cut unless the table lists a `DustOff`.

---

## 6. Beat table (every text item)

Positions: `c(x,y)` = row centre x, **baseline** y. `L x` / `R x` = left / right edge. Safe box x 60-1020, y 200-1540. Sizes in px.

| Frames | Shot | Words (exact) | Hand / recipe | Size, place | Move and frames |
|---|---|---|---|---|---|
| 0-90 | s01 hook | Row A: `JESUS,` + `THOU SON OF DAVID,` | SHOUT / R3 | `JESUS,` 104, rest 54, one baseline, c(540,275), maxW 860, tilt -2 deg | `JESUS,` is on at f0 already at scale .85, lands by f4. THOU f23, SON f25, OF f32, DAVID, f37 |
| | | Row B: `HAVE` `MERCY` `ON` `ME.` | SHOUT / R3 | **growing: 84 / 100 / 118 / 144**, one baseline, c(540,396), maxW 780 (stays inside the dark frame, x 150-930), tilt -3 deg (rises to the right) | `Shout` f58 / 61 / 72 / 79 |
| 90-150 | s02 hush | `Be quiet!` x3 (the "many") | TELLER / R2 | 64 at c(800,720) tilt -4; 80 at c(640,870) tilt +3; 104 at c(800,1035) tilt -3. All on robes, under every face. | `Drop` f114 / f126 / f133. From f133 all three sink 6 px more over 8 f (they press down on him). |
| 150-300 | s03 name | `Bartimaeus` | TELLER / R1 | 132, c(715,1450), tilt -4 deg (lies along the road), maxW 620 | `Write` f170 (8 f). v1 `Swash` under it, now RED EARTH, f177-185, y 1478 |
| | | `a blind beggar` | TELLER / R1 | 80, c(715,1535), tilt -4 deg | `Write` f221 |
| | | `Jericho` | TELLER / R1 | 88, c(700,325) | `Write` f260 |
| 300-450 | s04 the hard phrase | `“SON OF DAVID”` | SHOUT / R3 (his words) | 76, c(540,285) | `Shout` f313, small: scale .7 to 1, no flecks |
| | | `means` | TELLER / R1 | 64, c(540,355) | `Write` f331 |
| | | `God's promised King` | TELLER / R1 | 108, c(540,470), maxW 900 | `Write` by word f338 / 355 / 365. All three rows `DustOff` f392-402 (down). No words after f402. |
| 450-624 | s14 the road | `Jerusalem` | TELLER / R1 | 104, c(540,330) | `Write` f456 |
| | | `Would He stop` / `for a beggar?` | TELLER / R2. `beggar?` has a RED EARTH under-coat | 124, c(540,1275) and c(540,1410), maxW 900 | `Write` by word f557 / 563 / 566, then f574 / 583 / 586 |
| 624-798 | s05 louder | Row A: `THOU SON OF DAVID,` | SHOUT / R3 | 78, c(540,300), maxW 860 | `Shout` by word f695 / 700 / 706 / 713. Knocked out f733-738: y 0 to -30, opacity to 0. |
| | | Row B: `HAVE` `MERCY` `ON` `ME.` | SHOUT / R3 | **growing: 92 / 112 / 132 / 160**, one baseline, c(540,318), maxW 950 (**x 65-1015: it paints over the dark frame on both sides - the frame cannot hold him**), tilt -2 deg | `Shout` f739 / 742 / 754 / 760. All motion done by f766. **f768-798: frozen with the road.** |
| 798-900 | **s06 SACRED** | `And Jesus` \| `stood still` + `Mark 10:49` | WORD / R4 on light | 76, **one baseline y 1470, split by His body**: left block right edge x 400 (maxW 335), right block left edge x 668 (maxW 350). His robe hem stands in the gap. Ref: Fell Italic 40, L 668, baseline 1530. | `Press`: And f800, Jesus f802, stood f811, still f820, ref f830. Nothing of ours moves. |
| 900-1011 | s07 He calls | `He stopped` / `for one man.` | TELLER / R1; `one man.` in RED EARTH (still `multiply`) | 108, L 70, baseline 290. Row 2: 96, L 70, baseline 395, maxW 480 (stops 17 px short of His face guard) | `Write` f924 / 931, then f940 / 951 / 959 |
| 1011-1152 | s08 cloak | `He came.` | TELLER / R1 | 124, c(600,305), tilt -3 deg | `Write` f1060 (4 f). `DustOff` f1125-1135 (left). |
| 1152-1254 | s09 Jesus asks | `What wilt thou that I` / `should do unto thee?` | WORD / R5, SAGE INK | 70, c(540,1395) and c(540,1485), maxW 860 | Page patch wipes on left to right f1158-1168, then is still. `Press` by word: f1170 / 1174 / 1184 / 1194 / 1204, then f1210 / 1216 / 1224 / 1237 |
| 1254-1344 | s10 his prayer | `Lord,` / `that I` / `might` / `receive` / `my` / `sight.` | TELLER / R3 colours (RED EARTH on BONE coat), no `#drybrush`. **`sight.` = HOLLOW** | 80, right edge x 1010, baselines 350 / 440 / 530 / 620 / 710. `sight.` 96, baseline 815. Column is x 770-1010; his nose is x ~710. | `Write` f1261 / 1286 / 1294 / 1304 / 1315 / 1324. `sight.` stays empty to the cut. |
| 1344-1470 | s11 He heals | `Go thy way; thy faith` / `hath made thee whole.` | WORD / R5, SAGE INK | same patch and places as s09 | Patch f1350-1360. `Press` f1351 / 1358 / 1365 / 1404 / 1407, then f1418 / 1437 / 1444 / 1453 |
| 1470-1680 | **s12 HERO** | (nothing f1470-1584) then `At once he could` / `see.` | TELLER / R1; `see.` = **GILT** | Row 1: 72, R 1010, baseline 262. Row 2: `see.` **160**, R 1010, baseline 400. Both above his hair, right of Jesus's hair. | Row 1 words on at f1585 / 1590 / 1618 / 1624, the whole row under `Focus` f1585-1624 (soft smear that sharpens). `see.` `Press` f1628, fully sharp + `Glint` f1630-1644. First gold letter in the film. |
| 1680-1830 | s13 he follows | `He followed Jesus` | TELLER / R1 | 104, c(540,315) | `Write` f1737 / 1756 / 1771. `Glint` f1775-1789. `DustOff` f1790-1798 (up, GOLD). |
| | | `up the road to Jerusalem.` | TELLER / R1 | 84, c(540,315), maxW 880 | `Write` whole line f1798-1816 (follows the voice). Out on cut. |
| 1830-1950 | **s15 CROSS (SACRED)** | `He died` / `for our sins.` | WORD / R4 on dark: BONE + DUSK lift | 88, R 1000, baselines 305 and 405 (the dark teal sky, top right; far from the cross box) | `Press` 6 f at f1859 and f1886. Nothing else. |
| 1950-2070 | **s16 TOMB (SACRED)** | `He rose to life.` | WORD / R4 on light: INK | 96, c(540,1470) | `Press` 14 f at f2021 (with the warm lift). Holds to f2079. No gold on the letters: the motes carry the gold. |
| 2070-2375 | s17 bookend | `Jesus stood still` | WORD / R4 on light: INK | 88, c(540,262) | `Press` by word f2167 / 2178 / 2195 |
| | | `for one man.` | TELLER / R1 in RED EARTH | 104, c(540,350), maxW 520 | `Write` f2207 / 2224 / 2232. One `Glint` over both rows f2240-2256. |
| | | `Mark 10:46-52` | WORD, Fell Italic, INK | 42, L 600, baseline 420 | `Press` f2300. **Nothing new after f2315. No fade.** |

Word changes from v1 (meaning kept): sentence case everywhere except the Shout; `a blind beggar by the road` -> `a blind beggar`; `BE QUIET!` -> three small `Be quiet!`; final stops added (`He came.` `for one man.` `He rose to life.` `for our sins.`). KJV lines are letter-for-letter as v1.

---

## 7. Rules and QC (add to the v1 checklist; v1 face rules still bind)

- [ ] **Faces:** no letter, under-coat, fleck, page patch or glint pixel inside any guard of v1 section 5, on every QC grab. The `Shout` flight path is clamped outside the face guard.
- [ ] **KJV exact:** `Jesus, thou Son of David, have mercy on me.` / `Thou Son of David, have mercy on me.` / `And Jesus stood still` / `What wilt thou that I should do unto thee?` / `Lord, that I might receive my sight.` / `Go thy way; thy faith hath made thee whole.` (caps in the Shout are a lettering choice, not a text change).
- [ ] **WORD never moves:** frame-diff the text layer alone on s06, s09, s11, s15, s16 after each word is on: zero change.
- [ ] **No gold before f1470.** RED EARTH only on his words + `beggar?` + `one man.`. SAGE INK only on Jesus's two lines.
- [ ] **Phone test:** view each beat at 360 px wide. Every row readable. Tightest: s06 (76 px on paving), s10 column on the dark edge, s12 row 1 (72 px), `#drybrush` on Row A of s05.
- [ ] **Sound-off test:** watching muted, a newcomer can say who / what / why from the words alone.
- [ ] **Sacred calm:** s06, s15, s16 have no Shout, Write, Drop, DustOff, Glint or fleck.
- [ ] s05: all text motion ends by f766; f768-798 nothing of ours moves.
- [ ] All type inside x 60-1020, y 200-1540 (the s05 Row B reaches x 65-1015 on purpose).

## 8. Risks (honest)

1. **I have not seen this rendered.** The preview page is static HTML that I was not allowed to open; the three new fonts are chosen from knowledge, not from a test on this art. First build step: render 6 stills (f82, 765, 830, 1240, 1335, 1640) and look.
2. **Positions come from single frames.** Clips move. Tightest fits: s01 Row B vs hair top (~y 430); s06 blocks vs His hem (x ~415-655); s10 `sight.` vs nose; s17 row 2 vs Jesus's head guard (top y 355). Shrink 8 px at a time; never squeeze.
3. **Font widths are estimates.** Fit every row to its `maxW` with the real file.
4. **s06 at 76 px is smaller than v1's 104.** It buys the "He stands inside the sentence" idea. If it reads small on a phone: fall back to two centred rows under His guard (`And Jesus` / `stood still`, Fell 100, c(540,1425) and c(540,1530)) - still, inked, no outline.
5. **`multiply` ink on a dark patch** disappears. Any R1 row that crosses the DARK edge or a shadow must switch to R2. Check s08 (`He came.` near the top edge) and s07.
6. **Protest Revolution is rough by design.** If Row A of the cries is hard to read at 54-78 px, set Row A in Caveat Brush (RED EARTH, R3 colours) and keep Protest Revolution for the big `HAVE MERCY ON ME.` only.
7. **The under-coat is still a second colour round the letter.** It is offset and wobbly, not an even ring, but if it starts to look like the v1 sticker, cut its stroke from 10 to 6.
8. Simulated judgement only. No real viewer has seen it.
