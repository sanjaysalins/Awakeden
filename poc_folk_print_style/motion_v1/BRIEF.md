# Motion brief — "The Second Fire" (Folk Print POC) — transitions + doodles

Owner ask (2026-11-13): "can you do a better transition effect between scenes and can you use motion graphics to
add some great bolder fuller doodles to elevate this episode".

## The film
- Current cut: `SECOND_FIRE_SCORED_v2.mp4` (87.9 s, 1080x1920, 30 fps; 17 clips, HARD CUTS, 1.0x, trim only).
  Picture-only build: `build.py` (slot starts below). Audio is final (oud/ney/cello score + fire SFX); keep it.
- 17 shots, slots (s): s01 0-3.3 | s02 3.3-8.0 | s03 8.0-13.2 | s04 13.2-15.7 | s05 15.7-18.9 | s06 18.9-23.7 |
  s07 23.7-28.9 | s08 28.9-34.1 | s09 34.1-36.7 | s10 36.7-40.2 | s11 40.2-47.8 | s12 47.8-53.2 | s13 53.2-60.2 |
  s14 60.2-67.8 | s15 67.8-75.2 | s16 75.2-80.3 | s17 80.3-87.9 (incl. 3 s silent hold).
- Shot content + words: `PICTURE_PLAN.md`. Timed words: `score_sfx_panel/_timed_lines.txt`. Stills sheet:
  `motion_v1/STILLS_SHEET.jpg` (row order s01..s17). Full stills `stills_full/sNN.png` (1536x2752).
- Style: `STYLE.md` — flat mid-century folk-art print, burnt orange/coral/mustard + deep teal/bottle green + cream,
  risograph grain, bold simple shapes, thin dark outlines, woven geometric patterns (dots/zigzags/stripes), sunburst skies.
- Story spine: the "fire of coals" appears only twice in the Bible: the night Peter said "no" 3 times (teal night) and the
  sunrise breakfast where Jesus asks "do you love me?" 3 times (orange day). 3 no's -> 3 yes's. "Before Jesus asked Peter to
  feed anyone, Jesus fed Peter." The music: 3 notes falling at night, rising from sunrise. The SAME fire sound at 3 s, 37 s, end.

## What worked / failed before (Mary & Martha, same owner, `poc_warm_storybook_style/`)
- v1 doodles: owner "very forced ... not complementing" (generic stickers on top of the art).
- v2 WORKED: doodles drawn from the art's OWN vocabulary, coloured into the art (`motion_v2/MOTION_DESIGN.md`).
- Then the owner pushed: "much bigger", then "cutier and more fuller ... do that in all scenes" -> vines/buds/butterflies in
  every shot, x1.5 size, back-ease pop, sway, see-through swatches (~0.8). LOCKED. Code: `_remotion/src/MaryMarthaV4.tsx`.
- Zacchaeus motion push (`_remotion/src/ZaccPreview.tsx`) REJECTED as "sloppy". Avoid whatever made it sloppy (read it).
- This owner now asks for BOLDER and FULLER from the start. Do not go timid. But it must still look like part of the print.

## Hard rules
- Reverent: nothing on or across Jesus's face/body; no halo shapes; no doodles over faces at all; no text/lettering/glyphs.
- Voice + story first: the eye must still find the subject of each shot; doodles live in sky, sea, sand, edges, around fires.
- Transitions: motivated by the story and the folk-print look (e.g. sun-ray wipe at sunrise, wave wipe into the sea, fire-flare
  match between the two fires). Max ~3 transition TYPES; some cuts stay HARD on purpose (say which and why). No generic
  dissolves, no CG page curls. A transition may not delay or hide a key word; it can borrow up to ~0.3 s from either shot.
- Must be buildable in Remotion (SVG/CSS over the existing clips, 1080x1920, 30 fps), $0, deterministic.
- Clips must keep playing underneath (no freezes). No new AI renders.

## Deliverable
Write `motion_v1/MOTION_DESIGN.md`: (1) the idea in 3 lines; (2) the doodle vocabulary (6-10 motifs: shape, hex colours,
stroke, how it moves); (3) per shot s01..s17: which doodles, where (x,y in 1080x1920 px), size, timing (s), motion; (4) the
16 transitions: type, frames, what moves, why; (5) the two-fires moment (s02 / s10 / s11 / s17) designed as the showpiece;
(6) 3 risks + how to check each. Be concrete enough for an engineer to build without guessing.
