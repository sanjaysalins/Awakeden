# Comic motion design: "Jesus Promised Paradise to a Criminal" (38 s short)

Design only. $0. Nothing built into the film yet. Replaces the storybook doodle (walking figure in the hold). That doodle is dropped.

Preview: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\design\comic\comic_mock.html`
(`file:///F:/slk/PycharmProjects/JesusInTheBible/poc_comic_page/_ELEVATE/formula/design/comic/comic_mock.html`)

The mock was checked by maths and by flat PIL composites of the key states. It was NOT watched in a browser (house rule: never open one). The motion feel is unverified until the owner looks.

## The idea in one line

Loud comic language for the two thieves. Total stillness for Jesus. Then light breaks the ink on "Today."

6 moves. 5 are drawn. 1 is the planned absence of drawing.

## Ground rules used for every move

| Item | Value |
|---|---|
| Frame | 1080 x 1920, 30 fps. Frame number for a word = `ceil(word_start * 30)`, so a move is never early. |
| Ink | `#14100C` (20,16,12). Same as `T.INK` family and `impact_burst.INK`. |
| Bone (light line on dark sky) | `#F3E9D2` |
| Page paper | `#FAF0D6` (250,240,214), the Jesus pill ivory already in `build_w3.pill_tabs` |
| Line weight | 8-9 px borders and outlines, 5-6 px small marks. Matches the art's heavy outline. Square or mitred joins. No gradients, no glow, no soft shadows. |
| Line edge | Run every drawn edge through a +/-2 px noise wobble (reuse `panel_animator/grid_choreography._wobbled_rect` idea) so it is brush, not vector. |
| English pill zone (keep clear) | x 70-1010, y 974-1250 (tabs start at y 974) |
| Platform zones (nothing that matters) | top y < 200, bottom y > 1500, right rail x > 930 for y 900-1500 |
| Audio | Copy the audio stream of `today_paradise_short32_final.mp4` as is (`-c:a copy`). |
| Hold | 35.0-38.0 s is untouched. No move after 29.40 s. |

Per-frame push-in maths for anything stuck to the picture (from the earlier finding, `to_screen()` uses the mean zoom and is not enough):
`z = z0 + (z1 - z0) * i / n`, `vx = clamp(cx - 0.5/z, 0, 1 - 1/z)`, same for `vy`, `screen = ((ax - vx) * z * 1080, (ay - vy) * z * 1920)`. Then add the tracked offset of the clip's own motion.

## Beat table

### 1. Page slam, then dive. 0.00-3.75 s

| | |
|---|---|
| Words | "Jesus" 0.06, "a" 1.77, "criminal." 1.85-2.21, "Why?" 3.38 |
| Shots | Replaces shots 1-2 for this window. Clips: `jesus_turns_to_thief`, `mocker_thief_face`, `penitent_thief_face` (all t_in 0.0, running live inside the panels). |
| Page | Full frame `#FAF0D6` with ink dots (2 px dot, 20 px pitch, 13 percent). |
| Panel J (Jesus) | x 60-1020, y 470-940, tilt -1 deg. Letterbox close-up of His eyes: clip scaled 0.90, placed at (54, -304). Border only. Nothing is drawn on the picture. |
| Panel M (mocker) | x 555-1020, y 1290-1640, tilt +2 deg. Clip scaled 0.50 at (533, 979). |
| Panel T (thief who asks) | x 60-525, y 1290-1640, tilt -2 deg. Clip scaled 0.50 at (52, 945). |
| Panel style | 9 px ink border, hard ink drop shadow offset (12, 12). No blur. |
| Slams | J at frame 2 ("Jesus"). M at frame 54 ("a"). T at frame 56 ("criminal"). Each: scale 1.30 at frame 0, 0.97 at +3, 1.00 at +5. Page shake 8 px for 4 frames on J and on T. |
| Dive | Frames 71-83 (2.37-2.77 s), after "criminal." ends. Panel T's border grows to the full frame, tilt goes to 0, border goes to 0. Ease-out (cubic-bezier .3,.8,.2,1). |
| Landing frame | From frame 83 to the cut at 3.752 s the picture must equal the shipped film: `penitent_thief_face`, clip time `t - 1.9`, shipped zoom `1.3 + 0.2 * (t - 1.9) / 1.852` about (.42, .42). So "Why?" lands on the same full-bleed face as today. The panel view is that same view, scaled into the panel. (The mock ends on the plain full frame, a simplification.) |
| Lettering | Hook card "PARADISE FOR A CRIMINAL?" moves from y 420 to y 200 (above panel J), same art, same 0.0-2.2 s. The pill stays where it is and sits in the page gutter like a caption box. |
| Reuse | Slam curve and shake: `/livingpage` grammar (v2/LIVINGPAGE_STANDARD.md). Panel clips: `build_tp.render_shot`. Grid look: the Barabbas 3-panel pages. |
| New code | `page_slam()` in a new `build_s32_comic.py`: per-frame PIL composite of 3 clip crops into wobbled boxes. About 60 lines. |
| Why | The hook names two people: Jesus and a criminal. The page shows them as panels. There are two criminals, so "Why?" becomes "why this one?" and the camera answers by diving into him. |
| Bonus | Today the pill sits on Jesus' eyes in shot 1. Here His eyes are clear above it. |

