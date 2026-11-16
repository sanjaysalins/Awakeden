# Full comic motion: the kit + "Jesus Promised Paradise to a Criminal" (38 s)

Design only. $0. Nothing is built into the film yet. Third pass. It replaces the sparse 6-move design
(`F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\design\comic\COMIC_MOTION_DESIGN.md`).
The owner asked for full comic motion from start to finish. The old "5-6 moves" limit is gone.

Storyboard: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\design\comic_full\comic_full_mock.html`
(`file:///F:/slk/PycharmProjects/JesusInTheBible/poc_comic_page/_ELEVATE/formula/design/comic_full/comic_full_mock.html`)

The mock was checked by maths, by a CSS name/brace check, and by flat PIL composites of 12 key states.
It was NOT watched in a browser (house rule). The motion feel is unverified until the owner looks.

## The idea in one line

The whole film is one moving comic book. Loud ink for the two thieves. One clean, still splash page for Jesus. Then the page breaks open on "Today."

Numbers: 41 kit devices. In this film: 16 cut transitions (15 drawn + 1 deliberate hard cut), 3 page moves, about 24 doodle events. No transition is used twice in a row.

---

## 1. The kit (reusable for every episode)

Every device is one function (Python) or one component (Remotion) with the same name and the same parameters.
All times are frames at 30 fps. `at` = the frame the device starts. Frame of a word = `ceil(word_start * 30)`.

### Shared values

| Item | Value |
|---|---|
| Frame | 1080 x 1920, 30 fps |
| Ink / bone / paper | `#14100C` / `#F3E9D2` / `#FAF0D6` |
| Line weight | 9 px borders and outlines, 5-6 px small marks, 84 px for a brush slash. Mitred joins. No blur, no glow, no gradient. |
| Two-tone rule | A mark must read on any picture. Dark picture: bone fill + 6 px ink outline. Light picture: ink fill + 5 px bone outline. Lines: 18 px bone under, 8 px ink on top. |
| Pill zone (keep clear) | x 70-1010, y 974-1250 |
| Platform zones (nothing that matters) | y < 200, y > 1500, x > 930 for y 900-1500 |
| Easing | "slam" = scale 1.30, then 0.97 at +3, then 1.00 at +5. "glide" = cubic-bezier(.6,0,.3,1). "settle" = cubic-bezier(.3,.8,.2,1). |

### A. Core (4)

| Device | Parameters | What it does |
|---|---|---|
| `ink_stroke` | `pts, width, seed, tone="ink"|"bone"|"two"`, `draw=(at, frames)` | The only way a line is drawn. Polyline with +/-2 px seeded wobble along its length, square caps. `draw` makes it draw on from first point to last. |
| `boil` | `sets=2, hold=3` | Any held mark is drawn twice with two seeds. The two versions swap every 3 frames. Only marks boil. Pictures never do. |
| `anchor` | `clip, patch_xy, patch=64` then `to_screen(ax, ay, shot, i)` | Sticks a mark to the picture. OpenCV `matchTemplate` per source frame, then the per-frame push maths: `z = z0 + (z1 - z0) * i / n`, `vx = clamp(cx - 0.5/z, 0, 1 - 1/z)`, same for `vy`, `screen = ((ax - vx) * z * 1080, (ay - vy) * z * 1920)`. Gate: within 6 px on 5 sampled frames. |
| `guard` | `no_draw_masks, zones` | Fail-closed check on every frame: overlay alpha is 0 inside each Jesus-face mask and each crucifixion close-up mask. Warns if a mark's centre sits in the pill zone or a platform zone. |

### B. Layouts (4)

| Device | Parameters | Look |
|---|---|---|
| `page` | `panels=[...], dots=True` | Full frame of paper `#FAF0D6` with ink dots (2 px dot, 20 px pitch, 13 percent). Holds panels. |
| `panel` | `clip, t_in, box, tilt, scale, offset, shadow=(12,12)` | A live clip cropped into a box. 9 px wobbled ink border. Hard ink drop shadow, no blur. Tilt -3 to +3 degrees. |
| `inset_panel` | same as `panel`, `over=shot` | A small panel on top of a full-bleed shot. Never over Jesus' face. |
| `splash_border` | `inset=22, width=10` | One static ink border at the frame edge of a full-bleed shot. It does not animate. The comic word for this is a splash page. |

