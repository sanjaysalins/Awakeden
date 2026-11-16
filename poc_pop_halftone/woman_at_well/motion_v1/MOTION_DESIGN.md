# Woman at the well (Pop Halftone) - Motion layer v1 (design only, $0)

Comp 1080x1920, 30 fps, 2635 frames (87.83 s). Base = the 19 clips, 1.0x, same order, same cuts, audio untouched.
Frames are film frames, `f = round(film seconds x 30)`.
Cut frames: c01 0 | c02 132 | c03 240 | c04 348 | c05 434 | c06 569 | c07 683 | c08 801 | c09 981 | c10 1125 |
c11 1340 | c12 1463 | c13 1568 | c14 1653 | c15 1737 | c16 1977 | c17 2127 | c18 2263 | c19 2444 | end 2635.

**Two honest limits.**
- **Word frames are estimates (marked ~).** There is no word-level alignment file in `audio/`. Run a $0 forced
  alignment first and snap every "~" beat to its real word.
- **Positions are read off one small gridded frame per clip (good to about +-30 px).** Clips move (c17 pans a lot).
  Re-read every position on the first, middle and last frame of each clip. c13 and c18 are being re-made: re-read them.

---

## 1. One-line idea

**Well water falls and is gone. His water springs up.**
One bold comic water drop tells the whole story: empty outline = thirst. White drop falling = well water.
Teal drop rising = living water (John 4:14, "springing up"). The jar gets the same three "look here" ticks three times.

## 2. House look (6 lines)

1. **Sticker shapes.** Every doodle = flat fill + 9 px black outline + 4 px white edge outside it. Reads on any ray colour. No scratch, no wobble, no grain.
2. **Four colours, eyedropped from the clips:** teal, yellow, white, black. Red and orange stay the art's. Colour fill sits 5 px right-down of its outline (comic print offset).
3. **Big.** Drops 130-190 px tall. Ticks 110-160 px long, 16 px thick. Burst star 500 px wide.
4. **Loud half (c01-c09):** pop in 8 frames with back-ease (`pop` from SecondFireV1), then bob (scale +-3%, y +-6 px, period 80, phase = x). **Quiet half (c10-c19):** slow "well up" (40 frames, sine), no bounce.
5. **Nothing fades, nothing boils, no `Math.random`.** Things leave on the cut or shrink to 0 in 6 frames. Opacity is 100% or 0%.
6. **Keep-out is hard:** box every face (+40 px), every hand (+30 px), all of Jesus (+30 px). No doodle pixel inside. Nothing ever sits in a ring or arc round His head.

**Words on screen: two only.** `WHY?` (hook, comic burst, Bangers). `THE SAVIOUR OF THE WORLD` (KJV John 4:42, word for word, calm white box, straight, no bounce). Bangers.ttf is already in `_remotion/public`.

**Doodle kit (8 parts):** Drop (empty / white / teal) - Splash crown - Ripple ring - Jar ticks (5 strokes in a fan) -
Burst star - Dot rays (Ben-Day dots running out from the art's own sun) - Dust puff - Tomb flower (the art's own 5-petal outline flower).

---

## 3. Shot by shot (all 19)

"Tr." = how we go INTO THE NEXT shot. HARD = plain hard cut.

