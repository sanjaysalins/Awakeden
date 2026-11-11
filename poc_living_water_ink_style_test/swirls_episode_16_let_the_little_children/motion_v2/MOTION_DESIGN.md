# Ep16 "Let the Little Children" — Motion layer v2 (design spec, build-ready)

Comp: 1080x1920, 30 fps, 2271 frames. Base: `_remotion/public/ep16/base.mp4` (untouched).
Replaces the 5 pills in `_remotion/src/Ep16Children.tsx`. Build as a NEW file (`Ep16ChildrenV2.tsx`), keep v1.
All frames below are absolute comp frames. Word times come from `narration.alignment.json` (x30, rounded).
Positions were checked on real frames (gridded contact sheets) for faces and Shorts safe zones.

---

## 1. The idea in 3 lines

1. **The storyteller's desk.** Every mark looks made by the same hand that drew the film: torn paper, soft pencil, one brush of watercolour. No pills, no UI shapes.
2. **Grey pencil is the world's "no". Blue watercolour is Jesus's "yes".** People's words sit on paper in graphite. Jesus's words are painted in the blue of His own tunic.
3. **One small paper slip, "not now", is the thread.** It lands in the hook, comes back when the followers block the children, and at the end Jesus's blue washes over it.

Second thread (the spine): a small pencil **"a touch"** (seen twice) is answered by a big blue **"His arms."**

---

## 2. Beat table (8 moments)

Shot cuts (frames): sA 0-78 · p01 78-228 · p02 228-315 · sB 315-450 · p03 450-624 · sC 624-708 · p04 708-837 · sD 837-975 · p05 975-1158 · sE 1158-1305 · sF 1305-1437 · p06 1437-1614 · p07 1614-1746 · p08 1746-1878 · sG 1878-1950 · sH 1950-2040 · p09 2040-2269.

Safe box for TEXT: x 60-950, y 160-1490. "Box" = outer edge of the carrier (x1-x2, y1-y2). Font = Kalam 700 unless noted.