### C. Cut transitions (16)

`A` = outgoing picture, `B` = incoming. Default length in frames in brackets.

| # | Device | Parameters | Look | Energy |
|---|---|---|---|---|
| T1 | `panel_slam` | `panel, at, shake=8` (5) | Panel pops on: slam easing. Page shakes 8 px for 4 frames. | loud |
| T2 | `panel_dive` | `panel, at, frames=12` | Camera dives through a panel border. Border grows to full frame, tilt to 0, border to 0. Ends on the plain full-bleed shot. | loud |
| T3 | `whip_pan` | `dir="up"|"down", frames=4` | A slides off, B slides in, with 10 vertical bone streaks for 3 frames. Vertical only. | fast |
| T4 | `page_glide` | `from_panel, to_panel, frames=10` | Both shots are panels on one tall page. The camera glides down (or up) across the gutter. | medium |
| T5 | `slam_cut` | `tilt=3, frames=6` | B arrives as a tilted full-frame panel at scale 1.25 and snaps flat. | loud |
| T6 | `speed_zoom` | `center, frames=5` | A zooms to 1.9 about a point. 30 radial bone speed lines flash. B lands from 1.18 to 1.0. | loud |
| T7 | `ink_slash_split` | `p0, p1, width=84, gutter=26, frames=6` | One brush stroke is drawn top to bottom. It opens into a paper gutter. A stays on one side, B slides in on the other. | sharp |
| T8 | `halftone_dissolve` | `mode="radial"|"rise", center, frames=12` | B appears through growing dots. `radial` opens from a centre. `rise` climbs from the bottom with a 240 px band of dots on its edge. | soft |
| T9 | `page_flip_up` | `frames=10` | A is a page hinged at the top. It lifts up and away (it darkens as it tips). B is under it. | medium |
| T10 | `pull_out_to_page` | `box, frames=10` | The reverse of the dive. Full-bleed A shrinks into a small panel on a paper page. | medium |
| T11 | `border_fall` | `frames=10` | The whole page (paper, panels, borders) drops out of the bottom of the frame with a 5 degree tip. B is clean underneath. | release |
| T12 | `punch_cut` | none | A plain hard cut. Allowed once or twice a film, on purpose. | punch |
| T13 | `panel_shatter` | `panel, shards=6, at, frames=12` | `crack_lines` first. Then the panel breaks into 6 pieces along the cracks. They fall and turn. Shatters a frozen frame, not a live clip. | loud |
| T14 | `ink_bleed` | `origin, frames=13, rim=True` | B blots in from a point with a ragged edge and a thin ink rim leading it. Reuses `panel_animator/ink_transition.make_reveal_field(mode="blot")`. | medium |
| T15 | `iris` | `center, frames=10, open=True` | An ink ring opens (or closes) from a point. B is inside the ring. | medium |
| T16 | `gutter_wipe` | `dir="down"|"up", band=64, frames=10` | A bar of paper with two ink edges sweeps down the frame. B is behind it. Vertical only. | calm |

### D. Page moves (3)

| Device | Parameters | Look |
|---|---|---|
| `gutter_shift` | `dx, frames=8` | The gutter of a split slides. One panel gets more of the page. |
| `panel_join` | `panel, to_box, frames=8` | A small panel hops in an arc and lands overlapping another panel's corner. Two panels become one group. |
| `page_settle` | `scale=0.93, tilt=-0.7, frames=12` | The full-bleed picture eases back into a panel on paper and stops. For the last second of a film. |

### E. Doodles (14)

