# ELEVATE (Comic lane) - handover + resume. Written 2026-11-09 night (supersedes the 2026-11-08 version).

Lane: comic (Higgsfield). Worker brief: `F:\slk\PycharmProjects\JesusInTheBible\coord\LANE_COMIC.md`.
Owner is dyslexic: short plain words, ONE question at the end, full absolute paths + `file:///` links, NEVER auto-open anything. Gentle mode is ON (`C:\Users\sanjay\.claude\.gentle-state` = 3): one heavy job at a time, ffmpeg `-threads 2`, BelowNormal priority.
Standing owner rules: nothing paid without a quoted price + the owner's own separate yes (a pick locks WORDS only); blind panels always include a Fable seat + AI seats; the 4 questions on every pick page (who for / take-away / curiosity gap / global audience); NO media to GitHub (text/code/json/html only); no AI/method wording in public text.

## STATE: Barabbas short is FINISHED, LOCKED (A5) and upload-ready. Not uploaded. Not committed.
Piece: `F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_01_cross\barabbas_short\` (slug `barabbas-son-of-the-father`, series Words from the Cross, ref Matthew 27:15-26).
- **Final film:** `...\barabbas_short\visual\barabbas_short_A5_animated.mp4` (41.6 s, audio=video, 3.08 s landing hold). `FINAL_VIDEO.txt` points at it. `LOCKED.json` has its sha256 (re-locked after the red team, owner yes each time).
- **Words v4 (locked):** `poc_comic_page\_ELEVATE\short_barabbas\FINAL_WORDS.md`. Angle = the NAME: "In Aramaic, Barabbas means son of the father" -> Jesus said "Abba" (Mark 14:36) -> last line "Barabbas only had the name. Jesus died so we could call God Father too." (tag GALATIANS 4:5-6). Matt 27:25 never used; no group blamed. Took 3 blind rounds: rounds 1-2 felt "tired, heard it before" (owner), the fresh-detail angle fixed it.
- **Audio:** `...\barabbas_short\audio\narration.mp3` (38.52 s; voices narrator / pilate / crowd). v1 backup `narration_v1_backup.mp3`. Mix = score + crowd + door + choir, sidechain-ducked (built in `build_barabbas.py`, file `poc_comic_page\_ELEVATE\work\barabbas\mix_v2.m4a`). **The sound mix has NEVER been heard by Claude or (as far as noted) the owner. Ask for an ear-check.**
- **Picture:** owner's idea = 3-panel manga grid still (nano_banana_2 9:16, character ref via --image-references) animated 10 s with `gemini_omni_flash_1_2` image-to-video (22.5 cr/10 s, 11.25/5 s, 9/4 s at 720p). 4 grid clips (`visual\grids\a1..a4.mp4`, stills g1..g4) + 6 "moment" clips replacing slideshow stretches (`visual\moments\c1-c3, d1-d3`). Owner verdict on animated grids: "absolutely great".
- **Builder:** `poc_comic_page\_ELEVATE\build_barabbas.py` (`.venv\Scripts\python.exe poc_comic_page/_ELEVATE/build_barabbas.py A5`). Versions A..A4 + B are STALE vs the new narration timing (only A5 matches). B (pan-only control) was built from the first 4 grids with the OLD audio/lettering: if the A/B audience test is wanted, rebuild B for the new timing ($0).
- **Pack:** `...\barabbas_short\publish\` GREEN (0 fail, 0 warn): youtube_short/tiktok/facebook/instagram .md, captions.srt (aligned to the new audio), PUBLISH_INDEX.html, thumbs 16x9/9x16/1x1/tiktok (title SON OF THE FATHER? / MATTHEW 27). Title: `In Aramaic, Barabbas means "son of the father": look who went free`. Hashtags #Barabbas #Jesus #BibleStory #Gospel #Matthew27. Catalogue entry in `_website\manifest.yaml`; `_UPLOAD_TRACKER.html` rebuilt; `release_check.py` GREEN (83 items, 0 FAIL); `check_landing_hold.py` 0 FAIL.
- **Review pages (never auto-opened):** `...\barabbas_short\visual\_BARABBAS_AB.html` (older A4 vs A3 page, update to A5 if wanted), `...\barabbas_short\red_team\_RED_TEAM_BARABBAS.html`, `...\barabbas_short\publish\PUBLISH_INDEX.html`, `F:\slk\PycharmProjects\JesusInTheBible\_UPLOAD_TRACKER.html`.

## Red team (3 blind seats, Fable + Opus + Sonnet, film-only pack in `...\barabbas_short\red_team\pack\`): all REVISE
Fixed: Japanese-looking sky marks in the crowd clip (cut around them), tag Matt 27:22 -> 27:23, break-out burst moved to "So the robber went free", film now ends on Jesus with the cross (hand just before), clean tall thumbs, "In Aramaic" hedge (card, narration, copy), "Pilate knew", clearer last line + Galatians tag, #Easter -> #Gospel.
NOT fixed (owner choice): flame aura (owner's style); carried cross beam reads like an X (an upright cross picture would be ~$0.70, optional); faint ghost Jesus in the first-3-seconds grid overview (minor); two seats wanted an AI-disclosure line (left out per the owner's no-AI-wording rule); Pilate-pointing beat is slowed/held so it is calm and near-still.

## SPEND (all owner-approved with quoted prices; ledger rows `est_only`; the auto hook under-counts, corrective rows added)
Manga page test 0.30; grid test 1.23; A/B POC grids+clips ~3.78 + clip 4 1.13; moments 1.86; moments 2 1.76; voice 0.09 + re-record 0.04. **Total ~$8.55.** Higgsfield credit balance is SHARED with other sessions (it ran out once; owner topped up to ~502; last seen ~381 on 2026-11-09 night). Check `~/bin/hf.exe account status` first.

## RESUME TOMORROW (needs owner)
1. Owner watches `barabbas_short_A5_animated.mp4` and LISTENS to the sound (nobody has heard it). Fix anything by ear (free).
2. Owner uploads and sends links; record with `.venv\Scripts\python.exe upload_tracker.py --set barabbas-son-of-the-father <youtube|tiktok|facebook|instagram> <url>`.
3. Commit/push only when the owner says so. TEXT ONLY: before committing run `git diff --cached --name-only` and unstage any mp4/mp3/wav/png/jpg/gif/webm/mov; never `git add -f` media. Stage by explicit path.
4. Optional free/cheap: update `_BARABBAS_AB.html` to A5; rebuild B for the A/B audience test; upright cross picture (~$0.70, needs a yes); hide the opening ghost Jesus.
5. A/B audience test plan (owner approved the idea): same Barabbas film animated (A5) vs pan-only (B), post alternately on YouTube Shorts/TikTok; watch 3-second hold, average % watched, shares; odds with error bars; seed viewers matter more than the words.
6. Next story ideas already proposed (none started): "Jesus wept" John 11:35, Zacchaeus Luke 19. Rule: find a FRESH true detail first (the Barabbas lesson), words before money, 4 questions, blind panel with Fable.
7. Owner's two master prompts exist only in the conversation: (a) one-page manga prompt template; (b) 3-step pipeline = 3x1 grid still (nano_banana_2 9:16) -> 10 s image-to-video pan -> voice/SFX script. The grid pipeline is now the proven comic format.
8. Coordinator housekeeping: `barabbas_short` and `today_paradise_short32` are not on `coord/BOARD.json` (only the coordinator adds); leave a note via `coord.py note comic "..."`.

## Earlier work in this lane (done, kept for context)
- 2026-11-09 earlier: comic ELEVATE bake-offs 1+2 done ($0); Mockers-style translucent pill lettering won on 2 episodes (`_BAKEOFF_1_RESULT.html`, `_BAKEOFF_2_RESULT.html`); Today in Paradise 38 s short built, locked, in catalogue/tracker, commit 76532a5 pushed (no media). Thirty Pieces already uploaded by owner: stop work on it.
- 2026-11-08: diagnosis (4 blind seats), 10-step new-episode recipe, bake-off design (`_ELEVATE_DIAGNOSIS.html`, `_NEW_EPISODE_AND_BAKEOFF.html`).
