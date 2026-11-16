# Nazareth: upload checklist (2026-11-16, film FINAL v2 / words v7)

Paste ONLY from `publish/PUBLISH_INDEX.html`. The old draft `upload_kit.md` is archived and must not be used.
**Release rule:** Keep every platform private/draft until the owner records the release date, time and time zone here: ______.

## Before uploading (all platforms)
- [ ] File: `visual/nazareth_final.mp4` (1080x1920, 30 fps, 59.9 s, film FINAL v2, sha256 410a5b6822d17d9eb96941925ec067471ac514b73aa2546bf326a2abcd4dffe8). Check the sha256 against `FINAL_VIDEO.txt`.
- [ ] Thumbnails: `thumbs/thumb_16x9.jpg` and `thumbs/thumb_1x1.jpg` are NOT for upload on any platform. Only the 9:16 poster is used (`thumbs/thumb_9x16.jpg`, or `thumbs/thumb_tiktok.jpg` for TikTok).
- [ ] Confirm you hold the rights or licence for the score, voices and sound effects on all four platforms (no copyright claim after processing).
- [ ] Play it through once on a phone. Check the last frame, the hold and the sound.
- [ ] The video already has on-screen read-along words. Leave the platform's AUTO-captions OFF wherever they would be burned on top.

## YouTube (Short)
- [ ] Visibility: **PRIVATE** until the release rule at the top is filled in. At release, use YouTube's **Schedule** option (not a manual Private-to-Public flip).
- [ ] Title, description and tags from the paste page. Tags go in the TAGS field, not the description. Do NOT paste the HASHTAGS block (the hashtags are already in the description).
- [ ] Audience: **Not made for kids**. Age restriction: none. Paid promotion: no.
- [ ] Altered or synthetic content: **YES** (the platform switch only, never in the text).
- [ ] Category: Education. Licence: Standard YouTube.
- [ ] Video language: English. Title and description language: English.
- [ ] Subtitles: upload `publish/captions_locked.srt` (same content as `captions.srt`) as English. Do not use any other SRT. Viewers turn them on with CC.
- [ ] Thumbnail: upload `thumbs/thumb_9x16.jpg` in YouTube Studio if offered. If not, use the opening hook frame (first 2 s). Never the end card.
- [ ] Playlist: the Bible prophecy series playlist (same one as Bethlehem and Immanuel) (create it once).
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
- [ ] Cover: upload `thumbs/thumb_9x16.jpg`. Then **drag the profile-grid crop (3:4) up** so "THE LINE / HE LEFT UNREAD" both show.
- [ ] **Add AI label: ON.**
- [ ] "Also share to Facebook": **OFF**. Facebook gets its own post.
- [ ] Share to feed: on. Alt text: "Comic-book short about Jesus reading Isaiah 61 in Nazareth (Luke 4:16-30)."
- [ ] Captions: Instagram has no SRT upload. Leave auto-captions OFF, because the words are already on screen.

## Facebook (Reel)
- [ ] Reels have no title field. The description first line carries the hook. Paste the DESCRIPTION block only; do NOT paste any HASHTAGS block (hashtags are already in the description).
- [ ] **Hold:** Save as Draft until the release rule at the top is filled in.
- [ ] Description from the paste page. Cover: `thumbs/thumb_9x16.jpg`.
- [ ] **AI label: ON** (Meta switch).
- [ ] Captions: do NOT upload the SRT (it can show on top of the burned-in words). YouTube keeps the SRT upload (captions are off by default; viewers opt in).

## After release
- [ ] Private videos cannot take comments: right after the video goes public, post and pin this comment on YouTube:
  > Luke 4:19 stops at "the acceptable year of the Lord." The sentence in Isaiah 61:2 goes on: "and the day of vengeance of our God." The Bible does not say why Jesus stopped there. He told the room, "This day is this scripture fulfilled in your ears" (Luke 4:21). Later, at the cross, the rulers dared Him with different words but the same challenge: "He saved others; let him save himself" (Luke 23:35). Which part of this story stands out to you most? Read it: Isaiah 61:1-2; Luke 4:16-30; Luke 23:35; 1 Corinthians 15:3-4.

- [ ] After each post is live, open it on a phone: check the first line before "more", the cover crop, and that no doubled captions show.

## After posting
- [ ] Log every URL: `.venv\Scripts\python.exe upload_tracker.py --set nazareth_short <platform> <url>`.
- [ ] Read the 48-hour retention, and ask 3-5 real seed viewers for feedback.
