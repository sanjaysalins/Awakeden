"""FILM-ONLY blind pack, 5-guardrail panel on film/NAZARETH_FINAL_v1.mp4 (words v6, comic pages, cello score, SFX). Pattern = prophecy/01_bethlehem/guardrail_film_v3.
Shots described from build/contact_v5.jpg + the v5 page plan; spoken times from audio/timeline_v6.json. Leak-checked."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parent
R2 = EP.parents[1] / "poc_desert_storybook_heroes" / "bartimaeus" / "guardrail_r2"
SPOKEN = [
 (0.00, "narrator", "Jesus stopped reading in the middle of a sentence."),
 (2.80, "narrator", "In Nazareth, His home town, He read God's promise of someone sent with good news for the poor, freedom for prisoners, and a time of God's welcome."),
 (11.59, "narrator", "The prophet Isaiah's sentence goes on:"),
 (13.98, "isaiah", "and the day of vengeance of our God."),
 (16.92, "narrator", "He left the day of vengeance unread, and sat down."),
 (20.81, "jesus", "This day is this scripture fulfilled in your ears."),
 (25.54, "narrator", "He knew what His town would say:"),
 (27.51, "jesus", "Physician, heal thyself."),
 (30.18, "narrator", "He reminded them God once sent help to foreigners, not to them. Furious, they led Him to a cliff to throw Him down. He walked right through them."),
 (40.47, "narrator", "Later, at the cross, leaders mocked:"),
 (43.36, "leader", "He saved others; let him save himself."),
 (46.12, "narrator", "This time, He stayed, and gave His life."),
 (50.24, "narrator", "He stopped reading at the welcome. It is still open, for you, today."),
]
SHOTS = [
 (0.0, 2.8, "A comic-book page of two panels: Jesus in a lamp-lit stone synagogue, lifting His eyes from an open scroll; below, an old white-bearded prophet writing on a scroll at night. The top panel pushes in to fill the screen.", "big comic letters: HE STOPPED READING / read-along line"),
 (2.8, 11.5, "Panels slam in: a hillside stone village at morning; hands passing a scroll; Jesus standing reading to seated men; a poor widow looking up with hope; a broken iron shackle on a prison floor in a shaft of light; men listening. Soft light rays on the last word.", "read-along lines"),
 (11.5, 16.9, "The old prophet Isaiah under a dark stormy sky, the page goes hushed and dotted; Jesus' hands holding the scroll; men whispering.", "read-along line / speech tag: ISAIAH, ISAIAH 61:2 (dashed frame)"),
 (16.9, 20.8, "Hands roll the scroll closed; Jesus seated, calm, in the synagogue.", "read-along line"),
 (20.8, 25.5, "ONE full-screen picture: Jesus seated, one hand open, looking out at the room. Nothing moves, nothing is drawn.", "tag: JESUS, LUKE 4:21"),
 (25.5, 30.1, "An older villager frowning, doubtful; a row of stern men; Jesus' face, close.", "read-along line / tag: JESUS, LUKE 4:23"),
 (30.1, 35.4, "An old prophet (Elijah) at a mud-brick door by the sea with a foreign widow and her son; she holds a jar now full of flour. Then the hillside village and the doubtful villager.", "read-along line"),
 (35.4, 38.4, "A furious crowd grabs Jesus' arms and pushes Him up a rocky slope to a cliff edge above the village; Jesus calm. Below: stern staring men.", "read-along line in a spiky box"),
 (38.4, 40.4, "Jesus walks calmly toward us through the parted, stunned crowd; below, one angry face close up.", "read-along line"),
 (40.4, 49.9, "Dusk on a rocky hill outside a city wall: Jesus on a wooden cross; three richly robed leaders below point up and laugh (shown in a second panel), then the cross alone, still and quiet. Nothing drawn.", "read-along lines / tag: LEADER, LUKE 23:35"),
 (49.9, 59.1, "Full screen: Jesus at golden sunset on the hill above Nazareth, reaching His open hand toward the viewer. Holds 3 seconds after the last word while the music lands and fades.", "read-along lines"),
]
out = ["EVIDENCE PACK - a FINISHED 9:16 YouTube Short, 59.1 seconds (spoken words end at 56 s, then a 3-second hold).",
       "Bible story told as an animated comic-book page (panels slam in, pages turn), on-screen read-along lettering, an orchestral film score (solo cello, strings, harp; a cello tune that keeps stopping one note short and lands only at the very end) and soft sound effects.",
       "Voices: narrator, an old prophet voice, Jesus, a mocking leader. Title and description not written yet. Based on Isaiah 61:1-2 and Luke 4:16-30 (ending: Luke 23:35, 46).",
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
KJV = (EP / "words" / "v6" / "KJV.txt").read_text(encoding="utf-8").strip()
EXTRA = ("## NEW INSIGHT (what did the film show you that most people who know this story have never noticed? is it true to the KJV? 0-10)\n")
for p in sorted(R2.glob("prompt_*.md")):
    t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    i = t.index("\nEVIDENCE PACK"); j = t.index("OUTPUT FORMAT")
    head = t[:i]
    if "KJV TEXT" in head:
        head = head[:head.index("KJV TEXT")] + "KJV TEXT (the only authority; quote it):\n" + KJV + "\n"
    fmt = t[j:].replace("judge the SPOKEN WORDS", "judge the whole film").replace("## THREE SMALLEST FIXES", EXTRA + "## THREE SMALLEST FIXES")
    fmt = fmt.replace("## 3. GLOBAL AUDIENCE (", "## 3. GLOBAL AUDIENCE (include the ON-SCREEN words and pictures; ")
    head = head.replace("Jesus, David, Jericho or Jerusalem", "Jesus, Isaiah, Nazareth or Elijah")
    body = head + "\n" + pack + "\n\n" + fmt
    for w in ("Bartimaeus", "Jericho", "79 s", "65 seconds"):
        assert w not in body, (p.name, w)
    (HERE / p.name).write_text(body, encoding="utf-8")
print("pack ok:", n, "spoken lines,", len(SHOTS), "shots")
