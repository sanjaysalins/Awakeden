"""FILM-ONLY blind pack for the finished-film 5-guardrail panel (Born in Bethlehem, BETHLEHEM_FINAL_v1.mp4).
Seat roles copied from poc_desert_storybook_heroes/bartimaeus/guardrail_r2 (r3's builder had dropped the role text;
fixed here by splicing the pack in at the line-start 'EVIDENCE PACK' block). Extra question: PROMISE KEPT.
Leak-checked: no drafts, versions, designers or panel words in the pack."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
R2 = HERE.parents[2] / "poc_desert_storybook_heroes" / "bartimaeus" / "guardrail_r2"

SPOKEN = [
 (0.00, "narrator", "The Bible experts knew where the King would be born."),
 (3.10, "narrator", "Did they go?"),
 (3.90, "narrator", "About seven hundred years earlier, a prophet called Micah, a man who spoke God's message, named a small town: Bethlehem."),
 (12.64, "narrator", "Out of it, he said, a ruler would come,"),
 (15.82, "prophet", "that is to be ruler in Israel."),
 (17.86, "narrator", "Mary and Joseph lived far away. A tax order sent them to Bethlehem. There, Jesus was born."),
 (25.18, "narrator", "Wise men from the east came asking for the one born King. King Herod asked the experts where."),
 (32.24, "scribe", "In Bethlehem of Judaea."),
 (34.80, "narrator", "Bethlehem was close by."),
 (37.44, "narrator", "The Bible never says the experts went."),
 (40.52, "narrator", "The wise men went, and found the child."),
 (43.52, "narrator", "But Jesus had come much farther. He came down from heaven. He died for our sins. He rose again the third day."),
 (52.50, "narrator", "Before anyone went to Him, He came to us."),
]
SHOTS = [
 (0.0, 3.9, "Old Jewish scholars in prayer shawls lean over an open scroll by torchlight. Close-up: one stern scholar raises a finger. A night road; a gold ring and star are drawn around a far town; a few hollow sandal prints sit on the road.", "The Bible experts knew where the King would be born. (read-along) / DID THEY GO? (big comic letters, 'GO?' in gold)"),
 (3.9, 5.9, "A parchment scroll rolls across. A sun and moon wheel turns backwards over a time line; an arrow points back.", "ABOUT 100 ... 700 YEARS EARLIER (number counts up) / red stamp: A PROPHECY"),
 (5.9, 15.8, "An old prophet with a staff on a hilltop at sunset, pointing at a small hill town; a gold ring and crown are drawn over the town. Close-up of the prophet's face by lamplight; the lamp flame grows.", "name tag: Micah / read-along lines"),
 (15.8, 17.8, "The prophet's face; a parchment scroll opens and the words write themselves in old type.", "that is to be ruler in Israel.  tag: MICAH 5:2"),
 (17.8, 22.7, "A hand-drawn map of the land unfolds: Nazareth in the north, Bethlehem in the south, a sea and a river. Two small walkers go down a dashed road from Nazareth to Bethlehem. A small sealed paper (the tax order) appears. A gold star lands on Bethlehem.", "Nazareth / Bethlehem (map labels)"),
 (22.7, 27.8, "The map folds away. A stable at night: Mary and Joseph kneel by a baby in a manger, a lamp, a donkey and an ox. Below, wise men ride camels across a night desert.", "There, Jesus was born. / red stamp on the night sky: KEPT ✓  tag: MICAH 5:2 / tag: the east"),
 (27.8, 33.4, "A comic page: a king on a throne points at the scholars; one scholar holds a scroll (circled in gold); close-up of the king's hard face.", "King Herod asked the experts where. / speech balloon from the scholar: In Bethlehem of Judaea.  tags: A SCRIBE, MATTHEW 2:5, MICAH 5:2 (by the circled scroll)"),
 (33.4, 37.4, "The map again, closer: Jerusalem (a walled city) and Bethlehem just below it, joined by a short road. Hollow footprints pop onto the road; one blinks. Nobody walks it. The music stops.", "Bethlehem was close by.  (labels Jerusalem, Bethlehem)"),
 (37.4, 40.5, "Back to the scholars at their scroll; the stern scholar; the empty night road with hollow prints.", "The Bible never says the experts went."),
 (40.5, 43.5, "The map: camels come from the east; the footprints on the short road turn gold one by one down to Bethlehem. A star opens onto Mary holding the child.", "The wise men went, and found the child."),
 (43.5, 51.7, "A starry sky with a galaxy over dark sea (heaven). Three crosses on a hill under a storm. An empty tomb glowing with light from inside.", "read-along lines"),
 (51.7, 59.3, "Jesus standing at dawn in a garden, arms open, a warm glow around Him. Holds to the end (about 3 seconds after the last word, with music).", "Before anyone went to Him, He came to us. / end: PROMISED, THEN KEPT"),
]

out = ["EVIDENCE PACK — a FINISHED 9:16 YouTube Short, 59 seconds (spoken words end at 56 s, then a 3-second hold).",
       "Bible story told with animated comic-book pictures, hand-drawn map doodles, on-screen lettering, music (felt piano and cello) and quiet sound effects.",
       "Voices: narrator, an old prophet voice, a scribe voice. Title and description not written yet. Based on Micah 5:2, Matthew 2:1-11 and Luke 2:1-7 (ending: John 6:38, 1 Corinthians 15:3-4).",
       "", "SHOT BY SHOT (what the viewer SEES, READS and HEARS). Spoken lines are numbered:", ""]
n = 0
for a, b, pic, txt in SHOTS:
    out.append(f"[{a:4.1f}-{b:4.1f} s] PICTURE: {pic}")
    out.append(f"           ON SCREEN: {txt}")
    for t, who, line in SPOKEN:
        if a - 0.3 <= t < b - 0.3:
            n += 1
            out.append(f"           {n}. [{who}] {line}")
    out.append("")
assert n == len(SPOKEN), (n, len(SPOKEN))
pack = "\n".join(out)
LEAK = re.compile(r"\b(v\d|draft|revised|earlier version|previous|fable|panel|seat|round)\b", re.I)
bad = [l for l in pack.splitlines() if LEAK.search(l)]
if bad: sys.exit("LEAK: " + repr(bad))
(HERE / "pack.md").write_text(pack, encoding="utf-8")

KJV = (HERE.parent / "words" / "KJV.txt").read_text(encoding="utf-8").split("## John 7:40-43")[0].strip() + """

