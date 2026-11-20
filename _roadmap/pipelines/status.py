"""$0 lane board: read every STATE.md + LANE_QUEUE.md, print a summary, write _BOARD.html next to this file.
Dyslexia-friendly: one page, big text, each lane drawn as a track of 6 steps, "needs you" first."""
import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
GLOBS = ["threads/*/STATE.md", "encounters/*/STATE.md", "today/*/STATE.md", "poc_*/STATE.md"]
KEYS = ("lane", "title", "stage", "next", "waiting", "updated")

LANES = {
    "P1": ("The Thread", "Old Testament promise -> kept by Jesus", "Only when the New Testament itself quotes it or says \"fulfilled\"."),
    "P2": ("The Encounter", "Something Jesus did, seen through the whole Bible", "Starts from a moment in Jesus' life."),
    "P3": ("The Day", "A real-life struggle today, with the Bible's view", "Starts from the viewer's life. Extra safety checks."),
    "P4": ("The Lab", "Tests and new tools", "Small experiments. You decide: use it, park it, or drop it."),
}
# film steps (P1-P3): (label, stages, paid?)
FILM_STEPS = [
    ("Find a fresh idea", ("IDEA", "HUNT"), False),
    ("You pick", ("OWNER-PICK",), False),
    ("Words", ("WORDS",), False),
    ("Make the film", ("VOICE", "PICTURES", "CLIPS", "EDIT", "SOUND"), True),
    ("Final checks", ("FILM-CHECK", "PACKAGING"), False),
    ("Ready to post", ("RELEASE-PACK",), False),
]
LAB_STEPS = [
    ("Question", ("QUESTION",), False),
    ("Testing", ("TESTING",), False),
    ("You pick", ("OWNER-PICK",), False),
]
SHELF = {"DONE": "Done", "GRADUATED": "Done", "PARKED": "Parked (tried, did not pass yet)", "DROPPED": "Dropped"}


def read_state(p):
    d = {"folder": p.parent.relative_to(ROOT).as_posix()}
    for line in p.read_text(encoding="utf-8").splitlines():
        k, sep, v = line.partition(":")
        if sep and k.strip() in KEYS and k.strip() not in d:
            d[k.strip()] = v.strip()
    return d


def read_queue():
    q = {k: [] for k in LANES}
    f = HERE / "LANE_QUEUE.md"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            parts = [x.strip() for x in line.split("|")]
            if len(parts) == 3 and parts[0] in q:
                q[parts[0]].append(parts[1:])
    return q


def short(t, n=70):
    t = re.split(r" \(|; ", t or "")[0].strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def who_waits(w):
    w = (w or "").lower()
    if w.startswith("owner"):
        return "you", "Needs you"
    if w.startswith("hub"):
        return "hub", "Waiting on the hub"
    if w.startswith("panel"):
        return "hub", "Waiting for AI panel"
    return "go", "Working"


e = html.escape
items = [read_state(p) for g in GLOBS for p in sorted(ROOT.glob(g))]
queue = read_queue()

# ---------- console ----------
for lane, (name, *_r) in LANES.items():
    mine = [i for i in items if i.get("lane") == lane]
    print(f"\n{lane} {name} ({len(mine)})")
    for i in mine:
        print(f"  {i.get('stage', '?'):<13} {short(i.get('title', i['folder']), 40):<40} [{i.get('waiting', '')}]")
for i in items:
    if i.get("lane") not in LANES:
        print(f"  !! {i['folder']}: lane missing or unknown")

# ---------- needs you ----------
mine_owner = [i for i in items if (i.get("waiting") or "").lower().startswith("owner") and i.get("stage") not in SHELF]
if mine_owner:
    needs = "".join(
        f'<li><b>{e(short(i.get("title", "")))}</b><br>{e(i["waiting"].split("(", 1)[-1].rstrip(")"))}'
        f'<br><span class="path">F:\\slk\\PycharmProjects\\JesusInTheBible\\{e(i["folder"].replace("/", chr(92)))}</span></li>'
        for i in mine_owner)
    needs_html = f'<ol class="needs">{needs}</ol>'
else:
    needs_html = '<p class="calm">Nothing right now. The lanes are working.</p>'


def chip(i):
    cls, label = who_waits(i.get("waiting"))
    nxt = short(i.get("next", ""), 80)
    return (f'<div class="chip {cls}"><b>{e(short(i.get("title", i["folder"]), 48))}</b>'
            f'<span class="tag">{e(label)}</span>'
            + (f'<span class="nxt">Next: {e(nxt)}</span>' if nxt else "") + "</div>")