| # | Device | Parameters | Look | Use for |
|---|---|---|---|---|
| D1 | `ink_splat` | `xy, r=20, seed` | One blot + 9 flecks. Static after it lands. | every slam |
| D2 | `page_dots` | `rect, pitch=20, r=2` | Ben-Day dots on paper. | every page |
| D3 | `shock_lines` | `center, r0, r1, arc=(a0,a1), n=8, hold` | A crown of short wedges round a head. Pops with slam easing, boils, flies out. | surprise, a question |
| D4 | `border_build` | `box, at, frames_per_side=8` | An ink frame draws itself, one side at a time. | "look here", counting, the close |
| D5 | `pill_edge` | `style="spiky"|"dashed", t0, t1` | An outline round the existing pill. Spiky = shout (26-60 px spikes every 47 px, boils). Dashed = whisper (34 px dash, 24 px gap, still). Pill fill and words untouched. | who is loud, who is quiet |
| D6 | `shout_fan` | `mouth, arc=(a0,a1), n=6, pops=[frames]` | Wedges from a mouth: inner 84 px, outer 210 / 300 px. Pops on chosen words. | a shout |
| D7 | `speed_lines` | `mode="radial"|"focus"|"parallel", center, r0, arc, n` | Long thin wedges. `radial` = full circle (inside `speed_zoom`). `focus` = from the frame edge toward a subject. `parallel` = one direction. Boil on threes. | force, attention |
| D8 | `drops` | `anchor, n=3, dir, kind="sweat"|"tear", frames=24` | Teardrop shapes, 20-34 px, two-tone. They drift 80-110 px and go. | strain, grief |
| D9 | `motion_ticks` | `anchor, dir, n=3, len=110, frames=14` | Groups of 3 short strokes that slide the way the body moves. | a pull, a turn, a reach |
| D10 | `jolt` | `amp=8, frames=4` | The picture kicks 6-8 px. | one hit per shot at most |
| D11 | `crosshatch_shade` | `region, pitch=46, opacity=.75, frames=10` | Diagonal ink hatching fades over a panel. | someone fades out of the story |
| D12 | `halftone_vignette` | `center, rx, ry, rmax=10.5` | Dots close in from the edges, none in the middle, none in the pill. | a hush |
| D13 | `rays` | `mode="soft"|"burst", center, clear_r, arc, n` | `soft` = 5-6 thin lines, no slam. `burst` = 17 wedges, slam in, boil, fly out. Always a clear ring round the centre. | light, the big word |
| D14 | `crack_lines` | `panel, n=3, frames=4` | 3 jagged ink lines draw across a panel. Feeds `panel_shatter`. | "not that" |

### Binding rules for every device

- Nothing is drawn on Jesus' face or on a crucifixion close-up. A border round the picture is fine. A mark on it is not.
- Nothing to read. No sound words, glyphs, arrows, question marks. Nothing that only works left to right: all wipes, glides and whips run up or down, or from a point.
- The pill and its tabs are always the top layer. Everything else passes behind them.
- Audio is never touched: copy the stream of the shipped film (`-c:a copy`).

---

## 2. Beat sheet: the Thief film

Real word times from `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\today_paradise_short32\visual\today_paradise_short32_final.words.json`.
Shot table and zooms from `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\build_s32.py` (`SH`). `f` = frame.
Clips are in `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\today_paradise_luke2343\visual\clips`.
Mock card numbers are in the first column.