| Shot | Film time (frames) | Doodle: what, where, when | Tr. to next |
|---|---|---|---|
| **c01** jar alone (hook) | 0.00-4.40 (0-132) | **On frame 0:** 3 white drops already falling above the well mouth (~610,1370). They land f8, f20, f32, each with a small white splash crown. "She came for water." **~f80 "her jar":** 5 jar ticks pop in a fan above the jar mouth (~200,1190). **~f108 "Why?":** yellow burst star, centre (600,420), with `WHY?` 190 px. Pops, one small rock, then still. Sky only. | **T4 Question pop** (sec. 4) |
| **c02** she walks | 4.40-8.00 (132-240) | **~f140 "noon":** white dot rays run out of the art's sun behind the hill (~510,555). 9 rays, upward only, r 260 to 820. Draw f140-165, then crawl out slowly. Keep 60 px off her head and jar. | HARD |
| **c03** Jesus tired | 8.00-11.59 (240-348) | **Nothing.** First sight of Him. (The sun is right over His head here: any ray would read as a halo.) | HARD |
| **c04** "Give me to drink" | 11.59-14.47 (348-434) | **~f396 "drink":** ONE empty drop (outline only, 150 px) pops in the gap between the two heads, above His open palm, centre ~(560,880). 110 px clear of the palm, 150 px clear of both faces. Bobs. This is the "thirst" sign. | HARD |
| **c05** her surprise | 14.47-18.95 (434-569) | **f436 (right on the cut):** 3 surprise ticks pop up-left of her head, ~(230,520) (280,340) (430,230), pointing away from her. **~f520 "drink of me":** the empty drop pops top-right sky (880,330) and tips left-right once, like a question. | HARD |
| **c06** kept apart | 18.95-22.78 (569-683) | **~f600 "kept apart":** a bold black comic crack draws down the SKY only, x 540, y 0 to 470 (stops above the hill), 12 frames. **~f648 "asks":** the empty drop hops over the crack, (300,430) to (790,430), top of arc y 200, 16 frames. Lands with 3 tiny ticks. Both people are far below (heads y ~900). | HARD |
| **c07** "thirst again" | 22.78-26.70 (683-801) | Right sky lane only (x 760-1040, y 0-520). **~f738 "this water":** 3 white drops fall in, f730, f738, f746, and stop at (800,180) (900,330) (1000,250). **~f770 "thirst":** each one empties, top to bottom, f770, f777, f784. Three empty outlines hang. Nothing near His hand (hand ~870-1040, 1240-1340). | **T1 Well iris** |
| **c08** down the well | 26.70-32.70 (801-981) | **THE SPRING** (sec. 5, moment 2). Ripple rings, then 8 teal drops spring UP out of the colour disc, toward us. No words. | **T2 Burst fill** |
| **c09** her face | 32.70-37.49 (981-1125) | Right lane only (centre x 1010; check the shawl edge). **~f1010 "life":** 7 teal drops rise from below the frame, one every 9 frames, 40-frame flight, small S-path. They arc over the top and settle: (990,640) (960,380) (820,200) (600,130) (300,150) (120,300) (80,560). **~f1085 "never runs dry":** 3 more keep rising and are still in the air on the cut. It never stops. Nothing inside x 240-900, y 330-1920. | HARD |
| **c10** truth about her life | 37.49-44.68 (1125-1340) | **Quiet.** 3 teal drops are already hanging in the top sky on the first frame: (180,260) (560,140) (900,300). They only bob. Nothing pops. No count of five. The offer stays while the truth is told. | HARD |
| **c11** "the Christ will come" | 44.68-48.75 (1340-1463) | **~f1415 "will come":** white dot rays run out from the sun on the mountain she points at (~525,705). 7 rays, upward only, draw 30 frames. Nothing near her head or arm. | HARD (the cut IS the answer) |
| **c12** "I that speak unto thee am he" | 48.75-52.27 (1463-1568) | **Nothing.** | HARD |
| **c13** her tears + the 1 s silence | 52.27-55.10 (1568-1653) | **Nothing.** | HARD |
| **c14** she leaves the jar | 55.10-57.90 (1653-1737) | **~f1680 "her jar":** the same 5 jar ticks, above the jar mouth (~550,1200). Second time. **Dust puffs** on the path where she has just been: (290,1200) f1657, (430,1160) f1672, (585,1080) f1690, sizes 90 / 70 / 50 px. Each pops, then shrinks away in 10 frames. Check she is past each spot. | HARD (her line is somber now) |
| **c15** "Come, see a man" | 57.90-65.90 (1737-1977) | **Quiet.** Sky only (y 0-380). 4 teal drops well up slowly, one every 20 frames from f1745, at (120,170) (380,110) (700,140) (960,230). Then they only bob. Nothing new under "is not this the Christ?". | HARD |
| **c16** many come | 65.90-70.90 (1977-2127) | **~f2003 "Many come":** 8 teal drops well up left to right, 6 frames apart: (100,200) (120,450) (250,600) (460,620) (680,600) (880,620) (960,450) (980,210). Many drops for many people. **~f2064 "call Him":** white caption box, centre (540,330), two rows `THE SAVIOUR` / `OF THE WORLD`, 100 px. Wipes on left to right in 8 frames. Stays to the cut. Drops stay outside the box. | HARD (on "The jar stayed.") |
| **c17** the jar stayed | 70.90-75.44 (2127-2263) | **~f2140 "jar":** the 5 jar ticks, third time, above the jar mouth (~220,1165). **The jar drifts: track it** (2-point move). **~f2190 "came for water":** one empty drop pops above the jar, ~(220,960). **~f2238 "better water":** it fills teal, bottom to top, 8 frames. | **T3 Drop iris** |
| **c18** Jesus with the people | 75.44-81.48 (2263-2444) | **Quiet.** 5 teal drops already hanging in the top sky when the picture opens, scattered, NOT in an arc: (140,260) (330,470) (620,180) (850,420) (960,150). Bob only. Nothing below y 560. | HARD (quiet) |
| **c19** empty tomb + hold | 81.48-87.83 (2444-2635) | **f2444-~2500 "He died for our sins": nothing moves.** **~f2505 "rose":** 5 tomb flowers grow slowly along the bottom (x 150, 330, 520, 760, 930, y 1700-1880), 6 frames apart, no bounce. **~f2512 "the third day":** white dot rays from the sunrise (~600,840), 7 rays, upward, off the olive branch. **Nothing new after f2545.** Flowers sway a little. No fade. Nothing in or near the doorway (x 480-840, y 1150-1650). | end |

