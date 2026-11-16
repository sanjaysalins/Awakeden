"""Builds the 3 combined candidates (tagged by source seat) and the blind comparison pack (labels shuffled). Verifies KJV quotes by script."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(r"F:\slk\PycharmProjects\JesusInTheBible"); R1 = ROOT / "poc_comic_page" / "_words_mockers_r1"
D = ROOT / "poc_comic_page" / "_words_mockers_r2"; (D / "panel_r1").mkdir(parents=True, exist_ok=True)

CANDS = {
"A": ("spine: Fable; closing + Luke 23:34: Claude; opening echo of the card: Sonnet", """[narrator] A king named David wrote the words. The crowd at the cross spoke them, a thousand years later.
[narrator] First, David. People are laughing at him, and he writes down what they say.
[david] "He trusted on the LORD that he would deliver him" [Psalm 22:8]
[narrator] Deliver means rescue. Now the cross. Jesus, the Son of God, hangs there, dying. The leaders in the crowd call out.
[mocker] "He trusted in God; let him deliver him now" [Matthew 27:43]
[narrator] Hear it? Almost the same words, a thousand years apart. Then they shout one more thing.
[mocker] "come down from the cross" [Matthew 27:40]
[narrator] He could have come down. Jesus had said that no one takes His life from Him. He gives it Himself. So He stayed. And hanging there, He prayed for them.
[narrator] "Father, forgive them; for they know not what they do." [Luke 23:34]
[narrator] David's song does not end with laughing. It ends like this.
[david] "shall remember and turn unto the LORD" [Psalm 22:27]
[narrator] People from every nation, turning to the LORD. You can turn to the One who stayed."""),
"B": ("Claude (faithful) draft, trimmed by two lines", """[narrator] King David wrote these words. A crowd at a cross spoke words very like them, a thousand years later. The man on that cross was Jesus, the Son of God.
[narrator] First, David wrote:
[david] "He trusted on the LORD that he would deliver him." [Psalm 22:8]
[narrator] Then the crowd said:
[mocker] "He trusted in God; let him deliver him now." [Matthew 27:43]
[narrator] They said more to Him.
[mocker] "If thou be the Son of God, come down from the cross." [Matthew 27:40]
[narrator] He could have come down. Jesus had said:
[narrator] "No man taketh it from me." [John 10:18]
[narrator] He gave His life Himself. So He stayed. While they mocked, Jesus prayed for them:
[narrator] "Father, forgive them; for they know not what they do." [Luke 23:34]
[narrator] Now the ending. Psalm 22 does not end with mocking. David ended it with people from every nation turning to God.
[david] "Remember and turn unto the LORD." [Psalm 22:27]
[narrator] That means people like you, from any nation. No one is pushing you. The invitation is open. Turn to the One who stayed."""),
"C": ("short plain cut: Grok + Codex + Sonnet scene line", """[narrator] A king named David wrote these words. A thousand years later, a crowd at the cross spoke almost the same words. On that cross hung Jesus, the Son of God.
[narrator] People walk past and shake their heads. The leaders join in.
[david] "He trusted on the LORD that he would deliver him" [Psalm 22:8]
[mocker] "He trusted in God; let him deliver him now" [Matthew 27:43]
[narrator] Deliver means rescue. They said: if God wants Him, let God rescue Him. Then they shouted:
[mocker] "come down from the cross" [Matthew 27:40]
[narrator] He could have. He had said that no one takes His life, He lays it down Himself. He stayed, and He prayed for them: Father, forgive them.
[narrator] But David's song does not end with mocking. It says people from every nation will remember, and turn to the LORD.
[narrator] You can turn to the One who stayed."""),
}
import judge_words_r1 as J  # reuses in_kjv (prints r1 table on import; harmless)
res = {}
for k, (src, txt) in CANDS.items():
    body = re.sub(r"\[(?:Psalms?|Matthew|John|Luke) [\d:]+\]", "", txt)
    clean = re.sub(r"\[(narrator|david|mocker)\]", "", body)
    quotes = re.findall(r"\"([^\"]+)\"", clean)
    bad = [q for q in quotes if not J.in_kjv(q)]
    res[k] = dict(words=len(clean.split()), secs=round(len(clean.split()) / 2.75, 1), non_verbatim=bad, source=src)
    (D / ("cand_%s.md" % k)).write_text(txt, encoding="utf-8")
json.dump(res, open(D / "cands_check.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(res, indent=1))
# blind pack: shuffled labels
LAB = {"C": "X", "A": "Y", "B": "Z"}
inv = {v: k for k, v in LAB.items()}
pack = """# FILM-ONLY PACK: THREE CANDIDATE NARRATIONS FOR ONE SHORT (labels X, Y, Z)
Each is the narration of a 60-70 second vertical Bible short (YouTube Shorts / TikTok), watched worldwide. Comic-style pictures; the quoted Bible lines also appear in speech balloons; the first on-screen card reads: WHO WROTE THE MOCKERY?
Voices: [narrator], [david] (David's Psalm words), [mocker] (the crowd's Matthew taunts). Bible quotes are KJV. Quote verses for checking are at the end.
You are judging three different versions of the same short. They share the same Bible lines.