### 2. The shout. 6.95-10.87 s

| | |
|---|---|
| Words | "Christ," 7.74, "save" 8.77, "thyself" 9.07, "us." 10.45 |
| Shot | Shot 5, `mocker_taunts_jesus`, unchanged. |
| A. Spiky pill edge | A jagged ink outline round the existing pill, on from 6.95 to 10.87 s. Spikes point out 26-60 px, one every 47 px. Two layers: bone 18 px under, ink 8 px on top (ink alone is lost on the dark sky). On the top edge the outline rides above the two tabs (y 960) and makes no spike into them. Two spike sets swap every 3 frames (boil on threes). Pill fill and text untouched. |
| B. Shout marks | 6 wedges fanned from his mouth, angles -72 to -4 deg (up and right). Inner radius 84 px, outer 210 / 300 px alternating. Bone fill, 6 px ink outline. Mouth is at screen (512, 680) at 8.0 s. |
| Pops | Frames 233, 264, 273, 314. Each pop: scale 0.4 at frame 0, 1.08 at +2, 1.0 at +4, gone at +8. The "thyself" pop is 15 percent bigger. A 6-8 px picture jolt for 4 frames on "save" only. |
| Where it is not | Fan stays inside x 520-830, y 380-700. Jesus' small figure in this shot is at x 826-1070, y 940-1810. Nothing points at Him or touches Him. |
| Tracking | Mouth anchor: template-match a 64 px patch (mouth + fist) every frame in the source clip (OpenCV `matchTemplate`, $0), then the per-frame push maths. Gate: wedge root within 6 px of the mouth on 5 sampled frames. |
| Reuse | `BA.jagged_balloon` outline maths for the spikes. `panel_animator/impact_burst.draw_burst` for the wedges (add a `fan=(a0, a1)` argument in a copy, do not fork a second burst engine). |
| Why | He is the only one who shouts. The spiky edge is how comics draw a shout. It needs no reading. |

### 3. The ink split. 10.87-14.94 s