| # | Frames (on-off) | Word it hits | What appears | Motion | Box (px) / size | Colours | Why |
|---|---|---|---|---|---|---|---|
| **1a** | 0-162 | "pushed … away?" (f19-44) | Cream swatch, text **Pushed away?** | Already fully there on frame 0 (first-frame hook). Settle: scale 1.05→1, f0-6, ease-out cubic. Out: opacity 1→0, f150-162. | 305-945, 190-340. Text 104 px, centre (625, 265). | Swatch `#F6EEDC`, text `#2E2A27` | Hook must read on the very first frame. Sits on the buildings, right of the man's head (x<230), above the boy's face (y>740). |
| **1b** | 95-162 | "**not** now" (f95) | The **slip**: torn grey paper, text **“not now”** | Slap-down: f95-101, scale 1.25→1, rotate -9°→-3°, opacity 0→1 in first 4 f, ease-out back(1.6). Shadow grows 0→full over same 6 f. Out with 1a, f150-162. | 345-775, 370-510 (430x140). Text 92 px. Rotation -3°. | Slip `#E4DFD3`, text `#3A3A3C`, shadow `rgba(60,40,20,.28)` | Births the thread object. Cold grey paper vs warm cream = "someone else's word put on you". Lands after the cut (f78), on the backs of the crowd, no faces. |
| — | 162-393 | quiet (7.7 s) | nothing | | | | Let the pictures breathe. |
| **2** | 393-450 | "**touch**" (f401) | Small cream swatch, text **a touch**, then one pencil underline under "touch" | Swatch paints on f393-399 (L→R wipe). Text writes on f396-406 (so "touch" completes at ~f404). Underline draws f406-414, ease-out. Out: opacity f441-450. | 410-790, 180-315. Text 96 px, centre (600, 248). Underline from (548, 296) to (742, 290), 7 px. | Swatch `#F6EEDC`, text `#2E2A27`, underline `#9A4A2B` | Seeds the spine word. Top band is wall/tree; mother's hair starts y≈390. Small on purpose. |
| **3** | 497-612 | "**rebuked**" (f497), held through "tried to stop them" (to f592) | The same **slip “not now”** | Same slap-down as 1b, f497-503, rotate +7°→+2°. Hold. Out: f600-612, opacity 1→0 and y +24 px (slips off), ease-in cubic. | 385-815, 310-450. Same size as 1b. Rotation +2°. | as 1b | Ties the viewer's "not now" to the story: this is what the followers did to the children. Also explains "rebuked" to ESL viewers without a definition. Over building/tree; followers' heads start y≈560. **See risk note R1.** |
| — | 612-794 | quiet (6 s) | nothing | | | | "Then Jesus saw it" plays clean on His face. |
| **4** | 794-836 | "**Angry.**" (f794) | Cream swatch, text **Angry.**, two hard pencil underlines | No write-on (anger does not write slowly). Swatch + text stamp in together: f794-797, scale 1.12→1, opacity 0→1, ease-out cubic. Underline 1 draws f798-802, underline 2 draws f803-807 (linear, fast). Out: opacity f827-836. | 280-800, 1262-1462. Text 150 px, centre (540, 1345). Underlines: (330,1428)→(752,1418) and (352,1446)→(736,1440), 9 px and 6 px. | Swatch `#F6EEDC`, text `#2E2A27`, lines `#9A4A2B` | Plain meaning of "much displeased". On the tunic, well under the beard (y≈1170). Ends inside p04 so it never crosses onto the children's faces in sD. |
| — | 836-977 | quiet (4.7 s) | nothing | | | | "Not with the children" is said by the picture (kids at His side). |
| **5** | 977-1158 | Jesus speaks (voice starts f979). Line 2 on "**to come unto me**" (f1017) | Blue **wash**, text **Let the children / come to Me.** Small tag **Jesus · Mark 10:14** | Wash blooms f977-991 from its left end (see 3.3). Line 1 writes on f983-1001. Line 2 writes on f1017-1031. Tag fades in f1040-1050. Hold. Out: all opacity f1146-1158. On screen 6.0 s. | Wash 130-950, 160-415. Text 88 px, line centres y 240 and y 338, x-centre 540. Tag swatch 140-420, 408-460, text 38 px (Kalam 400), rotate -1.5°. | Wash `#3D6497`, edge `#2B4A75`, text `#FBF4E4`. Tag swatch `#F6EEDC`, text `#2E2A27` | The hero moment. First blue in the film. The plain meaning sits on screen while the KJV is spoken, so "Suffer" cannot be misread as pain. Above His head (hair top y≥443); tag sits left over tree/wall. |
| — | 1158-1535 | quiet (12.6 s) | nothing | | | | The kids run to Him, then sit with Him. The plain-words narration carries it. No text needed. |
| **6** | 1535-1612 | "**like a little child.**" (f1539-1568) | Cream swatch, text **like a little child** | Swatch paints on f1535-1541. Text writes on f1539-1562 (tracks the voice). Hold. Out: opacity f1602-1612. | 190-890, 205-345. Text 84 px, centre (540, 275). | Swatch `#F6EEDC`, text `#2E2A27` | The one line aimed at grown-ups. Over arch/tree; faces start y≈715. |
| — | 1612-1900 | quiet (9.6 s) | nothing | | | | **The two hero pictures (He picks the boy up, He blesses the girl) play with NO text.** The picture is the verse. |
| **7a** | 1900-1950 | "a **touch.**" (f1911) | Small cream swatch **a touch** + underline (exact twin of beat 2) | Swatch paints f1900-1905. Text writes f1903-1912. Underline f1912-1919. Hard cut out with the shot at f1950 (no fade). | 100-440, 262-390. Text 84 px, centre (270, 326). Underline (232,372)→(402,367), 6 px. | as beat 2 | Viewer has seen this exact small mark before (beat 2). Top-left blur is empty in every frame of sG; the hands stay right/below. |
| **7b** | 1978-2040 | "His **arms.**" (f1984-1999) | Big blue **wash**, text **His arms.**, one cream brush arc under it | Wash blooms f1978-1990. Text writes on f1986-1999. Arc draws f1999-2011, ease-out. Out: opacity f2030-2040. | Wash 220-860, 180-400. Text 150 px, centre (540, 278). Arc: `M 318 352 Q 540 398 762 352`, 10 px, round caps. | Wash `#3D6497`, text + arc `#FBF4E4` | The spine lands: small grey pencil "a touch" → much bigger, blue, painted. The arc is a simple open curve (reads like arms going round). Over the olive tree; His head starts y≈520. |
| **8a** | 2072-2176 | "**not** now." (f2072) | The **slip “not now”**, small, top-left | Slap-down f2072-2078 (as 1b), rotate -10°→-4°. Hold. Then on "**Look**" (f2137): blue bloom grows over it f2137-2151 (radius 0→250 px from slip centre). Slip text fades f2139-2147. The blue stain fades out f2158-2176. | 70-390, 185-295 (320x105 = the 1b slip at scale 0.75). Text 69 px. Bloom centre (230, 240). | Slip as 1b. Bloom `#3D6497` at 0.85 | Third and last return. Jesus's colour covers the "no". Top-left arch is free in every frame (girl's bun x≥410, her waving hand x≥410, y≥320). |
| **8b** | 2140-2269 (end) | "**Look** at who **Jesus picked up.**" (f2137-2178) | Blue **wash**, text **Look at who / Jesus picked up.** | Wash blooms f2140-2154. Line 1 writes on f2146-2158. Line 2 writes on f2158-2178 (tracks "Jesus" f2152, "picked" f2164, "up" f2175). **No out.** Holds to the last frame (3.0 s still after the last word). | Wash 120-920, 1222-1478. Text 90 px, line centres y 1302 and y 1402, x-centre 520. | Wash `#3D6497`, edge `#2B4A75`, text `#FBF4E4` | Landing line in Jesus's colour, on the robe. All three faces stay clear (lowest face edge y≈1145-1210). Stays inside the Shorts safe box (bottom 1490, right 950). |

