"""FILM-ONLY blind pack, 5-guardrail panel on Immanuel v2 (film/IMMANUEL_SCORED_v2.mp4: words v2, comic motion,
orchestral score). Copied from prophecy/01_bethlehem/guardrail_film_v3/build_pack.py (same seats/questions, roles from
bartimaeus/guardrail_r2). Shots from film/_contact_v2.png. Spoken times from audio_v2/timeline.json. Leak-checked."""
import re, sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
EP = HERE.parent
R2 = EP.parents[1] / "poc_desert_storybook_heroes" / "bartimaeus" / "guardrail_r2"
SPOKEN = [(x["start"], x["who"], x["text"]) for x in json.loads((EP / "audio_v2" / "timeline.json").read_text(encoding="utf-8"))]
SHOTS = [
 (0.0, 12.0, "A comic-book page of 3 panels, the camera pans down. Top: an old scroll by a small oil lamp. Middle: King Ahaz (gold crown, red robe) grips the city wall of Jerusalem at night, afraid; enemy campfires on the dark hills. Bottom: the prophet Isaiah talks with the king by a stone water channel; a boy stands with Isaiah.", "big comic word: NO. / tag: KING AHAZ / read-along lines"),
 (12.0, 17.7, "Night, a stone palace room lit by oil lamps. The king pushes an open chest full of gold and silver temple bowls toward two kneeling messengers in dusty travel cloaks, who lift it by its poles. A road leads away into the hills.", "big comic word with an impact burst: SAVE ME / tag: 2 KINGS 16:7 / read-along lines"),
 (17.7, 24.7, "The prophet Isaiah alone on a hill at dawn, hand raised, speaking, the city behind him.", "big comic word: IMMANUEL with a small label under it: GOD WITH US / tag: ISAIAH 7:14 / read-along"),
 (24.7, 31.7, "Page of 3 panels: young Mary at a doorway in a village; Joseph sitting troubled at night by a lamp; Joseph asleep on a mat.", "tag: 700 YEARS LATER / read-along lines"),
 (31.7, 44.2, "A tall angel of soft white light, no wings, stands over Joseph asleep on his mat, one hand open toward him.", "big comic words: FEAR NOT, then JESUS / tag: MATTHEW 1:20-21 / read-along lines"),
 (44.2, 51.9, "Page of 3 panels: a man (Matthew) writing on a scroll by lamplight; Joseph holding the newborn baby; Mary and Joseph with the baby by a lamp.", "big comic words: HE SAVES, then GOD WITH US / read-along lines"),
 (51.9, 58.0, "Page of 3 panels, camera pans down: the baby in a manger; three crosses on a hill under storm clouds; an open, empty tomb glowing from inside, grave cloths inside.", "tags: AT THE CROSS, THE THIRD DAY / read-along lines"),
 (58.0, 64.2, "The risen Jesus, with a soft gold glow around Him, walks toward us down a grassy path by a lake, smiling, His arm around a young man; friends walk beside them. Holds about 3 seconds after the last word as the music finishes.", "read-along: I am with you always. (the voice says the KJV 'alway') / end card in a gold frame: GOD WITH US / MATTHEW 1:23"),
]
out = ["EVIDENCE PACK — a FINISHED 9:16 YouTube Short, 64.2 seconds (spoken words end at 61.2 s, then a 3-second hold).",
       "Bible story told as animated comic-book pages and single comic panels (big comic words slam in), on-screen read-along lettering, an orchestral film score (strings, French horns, a little timpani; a 4-note tune left unfinished until the very end) and sound effects.",
       "Voices: narrator, an old prophet voice, an angel voice, the voice of Jesus. Title and description not written yet. Based on Isaiah 7:1-14, 2 Kings 16:5-8 and Matthew 1:18-25 (ending: 1 Corinthians 15:3-4, Matthew 28:20).",
       "", "SHOT BY SHOT (what the viewer SEES, READS and HEARS). Spoken lines are numbered:", ""]
n = 0
for a, b, pic, txt in SHOTS:
    out.append(f"[{a:4.1f}-{b:4.1f} s] PICTURE: {pic}")
    out.append(f"           ON SCREEN: {txt}")
    for t, who, line in SPOKEN:
        if a - 0.3 <= t < b - 0.3:
            n += 1; out.append(f"           {n}. [{who}] {line}")
    out.append("")
assert n == len(SPOKEN), (n, len(SPOKEN))
pack = "\n".join(out)
LEAK = re.compile(r"\b(v\d|draft|revised|earlier version|previous|fable|review panel|seat|round|locked|insight|hunt)\b", re.I)
bad = [l for l in pack.splitlines() if LEAK.search(l)]
if bad: sys.exit("LEAK: " + repr(bad))
(HERE / "pack.md").write_text(pack, encoding="utf-8")
KJV = (EP / "insight_hunt" / "KJV_HUNT.txt").read_text(encoding="utf-8") + "\n" + (EP / "words" / "KJV.txt").read_text(encoding="utf-8")
EXTRA = "## PROMISE KEPT (in your own words: who made what promise, how long before, and what came true? did the film make it feel like a promise kept? 0-10)\n"
for p in sorted(R2.glob("prompt_*.md")):
    t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    i = t.index("\nEVIDENCE PACK"); j = t.index("OUTPUT FORMAT")
    head = t[:i]
    if "KJV TEXT" in head:
        head = head[:head.index("KJV TEXT")] + "KJV TEXT (the only authority; quote it):\n" + KJV + "\n"
    fmt = t[j:].replace("judge the SPOKEN WORDS", "judge the whole film").replace("## THREE SMALLEST FIXES", EXTRA + "## THREE SMALLEST FIXES")
    fmt = fmt.replace("## 3. GLOBAL AUDIENCE (", "## 3. GLOBAL AUDIENCE (include the ON-SCREEN words and pictures; ")
    head = head.replace("Jesus, David, Jericho or Jerusalem", "Jesus, Isaiah, Ahaz, Assyria or Jerusalem")
    body = head + "\n" + pack + "\n\n" + fmt
    for w in ("Bartimaeus", "Jericho", "79 s", "65 seconds"):
        assert w not in body, (p.name, w)
    (HERE / p.name).write_text(body, encoding="utf-8")
print("pack ok:", n, "spoken lines,", len(SHOTS), "shots")