| Card | Time (f) | Words | Shot / clip | Device + parameters | Why |
|---|---|---|---|---|---|
| 1 | 0.00 (f0) | | Page 1 | `page(dots)`. Hook card moves to y 200. | The film opens as a comic page. |
| 1 | 0.07 (f2) | "Jesus" | Panel J: `jesus_turns_to_thief` t_in 0.0, box x 60-1020, y 470-940, tilt -1, letterbox on His eyes | `panel_slam(shake=8)` + `ink_splat((1010,950))` in the gutter | Border only. Nothing on His picture. |
| 1 | 1.80 (f54) | "a" | Panel M: `mocker_thief_face`, box x 555-1020, y 1290-1640, tilt +2 | `panel_slam(shake=0)` + `ink_splat((1030,1280))` | Two criminals: two panels. |
| 1 | 1.87 (f56) | "criminal." | Panel T: `penitent_thief_face` t_in 0.0, box x 60-525, y 1290-1640, tilt -2 | `panel_slam(shake=8)` + `ink_splat((70,1650))` | |
| 2 | 2.37 (f71-83) | (pause) | Panel T to full bleed. Ends on shipped view: zoom `1.3 + 0.2 * (t - 1.9) / 1.852` about (.42,.42) | `panel_dive(T, frames=12)` | "Why this one?" The camera answers. |
| 2 | 3.40 (f102-112) | "Why?" | `penitent_thief_face` | `shock_lines(center=head (510,800), r0=450, r1=560/640, arc=(200,340), n=8)`, ink fill + bone edge, pop f102, boil, fly out by f112. `anchor` on his head. | The comic mark for a question, with no glyph. |
| 3 | 3.75 (f113-117) | | to Page 2, panel A: `two_thieves_wide` t_in 0.0, box x 40-1040, y 60-1860 | `whip_pan(dir="up", frames=4)` | Fast early pace. |
| 3 | 3.87 (f116-128) | "Two" | same | `border_build(box=(60,390,270,940))` round the left thief | Counting without numbers. |
| 3 | 4.10 (f123-135) | "criminals" | same | `border_build(box=(770,400,1010,950))` round the right thief. Both boxes fade f147-152. | Neither box touches Jesus (x 400-640). `anchor` both boxes. |
| 4 | 4.93 (f148-158) | "on crosses" | to Page 2, panel B: `golgotha_hill_wide` t_in 0.0 | `page_glide(A, B, frames=10)` down across the gutter | Reading down a page. |
| 4 | 5.27-6.95 | "beside Him." | panel B | No doodle. He is the centre of this picture. Border and gutter only. | No-draw rule. |
| 5 | 6.95 (f209-214) | | `mocker_taunts_jesus` t_in 0.5, as shipped | `slam_cut(tilt=3)` + `ink_splat` x2 in the top corners (y < 200) | He bursts in. |
| 5 | 6.95-10.87 | whole line | same | `pill_edge("spiky")` | Shout, no reading. |
| 5 | f233, f264, f273, f314 | "Christ," "save" "thyself" "us." | same | `shout_fan(mouth, arc=(-88,-4), n=6, pops=[233,264,273,314])`. "thyself" pop 15 percent bigger. `anchor` on mouth + fist. | |
| 5 | 8.80 (f264-300) | "save thyself" | same | `speed_lines("focus", center=mouth, r0=420, arc=(150,270), n=9)`, bone, boil. `jolt(8)` at f264. | Arc is up and left only. Jesus' figure (x 826-1070, y 940-1810) is never crossed. |
| 5 | 10.47 (f314-338) | "us." | same | `drops(anchor=head, n=3, dir=up-left, kind="sweat")` | Strain. |
| 6 | 10.73 (f322-327) | | to `mocker_thief_face` t_in 0.0, as shipped | `speed_zoom(center=mouth, frames=5)` | We crash into his face. |
| 6 | 11.03 (f331-355) | "One wanted" | same | `drops(anchor=temple (850,640), n=3, dir=down-right)` | |
| 6 | 11.60 (f348-362) | "off" | same | `motion_ticks(anchors: 3 left of head, 3 right, dir="up", len=110)`, bone | He wants up and off. |
| 7 | 12.60 (f378-383) | | left: `mocker_thief_face` keeps playing. right: `penitent_thief_face` t_in 1.0 | `ink_slash_split(p0=(762,0), p1=(318,1920))` + 4 flecks | "One ... the other." Top-to-bottom stroke. Mirrored it reads the same. |
| 7 | 13.53 (f406-414) | "asked" | same | `gutter_shift(dx=-150)`. Mocker panel: brightness .55, colour .35, + `crosshatch_shade`. Thief panel +8 percent brightness. | The one who asked for little gets the page. |
| 7 | 14.53 (f436-448) | (after "little.") | same | `gutter_shift(dx=-700, frames=12)`: the gutter slides off. The mocker is gone. | He leaves the story here. |
| 8 | 14.97 (f449-461) | | `confession_face_hands` t_in 0.0, as shipped | `halftone_dissolve("radial", center=(600,1240))`. The edge dots stay on as `halftone_vignette(center=(600,1240), rx=470, ry=560)`. | The transition becomes the hush. |
| 8 | 15.10 (f453-561) | "Lord, remember me..." | same | `pill_edge("dashed")` | A whisper. The opposite of the spiky edge. |
| 8 | 18.20 (f546-558) | "kingdom." | same | Vignette dots above y 700 fade out. | The top opens before the sky. |
| 9 | 18.60 (f558-567) | | `kingdom_light_clouds` t_in 0.0, as shipped | `page_flip_up(frames=10)` | He looks up. The page lifts up. |
| 9 | 19.07 (f572-640) | "asked to be remembered." | same | `rays("soft", center=light gap (540,280), clear_r=230, arc=(45,135), n=6)`, bone, boil, opacity 75 percent | Hope, drawn lightly. |
| 10 | 21.57 (f648-658) | "Someday." | same clip, now a panel: box x 260-820, y 220-920 on `page(dots)` | `pull_out_to_page(box, frames=10)`. Holds small to f664. | Someday is small and far away. |
| 11 | 22.13 (f664-673) | (0.4 s pause) | `jesus_turns_to_thief` t_in 1.5, as shipped | `border_fall(frames=10)`. Under it: the shot + `splash_border(inset=22)`. | Every border falls away. |
| 11 | 22.47-26.53 (f674-796) | "To day shalt thou be with me in paradise." | same | **Nothing.** No dots, lines, shake, boil. The one static border does not move. | Change of register. The loudest thing in a loud film is stillness. |
| 12 | 26.53 (f796) | | Page 3: the same "someday" panel (same box, same crop, frozen frame) | `punch_cut` | The one hard cut. It ends the stillness. |
| 12 | 26.63 (f799-803) | "Not" | same | `crack_lines(panel, n=3)` | |
| 12 | 26.97 (f809-821) | "someday." | same | `panel_shatter(shards=6)`. An empty paper panel with its border stays. | Someday breaks. |
| 12 | 27.37-27.70 (f821-831) | (silence) | empty panel | Nothing. | An empty frame, waiting. |
| 13 | 27.70 (f831-844) | (silence) | `paradise_dawn` t_in 3.25, cx .5, cy .38, z 1.30 to 1.34, full bleed | `ink_bleed(origin=(540,570), rim=True)` out of the empty panel | The promised place fills the empty frame. |
| 13 | 28.17 (f845-867) | "Today." | same | `rays("burst", center=sun (606,740), clear_r=270, arc=(158,382), n=17)`. Slam f845, boil to f859, fly out f859-867. Clipped at y 940. | His far figure (80 x 230 px at (554,697)) sits inside the clear ring. No line touches Him. |
| 14 | 29.40 (f882-892) | | Page 4. Panel J: `risen_mercy_hand` t_in 0.0, box x 60-1020, y 210-940, scale 1.05, face centred. Panel T: `thief_looks_to_jesus` (new clip), 300 x 280 at (60,1290), crop on his head. | `iris(center=(606,740), frames=10)` | The ring opens from the sun onto Jesus. |
| 14 | 31.47 (f944-952) | "With Him." | same | `panel_join(T, to_box=(30,720,330,1000), tilt=-3)`. Lands on "Him." f952. | "With Him", shown: his panel joins His. It lands on His shoulder corner, 100 px clear of the beard. |
| 15 | 31.93 (f958-968) | | `us_under_cross_shadow` t_in 0.0, as shipped | `gutter_wipe(dir="down", frames=10)` | Calm. Turning to the viewer. |
| 15 | 33.07 (f992-1012) | "You" | same | `speed_lines("focus", center=(540,800), r0=520, n=8, top and sides only)`, ink fill, boil | The page points at the two who kneel: you. |
| 15 | 33.40 (f1002-1040) | "ask Him to remember you" | same | `pill_edge("dashed")` | The same whisper edge the thief had. You can ask the same way. |
| 16 | 35.00 (f1050-1064) | (hold) | `paradise_dawn` t_in 0.0, as shipped | `halftone_dissolve("rise")` | Dawn comes up. |
| 16 | 35.60 (f1068-1100) | (hold) | same | `border_build(box=(20,20,1060,1900), frames_per_side=8)` | The last panel is drawn. |
| 16 | 36.80 (f1104-1116) | (hold) | same | `page_settle(scale=.93, tilt=-.7)`. Dead still f1116-1140. | The book closes softly. 0.8 s of full stillness at the end. |