Count: 16 shots with doodles (4 of them quiet: c10, c15, c18, c19), 3 plain. 2 word beats. 4 special transitions, 14 hard cuts.

---

## 4. The 4 special transitions

None of them needs extra footage we do not have. Clip tails were checked against `_work/build_report.json`.

| # | Cut | What you see | Why (story) | Footage need |
|---|---|---|---|---|
| **T1 Well iris** | c07 -> c08, f801-813 | A circle opens from the well mouth under His hand (~940,1590) and shows the view down the well. Edge = one black ring 14 px + one teal ring 10 px. The 3 empty drops are swallowed. | He points at the well. We go in. | c07 plays 12 frames past its slot (it has 33 spare). |
| **T2 Burst fill** | c08 -> c09, f969-989 | The art's own colour disc in the water grows (a vector copy: 16 flat ray wedges, black rim) from r 225 to full frame, f969-981. At the cut the frame is all colour. Then the wedges fold open like a pinwheel in 8 frames (`rayMask` from SecondFireV1) and her face is there, inside the same colours. | "Life from God inside you." The water fills the frame, and she is in it. | None. |
| **T3 Drop iris** | c17 -> c18, f2263-2275 | The teal drop above the jar grows. The drop SHAPE is the window: inside it is Jesus with the people. 12 frames. Edge = a plain 12 px black line, nothing else. | "...found better water: Jesus." The better water is Him. | c17 plays 12 frames past its slot (it has 45 spare). c18 needs none. |
| **T4 Question pop** | c01 -> c02, f126-138 | The `WHY?` star swells to fill the frame flat yellow (6 frames). On the cut the yellow breaks into halftone dots that shrink away (6 frames). The last dots line up with the "noon" dot rays. | The question throws us into the story. | None. **First one to drop if it feels like too much.** |

Reuse: transition scaffold `TR / trP / shotStart / shotEnd`, `irisR`, `rayWedges`, `rayMask` from `_remotion/src/SecondFireV1.tsx`;
layer set-up `Shots / Clip / Beat` from `_remotion/src/MaryMarthaV4.tsx`. Doodles are children of their own shot's layer, so the masks cut them with their picture.

---

## 5. The signature moments, frame by frame

### Moment 1 - The hook (c01 into c02, f0-138)
- **f0:** three white drops are already in the air above the well. Motion on the very first frame.
- **f8 / f20 / f32:** each lands in the well mouth. Small white splash crown, 3 lobes, pops and is gone in 10 frames.
- **~f80 "her jar":** five thick black-and-white ticks pop in a fan over the jar mouth. The eye goes to the jar.
- **~f108 "Why?":** yellow burst star slams in over the sky. `WHY?` in black. It rocks 2 degrees once and stops.
- **f126-132:** the star swells and floods the frame yellow.
- **f132-138:** hard cut under the yellow. Yellow breaks into dots. Dots shrink. She is walking. "About noon."

### Moment 2 - The spring (end of c07 to start of c09, f730-1125). The showpiece.
- **f730-746 (c07):** three white drops fall into the sky beside Him. "This water."
- **f770-784:** each one empties. Three hollow outlines. "Thirst again."
- **f801-813:** T1. The circle opens from the well mouth. We are looking down the well. The hollow drops are gone.
- **~f845 "different water":** two black ripple rings leave the colour disc (centre ~540,1050, r ~225) and widen to r 420 and r 520. The art draws the same rings itself late in this clip, so they belong.
- **~f892 "a gift from God":** the first 3 teal drops jump out of the disc **toward the viewer**: they start tiny at the centre and grow as they fly out to (540,430) (150,790) (930,790). Pointed end faces the centre.
- **~f935 "Drink it":** 5 more, one every 5 frames, until 8 teal drops sit in a ring on the stones (r ~560). A fountain seen from above. They bob. Keep the disc itself clean.
- **f969-981:** T2. The disc grows and swallows drops, stones and frame. All colour on "never thirst".
- **f981-989:** the colour folds open. Her face.
- **~f1010 on:** teal drops rise up the right edge and settle over her head line, far from her face. On "never runs dry" three more are still rising when we cut. First time in the film a drop goes UP and stays.

