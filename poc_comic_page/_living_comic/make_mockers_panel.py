"""Builds the blind guardrail-panel pack for Piece 2 (film-only: spoken words + title + runtime). No drafts, no opinions."""
import json, re
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
D = ROOT / "poc_comic_page" / "_panel_mockers_words"
corpus = json.load(open(ROOT / "data" / "kjv_corpus.json", encoding="utf-8-sig"))
def verse(book, ch, v):
    for b in corpus:
        if b["name"] == book: return b["chapters"][ch - 1][v - 1]
ps = " ".join("Psalm 22:%d %s" % (v, verse("Psalms", 22, v)) for v in range(6, 10))
mt = " ".join("Matthew 27:%d %s" % (v, verse("Matthew", 27, v)) for v in range(39, 45))
psl = " ".join("Psalm 22:%d %s" % (v, verse("Psalms", 22, v)) for v in range(27, 29))
import re as _re
nar0 = (ROOT / "batches/cluster_01_cross/mockers_words_ps227/audio/spoken_script.txt").read_text(encoding="utf-8-sig")
nar = chr(10).join("%d. %s" % (i + 1, t.strip()) for i, t in enumerate(_re.split(r"(?<=[.?!])\s+", nar0.strip()) ))
pack = """# FILM-ONLY PACK (what the viewer hears and sees)
Format: a 78-second vertical (9:16) Bible short for YouTube Shorts / TikTok, narrated, comic-style pictures with big on-screen question card at the start. Audience: worldwide.
First on-screen card (first 2.6 seconds): WHO SCRIPTED THE MOCKERY?
Title shown on upload: The Mockers' Words (Psalm 22:7-8)
Pictures (described, not seen by you): a crowd as dark silhouettes, an old king writing by lamplight, an open scroll, a man mocking and pointing up, a cross at dusk, a calm figure on the cross, many people walking toward a hill at dawn.
On-screen text: the quoted Bible lines appear in speech balloons as they are spoken; one card shows DELIVER = RESCUE.
Runtime: 78 seconds.

## EVERYTHING THE VIEWER HEARS (voices: narrator; david for the Psalm; mocker for the Matthew taunts)
""" + nar + """

## KJV TEXT SUPPLIED FOR CHECKING (authority)
""" + ps + "\n" + mt + "\n" + psl + "\n"
(D / "pack.md").write_text(pack, encoding="utf-8")
L = {
 "judge": ["JUDGE, NO HAT", "Judge this film for the whole worldwide audience at once: newcomer, Bible reader, scroller, second-language reader. Answer the five questions honestly and name the ONE change that helps the most people."],
 "newcomer": ["THE TOTAL NEWCOMER", "You have never opened a Bible and know nothing about Psalms, Matthew, the cross or Jesus beyond what this film says. English is your second language; you are on a phone. Use ONLY the pack. For question 4 say you cannot judge accuracy and list what you were TOLD that you could not follow. Report what you understood, guessed, and every question you are left with."],
 "bible": ["BIBLE READER AND FACT CHECKER", "You know the Bible well. Check every factual claim in the SPOKEN lines against the KJV text at the end of the pack. Question 4 is your main job: line by line, mark RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG, quote the line, cite the verse. Pay special attention to: 'nearly line for line', 'unwilling witnesses', 'He could have come down', 'showed He was the Son', the Psalm 22:27 landing."],
 "hook": ["HOOK AND RETENTION ANALYST", "Judge the first 3 seconds, the curiosity gap (where it opens, where it pays off), the pacing of a 78-second short, and what share would watch to the end. Give odds with error bars. Name the weakest 10 seconds."],
 "global": ["GLOBAL AND SECOND-LANGUAGE READER", "You read English as a second language. Mark every word, idiom or phrase that would fail in translation or on a small screen (quote it). Say who is served and who is not worldwide, and whether anything could offend or confuse another culture."]}
(D / "lenses.json").write_text(json.dumps(L, indent=1), encoding="utf-8")
print("ok", len(pack))