## John 6:38
For I came down from heaven, not to do mine own will, but the will of him that sent me.

## 1 Corinthians 15:3-4
For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:
"""
EXTRA = "## PROMISE KEPT (in your own words: who made what promise, how long before, and what came true? did the film make it feel like a promise kept, or only a story about who went? 0-10)\n"
for p in sorted(R2.glob("prompt_*.md")):
    t = p.read_text(encoding="utf-8")
    t = t.replace("\r\n", "\n")
    i = t.index("\nEVIDENCE PACK"); j = t.index("OUTPUT FORMAT")
    head = t[:i]
    if "KJV TEXT" in head:
        head = head[:head.index("KJV TEXT")] + "KJV TEXT (the only authority; quote it):\n" + KJV + "\n"
    fmt = t[j:]
    fmt = fmt.replace("judge the SPOKEN WORDS", "judge the whole film").replace("## THREE SMALLEST FIXES", EXTRA + "## THREE SMALLEST FIXES")
    fmt = fmt.replace("## 3. GLOBAL AUDIENCE (", "## 3. GLOBAL AUDIENCE (include the ON-SCREEN words and pictures; ")
    head = head.replace("Jesus, David, Jericho or Jerusalem", "Jesus, Micah, Herod, Bethlehem or Jerusalem")
    body = head + "\n" + pack + "\n\n" + fmt
    for w in ("Bartimaeus", "Jericho", "79 s", "65 seconds"):
        assert w not in body, (p.name, w)
    (HERE / p.name).write_text(body, encoding="utf-8")
print("pack ok:", n, "spoken lines,", len(SHOTS), "shots")