lanes_html = []
for n, (lane, (name, what, rule)) in enumerate(LANES.items(), 1):
    mine = [i for i in items if i.get("lane") == lane]
    steps = LAB_STEPS if lane == "P4" else FILM_STEPS
    cells = []
    for k, (label, stages, paid) in enumerate(steps, 1):
        here = [i for i in mine if i.get("stage") in stages]
        cells.append(
            f'<div class="step{" has" if here else ""}"><div class="sh"><span class="num">{k}</span>{e(label)}'
            + ('<span class="money">$ asks you first</span>' if paid else "") + "</div>"
            + "".join(chip(i) for i in here) + "</div>")
    shelves = []
    for st, lab in (("PARKED", SHELF["PARKED"]), ("DONE", "Done"), ("DROPPED", "Dropped")):
        got = [i for i in mine if i.get("stage") == st or (st == "DONE" and i.get("stage") == "GRADUATED")]
        if got:
            shelves.append(f'<p class="shelf"><b>{lab}:</b> ' + " · ".join(e(short(i.get("title", ""), 40)) for i in got) + "</p>")
    q = queue.get(lane, [])
    up = ('<div class="up"><b>Up next:</b><ol>' + "".join(
        f"<li>{e(t)}" + (f' <span class="ref">{e(r)}</span>' if r != "-" else "") + "</li>" for t, r in q) + "</ol></div>") if q else ""
    lanes_html.append(f"""<section class="lane l{n}">
<h3><span class="badge">{lane}</span> {e(name)}</h3>
<p class="what">{e(what)}. <span class="rule">{e(rule)}</span></p>
<div class="track t{len(steps)}">{''.join(cells)}</div>
{up}{''.join(shelves)}</section>""")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Film Lanes Board</title>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fbf7ee;--ink:#1f1f1f;--soft:#5b5b5b;--card:#ffffff;--line:#e3dccb;
--you:#c0392b;--youbg:#fdecea;--hub:#9a6a00;--hubbg:#fff4d6;--go:#1e7b45;--gobg:#e6f4ea;
--l1:#2f5fa7;--l2:#8a4fb0;--l3:#c2621b;--l4:#4f7f6a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;
--you:#ff8a80;--youbg:#3a1f1d;--hub:#f2c14e;--hubbg:#3a3019;--go:#7bd39a;--gobg:#1d3326;--l1:#7aa7ef;--l2:#c79be6;--l3:#f0a060;--l4:#8cc4ab}}}}
:root[data-theme="dark"]{{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;
--you:#ff8a80;--youbg:#3a1f1d;--hub:#f2c14e;--hubbg:#3a3019;--go:#7bd39a;--gobg:#1d3326;--l1:#7aa7ef;--l2:#c79be6;--l3:#f0a060;--l4:#8cc4ab}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:20px/1.6 "Atkinson Hyperlegible",Verdana,sans-serif;letter-spacing:.02em;
margin:0 auto;padding:20px 16px 60px;max-width:1150px}}
h1{{font-size:34px;margin:0 0 4px}}h2{{font-size:27px;margin:44px 0 12px}}h3{{font-size:24px;margin:0 0 4px}}
.sub{{color:var(--soft);margin:0 0 20px}}
.box{{background:var(--card);border:2px solid var(--line);border-radius:14px;padding:16px 20px}}
.youbox{{border-color:var(--you);background:var(--youbg)}}
.needs li{{margin:0 0 12px}}.calm{{margin:0;color:var(--go);font-weight:700}}
.path{{font-size:16px;color:var(--soft);word-break:break-all}}
.lane{{background:var(--card);border:2px solid var(--line);border-left:12px solid var(--c);border-radius:14px;padding:16px 18px;margin:0 0 22px}}
.l1{{--c:var(--l1)}}.l2{{--c:var(--l2)}}.l3{{--c:var(--l3)}}.l4{{--c:var(--l4)}}
.badge{{background:var(--c);color:var(--bg);border-radius:8px;padding:0 10px;margin-right:6px}}
.what{{margin:0 0 12px}}.rule{{color:var(--soft)}}
.track{{display:grid;gap:8px}}.t6{{grid-template-columns:repeat(6,1fr)}}.t3{{grid-template-columns:repeat(3,1fr)}}
.step{{border:2px dashed var(--line);border-radius:10px;padding:8px;min-height:90px}}
.step.has{{border:2px solid var(--c)}}
.sh{{font-weight:700;font-size:17px;line-height:1.3}}
.num{{display:inline-block;width:26px;height:26px;border-radius:50%;background:var(--c);color:var(--bg);text-align:center;line-height:26px;margin-right:6px;font-size:15px}}
.money{{display:block;font-weight:400;font-size:15px;color:var(--hub)}}
.chip{{margin-top:8px;border-radius:8px;padding:6px 8px;font-size:17px;line-height:1.35}}
.chip b{{display:block}}.tag{{display:inline-block;font-weight:700;font-size:15px;margin-top:2px}}
.nxt{{display:block;font-size:15px;color:var(--soft);margin-top:2px}}
.chip.you{{background:var(--youbg);border:2px solid var(--you)}}.chip.you .tag{{color:var(--you)}}
.chip.hub{{background:var(--hubbg);border:2px solid var(--hub)}}.chip.hub .tag{{color:var(--hub)}}
.chip.go{{background:var(--gobg);border:2px solid var(--go)}}.chip.go .tag{{color:var(--go)}}
.up{{margin-top:12px}}.up ol{{margin:4px 0 0;padding-left:28px}}.ref{{color:var(--soft);font-size:16px}}
.shelf{{margin:8px 0 0;color:var(--soft);font-size:17px}}
.how{{counter-reset:s;list-style:none;padding:0;margin:0}}
.how li{{position:relative;padding:12px 12px 12px 62px;margin:0 0 10px;background:var(--card);border:2px solid var(--line);border-radius:12px}}
.how li::before{{counter-increment:s;content:counter(s);position:absolute;left:14px;top:12px;width:34px;height:34px;border-radius:50%;
background:var(--ink);color:var(--bg);text-align:center;line-height:34px;font-weight:700}}
.who{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.who div{{background:var(--card);border:2px solid var(--line);border-radius:12px;padding:12px}}
.key span{{display:inline-block;border-radius:8px;padding:0 10px;margin:4px 8px 4px 0;font-weight:700}}
@media (max-width:820px){{.t6,.t3{{grid-template-columns:1fr}}.step{{min-height:0}}.step:not(.has){{opacity:.6}}.who{{grid-template-columns:1fr}}body{{font-size:19px}}}}
</style></head><body>
<h1>Our 4 film lanes</h1>
<p class="sub">Updated {date.today():%d %b %Y}. Four lanes run side by side. Each film moves left to right.</p>

<h2>1. Needs you</h2>
<div class="box youbox">{needs_html}</div>

<h2>2. Where each film is</h2>
<p class="key"><span style="background:var(--gobg);color:var(--go)">Working</span><span style="background:var(--hubbg);color:var(--hub)">Waiting on the hub</span><span style="background:var(--youbg);color:var(--you)">Needs you</span></p>
{''.join(lanes_html)}

<h2>3. How we work</h2>
<ol class="how">
<li><b>A lane takes the next idea</b> from its "Up next" list. Free.</li>
<li><b>The AI panel tests the idea, blind.</b> Fable + Claude + Codex + Gemini (+ Grok when it has credit). Is it fresh? Is it true? Does it land on Jesus? <br>About 1 in 3 ideas fail here. That is normal. It costs nothing.</li>
<li><b>A passing idea comes to you.</b> You pick it, or not.</li>
<li><b>Words are written and checked</b> by the panel. Everything on screen is also spoken, so dubbing works.</li>
<li><b>Making the film costs money.</b> I show you the price first. Nothing is spent until you say yes.</li>
<li><b>Final checks, then it is ready.</b> Title, poster and captions are checked. You post it.</li>
</ol>

<h2>4. Who does what</h2>
<div class="who">
<div><b>You</b><br>Pick ideas. Say yes to spend. Post films.</div>
<div><b>The lanes (P1-P4)</b><br>Each does its own work, in its own folder. At most 1 film being made and 1 idea being tested per lane.</div>
<div><b>The hub (me)</b><br>Keeps the shared files. Runs the AI panel queue and the paid queue, one at a time. Keeps this board up to date.</div>
</div>
</body></html>"""
out = HERE / "_BOARD.html"
out.write_text(page, encoding="utf-8")
print(f"\n{len(items)} items -> {out}")
