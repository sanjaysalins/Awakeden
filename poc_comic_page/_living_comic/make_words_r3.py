"""Y2 = candidate Y (Fable spine) + convergent fixes from the 5-seat blind comparison. Verifies quotes, builds the confirm pack (one version, guardrail format)."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible")
D = ROOT / "poc_comic_page" / "_words_mockers_r3"; (D / "panel_r1").mkdir(parents=True, exist_ok=True)
Y2 = """[narrator] People at the cross shout at Jesus, the Son of God. Listen.
[mocker] "He trusted in God; let him deliver him now" [Matthew 27:43]
[narrator] Deliver means rescue. Now, a thousand years earlier, a king named David. People laugh at him too, and he writes down what they say.
[david] "He trusted on the LORD that he would deliver him" [Psalm 22:8]
[narrator] Almost the same words, a thousand years apart. People passing by shout one more thing.
[mocker] "If thou be the Son of God, come down from the cross" [Matthew 27:40]
[narrator] If you are God's Son, come down. He could have. Jesus had said that no one takes His life from Him. He gives it Himself. So He stayed. And He prayed for them.
[narrator] "Father, forgive them; for they know not what they do." [Luke 23:34]
[narrator] Near its end, David's song says people from every nation will turn to God.
[david] "shall remember and turn unto the LORD" [Psalm 22:27]
[narrator] You can turn to the One who stayed."""
(D / "cand_Y2.md").write_text(Y2, encoding="utf-8")
import judge_words_r1 as J
clean = re.sub(r"\[(narrator|david|mocker)\]", "", re.sub(r"\[(?:Psalms?|Matthew|John|Luke) [\d:]+\]", "", Y2))
quotes = re.findall(r"\"([^\"]+)\"", clean)
bad = [q for q in quotes if not J.in_kjv(q)]
n = len(clean.split()); print("words", n, "secs@2.75", round(n / 2.75, 1), "non_verbatim", bad)
R1 = ROOT / "poc_comic_page" / "_words_mockers_r1" / "pack.md"
kjv = R1.read_text(encoding="utf-8").split("## KJV text you may quote (the only authority)")[1].split("## OUTPUT FORMAT")[0]
pack = """# FILM-ONLY PACK (what the viewer hears and sees)
Format: a 60-65 second vertical (9:16) Bible short for YouTube Shorts / TikTok, narrated, comic-style pictures; the quoted Bible lines also appear in speech balloons; first on-screen card (first 2.6 seconds): WHO WROTE THE MOCKERY?
Title shown on upload: The Mockers' Words (Psalm 22:7-8)
One extra on-screen card: DELIVER = RESCUE (during the first Psalm quote).
Voices: [narrator], [david] (David's Psalm words), [mocker] (the crowd's Matthew taunts). Bible quotes are KJV; references are in brackets.

## EVERYTHING THE VIEWER HEARS (numbered lines)
""" + "\n".join("%d. %s" % (i + 1, l) for i, l in enumerate(Y2.split("\n"))) + "\n\n## KJV TEXT SUPPLIED FOR CHECKING (authority)" + kjv
(D / "pack.md").write_text(pack, encoding="utf-8")
L = {"judge": ["JUDGE, NO HAT", "Judge this film for the whole worldwide audience at once. Answer the five questions and name the ONE change that helps most."],
     "newcomer": ["THE TOTAL NEWCOMER", "You have never opened a Bible and know nothing about Jesus beyond the pack. English is your second language, on a phone. For question 4 say you cannot judge accuracy and list what you were TOLD that you could not follow. Report what you understood, guessed, and every question you are left with."],
     "bible": ["BIBLE FACT-CHECKER", "Check every claim in the SPOKEN lines against the KJV text supplied: RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG, quoting the line and verse. Check each quote is verbatim."],
     "hook": ["HOOK AND RETENTION", "Judge the first 5 seconds after the card, pacing, the weakest 10 seconds, and give odds with error bars for watching to the end."],
     "global": ["SECOND-LANGUAGE READER", "Quote every word or idiom that would fail in translation or on a small screen; who is served and who is not; anything that could offend."]}
(D / "lenses.json").write_text(json.dumps(L, indent=1), encoding="utf-8")
fmt = Path(r"F:\slk\PycharmProjects\JesusInTheBible\poc_comic_page\_panel_mockers_words\format.txt").read_text(encoding="utf-8")
(D / "format.txt").write_text(fmt, encoding="utf-8")
(D / "header.txt").write_text("You are ONE independent, HOSTILE voice on a review panel (you have not seen the other voices or any earlier version). Everything is in the EVIDENCE PACK. Do not ask questions. Do not use tools. Output the review text only.\n", encoding="utf-8")
print("ok")