Count: 8 moments, 5 quiet stretches (7.7 s, 6 s, 4.7 s, 12.6 s, 9.6 s). Blue appears only 3 times (beats 5, 7b, 8).

### Timing notes the builder must know
- whisperx gives "Suffer" f939 and "He [took]" f1646. Both are wrong (stretched over a pause). Real voice starts are **f979** (Jesus) and **f1694** ("took"). These match v1 and the shot cuts. Do not use the json value for those two words. Confirm f979 by ear before final render.
- Beat 3's slip is on screen f497-612 = 3.8 s. Beat 4 is short (1.4 s) but it is one word at 150 px.
- Beat 7b text is fully written for about 1.0 s before the fade (2 words at 150 px). If it feels rushed on a phone, start the fade at f2034 instead of f2030. Do not let it cross the cut at f2040.

### Risk note
- **R1 (beat 3).** Mark 10 does not quote what the followers said. The slip is the film's own hook phrase used as a motif, not a Bible quote: it has no speech tail and no speaker tag, and it is the same object as in the hook. If the doctrine panel objects, drop beat 3 only. Beats 1 and 8 still bookend on their own.

---

## 3. Device build notes (Remotion)

File: `_remotion/src/Ep16ChildrenV2.tsx`. Layers, bottom to top: `OffthreadVideo` → `<Defs/>` (zero-size SVG holding all filters) → beats (each in a `<Sequence layout="none">`) → `<PaperGrain/>`.

