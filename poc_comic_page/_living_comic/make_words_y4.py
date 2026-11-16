"""Y4 = Y3 + convergent fixes from the Y3 confirm round (5 seats). Verifies KJV quotes by script."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); D = ROOT / "poc_comic_page" / "_words_mockers_r4"
Y4 = """[narrator] Jesus, the Son of God, is dying on a cross. The leaders shout at Him. Listen.
[mocker] "He trusted in God; let him deliver him now" [Matthew 27:43]
[narrator] In plain words: he trusted God, so let God rescue him. Now go back a thousand years, to a king named David. People laugh at David too. He writes their words into a song, Psalm 22.
[david] "He trusted on the LORD that he would deliver him" [Psalm 22:8]
[narrator] Almost the same words, a thousand years apart. People passing by also shout.
[mocker] "If thou be the Son of God, come down from the cross" [Matthew 27:40]
[narrator] If you are God's Son, come down. He could have come down. Jesus had said that no one takes His life from Him. He gives His life Himself. He stayed. And on the cross, He also prayed:
[narrator] "Father, forgive them; for they know not what they do." [Luke 23:34]
[narrator] That same song had these insults a thousand years early. Later in that song, David says people from every nation will turn to God.
[narrator] Jesus stayed for the people who mocked Him. You can turn to Him too."""
(D / "cand_Y4.md").write_text(Y4, encoding="utf-8")
import judge_words_r1 as J
clean = re.sub(r"\[(narrator|david|mocker)\]", "", re.sub(r"\[(?:Psalms?|Matthew|John|Luke) [\d:]+\]", "", Y4))
quotes = re.findall(r"\"([^\"]+)\"", clean); bad = [q for q in quotes if not J.in_kjv(q)]
n = len(clean.split()); print("words", n, "secs@2.75", round(n / 2.75, 1), "non_verbatim", bad)
banned = [w for w in ("script", "unwilling", "scorn", "ends of the world", "messiah", "line for line", "whole song", "heard the insults") if w in clean.lower()]
print("banned used:", banned)