| | |
|---|---|
| Words | "One" 11.02 ... "cross." 12.24, "The other" 13.00, "asked" 13.51 |
| Shots | Shots 6-7. Same clips, same order. The hard cut at 12.60 s becomes the split. |
| 10.87-12.60 | Mocker full-bleed as shipped. |
| Slash | Frames 378-383. One ink brush stroke, 84 px wide, drawn top to bottom from (762, 0) to (318, 1920). Then it opens into the gutter. 4 small ink flecks (5-9 px) stay beside it. |
| Gutter | 26 px of page paper between two 9 px ink edges. Line from (760, 0) to (320, 1920). About 13 deg off vertical. |
| Left panel | Mocker, `mocker_thief_face` keeps playing (t_in continues). Scale 1.0, shifted x -247. |
| Right panel | Thief who asks, `penitent_thief_face` t_in 1.0. Scale 1.20, at (270, -175). Slides in 56 px from the right during the slash. |
| Turn | Frames 406-414 ("asked"). The gutter slides 150 px left, ease-out. Mocker panel dims to 55 percent brightness, 35 percent colour. Thief panel +8 percent brightness. Mocker picture x -322, thief picture x 195. |
| Pill | Unchanged, on top. The gutter passes behind it. Both faces sit above or beside it. |
| Not left-to-right | The order comes from time (one man, then the slash, then the other). The slash runs top to bottom. Mirrored, it reads the same. |
| Reuse | Dim / brighten = `grid_choreography.activeness()` weights. Wobbled edges = `_wobbled_rect` idea. `build_tp.render_split` shows the two-clip crop pattern (it is a flat horizontal stack, so the polygon mask is new). |
| New code | `diag_split()`: two `render_shot` crops + a polygon mask per frame. About 50 lines. |
| Why | "One ... the other." Two men, same place, two answers. The ink cuts them apart. The one who "asked for very little" is given more of the page. |
| Known wart | The mocker's face is big in a narrow panel (eye and mouth only). That is tight but reads as a shout. |

### 4. The hush. 14.94-18.70 s

| | |
|---|---|
| Words | "Lord," 15.08, "remember" 15.71, "kingdom." 18.18-18.58 |
| Shot | Shot 8, `confession_face_hands`, unchanged. |
| Move | Ink halftone dots close in from the edges. Offset grid: 30 px across, 15 px down. Dot radius = `min(10.5, (d - 1) * 9)` px where `d` is the distance from (600, 1240) in an ellipse of 470 x 560. So zero dots round his bowed head, biggest in the corners. Ink `#14100C` at 72 percent. |
| Timing | Fades in over frames 453-473 (from "Lord"). Holds. Dots above y 700 fade out over frames 546-561 (on "kingdom") so the top opens just before the cut to the light. |
| Rules | No slam, no shake, no border. No dots inside the pill box (x 50-1030, y 955-1205). |
| Tracking | Not needed. The edge is soft and wide. Use the push maths only for the centre. |
| Reuse | None fits (print-grade is a whole-frame grade). New `halftone_vignette()`, about 25 lines of PIL. |
| Why | After the shout, the page goes quiet. Halftone is the comic way to say "soft". It also sets up move 5: quiet, then nothing at all. |

### 5. Jesus speaks. Nothing moves. 22.45-26.53 s

| | |
|---|---|
| Words | "To day shalt thou be with me in paradise." 22.53-26.25 |
| Shot | Shot 10, `jesus_turns_to_thief`, unchanged. |
| Move | None. No border, no lines, no dots, no shake. The last comic mark is gone by 18.70 s. The next starts at 27.70 s. |
| Gate | Frames 673-796 of the new film must match the shipped film (mean absolute pixel difference under 1.0 per frame). A machine check, fail-closed. |
| Why | `/livingpage` sacred stillness. Every other voice gets ink. His does not need it. The contrast is the move. |

### 6. Today. 26.53-29.40 s

