## VERDICT: FIX FIRST

The text is accurate and honest. But three blanks stop the upload (rights, release time, YouTube caption cert), and a few settings are missing.

## ISSUES

1. **Checklist, Rights line | it is blank.** This one blocks the upload. Grok Imagine and Antigravity (Google) are not image-licence services with clear terms, so check that both allow commercial use on all four platforms. Fill in the name, the date, and each tool's terms page.
2. **Checklist, Release rule | it is blank, and TikTok can only schedule about 10 days ahead.** Add: "The release moment must be no more than 10 days after the TikTok upload. Someone must be online at release to post and pin the YouTube comment."
3. **YouTube, Subtitles | the caption certification step is missing.** Add: "Caption certification: This content has never aired on TV in the US."
4. **YouTube and Meta, auto-dubbing and AI translation | not covered.** YouTube can auto-dub the film, and Meta can make an AI voice translation. Either would put new AI voices over Jesus and Job. Add: "YouTube Advanced > Automatic dubbing: OFF. Instagram/Facebook 'Translate your voice with Meta AI': OFF."
5. **captions_locked.srt, cues 6 and 7 | a bad line break splits the key phrase across two cues.** Use:
   - cue 6 (20,760–23,460): `Jesus comes "walking upon the sea,"`
   - cue 7 (23,500–26,880): `as Job said only God does.` / `He "would have passed by them."`
6. **YouTube and Facebook DESCRIPTION | the film's answer is missing.** They cite Job 9:32-33 but never say "mediator" or "daysman". These are hard words for a second-language viewer. After the 1 Timothy sentence, add: `Job said there was no "daysman betwixt us" (Job 9:33), no one to stand between God and him. The Bible later calls Jesus the "one mediator between God and men" (1 Timothy 2:5, KJV): the one who stands between.`
7. **Instagram and Facebook, remix/download | no setting.** TikTok and YouTube tie remixing to the rights line, but the Meta posts don't. Add: "Allow remix / downloads: ON only if the rights line is filled; otherwise OFF."
8. **Facebook | 'Also share to Instagram' is not covered.** Add: "Share to Instagram: OFF."
9. **Facebook title | facebook.md has no TITLE field.** The checklist sends the uploader to the YouTube section for it, which invites pasting from the wrong place. Add `## TITLE` (the same title) to facebook.md and rebuild the paste page.
10. **PUBLISH_INDEX.html | could be out of date.** Nothing proves it was built after the .md files were locked. Add: "The paste page build time must be later than every platform .md file. If not, rebuild it."
11. **Hash commands | relative paths.** Add: "Run these from the project root folder (the one that holds `visual\` and `publish\`)."
12. **Captions step | it compares captions.srt and then says upload captions_locked.srt.** That is confusing. Delete the captions.srt comparison and keep "Upload only `publish\captions_locked.srt` (UTF-8)."
13. **Thumbnails | not checked.** YouTube thumbnails must be under 2 MB, and a 1080x1920 JPG can be bigger. Check `thumb_tiktok.jpg` has the same hash as `thumb_9x16.jpg`, or only use one file.
14. **Pinned comment | reference list doesn't match.** It says "Job 9:8-11" where every other field says "Job 9:8; Job 9:11". This is minor, but make them match: `Job 9:8; 9:11; 9:32-33`.

## OWNER CALLS

- **Title:** fair, and the film pays it off ("as Job said only God does").
- **Poster:** it shows Job reaching toward Jesus as if he sees Him. The film's turn is "Job could not see Him." The poster reverses that, and viewers may think Job was there. "SO WHO IS THIS?" also echoes the storm in Mark 4:41, not Mark 6.
- **Locked words "Instead of passing by":** this frames passing by as Jesus' plan. The descriptions' "The Bible does not say why" softens it. Keep that line in every field.
- **"He has felt pain too":** Hebrews 4:15 says "infirmities" and "tempted", not "pain". It is defensible, but it is a stretch.

## MISSING UPLOAD STEPS

- Check loudness, about −14 LUFS integrated with peaks ≤ −1 dBTP, before uploading.
- TikTok Studio: run "Copyright check" before you schedule.
- TikTok on a phone: Settings > "Upload HD": ON.
- YouTube: "Allow auto-translated title/description": decide on purpose.
- Within 1 hour of release, someone replies to the first comments on all four platforms. Use a grace tone and don't argue.
- Facebook/Instagram: turn off Meta's auto-generated captions on the post itself, not just "don't upload the SRT".
- Check that YouTube shows the poster thumbnail on desktop search and the channel grid too, not only in the app.
- Record the rights checker's name in the tracker log as well.

## WHAT IS GOOD

- Every KJV quote I checked is word-for-word, the Job lines are kept separate, and "Job did not name Jesus" is stated.
- No AI wording in any public text, the brand is right everywhere, and no first line gives away the boat ending.
- The Content ID warning (video is over 1 minute) and the doubled-captions/safe-zone checks are real, sharp catches.