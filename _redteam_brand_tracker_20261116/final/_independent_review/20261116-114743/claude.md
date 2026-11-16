# Independent review — claude (OK, 217s)

**Review of the YouTube upload tracker: REVISE**

The core works. Only YouTube is tracked. Hide/Unhide works and saves in the browser. There are no Awakeden words on the page. Episode 12 is correctly blocked. Episode 17 (no finished film) does not show. The 14 posted items all match the two link files.

But there are some real defects.

**1. Swirls episodes reach "Next up" with no ready check**
- Main pieces must pass a ready check first (`pipeline/release_state.py:349`).
- Swirls cards do not. Any Swirls folder with an `episode.py` and no YouTube link goes straight into "Next up" (`build_upload_tracker.py:422-437`). It does not check for a GREEN pack, a locked film, or the owner's OK.
- So the 8 Swirls cards there now (Jacob's Ladder pilot, ep02, 06, 07, 08, 10, 11, 13) are "ready" only because nothing failed.
- Pilot risk: Jacob's Ladder now points to a rewrite film (`poc_living_sketchbook/_rewrite_v4/panel_jl/video/jacobs_ladder_v3_sfx.mp4`). Your notes say the old pilot shipped with the dropped-filter bug. Nothing confirms this rewrite fixes it.
- Ep06 Talitha Cumi: its `FINAL_VIDEO.txt` is new and not yet saved in git.
- **Fix:** let a Swirls card into "Next up" only if its pack passed and its film is locked. Otherwise send it to "Finished but blocked" with the reason.

**2. The Swirls link command writes bad data with no checks** (`poc_living_water_ink_style_test/swirls_upload_tracker.py:230-242`)
- It does not check that the link is a YouTube link. Any text gets saved.
- It does not check the episode name. A typo saves a fake entry, and the real card stays in "Next up".
- It silently replaces an old link. The main command blocks that unless you add `--repost` (`upload_tracker.py:82-94`).
- It does not save the video's fingerprint, so a changed file after posting can't be caught.
- Any extra word in the command crashes it.
- **Fix:** reuse `upload_tracker.video_id()`, check the name against the found episodes, and add the same `--repost` guard.

**3. After you paste a link, the page does not update**
- Step 3 says run the command, and step 4 says run `release_check.py`. Neither rebuilds the tracker page.
- The Swirls command rebuilds only its own separate page (`_SWIRLS_UPLOAD_TRACKER.html`).
- So the card you just posted stays in "Next up" until you re-run `build_upload_tracker.py` yourself. You could post it twice.
- **Fix:** make both commands rebuild the tracker at the end, or add a step 5 "rebuild the page".

**4. "Today in Paradise" shows as #1 to post, but a 38-second cut of it is already live**
- `today-in-paradise` is #1 "Wk2 Fri - LAUNCH". `today-in-paradise-38s` is already posted (`youtube_id` WDZS5VvbGrs, 2026-11-14).
- Same story, same verse, same launch slot. Posting #1 would put up a near-copy.
- **Fix:** mark it "already covered by the 38s cut" or move it down, and ask the owner.

**5. The "publish pack" links still show TikTok, Facebook and Instagram**
- All 30 packs I checked have these 3 extra cards, and the folders still hold `tiktok.md`, `facebook.md` and `instagram.md`.
- The tracker's step 1 sends the owner into each pack, so they still see 4 platforms.
- **Fix:** rebuild the packs as YouTube only, or hide those cards.

**6. "SPARE BANK" items look ready when they are not**
- Items #20-24 say "style-check first", but they sit in "Next up" with a live COPY button.
- 9 items are just "unscheduled" (#25-33). One is `bronze-serpent-01-look-and-live`, while its siblings 02 and 03 are scheduled.
- Swirls cards have no number at all.
- **Fix:** put the spare bank in its own "check first" section. Give Swirls and unscheduled items a number or a clear "pick a slot" note.

**7. Old platform words are left in the code**
- `upload_tracker.py:14`: the help example still shows `tiktok https://www.tiktok.com/@awakeden/...`. That is an Awakeden reference in a tool the page copies.
- `upload_tracker.py:32`: a comment still lists all 4 platforms.
- `pipeline/release_state.py:28,31`: `PLATFORMS` still has all 4, and the comment "PLATFORMS stays the list --set accepts" is false now, since `--set` rejects them.
- `build_upload_tracker.py:5`: the header still says "all four thumbnails, read page… updates the website manifest + read pages".
- `build_upload_tracker.py:74`: the thumbnail search still looks for a `tiktok` file.
- **Fix:** remove them all and reduce the list to YouTube only.

**8. Smaller points**
- **Wording a dyslexic owner will stumble on:** the pinned film's label reads "v5 hook-fixed (PINNED final; old pin in FINAL_VIDEO.txt.prev_v4)", with "cards: VERILY=TRULY" next to it (`build_upload_tracker.py:115`). The episode block says "mark it studio_complete in the manifest first" (`:240`). Both are internal jargon.
- **The page writes files while it builds:** building the tracker can silently rewrite `FINAL_VIDEO.txt` pins (`swirls_upload_tracker.py:107`). A film pinned by hand could be overwritten just by refreshing the page.
- **One "AI" word stays, on purpose:** "Altered content / AI disclosure" (`build_upload_tracker.py:46`). That is YouTube's own setting name, so it is correct. Say so in the code, so the no-AI-wording sweep does not "fix" it.
- **Hide only works in one browser:** it is saved in that browser only, so hidden cards come back in another browser or a private window. Fine as designed, but say so on the page.
- **Leftover code:** `ep_todo` and `_group_by_episode([], …)` in `main()` do nothing.

VERDICT: REVISE
TOP FIXES:
1. Check Swirls episodes before "Next up": only a passed pack plus a locked film gets in; send the rest to "Finished but blocked" with the reason (Jacob's Ladder pilot and ep06 need checking).
2. Harden the Swirls link command (YouTube link check, episode-name check, `--repost` guard, save the fingerprint), and rebuild the tracker after every link is saved, so posted cards leave "Next up".
3. Take `today-in-paradise` out of #1 (the 38s cut already covers it), put the spare bank in its own "check first" section, and remove all TikTok/Facebook/Instagram and Awakeden traces from the code and the packs.
