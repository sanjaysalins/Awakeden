# Born in Bethlehem: upload checklist (red team r2, 2026-11-15; updated 2026-11-16 for film v6 / words v4.1)

Paste ONLY from `publish/PUBLISH_INDEX.html`. The old draft `upload_kit.md` is archived and must not be used.
**Release rule:** Keep every platform private/draft until the owner records the release date, time and time zone here: ______.

## Before uploading (all platforms)
- [ ] File: `visual/bethlehem_final.mp4` (1080x1920, 30 fps, 59.4 s, film v6, sha256 f1ac7b19e61119161dcfb4c46a5570f34f4f17deb3a0350e13995b649b24fa20). Check the sha256 against `FINAL_VIDEO.txt`.
- [ ] Thumbnails: `thumbs/thumb_16x9.jpg` and `thumbs/thumb_1x1.jpg` are NOT for upload on any platform. Only the 9:16 poster is used (`thumbs/thumb_9x16.jpg`, or `thumbs/thumb_tiktok.jpg` for TikTok).
- [ ] Play it through once on a phone. Check the last frame, the hold and the sound.
- [ ] The video already has on-screen read-along words. Leave the platform's AUTO-captions OFF wherever they would be burned on top.

## YouTube (Short)
- [ ] Visibility: **PRIVATE** until the release rule at the top is filled in.
- [ ] Title, description and tags from the paste page. Tags go in the TAGS field, not the description. Do NOT paste the HASHTAGS block (the hashtags are already in the description).
- [ ] Audience: **Not made for kids**. Age restriction: none. Paid promotion: no.
- [ ] Altered or synthetic content: **YES** (the platform switch only, never in the text).
- [ ] Category: Education. Licence: Standard YouTube.
- [ ] Video language: English. Title and description language: English.
- [ ] Subtitles: upload `captions.srt` as English. Viewers turn them on with CC.
- [ ] Thumbnail: upload `thumbs/thumb_9x16.jpg` in YouTube Studio if offered. If not, use the "DID THEY GO?" hook frame at about 3.4 s. Never the end card.
- [ ] Playlist: the Bible prophecy series playlist (create it once).
- [ ] Shorts remixing: allow. Comments: on, hold potentially inappropriate for review.
- [ ] Links in Shorts descriptions are not clickable. Set the channel link and the Related video link if wanted.

## TikTok
- [ ] Caption from the paste page. Hashtags are already in the caption, so do NOT paste the HASHTAGS block a second time.
- [ ] Cover: upload `thumbs/thumb_tiktok.jpg`, or pick the hook frame.
- [ ] **AI-generated content: ON.**
- [ ] Duet: on. Stitch: on. Download: on. Branded content: OFF.
- [ ] **Save as Draft** (do not post as Only me: a private-then-public post can lose its first push). When released, post or schedule from the draft.

## Instagram (Reel)
- [ ] Caption from the paste page. Hashtags are already in the caption.
- [ ] **Hold:** Save as Draft until the release rule at the top is filled in.
- [ ] Cover: upload `thumbs/thumb_9x16.jpg`. Then **drag the profile-grid crop (3:4) up** so "EXPERTS KNEW / DID THEY GO?" both show.
- [ ] **Add AI label: ON.**
- [ ] "Also share to Facebook": **OFF**. Facebook gets its own post.
- [ ] Share to feed: on. Alt text: "Comic-book short about Micah 5:2 and Jesus born in Bethlehem."
- [ ] Captions: Instagram has no SRT upload. Leave auto-captions OFF, because the words are already on screen.

## Facebook (Reel)
- [ ] Reels have no title field. The description's first line already asks the title question. Paste the DESCRIPTION block only; do NOT paste any HASHTAGS block (hashtags are already in the description).
- [ ] **Hold:** Save as Draft until the release rule at the top is filled in.
- [ ] Description from the paste page. Cover: `thumbs/thumb_9x16.jpg`.
- [ ] **AI label: ON** (Meta switch).
- [ ] Captions: do NOT upload the SRT (it can show on top of the burned-in words). YouTube keeps the SRT upload (captions are off by default; viewers opt in).

## After release
- [ ] Private videos cannot take comments: right after the video goes public, post and pin this comment on YouTube:
  > Micah pointed to Bethlehem about 700 years before Jesus was born, and added "from of old, from everlasting." Christians read it this way: Bethlehem was His birthplace, not His beginning (John 6:38). The Bible does not say whether the experts went. The wise men went, and so did the shepherds (Luke 2:15-16). Some people argued among themselves about where the Christ would come from (John 7:41-43). What surprised you more: how old the promise was, or that Jesus came down from heaven to us? Read it: Micah 5:2; Matthew 2:1-11; Luke 2:4-7; Luke 2:15-16; Luke 2:39; John 7:41-43; John 6:38; 1 Corinthians 15:3-4.

## After posting
- [ ] Log every URL: `.venv\Scripts\python.exe upload_tracker.py --set bethlehem_short <platform> <url>`.
- [ ] Read the 48-hour retention, and ask 3-5 real seed viewers for feedback.
