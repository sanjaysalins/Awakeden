"""Owner rule 2026-11-16: the Awakeden brand + awakeden.com site are retired.
Rewrites every PUBLIC text file (publish packs, upload kits, publish_meta.json) to the
Salt and Light Kingdom brand and drops every awakeden.com link. Review/panel transcripts
are history and are left alone.
Usage: python tools_strip_awakeden.py [--apply]   (dry run by default)"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SKIP = ("_independent_review", "red_team", "_redteam", "panel", "prompt", "_pre_")
YT_H, YT_U = "@saltandlightkingdomorg", "https://www.youtube.com/@saltandlightkingdomorg"
NL = r"(?:\r?\n|\n|<br>)"
LINK = r"https?://(?:www\.)?awakeden\.com[^\s\"'<\)]*"

def fix(t: str, name: str) -> str:
    t = re.sub(NL + r"?[ \t]*Read it panel by panel:[ \t]*" + LINK, "", t)
    t = t.replace("@awakeden (https://youtube.com/@awakeden)", f"{YT_H} ({YT_U})")
    t = re.sub(r"https?://(?:www\.)?youtube\.com/@awakeden", YT_U, t)
    follow = {"tiktok.md": "Follow @saltandlightkingdom", "instagram.md": "Follow @salt.andlightkingdomorg"}
    if name in follow:
        t = t.replace("Follow @awakeden", follow[name])
    else:
        t = re.sub(NL + r"?[ \t]*Follow @awakeden(?=" + NL + r"|$|\")", "", t)
    t = re.sub(r"(" + NL + r"){1,2}[ \t]*" + LINK + r"[ \t]*(?=" + NL + r"|$|\"|</)", "", t)  # bare site line
    t = re.sub(r"(\"read_url\":\s*)\"" + LINK + "\"", r'\1""', t)
    t = re.sub(LINK, "", t)
    t = t.replace("#Awakeden", "#SaltAndLightKingdom")
    t = re.sub(r"\bAWAKEDEN\b", "SALT AND LIGHT KINGDOM", t)
    t = re.sub(r"\b[Aa]wakeden\b", "Salt and Light Kingdom", t)
    return t

apply = "--apply" in sys.argv
nf = 0
for p in ROOT.rglob("*"):
    if any(x in p.parts for x in (".venv", "node_modules", ".git", "_website")): continue
    if p.suffix not in (".md", ".html", ".json", ".txt") or not p.is_file(): continue
    rel = str(p.relative_to(ROOT)).replace("\\", "/")
    if any(s in rel for s in SKIP): continue
    if not (any(d in rel for d in ("/publish/", "/upload/")) or p.name == "publish_meta.json"): continue
    t = p.read_text(encoding="utf-8")
    if not re.search("awakeden", t, re.I): continue
    new = fix(t, p.name)
    nf += 1
    left = len(re.findall("awakeden", new, re.I))
    print(("FIX " if apply else "would fix ") + rel + (f"   !! {left} left" if left else ""))
    if apply: p.write_text(new, encoding="utf-8")
print(f"{'fixed' if apply else 'would fix'} {nf} files")
