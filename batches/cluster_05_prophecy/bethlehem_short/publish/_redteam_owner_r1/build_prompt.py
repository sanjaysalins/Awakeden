"""Blind red-team prompt for the Bethlehem publish pack (copied from bartimaeus_short/publish/_redteam_owner_r1). $0."""
import json
from pathlib import Path
D = Path(__file__).resolve().parent; PUB = D.parent
EP = Path(r"F:\slk\PycharmProjects\JesusInTheBible\prophecy\01_bethlehem")
B = Path(r"F:\slk\PycharmProjects\JesusInTheBible\batches\cluster_04_encounters\bartimaeus_short\publish\_redteam_owner_r1\PROMPT.md").read_text(encoding="utf-8")
head = B[:B.index("KJV TEXT (the authority):")]
head = head.replace("79-second", "59.5-second").replace('Flag overclaims ("a whole crowd" vs "many", where he followed, etc.).',
    'Flag overclaims. The Bible is SILENT on whether the experts (chief priests and scribes) went to Bethlehem: any text saying or implying they refused, stayed home or did not care is an overclaim.')
head = head.replace("the video also tells of the cross and the resurrection from 1 Corinthians 15:3-4",
    "the video tells Micah 5:2, Matthew 2:1-11, Luke 2:1-7, and ends with John 6:38 and 1 Corinthians 15:3-4")
kjv = (EP / "words" / "KJV.txt").read_text(encoding="utf-8").split("## John 7:40-43")[0].strip()
kjv += ("\n\n## John 6:38\nFor I came down from heaven, not to do mine own will, but the will of him that sent me.\n\n"
        "## 1 Corinthians 15:3-4\nFor I delivered unto you first of all that which I also received, how that Christ died for our sins "
        "according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:\n")
words = (EP / "words" / "FINAL_WORDS_v3.md").read_text(encoding="utf-8")
card = json.loads((EP / "_packaging" / "19_bethlehem" / "packaging.json").read_text(encoding="utf-8"))
parts = [head, "KJV TEXT (the authority):\n" + kjv,
         "\nTHE VIDEO'S LOCKED SPOKEN WORDS (cannot change; the pack must match them):\n" + words,
         '\nTHUMBNAIL (all platforms): painted comic-book movie poster. Top words "EXPERTS KNEW" (cream) / "DID THEY GO?" (gold). '
         "Below, in an inked panel: two old Jewish scholars in prayer shawls read a scroll by a small oil lamp, both looking down at the page; "
         "the lamp's flame rises into the risen Jesus, arms open, wrapped in a flame-like gold-and-blue glow. A tiny hill town with a star far behind.",
         "\nPINNED COMMENT (YouTube): " + card["pinned_comment"], "\n==== THE PLATFORM FILES ===="]
for f in ("youtube_short.md", "tiktok.md", "instagram.md", "facebook.md"):
    parts.append(f"\n---- {f} ----\n" + (PUB / f).read_text(encoding="utf-8"))
parts.append("\n---- captions.srt (the spoken words, timed) ----\n" + (PUB / "captions.srt").read_text(encoding="utf-8"))
txt = "\n".join(parts)
for bad in ("Bartimaeus", "Jericho", "STOOD STILL"):
    assert bad not in txt, bad
(D / "PROMPT.md").write_text(txt, encoding="utf-8"); print("ok", len(txt.split()), "words")
