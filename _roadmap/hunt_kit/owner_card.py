"""Gate 6: python owner_card.py <topic_dir> <card letter>
Writes <topic_dir>/_OWNER_CARD.html. REFUSES unless the card is PASS in a CURRENT GATE.md (gate.py run after
CARDS.md and every judge/context file last changed). Order on the page: the question "Had you seen this before?",
the insight in one line, the two anchors side by side, the why-verse, the label(s); scores, COMMON count, flags AFTER.
Never opens anything."""
import html, re, sys
from pathlib import Path
from _rules import need, card_text, field, labels, vtext, fmt
from gate import evaluate
T = Path(sys.argv[1]).resolve(); cid = sys.argv[2].upper()
need(T, "owner_card")
G = T / "GATE.md"
if not G.exists(): sys.exit("owner_card: REFUSED - no GATE.md; run gate.py first")
newest = max(f.stat().st_mtime for f in [T / "CARDS.md", *(f for f in T.glob("judge_*.md") if f.name.startswith("judge_")), *(T / f"context_{s}.md" for s in ("codex", "gemini") if (T / f"context_{s}.md").exists())])
if G.stat().st_mtime < newest: sys.exit("owner_card: REFUSED - GATE.md is older than CARDS/judge/context files; re-run gate.py")
gtxt = G.read_text(encoding="utf-8")
if cid not in [x.strip() for x in (re.search(r"^PASS cards: (.*)$", gtxt, re.M) or [0, ""])[1].split(",")]:
    sys.exit(f"owner_card: REFUSED - card {cid} is not PASS in GATE.md")
r = evaluate(T, "Driver 1" in gtxt)
row = next(x for x in r["rows"] if x["cid"] == cid)
if row["why"]: sys.exit(f"owner_card: REFUSED - card {cid} no longer passes: {'; '.join(row['why'])}")
txt = card_text(T)[cid]
title = txt.split("\n", 1)[0].lstrip(" -").strip()
a1, a2, wv = row["anchors"]["ANCHOR-1"], row["anchors"]["ANCHOR-2"], row["anchors"]["WHY-VERSE"]
scores = "<table>" + "".join(f"<tr><th>{k}</th><td>{v:g} / 10</td></tr>" for k, v in row["med"].items()) + "</table>"
scores += f"<p>COMMON (yes or partly): {row['com']} of {len(r['judges'])} judges. SOUND flags: none. CONTEXT: codex PASS, gemini PASS.</p>"
slots = {"CARD": cid, "TOPIC": T.parent.name, "PASSAGE": field(txt, "PASSAGE") or title, "INSIGHT": field(txt, "INSIGHT") or title,
         "LABEL": " + ".join(dict.fromkeys(labels(txt))), "REF1": fmt(a1), "TEXT1": vtext(a1), "REF2": fmt(a2), "TEXT2": vtext(a2),
         "WHY": f"{fmt(wv)}: {vtext(wv)}", "NOT": field(txt, "DOES NOT PROVE")}
page = re.sub(r"<!--.*?-->\s*", "", Path(__file__).with_name("OWNER_CARD_TEMPLATE.html").read_text(encoding="utf-8"), flags=re.S)
for k, v in slots.items(): page = page.replace("{" + k + "}", html.escape(v))
page = page.replace("{SCORES}", scores)  # built here, already safe HTML
(T / "_OWNER_CARD.html").write_text(page, encoding="utf-8")
print("wrote", T / "_OWNER_CARD.html")
print("link: file:///" + str(T / "_OWNER_CARD.html").replace("\\", "/"))
