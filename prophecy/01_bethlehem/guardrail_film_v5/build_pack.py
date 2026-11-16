"""FILM-ONLY blind pack, 5-guardrail panel on the LOCKED film (film/BETHLEHEM_FINAL_v3.mp4, words v3, comic motion,
orchestral score). Same seats/questions as guardrail_film/ (roles from bartimaeus/guardrail_r2). Shots described from
a frame sheet of the real film (_frames/sheet.png). Spoken times from audio_v3/narration_v3.words.json. Leak-checked."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parent
R2 = EP.parents[1] / "poc_desert_storybook_heroes" / "bartimaeus" / "guardrail_r2"

SPOKEN = [
 (0.00, "narrator", "The Bible experts knew where the King would be born. Did they go?"),
 (3.92, "narrator", "God's prophet Micah named a small town: Bethlehem. God promised a King from there:"),
 (9.57, "prophet", "ruler in Israel."),
 (10.97, "narrator", "It goes on:"),
 (12.19, "prophet", "from everlasting."),
 (13.26, "narrator", "Bethlehem would be His birthplace, not His beginning. There, God's promise came true: Jesus, the King, was born. Wise men came asking for this King. King Herod asked the experts."),
 (25.32, "scribe", "In Bethlehem of Judaea."),
 (27.96, "narrator", "Bethlehem was close by."),
 (30.56, "narrator", "The Bible never says the experts went. The wise men went, and found the child."),
 (36.56, "narrator", "Jesus grew up in Galilee. Later, people argued: can the King come from Galilee? The promise said Bethlehem. He was born there."),
 (44.77, "narrator", "But Jesus came much farther. He came down from heaven. He died for our sins. On the third day, He rose from the dead."),
 (53.14, "narrator", "Before anyone went to Him, He came to us."),
]
SHOTS = [
 (0.0, 3.9, "A comic-book page of panels. Top: Jewish scholars in prayer shawls lean over an open scroll by torchlight. Middle: close-up of one stern scholar raising a finger. Bottom: a dark night road winding to a far hill town, labelled BETHLEHEM.", "read-along lines / big comic letters: DID THEY GO? ('GO?' in gold)"),
 (3.9, 13.2, "The old prophet Micah, close by lamplight; a parchment scroll strip over a sunlit hill town. The scroll writes 'ruler in Israel.' then, in gold, 'from everlasting.'", "name tag MICAH, chip MICAH 5:2 / read-along lines"),
 (13.2, 16.6, "The prophet on a hilltop at sunset, pointing at a small town; a dashed frame drawn around the town.", "read-along: Bethlehem would be His birthplace, not His beginning."),
 (16.6, 21.2, "A stable at night: Mary and Joseph by a baby in a manger; the dashed frame turns solid gold around this panel. Below it a dark starry sky with one star.", "read-along: There, God's promise came true: Jesus, the King, was born. / CAME TRUE stamp"),
 (21.2, 27.9, "Wise men on camels (brief); King Herod on a throne points at the scholars; the scholars before him, one holding a scroll; close-ups of the king's hard face.", "caps KING HEROD, JERUSALEM / read-along lines / speech balloon from a scholar: In Bethlehem of Judaea. tags A SCRIBE, MATTHEW 2:5"),
 (27.9, 36.5, "A flat hand-drawn map: Jerusalem and Bethlehem joined by a short road with a gold star on Bethlehem; the scholars at their scroll; the empty night road with hollow white footprints; the music stops for about one second; then the footprints turn gold one by one down to Bethlehem; wise men on camels.", "read-along: Bethlehem was close by. / The Bible never says the experts went. / big comic letters WENT / The wise men went, and found the child."),
 (36.5, 44.7, "Mary holding the child wipes away to a full-page hand-drawn map in blue and gold: NAZARETH far in the north inside a dashed region labelled GALILEE; a big gold '?' pops over Galilee; the camera travels south past JERUSALEM to BETHLEHEM, whose star and frame turn gold, with a burst on 'born'.", "read-along lines"),
 (44.7, 53.1, "A starry sky with a galaxy over a dark sea (heaven). Three crosses on a hill under a storm. An open, empty tomb glowing from inside, grave cloths on the stone.", "read-along lines"),
 (53.1, 59.0, "Jesus standing at dawn in a garden, arms open, a warm glow around Him; a gold border closes around the page. Holds about 3 seconds after the last word as the music finishes.", "read-along: Before anyone went to Him, He came to us. / end card: PROMISED. (cream) CAME TRUE. (gold)"),
]
out = ["EVIDENCE PACK — a FINISHED 9:16 YouTube Short, 59.0 seconds (spoken words end at 56 s, then a 3-second hold).",
       "Bible story told as an animated comic-book page (panels slam in, page whips), hand-drawn map doodles, on-screen read-along lettering, an orchestral film score (strings, French horns, timpani; a horn tune left unfinished until the very end) and sound effects.",
       "Voices: narrator, an old prophet voice, a scribe voice. Title and description not written yet. Based on Micah 5:2, Matthew 2:1-11 and Luke 2:1-7 (also John 7:41-43; ending: John 6:38, 1 Corinthians 15:3-4).",
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

KJV = (EP / "words" / "KJV.txt").read_text(encoding="utf-8").strip() + """

## John 6:38
For I came down from heaven, not to do mine own will, but the will of him that sent me.

## 1 Corinthians 15:3-4
For I delivered unto you first of all that which I also received, how that Christ died for our sins according to the scriptures; And that he was buried, and that he rose again the third day according to the scriptures:
"""
EXTRA = "## NEW TO YOU (as a regular churchgoer: what here had you NOT heard before? quote it. 0-10)\n## PROMISE KEPT (in your own words: who made what promise, how long before, and what came true? did the film make it feel like a promise kept, or only a story about who went? 0-10)\n"
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
