# BUILD BRIEF - Bethlehem film v5 (words v4 + voice v4). $0 ONLY.

## Hard rules
- $0. NO paid calls of any kind (no ElevenLabs, OpenArt, HF, Kling, Gemini, API). Only local Remotion, ffmpeg, Python.
- NEVER open any file/browser/HTML. Never commit. Never touch film/FINAL_VIDEO.txt (the locked v4 film stays pinned).
- Do not edit BethlehemV6.tsx; make a NEW file. Remotion composition ids cannot contain "_" (use e.g. "BTH8").
- Never commit or copy media into git.

## Inputs
- Locked words: prophecy/01_bethlehem/words/FINAL_WORDS_v4.md
- New voice: prophecy/01_bethlehem/audio_v4/narration_v4.mp3 (copied to _remotion/public/bethlehem/narration_v4.mp3), 56.25 s file.
- Word times (143 words, exact script text, real seconds): prophecy/01_bethlehem/audio_v4/narration_v4.words.json
- Turn timeline: prophecy/01_bethlehem/audio_v4/timeline.json
- The LOCKED current film's code: _remotion/src/BethlehemV6.tsx (comp in _remotion/src/Root.tsx). It is keyed to real seconds and to WORD INDICES wt(i) of audio_v3/narration_v3.words.json. Read it fully first, plus the v3 words json, to understand every wt(i) and hard-coded second.
- Reference: the locked film it renders to = prophecy/01_bethlehem/film/BETHLEHEM_FINAL_v4.mp4 (= v7 picture + v3 audio). The v7 picture fixes are already in BethlehemV6.tsx (NightCover over P3, KING HEROD cap, no underline on "never").
- Score + SFX scripts used for the locked film: prophecy/01_bethlehem/score/mix_score_cine.py (score parts score/cine_part1_raw.mp3 + cine_part2_raw.mp3, split near the gospel turn), prophecy/01_bethlehem/sfx/add_sfx_v6.py. Both key off audio_v3 word times; make v4 copies (mix_score_v4words.py, add_sfx_v8.py) keyed to narration_v4.words.json.

## What changed in the words (old v3 -> new v4)
- Micah intro shortened: "God's prophet Micah named a small town: Bethlehem. God promised a King from there:" then [prophet] "ruler in Israel." (same prophet clip).
- NEW: "It goes on:" (11.04) [prophet] "from everlasting." (12.22-12.9) "Bethlehem would be His birthplace, not His beginning." (13.34-16.3)
- CUT: "Mary and Joseph lived far away. A tax order sent them to Bethlehem." -> the TaxInset and the walking-route use of the MapSplash are no longer needed THERE.
- "There, God's promise came true: Jesus, the King, was born." (16.7-20.5) unchanged words.
- "Wise men came asking for this King. King Herod asked the experts." (21.28-24.9) then scribe "In Bethlehem of Judaea." (25.35)
- "Bethlehem was close by." (28.1) 1 s silence, "The Bible never says the experts went. The wise men went, and found the child." (30.68-36.5) - same as before, ~8.3 s earlier.
- NEW Galilee beat (36.72-44.6): "Jesus grew up in Galilee. Later, people argued: can the King come from Galilee? The promise said Bethlehem. He was born there."
- Gospel (44.82-52.84) and landing "Before anyone went to Him, He came to us." (53.17-55.9) unchanged words, ~0.3 s earlier.

## Picture plan (keep everything that already works; same clips, same style, same comic motion)
1. 0-4.0 hook: unchanged.
2. Micah (4.0-16.5): same prophet/town pages. Pills carry the new words. The parchment scroll strip: line 1 "ruler in Israel." on the prophet words (9.7-10.5) as now; ADD line 2 "from everlasting." written on the same strip word-timed to 12.22/12.37 in GOLD, with the "MICAH 5:2" chip. Under "Bethlehem would be His birthplace, not His beginning." hold the town panel with its dashed frame (the "promise" frame) - it turns gold later at "true:" as now. "birthplace" and "beginning" may get a gold mark in the pill.
3. Birth (16.7-20.5) -> wise men/Herod/scribe (21.3-27.9): the v6 pages and marks (CAME TRUE stamp at "true:", KING HEROD cap at "Herod", scribe balloon) re-keyed to the new word times. The whips/slams move with their words.
4. Close by / never / went (28.1-36.5): the v6 MapMid + footprints + WENT beat, re-keyed (~8.3 s earlier).
5. NEW Galilee beat (36.7-44.6): REUSE the full-page hand-drawn map (MapSplash: NAZARETH far north, JERUSALEM, BETHLEHEM south). No walkers, no tax order. On "Galilee." show a hand-lettered region label "GALILEE" near Nazareth in the north (same lettering style as the map's labels); on "can the King come from Galilee?" a big hand-drawn "?" pops over Galilee; on "The promise said Bethlehem." the camera travels south down the map to Bethlehem and its star/frame goes gold; on "He was born there." a gold flash/slam on Bethlehem. Keep the Mockers-style translucent pills for the words. Comic motion stays (one slam, one whip in/out is enough).
6. Gospel + landing + end card (44.8-end): the v6 beats re-keyed. Film length = last word end (~55.9) + at least 3.0 s hold -> about 59.0 s (1770 frames). Must stay UNDER 60 s.
- All clips still play at 1.0x, trim only (owner rule: never stretch/freeze/boomerang a clip). If a slot is now longer than its clip, use a different clip or a $0 graphic cover, never a freeze.

## Audio
- Narration track = narration_v4.mp3. Score: fit the two cinematic score parts to the new timing the same way mix_score_cine.py does (part 2 enters at the gospel turn "But Jesus came much farther", now 44.82; the end drop lands after the last word; keep the ducking under the voice). SFX: re-key add_sfx_v6.py (booms on slams, whooshes on whips; drop SFX that belonged to the cut tax/walk beat; add a soft paper/pen sound for the scroll line "from everlasting" only if one already exists in the local sound library).
- Audio and video durations must match (INV-26): run `.venv\Scripts\python.exe check_landing_hold.py` - 0 FAIL for the new file.

## Output
- _remotion/src/BethlehemV8.tsx (+ comp in Root.tsx, id BTH8), render -> prophecy/01_bethlehem/film/BETHLEHEM_FILM_v8.mp4 (picture + voice), then score + SFX -> prophecy/01_bethlehem/film/BETHLEHEM_FINAL_v5.mp4. Report duration, LUFS (target about -16), true peak.
- Check it by LOOKING: extract frames at every new/changed beat (11.5, 12.5, 14.5, 17.5, 18.2, 23.8, 25.5, 28.5, 31.0, 34.5, 37.6, 41.2, 42.8, 44.4, 47, 50, 54, 58) into prophecy/01_bethlehem/film/_v5_frames/ + one contact sheet, and Read them yourself. Check: pills never cover a face, no flash frames at cuts (check frame-to-frame brightness jumps), "from everlasting" readable on the scroll, GALILEE label spelled right, the "?" on Galilee, gold on Bethlehem, no leftover tax-order or walkers.
- A simple review page prophecy/01_bethlehem/_FINAL_v5.html (dyslexia-friendly: big video, short words) with the film and the contact sheet, plus one line "what changed".
- Final reply: the output paths, duration, LUFS, check_landing_hold result, and an honest list of anything that looks off.
