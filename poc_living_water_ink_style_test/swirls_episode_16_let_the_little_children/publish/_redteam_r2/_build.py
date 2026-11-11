"""Build the BLIND red-team pack on the REAL upload text for ep16 (every platform file, captions.srt,
pinned comment + share lines from the packaging card, thumbnail text). Facts only, then leak-check.
Usage: python _build.py [out_name]   (default redteam_pack.md; the re-test writes its own name)"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE.parent
EP = PUB.parent
REPO = EP.parent.parent
sys.path.insert(0, str(REPO))
from pipeline import scripture  # noqa: E402

out = HERE / (sys.argv[1] if len(sys.argv) > 1 else "redteam_pack.md")
card = json.loads((EP / "_packaging" / "16_let_the_little_children" / "packaging.json").read_text(encoding="utf-8"))
ns = {}
exec((EP / "episode.py").read_text(encoding="utf-8-sig"), {"__file__": str(EP / "episode.py")}, ns)
fc = ns["FRONT_COVER"]

def kjv(ref):
    return (scripture.fetch_kjv(ref) or "").strip()

narr = (EP / "narration.md").read_text(encoding="utf-8").strip()
files = ["youtube_short.md", "tiktok.md", "facebook.md", "instagram.md"]
body = "\n\n".join(f"# FILE {f}\n{(PUB / f).read_text(encoding='utf-8').strip()}" for f in files)
srt = (PUB / "captions.srt").read_text(encoding="utf-8").strip()

PACK = f"""# RED TEAM: the real upload text for a 75.7 s vertical short (YouTube Short, TikTok, Facebook Reel, Instagram Reel) on Mark 10:13-16 (Jesus and the little children).

Channel rules: no AI wording in any public text (no "AI-generated", "made with AI" etc.; the platforms' own AI-content switches are turned ON at upload instead); plain English for a worldwide audience (many non-native speakers, auto-translate); quoted Scripture must be exact KJV; grace, no pressure or fear; must point to Jesus; no clickbait or overclaim; the film's own words and the text must agree.

Platform limits: YouTube title max 100 chars (aim 70), description 5000; YouTube shows the first 3 hashtags, more than 15 voids all; TikTok caption 4000, 3-6 hashtags; Instagram caption 2200, max 30 hashtags (aim 5); Facebook title 255.

Thumbnail (one picture used for 9:16, 1:1 and 16:9): big title '{fc.title.upper()}', the reference '{fc.subtitle}', brand AWAKEDEN, and a storybook drawing of Jesus (long dark hair, beard, patched blue tunic) carrying two laughing little girls, one on His shoulders with her hand in His hair, one hugging His side; stone arch, olive tree, warm sun.

## Spoken words of the film
{narr}

## Words written on screen in the film (in order)
Pushed away? | "not now" (a small paper slip, at the start, then near the man who holds up his hand to stop the people, then again at the end) | a touch | Angry. | Let the children come to Me. (small label: Jesus · Mark 10:14) | like a little child | a touch | His arms. | Look at who Jesus picked up.

## Extra lines from the packaging card (pinned comment and share lines, to be posted too)
Pinned comment: {card['pinned_comment']}
Shareable fact: {card['shareable_fact']}
Send-to line: Send this to {card['send_to']}.
Next teaser: {card['next_teaser']}

## KJV (the only authority)
Mark 10:13-16: {kjv('Mark 10:13-16')}
Matthew 19:13-15: {kjv('Matthew 19:13-15')}
Luke 18:15-17: {kjv('Luke 18:15-17')}

{body}

# FILE captions.srt (uploaded beside the video)
{srt}
"""

LENS = """YOUR CHECKLIST (cite the exact platform + phrase every time; give the replacement wording):
1. Bible accuracy against the KJV above: every claim and every quote, word for word. Anything the text does not say (overclaim)?
2. Clickbait or misleading: does any title, thumbnail text or first line promise what the film does not show?
3. Global / ESL clarity: words or idioms that fail for a non-native reader or machine translation; quote them and give the plainest replacement.
4. Cultural and child-safety sensitivity: children in the thumbnail and the text; any phrase that could be read the wrong way in any culture.
5. Platform rules: length limits, hashtag counts, tags.
6. AI-sounding wording or slop in the public text; and is the AI disclosure handled honestly?
7. Consistency: do the titles, descriptions, captions and thumbnail agree with the film's spoken and on-screen words?"""

LEAK = re.compile(r"\b(red_team_r1|seat|fable|codex|grok|sonnet|opus|owner|panel|earlier review|round 1|convergen\w*|before/after|provisional)\b", re.I)
hits = LEAK.findall(PACK + LENS)
if hits:
    sys.exit(f"LEAK: {sorted(set(hits))}")
out.write_text(PACK, encoding="utf-8")
(HERE / "lens.txt").write_text(LENS, encoding="utf-8")
print("wrote", out.name, len(PACK), "chars; leak check clean")
