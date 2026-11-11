"""Build the BLIND red-team r1 pack for ep16 (finished film) from real files, then leak-check it.
Writes BRIEF.md (image seats), pack.md + lenses.json + format.txt + header.txt (CLI seats via panel_generic.py).
Facts only: spoken words (from the .srt), on-screen text (from _remotion/src/Ep16ChildrenV2.tsx frames / 30),
picture changes (ffmpeg scene detect), a plain shot list, the KJV. No opinions, no earlier panel results."""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
srt = (EP / "swirls_episode_16_let_the_little_children.srt").read_text(encoding="utf-8")

def ts(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

lines = []
for blk in re.split(r"\n\s*\n", srt.strip()):
    p = blk.strip().splitlines()
    a, b = p[1].split(" --> ")
    lines.append((ts(a), ts(b), " ".join(p[2:])))
# merge caption chunks into sentences
sents, cur = [], None
for a, b, t in lines:
    if cur is None:
        cur = [a, b, t]
    else:
        cur[1] = b; cur[2] += " " + t
    if re.search(r'[.?!:]"?$', t.strip()) and not t.strip().endswith(":"):
        sents.append(cur); cur = None
if cur: sents.append(cur)
spoken = "\n".join(f"{a:5.1f}-{b:5.1f}  {t}" for a, b, t in sents)

ONSCREEN = [  # frames from Ep16ChildrenV2.tsx Beat from/to, /30
    (0.0, 5.4, 'handwritten words "Pushed away?" (top)'),
    (3.2, 5.4, 'a small paper slip with handwritten "not now" in quote marks'),
    (13.1, 15.0, 'handwritten "a touch"'),
    (16.6, 20.4, 'the same paper slip "not now", placed near the man with the raised hand'),
    (26.5, 27.9, 'large handwritten "Angry." (lower middle)'),
    (32.6, 38.6, 'blue box "Let the children come to Me." with small "Jesus · Mark 10:14" under it'),
    (51.2, 53.7, 'handwritten "like a little child"'),
    (63.3, 65.0, 'handwritten "a touch" (over the reaching hands)'),
    (65.9, 68.0, 'large blue "His arms."'),
    (69.1, 72.5, 'the paper slip "not now" comes back, then fades'),
    (71.3, 75.7, 'blue box "Look at who Jesus picked up." held to the end'),
]
SHOTS = [
    (0.0, 2.6, "Close-up: a small boy with tears on his face; the side of a grown man's robe at the right edge."),
    (2.6, 7.6, "The boy stands by a wall; two grown men walk away from him down the street."),
    (7.6, 10.6, "A family walks toward us: a father with a laughing small boy on his shoulders, a mother carrying a baby, a little girl holding her hand."),
    (10.6, 15.1, "A mother holds a small child who reaches out his arm."),
    (15.1, 20.9, "A young man in a brown robe holds up his open hand; an older grey-haired man behind him; a mother holding a child; three small, sad children in front."),
    (20.9, 28.1, "Jesus (long dark hair, beard, patched blue tunic) turns and looks; then a close shot, His hand on His chest, frowning."),
    (28.1, 32.7, "Jesus, one hand raised, faces the two men; children near Him."),
    (32.7, 38.8, "Jesus kneels on steps with His arms open; three small children run to Him; He hugs one."),
    (38.8, 43.8, "The two men look surprised; three children walk away from them, hand in hand, down the street."),
    (43.8, 48.2, "Jesus sits on a low wall under an olive tree with four laughing children on and around Him."),
    (48.2, 54.1, "An old woman kneels, laughing, holding hands with a laughing little girl."),
    (54.1, 58.6, "Jesus hugs a small boy and holds him up."),
    (58.6, 63.0, "Jesus, seated, rests His hands on the head of a little girl with closed eyes; two children watch."),
    (63.0, 65.4, "Close-up: a grown-up's hand in a blue sleeve reaches down to a small child's hand."),
    (65.4, 68.4, "Jesus kneels and hugs three laughing children at once."),
    (68.4, 75.7, "Jesus holds two laughing little girls (one on His shoulders, one hugging His side); stone arch, olive tree, warm sun. This is the last picture."),
]
KJV = """Mark 10:13 And they brought young children to him, that he should touch them: and his disciples rebuked those that brought them.
Mark 10:14 But when Jesus saw it, he was much displeased, and said unto them, Suffer the little children to come unto me, and forbid them not: for of such is the kingdom of God.
Mark 10:15 Verily I say unto you, Whosoever shall not receive the kingdom of God as a little child, he shall not enter therein.
Mark 10:16 And he took them up in his arms, put his hands upon them, and blessed them.
(Matthew 19:13-15 and Luke 18:15-17 tell the same event.)"""

shots = "\n".join(f"{a:5.1f}-{b:5.1f}  {t}" for a, b, t in SHOTS)
onscr = "\n".join(f"{a:5.1f}-{b:5.1f}  {t}" for a, b, t in ONSCREEN)
cuts = "2.6, 7.6, 10.6, 15.1, 20.9, 28.1, 32.7, 38.8, 43.8, 48.2, 54.1, 58.6, 63.0, 65.4, 68.4"

PACK = f"""# A finished vertical short film (YouTube Shorts / TikTok / Reels), 75.7 seconds, 9:16

**What it is:** a narrated short for a channel that finds Jesus across the whole Bible, for a worldwide audience (many viewers read English as a second language). Look: warm pencil-and-watercolour storybook pictures; each picture is a short animated clip. Soft piano music. A narrator voice, and a second voice for the words of Jesus. Captions are uploaded as a separate file (not burned in). Story: Mark 10:13-16.

## Spoken words, with the real time each sentence is said (seconds)
{spoken}
(voice ends about 72.8 s; the film runs to 75.7 s)

## Words written on screen (seconds)
{onscr}

## Pictures, in order (seconds)
Picture changes (cuts) at: {cuts} s.
{shots}

## KJV (the only authority for accuracy)
{KJV}
"""

FMT = """OUTPUT (Markdown, max ~700 words, exactly these headings, cite a time in seconds every time):
## 1. WHO IS THIS FOR (one named viewer; who stops, who finishes, who shares; who is NOT served)
## 2. MAIN TAKEAWAY (one sentence a viewer could say back; which line carries it; is it clear?)
## 3. GLOBAL AUDIENCE (who / what / why in my own words; where I got lost or misled, quote it; words that fail in translation)
## 4. BIBLICALLY ACCURATE (spoken words, on-screen words AND pictures, claim by claim: RIGHT / OVERCLAIMED / UNSUPPORTED / WRONG; quote it; cite the verse)
## 5. BEST VERSION POSSIBLE (the ONE highest-value change; score 0-10 against the best short explainer in the world)
## 6. PICTURE vs WORDS (where a picture says something different from, or late for, the voice; anything a viewer could take the wrong way)
## 7. VERDICT: SHIP / FIX / REBUILD, a score 0-10, and odds with error bars that a cold viewer watches to the end
## 8. THE FIVE HIGHEST-VALUE FIXES (ranked). NOTE: the film itself is locked; say which fixes need a re-edit and which can be done in the upload text (title, description, pinned comment) instead."""

HEADER = ("You are ONE independent, HOSTILE reviewer on a blind red team (you have not seen any other review). Assume the film has real flaws and find them. Do not flatter. "
          "Everything you need is in the EVIDENCE PACK below. Do not ask questions. Do not use tools. Output the review text only.\n")

LENSES = {
    "bible": ["THE BIBLE READER AND FACT CHECKER",
              "You know the Bible well. Check every spoken line, every on-screen word and every picture against the KJV above. Section 4 is your main job: go line by line. Check every quoted KJV phrase is word-for-word. Would you send this to your church group?"],
    "hook": ["THE HOOK, RETENTION AND GLOBAL-AUDIENCE ANALYST",
             "You study short-video retention and how English travels for non-native viewers. Walk the film second by second as a scroller: when do they stay, where do they leave, where is the curiosity gap opened and paid? Quote any word that fails for a non-native reader or machine translation. Give calibrated odds with error bars, never certainty."],
}

BRIEF = PACK + f"""
## The pictures themselves (look at them)
Contact sheets, a frame every 2 seconds, time printed above each frame: `sheet_1.jpg` (0-18 s), `sheet_2.jpg` (20-38 s), `sheet_3.jpg` (40-58 s), `sheet_4.jpg` (60-75.2 s). Single frames at full size: `frames/t_XXX.X.jpg`.
Your focus: the five questions below, judged on the WHOLE film (pictures, words, on-screen text) as a cold viewer would meet it.

{FMT}
"""

LEAK = re.compile(r"\b(weak|risk|motif|misread|panel|seat|fable|codex|grok|sonnet|opus|owner|locked by|provisional|known|earlier|lands ~|surprise|guardrail|X5|kingdom of God.{0,20}not explained)\b", re.I)
for name, txt in [("pack.md", PACK), ("BRIEF.md", BRIEF), ("lenses.json", json.dumps(LENSES))]:
    hits = LEAK.findall(txt)
    if hits:
        sys.exit(f"LEAK in {name}: {sorted(set(hits))}")
(HERE / "pack.md").write_text(PACK, encoding="utf-8")
(HERE / "BRIEF.md").write_text(BRIEF, encoding="utf-8")
(HERE / "format.txt").write_text(FMT, encoding="utf-8")
(HERE / "header.txt").write_text(HEADER, encoding="utf-8")
(HERE / "lenses.json").write_text(json.dumps(LENSES, indent=1, ensure_ascii=False), encoding="utf-8")
print("pack ok, leak check clean;", len(sents), "sentences,", len(SHOTS), "shots")
