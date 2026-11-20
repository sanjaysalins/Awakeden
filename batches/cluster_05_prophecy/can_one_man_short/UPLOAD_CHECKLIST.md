# Can One Man Heal and Forgive?: upload checklist (2026-11-17, film T12 comic v3 final)

Paste ONLY from `publish/PUBLISH_INDEX.html`. The old draft `upload_kit.md` is archived and must not be used.
**Release rule:** Keep every platform private/draft until the owner records the release date, time and time zone here: **2026-11-20 (owner, "today")** - time: the moment you post; use that SAME moment on all four.

## Before uploading (all platforms)
- [ ] File: `visual/can_one_man_final.mp4` (1080x1920, 30 fps, 69.7 s, sha256 c88b71ae03ce552e454931d891e566597c97de210795e9e6e589630ed6854cad). Check the sha256 against `FINAL_VIDEO.txt`.
- [ ] Thumbnails: `thumbs/thumb_16x9.jpg` and `thumbs/thumb_1x1.jpg` are NOT for upload on any platform. Only the 9:16 poster is used (`thumbs/thumb_9x16.jpg`, or `thumbs/thumb_tiktok.jpg` for TikTok).
- [ ] Confirm you hold the rights or licence for the score, voices and sound effects on all four platforms (no copyright claim after processing).
- [ ] Play it through once on a phone. Check the last frame, the hold and the sound.
- [ ] The video already has on-screen read-along words. Leave the platform's AUTO-captions OFF wherever they would be burned on top.

## YouTube (Short)
- [ ] Before upload: compare `publish/captions.srt` and `publish/captions_locked.srt` byte for byte (`cmp`). If they differ, stop and copy the locked file over.
- [ ] Visibility: **PRIVATE** until the release rule at the top is filled in. At release, use YouTube's **Schedule** option (not a manual Private-to-Public flip).
- [ ] Title, description and tags from the paste page. Tags go in the TAGS field, not the description. Do NOT paste the HASHTAGS block (the hashtags are already in the description).
- [ ] Audience: **Not made for kids**. Age restriction: none. Paid promotion: no.
- [ ] Altered or synthetic content: **YES** (the platform switch only, never in the text).
- [ ] Category: Education. Licence: Standard YouTube.
- [ ] Video language: English. Title and description language: English.
- [ ] Subtitles: upload `publish/captions_locked.srt` (same content as `captions.srt`) as English. Do not use any other SRT. Viewers turn them on with CC.
- [ ] Thumbnail: upload `thumbs/thumb_9x16.jpg` in YouTube Studio if offered. If not, use the opening hook frame (first 2 s). Never the end card.
- [ ] Playlist: the Bible prophecy series playlist (same one as Bethlehem, Immanuel and Nazareth) (create it once).
- [ ] After processing (still PRIVATE): open the Checks / Copyright tab. This Short is over 1 minute, so any Content ID claim can block it in some countries. Resolve every claim before scheduling.
- [ ] Shorts remixing: allow. Comments: on, hold potentially inappropriate for review.
- [ ] Links in Shorts descriptions are not clickable. Set the channel link and the Related video link if wanted.

## TikTok
- [ ] Caption from the paste page. Hashtags are already in the caption, so do NOT paste the HASHTAGS block a second time.
- [ ] Cover: upload `thumbs/thumb_tiktok.jpg`, or pick the hook frame.
- [ ] **AI-generated content: ON.**
- [ ] Duet: on. Stitch: on. Download: on. Branded content: OFF.
- [ ] **Save as Draft.** The draft lives on that one phone only: do not log out, reinstall or switch phones. When released, post from the draft on the same phone.

## Instagram (Reel)
- [ ] Caption from the paste page. Hashtags are already in the caption.
- [ ] **Hold:** Save as Draft until the release rule at the top is filled in.
- [ ] Cover: upload `thumbs/thumb_9x16.jpg`. Then **drag the profile-grid crop (3:4) up** so "ONLY GOD / CAN FORGIVE" both show.
- [ ] **Add AI label: ON.**
- [ ] "Also share to Facebook": **OFF**. Facebook gets its own post.
- [ ] Share to feed: on. Alt text: "Comic-book short about Jesus forgiving and healing a man who could not walk (Mark 2:1-12), and a warning in Isaiah 6:10 and Mark 4:12."
- [ ] Captions: Instagram has no SRT upload. Leave auto-captions OFF, because the words are already on screen.

## Facebook (Reel)
- [ ] Reels have no title field. The description first line carries the hook. Paste the DESCRIPTION block only; do NOT paste any HASHTAGS block (hashtags are already in the description).
- [ ] **Hold:** Save as Draft until the release rule at the top is filled in.
- [ ] Description from the paste page. Cover: `thumbs/thumb_9x16.jpg`.
- [ ] **AI label: ON** (Meta switch).
- [ ] Captions: do NOT upload the SRT (it can show on top of the burned-in words). YouTube keeps the SRT upload (captions are off by default; viewers opt in).

## After release
- [ ] Private videos cannot take comments: right after the video goes public, post and pin this comment on YouTube:
  > Isaiah 6:10 ends "be healed." In Mark 4:12, Jesus gives the same warning and it ends "their sins should be forgiven them." (Matthew 13:15 has "heal them"; the Bible does not say why the words differ.) In Mark 2, Jesus says "Son, thy sins be forgiven thee" before He tells the man to get up (Mark 2:5-11). In the synagogue Jesus read that He was sent "to heal the brokenhearted" (Luke 4:18). Which do you think was the bigger gift? Read it: Isaiah 6:9-10; Mark 4:11-12; Matthew 13:13-15; Mark 2:1-12; Luke 4:18.

- [ ] After each post is live, open it on a phone: check the first line before "more", the cover crop, and that no doubled captions show.

## After posting
- [ ] Log every URL: `.venv\Scripts\python.exe upload_tracker.py --set can_one_man_short <platform> <url>`.
- [ ] Read the 48-hour retention, and ask 3-5 real seed viewers for feedback.
