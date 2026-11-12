# Motion design brief: Mary and Martha (Warm Storybook), tighter cut v2

Owner's words (2026-11-12, after watching MARY_MARTHA_SCORED_v2.mp4): "its nice, I just [feel] we can do a better
transitions effects for this episode and we can do the great motions graphics and doodles".
So: (1) better TRANSITIONS between the 15 shots (now all hard cuts), (2) great MOTION GRAPHICS, (3) DOODLES.
$0 only: built in Remotion (1080x1920, 30 fps) by me after your spec. No new AI images or clips.

## Read these (all paths absolute)
- The film words + timing: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\voice_v2\narration.md
  and per-word times (seconds) F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\voice_v2\narration.alignment.json
- The 15 shots, one gridded frame each (red grid = 108 px wide x 192 px tall cells of the real 1080x1920 frame, 10x10 cells):
  F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\f01.png ... f15.png (f01 = shot 1, in film order), sheet SHEET_grid.jpg
- The look: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\STYLE.md
- A spec we built before for another episode (copy its FORMAT and precision, NOT its ideas or colours — that film was ink+watercolour, this one is warm storybook):
  F:\slk\PycharmProjects\JesusInTheBible\poc_living_water_ink_style_test\swirls_episode_16_let_the_little_children\motion_v2\MOTION_DESIGN.md
  and its Remotion build F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\Ep16ChildrenV2.tsx

## The cut (film seconds; frames = s x 30). Film = 71.61 s = 2148 frames (68.61 s voice + 3 s silent hold).
Each shot is its own Kling clip played at 1.0x from its frame 0. "Tail" = spare clip seconds AFTER the cut, usable for a transition
that overlaps INTO the next shot (the next shot must still start at its cut time, on its word).
| # | clip | start-end | words | tail |
|---|---|---|---|---|
| 1 | s01 | 0.00-5.95 | You do everything for everyone. Does anyone even care? | 0.09 |
| 2 | s02 | 5.95-8.70 | Martha asked Jesus that. | 2.29 |
| 3 | s03 | 8.70-10.95 | She had opened her home to Him. | 2.79 |
| 4 | s04 | 10.95-15.45 | While she served, her sister Mary sat at His feet and listened. | 0.54 |
| 5 | s05 | 15.45-22.25 | MARTHA: Lord, dost thou not care ... help me. | 1.24 |
| 6 | s06 | 22.25-27.90 | His answer? Her name. Twice. | 0.39 |
| 7 | s07 | 27.90-31.80 | JESUS: Martha, Martha, thou art careful and troubled about | 3.14 |
| 8 | s08 | 31.80-35.30 | many things: But one thing is needful: | 2.54 |
| 9 | s09 | 35.30-40.25 | and Mary hath chosen that good part ... from her. | 0.09 |
| 10 | s10 | 40.25-43.75 | "Careful" means full of worry. | 3.54 |
| 11 | s11 | 43.75-50.40 | The one thing needed was to hear Him ... from Mary. | 1.39 |
| 12 | s13 | 50.40-53.85 | So, did He care? | 2.59 |
| 13 | s14 | 53.85-61.45 | Later, the Bible says: "Now Jesus loved Martha, and her sister, and Lazarus." | 0.44 |
| 14 | s12 | 61.45-64.00 | He never called Martha's work wrong. | 3.49 |
| 15 | s15 | 64.00-71.61 | Under all her work, He saw her worry. And He loved her. (+3 s hold) | 2.43 |
Music: soft felt piano; it turns at 50.4 s ("So, did He care?") and warms fully at ~55.4 s ("Now Jesus loved Martha").

## Rules
- Global audience, English as a second language: on-screen words few, plain, short; they must HELP a newcomer
  (e.g. plain meaning of "careful" = worry, "many things" vs "one thing"). Never a full caption track.
- KJV words on screen must be word-for-word. Do not put words in Martha's or Jesus' mouth.
- Doodles must look drawn by the SAME hand as the pictures (soft pencil + gouache, honey / terracotta / cream; see STYLE.md).
  No UI shapes, no pills, no glow, no sparkle, no lens flares, no emoji, no generic infographic clichés.
- Never cover faces or hands-touching moments. Respect Shorts safe zones (keep text inside x 60-950, y 160-1490).
- Leave quiet stretches: the hero pictures (s14 the family, s15 the ending) should breathe. Spread effects thin and pick each on purpose.
- Martha is not the villain. No mockery of her work. Grace, not pressure.
- Transitions: pick per cut, on purpose (many cuts should stay hard cuts). A transition may only overlap into the next shot
  by up to the outgoing clip's tail. Name an exact duration in frames and the easing.
- ONE visual thread from first frame to last (like the ep16 "not now" slip), that pays off at the ending.

## Output
Write ONE file: F:\slk\PycharmProjects\JesusInTheBible\poc_warm_storybook_style\motion_v1\MOTION_DESIGN.md
Build-ready, same precision as the ep16 spec: the idea in 3 lines, a beat table (frames on/off, word it hits, what appears,
motion with easing, box in px checked against the gridded frames, colours as hex, why), a transitions table (every cut:
hard / which effect / frames), the thread, a "do not" list, and risks. Do not write any code.
