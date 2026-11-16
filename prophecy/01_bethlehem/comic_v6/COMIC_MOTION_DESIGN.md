# Born in Bethlehem - COMIC MOTION DESIGN v6

Design only. $0. Words and voice are LOCKED (`words/FINAL_WORDS_v3.md`, `audio_v3/narration_v3.words.json`).
Film: 1080x1920, 30 fps, 59.5 s. Same 8 clips. Clips play at 1.0x, trim only.
Standard: `v2/LIVINGPAGE_STANDARD.md`, adapted to a short. Devices: `panel_animator/README.md`.
Previews: `comic_v6/preview_1.png` .. `preview_4.png` (built by `comic_v6/make_previews.py`).

## 0. What was wrong (from the v2 film frames)

The pictures are comic pages: black ink, flat rich colour, three panels, white gutters.
The overlays came from a different book:

| Overlay today | Why it reads "sketchbook" |
|---|---|
| Map of Judaea | A full cream parchment page with thin pencil lines. It **replaces** the comic page three times (about 10 s). |
| Time scroll | Another full cream page. No panel, no ink, no colour. |
| Rings, stars, crown, footprints | Thin wobbly pencil lines. No black outline, no flat fill. |
| Red stamps | Office rubber stamps, tilted. A desk object, not a comic object. |
| KJV scroll | A parchment prop on top of the art. |

So the fix is not "more doodles". It is: **nothing may leave the comic page.**

## 1. The series grammar (repeats in every prophecy episode)

1. **The page is the world.** Every graphic is a panel, a border, a gutter, lettering, or ink. No parchment, no pencil, no stamps, no props.
2. **A map is a panel, never a page.** It is drawn in the art's own ink (black outline 7 px, flat colour, dot screen) and sits in one panel slot while the other panels keep playing real clips. One full-height map splash is allowed per episode, at most 5 s.
3. **One line code, used for everything:**
   **dashed ink = promised / not done yet. Solid gold ink = done.**
   Footprints, panel frames and the end card all obey it. A newcomer learns it once, in the first 4 s.
4. **Motion is cut on the words.** Slams, whips and takeovers land within +/-0.05 s of a spoken word (30 fps frame snap). No motion that is not on a word.
5. **Punch budget for a 59 s short:** at most 5 slams, 3 whips, 2 takeovers, 2 impact bursts, 2 ink transitions. Spread thin. Never two in the same second.
6. **Slam = 4-frame slide + ink speed lines + 6-frame page shake + low boom.** The standard's white impact flash is **dropped** here (owner: no flash frames). Speed lines do that job.
7. **Sacred stillness.** Birth, Mary and the child, the cross, the tomb, the risen Jesus: no slam, no shake, no burst, no speed lines, no big lettering. Only slow line draws on **borders and gutters**, never on the picture. Other panels step back (dim + dot screen) so the eye rests.
8. **Lettering is owner-locked.** See-through Mockers pills, Kalam, speaker tab, gold verse chip. Not replaced. Comic touches allowed: a see-through tail for the two quoted voices (prophet, scribe).
9. **Big comic lettering is rare and spoken.** Bangers, cream or gold, black outline, hard ink shadow, tilted. At most 2 per episode, only words the voice says, only over empty sky or a gutter. Here: `DID THEY GO?` and `WENT`.
10. **Place and time captions** are the small yellow comic caption box (ink border, hard shadow). At most 4 per episode, in a panel corner. They label, they do not narrate.
11. **Print pass last.** `print_grade` over the whole film: paper grain + faint dot screen in the darks, so drawn panels and painted panels sit in one print.
12. **Extra words on screen** (not narration): only place names, verse chips, speaker tabs. No distances, no numbers that are not spoken.

## 2. The ONE signature move: THE PROMISE PANEL

A prophecy is **an empty panel waiting for its picture.**

- When the prophet speaks the promise, a **dashed, empty ink panel frame** draws itself on the page, with the gold verse chip (`MICAH 5:2`) on its corner.
- When the promise comes true, the **same frame returns as one solid gold line** around the panel that fulfils it. A cream tab `CAME TRUE` joins the verse chip.
- It never slams. It draws. Dashed in ~10 frames, gold in ~25 frames.
- End card: the gold frame draws round the **whole screen**. The whole film is the kept promise.

