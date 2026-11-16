# Motion / doodle / edit layer - design brief (Fable seat). Design only, no build, $0.

## The ask (owner, verbatim)
"do a very creative bold and creative doodling across this and do some clever edits and transitions effects to elevate this video. Look at the past few episodes to get a good idea"

## The film
- Woman at the well (John 4), ~87.8 s vertical 1080x1920, 30 fps. 19 Kling clips, hard cuts, trim only.
- Look: black-and-white halftone ink people/places on loud pop-art burst rays (orange, red, teal, yellow).
- Shots in order: motion_v1/STILLS_SHEET.jpg. Words: words/FINAL_WORDS_v1.md (line 12 is now a quiet, awed read).
- Line times (voice time): audio/timeline.json. FILM time = voice time, +1.0 s after 54.10 (a silent pause after "He is the Christ"), +3.0 s hold at the end.
- Cut list (film time): build_film.py CUTS. Current film: WOMAN_AT_WELL_POC.mp4 (being rebuilt with 2 softer shots + quieter line 12; same order).
- Owner's tone notes today: tears/joy close-up felt unnatural -> now quiet tears; Jesus laughing -> now a gentle smile; her "Come, see a man" -> now somber and reflective. The film's ending should feel reflective, not loud.

## Past episodes to learn from (read these)
- LIKED: Mary and Martha motion layer. Design poc_warm_storybook_style/motion_v2/MOTION_DESIGN.md (+ OWNER_REFS.jpg, QC_sheet.jpg); code poc_warm_storybook_style/_remotion/src/MaryMarthaV4.tsx. Owner rounds there: "bigger doodles, flowers/vines/butterflies in all 15 scenes."
- LIKED: The Second Fire motion layer. poc_folk_print_style/motion_v1/MOTION_DESIGN.md; code poc_folk_print_style/_remotion/src/SecondFireV1.tsx.
- REJECTED as "sloppy": Zacchaeus motion pass. poc_scratchy_ink/zacchaeus/_work/MOTION_DESIGN_FABLE.md (rough displaced scratchy lines + caption pills over scratchy art = mess).
- You may extract frames from any .mp4 with ffmpeg to look.

## Hard rules
- Bold but CLEAN: crisp shapes, confident line weight, designed for this pop-art/halftone world (think comic-book graphics: halftone dot fields, burst stars, speed lines, ink splashes, bold outline doodles), not wobbly scratch.
- Doodles drawn in code (SVG/Remotion), never by an image model. No text drawn by models.
- Reverent: nothing jokey on Jesus, the tears, or the tomb. Quiet moments get quiet doodles or none.
- Never cover faces or hands. Never add a halo/glow on Jesus. Do not animate over the art in ways that change what the Bible says.
- Global audience: if any words appear on screen, short and plain; KJV only word-for-word.
- Transitions: clever but motivated by the story (e.g. the water/jar/burst idea), at most ~5 special ones; hard cuts stay the default.
- It must still build in Remotion like the two liked episodes (reuse their components where possible).

## Output: write motion_v1/MOTION_DESIGN.md
1. One-line idea (the visual spine of the doodles).
2. House look in <=6 lines (colours, line, motion rules).
3. A shot-by-shot table (all 19 shots): film time, doodle (what, where on frame, when it draws on, on which word), transition into the next shot.
4. The 3-5 signature moments described frame by frame.
5. What you deliberately leave plain, and why.
6. Top 3 risks of looking sloppy, and how the design avoids them.
Keep it short, plain words. Write the file, then return a 10-line summary.
