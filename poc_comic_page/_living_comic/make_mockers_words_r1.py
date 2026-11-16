"""Blind multi-writer drafting pack for the Piece 2 narration rewrite. Writers see: source verses, rules, problem list. NOT the current script."""
import json
from pathlib import Path
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
D = ROOT / "poc_comic_page" / "_words_mockers_r1"; (D / "panel_r1").mkdir(parents=True, exist_ok=True)
corpus = json.load(open(ROOT / "data" / "kjv_corpus.json", encoding="utf-8-sig"))
def verse(book, ch, v):
    for b in corpus:
        if b["name"] == book: return b["chapters"][ch - 1][v - 1]
def span(book, ch, a, b): return "\n".join("%s %d:%d %s" % (book, ch, v, verse(book, ch, v)) for v in range(a, b + 1))
kjv = "\n".join([span("Psalms", 22, 6, 9), span("Psalms", 22, 27, 28), span("Matthew", 27, 39, 44), span("Matthew", 26, 53, 53), span("John", 10, 17, 18), span("Luke", 23, 34, 34)])
pack = """# WRITING BRIEF (write your own version from scratch)
You are writing the narration for a 60-75 second vertical Bible short (YouTube Shorts / TikTok), spoken aloud, watched worldwide including by people who read English as a second language. Comic-style pictures, big on-screen cards, speech balloons for quoted Bible lines.

## The thread (keep this ONE spine)
When Jesus hung on the cross, the people mocking Him said words that echo what King David wrote in Psalm 22 about a thousand years earlier. They did not know it. Then: He could have come down and did not; He stayed. And Psalm 22 does not end with mocking: it ends with people from every nation turning to the LORD. The ending invites the listener (grace, no pressure, no fear or loss framing) to turn to the One who stayed.

## Hard rules
1. Quoted Bible lines must be KJV VERBATIM from the verses below (you may quote a fragment, but every fragment word-for-word, in order, no changes). Everything else is your own plain narration.
2. Voices: [narrator], [david] (David's own Psalm words), [mocker] (the crowd's Matthew taunts). Tag every paragraph with its voice, like [narrator]. Quotes go in the david or mocker voice with the exact reference.
3. Length: 175 to 200 spoken words in total including quotes (about 70 seconds at natural speed). Do not exceed 200.
4. Global audience: clever in structure, never in vocabulary. Short sentences. No idioms a second-language reader could misread. A total newcomer must be able to say who, what and why.
5. Say once, early, in plain words who Jesus is (do not assume the viewer knows).
6. Answer the on-screen opening question card, which will read: WHO WROTE THE MOCKERY? -> your first lines must name who wrote the words (David) and who spoke them (the crowd at the cross).
7. Every claim beyond the verses must be sound and Bible-backed (the extra verses below back 'He could have come down' and 'for the very people'). Do not claim what the mockers thought or felt. Do not claim the whole Psalm is only about Jesus. No gain/loss, no manufactured pressure.
8. The last line must be earned by the piece's own words (not a stock closer).
9. Quote density: no more than ONE short matched pair of quotes (David then crowd) in the first 25 seconds; keep each quoted piece under 12 words.

## Problems to avoid (a reviewing panel found these in an earlier version; do not use these words or moves)
- the word 'script' or 'scripted' (reads as 'staged'); 'unwilling'; 'win the scorners'; 'scorn'/'scorners' (rare words); 'the ends of the world' (sounds like the end of the world); 'Messiah' unexplained; 'nearly line for line' (overclaims: only one clause echoes); 'the whole song was about' (too strong); claiming what the crowd was thinking.
- two or three closing sentences that restate the same point. One conclusion, one invitation.
- splitting one taunt across two paragraphs so a quote opens and never closes.

## KJV text you may quote (the only authority)
""" + kjv + """

## OUTPUT FORMAT
Give: (a) the narration as tagged paragraphs [narrator]/[david]/[mocker] with exact KJV quotes and references in brackets after each quote; (b) the word count; (c) two lines: your spine in one sentence, and what you cut and why. Nothing else.
"""
(D / "pack.md").write_text(pack, encoding="utf-8")
L = {
 "w_plain": ["WRITER: PLAIN WORDS FIRST", "Write the clearest possible version for a second-language scroller. Prefer the simplest common word every time."],
 "w_hook": ["WRITER: HOOK AND PAYOFF", "Write the version with the strongest first 3 seconds and one clean payoff, then one invitation."],
 "w_faith": ["WRITER: FAITHFUL TO THE TEXT", "Write the version a careful Bible reader would sign off on claim by claim, still short and plain."],
 "w_story": ["WRITER: SCENE AND STORY", "Write the version that puts the listener at the foot of the cross, concrete and visual, one scene at a time (pictures change every 4 seconds)."],
 "w_free": ["WRITER: FREE HAT", "Write the best version you can by your own judgment."]}
(D / "lenses.json").write_text(json.dumps(L, indent=1), encoding="utf-8")
(D / "format.txt").write_text("Follow the OUTPUT FORMAT in the brief exactly.", encoding="utf-8")
(D / "header.txt").write_text("You are ONE independent writer on a blind panel; you have not seen any other writer's work or any earlier draft. Everything you need is in the BRIEF. Do not ask questions. Do not use tools. Output the requested text only.\n", encoding="utf-8")
print("ok", len(pack))