This replaces the red stamps "A PROPHECY" and "CAME TRUE". It works for every episode (Isaiah 53, Zechariah 9:9, Psalm 22): dashed frame at the promise, gold frame at the fulfilment.
The footprints are the same idea in small: dashed print = a step not taken; gold print = a step taken.

## 3. Beat by beat (times are the real v3 voice)

Panel rects come from gutter tracking (section 5). "Rack" = `grid_choreography` (one panel bright, others dim).

| Time (s) | Voice | What the viewer sees | Device | Why |
|---|---|---|---|---|
| 0.00-0.50 | "The Bible" | P1 page, held wide. All three panels alive. Pill reads along. | none | Frame 1 holds real art (DoD 4). |
| 0.50-1.30 | "experts knew" | Rack to top panel on "experts". On "knew" (0.94) the face panel **slams**: 4-frame push to 1.08, shake, boom. | rack + SLAM 1 | "Knew" is the charge of the hook. |
| 1.30-3.30 | "where the King would be born." | Rack down to the night-road panel on "where". Its ink border thickens. Small caption box `BETHLEHEM` on the far town at "born" (2.14). | rack + caption | Shows "where" before the question. |
| 3.32-4.10 | "Did they go?" | `DID` 3.32, `THEY` 3.42, `GO?` 3.58 slam in, one word each, over the road panel's sky, tilted. From 3.58: 7 **dashed hollow** prints stamp up the painted road, one every 2 frames. Shake on `GO?`. Pill is hidden for this line (the lettering is the read-along). | SLAM 2 + lettering | Hook kept. Teaches "dashed = not done". **preview_1** |
| 4.10-6.05 | "About 700 years earlier," | **WHIP** left through the gutter to the P2 page (3-frame streak + whoosh). A yellow caption box `ABOUT 700 YEARS EARLIER` snaps into the top-left corner on "700" (4.22), holds to 6.0. No parchment page. | WHIP 1 + caption | The classic comic time caption. Saves 2 s of empty paper. |
| 6.10-9.10 | "a prophet called Micah, a man who spoke God's message," | P2 page pans. On "Micah" (6.72): speaker tab `MICAH` with a short ink pointer. Rack to his face panel, then the sunlit town panel on "message". | rack | Calm. Let the art work. |
| 9.10-11.55 | "named a small town," | M1 full frame (Micah points). Cut is a plain hard cut. | none | A moment clip needs no dressing. |
| 11.60-14.60 | "Bethlehem. God promised a King from there." | **PROMISE PANEL, part 1.** On "Bethlehem" a dashed empty frame (2.1:1, about 420x200) draws round the far town. Chip `MICAH 5:2` lands on its corner at "promised" (12.88). On "King" (13.46) a small inked gold crown (black outline) pops inside the frame. | signature | The promise is an empty panel. |
| 14.80-17.30 | "Micah called Him / ruler in Israel." | P2 lamp, then Micah's face (as now). The KJV words sit in the pill with tab `MICAH`, a see-through tail up to him, chip `MICAH 5:2`. The dashed frame shrinks into the top-right corner as a small badge and stays. | pill + tail | Parchment scroll removed. Lettering stays see-through. |
| 17.45-19.70 | "Mary and Joseph lived far away." | **Map splash panel** wipes in with a brush `ink_transition` (8 frames) on "Mary". Night-blue, inked, dotted. `NAZARETH` caption top. Camera starts on Nazareth. Two small inked walkers. On "far" (18.44) the camera glides south. | ink transition 1 | The only full-height map. It is a panel: white margin, ink border. |
| 19.74-21.90 | "A tax order sent them to Bethlehem." | On "tax" (19.86) a small inset panel **slams** onto the map: an inked scroll with a red seal, impact burst on the seal. Gold prints stamp south behind the walkers (they went). On "Bethlehem" (20.96) the **dashed promise frame** is waiting round Bethlehem on the map. | SLAM 3 + burst 1 | The seal is a real point of contact. Gold prints: they went. |
| 21.90-22.10 | (join) | **TAKEOVER:** the camera dives into the dashed frame. Its edges become the manger panel's border (match cut, 6 frames). | TAKEOVER 1 | The empty panel is about to be filled. |
| 21.96-24.40 | "There, God's promise came true:" | **Sacred.** Manger panel. The two lower panels step back. From "promise" (23.02) to "true" (23.84) the dashed frame becomes **one solid gold line**, drawn once round the border. `MICAH 5:2` + `CAME TRUE` tabs fade in on the gutter at 23.84. | signature, part 2 | No slam, no stamp, no shake. **preview_3** |
| 24.48-26.60 | "Jesus, the King, was born." | Held. Pill only. Gold frame stays. | stillness | Sacred hold, 2.1 s. |
| 27.30-27.80 | "Wise men" | Rack releases down to the camel panel. | rack | Eye moves, nothing added to the manger. |
| 27.80-30.40 | "reached Jerusalem, asking where this King was." | **WHIP** through the gutter to the P4 page on "Jerusalem". Caption box `JERUSALEM` top-left. | WHIP 2 + caption | Place caption in comic form. |
| 31.02-33.40 | "Herod, the king there, asked the experts." | Herod's throne panel **slams** on "Herod" (shake, boom). Rack to the scribes panel on "experts" (32.90). | SLAM 4 | Herod is the threat. Not sacred. |
| 33.84-35.60 | "In Bethlehem of Judaea." | Scribe panel pushes in. Speech pill with see-through tail, tab `A SCRIBE`, chip `MATTHEW 2:5` (as now). | pill + tail | Kept. |
| 36.30 | (cut) | **WHIP** up through the gutter to the P1 page (clip from 1.3 s). | WHIP 3 | P4 footage ends at 37.5. |
| 36.44-37.90 | "Bethlehem was close by." | The **middle panel** brush-wipes into the **map panel** (8 frames). Top panel still shows the experts over their scroll. Bottom panel still shows the real night road. On "close" (37.30): 7 dashed hollow prints stamp along the short road. | ink transition 2 | The map is one panel of a live page. **preview_2** |
| 37.90-39.00 | (the 1 s silence) | Nothing moves but the clips. The first hollow print pulses once. Score dips. | stillness | The silence is the point. Kept. |
| 39.04-41.90 | "The Bible never says the experts went." | Rack to the experts (top). On "never" a double ink underline in the pill. On "went." (40.72) the same dashed prints stamp on the **painted road** below. They stay hollow. | rack | Calls back the hook picture. |
| 42.12-44.00 | "The wise men went," | On "went" (42.80) the **camel panel slams** over the experts, tilted 3 degrees, speed lines, shake, boom. `WENT` lettering on its corner. The map prints turn **gold** one every 2 frames, impact burst on the last, then gold prints carry on **across the gutter** down the painted road. | SLAM 5 + burst 2 + border-break | The pay-off of the spine. **preview_4** |
| 44.00-46.00 | "and found the child. But Jesus came" | **Sacred.** M2, Mary and the child. A round inked panel opens from the Bethlehem star (20 frames, no flash). Pill only. | calm iris | No ring, no rays on the picture. |
| 46.00-47.10 | "much farther." | P5 page. Rack to the sky panel. | rack | |
| 47.16-48.60 | "He came down from heaven." | One unbroken **gold line** comes down from the galaxy, **crosses the gutter**, and stops on the top border of the cross panel. It never enters it. Slow (40 frames). | border-break, slow | Gold = the one who came. The only one whose line crosses every gutter. |
| 48.92-50.50 | "He died for our sins." | **Sacred.** Cross panel. Nothing added. Other panels step back. | stillness | |
| 50.80-52.20 | "On the third day," | **Sacred.** Tomb panel, rack only. | stillness | |
| 52.24-53.40 | "He rose from the dead." | The tomb panel's ink border opens and the M3 picture grows from panel size to the full screen (20 frames, ease, no shake). | border-break, calm | LIVINGPAGE queued move: the risen panel is too big for its frame. |
| 53.50-56.40 | "Before anyone went to Him, He came to us." | Pill only. Gold brush underline under "He came to us" at 55.42. | stillness | |
| 56.40-59.50 | (hold) | The gold Promise frame draws round the whole screen (30 frames). Two tabs low: dashed `PROMISED.` then gold `CAME TRUE.` Hold 3.1 s. | signature, close | End card kept, in the same code. |

