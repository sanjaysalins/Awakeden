## VERDICT: FIX FIRST

No Bible error and no rule break found in the public text. Six small fixes, all text or checklist. Nothing needs a re-render.

## ISSUES (most serious first)

1. **captions_locked.srt, cues 6-7 | The break makes a false claim for 2.7 s.** Cue 6 reads: `Jesus comes "walking upon the sea," as Job said`. Alone on screen, that says Job foretold Jesus walking on the sea. This is the exact error the pack denies elsewhere. Replace (re-time the split from the word alignment, at the start of "as"):
   - Cue 6: `Jesus comes` / `"walking upon the sea,"`
   - Cue 7: `as Job said only God does.` / `He "would have passed by them."`

2. **youtube_short.md + facebook.md, DESCRIPTION | Film's Job lines look like KJV.** The film and captions put "He goes past me, and I do not see Him." in quote marks. The description ends "Scripture quotations: King James Version (KJV)." A pastor will check and find the words are not KJV. Replace the last line with: `Scripture quotations here: King James Version (KJV). In the film, Job's two lines are said in plain modern English.`

3. **captions_locked.srt, cues 2, 3, 10, 18 | No speaker labels.** Three voices, and a deaf or sound-off viewer cannot tell who speaks. "It is I" could read as Job. Add labels (labels do not change the locked words): cue 2 `[Job] "He goes past me,`, cue 10 and cue 18 `[Jesus] "It is I; be not afraid."`

4. **Checklist, section 4 alt text vs line 1 | Rule contradiction.** Line 1 says the paste page is the ONLY paste source. The Instagram alt text lives only in the checklist. Either add an ALT_TEXT field to instagram.md and rebuild the page, or change line 1 to: `Paste ONLY from PUBLISH_INDEX.html. One exception: the Instagram alt text in section 4.`

5. **Checklist, section 1 | No check that the paste page is fresh.** PUBLISH_INDEX.html is built from the four files. If a file was edited after the build, the uploader pastes old text. Add: `Open PUBLISH_INDEX.html. The YouTube TITLE must read exactly "Jesus Walks on Water. Job Said Only God Does." and the first description line must start "Long ago, a man named Job". If not, rebuild and STOP.`

6. **Checklist, section 1 hash commands | Relative paths.** `visual\job_sea_final.mp4` fails or hits the wrong file if PowerShell is in another folder. Add first: `cd F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_05_prophecy\job_sea_short`

7. **Checklist, section 2 Thumbnail | Route not decided.** Shorts take no uploaded image, only a frame, and the frame picker is in the phone app. A desktop upload may leave an auto-picked frame (possibly the end hold). Replace with: `Upload this Short from the YouTube phone app, or edit the thumbnail in the phone app right after a desktop upload. Pick a frame from the first 2 s (Job on the rock). The poster cannot be used on YouTube. Check the saved result before scheduling.` (I could not verify today's app behaviour. Test it on the private upload.)

8. **youtube_short.md + facebook.md, paragraph 2 | ESL.** "Lo, he goeth by me" has no plain gloss, but "treadeth" does. Replace with: `"Lo, he goeth by me, and I see him not." (Job 9:11, KJV: He goes past me, and I do not see Him.)`

9. **PINNED_COMMENT | Citation style differs.** "Job 9:8-11, 9:32-33" vs "Job 9:8; Job 9:11; Job 9:32-33" everywhere else. Replace the end with: `Read it: Job 9:8; Job 9:11; Job 9:32-33; Mark 6:45-51; 1 Timothy 2:5; Hebrews 4:15.`

10. **youtube_short.md TAGS | Over-promise.** "job in the bible explained" is not paid off by a 67 s short. Replace with: `job 9 8 meaning`.

11. **Checklist, sections 4-5 | AI label in Meta Business Suite.** The label switch may not show in the Business Suite scheduler. Add: `If the AI label switch is not shown, do not schedule there. Post from the app, where the switch exists.`

12. **Checklist, section 3 TikTok | Scheduled posts.** Add: `A scheduled TikTok may not be editable. Read the caption once more before you press Schedule.` Also add the cover crop check: `Check both poster lines show in the profile-grid crop.`

## OWNER CALLS (locked; notes only)

- **Title:** honest, and fully paid off. Risk: a newcomer may read "Job" as work. The first description line ("a man named Job") repairs it, the title alone does not.
- **Poster:** Job was not at the sea. The film says "Long after", so the poster is an idea, not a lie, but a sharp critic can call it misleading. Also: painted colour poster vs sepia ink film is a look mismatch. And the poster cannot show on YouTube Shorts at all.

## MISSING UPLOAD STEPS

- Confirm the logged-in account on all four is **Salt and Light Kingdom** before upload (the channel is shared with other work).
- YouTube: set automatic dubbing ON or OFF on purpose (auto-dub will re-voice the KJV lines).
- Write the release time in each platform's own time zone setting; check each scheduler shows the same moment.
- Rights line: add KJV (Crown rights apply in the UK; short quotes are normally allowed). Record the check.
- A rollback line: if an error is found after release, fix text in place; never delete and re-upload without the owner.
- Record which phone holds the TikTok/Instagram drafts.

## WHAT IS GOOD

- Every KJV quote in the paste text is word-for-word, and "The Bible does not say why" is stated on every platform.
- "Job did not name Jesus" is in every description and the pinned comment. No AI wording, no pressure, no spoiler in line one, correct brand.
- The checklist has real stop gates: file hash, Content ID over 1 minute, private until scheduled, doubled-caption checks.
