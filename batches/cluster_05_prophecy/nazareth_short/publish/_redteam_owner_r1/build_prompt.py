"""Blind red-team prompt for the Nazareth publish pack (pattern: bethlehem_short/publish/_redteam_owner_r4). $0.
Built by script from the shipped copy + locked words + KJV only. No earlier drafts, no opinions."""
import json, re
from pathlib import Path
D = Path(__file__).resolve().parent; PUB = D.parent; PIECE = PUB.parent
EP = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\02_nazareth")
kjv = (EP / "words" / "KJV.txt").read_text(encoding="utf-8")
kjv = "\n".join(l for l in kjv.splitlines() if not l.startswith("2 Corinthians"))
kjv += ("\nLuke 23:35 And the people stood beholding. And the rulers also with them derided him, saying, He saved others; let him save himself, if he be Christ, the chosen of God.\n"
        "1 Corinthians 15:3-4 For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:\n")
words = "\n".join(l for l in (EP / "words" / "FINAL_WORDS_v7.md").read_text(encoding="utf-8").splitlines() if l.startswith("["))
card = json.loads((EP / "_packaging" / "21_nazareth" / "packaging.json").read_text(encoding="utf-8"))
HEAD = """You are ONE independent red-team seat (you have not seen any other seat or any earlier review). Be hostile, specific and honest; no flattery. Use only what is below. Do not ask questions. Do not use tools. Output text only.

JOB: red-team the full PUBLICATION + UPLOAD for a finished 59.9-second vertical Bible short before it goes live on YouTube Shorts, TikTok, Instagram Reels and Facebook. The uploader will paste the text below and follow the checklist below. Find everything that is wrong, risky, inconsistent, weak, missing or against the rules.

CHECK:
1. Bible accuracy: every claim and quote vs the KJV text below; KJV quotes word-for-word. In Luke 4:18-19 the quote stops at "the acceptable year of the Lord"; Isaiah 61:2 continues "and the day of vengeance of our God". The Bible does NOT say why Jesus stopped there. Any text that says or implies a reason (judgment cancelled, deleted, denied, postponed, ignored, "grace only") is an overclaim; equally, anything implying the vengeance line is false or removed from the Bible is an error. Check the Elijah/widow claim (Luke 4:25-26), the cliff (Luke 4:28-30), the Luke 23:35 link (who said it, and that Luke 23:35 and Luke 4:23 are different words), and "rose again the third day" (1 Corinthians 15:3-4).
2. Honesty: no clickbait; title + thumbnail + text must be paid off by the video. Does "left unread" / "stopped reading mid-sentence" fairly describe what Luke 4:17-20 shows?
3. Consistency: title, thumbnail, descriptions, captions, pinned comment, tags and checklist agree with each other and with the video's locked words.
4. Global audience: plain words for English-second-language viewers; a total newcomer with no Bible knowledge.
5. Platform fit, per platform: hard limits and best practice (title/caption/description lengths, what shows before "more", hashtag count/order/placement, tags, links, Shorts/Reels specifics, custom thumbnail/cover for Shorts/Reels/TikTok, captions upload).
6. Upload settings: are the checklist settings right and complete for each platform? What is missing?
7. Owner rules: NO AI wording anywhere in public text (disclosure ONLY with each platform's own switch); the scripture range shown must cover what the narration covers; grace, not pressure; no spoiler of the payoff in the first line; the brand is "Salt and Light Kingdom" (any other brand name is an error).
8. Files: video specs, thumbnail sizes/crops, captions file (format, timing, line length, reading speed, words must match the locked words), and any risk of pasting from the WRONG source.
9. Anything else a sharp editor, a pastor, a platform reviewer or a lawyer would catch.

OUTPUT (markdown, max ~600 words):
## VERDICT: SHIP / FIX FIRST / BLOCK
## ISSUES (most serious first; each: where (file/field/setting) | the problem | exact replacement text or exact setting)
## MISSING UPLOAD STEPS (bullets)
## WHAT IS GOOD (max 3 bullets)
"""
FILES = """
FILES THE UPLOADER HAS
- Video: nazareth_final.mp4, H.264 + AAC, 1080x1920, 30 fps, 59.9 s; spoken words end at about 56.4 s then a hold. Comic-book pages with on-screen read-along words burned in. It shows: Jesus reading a scroll in a synagogue, the crowd, an angry crowd and a cliff edge, Jesus walking through the crowd, and Jesus on the cross in a wide shot (no blood or wounds shown).
- Thumbnails: thumb_9x16.jpg 1080x1920 (the poster), thumb_tiktok.jpg 1080x1920 (same), thumb_16x9.jpg 1280x720 and thumb_1x1.jpg 1080x1080 (the 9:16 poster centred over a blurred copy of itself).
- captions_locked.srt (below, uploaded as English on YouTube).
- A paste page (PUBLISH_INDEX.html) built from the four platform files below.

THUMBNAIL: painted movie-poster key art. Words "THE LINE" / "HE LEFT UNREAD". Jesus looks at the viewer with his finger on a scroll at the place where the lit text turns to shadow, in a plain stone synagogue.

PINNED COMMENT (YouTube, posted after release): """ + card["pinned_comment"] + "\n"
chk = (PIECE / "UPLOAD_CHECKLIST.md").read_text(encoding="utf-8")
parts = [HEAD, "KJV TEXT (the authority):\n" + kjv, "\nTHE VIDEO'S LOCKED SPOKEN WORDS (cannot change):\n" + words, FILES,
         "\n==== THE UPLOAD CHECKLIST (settings the uploader follows) ====\n" + chk.split("\n", 1)[1],
         "\n==== THE PLATFORM FILES (paste source) ===="]
for f in ("youtube_short.md", "tiktok.md", "instagram.md", "facebook.md"):
    parts.append(f"\n---- {f} ----\n" + (PUB / f).read_text(encoding="utf-8"))
parts.append("\n---- captions_locked.srt ----\n" + (PUB / "captions_locked.srt").read_text(encoding="utf-8"))
txt = "\n".join(parts)
for bad in ("Bartimaeus", "seat_", "red team", "red-team notes", "FINAL_WORDS", "OWNER CALL", "convergent"):
    assert bad not in txt, bad
(D / "PROMPT.md").write_text(txt, encoding="utf-8"); print("ok", len(txt.split()), "words")