### What changes from the shipped film (owner should know)

1. The hook card moves up (y 420 to y 200). Same words.
2. Shots 3-4 (the two wide shots) become two panels on one page.
3. **`answer_light_profile` (26.53-29.40) is replaced** by the "someday" panel breaking and the garden bleeding in. Reason: that shot is a crucifixion close-up, so nothing may be drawn on it. Option B if the owner misses it: keep it clean and full-bleed for 26.53-27.70, skip cards 12, start the bleed at 27.70 as in the old design.
4. The risen Jesus shot (29.40-32.00) sits in a panel, with a new small thief panel from the unused clip `thief_looks_to_jesus`.
5. Jesus' own line gets one static border. Nothing else.
6. The 3 s hold gets a drawn border and a settle. It still ends dead still.

### Gates before calling it built

- Word sync: every word-tied frame = `ceil(word_start * 30)`. Never early.
- Stillness gate: frames 674-796, inside the splash border, match the shipped film (mean absolute difference under 2.0 per frame; 1.0 if built in Python).
- `guard`: overlay alpha 0 inside the Jesus-face masks (panel J card 1, shot 10, panel J card 14, far figure cards 13 and 16) on every frame.
- `anchor` gates: shout fan, sweat, thief boxes, shock crown, sun rays (6 px on 5 frames each).
- Variety gate: no transition device twice in a row (see section 4).
- Audio stream hash equals the shipped film. `check_landing_hold.py` 0 FAIL.
- Eye check at full zoom, 2 frames per card. Then the blind panel (Fable seat + AI seats) on the film only.

