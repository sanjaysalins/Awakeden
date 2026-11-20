"""Build the blind red-team PROMPT.md for the T13 publish pack from the real pack files."""
from pathlib import Path

D = Path(__file__).resolve().parent
P = D.parent.parent  # job_sea_short
pub = P / "publish"

HEAD = """You are ONE independent red-team seat (you have not seen any other seat or any earlier review). Be hostile, specific and honest; no flattery. Use only what is below. Do not ask questions. Do not use tools. Output text only.

JOB: red-team the full PUBLICATION + UPLOAD for a finished 67.3-second vertical Bible short before it goes live on YouTube Shorts, TikTok, Instagram Reels and Facebook. The uploader will paste the text below and follow the checklist below. The poster and the title are LOCKED by the owner (judge them, but put any poster or title note under a separate heading OWNER CALLS, not in ISSUES). Find everything that is wrong, risky, inconsistent, weak, missing or against the rules.

CHECK:
1. Bible accuracy: every claim and quote vs the KJV text below; KJV quotes word-for-word. Job 9:8 says God "alone ... treadeth upon the waves of the sea". Mark 6:48 says Jesus "would have passed by them" and the Bible does NOT say why: any text that gives a reason, or says He walked past / ignored / abandoned them, is an error. Job did not name or foretell Jesus; he described what only God does. "He has felt pain too" in the film is backed by Hebrews 4:15 only. The film's two Job lines are plain-English renderings (owner choice), not KJV quotes; copy that quotes Job must use the KJV wording.
2. Honesty: no clickbait; title + thumbnail + text must be paid off by the video. Does the title "Jesus Walks on Water. Job Said Only God Does." fairly describe what the film shows? Does the poster "MAN ON THE SEA / SO WHO IS THIS?" (old Job on a rock watching Jesus walk on the sea toward a boat; Job was not there historically, it is a poster idea) mislead?
3. Consistency: title, thumbnail, descriptions, captions, pinned comment, tags and checklist agree with each other and with the video's locked words.
4. Global audience: plain words for English-second-language viewers; a total newcomer with no Bible knowledge (does "Job" read as a person?).
5. Platform fit, per platform: hard limits and best practice (title/caption/description lengths, what shows before "more", hashtag count/order/placement, tags, links, Shorts/Reels specifics, custom thumbnail/cover, captions upload).
6. Upload settings: are the checklist settings right and complete for each platform? What is missing?
7. Owner rules: NO AI wording anywhere in public text (disclosure ONLY with each platform's own switch); the scripture range shown must cover what the narration covers; grace, not pressure; no spoiler of the payoff (He climbed into their boat / "Let Him into your life") in the first line; the brand is "Salt and Light Kingdom" (any other brand name is an error).
8. Files: video specs, thumbnail sizes/crops, captions file (format, timing, line length, reading speed, words must match the locked words), and any risk of pasting from the WRONG source.
9. Anything else a sharp editor, a pastor, a platform reviewer or a lawyer would catch.

OUTPUT (markdown, max ~600 words):
## VERDICT: SHIP / FIX FIRST / BLOCK
## ISSUES (most serious first; each: where (file/field/setting) | the problem | exact replacement text or exact setting)
## MISSING UPLOAD STEPS (bullets)
## WHAT IS GOOD (max 3 bullets)

KJV TEXT (the authority):
Job 9:8 Which alone spreadeth out the heavens, and treadeth upon the waves of the sea.
Job 9:11 Lo, he goeth by me, and I see him not: he passeth on also, but I perceive him not.
Job 9:32 For he is not a man, as I am, that I should answer him, and we should come together in judgment.
Job 9:33 Neither is there any daysman betwixt us, that might lay his hand upon us both.
Mark 6:48 And he saw them toiling in rowing; for the wind was contrary unto them: and about the fourth watch of the night he cometh unto them, walking upon the sea, and would have passed by them.
Mark 6:49 But when they saw him walking upon the sea, they supposed it had been a spirit, and cried out:
Mark 6:50 For they all saw him, and were troubled. And immediately he talked with them, and saith unto them, Be of good cheer: it is I; be not afraid.
Mark 6:51 And he went up unto them into the ship; and the wind ceased: and they were sore amazed in themselves beyond measure, and wondered.
1 Timothy 2:5 For there is one God, and one mediator between God and men, the man Christ Jesus;
Hebrews 4:15 For we have not an high priest which cannot be touched with the feeling of our infirmities; but was in all points tempted like as we are, yet without sin.

THE VIDEO'S SPOKEN WORDS (cannot change):
"""

narr = "\n".join(l for l in (P / "narration.md").read_text(encoding="utf-8").splitlines() if not l.startswith("<!--"))

FILES = """

FILES THE UPLOADER HAS
- Video: job_sea_final.mp4, H.264 + AAC, 1080x1920, 30 fps, 67.3 s; spoken words end at about 64.0 s then a hold. Sepia ink comic-book panels with read-along words burned in; the only colour is a red ring around Jesus. Narrator, an old man's voice (Job) and a voice for Jesus. It shows Job on a rock by a stormy sea, men rowing at night, Jesus walking on the water, Jesus stepping into the boat.
- Thumbnails: publish/thumbs/thumb_9x16.jpg 1080x1920 (the poster), thumb_tiktok.jpg (same), thumb_16x9.jpg and thumb_1x1.jpg (not for upload).
- captions_locked.srt (below, uploaded as English on YouTube).
- A paste page (PUBLISH_INDEX.html) built from the four platform files below; it shows each field with a copy button, including the YouTube PINNED_COMMENT section of youtube_short.md.

THUMBNAIL: epic painted movie-poster key art: old Job on a rock (seen from behind) reaching toward Jesus, who walks toward him on a stormy sea, red ring behind His head, a boat of rowers beside. Words "MAN ON THE SEA" / "SO WHO IS THIS?".

"""

parts = [HEAD, narr, FILES]
parts.append("\n==== THE UPLOAD CHECKLIST ====\n\n" + (P / "UPLOAD_CHECKLIST.md").read_text(encoding="utf-8"))
parts.append("\n\n==== THE PLATFORM FILES (paste source) ====\n")
for f in ["youtube_short.md", "tiktok.md", "instagram.md", "facebook.md"]:
    parts.append(f"\n---- {f} ----\n" + (pub / f).read_text(encoding="utf-8"))
parts.append("\n\n---- captions_locked.srt ----\n" + (pub / "captions_locked.srt").read_text(encoding="utf-8"))
(D / "PROMPT.md").write_text("".join(parts), encoding="utf-8")
print("PROMPT.md", len("".join(parts)), "chars")