Shared helpers:
```ts
const clamp = {extrapolateLeft:"clamp", extrapolateRight:"clamp"} as const;
const OUT  = Easing.out(Easing.cubic);
const BACK = Easing.out(Easing.back(1.6));
const boilSeed = (f:number) => [3, 11, 27][Math.floor(f/5) % 3];   // 6 fps "line boil", 3 poses
```
`boilSeed` must be fed the ABSOLUTE comp frame (inside a Sequence, add the Sequence's `from`), so re-renders are identical.

### 3.0 `<Defs/>` — the four filters (define once)
All filters: `x="-15%" y="-15%" width="130%" height="130%"`, `colorInterpolationFilters="sRGB"`.

```xml
<!-- deckle: rough hand-torn / dry-brush EDGE for swatches and the slip. Static seed. -->
<filter id="deckle">
  <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G"/>
</filter>

<!-- wash: watercolour edge, bigger and lazier than deckle. Static seed. -->
<filter id="wash">
  <feTurbulence type="fractalNoise" baseFrequency="0.009 0.016" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="34" xChannelSelector="R" yChannelSelector="G"/>
</filter>

<!-- graphite: grain knocked out of TEXT. NO displacement, static seed (text must never shimmer). -->
<filter id="graphite">
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="9" result="g"/>
  <feColorMatrix in="g" type="matrix"
     values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.85" result="holes"/>
  <feComposite in="SourceGraphic" in2="holes" operator="in"/>
</filter>

<!-- pencil: wobble + grain for drawn STROKES only (underlines, arc). seed = boilSeed(frame). -->
<filter id="pencil">
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed={boilSeed(frame)} result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="4" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="9" result="g"/>
  <feColorMatrix in="g" type="matrix"
     values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.85" result="holes"/>
  <feComposite in="d" in2="holes" operator="in"/>
</filter>
```
Tune the last matrix number (1.85) so about 10-12% of ink pixels are knocked out. Text must stay fully readable at phone size. If in doubt, less grain.

### 3.1 `<Swatch>` — cream paint/paper carrier (beats 1a, 2, 4, 6, 7a, tag in 5)
- One `<svg>` at full comp size, `position:absolute`.
- Shape: `<rect x y width height rx="18">` inset 14 px from the Box in the table (the deckle filter pushes the edge back out to about the Box). `fill="#F6EEDC"`, `fillOpacity=0.94`, `filter="url(#deckle)"`.
- Dry-brush tail: a second rect, same vertical centre, height 55% of the first, starting at 70% of the width and running 40 px past the right end (but never past x 950), `fillOpacity=0.55`, same filter. This gives the "brush ran out of paint" right edge. Skip the tail on beat 1a (already at x 945) and on the tiny tag in beat 5.
- Paper shade: a third copy of the main rect, `fill="#E6D8BC"`, `fillOpacity=0.35`, translated (0, 5), drawn FIRST (under), same filter. A thin warm lower edge, not a drop shadow.
- **Paint-on** (beats 2, 6, 7a): wrap the three rects in `<g mask="url(#mN)">`. Mask = white `<rect>` whose width goes 0→(box width+60) over 6 frames, linear, with `filter="url(#deckle)"` on the mask rect so the leading edge is ragged.
- Beat 1a and 4 do not paint on (see table).

### 3.2 `<WriteOn>` — the text (all beats)
- Real HTML text: `<div style={{fontFamily:"Kalam", fontWeight:700, fontSize, lineHeight:1.1, whiteSpace:"nowrap", color, filter:"url(#graphite)"}}>`, absolutely placed so the line's centre matches the table.
- Reveal per line with CSS `clip-path: inset(-20% R% -20% -5%)` where `R = interpolate(frame,[start,end],[105,-5],{...clamp})` — **linear** (a hand writes at an even speed).
- Speed floor: never faster than 1.0 frame per character.
- On blue washes use colour `#FBF4E4` and **no** `#graphite` filter (cream paint on blue should be solid; grain there costs contrast). Add `textShadow:"0 2px 0 rgba(30,50,85,.45)"`.
- No letter boil, no per-letter bounce. Text is still once written.

### 3.3 `<Wash>` — Jesus's blue watercolour (beats 5, 7b, 8b, and the bloom in 8a)
Four stacked SVG shapes, all the same rounded rect (`rx=60`, inset 24 px from the Box), all `filter="url(#wash)"`, all inside one `<g mask>`:
1. **Bleed halo** — fill `#3D6497`, `fillOpacity .22`, scaled 1.05 about the centre, `style={{mixBlendMode:"multiply"}}`. Wet paper around the stroke.
2. **Body** — fill `#3D6497`, `fillOpacity .90`.
3. **Pooled edge** — no fill, `stroke="#2B4A75"`, `strokeWidth 7`, `strokeOpacity .55`. Pigment gathering at the rim; this is what makes it read as watercolour and not a blue pill.
4. **Mottle** — fill `#6E93C4`, `fillOpacity .16`, with its own extra filter: feTurbulence `baseFrequency 0.035`, octaves 2, seed 21 → feColorMatrix alpha = `1.6*R - 0.5` → `feComposite in` with the shape. Soft lighter blotches inside.

**Bloom-in mask** (14 frames, ease-out cubic): mask = white `<ellipse>` centred on the wash's LEFT end at mid-height (`cx = box.x1 + 90`, `cy = box mid-y`), `rx` 0→(box width × 1.15), `ry` 0→(box height × 1.3), with `filter="url(#wash)"` on the ellipse so the wet front is uneven. Group opacity 0→1 over the first 5 frames.
- Beat 8a bloom: a `<circle>` at (230, 240), r 0→250 over f2137-2151 (ease-out cubic), fill `#3D6497` `.85`, `filter="url(#wash)"`, plus the pooled-edge stroke (5 px). Fades out f2158-2176. Check on f2151 that the displaced edge stays left of x 410 (the girl's bun); if not, cap r at 220.
- Out (beats 5, 7b): plain opacity fade. No un-bloom.

### 3.4 `<Slip>` — the "not now" paper (beats 1b, 3, 8a) — ONE component, three uses
- Props: `cx, cy, scale, rotFrom, rotTo, at`.
- Paper: `<polygon>` 430x140 with slightly uneven corners — points (relative to top-left): `0,8 212,0 430,6 426,134 220,140 4,132`. Fill `#E4DFD3`, filtered with a local copy of `#deckle` at `scale="9"` (a tear, finer than brushed paint).
- Shadow: the same polygon under it, fill `rgba(60,40,20,.28)`, translate (4, 9), `filter: blur(7px)`. This is the ONLY drop shadow in the film: the slip is an object lying on the page, everything else is paint on the page.
- Text: `“not now”` (real curly quotes), Kalam 700, 92 px, `#3A3A3C`, `filter:url(#graphite)`, centred.
- Slap-down over 6 frames from `at`: `scale` 1.25→1 (× prop scale), `rotate` rotFrom→rotTo, both BACK easing; opacity 0→1 in 4 frames; shadow opacity 0→1 over the 6 frames.
- Transform origin = slip centre. No idle wobble after landing.

### 3.5 `<PencilLine>` and the arc (beats 2, 4, 7a, 7b)
- `<path d="M x1 y1 Q mx my x2 y2" pathLength={1} strokeDasharray={1} strokeDashoffset={1-p} fill="none" strokeLinecap="round" filter="url(#pencil)"/>`.
- Underlines: control point = line midpoint shifted 6 px down (a slight sag). `p` from `interpolate(frame,[a,b],[0,1],{...clamp, easing: OUT})`.
- Beat 4's two lines use linear easing and 4-5 frames each (pressed, fast).
- Beat 7b arc: path in the table, stroke `#FBF4E4`, 10 px; add a second pass of the same path, 3 px, opacity .5, translated (6, 9), starting 3 frames later (dry second bristle).
- The `#pencil` filter boils (3 poses, changes every 5 frames). It is used ONLY on these strokes.

### 3.6 `<PaperGrain/>` — top layer, whole frame, subtle
- Purpose: put the overlays and the film under one sheet of paper so nothing looks pasted on.
- Build as a CSS background on a full-frame div: an inline SVG data-URI, 540x960, containing `<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="5"/>` + `<feColorMatrix type="saturate" values="0"/>`, `background-size:1080px 1920px`.
- `mixBlendMode:"multiply"`, `opacity: 0.06`. **Static** (no flicker, no moving grain).
- No vignette, no colour grade, no light leaks. The footage grade is already right.
- If render time suffers, drop this layer first; it is the least important.

---

## 4. Fonts, palette, texture

**Font (one hand for the whole film):** Kalam (Google Fonts). 700 for all lines, 400 for the one small tag. Already bundled (`_remotion/public/Kalam-Bold.ttf`, `Kalam-Regular.ttf`), load with the existing `useFonts()` from `TalithaCumi.tsx`. No second typeface: the change in look comes from paper, pencil and paint, not from a new font.

**Palette**

| Role | Hex |
|---|---|
| Warm paper (swatches) | `#F6EEDC` |
| Paper shade (lower edge) | `#E6D8BC` |
| Graphite (narrator text) | `#2E2A27` |
| Cold slip paper | `#E4DFD3` |
| Slip text | `#3A3A3C` |
| Sienna pencil (underlines only) | `#9A4A2B` |
| Jesus blue (wash body) | `#3D6497` |
| Blue pooled edge | `#2B4A75` |
| Blue mottle | `#6E93C4` |
| Cream paint on blue (text, arc) | `#FBF4E4` |

Rule: blue is only ever Jesus's words or act. Sienna is only ever a pencil underline. Nothing else gets a colour.

**Texture:** `PaperGrain` at 6% multiply, static (3.6). That is all.

---

## 5. What I cut and why

- **A drawn "stop" line across the street (p03)** — the frame is full of people and children; a line would cross bodies and look pasted on. The returning slip says the same thing better.
- **A pencil ring around the touching hands (sG)** — the hands move through the whole shot, so a ring would drift off them. Sloppy risk.
- **A blue "embrace" arc drawn around the group hug (sH)** — His arms are already around them in the picture. Drawing it again is noise. Kept only as a small arc under the words.
- **Text on "He took them up in his arms" and "blessed them" (p07, p08)** — these are the two best pictures in the film. They play clean. Also removes the old "Mark 10:16" chip; one reference (10:14) places the story, and the full range goes in the description.
- **"This story is for you", "Not with the children", "Do not stop them", "God's kingdom belongs to…"** — all spoken clearly over pictures that show them. More text would turn the film into subtitles.
- **Strike-through on "a touch"** — He did not refuse the touch, He gave more. So "a touch" is never crossed out; it is simply answered by something bigger.
- **Letter-by-letter bounce, boil on text, moving grain, glow, sparkle, light sweeps** — hurts reading (ESL / dyslexia) and reads as app template, not storybook.
- **A second display font** — one hand, one storyteller.
- **Un-bloom / fancy exits** — every exit is a plain short fade (or a hard cut with the shot). Entrances carry the craft; exits stay invisible.

---

## 6. QC list before showing the owner (all $0)

1. Export stills at f0, 100, 404, 520, 806, 1035, 1565, 1915, 2012, 2100, 2150, 2265. On each: no carrier touches a face; every text box inside x 60-950, y 160-1490.
2. Frame 0 shows "Pushed away?" fully written.
3. Play at 1x on a phone-size window: each text readable in one pass; "Angry." and "His arms." land on the word, not before.
4. Zoom 2x on text edges: grain has not eaten thin strokes (look at "t", "i", the quote marks).
5. Blue wash edge looks like wet paint (uneven, darker rim), not a rounded rectangle. If it reads as a pill, raise `#wash` scale to 44 and the rim opacity to .65.
6. Hold check: last frame = landing wash fully written; audio and video same length (`check_landing_hold.py`).