### Honest risks (my guess, not data)

- Owner reads it as "proper graphic comic": about 80 percent (+/- 15).
- Cards 12-13 (shatter, then bleed, then burst in 2.3 s) feel like too much straight after the still: about 35 percent (+/- 20). Fix if so: drop `crack_lines`, keep the rest.
- The garden is seen twice (27.70 and the hold). Same risk as last pass.
- `panel_join` lands near His hair edge. If the panel reads as "on Him", land it 60 px lower, on the border only.
- Simulated viewers are not real. Test with 3 real people, sound off.

---

## 3. Renderer: Remotion for the picture, Python before and after

**Pick: Remotion** (`F:\slk\PycharmProjects\JesusInTheBible\_remotion\`, remotion 4.0.290 already installed, 30 comps already there).

Why:
- This design is 16 transitions that tilt, scale, flip, clip and shatter **live video layers**. In CSS each is 5-15 lines (transform, `clip-path`, `perspective`). In PIL each is a 50-line per-frame compositor, and 1140 frames x up to 3 decoded clips is slow to iterate.
- The mock is already HTML/CSS/SVG. It ports almost 1:1. Draw-on strokes are `stroke-dashoffset`. Boil is `frame % 6 < 3`.
- The kit becomes typed components (`<PanelSlam at={2} .../>`). An episode is one `episode.json` (shots, events). That is the pipeline shape the Living Comic machine already uses.
- It matches the owner rule "clips first, Remotion on top".

Python keeps three jobs (all $0, all existing code):
1. **Before:** pills, tabs and hook card PNGs from `build_w3.pill_tabs` / `build_tp.light_text` (so lettering is pixel-identical); `anchor` tracks to JSON (OpenCV); ink-bleed mask frames from `panel_animator/ink_transition.py`.
2. **After:** ffmpeg mux, video from Remotion + audio stream copied from the shipped film.
3. **Gates:** stillness, guard, anchor, variety, landing hold.

Build notes for the engineer:
- New folder `_remotion/src/comic/`: `ink.ts` (seeded noise, `wobblePath`, wedge and splat makers), `devices/*.tsx` (one file per device, names as in section 1), `ComicFilm.tsx` (reads `episode.json`). Add one `<Composition>` to `Root.tsx`. Touch nothing else there.
- Wobble: compute wobbled points in JS with a seed. Do not use the SVG `feTurbulence` filter in the render (the mock uses it; it is slow and can differ between machines).
- Use `<OffthreadVideo>` with `startFrom`. `panel_shatter` and the "someday" panel at card 12 use a still frame (`<Img>`), not six videos.
- Risk: Remotion re-encodes and can shift colour slightly. That is why the stillness gate is 2.0, not 1.0. If the gate fails, render frames 674-796 straight from the shipped film and splice.
- Fallback: if Remotion video decode is unstable on this machine, the same `episode.json` can drive a Python build (`build_tp.render_shot` crops + PIL). The device names and parameters do not change.

---

## 4. Template rules for any 30-60 s film

**Length.** The audio sets the length. Never cut or stretch words to fit motion. The kit scales by count, not by speed.

| Film | Cuts with a transition | Doodle events | Pages (multi-panel) | Stillness window |
|---|---|---|---|---|
| 30 s | 11-13 | 16-20 | 3 | Jesus' line, at least 3 s |
| 38 s (this film) | 16 | about 24 | 4 | 4.1 s |
| 45 s | 17-20 | 26-30 | 4-5 | Jesus' line |
| 60 s | 22-26 | 34-40 | 5-7 | Jesus' line |

**Density.** One cut every 2-3 s. One doodle event every 1.5 s on average, outside the stillness window. At most 3 doodle devices on screen at once. At most one `jolt` per shot.

**Variety.**
- Never the same transition twice in a row.
- No transition more than twice per film, except `panel_slam` (it builds pages).
- At least 8 different transitions in a 30 s film, 10 in 45 s, 12 in 60 s.
- `punch_cut` at most twice. Always on purpose: out of a stillness, or onto a hit.
- Match energy to the line. Shout or action: `slam_cut`, `speed_zoom`, `panel_shatter`, `whip_pan`. Contrast of two people: `ink_slash_split`. Quiet or prayer: `halftone_dissolve`, `gutter_wipe`. Looking up or hope: `page_flip_up`, `iris`. Far or later: `pull_out_to_page`. Arrival: `ink_bleed`, `panel_dive`.

**Rhythm (the page feel).**
- Open on a page (2-3 panels) and dive in within 3 s.
- Never more than 3 full-bleed shots in a row without a page, a split or an inset.
- A page every 8-10 s. Full bleed where it hits.
- Give each speaker a mark that needs no reading: loud = spiky edge + fan. Quiet = dashed edge + halftone. Reuse a speaker's mark later to echo them (here: the dashed edge returns on "you").

**Jesus (binding).**
- His line: `border_fall` just before it, then `splash_border` only. Zero motion graphics until His last word ends. The stillness gate enforces it.
- Never a mark on His face or on a crucifixion close-up. A crucifixion close-up either stays clean or is not used.
- In a wide shot where He is small, keep a clear ring (here 250 px) and never aim a line at Him.

**Close.**
- The 3 s hold: `halftone_dissolve("rise")` or `iris` in, `border_build`, `page_settle`. The last 0.8 s is fully still. Sound keeps running to the end.

**Always.**
- Wordless. Vertical or radial motion only. Pill on top. Zones kept. Two-tone marks. Only marks boil. Audio copied, not re-mixed.
- Log which transitions each film used. The next film must not open or close with the same pair.
