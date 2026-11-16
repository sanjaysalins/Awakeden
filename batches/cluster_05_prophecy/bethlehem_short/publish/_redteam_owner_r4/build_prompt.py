"""Red team r4 (owner ask 2026-11-16 "yes run it": re-test after r3 fixes) on the pack updated for film v6 / words v4.1.
Fresh blind seats; same JOB/CHECK as r2 plus the new claims (from everlasting, Galilee / John 7). $0."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent; PUB = D.parent; PIECE = PUB.parent
EP = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem")
kjv = (EP / "words" / "KJV.txt").read_text(encoding="utf-8").strip()
kjv += ("\n\n## John 6:38\nFor I came down from heaven, not to do mine own will, but the will of him that sent me.\n\n"
        "## Luke 2:39\nAnd when they had performed all things according to the law of the Lord, they returned into Galilee, to their own city Nazareth.\n\n"
        "## Matthew 2:23\nAnd he came and dwelt in a city called Nazareth: that it might be fulfilled which was spoken by the prophets, He shall be called a Nazarene.\n\n"
        "## 1 Corinthians 15:3-4\nFor I delivered unto you first of all that which I also received, how that Christ died for our sins "
        "according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:\n")
words = "\n".join(l for l in (EP / "words" / "FINAL_WORDS_v4.md").read_text(encoding="utf-8").splitlines() if l.startswith("["))
card = json.loads((EP / "_packaging" / "19_bethlehem" / "packaging.json").read_text(encoding="utf-8"))
HEAD = """You are ONE independent red-team seat (you have not seen any other seat or any earlier review). Be hostile, specific and honest; no flattery. Use only what is below. Do not ask questions. Do not use tools. Output text only.

JOB: red-team the full PUBLICATION + UPLOAD for a finished 59.4-second vertical Bible short before it goes live on YouTube Shorts, TikTok, Instagram Reels and Facebook. The uploader will paste the text below and follow the checklist below. Find everything that is wrong, risky, inconsistent, weak, missing or against the rules.

CHECK:
1. Bible accuracy: every claim and quote vs the KJV text below; KJV quotes word-for-word. The Bible is SILENT on whether the experts (chief priests and scribes) went to Bethlehem: anything saying or implying they refused, stayed home or did not care is an overclaim. The shepherds also went (Luke 2:15-16): do not imply only the wise men went. Micah 5:2 "from of old, from everlasting" is read by some as an ancient family line: the copy must not claim this verse alone PROVES Jesus is God, and must not claim a motive for why Matthew 2:6 quotes less of the verse. In John 7:41-43 people argued among themselves: they did not question Jesus to His face, and it was "some", not everyone.
2. Honesty: no clickbait; title + thumbnail + text must be paid off by the video.
3. Consistency: title, thumbnail, descriptions, captions, pinned comment, tags and checklist agree with each other and with the video's locked words.
4. Global audience: plain words for English-second-language viewers.
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
- Video: bethlehem_final.mp4, H.264 + AAC, 1080x1920, 30 fps, 59.4 s, 69 MB, spoken words end at 56.4 s then a 3 s hold. On-screen read-along words are burned in. A small caption "ABOUT 700 YEARS BEFORE" shows on the Micah intro; the end card reads "PROMISED. CAME TRUE."
- Thumbnails: thumb_9x16.jpg 1080x1920 (the poster), thumb_tiktok.jpg 1080x1920 (same), thumb_16x9.jpg 1280x720 and thumb_1x1.jpg 1080x1080 (the whole 9:16 poster centred over a blurred copy of itself).
- captions.srt (below), English.
- A paste page (PUBLISH_INDEX.html) built from the four platform files below. ALSO in the folder: an older engine draft upload/upload_kit.md (stale, marked DO NOT PASTE, still mentions a tax order that is no longer in the video).

THUMBNAIL: painted comic-book movie poster. Top words "EXPERTS KNEW" (cream) / "DID THEY GO?" (gold). Below, in an inked panel: two old Jewish scholars in prayer shawls by a small oil lamp with a scroll; one reads the scroll, the other looks up and out toward a tiny far hill town with a star. The lamp's flame rises into the risen Jesus, arms open, wrapped in a flame-like gold-and-blue glow.

PINNED COMMENT (YouTube): """ + card["pinned_comment"] + "\n"
parts = [HEAD, "KJV TEXT (the authority):\n" + kjv, "\nTHE VIDEO'S LOCKED SPOKEN WORDS (cannot change):\n" + words, FILES,
         "\n==== THE UPLOAD CHECKLIST (settings the uploader follows) ====\n" + "# Born in Bethlehem: upload checklist\n" + (PIECE / "UPLOAD_CHECKLIST.md").read_text(encoding="utf-8").split("\n", 1)[1],
         "\n==== THE PLATFORM FILES (paste source) ===="]
for f in ("youtube_short.md", "tiktok.md", "instagram.md", "facebook.md"):
    parts.append(f"\n---- {f} ----\n" + (PUB / f).read_text(encoding="utf-8"))
parts.append("\n---- captions.srt ----\n" + (PUB / "captions.srt").read_text(encoding="utf-8"))
txt = "\n".join(parts)
for bad in ("Bartimaeus", "Jericho", "seat_", "red team r2", "r1 ", "v4.1", "FINAL_WORDS"):
    assert bad not in txt, bad
(D / "PROMPT.md").write_text(txt, encoding="utf-8"); print("ok", len(txt.split()), "words")
