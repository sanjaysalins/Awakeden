"""Living Comic gates ($0). Reads an episode.json, prints PASS/FAIL per gate.
Rules come from the panel rounds (see _panel_design/_DESIGN_PANEL_REPORT.html, _panel_proof/).
  .venv\Scripts\python.exe poc_comic_page/_living_comic/lc_gates.py <episode.json>"""
import json, re, sys

def norm(s): return re.sub(r"[^a-z' ]", "", s.lower()).split()

def gates(ep):
    out = []
    def g(name, ok, msg=""): out.append((name, ok, msg))
    P, B, C = ep["panels"], ep["balloons"], ep.get("cards", [])
    dur = ep["audio"]["dur"]
    # LC-1 panel timeline is contiguous and covers the audio
    ok = abs(P[0]["t"][0]) < 1e-6 and abs(P[-1]["t"][1] - dur) < 0.05 and all(abs(P[i]["t"][1] - P[i+1]["t"][0]) < 1e-6 for i in range(len(P)-1))
    g("LC-1 panels contiguous, cover audio", ok)
    # LC-2 balloon <= 8 words and enough reading time
    bad = []
    for b in B:
        w = len(b["text"].split()); need = 1.2 + 0.25 * w; have = b["t"][1] - b["t"][0]
        if w > 8 or have < need - 1e-6: bad.append(f'"{b["text"]}" words={w} on={have:.2f}s need={need:.2f}s')
    for c in C:
        w = sum(len(l.split()) for l in c["lines"]); have = c["t"][1] - c["t"][0]
        if have < 1.2 + 0.25 * w - 1e-6: bad.append(f'card {c["lines"]} on={have:.2f}s need={1.2+0.25*w:.2f}s')
    g("LC-2 balloon<=8 words + reading time", not bad, "; ".join(bad))
    # LC-3 Jesus balloons: KJV verbatim, in order, whole chain, speaker attribution
    bad = []
    for ref, verse in ep["kjv"].items():
        chain = [b for b in B if b["speaker"] == "jesus" and b["kjv_ref"] == ref]
        if not chain: continue
        if norm(" ".join(b["text"] for b in chain)) != norm(verse): bad.append(f"{ref}: chain != verse")
        if any(chain[i]["t"][0] > chain[i+1]["t"][0] for i in range(len(chain)-1)): bad.append(f"{ref}: out of order")
        if len({b["t"][1] for b in chain}) > 1 and False: pass
    if any(b["speaker"] == "jesus" and b.get("kjv_ref") not in ep["kjv"] for b in B): bad.append("jesus balloon without known kjv_ref")
    g("LC-3 Jesus words = KJV verbatim, in order, whole chain", not bad, "; ".join(bad))
    # LC-4 ink wake only on first panel + Jesus panel, never on a sacred non-jesus panel
    bad = [p["id"] for p in P if p.get("ink_wake") and p.get("role") not in ("first", "jesus")]
    g("LC-4 ink wake only on first/jesus panel", not bad, ",".join(bad))
    # LC-5 invented lines: none in episode 1, max 2 ever, none within 10s of a Jesus balloon
    inv = [b for b in B if b.get("invented")]
    bad = []
    if ep.get("first_episode") and inv: bad.append("invented line in first episode")
    if len(inv) > 2: bad.append("more than 2 invented")
    for b in inv:
        for j in (x for x in B if x["speaker"] == "jesus"):
            if abs(b["t"][0] - j["t"][0]) < 10: bad.append(f'invented "{b["text"]}" within 10s of Jesus balloon')
    g("LC-5 invented lines", not bad, "; ".join(bad))
    # LC-6 each balloon sits inside a panel; sacred panels carry no sfx
    bad = []
    for b in B:
        if not any(p["t"][0] - 1e-6 <= b["t"][0] and b["t"][1] <= p["t"][1] + 1e-6 for p in P):
            bad.append(f'"{b["text"]}" crosses a panel cut')
    for s in ep.get("sfx", []):
        if any(p.get("sacred") and p["t"][0] <= s["t"] < p["t"][1] for p in P): bad.append(f'sfx at {s["t"]} on sacred panel')
    g("LC-6 balloon inside a panel; no sfx on sacred", not bad, "; ".join(bad))
    # LC-7 every decode word has a card
    covered = {d for c in C for d in c.get("decodes", [])}
    miss = [w for w in ep.get("decode_words", []) if w not in covered]
    g("LC-7 decode words all have a card", not miss, ",".join(miss))
    # LC-8 one text group at a time: card must not overlap balloons
    bad = [c["lines"][0] for c in C if any(b["t"][0] < c["t"][1] and c["t"][0] < b["t"][1] for b in B)]
    g("LC-8 card never over balloons", not bad, ",".join(bad))
    return out

if __name__ == "__main__":
    ep = json.load(open(sys.argv[1], encoding="utf8")); res = gates(ep); fails = 0
    for n, ok, m in res:
        print(("PASS " if ok else "FAIL ") + n + (f"  -> {m}" if m else "")); fails += (not ok)
    print("RESULT:", "LC-READY" if not fails else f"{fails} FAIL")
    sys.exit(1 if fails else 0)
