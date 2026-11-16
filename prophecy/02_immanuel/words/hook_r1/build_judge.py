"""Blind hook judge pack: 7 hooks (incl. current as control), shuffled letters, writer key kept out. $0."""
import random, json
from pathlib import Path
H = Path(__file__).resolve().parent
HOOKS = [  # (source, hook, bridge end after "Jesus is that promised son, and")
 ("current",  "This baby's name is not a word. It is a sentence.", "Immanuel is the sentence: God with us."),
 ("fable1",   "God offered a scared king a sign. The king said no.", "Immanuel means God with us: the sign God gave anyway."),
 ("claude1",  "A scared king refused a sign from God. God gave one anyway: a baby.", "Immanuel is the sign the king would not ask for: God with us."),
 ("fable2",   "Two armies were coming. God's answer was a baby.", "Immanuel is God's answer: God with us."),
 ("claude3",  "Everyone knows the Christmas baby's name. God had already given Him another one.", "Immanuel is the other name: God with us."),
 ("fable3",   "Jesus has another name. It tells you where God is.", "His other name, Immanuel, means: God with us."),
 ("codex2",   "God promised Immanuel. Why was the baby called Jesus?", "Immanuel tells us who Jesus is: God with us."),
]
random.seed(20261115); order = HOOKS[:]; random.shuffle(order)
letters = "ABCDEFG"; key = {letters[i]: h[0] for i, h in enumerate(order)}
opts = "\n".join(f"=== {letters[i]} ===\nFIRST LINE: {h[1]}\nBRIDGE LINE: Matthew's book about Jesus says the promise came true. Jesus is that promised son, and {h[2]}\n" for i, h in enumerate(order))
P = f"""You are ONE independent reviewer. You have not seen any other review. Be honest and specific. Do not flatter.

A 59-second vertical Bible video, episode 2 of "Promised, then kept" (an Old Testament promise and how it came true in Jesus). Worldwide audience: many with English as a second language, many with no Bible knowledge, on a phone, captions on, scrolling fast. Also Bible readers who know the Christmas story.

The script is LOCKED except its FIRST LINE and the end of one BRIDGE LINE. The locked script ({{FIRST LINE}} and {{BRIDGE LINE}} are filled from each option below):
[narrator] {{FIRST LINE}}
[narrator] About seven hundred years before Jesus, in King Ahaz's day, God gave a promise through Isaiah, a man who spoke God's message:
[prophet] Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.
[narrator] (pause) Mary, a virgin, who had never been with a man, was pregnant by God's Holy Spirit.
[narrator] An angel told her husband Joseph:
[angel] thou shalt call his name JESUS: for he shall save his people from their sins.
[narrator] {{BRIDGE LINE}}
[narrator] With us as a baby. With us at the cross, where He died for our sins. On the third day, He rose from the dead. He promised:
[jesus] I am with you alway.
[narrator] Still true.

KJV facts behind it: Isaiah 7:1-2 two kings came to war against Jerusalem and King Ahaz's heart shook "as the trees of the wood are moved with the wind". 7:11 "Ask thee a sign of the LORD thy God". 7:12 Ahaz: "I will not ask, neither will I tempt the LORD." 7:14 "Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel." 7:15-16 the sign also pointed to Ahaz's own day. Matthew 1:21-23: call his name JESUS; "they shall call his name Emmanuel, which being interpreted is, God with us." Matthew 1:25 "he called his name JESUS".

THE OPTIONS:
{opts}
=== Answer (max ~400 words, plain English) ===
A table, one row per option: letter | STOP (would a fast-scrolling newcomer stop? 0-10) | CLEAR (does a second-language viewer get every word at once? 0-10) | HONEST (true to the KJV, no bait, truly paid off? 0-10) | FIT (flows into the locked script and its ending? 0-10) | one-line reason.
Then: YOUR PICK (one letter), your second pick, and the single biggest risk of your pick.
"""
for bad in ("fable", "claude", "codex", "gemini", "grok", "current"):
    assert bad not in P.lower().replace("current hook", ""), bad
(H / "JUDGE_PACK.md").write_text(P, encoding="utf-8"); (H / "_KEY_do_not_give.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
print("ok", len(P.split()), key)
