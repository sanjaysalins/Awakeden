## VERDICT: FIX FIRST

## ISSUES
1. `youtube_short.md` & `facebook.md` | Bible citation error: You cite `(Luke 4:25-27)` for the "foreign widow". Verse 27 is about Naaman the leper in the time of Elisha, not the widow in the time of Elijah. | `a foreign widow in the days of Elijah (Luke 4:25-26).`
2. Upload Checklist (YouTube, TikTok, Facebook) | Ghost instructions: You command the uploader "Do NOT paste the HASHTAGS block", but no `## HASHTAGS` block exists in your source markdown files. The uploader will stall looking for it. | Delete the warnings about the HASHTAGS block.
3. Upload Checklist (YouTube) | File name mismatch: You instruct the uploader to use `captions.srt`, but the actual provided file is `captions_locked.srt`. | `upload captions_locked.srt as English.`
4. Upload Checklist (TikTok) | Impossible UI action: You instruct the uploader to "post or schedule from the draft". TikTok mobile does not allow scheduling from drafts. TikTok web allows scheduling but does not support drafts. | `When released, post directly from the draft.`
5. Upload Checklist (Instagram) | Invalid platform spec: You demand a "profile-grid crop (3:4)". Instagram profile grids are 1:1, and Reel feed previews are 4:5. 3:4 is wrong for both. | `drag the profile-grid crop (1:1) up`
6. `captions_locked.srt` & Upload Checklist (YouTube) | Visual conflict: The video already has burned-in read-along words. Uploading an SRT without forcing it off creates overlapping double-text for the large percentage of users with CC enabled by default. | Explicitly warn the uploader to check CC placement or rely on burned-in text.

## MISSING UPLOAD STEPS
- **YouTube Shorts:** No step exists to link the "Related Video" to direct Short viewers to a long-form video (mentioned casually, but no actionable step).
- **Facebook Reels:** No step to explicitly ensure visibility is set to **Public** upon release. Moving from a saved draft often defaults to tighter privacy unless verified.
- **Cross-Platform:** No instruction on the release sequence. Pushing all four simultaneously without staggered timing can trigger automated cross-platform unoriginal content flags (e.g., TikTok flagging it as a YouTube re-upload).

## WHAT IS GOOD
- The copy strictly obeys the theological rule: "The Bible does not say why Jesus stopped there" is present and prevents overclaims.
- Platform constraints are nailed: TikTok and Instagram captions are well under the limits, and the YouTube title fits perfectly without spoiling the payoff.
- The KJV Scripture citations in the text blocks are highly accurate, successfully catching differences between the spoken adaptations and the literal text.