Counts: 5 slams, 3 whips, 1 takeover, 2 bursts, 2 ink transitions, 2 big letterings, 4 caption boxes (`BETHLEHEM`, `ABOUT 700 YEARS EARLIER`, `NAZARETH`, `JERUSALEM`; the map's own town captions count as part of the map panel).

## 4. Sacred check

| Window | On screen | Not on screen |
|---|---|---|
| 21.96-26.60 birth | gold line on the panel border, two tabs in the gutter, pill | slam, shake, burst, lettering, anything over the manger |
| 44.00-46.00 Mary and child | calm round panel opening, pill | rings, rays, gold on the picture |
| 47.16-52.20 heaven, cross, tomb | gold line in sky panel + gutter only, pills | anything inside the cross or tomb panels |
| 52.24-59.50 risen Jesus | panel grows, pill, underline, screen-edge frame, tabs | shake, boom, burst, anything on His face or body |

## 5. Build notes (Remotion)

- New file `_remotion/src/BethlehemV6.tsx`. Do not touch `BethlehemV5.tsx`. Composition ids start with `BTH6_`.
- Drop the old time warp. Key everything to `narration_v3.words.json` directly. One helper: `at(wordIndex) -> frame`.
- **Gutter tracking.** P1, P3, P4, P5 pan slowly, so panel rects move. Measure once per clip: every 0.5 s, find rows where mean brightness > 225 across x 200-880 (those are the gutters). Store `{t, y0, y1}` per panel in `comic_v6/panel_rects.json`, lerp between keys. Measured so far (1080x1920): P1 at 2.6 s gutters 578-597 and 1250-1270; at 7.9 s 367-389 and 1164-1185. P3 at 1.5 s 623-638 and 1295-1309.
- **Map panel** = one SVG component `MapPanel({rect, view, goldUpto})`. Black stroke 7 px round joins, flat fills, an SVG dot-screen pattern. Night palette sampled from the P1 road panel (#1e3476 to #101a42). Road band #6a84c4. Towns ochre #e2a842 / shadow #96602a. Sea #2a96aa.
- **Footprints** = one component `Print({dashed|gold})`. Draw a real shoe-sole path (the preview uses two ellipses; make it better). Stamp = scale 1.5 to 1 in 3 frames. Gold fill #f6b923, 4 px black outline.
- **Promise frame** = `PromiseFrame({rect, state: dashed|gold, progress})` using stroke-dashoffset. Same wobble seed in both states so it is clearly the same frame.
- Reuse: `grid_choreography` idea for rack focus (dim 35% + dot screen on the others), `impact_burst` shapes for the 2 bursts, `ink_transition` mask for the 2 brush wipes, `print_grade` as the last ffmpeg pass. `line_boil` and `parallax` are not used: every panel is already a moving clip.
- Clip use: P1 0-4.1 and 1.3-9.0 (36.3-44.0); P2 0-5.0 and 5.55-9.5; M1 0-5.0; P3 0-5.7; P4 0-8.8; M2 0.7-2.7; P5 0-6.2; M3 0-7.3. All inside the clip lengths. No freeze, no loop.
- Sound (not designed here): 5 booms, 3 whooshes, 2 small hits, score dip at 37.9-39.0. Measure the mix.

## 6. Honest risks

1. **The drawn map is flatter than the painted panels.** In the previews it reads as "flat vector comic" next to "painted comic". The dot screen, ink weight and print pass help; they do not fully close the gap. It is small (one panel) for map B/C, but the 4.4 s map splash (17.45-21.9) is the weakest stretch. Fallback: make that splash a half-height panel over a held P2 pan.
2. **The previews are stills. The comic feel is won in motion** (slams on words, rack focus, whips). Build a 9 s motion test of 36.3-45.0 first, before the full film.
3. **Gutter tracking** is new work. If a rect drifts 5 px the map panel shows a white sliver. Needs an eye-check per clip.
4. **Yellow caption boxes are opaque.** The owner rejected opaque lettering boxes. These are small place/time labels in corners (under 4% of the frame each), not narration. If the owner dislikes them, swap to the gold chip style; the design survives.
5. **`DID THEY GO?` and `WENT` are Bangers.** Same font the owner rejected for narration boxes. Here it is display lettering over empty sky, twice. Needs the owner's yes.
6. **Gold frame on the manger panel** touches only the border, but it is still gold on a sacred beat. Needs the doctrine panel's and the owner's eye.
7. **P1 footage is seen twice** (hook, then 36.3-44.0). The second time its middle panel is the map and its top is covered by the camels at 42.8, so it should not feel repeated. Check in the motion test.
8. `NAZARETH` is not a spoken word (kept from v2, as the owner allowed). `the east` is dropped.
9. Not yet run: the 5-CLI panel on this plan, the global-audience blind test, the guardrail questions. This is a design, not a lock.