| | |
|---|---|
| Words | "Not someday." 26.63-27.45, silence, "Today." 28.14-28.62 |
| Shots | Shot 11 `answer_light_profile` as shipped until 27.70 s. Then a 1.7 s look ahead at the garden: `paradise_dawn`, t_in 3.25, cx .5, cy .38, z 1.30 to 1.34. Hard cut at 29.40 s to shot 12 as shipped. |
| Ink bleed | Frames 831-844, inside the silence before "Today." The garden bleeds in from the light gap in the clouds, origin (0.72, 0.12), top right, away from His face. Blot mode. An ink rim leads the edge by about 3 percent of the field. |
| Sun lines | Land on frame 845 ("Today."). 17 ink wedges round the sun at screen (606, 740). Inner radius 250-290 px, outer 600 / 900 px alternating, 18-30 px wide at the far end, pointed at the near end. Angles 158 to 382 deg: none point down. Clipped at y 940, above the pill. |
| Motion | Scale 1.30 at frame 845, 0.98 at 847, 1.00 at 848. Two wedge sets swap every 3 frames until 859 (end of the word). Frames 859-867: lines fly out to scale 1.6 and fade. |
| His figure | In the garden He is a small far figure (about 80 x 230 px, centre (554, 697)). The furthest point of the figure is 171 px from the sun. The 250 px clear ring means no line touches Him. |
| Tracking | The sun is picture-anchored. Track the two inner cypress feet (same two points as the earlier finding) for move + scale, then the push maths. Gate: ray centre within 6 px of the sun on 5 frames. |
| Reuse | `panel_animator/ink_transition.make_reveal_field(mode="blot", origin, w=1080, h=1920)` + `render_mask_frames` + `maskedmerge`. `render()` already takes `w`, `h`. Rays: `impact_burst.draw_burst` wedge maths. |
| New code | The ink rim (a second threshold on the same field, about 10 lines). `sun_rays()` about 30 lines. |
| Why | He asked for someday. The answer is today. So the promised place does not wait for the end of the film: it breaks through the dark on the word. |
| Honest risk | This shows the garden twice (here, tighter and later in the clip, and in the 3 s hold). It may soften the ending. If the owner feels that, drop move 6 whole. Do not move the lines onto the profile shot: that is a crucifixion close-up. |

## What stays as shipped

3.75-6.95 s, 18.70-27.70 s, 29.40-38.00 s. All pills, tabs, verse chips, audio, the 3.0 s hold.

## Changes the owner should know about

1. The hook card moves up (y 420 to y 200). Same words.
2. Shots 1-2 become a page for 2.4 s, then the same full-bleed thief face as today.
3. A 1.7 s look ahead at the garden at 27.70 s (move 6).

## Gates before calling it built

- Word sync: every move frame = `ceil(word_start * 30)` from `today_paradise_short32_final.words.json`.
- Stillness gate (move 5) and landing-frame gate (move 1, frames 83-112).
- Tracking gates (moves 2 and 6).
- No-draw gate: a mask of Jesus' face per shot. Overlay alpha inside it must be 0 on every frame.
- `check_landing_hold.py` still 0 FAIL. Audio stream hash equal to the shipped film.
- Eye check at full zoom on 2 frames per move. Then a blind panel (Fable seat + AI seats) on the film only, before any upload.

## Honest odds (my guess, not data)

- Owner reads it as "graphic comic, not storybook": about 75 percent (+/- 15).
- Move 6 kept as is after a real watch: about 55 percent (+/- 20). It is the boldest call.
- Simulated viewers are not real. Test with 3 real people, sound off.

## Rejected

| Idea | Why not |
|---|---|
| Sun lines on the "Today." profile shot | Crucifixion close-up. Lines by His head sit in the no-draw zone. |
| Sun lines when Jesus says "To day" (22.53 s) | Breaks sacred stillness, and it is His face. |
| Onomatopoeia ("CRACK", "BAM") | Needs reading. English only. |
| Tail from the pill to the mocker's mouth | His mouth moves in the clip, and the pill is full width: the tail reads as a pointer, not a balloon. The fan does the job. |
| Left and right flat split for the two thieves | Reads as left-to-right order. The steep diagonal plus time order avoids that. The old `SPLITS` arm (flat top and bottom, gold bar) also put the lower face in the caption zone. |
| Speed lines behind the mocker's whole body | Ink lines vanish on the dark sky. Bone lines that big look like a template effect. |
| Panel border or red-letter bar round Jesus when He speaks | Any frame is still an effect. Nothing is stronger. |
| Halftone on the garden or on the hold | The landing stays clean. |
| Line-boil on the whole film | It wobbles His face. Only the drawn marks boil. |
| The walking-figure doodle in the hold | Judged too storybook. Dropped. |
| A 7th move on "With Him" (29.4-32 s) | That shot is the risen Jesus' face. No-draw. |
