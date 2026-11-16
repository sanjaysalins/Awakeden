"""Red team r2 (owner ask 2026-11-15: "red team your publication and upload details"). Fresh blind seats.
Covers the CURRENT publish pack (after r1 fixes) PLUS the upload details: settings, files, thumbnails, captions file,
pinned comment, and the stale engine upload kit as a paste-source risk. $0."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent; PUB = D.parent; PIECE = PUB.parent
EP = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem")
kjv = (EP / "words" / "KJV.txt").read_text(encoding="utf-8").split("## John 7:40-43")[0].strip()
kjv += ("\n\n## John 6:38\nFor I came down from heaven, not to do mine own will, but the will of him that sent me.\n\n"
        "## 1 Corinthians 15:3-4\nFor I delivered unto you first of all that which I also received, how that Christ died for our sins "
        "according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:\n")
words = (EP / "words" / "FINAL_WORDS_v3.md").read_text(encoding="utf-8")
card = json.loads((EP / "_packaging" / "19_bethlehem" / "packaging.json").read_text(encoding="utf-8"))
HEAD = """You are ONE independent red-team seat (you have not seen any other seat or any earlier review). Be hostile, specific and honest; no flattery. Use only what is below. Do not ask questions. Do not use tools. Output text only.

JOB: red-team the full PUBLICATION + UPLOAD for a finished 59.5-second vertical Bible short before it goes live on YouTube Shorts, TikTok, Instagram Reels and Facebook. The uploader will paste the text below and set the settings below. Find everything that is wrong, risky, inconsistent, weak, missing or against the rules.

CHECK:
1. Bible accuracy: every claim and quote vs the KJV text below; KJV quotes word-for-word. The Bible is SILENT on whether the experts (chief priests and scribes) went to Bethlehem: anything saying or implying they refused, stayed home or did not care is an overclaim. The shepherds also went (Luke 2:15-16), outside this video's range: do not imply only the wise men went.
2. Honesty: no clickbait; title + thumbnail + text must be paid off by the video.
3. Consistency: title, thumbnail, descriptions, captions, pinned comment, tags and settings agree with each other and with the video's locked words.
4. Global audience: plain words for English-second-language viewers.
5. Platform fit, per platform: hard limits and best practice (title/caption/description lengths, what shows before "more", hashtag count/order/placement, tags, links, Shorts/Reels specifics, whether a custom thumbnail can actually be used for a Short/Reel/TikTok and how, captions upload, cover frame).
6. Upload settings: are they right and complete for each platform (audience/made for kids, altered or synthetic content disclosure switch, category, language, captions language, licence, comments, visibility, playlist/series, location, remix/duet/stitch, schedule)? What is missing?
7. Owner rules: NO AI wording anywhere in public text (the disclosure is done ONLY with each platform's own switch); the scripture range shown must cover what the narration covers; grace, not pressure; no spoiler of the payoff in the first line.
8. Files: video specs, thumbnail sizes/crops, captions file (format, timing, line length, reading speed), and any risk of pasting from the WRONG source.
9. Anything else a sharp editor, a pastor, a platform reviewer or a lawyer would catch.

OUTPUT (markdown, max ~600 words):
## VERDICT: SHIP / FIX FIRST / BLOCK
## ISSUES (most serious first; each: where (file/field/setting) | the problem | exact replacement text or exact setting)
## MISSING UPLOAD STEPS (bullets)
## WHAT IS GOOD (max 3 bullets)
"""
FILES = """
FILES THE UPLOADER HAS
- Video: bethlehem_final.mp4, H.264 + AAC, 1080x1920, 30 fps, 59.5 s, 72 MB, spoken words end at 56.4 s then a 3 s hold.
- Thumbnails: thumb_9x16.jpg 1080x1920 (the poster), thumb_tiktok.jpg 1080x1920 (same), thumb_16x9.jpg 1280x720 and thumb_1x1.jpg 1080x1080 (the whole 9:16 poster centred over a blurred copy of itself).
- captions.srt (below), English.
- A paste page (PUBLISH_INDEX.html) built from the four platform files below. ALSO in the folder: an older engine draft upload/upload_kit.md that still has the OLD first line ("Bethlehem was named 700 years before Jesus. The experts knew. Who went to see the King?") and a "YouTube (Long-form 16:9)" block; the team rule is to paste only from publish/.

UPLOAD SETTINGS (house defaults, same for every video)
- Audience: NOT made for kids
- Altered content / AI disclosure: YES (synthetic/altered imagery) via the platform switch
- Category: Education
- License: Standard YouTube licence
- Comments: On, hold potentially inappropriate for review
- Visibility: Public (YouTube first; TikTok/FB/IG within 24-48 h). Posting is currently held until the series has 30 episodes.

THUMBNAIL: painted comic-book movie poster. Top words "EXPERTS KNEW" (cream) / "DID THEY GO?" (gold). Below, in an inked panel: two old Jewish scholars in prayer shawls read a scroll by a small oil lamp, both looking down at the page; the lamp's flame rises into the risen Jesus, arms open, wrapped in a flame-like gold-and-blue glow. A tiny hill town with a star far behind.

PINNED COMMENT (YouTube): """ + card["pinned_comment"] + "\n"
parts = [HEAD, "KJV TEXT (the authority):\n" + kjv, "\nTHE VIDEO'S LOCKED SPOKEN WORDS (cannot change):\n" + words, FILES, "\n==== THE PLATFORM FILES (paste source) ===="]
for f in ("youtube_short.md", "tiktok.md", "instagram.md", "facebook.md"):
    parts.append(f"\n---- {f} ----\n" + (PUB / f).read_text(encoding="utf-8"))
parts.append("\n---- captions.srt ----\n" + (PUB / "captions.srt").read_text(encoding="utf-8"))
txt = "\n".join(parts)
for bad in ("Bartimaeus", "Jericho", "seat_", "r1 "):
    assert bad not in txt, bad
(D / "PROMPT.md").write_text(txt, encoding="utf-8"); print("ok", len(txt.split()), "words")