"""
for lab in "XYZ":
    pack += "## VERSION %s\n%s\n\n" % (lab, CANDS[inv[lab]][1])
pack += "## KJV TEXT SUPPLIED (authority)\n" + re.sub(r"\n+$", "", (R1 / "pack.md").read_text(encoding="utf-8").split("## KJV text you may quote (the only authority)")[1].split("## OUTPUT FORMAT")[0])
(D / "pack.md").write_text(pack, encoding="utf-8")
L = {k: v for k, v in {
 "judge": ["JUDGE, NO HAT", "Judge all three versions for the whole worldwide audience. For EACH version give the answers to the five questions in one or two lines each (who for, main takeaway, global audience, biblically accurate, best version), a 0-10 score and a curiosity-gap score. Then RANK X/Y/Z and say what to take from the others. Quote lines by version and paragraph."],
 "newcomer": ["TOTAL NEWCOMER", "You have never opened a Bible and know nothing about Jesus beyond the pack. English is your second language, on a phone. For EACH version: say who/what/why in your own words, every word or line you could not follow, 0-10. Then RANK X/Y/Z."],
 "bible": ["BIBLE FACT-CHECKER", "Check EVERY claim in EACH version against the supplied KJV text: RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG, quoting the line. Also check quotes are verbatim. Score each 0-10, RANK X/Y/Z."],
 "hook": ["HOOK AND RETENTION", "For EACH version judge the first 5 seconds after the card, pacing, where the weakest 10 seconds are, and give odds with error bars for watching to the end. Score each 0-10 and RANK X/Y/Z."],
 "global": ["SECOND-LANGUAGE READER", "For EACH version quote every word or idiom that would fail in translation or on a small screen, say who is served and who is not, anything that could offend. Score each 0-10 and RANK X/Y/Z."]}.items()}
(D / "lenses.json").write_text(json.dumps(L, indent=1), encoding="utf-8")
(D / "format.txt").write_text("OUTPUT FORMAT (Markdown, max ~700 words): ## PER VERSION (X, Y, Z: your answers, score /10) ## RANKING (best to worst, one reason) ## WHAT TO TAKE FROM THE OTHERS ## ANY ACCURACY PROBLEM (quote it)", encoding="utf-8")
(D / "header.txt").write_text("You are ONE independent, hostile voice on a review panel (you have not seen the other voices). Everything is in the EVIDENCE PACK. Do not ask questions. Do not use tools. Output the review text only.\n", encoding="utf-8")
(D / "label_key.json").write_text(json.dumps(LAB), encoding="utf-8")
print("pack ok")
