"""Y3 = Y2 + convergent fixes from the 5-seat confirm round. Verifies quotes; writes the candidate file and an owner page."""
import re, sys, json, html
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); D = ROOT / "poc_comic_page" / "_words_mockers_r3"
Y3 = """[narrator] Jesus, the Son of God, is dying on a cross. People shout at Him. Listen.
[mocker] "He trusted in God; let him deliver him now" [Matthew 27:43]
[narrator] In plain words: he trusted God, so let God rescue him. Now go back a thousand years, to a king named David. People laugh at him too. He writes it into a song.
[david] "He trusted on the LORD that he would deliver him" [Psalm 22:8]
[narrator] Almost the same words, a thousand years apart. People passing by shout one more thing.
[mocker] "If thou be the Son of God, come down from the cross" [Matthew 27:40]
[narrator] If you are God's Son, come down. He could have come down. Jesus had said that no one takes His life from Him. He gives His life Himself. So He stayed. And from the cross He prayed:
[narrator] "Father, forgive them; for they know not what they do." [Luke 23:34]
[narrator] That same song heard the insults a thousand years early. It also says what comes next: people from every nation will turn to God.
[david] "All the ends of the world shall remember and turn unto the LORD" [Psalm 22:27]
[narrator] You can turn to the One who stayed."""
(D / "cand_Y3.md").write_text(Y3, encoding="utf-8")
import judge_words_r1 as J
clean = re.sub(r"\[(narrator|david|mocker)\]", "", re.sub(r"\[(?:Psalms?|Matthew|John|Luke) [\d:]+\]", "", Y3))
quotes = re.findall(r"\"([^\"]+)\"", clean); bad = [q for q in quotes if not J.in_kjv(q)]
n = len(clean.split()); print("words", n, "secs@2.75", round(n / 2.75, 1), "non_verbatim", bad)
# balloon-length check (<=8 words per balloon; Ps 22:27 splits in two)
for q in quotes: print(len(q.split()), q)
