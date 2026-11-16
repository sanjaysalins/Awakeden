# Final red-team pack: YouTube upload tracker (2026-11-16)

## What the owner asked, in order (verbatim)
1. "from now on just track youtube links"
2. "if the links are there, have a mechanism for me to hide them or unhide them"
3. "remove any reference in the publication of any locked episode any reference to AI"
4. "we no longer supporting awakeen, so remove all of their reference completely" (brand is now Salt and Light Kingdom; old website retired; already-posted YouTube videos left as they are)
5. About Swirls of Life episodes held by an old 30-episode rule: "oh if they are ready, we should start looking at posting them already"

Owner is dyslexic: the page must be simple, short words, easy to act on.

## Your job
Find REAL defects in the tracker page and the code that builds it and logs links: wrong counts, wrong section, a ready item missing or a not-ready item shown as ready, a posted item shown as to-post, broken buttons/JS, commands that would write bad data, leftover TikTok/Facebook/Instagram or Awakeden or AI wording, confusing wording for the owner. File + line + why + fix. No praise. End with VERDICT: PASS | REVISE | FAIL.

## Files to read in the repo (F:\slk\PycharmProjects\JesusInTheBible)
- build_upload_tracker.py (builds the page)
- _UPLOAD_TRACKER.html (the built page)
- upload_tracker.py and poc_living_water_ink_style_test/swirls_upload_tracker.py (the two logging commands the page copies)
- pipeline/release_state.py (queue logic), data/release_ledger.json, poc_living_water_ink_style_test/_swirls_release_ledger.json
