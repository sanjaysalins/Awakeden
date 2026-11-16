"""FILM-ONLY blind pack, 5-guardrail panel on the LOCKED film (film/BETHLEHEM_FINAL_v3.mp4, words v3, comic motion,
orchestral score). Same seats/questions as guardrail_film/ (roles from bartimaeus/guardrail_r2). Shots described from
a frame sheet of the real film (_frames/sheet.png). Spoken times from audio_v3/narration_v3.words.json. Leak-checked."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parent
R2 = EP.parents[1] / "poc_desert_storybook_heroes" / "bartimaeus" / "guardrail_r2"

SPOKEN = [
 (0.00, "narrator", "The Bible experts knew where the King would be born."),
 (3.32, "narrator", "Did they go?"),
 (4.10, "narrator", "About seven hundred years earlier, a prophet called Micah, a man who spoke God's message, named a small town: Bethlehem."),
 (12.66, "narrator", "God promised a King from there. Micah called Him"),
 (15.99, "prophet", "ruler in Israel."),
 (17.45, "narrator", "Mary and Joseph lived far away. A tax order sent them to Bethlehem."),
 (21.96, "narrator", "There, God's promise came true: Jesus, the King, was born."),
 (27.30, "narrator", "Wise men reached Jerusalem, asking where this King was. Herod, the king there, asked the experts."),
 (33.84, "scribe", "In Bethlehem of Judaea."),
 (36.44, "narrator", "Bethlehem was close by."),
 (39.04, "narrator", "The Bible never says the experts went."),
 (42.12, "narrator", "The wise men went, and found the child."),
 (45.16, "narrator", "But Jesus came much farther. He came down from heaven. He died for our sins. On the third day, He rose from the dead."),
 (53.50, "narrator", "Before anyone went to Him, He came to us."),
]
SHOTS = [
 (0.0, 4.0, "A comic-book page of panels. Top: Jewish scholars in prayer shawls lean over an open scroll by torchlight. Middle: close-up of one stern scholar raising a finger. Bottom: a dark night road winding to a far hill town, labelled BETHLEHEM.", "read-along: The Bible experts knew where the King would be born. / then big comic letters: DID THEY GO? ('GO?' in gold)"),
 (4.0, 12.6, "Panels: an old prophet with a staff on a hilltop at sunset, pointing; a close-up of the prophet by lamplight; a small hill town at sunset. A dashed frame is drawn around the town.", "yellow caption box: ABOUT 700 YEARS EARLIER / name tag: MICAH / read-along lines"),
 (12.6, 17.4, "The prophet's face, close; the town again with the dashed frame. A parchment strip shows the quoted words.", "read-along: God promised a King from there. Micah called Him ruler in Israel.  tags: MICAH, MICAH 5:2"),
 (17.4, 22.0, "A full-page flat hand-drawn map in blue and gold: NAZARETH far in the north, JERUSALEM (a walled city), BETHLEHEM in the south, a sea and a river. Two small walkers go down a long dashed road south. A tax paper slides in.", "map labels / read-along: Mary and Joseph lived far away. A tax order sent them to Bethlehem."),
 (22.0, 27.3, "Comic panels: a stable at night, Mary and Joseph by a baby in a manger, a lamp, a donkey and an ox; the dashed frame turns solid gold around this panel. Below: wise men on camels crossing a night desert. Then a king on a throne, close.", "read-along: There, God's promise came true: Jesus, the King, was born. / tabs: MICAH 5:2, CAME TRUE"),
 (27.3, 36.4, "Panels: King Herod on a throne points at the scholars; the scholars stand before him, one holding a scroll; close-ups of the king's hard face.", "tag: JERUSALEM / read-along lines / speech balloon from the scholar: In Bethlehem of Judaea.  tags: A SCRIBE, MATTHEW 2:5"),
 (36.4, 42.0, "The map, close: Jerusalem and Bethlehem joined by a short road with a gold star on Bethlehem. Then the scholars at their scroll again and the empty night road; hollow white footprints sit on the road. The music stops for about one second.", "read-along: Bethlehem was close by. / The Bible never says the experts went. ('never' underlined)"),
 (42.0, 45.0, "Wise men on camels; the map: footprints on the short road turn gold one by one down to Bethlehem; the night road with gold footprints.", "big comic letters: WENT / read-along: The wise men went, and found the child."),
 (45.0, 53.4, "A starry sky with a galaxy over a dark sea (heaven). Three crosses on a hill under a storm. An open, empty tomb glowing from inside, grave cloths on the stone.", "read-along lines"),
 (53.4, 59.5, "Jesus standing at dawn in a garden, arms open, a warm glow around Him; a gold border closes around the page. Holds about 3 seconds after the last word as the music finishes.", "read-along: Before anyone went to Him, He came to us. / end card: PROMISED. (cream) CAME TRUE. (gold)"),
]
out = ["EVIDENCE PACK — a FINISHED 9:16 YouTube Short, 59.5 seconds (spoken words end at 56 s, then a 3-second hold).",
       "Bible story told as an animated comic-book page (panels slam in, page whips), hand-drawn map doodles, on-screen read-along lettering, an orchestral film score (strings, French horns, timpani; a horn tune left unfinished until the very end) and sound effects.",
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
LEAK = re.compile(r"\b(v\d|draft|revised|earlier version|previous|fable|review panel|seat|round|locked)\b", re.I)
bad = [l for l in pack.splitlines() if LEAK.search(l)]
if bad:
    sys.exit("LEAK: " + repr(bad))
(HERE / "pack.md").write_text(pack, encoding="utf-8")

KJV = (EP / "words" / "KJV.txt").read_text(encoding="utf-8").split("## John 7:40-43")[0].strip() + """

## John 6:38
For I came down from heaven, not to do mine own will, but the will of him that sent me.

## 1 Corinthians 15:3-4
For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:
"""
EXTRA = "## PROMISE KEPT (in your own words: who made what promise, how long before, and what came true? did the film make it feel like a promise kept, or only a story about who went? 0-10)\n"
for p in sorted(R2.glob("prompt_*.md")):
    t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    i = t.index("\nEVIDENCE PACK"); j = t.index("OUTPUT FORMAT")
    head = t[:i]
    if "KJV TEXT" in head:
        head = head[:head.index("KJV TEXT")] + "KJV TEXT (the only authority; quote it):\n" + KJV + "\n"
    fmt = t[j:].replace("judge the SPOKEN WORDS", "judge the whole film").replace("## THREE SMALLEST FIXES", EXTRA + "## THREE SMALLEST FIXES")
    fmt = fmt.replace("## 3. GLOBAL AUDIENCE (", "## 3. GLOBAL AUDIENCE (include the ON-SCREEN words and pictures; ")
    head = head.replace("Jesus, David, Jericho or Jerusalem", "Jesus, Micah, Herod, Bethlehem or Jerusalem")
    body = head + "\n" + pack + "\n\n" + fmt
    for w in ("Bartimaeus", "Jericho", "79 s", "65 seconds"):
        assert w not in body, (p.name, w)
    (HERE / p.name).write_text(body, encoding="utf-8")
print("pack ok:", n, "spoken lines,", len(SHOTS), "shots")
