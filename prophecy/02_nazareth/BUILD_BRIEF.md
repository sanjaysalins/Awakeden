# Build brief: Nazareth comic film v1 ($0 build)

Goal: build "He stopped mid-sentence" (Isaiah 61 -> Luke 4) as a comic-PAGES film with the same kit and look as the locked Thief model film. $0: no paid tools.

## Read first (model to copy)
- Model film lock: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\MODEL_FILM_LOCK.json`
- Formula card: `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\design\FORMULA_CARD.md` (section 1 Look row + section 3)
- Build notes + "how a new episode declares pages": `F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_ELEVATE\formula\build\BUILD_NOTES.md`
- Thief episode builder + data: `...\formula\build\build_thief_v3.py`, `thief_episode_v3.json`, `pages.py`, `prep_assets.py`, `gates_comic.py`, `frames.cjs`
- Kit: `F:\slk\PycharmProjects\JesusInTheBible\_remotion\src\comic_kit\` and `_remotion\src\ThiefComic.tsx`
- Pills: `poc_comic_page\_ELEVATE\build_w3.py` `pill_tabs` (same translucent pill + speaker tab + verse chip as Thief), hook card `build_tp.light_text`.

## Inputs (episode folder `F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_nazareth\`)
- Locked words: `words\FINAL_WORDS_v4.md`.
- Audio (final, includes the 3.0 s silent hold): `audio\narration.mp3` = 54.64 s. Word times: `audio\narration.words.json` (whisper). Turn times: `audio\timeline.json`.
- Clips (720x1280, 24 fps, no audio): `clips\S01.mp4` .. `S14.mp4`. 5 s each except S09 and S14 = 10 s. Stills (same pictures) in `stills\S01.png` ..
  S01 Jesus stops reading, lifts eyes | S02 Nazareth village | S03 synagogue wide, Jesus reads (USE ONLY first ~2.5 s: end zooms onto scroll scribbles) | S04 attendant hands scroll | S05 poor widow, hope | S06 broken shackle | S07 Jesus' hands roll scroll shut | S08 Isaiah writing at night (USE ONLY first ~2.5 s: end is just a hand) | S10 also only first ~3 s (camera drifts off the front man) | S09 Jesus seated (His line) | S10 row of men staring | S11 two men amazed | S12 townsman doubting | S13 boy with Joseph in workshop (memory: give it a sepia/aged tint) | S14 Jesus on the hill above Nazareth at sunrise (landing + hold).

## Beats (word times, seconds)
hook "Jesus stopped reading in the middle of a sentence" 0.0-2.6 | "In Nazareth, His home town" 2.96-4.5 | "stood to read from the prophet Isaiah, written long before" 4.9-8.3 | "He read God's promise of someone sent with good news for the poor" 9.44-12.9 | "freedom for prisoners" 13.18-14.3 | "and a time of God's welcome" 14.5-16.1 | "Then He rolled up the scroll" 16.82-18.2 | "Isaiah's sentence goes on:" 18.96-20.4 | ISAIAH "and the day of vengeance of our God" 20.9-23.3 | "He left the day of vengeance unread, and sat down" 23.5-26.4 | "Every eye was on Him" 27.28-29.0 | JESUS "This day is this scripture fulfilled in your ears" 29.62-34.2 | "The people were amazed at His kind words" 34.44-36.6 | "They knew Him as a local boy" 37.14-38.6 | TOWNSMAN "Is not this Joseph's son?" 39.56-42.3 | "That local boy was saying Isaiah's promise was about Him" 42.34-45.7 | "He stopped reading at God's welcome, and said: This day." 46.76-51.5 | silent hold 51.5-54.64 (S14, still).
Check exact frames against `narration.words.json` (move frame = ceil(word_start*30), never early).

## Rules (binding)
- Comic pages: 2-4 live panels per page, panels slam in on words, camera reads panel by panel. >= 60% of runtime on 2+ panel pages (gate G10). Full-bleed only for the hook payoff, Jesus' line, and the landing/hold.
- Every panel is a real clip. NEVER freeze, boomerang, ping-pong or slow a clip to fill a slot; trim only. A clip must be >= its on-screen time (5 s clips: keep each panel's life <= ~5 s, or use S09/S14 for long holds). S03/S08 only their first ~2.5 s.
- No duplicate clip on one page (G11). Crop on faces, never the back of a head. Check every crop by eye.
- Jesus' line (29.6-34.2): S09, still. No border motion, no doodles, no marks. Nothing drawn on any Jesus face panel (add no_draw masks for S01, S03, S07, S09, S14).
- Hook: Isaiah's skipped words are the heart: make "and the day of vengeance of our God" feel like words left on the page (e.g. S08 page with a quiet halftone hush), but draw NO letters or words on the art.
- Pills: English pills on screen like Thief (y around 1000, keep clear of top 200 px and bottom from 1500 px). Speaker tabs: ISAIAH + chip ISAIAH 61:2; JESUS + chip LUKE 4:21 (jesus style); A TOWNSMAN + chip LUKE 4:22. Narrator pills without tab. One short hook card in the first ~2 s (e.g. "HE STOPPED READING", Bangers-style like Thief's hook card). No other text, no sound-effect words.
- Full comic motion (owner): page turns, slams, dives, doodles throughout, each tied to a word, but stillness for Jesus' line and the 3 s hold. Vary transitions (no device twice in a row).
- Output 1080x1920, 30 fps, exactly the audio length; audio = `audio\narration.mp3` copied bit-for-bit (no music yet).
- Gentle mode: Remotion `--concurrency=2`, ffmpeg `-threads 2`, one heavy job at a time.
- Put clips into `_remotion\public\comic_nazareth\` (30 fps, prepped like prep_assets.py). Add ONE new Composition in Root.tsx (id without underscores, e.g. NazarethComic) with the right frame count; do not touch other compositions.
- Never commit anything. Never open any file or browser.

## Deliver
1. `prophecy\02_nazareth\film\NAZARETH_COMIC_v1.mp4`
2. Episode data + builder in `prophecy\02_nazareth\build\` (`build_nazareth.py` -> `nazareth_episode.json`), gates run (adapt gates_comic.py: duration, audio identical, stillness on Jesus' line, word sync, pill zone, no-draw, G10 coverage, G11 variety) -> `build\gates_out.txt`.
3. Contact sheet `build\contact_v1.jpg` (one frame per page + key moments) and LOOK at it yourself: crops on faces, no clones, no text on art.
4. Review page `prophecy\02_nazareth\_FILM_v1.html` (simple, big video, short words; the video via relative path).
5. Short report: page plan (page -> panels -> times), gate results, anything you are unsure of.
