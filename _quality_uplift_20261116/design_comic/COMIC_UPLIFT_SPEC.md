# Comic uplift: build spec for the 9 graphic comic shorts

Date: 2026-11-16. Design pass only. Nothing built. Nothing spent. Repo untouched (only this folder written).
Owner page (short, with a moving mock): `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\design_comic\_COMIC_UPLIFT_PLAN.html`

---

## PART 0. Plain summary (read this first)

**What I found (I watched all 9 by frames, and read the build files).**

1. **Grids are one clip cut 3 ways.** True in all 9. It is a setting in the build (`hero_frac3` / `hero_band3`). The same tool can already do a page with 3 different clips. So this is a $0 fix.
2. **New find: clips are slowed down to fill time.** Each clip is 5 seconds. Many slots are 5.5 to 8 seconds. The old tool stretches the clip (slow motion, up to 1.58x). Your rule says no. About 32 slots in the 9 films. Fix at $0: cut to a second picture on a spoken word.
3. **Correction to the first report.** It said "use other clips we already have". In 8 of 9 folders every clip is already used. Spare clips do exist, but in sister folders (same art style). I list the exact files.
4. **Some key pictures are stills with a camera slide, not real clips** (David writing, the scroll, 5 pictures in Women First Witnesses). Real clips of David and the scroll exist in the Mockers folder. $0.
5. **Wrong picture on key lines**: Forsaken Cry 0:40, Behold Thy Son 0:28 and 0:32, I Thirst 0:36, Empty Tomb 0:48.
6. **No doodles anywhere yet.**
7. **Women First Witnesses has a broken subtitle file** (covers 13 s of an 82 s film) and no word timings. $0 to redo.

**What I designed.**

- One small **kit of 6 hand-drawn marks** for all 9 films (gold thread, ink ring, strike, underline, tally, dotted route). No new words on screen. Never on Jesus. None while Jesus speaks. Max 6 per film.
- A **fix list per film**, with exact clip files.
- A **pilot**: *Woman, Behold Thy Son*. Full shot list below.

