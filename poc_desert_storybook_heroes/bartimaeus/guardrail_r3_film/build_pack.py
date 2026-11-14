"""Build the FILM-ONLY blind pack for the finished-film guardrail panel (round 3) and one prompt per seat.
Seat preambles + output format are reused from guardrail_r2; only the EVIDENCE PACK is replaced. Leak-checked."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
R2 = HERE.parent / "guardrail_r2"
lines = (HERE.parent / "score_panel" / "_timed_lines.txt").read_text(encoding="utf-8").strip().splitlines()
SHOTS = [  # start-end s, picture (plain description), on-screen words
 (0.0, 3.0, "A blind beggar on the ground, arms out, eyes shut, crying out. Feet of a crowd behind him. A dark painted edge frames the picture. Red rings ripple from his mouth.", "JESUS, THOU SON OF DAVID, / HAVE MERCY ON ME. (rough red brush letters, each word bigger)"),
 (3.0, 5.0, "People in the crowd hush him, one with a finger to his lips. He holds out a bowl.", "Be quiet! (three times, getting bigger)"),
 (5.0, 10.0, "He sits by the road outside a walled city gate. A crowd walks out of the gate.", "Bartimaeus / a blind beggar / Jericho"),
 (10.0, 15.0, "Jesus walks at the front of a big crowd.", "“SON OF DAVID” means God's promised King"),
 (15.0, 20.8, "A far view of a city on a hill. A dotted road line draws itself up to a small cross mark on a hill.", "Jerusalem / Would He stop for a beggar?"),
 (20.8, 26.6, "He cries out again, hands cupped at his mouth. Big rings spread. At the end everything freezes.", "THOU SON OF DAVID, / HAVE MERCY ON ME. (red, bigger, breaking past the dark edge)"),
 (26.6, 30.0, "Jesus stands still on a paved road; the crowd around Him is blurred and frozen. The music stops.", "And Jesus | stood still  (old Bible type, split by His body)  Mark 10:49"),
 (30.0, 33.7, "Jesus holds out His arm, calling. Two people stand near.", "He stopped / for one man."),
 (33.7, 38.4, "He flings off his red cloak and stumbles forward, arms out.", "He came."),
 (38.4, 41.8, "Jesus bends toward him. He stands close, eyes still shut.", "What wilt thou that I / should do unto thee?  (on a patch of bare paper, green ink)"),
 (41.8, 44.8, "Close-up of his face: eyes shut, a tear, hands pressed together.", "Lord, / that I / might / receive / my / sight.  (“sight.” is an empty outline)"),
 (44.8, 49.0, "Jesus beside him, smiling.", "Go thy way; thy faith / hath made thee whole.  (bare paper, green ink)"),
 (49.0, 56.0, "The dark edge lifts and warm gold light blooms. Close-up: his eyes are open, looking up at Jesus, tears, smiling.", "At once he could / see.  (“see.” big and gold)"),
 (56.0, 61.0, "Seen from behind: he walks after Jesus and the crowd up a road. Gold dust drifts up.", "He followed Jesus / up the road to Jerusalem."),
 (61.0, 65.0, "A lone empty cross on a hill at sunset, a city below.", "He died / for our sins."),
 (65.0, 69.0, "An empty tomb, linen cloth inside, morning light.", "He rose to life."),
 (69.0, 79.2, "Jesus and him walk side by side up the road toward the sunset, seen from behind. The last 3 seconds hold with music.", "Jesus stood still / for one man.  Mark 10:46-52"),
]
spoken = []
for ln in lines:
    m = re.match(r"\s*([\d.]+)-\s*([\d.]+)\s+\[(\w+)\]\s+(.*)", ln)
    spoken.append((float(m[1]), float(m[2]), m[3], m[4]))
out = ["EVIDENCE PACK — a FINISHED 9:16 YouTube Short, 79 seconds (spoken words end at 76 s, then a 3-second hold).",
       "Bible story told with animated storybook paintings, music (oud, drum, felt piano, strings) and sound effects, plus on-screen lettering.",
       "Voices: narrator, Jesus, Bartimaeus. Title and description not written yet. Based on Mark 10:46-52 (with Mark 10:32-34 and 1 Corinthians 15:3-4 for the ending).",
       "", "SHOT BY SHOT (what the viewer SEES, READS and HEARS). Spoken lines are numbered:", ""]
n = 0
for a, b, pic, txt in SHOTS:
    out.append(f"[{a:4.1f}-{b:4.1f} s] PICTURE: {pic}")
    out.append(f"           ON SCREEN: {txt}")
    for s in spoken:
        if a - 0.3 <= s[0] < b - 0.3:
            n += 1
            out.append(f"           {n}. [{s[2]}] {s[3]}")
    out.append("")
assert n == len(spoken), (n, len(spoken))
pack = "\n".join(out)
LEAK = re.compile(r"\b(v\d|draft|revised|earlier version|previous|fable|panel|seat|round)\b", re.I)
bad = [l for l in pack.splitlines() if LEAK.search(l)]
if bad: sys.exit("LEAK: " + repr(bad))
(HERE / "pack.md").write_text(pack, encoding="utf-8")
for p in sorted(R2.glob("prompt_*.md")):
    t = p.read_text(encoding="utf-8")
    i, j = t.index("EVIDENCE PACK"), t.index("OUTPUT FORMAT")
    t = t[:i] + pack + "\n\n" + t[j:]
    t = t.replace("judge the SPOKEN WORDS", "judge the whole film").replace("about 65 seconds", "79 seconds")
    t = t.replace("## 3. GLOBAL AUDIENCE (", "## 3. GLOBAL AUDIENCE (include the ON-SCREEN words and pictures; ")
    (HERE / p.name).write_text(t, encoding="utf-8")
print("pack ok:", n, "spoken lines,", len(SHOTS), "shots")