### Moment 3 - The drop iris (c17 into c18, f2140-2275)
- **~f2140 "The jar stayed":** the five jar ticks, for the third and last time. Same jar, same ticks as the hook.
- **~f2190 "She came for water":** one hollow drop pops above the jar. Still empty.
- **~f2238 "better water":** it fills with teal, bottom to top.
- **f2263-2275:** the drop grows until its shape is the whole frame. Inside it: Jesus, sitting with the people.
- **~f2280 "Jesus":** the picture is fully open before His name is said. Five teal drops hang quietly in the sky. Nothing else moves in our layer.

### Moment 4 - The held silence (c12 + c13, f1463-1653)
- **f1463:** hard cut to His face. The layer is empty. "I that speak unto thee am he."
- **f1568:** hard cut to her tears. Still empty. "He is the Christ."
- **f1623-1653:** the 1 s silence. Nothing. 6.3 s with no doodle at all, right after the loudest part. That is the point.

### Moment 5 - The tomb (c19, f2444-2635)
- **f2444-2500:** our layer does nothing under "He died for our sins".
- **~f2505 "rose":** five small outline flowers, the same flower the art already has at the tomb, grow along the bottom. Slow.
- **~f2512-2540:** white dot rays walk out from the sunrise.
- **f2545-2635:** nothing new. Flowers sway. Dots crawl. Last frame holds as it is.

---

## 6. What I leave plain, and why

- **c03 (Jesus tired), c12 ("am he"), c13 (her tears):** no doodle at all. Reverence. And in c03 the art's sun sits right above His head: anything added there turns into a halo.
- **No drop ever touches a tear, a face, a hand, the jar itself, or the tomb door.**
- **No count of "five husbands".** Putting five marks over her would shame her and would add a meaning the Bible does not state.
- **No drops at the tomb.** The spring picture ends with Jesus among the people. The tomb only gets the art's own flowers and sun.
- **No "shall never thirst" on screen.** The phrase lands right on the c08/c09 cut, and c09 is all face: there is no clean place for it.
- **14 of 18 cuts stay hard,** including into His face, into her tears, into "Come, see a man" (now somber), and into the tomb.
- **No red or orange doodles, no speed-line swipes, no caption pills, no arrows, no lines joining people.**

## 7. Top 3 risks of looking sloppy

**R1. Doodles land on a face, a hand or Jesus, or float off their anchor.** Positions are from one small frame; c17 pans; c13/c18 are being re-made.
*How the design avoids it:* doodles live in sky and edge lanes only. Before any render, export first / middle / last frame of every shot with the doodles AND the keep-out boxes in red; zero overlap allowed. Track the jar in c17 and the disc in c08 with a 2-point move (`CAM / camAt` in SecondFireV1). Zoom 2x on every frame with Jesus.

**R2. It reads as stickers pasted on, or as a diagram (the Zacchaeus and Mary-Martha-v1 mistake).**
*How the design avoids it:* one shape family, one outline weight, four colours taken from the clips, no fades, no wobble. The two riskiest marks are the **crack in c06** and the **empty drop over His palm in c04**. Fallbacks, in order: move the c04 drop up into the sky at (560,380); drop the crack and keep only the hop. Build ONE 20 s test first (f683-1125, c07 to c09) with a `DENSITY` knob (as SecondFireV1) and show it at 1.0 and 0.6 side by side.

**R3. Timing and tone slip: beats miss their words, or the ending gets loud.**
*How the design avoids it:* every "~" frame is snapped to a real aligned word before build. Back-ease pops stop after c09; from c10 on, everything wells up slowly. Nothing new appears in the last 3 s. Transition edges are plain lines (the T3 edge crosses His face for about 1 frame: check it at 2x; if it bothers, start the drop 150 px lower). Finish with `check_landing_hold.py`.

One more check: if burned captions are added later, they will fight `WHY?` and the Saviour box. Pick one or the other for those two beats.

## 8. New parts to build (small)

`Drop` (3 states + fill/empty move), `JarTicks`, `BurstStar`, `Caption`, `Crack`, `Puff`, `DiscGrow`, `DropIris`.
Reused as they are: `pop`, `sway`, `lerp`, `Ripple`, `Crown` (splash), `Rays` (dot rays), `Flight / sPath / posOn` (rising drops), `Daisy` (re-skinned as the tomb flower).