**Money.** The whole plan is **$0** to build. Optional paid extras are listed apart: about **$5 must-have later** (Thomas' hands, 3 Women clips), about **$10 to $14 nice-to-have**. Rough. Needs a real quote. Nothing is spent without your yes.

**No narration changes in this pass.** Audio is copied bit for bit from each shipped film.

**My pick: build the pilot (Woman, Behold Thy Son) first, $0. Say yes?**

---

## PART 1. How these films are really built (facts the executor needs)

| Fact | Where |
|---|---|
| Each film = a spec of beats. | `<piece>\visual\livingpage_short.spec.json` |
| Engine (ffmpeg + PIL). | `F:\slk\PycharmProjects\JesusInTheBible\longform\02_Psalm_22_Song_From_The_Cross\build_livingpage_16x9.py` run with `--pool <piece>\visual --spec livingpage_short.spec.json --page 1080x1920 --clips` |
| Page templates. | `F:\slk\PycharmProjects\JesusInTheBible\longform\_style_poc\ew04\_mocomic\comic_engine.py` `TEMPLATES` |
| `hero_frac3`, `hero_band3`, `hero_frac4` = mode `fracture` = ONE clip cut into panels. | same file |
| `stack_h` (2 rows), `two_v` (2 columns), `strip_h3` (3 rows), `quad`, `big_inset` = mode `fill_each` = one clip per panel. | same file |
| A clip shorter than its slot is slowed (`setpts`) or boomeranged. | `comic_engine.py` lines 277-288 |
| Per-beat segments and caption layers are kept. | `<piece>\visual\_livingpage_work\seg_NN.mp4`, `_kc16_<beat>_<state>.png` (1080x1920 RGBA, one per caption word state), `_red16_*.png` |
| Chain to the final: spec preview -> `_scored.mp4` -> `_sfx.mp4` -> hook + decode cards by ffmpeg drawtext -> `_sfx_v5hook.mp4`. | card data: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_audit\fixes\<id>.json`, recipe: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_audit\BRIEF.md` |
| Sound baked into the audio: a boom at every `fill_each` panel arrival (`clips[].at`), a tick at every `inserts[].at`, a whoosh at every `whip`, a tear at `border_break`. Fracture panels have NO boom. | engine lines 600-680 |
| Remotion comic kit (typed, data driven, 14 wordless doodles, 12 transitions, page moves, gates). | `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\comic_kit\`, notes `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build\BUILD_NOTES.md`, gates `...\formula\build\gates_comic.py` |
| Word timings. | `<piece>\audio\alignment.json` (list of `{w,start,end}`). Good for 8 films. **Stale for Women** (13 s only). |

### The route I chose (and why)

**Keep the livingpage engine for the pictures. Put one Remotion layer on top for marks and page turns.**

- It is the owner's rule: clips first, Remotion on top.
- Bake-off 2 showed the shipped livingpage film beat a full rebuild from clips (3 of 4 seats). So do not rebuild in a new look.
- The audio never changes, so score, SFX and voice stay locked.

```
uplift spec (new file)  ->  livingpage engine (--no-sfx)  ->  seg_NN.mp4 per beat
   ->  Remotion "UpliftFilm" (segs in a row + page turns + marks)  ->  silent mp4
   ->  hook + decode cards (same drawtext recipe, same numbers)
   ->  mux: video new, audio COPIED from the shipped final  ->  <slug>_uplift_v1.mp4
```

Never overwrite. Build in a new pool folder `<piece>\visual_uplift\` (copy the stills, `*.anchor.json`, clips and the spec there; engine flag `--pool`). `FINAL_VIDEO.txt` changes only after the owner says yes.

---

## PART 2. The comic uplift kit

### 2a. Fix rules (apply to every film)

| # | Rule | How |
|---|---|---|
| F1 | No page shows one clip twice. | Every `hero_frac3` / `hero_band3` / `hero_frac4` beat becomes a full single panel, or a `fill_each` page with different clips. |
| F2 | No clip is stretched. Speed factor max 1.05. | Slot longer than 5.29 s (4.24 s for the two 4.04 s clips) gets a second shot, cut on a word start. |
| F3 | The key line shows the thing it says. | Swaps listed per film. |
| F4 | No still-with-camera-slide where a real clip exists. | David and scroll: use the Mockers clips. Others: priced list. |
| F5 | One clip: max 3 uses in a film, max 1 of them full-bleed, each use a different crop and a different start time. | The engine lint says max 2. A 3rd use as a small panel is an allowed, listed exception. |
| F6 | Audio is untouched. | Beat edges never move. Keep every existing `clips[].at`, `inserts[].at`, `whip`, `border_break` time. New panel arrivals use `"flash": false` (soft, silent). |
| F7 | Each film ends on its own picture of Christ. | `cross_at_dawn` stays the ending of *It Is Finished* only. |
| F8 | Crop a panel on the face, never the back of a head. Check cloned people and era on every new crop. | Eye check on a contact sheet. |

### 2b. The 6 marks (new, built once in Remotion)

Look: brush ink, hand wobble, same weight as the panel borders. Captions are Comic Sans Bold in a cream box, so marks are plain strokes, never letters.

| Colour | Hex | Use |
|---|---|---|
| Ink | `#14100C` | default, on light pictures and on the caption box |
| Bone | `#F4ECD8` | on dark pictures |
| Gold | `#F2C14E` (the hook card yellow) with a 3 px ink under-stroke offset (2,2) | the Echo Thread only |

| # | Mark | What it is | Size and timing | Max per film | Exists? |
|---|---|---|---|---|---|
| K1 | **Echo thread** | One gold hand line that ties two things that match: Old Testament to Jesus, shadow to cross, one person to another. Crosses a gutter between two panels. Ends in a small knot. | 7 px. Draws in 12 to 16 frames, starting on the word. Holds to the end of the beat. | 2 | New. `thread` |
| K2 | **Ink ring** | A hand ellipse, two passes (full, then a lighter offset pass). Around ONE caption word or one small object. | 7 px then 4 px. 12 + 8 frames. Holds until the caption box changes, min 1.0 s. | 2 (or more if the ring is the film's one running idea, see Empty Tomb) | Look exists in `panel_animator\annotators_circle.py`. New in Remotion: `ink_ring` |
| K3 | **Strike** | One hand line through a caption word the narrator rejects ("Not judge"). | 7 px. 6 frames. | 2 | New. `ink_strike` |
| K4 | **Underline** | One hand line under a caption word. | 7 px. 8 frames. | 2 | New. `ink_underline` |
| K5 | **Tally** | Hand ticks that count something the voice counts (3 days, 8 days, 2 works). Ticks land one by one, 3 frames each. | 54 px tall, 6 px. In a clear corner of the picture, never the caption zone. | 1 | New. `tally` |
| K6 | **Dotted route** | A dotted path that draws itself, with a small arrow head. For a walk, a run, a "went the other way". | Dots 10 px, gap 22 px. Speed fits the phrase. | 1 | New. `route` (also the gaze line: `route` with `dash:"gaze"`, no arrow) |

Already built and allowed (the comic energy set, use 0 to 2 per film): `speed_lines`, `shout_fan`, `shock_lines`, `rays`, `crack_lines`, `halftone_vignette`, `drops`, `motion_ticks` in `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\comic_kit\doodles.tsx`.
Page turns already built (use 2 to 4 per film, never the same one twice in a row): `page_flip_up`, `halftone_dissolve`, `ink_bleed`, `whip_pan`, `iris`, `gutter_wipe`, `punch_cut` in `...\comic_kit\transitions.tsx`.

### 2c. Mark rules (so it never gets busy)

1. **Max 6 marks in a film up to 60 s. Max 8 in a longer film.** Page turns do not count.
2. **One mark at a time.** Never two drawing together. Never while a hook or decode card is up in the same area.
3. **Never on Jesus** (face, body, hands, halo). Every panel that shows Him gets a `no_draw` box. A thread may end on the wood at the foot of the cross.
4. **No mark while Jesus speaks** (caption speaker tab JESUS). Stillness there.
5. **No mark on the last shot.** The landing is still.
6. **No new words.** Marks point at words already in the caption, or at the picture. (Films get dubbed. Meaning must be spoken.)
7. **Never early.** A mark starts on the start frame of its word (`ceil(start*30)`), never before.
8. **Marks boil** (2 drawings, swap every 3 frames). Pictures never boil. No boil in quote beats.
9. A page turn may hold the last frame of the old beat under the wipe for up to 10 frames. That is a turn, not a fill.
10. Keep `y 1480 to 1920` clear of marks when the caption sits there. A mark on a caption word is the only thing allowed inside the caption box.

### 2d. Tool work, once ($0)

| # | Build | File | Notes |
|---|---|---|---|
| T1 | A `fill_each` twin of the big-plus-two layout. | `comic_engine.py` `TEMPLATES`: add `"big_two": ("fill_each", "corner", lambda a: _big_two(a))` | One line. Additive. |
| T2 | Mid-beat cuts: a beat may hold `"parts": [{"until": t, "tpl":..., "clips":[...]}, ...]`. Build each part as its own segment, join, THEN apply the caption, shake, fx, exact frames. The caption runs across the cut. | `build_livingpage_16x9.py`, about 30 lines, behind the new key so old specs build the same. | Test: an old spec must still give the same `seg_NN.mp4` sizes and frame counts. |
| T3 | `t_in` on a clip def (start offset in the source clip, seconds). | same engine, pass to the trim | Needed for F5. If the engine already trims from 0 only, add `-ss`. |
| T4 | New marks K1 to K6. | new file `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\comic_kit\hand.tsx`, using `InkStroke`, `wobblePts`, `boilSeed`, `mulberry` from `core.tsx`. Register the 6 kinds in the doodle switch. | Positions: `pos.xy` (screen px) or `pos.track` (list of `[frame,x,y]`). |
| T5 | `UpliftFilm.tsx`: plays `seg_NN.mp4` back to back (`OffthreadVideo`), page turns between them, marks on top, `marks:true` render mode for gates. One `<Composition id="UpliftFilm">` line in `Root.tsx` (that file has uncommitted edits: add one line only). | `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\UpliftFilm.tsx` | Copy the pattern of `ComicFilm.tsx`. |
| T6 | `word_boxes.py`: caption word boxes. Kinetic captions: box of word n = pixels in `_kc16_<beat>_<n>.png` that are not in state n-1. Quote captions: split red ink runs in `_red16_*.png` by row and gap, check the count equals the word count. | new folder `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\uplift\` | Output `word_boxes.json`. |
| T7 | `track_pts.py`: follow a picture point through a clip segment (OpenCV LK or template match), output `[frame,x,y]`. | same folder. Start from `build_thief.track()` in `...\formula\build\build_thief.py`. | Gate: max 12 px off on 5 frames, checked by eye. |
| T8 | `build_uplift.py <piece>` (runs the chain in Part 1) and `gates_uplift.py`. | same folder | Gates below. |

### 2e. Gates (all must pass before the owner sees a film)

| Gate | Check |
|---|---|
| U1 | Video and audio same length as the shipped final, within 1 frame. 1080x1920, 30 fps. |
| U2 | Audio stream MD5 equals the shipped final's audio MD5. |
| U3 | Beats that did not change: mean pixel difference to the shipped film under 2.0 (cards and marks masked). |
| U4 | No clip speed factor above 1.05 (report every slot: slot length, clip length, factor). |
| U5 | No page with the same clip twice. Uses per clip max 3, full-bleed max 1. Exceptions listed. |
| U6 | Marks: count within the cap, none overlap in time, none start before their word, none inside a `no_draw` box, none in a JESUS quote beat, none on the last beat (marks-only render, pixel count). |
| U7 | Caption zone and card zone clear of marks (except ring, strike, underline on a caption word). |
| U8 | Eye check: contact sheet at 1.5 s steps. Faces not cropped. Same person looks the same. Era. No cloned people. Look at every mark at 2x zoom. |
| U9 | Blind red team of the finished film (independent Fable seat + AI panel), old vs new, before any pin or upload. `check_landing_hold.py` and `release_check.py` green. |

---

## PART 3. Per film

Notation: `b7` = beat 7 of the shipped spec. Times in seconds. "full" = one full-bleed panel. All clip paths are real files checked on disk today. Shared base: `B1 = F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross`, `B2 = F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_02_resurrection`.

**Honest note.** The pilot (film 4) is worked out shot by shot in Part 4. For the other 8 the fix list and the marks are firm, but the executor must finish each one with the same method as the pilot: write the uplift spec, run the engine lint, check rule F5, and look at a contact sheet. Where a film runs out of spare clips I say so.

Two clips serve three films (David and the scroll). They are 720x1280 and 4.04 s:
`B1\mockers_words_ps227\visual\clips\david_writing_psalm.mp4`
`B1\mockers_words_ps227\visual\clips\psalm_scroll_night.mp4`
Use them at most 4.24 s per shot. Check sharpness when full-bleed (1.5x upscale). If soft: priced re-animate at 1080p (see money).

### Film 1. The Forsaken Cry (58.2 s, 13 beats)

Slowed today: b3 5.25 s, b9 6.11 s, b10 7.34 s. Stills not clips: b2 David, b5 scroll.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b2 4.92-9.80 | David still cut 3 ways | Two shots: 4.92-7.10 David clip (Mockers file), 7.10-9.80 scroll clip (Mockers file). Cut on "a thousand" 7.10. |
| b3 9.80-15.05 | three crosses cut 3 ways | 9.80-13.75 `golgotha_hill_wide` full. 13.75-15.05 `face_on_cross` full ("Jesus made it His own" 13.75). |
| b4 15.05-17.82 | two strangers kneeling under "David's very first line" (wrong) | David clip, start offset 1.5 s. |
| b5 17.82-22.60 | scroll still | 17.82-21.49 scroll clip. 21.49-22.60 David clip tail (start offset 2.8). Quote caption runs across. |
| b7 27.15-31.90 | nail head and fresh blood in frame at the ninth hour | Same clip `bowed_head_finished`, crop up: zoom 1.25, bias y 0.25. Hand and nail leave the frame. Check all 5 s. |
| b8 31.90-34.45 | faces cut 3 ways | `two_v` page: left scroll clip (3rd use, small), right `bowed_head_finished` (small, cropped as above). This is the "same words" page. |
| b9 34.45-40.56 | face cut 3 ways, slowed | 34.45-38.10 `face_on_cross` full is its 2nd full use, so make it a `stack_h` page with `look_up_faces` below. 38.10-40.56 `golgotha_hill_wide` centre-cross crop. |
| b10 40.56-47.90 | **warm risen Jesus under "bearing the forsaking"** (wrong) | 40.56-44.60 `us_under_cross_shadow` full (us, under His cross: "taking our place"). 44.60-47.90 `stack_h`: `ninth_hour_darkness` over `darkness_veil_torn` (a dark page). Keep the insert at 45.2. |
| b12 51.70-55.60 | father at door cut 3 ways | `father_lamp_doorway` full. |
| b13 55.60-58.18 | shared cross at dawn | `risen_mercy_hand` (moved here from b10). The film now ends on the risen Christ: "He opened it from the dark". |

**(b) Marks (4)**

| Word, time | Mark |
|---|---|
| "thousand" 7.20 | K4 underline on caption words A THOUSAND YEARS |
| "same" 32.39 | K1 gold thread across the gutter, from the scroll to the cross beam (wood, not Him). The film's one big idea. |
| "my" 39.42 | K2 ring on caption words MY GOD |
| 44.60 to 47.4, opens at "He was forsaken" 48.50 | `halftone_vignette` closes in on the dark page, then clears as the light pours (existing doodle) |

Page turns: `ink_bleed` at 47.90 (dark to light).

**(c) Needs money:** none required. Later, with the "my God, and your God" idea (words gate first): 1 new clip, Easter morning, about $1 to $1.50.

### Film 2. I Thirst (55.7 s, 12 beats)

Slowed today: b5 7.2 s, b7 6.15 s, b9 7.3 s, b10 5.4 s. Stills not clips: b3 David, b6 scroll.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1 0-4.90 | ocean cut 3 ways | `ocean_creation_wide` full. Hook card stays. |
| b2 4.90-8.60 | face cut 3 ways | `face_on_cross` full. |
| b3 8.60-13.00 | David still cut 3 ways | 8.60-10.93 David clip. 10.93-13.00 `B1\forsaken_cry_ps221\visual\clips\golgotha_hill_wide.mp4` ("someone else's death"). |
| b4 13.00-15.20 | strangers kneeling under "Watch the body give out" | `bowed_head_finished` full, cropped up (no nail, as film 1). |
| b5 15.20-22.40 | pot, slowed 1.43x | 15.20-19.59 `potsherd_dry_clay`. 19.59-22.40 `face_on_cross` small crop is not possible full twice, so: `stack_h` page, pot above (already running), face below arriving 19.59 ("and my tongue"). Decode cards stay. |
| b6 22.40-26.45 | scroll still | scroll clip (4.04 s, fits). |
| b7 26.45-32.60 | bowed head, slowed | 26.45-29.53 `potsherd_dry_clay` cracks crop (offset 2.5). 29.53-32.60 `us_under_cross_shadow` ("sinking into the dust"). |
| b9 36.70-44.00 | **Jesus in the garden cut 3 ways under "it paints the thirst"** (wrong) | 36.70-39.96 `two_v` page: left scroll clip, right `vinegar_sponge_reed` (crop on reed and sponge). 39.96-44.00 `potsherd_dry_clay` wide (3rd use). Garden clip leaves the film. |
| b10 44.00-49.40 | stream, 5.4 s | `living_water_stream` full, entered by a 10-frame `ink_bleed` from the dry clay. This is the dry-to-wet turn. |
| b11 49.40-53.30 | shared risen hand | `ocean_creation_wide` second crop ("Bring Him your thirst": back to the sea of the opening). |
| b12 53.30-55.74 | shared cross at dawn | `risen_mercy_hand` ("That water is Himself"). |

**(b) Marks (3)**

| Word, time | Mark |
|---|---|
| "foretell" 38.12 | K1 gold thread across the gutter: scroll to the reed |
| "living" 46.56 | K4 underline on LIVING WATER |
| "thirst" 51.06 | K2 ring on caption word THIRST |

**(c) Needs money (optional):** cupped hands lifting water, 1 still + clip, about $1 to $1.50, for b11.

### Film 3. Today in Paradise (59.1 s, 16 beats)

Slowed today: b7 7.95 s (1.58x, the worst), b8 5.24, b10 6.44.

**Your call first:** the loved 38 s Thief short tells this same story with these same clips and is already posted. This 59 s film may read as a repeat. I put it last.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1 0-2.90 | crosses cut 3 ways | `golgotha_hill_wide` full. |
| b7 18.82-26.77 | two thieves cut 3 ways, slowed 1.58x | 18.82-23.02 `two_thieves_wide` full. 23.02-26.77 `stack_h`: `penitent_thief_face` over `golgotha_hill_wide` centre cross ("this man hath done nothing amiss"). |
| b8 26.77-32.01 | confession cut 3 ways, **flash of the mocker during the confession** | `confession_face_hands` full. Keep the insert time, change its picture to `golgotha_hill_wide`. |
| b10 36.37-42.81 | Jesus' line, slowed 1.28x | 36.37-41.79 `jesus_turns_to_thief` entered by a 10-frame `iris` (no ring). 41.79-42.81 `penitent_thief_face` (he hears "in paradise"). No marks. |
| b11 42.81-46.35 | shared risen hand under "He asked for someday" | 42.81-44.65 `kingdom_light_clouds` (someday, far off). 44.65-46.35 `answer_light_profile` small page with `paradise_dawn`. |
| b12-b14 | quick 2-panel pages | keep (they are real 2-clip pages). |

"Same nails" but ropes: b2 already shows `nail_through_hand` on the word "nails". That helps. The ropes stay in other shots. Real fix costs money (below).

**(b) Marks (4)**

| Word, time | Mark |
|---|---|
| "Same" 2.90, 4.04, 5.20 | K5 tally, 3 ticks, one per "Same" |
| "save" 13.52 | `shout_fan` from the mocker's mouth (existing, proven on the Thief film) |
| "nothing" 25.57 | K2 ring on caption words NOTHING AMISS (the thief speaks, not Jesus) |
| "same" 45.59 | K4 underline on SAME AFTERNOON |

**(c) Needs money:** thieves drawn nailed, 3 stills + clips, about $3.50 to $4.50. Or change one word in the voice (words gate + voice quote). My advice: hold this film.

### Film 4. Woman, Behold Thy Son (59.1 s, 13 beats) = THE PILOT

See Part 4.

### Film 5. It Is Finished (59.1 s, 17 beats)

Slowed today: b8 5.8 s, b13 5.67 s.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1 0-3.40 | garden cut 3 ways | `eden_garden_finished` full. |
| b3 7.03-12.00 | bench cut 3 ways. Saw looks modern. | `carpenter_bench_rest` full, crop on the mallet and pegs so the saw is out of frame (try zoom 1.5). If the saw cannot be cropped out: priced. |
| b4 12.00-15.55 | crosses cut 3 ways. **The world never breaks on screen.** | 12.00-13.86 `eden_garden_finished` second crop + `crack_lines` on "wrecked" 12.94. 13.86-15.55 `golgotha_hill_wide` full ("the Son came down"). |
| b7 22.60-24.40 | olives cut 3 ways | `gethsemane_olives_night` full. |
| b8 24.40-30.20 | John 17 prayer, slowed | 24.40-27.33 `jesus_prays_night`. 27.33-30.20 `hands_shaping_light` small page with `nail_through_hand` ("I have finished the work"). No marks (He speaks). |
| b9 30.20-31.80 | strangers cut 3 ways | `us_under_cross_shadow` full. |
| b12 39.85-43.08 | garden + face page | keep. Add marks. |
| b13 43.08-48.75 | tomb cut 3 ways, slowed | 43.08-45.65 `seventh_day_light` ("finished creation, and rested"). 45.65-48.75 `tomb_stone_sealed` full. Check the round stone does not roll (first frame vs last frame). |
| decode card | GAVE UP THE GHOST = DIED runs 38.85-40.70, over the next page | end it at 39.85. |
| b17 ending | cross at dawn | keep. This is the one film that owns it. |

Fact note, your call: the John 17 prayer is drawn in the garden. John 18:1 says He prayed it before the garden.

**(b) Marks (4)**

| Word, time | Mark |
|---|---|
| "wrecked" 12.94 | `crack_lines` across the garden (existing, never used yet) |
| "Two" 39.89, "works" 40.45 | K5 tally, 2 ticks |
| "One" 41.41 | K1 gold thread across the gutter: garden to the cross wood |
| "morning" 50.91 | `rays` soft behind the open tomb (existing) |

**(c) Needs money (optional):** bench without the saw, about $1.20. John 17 in the right place, about $1.20.

### Film 6. Father, Into Thy Hands (59.0 s, 14 beats)

Slowed today: b9 6.05 s, b13 5.65 s. Stills not clips: b3 scroll, b8 father at the door.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1 0-4.16 | crosses cut 3 ways | `golgotha_hill_wide` full. |
| b2 4.16-9.30 | child cut 3 ways | `child_sleeping_lamp` full (5.14 s, inside the limit). |
| b3 9.30-14.60 | scroll still | 9.30-13.34 scroll clip. 13.34-14.60 `child_sleeping_lamp` lamp crop (offset 3.0). |
| b4 14.60-17.98 | face cut 3 ways | `face_on_cross` full. |
| b7 25.20-29.40 | hands cut 3 ways | `father_hand_childs_hand` full. |
| b8 29.40-33.10 | father at door, a still cut 3 ways | real clip `B1\forsaken_cry_ps221\visual\clips\father_lamp_doorway.mp4`, full. |
| b9 33.10-39.15 | nail under "The Psalm he prayed says" | Two shots: 33.10-36.85 scroll clip ("thou hast redeemed me"), 36.85-39.15 `nail_through_hand` ("On that cross, he was buying that redemption"). Keep the insert time. |
| b11 41.80-43.58 | tomb | `child_waking_dawn` full ("morning came"). |
| b12 43.58-48.30 | waking child cut 3 ways | `stack_h`: `first_day_morning` over `father_holds_sleeping_child` crop. |
| b13 48.30-53.95 | closing eyes, slowed | 48.30-51.91 `child_eyes_closing`. 51.91-53.95 `father_hand_childs_hand` second crop ("the hands are strong"). |
| b14 53.95-59.03 | shared cross at dawn | `first_day_morning` (the open tomb at sunrise: "He keeps the morning"). Lands on the risen Christ's morning, and it is this film's own. |
| decode card | COMMEND = ENTRUST runs 23.90-25.70 | end it at 25.20. |

**(b) Marks (4). The best doodle idea of the whole set lives here.**

| Word, time | Mark |
|---|---|
| "judge" 29.70 | K3 strike through caption word JUDGE |
| "stranger" 31.05 | K3 strike through caption word STRANGER |
| "Father" 32.70 | K2 ring on caption word FATHER. Two wrong words struck, one word kept. No letters added. |
| "third" 42.03 | K5 tally, 3 ticks |

**(c) Needs money:** none. Later, with the "first and last words" idea: boy in the temple, about $1 to $1.50.

### Film 7. The Sign of Jonah (69.5 s, 20 beats)

Slowed today: b9 5.42 s, b10 5.16 s (inside the limit). Two clips are used full twice back to back (b16+b17, b19+b20).

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1, b3, b6 | one clip cut 3 ways | full: `jonah_cast_overboard`, `storm_ship_waves`, `lot_falls_jonah`. |
| b4 8.64-11.96 | Nineveh as a stepped pyramid (wrong era look) | `stack_h` page. Top: a paper map panel drawn in Remotion (K6: a dot, an arrow east for "sent", then at b5 a boat line west). Bottom: `nineveh_distant_walls` cropped to the gate towers only (zoom 1.6, bias y 0.75) so the pyramid top is out of frame. Check by eye. |
| b5 11.96-14.59 | storm cut 3 ways | same page stays: bottom swaps to `storm_ship_waves` close crop. The boat line draws on "drown" 13.82. |
| b8 21.35-25.51 | Jonah in fish cut 3 ways | `stack_h`: `great_fish_rising` crop over `jonah_in_the_deep` crop. |
| b9 25.51-30.93 | 5.42 s | enter by a 10-frame `page_flip_up` ("long after I was dust"). |
| b12 40.83-44.40 | sinking cut 3 ways | `jonah_sinking_down` full. |
| b14 49.50-53.38 | tomb + shore page, half blank at first | keep the page and its boom time. Top panel present from 49.50. Add the thread. |
| b16+b17 54.60-61.40 | same clip full twice | 54.60-59.42 `mercy_hand_into_deep` as one run (4.82 s). 59.42-61.40 `three_days_dark_tomb` ("It cost Him the grave"). |
| b19+b20 63.60-69.52 | same clip full twice | 63.60-66.70 `stone_rolled_dawn` ("rose again"). 66.70-69.52 `risen_christ_wounds` (landing). |

**(b) Marks (5)**

| Word, time | Mark |
|---|---|
| "throw" 1.32 | `speed_lines` parallel, down |
| "sent" 10.92, "drown" 13.82 | K6 route on the map panel: arrow one way, boat the other way |
| "lot" 18.13 | K2 ring round the fallen lot (tracked) |
| "Three" 22.95 | K5 tally, 3 ticks (Jonah's own line, not Jesus') |
| "than" 51.34 | K1 gold thread across the gutter: empty tomb to Jonah on the shore |

Existing punch and border break on "He rose" 53.38 stay.

**(c) Needs money (only if the crop fails):** Assyrian Nineveh, 1 still + clip, about $1.20.

### Film 8. The Empty Tomb (79.1 s, 20 beats)

Slowed today: b14 5.42, b16 5.74, b17 6.06, b18 5.48. Same clip back to back: b3+b4 (Mary), b7+b8 (napkin), b15+b16 (Thomas).

This film is short of pictures: the linen and the napkin each need about 9 s and have one 5 s clip each.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b3+b4 9.50-16.16 | Mary clip twice | 9.50-14.16 `mary_runs_predawn` one run. 14.16-16.16 `stone_taken_away_dark` door crop ("we know not where"). |
| b5 16.16-18.74 | runners cut 3 ways | `two_disciples_running` full. |
| b6 18.74-21.86 | linen cut 3 ways | `stack_h`: `john_believes_inside` crop over `linen_left_lying` crop. |
| b7 21.86-26.04 | napkin | `linen_left_lying` full ("not lying with the linen clothes"). |
| b8 26.04-30.93 | napkin cut 3 ways | `napkin_wrapped_apart` full, one run (4.89 s). |
| b9 30.93-33.24 | John cut 3 ways | `john_believes_inside` full is needed at b12, so here: `tomb_doorway_dawn` crop (he steps in). |
| b10 33.24-36.16 | stone cut 3 ways | `stone_rolled_dawn` dark-doorway crop, full. |
| b11 36.16-40.03 | linen | `stack_h`: `linen_left_lying` (3rd use, small) over `napkin_wrapped_apart` (small). |
| b13 44.43-47.73 | risen Christ cut 3 ways | `risen_christ_seeking` small page with `john_believes_inside` crop. |
| b14 47.73-53.15 | **the outside stone under "The linen was enough"** (wrong) | 47.73-51.93 `stone_taken_away_dark` wide. 51.93-53.15 cut to the cloth on "The linen": `napkin_wrapped_apart` (offset 3.0). |
| b15+b16 53.15-61.43 | Thomas clip twice, hands very red | $0 version: 53.15-55.69 `jesus_shows_thomas` cropped on Thomas. 55.69-60.50 same clip wide, one run. This is over the limit (8.28 s of one 5 s clip). Real fix is the priced Thomas clip. |
| b17 61.43-67.49 | 6.06 s | enter by a 10-frame `halftone_dissolve`. Still 1.14x. Accept for a quote beat or use the priced clip. No marks. |
| b18 67.49-72.97 | 5.48 s | enter by a 10-frame `page_flip_up`. |

Check each tomb clip, first frame vs last frame: the round stone must not roll.

**(b) Marks (6). The ring is this film's running idea: evidence.**

| Word, time | Mark |
|---|---|
| "ran" 16.34 | `speed_lines` behind the runners |
| "place" 27.16 | K2 ring round the rolled napkin (tracked). Bone colour. |
| "saw" 42.29 | K2 ring on caption word SAW |
| "linen ... enough" 52.73 | K4 underline on ENOUGH |
| "Eight" 55.69 | K5 tally, 8 ticks |
| "you" 71.83 | K2 ring on caption word YOU |

**(c) Needs money:** Thomas with healed marks, not wet blood: 1 still + clip, about $1.20 to $1.50 (I rate this must-have). Second angle of the linen and of the napkin: about $2.40 (nice to have).

### Film 9. Women as First Witnesses (82.0 s, 18 beats)

Do first, $0: re-run word alignment on `B2\women_first_witnesses_luke245\audio\narration.mp3` (the `alignment.json` there is an old 13 s file), then rebuild `publish\captions.srt` (it also stops at 13 s). Mark times below are beat times until that is done.

Slowed today: b1 5.29, b9 6.2, b11 5.73, b13 5.11. Stills with a camera slide, not clips: `women_tell_news` (b2, b5), `women_behold_burial` (b8), `magdalene_face_cu` (b14), `graveclothes_linen` (b15). Three real clips sit unused: `two_men_shining`, `women_dawn_spices`, `women_remember`.

**(a) Fixes, $0**

| Beat | Now | Change |
|---|---|---|
| b1 0-5.29 | apostles cut 4 ways | `stack_h`: `apostles_dismiss` over `apostles_doubt_closer`. |
| b2 5.29-9.77 | still | `women_plead_closer` full. |
| b3 9.77-13.40 | pleading cut 3 ways | `women_remember` full (unused clip; look at it first). |
| b5 17.50-21.50 | still | `stack_h`: `women_run_tell` crop over `apostles_doubt_closer` crop. |
| b8 29.20-32.20 | still | `women_dawn_spices` is dawn, not burial. No $0 clip fits. Keep the still as a small panel beside `women_cross_afar`, or use the priced clip. |
| b9 32.20-38.40 | 6.2 s | 32.20-35.30 `women_tiny_dawn`. 35.30-38.40 `women_dawn_spices` (unused clip). |
| b10+b11 38.40-49.00 | same clip full twice | b10 `two_men_shining` (unused clip). b11 `women_bowed` one run 5.04 s, entered by a 10-frame `halftone_dissolve`. |
| b14 59.11-63.60 | still | priced, or `women_remember` second crop. |
| b15 63.60-68.00 | still | `B2\empty_tomb_john208\visual\clips\linen_left_lying.mp4`. |
| b16 68.00-73.00 | running cut 3 ways | `women_run_tell` full. |
| b17+b18 73.00-82.04 | same clip full twice, 9 s | 73.00-77.50 `risen_prophecy` second crop. 77.50-82.04 `risen_christ_seeking` (landing). |

**(b) Marks (5)**

| Line, beat | Mark |
|---|---|
| "idle tales" b2 | K2 ring on caption words IDLE TALES |
| b6 to b9 (21.5, 26.5, 29.2, 32.2) | K6 trail: a short dotted line with 4 stops in the top margin. One stop inks in per beat: Galilee, the cross, the grave, the dawn. No labels. |
| "The idle tale was true" b16 | K3 strike through caption word IDLE. Pays off the ring. |
| "first to know" b15 | K4 underline on FIRST |
| b13 | `rays` soft is not allowed here (words of the angels quoting Jesus, picture is Jesus). No mark. |

**(c) Needs money:** animate 3 stills we already have (`women_tell_news`, `women_behold_burial`, `magdalene_face_cu`), about $0.25 to $0.75 each, about $2 in all. I rate this must-have under the "hero images are real clips" rule.

---

## PART 4. The pilot: Woman, Behold Thy Son

### Why this one first

- **Smallest real test**: 59 s, 13 beats, 11 own clips.
- **It has the worst wrong-picture spot** of the nine: Jesus' two sayings play over two strangers and a nail. The right clips already exist in its own folder.
- **Its words are stable.** No new insight is queued for it, so the work is not thrown away.
- **It proves the kit's main mark** (the gold thread) twice, plus the gaze line, the route and two page turns. Film 2 in the order (Empty Tomb) then proves ring, underline and tally.
- All $0.

### Files

| Thing | Path |
|---|---|
| Piece | `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\woman_behold_john1926` |
| Shipped final (audio source, read only) | `...\woman_behold_john1926\visual\woman_behold_john1926_sfx_v5hook.mp4` (59.07 s) |
| Shipped spec | `...\woman_behold_john1926\visual\livingpage_short.spec.json` |
| Words | `...\woman_behold_john1926\audio\alignment.json` |
| Cards | `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_audit\fixes\woman-behold-thy-son.json` (hook "DYING, HE STILL SAW HIS MOTHER." 0-2.0 s; decode BEHOLD = HERE IS 29.8-32.2 s) |
| Own clips (all 1080x1920, 5.04 s) | `...\visual\clips\` : `simeon_baby_temple`, `mary_infant_shadow`, `golgotha_hill_wide`, `mary_at_cross`, `mary_and_john`, `jesus_looks_down`, `face_on_cross`, `john_leads_home`, `us_under_cross_shadow`, `nail_through_hand`, `risen_mercy_hand` |
| Borrowed clips (copy with their `.png` and `.anchor.json` into `visual_uplift\`) | `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\pierced_zech1210\visual\clips\john_watching.mp4` and `...\pierced_zech1210\visual\clips\mourners_only_son.mp4` |
| New pool | `...\woman_behold_john1926\visual_uplift\` |
| Output | `...\woman_behold_john1926\visual\woman_behold_john1926_uplift_v1.mp4` |

What the clips show (I looked): `mary_and_john` = John holding a crying Mary, bottom left; Jesus on the cross top right. `mary_at_cross` = Mary's face in profile, bottom left corner, the cross above. `jesus_looks_down` = His face, close, eyes down. `john_watching` = John alone, looking up, hand on chest, a cross far left. `mourners_only_son` = a group of mourners below the cross, dark sky. `john_leads_home` = John and Mary from behind walking to a city gate, three crosses on the hill.

**Risk to check by eye:** John in `john_watching` wears a tan cloak; John in `mary_and_john` wears grey with a brown mantle. Crop `john_watching` tight on the face and sky so the robe hardly shows. If he still reads as a different man, use `mary_and_john` cropped on John instead and list the extra use.

### Shot list (old beat edges never move)

Sound that is baked in and must keep its picture: boom 41.50 (b10 panel 2), boom 51.70 (b12 panel 2), tick 19.80 (b5 insert), tick 47.00 (b11 insert), whoosh at 7.84 and 49.22 (whips), tear 28.80 (border break), dawn 53.20.

| # | Time | Words | Now | New picture | Page | Notes |
|---|---|---|---|---|---|---|
| 1 | 0.00-4.18 | An old man in the temple... one dark sentence. | `simeon_baby_temple` full | same | full | No change. `punch`, `ramp` stay. Hook card stays. |
| 2 | 4.18-7.84 | Yea, a sword shall pierce through thy own soul also. | `mary_infant_shadow` full | same | full | No change. Quote beat (Simeon). No marks. |
| 3 | 7.84-13.06 | Simeon told Mary. Some thirty years later, the sword lands. | three crosses cut 3 ways | top: `mary_infant_shadow`, crop on the wall and the cross shadow (zoom 1.3, bias y 0.15, start offset 2.5 s), from 7.84. bottom: `golgotha_hill_wide`, crop on the centre cross and its foot, arrives 8.54, slide up, `flash:false`. | `stack_h` | Keep `whip`. Top panel runs 5.22 s = 1.036x, inside the limit. **Mark M1.** |
| 4 | 13.06-15.75 | Now there stood by the cross of Jesus his mother. | `mary_at_cross` full | same | full | No change. |
| 5a | 15.75-18.67 | Close enough to watch her son die. | John and Mary cut 3 ways | `golgotha_hill_wide` full, low crop (zoom 1.15, bias y 0.6), start offset 2.0 s | full | Part 1 of beat 5 (T2). `punch` stays on the beat. |
| 5b | 18.67-22.09 | Jesus looks down, sees her wound, and turns to bind it. | same | top: `jesus_looks_down` from 18.67. bottom: `mary_at_cross` cropped on her face (zoom 1.8, bias x 0.1, y 0.85, start offset 2.5 s), arrives 19.73 ("sees"), slide up, `flash:false`. | `stack_h` | Part 2. Keep the 4-frame insert at 19.80 (picture: `nail_through_hand`, as now). **Mark M2** starts after the insert. |
| 6a | 22.09-24.25 | When Jesus therefore saw his mother, | His face cut 3 ways | `mary_and_john` full (what He saw), start offset 0 | full | Part 1 of beat 6. Quote caption runs across both parts. The hollow-air sound at 22.15 stays. |
| 6b | 24.25-28.75 | and the disciple standing by, whom he loved, he saith unto his mother, | same | `john_watching` full, tight on the face (zoom 1.25, bias x 0.6, y 0.35) | full | Part 2. 4.50 s. |
| 7 | 28.75-31.87 | **Woman, behold thy son!** | two strangers kneeling (wrong) | top: `mary_and_john`, crop on the two faces with sky above (zoom 1.4, bias x 0.3, y 0.7, start offset 2.2 s). bottom: `jesus_looks_down`, eyes at about 35% of the panel height (start offset 2.0 s). Both present from the first frame. No slide, no flash. | `stack_h` | Jesus speaks: **no marks, no page turn**. Border break at 28.80 stays. The decode card (top, y 170-320) now sits on sky above Mary and John. The quote caption sits on His chest, not His face: check. |
| 8 | 31.87-36.22 | Then saith he to the disciple, **Behold thy mother!** | a nail in a hand (wrong) | top: `john_watching` face crop (zoom 1.5, start offset 2.5 s) from 31.87. bottom: `mary_at_cross` face crop (as 5b, start offset 0.5 s), arrives 33.87 on "Behold", slide up, `flash:false`. | `stack_h` | Keep `cap_at: 2.0` (the caption lands with the second panel). No marks. |
| 9 | 36.22-39.94 | And from that hour that disciple took her unto his own home. | `john_leads_home` full | same | full | Enter by page turn P1. **Mark M3.** |
| 10 | 39.94-43.60 | He gave her the disciple he loved. A son. A home. | Simeon + Mary and baby (wrong for this line), half blank until 41.5 | left: `mary_and_john` cropped on Mary only (zoom 2.0, start offset 3.5 s) from 39.94. right: `john_watching` cropped on John only (zoom 1.6, start offset 0.5 s), arrives **41.50** (the boom is there), slide right, flash on. | `two_v` | **Mark M4.** |
| 11a | 43.60-47.58 | While judgment fell on him, he cared for someone else. | looking-down face cut 3 ways | `face_on_cross` full | full | Part 1. `punch` stays. Keep the 4-frame insert at 47.00 (`golgotha_hill_wide`, as now). |
| 11b | 47.58-49.22 | That is who is dying there. | same | `nail_through_hand` full | full | Part 2. |
| 12 | 49.22-53.16 | Your wound is not invisible to him. He sees it from the cross. | Mary + crosses | top: `us_under_cross_shadow` (us) from 49.22. bottom: `golgotha_hill_wide` third crop (wide, start offset 3.5 s... if under 1.5 s is left in the clip, use offset 0 with a different crop), arrives **51.70** (the boom is there). | `stack_h` | Keep `whip`. |
| 13a | 53.16-55.18 | Stand where Mary stood. | risen hand, slowed 1.17x | `mourners_only_son` full, warm grade (`fx.temp` 5200) | full | Part 1. Enter by page turn P2. |
| 13b | 55.18-59.06 | The Son who saw her will behold you, and bind what the sword tore. | same | `risen_mercy_hand` full, 3.88 s | full | Part 2. Landing on Christ. **No marks.** Landing hold check. |

Clip use count after the change: `mary_at_cross` 3 (1 full), `mary_and_john` 3 (1 full), `john_watching` 3 (1 full), `golgotha_hill_wide` 3 (1 full) + 1 insert, `jesus_looks_down` 2 (0 full), `mary_infant_shadow` 2 (1 full), `nail_through_hand` 1 full + 1 insert, others 1. Slowest slot: shot 3 top panel, 1.036x. Everything else is 1.0x, trim only.

### Marks (4) and page turns (2)

| Id | Kind | Starts on | Frames | What is drawn | Where |
|---|---|---|---|---|---|
| M1 | K1 `thread`, gold | "sword" 11.54 (frame 347), done by "lands" 12.06 (frame 362). Holds to 13.06. | 16 | One hand line from the middle of the cross **shadow** on the wall (top panel) down across the gutter to the **foot of the centre cross** (bottom panel, on the wood and rock, never on Him). Small knot at the end. | Both ends tracked with `track_pts.py` (the shadow drifts in the clip). Soft S curve, 3 wobble points. |
| M2 | K6 `route`, `dash:"gaze"`, bone | frame 600 (20.00 s, after the insert flash 19.80-19.93). Done by 20.35. Holds to 22.09. | 10 | A dashed sight line from the bottom edge of the top panel (below His chin, outside the `no_draw` box) down to just above Mary's eyes in the bottom panel. No arrow head. | End point tracked on Mary's brow. |
| M3 | K6 `route`, ink | "took" 38.23 (frame 1147) to "home" 39.54 (frame 1187). Holds to 39.94. | 40 | A dotted path from in front of the two walkers' feet up the road to the lit gate. At "home": two short strokes, a small roof, above the gate. | 3 points tracked: feet, mid road, gate. Stay out of the caption zone (the quote box is low: check its box first with `word_boxes.py`; if the road start is under the caption, start the dots above the box). |
| M4 | K1 `thread`, gold | "son" 42.14 (frame 1265) to 42.50. Knot ties on "home" 43.24 (frame 1298). Holds to 43.60. | 12 + 6 | One hand line from Mary's shoulder (left panel) across the gutter to John's shoulder (right panel). On "home" a small knot closes at the gutter. A new family, drawn. | Tracked on both shoulders. |
| P1 | `page_flip_up` | 36.22 | 8 | "And from that hour": the page turns. | Old last frame may hold under the flip. |
| P2 | `halftone_dissolve` (rise) | 53.16 | 8 | Into the dawn (the dawn sound is at 53.20). | |

`no_draw` boxes: all of the `jesus_looks_down` panel in shots 5b and 7; the right 40% of any `mary_and_john` crop that shows His body; the centre cross body in `golgotha_hill_wide` (the foot of the post is free); all of shots 11a, 11b, 13b.

### Build steps for the pilot

1. Tool work T1 to T8 (once).
2. Copy the pool to `visual_uplift\`. Write `livingpage_short.uplift.spec.json` from the shot list. Keep every field of unchanged beats byte for byte.
3. `build_livingpage_16x9.py --pool <visual_uplift> --spec livingpage_short.uplift.spec.json --page 1080x1920 --clips --no-sfx --lint`, then the real build. Read the report: slot, clip, factor per panel.
4. Contact sheet of the new segments. Fix crops (rule F8) before any mark work.
5. `word_boxes.py`, `track_pts.py`. Write `uplift_marks.json` (M1 to M4, P1, P2, `no_draw`).
6. Remotion render (`UpliftFilm`, `--muted --crf=12`), then a marks-only render for the gates.
7. Hook and decode cards with the same drawtext recipe and numbers as the shipped film.
8. Mux with the shipped audio (`-map 0:v -map 1:a -c:a copy`). `+faststart`.
9. Gates U1 to U8. Then one owner page: old and new side by side, the 4 marks as stills at 2x, the gate table. Then U9 red team before any pin.

Rough effort: tools about one build session, pilot film about half a session. $0.

---

## PART 5. Build order and money

| Order | Film | Why here | $0 work | Paid, must | Paid, nice |
|---|---|---|---|---|---|
| 1 | Woman, Behold Thy Son (pilot) | smallest, worst wrong picture, stable words | all | 0 | own-ending clip about $1 to $1.50 |
| 2 | The Empty Tomb | proves ring, underline, tally | all but Thomas | Thomas clip about $1.20 to $1.50 | linen + napkin second angles about $2.40 |
| 3 | I Thirst | short, stable words, dry-to-wet turn | all | 0 | cupped hands about $1 to $1.50 |
| 4 | Father, Into Thy Hands | the strike-strike-ring on "Father" | all | 0 | 0 |
| 5 | The Sign of Jonah | map and thread; hook may change later (words gate) | all | 0 | Nineveh about $1.20 if the crop fails |
| 6 | It Is Finished | crack in the garden | all | 0 | bench about $1.20, John 17 place about $1.20 |
| 7 | The Forsaken Cry | landing words may change (strong new idea) | all | 0 | David + scroll at 1080p about $1.50 (helps films 1, 2, 6) |
| 8 | Women as First Witnesses | needs word timings first; court beat may be rewritten | most | 3 clips from stills we have, about $2 | 0 |
| 9 | Today in Paradise | same story as the posted Thief short; "same nails" | most | 0 | nailed thieves about $3.50 to $4.50 |

**Totals.** $0 work: all 9 films, plus the tools. Paid, must-have: about **$3.50 to $5**. Paid, nice-to-have: about **$10 to $14**. These are rough (plus or minus 30%), from the usual "about $1 to $1.50 per new shot, $0.25 to $0.75 to animate a still we have". Re-derive from the real invoice. Each spend needs its own quote and its own yes.

## PART 6. Later, needs the words gate (not in this pass)

No narration changes here. The checked ideas from `F:\slk\PycharmProjects\JesusInTheBible\_quality_uplift_20261116\_SUMMARY.html` stay parked: Forsaken Cry ("my God, and your God"), Women (Joanna), Jonah (Galilee), Empty Tomb (Lazarus still bound), Into Thy Hands (first and last words), Today in Paradise and It Is Finished (rework first). If one is adopted later, only the beats under the new words are rebuilt; the kit, the tools and the other beats stand.

One caption idea also parked (captions are on-screen words, so owner OK first): Today in Paradise could show SOMEDAY in the caption and strike it.

## Limits, said plainly

- I saw frames at 1.5 s steps and single clip frames. I did not watch playback or hear sound.
- The other 8 films are planned to the level of "which clip, which word, which mark". The executor must finish crops and the F5 count with the lint, as shown in the pilot.
- `women_remember`, `two_men_shining`, `women_dawn_spices`, `mourners_only_son` were checked to exist; only `mourners_only_son` and `john_watching` were looked at. Look before use (they may have been left out for a defect).
- Mark positions on moving pictures depend on tracking. Budget time for it.
- Odds (my guess): the pilot reads as clearly better than the shipped film to the owner: about 70%, plus or minus 15. Marks feel forced: about 20%, plus or minus 10. That is why the cap is low and the pilot comes first.
