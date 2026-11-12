"""Build the BLIND round-2 red-team pack on the REAL upload text for mary_martha_short (every platform file,
captions.srt, pinned comment + share lines from the merged card, thumbnail text). Facts only, then leak-check."""
import re, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent; EP = HERE.parent; PUB = EP / "publish"
KJV = (EP / "red_team" / "pack" / "kjv_luke10_john11.txt").read_text(encoding="utf-8").strip()
narr = "\n".join(l for l in (EP / "narration.md").read_text(encoding="utf-8").splitlines() if not l.startswith("<!--")).strip()
files = ["youtube_short.md", "tiktok.md", "facebook.md", "instagram.md"]
body = "\n\n".join(f"# FILE {f}\n{(PUB / f).read_text(encoding='utf-8').strip()}" for f in files)
srt = (PUB / "captions.srt").read_text(encoding="utf-8").strip()
PACK = f"""# RED TEAM: the real upload text for a 74 s vertical short (YouTube Short, TikTok, Facebook Reel, Instagram Reel) on Luke 10:38-42 + John 11:5 (Martha and Mary).

Channel rules: ONE honest AI line per platform ("Art and voices made with AI tools."), no other AI or tool wording in public text; plain English for a worldwide audience (many non-native speakers, auto-translate); quoted Scripture must be exact KJV; grace, no pressure or fear; must point to Jesus; never put Martha down (Jesus did not call her work wrong) and never say Mary earned anything; no clickbait or overclaim; the film's own words and the text must agree; title + thumbnail words must work as ONE curiosity pair (thumbnail asks, title adds) that the film pays off.

Platform limits: YouTube title max 100 chars (aim 70), description 5000, first ~150 chars show before "more"; YouTube shows the first 3 hashtags, more than 15 voids all; TikTok caption 4000, 3-6 hashtags; Instagram caption 2200, max 30 hashtags (aim 5); Facebook title 255.

Thumbnails (all from one storybook drawing; look at the 4 jpg files in the thumbs/ folder next to this pack if you can view images): big words 'DOES ANYONE / EVEN CARE?', small line 'MARTHA · LUKE 10', brand AWAKEDEN. The drawing: Martha (long black hair, mustard dress, cloth in hand, worried face, red cheeks) speaks with an open hand to Jesus (brown hair, beard, cream robe, seated on a stool); Mary (long red-orange hair) sits on the floor at His feet looking up; cream wall, small oil lamp, jugs. 16:9 = words left, picture right; 9:16 and TikTok = words on top, framed picture below; 1:1 = words on top, framed picture below.

## Spoken words of the film
{narr}

## Words written on screen in the film (in order)
Does anyone care? | Martha | Mary | Martha, Martha, (in red-brown, as Jesus speaks) | one thing | "careful" means full of worry | And He loved her.

## Extra lines to be posted too
Pinned comment: Jesus said Martha's name twice. Why do you think He did that?
Shareable fact: In the King James Bible, "careful" means full of worry. Jesus named her worry, not her work.
Send-to line: Send this to the one who does everything for everyone.
Next teaser: Next: another person who brought Jesus a hard question, and how He answered.

## KJV (the only authority)
{KJV}

{body}

# FILE captions.srt (uploaded beside the video)
{srt}
"""
LENS = """YOUR CHECKLIST (cite the exact platform + phrase every time; give the replacement wording):
1. Bible accuracy against the KJV above: every claim and every quote, word for word. Anything the text does not say (overclaim)? Are refs honest for what is quoted vs told?
2. Clickbait or misleading: does any title, thumbnail text or first line promise what the film does not show? Does the title + thumbnail pair raise a real question the film answers?
3. Global / ESL clarity: words or idioms that fail for a non-native reader or machine translation; quote them and give the plainest replacement.
4. Respect: is Martha ever put down, or Mary set up as the winner? Grace, not pressure?
5. Platform rules: length limits, front-loading before "more", hashtag counts, tags, search words a real person types.
6. AI-sounding wording or slop in the public text; and is the AI disclosure handled honestly?
7. Consistency: do the titles, descriptions, captions and thumbnail agree with the film's spoken and on-screen words?
End with: VERDICT: PASS | REVISE, a score 0-10, and at most 8 concrete fixes (file + old text -> new text), most important first. Plain short words."""
LEAK = re.compile(r"\b(red_team|seat|fable|codex|grok|sonnet|opus|owner|panel|earlier review|round 1|convergen\w*|before/after|r1)\b", re.I)
hits = LEAK.findall(PACK + LENS)
if hits:
    raise SystemExit(f"LEAK: {sorted(set(hits))}")
(HERE / "redteam_pack.md").write_text(PACK, encoding="utf-8"); (HERE / "lens.txt").write_text(LENS, encoding="utf-8")
(HERE / "thumbs").mkdir(exist_ok=True)
for n in ["thumb_16x9.jpg", "thumb_9x16.jpg", "thumb_1x1.jpg", "thumb_tiktok.jpg"]:
    shutil.copy2(PUB / "thumbs" / n, HERE / "thumbs" / n)
print("wrote redteam_pack.md", len(PACK), "chars; leak check clean")
