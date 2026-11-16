"""Machine checks for BETHLEHEM_ANIMATIC_v1.mp4. Reads the SAME data the Remotion comp renders from. $0.
Run: .venv\\Scripts\\python.exe prophecy\\01_bethlehem\\animatic\\check_animatic.py  -> writes animatic\\CHECKS.md"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import ImageFont

R = Path("F:/slk/PycharmProjects/JesusInTheBible")
A = R / "prophecy/01_bethlehem/animatic"
D = json.load(open(R / "_remotion/public/bethlehem/animatic_data.json", encoding="utf-8"))
WORDS = json.load(open(R / "prophecy/01_bethlehem/audio/narration.words.json", encoding="utf-8"))
KJV = (R / "prophecy/01_bethlehem/words/KJV.txt").read_text(encoding="utf-8")
MP4 = A / "BETHLEHEM_ANIMATIC_v1.mp4"
kalam = lambda s: ImageFont.truetype(str(R / "_remotion/public/Kalam-Bold.ttf"), s)
bang = lambda s: ImageFont.truetype(str(R / "_remotion/public/Bangers.ttf"), s)
W = lambda font, t: font.getlength(t)
import math
F = lambda s: math.floor(s * 30 + 0.5)
SAFE = (60, 200, 960, 1540)
res = []  # (status, name, detail)
def add(ok, name, detail=""): res.append(("PASS" if ok else "FAIL", name, detail))
def note(name, detail): res.append(("NOTE", name, detail))
pages = {p["n"]: p for p in D["pages"]}

# ---- 1. boxes inside safe zone ----
def cy(pg): return 1461 if pg == 9 else 1092
boxes = []  # (item, label, x0,y0,x1,y1)
for it in D["items"]:
    if it["kind"] in ("pill", "speech"):
        h = len(it["lines"]) * 62 + 40; top = cy(it["page"]) - h / 2
        boxes.append((it["id"], "pill", 70, top, 950, top + h))
        if it.get("tab"):
            w = W(kalam(28), it["tab"]) + 34; boxes.append((it["id"], "tab", 96, top - 30, 96 + w, top + 12))
        if it.get("chip"):
            w = W(kalam(28), it["chip"]) + 34; boxes.append((it["id"], "chip", 924 - w, top - 30, 924, top + 12))
        if it["kind"] == "speech": boxes.append((it["id"], "tail", 400, top + h, 462, top + h + 38))
        if it.get("goldTab"):
            w = W(kalam(28), "Bethlehem") + 34; boxes.append((it["id"], "goldtab", 96, top - 30, 96 + w, top + 12))
    elif it["kind"] == "slab":
        w = max(W(bang(104), l) for l in it["lines"]) + 40; boxes.append((it["id"], "slab", 540 - w / 2, 400, 540 + w / 2, 400 + 114 * len(it["lines"])))
    elif it["kind"] == "scroll":
        boxes.append((it["id"], "card", 70, 940, 950, 1190))
hw = W(kalam(54), "Bethlehem") + 44; boxes.append(("gold", "home", 70, 210, 70 + hw, 282))
bad = [(i, l, round(x0), round(y0), round(x1), round(y1)) for i, l, x0, y0, x1, y1 in boxes if x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]]
add(not bad, "every text item inside the safe zone (x 60-960, y 200-1540)", f"{len(boxes)} boxes checked" + (f"; OUT: {bad}" if bad else ""))
# pill reading line homes
bl = []
for i, l, x0, y0, x1, y1 in boxes:
    if l == "pill":
        pg = next(it["page"] for it in D["items"] if it["id"] == i)
        lo, hi = (1400, 1522) if pg == 9 else (1000, 1184)
        if y0 < lo or y1 > hi: bl.append((i, round(y0), round(y1)))
add(not bl, "pills sit inside their reading-line home (1000-1184; QUIET ROWS 1400-1522)", str(bl) if bl else "")

# ---- 2. words / letters / lines, and text fits the pill ----
bad = []; fit = []
for it in D["items"]:
    if len(it["lines"]) > 2: bad.append((it["id"], "lines>2"))
    for ln in it["lines"]:
        if len(ln.split()) > 7: bad.append((it["id"], "words>7", ln))
        if len(ln) > 28: bad.append((it["id"], "letters>28", ln, len(ln)))
        if it["kind"] in ("pill", "speech") and W(kalam(54), ln) > 880 - 8 - 56: fit.append((it["id"], ln, round(W(kalam(54), ln))))
        if it["kind"] == "scroll" and W(kalam(60), ln) > 800 - 60: fit.append((it["id"], ln, round(W(kalam(60), ln))))
add(not bad, "max 7 words and 28 letters a line, max 2 lines", str(bad) if bad else f"{len(D['items'])} items")
add(not fit, "every line fits inside its pill / scroll width", str(fit) if fit else "")

# ---- 3. one text item at a time; durations ----
its = sorted(D["items"], key=lambda i: i["start"])
ov = [(a["id"], b["id"]) for a, b in zip(its, its[1:]) if F(a["end"]) > F(b["start"])]
add(not ov, "never two text items at once", str(ov) if ov else "all items strictly sequential (frame-rounded)")
shell = []  # card shell open must not overlap a pill
for it in D["items"]:
    if it["kind"] == "scroll" and it.get("open"):
        for o in D["items"]:
            if o["kind"] in ("pill", "speech", "slab") and F(o["start"]) < F(it["start"]) and F(o["end"]) > F(it["open"]) and o["page"] in (it["page"], it["page"]):
                if o["id"] != it["id"] and F(o["end"]) > F(it["open"]) and F(o["start"]) < F(it["start"]): shell.append((o["id"], it["id"]))
add(not shell, "scroll card shell never opens while a pill is still up", str(shell) if shell else "")
short = []
for it in D["items"]:
    dur = (F(it["end"]) - F(it["start"])) / 30; nw = sum(len(l.split()) for l in it["lines"])
    if dur < 1.2 - 1e-6 or dur < 0.28 * nw - 1e-6: short.append((it["id"], round(dur, 2), nw, round(0.28 * nw, 2)))
add(not short, "each item stays >= 1.2 s and >= 0.28 s a word", str(short) if short else "min slack shown in table below")

# ---- 4. KJV exact + chip verse ----
strip = lambda s: s.rstrip(".,;:!?")
kj = []
verse_of = {"MICAH 5:2": "Micah 5:2", "MATTHEW 2:5": "Matthew 2:5"}
kjv_lines = {m.group(1) + " " + m.group(2): m.group(3) for m in (re.match(r"(\w+) (\d+:\d+) (.*)", l) for l in KJV.splitlines()) if m}
for it in D["items"]:
    if not it.get("kjv"): continue
    txt = strip(" ".join(it["lines"]))
    vk = verse_of[it["chip"]]
    ok_verse = txt in kjv_lines.get(vk, "")
    ok_any = txt in KJV
    kj.append((it["id"], txt, it["chip"], "in-verse" if ok_verse else ("OTHER VERSE" if ok_any else "NOT IN KJV")))
    if it["lines"][-1] != strip(it["lines"][-1]) and it["lines"][-1][-1] != ".": pass
add(all(k[3] == "in-verse" for k in kj), "every on-screen KJV string is word for word in words/KJV.txt, chip names the right verse", "; ".join(f"{k[0]} '{k[1]}' {k[2]} {k[3]}" for k in kj))
note("KJV end punctuation", "Design writes `ruler in Israel.` and `In Bethlehem of Judaea.`; KJV has `;` and `:` there. Words are exact; only the closing mark differs (design's choice, kept).")

# ---- 5. clip length vs on-screen ----
cl = []
for p in D["panels"]:
    on = (F(p["on"][1]) - F(p["on"][0])) / 30; spare = p["clipLen"] - on
    cl.append((p["id"], p["still"], p["clip"], p["clipLen"], round(on, 2), round(spare, 2)))
add(all(c[5] >= 0.4 - 1e-6 for c in cl), "every clip length minus its on-screen time >= 0.4 s", f"min spare {min(c[5] for c in cl)} s ({[c[0] for c in cl if c[5] == min(c[5] for c in cl)]})")

# ---- 6. sacred pages: no shake / boom / slab ----
sa = [(e["type"], e["page"], e["t"]) for e in D["events"] if pages[e["page"]]["sacred"] and e["type"] in ("shake+boom", "slab", "riffle", "shake", "boom")]
sa += [(p["id"], "shake") for p in D["panels"] if pages[p["page"]]["sacred"] and p["land"] == "shake"]
sa += [(i["id"], "slab") for i in D["items"] if pages[i["page"]]["sacred"] and i["kind"] == "slab"]
add(not sa, "no shake, boom or slab event inside a sacred page (5, 7, 9, 10; page 8 treated sacred too)", str(sa) if sa else "events on pages " + str(sorted({e['page'] for e in D['events']})))

# ---- 7. video / audio ----
def probe(sel, ent, extra=()):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", sel, "-show_entries", ent, "-of", "default=nw=1:nk=1", *extra, str(MP4)], capture_output=True, text=True).stdout.split()
    return o
if MP4.exists():
    nb = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(MP4)], capture_output=True, text=True).stdout.strip().rstrip(","))
    vdur = float(probe("v:0", "stream=duration")[0]); adur = float(probe("a:0", "stream=duration")[0])
    fdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(MP4)], capture_output=True, text=True).stdout.strip().rstrip(","))
    size = probe("v:0", "stream=width,height,r_frame_rate")
    add(nb == 1548, "film is 1548 frames", f"counted {nb}")
    add(size[:2] == ["1080", "1920"] and size[2] == "30/1", "1080x1920 at 30 fps", str(size))
    add(abs(vdur - adur) <= 0.05, "audio duration == video duration", f"video {vdur:.3f} s, audio {adur:.3f} s, container {fdur:.3f} s")
    last = WORDS[-1]["end"]
    hold = vdur - last
    add(hold >= 3.0, "landing hold >= 3.0 s (last spoken word to end of file)", f"last word ends {last:.2f} s; file ends {vdur:.3f} s; hold {hold:.2f} s; audio hold {adur-last:.2f} s")
    # is audio really there to the end? (mean level of the last 3 s should be near silence, not truncated stream)
else:
    add(False, "film exists", str(MP4))

# ---- 8. sync of pill start vs spoken word ----
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
sync = []
for it in D["items"]:
    if it["kind"] == "slab": continue
    first = norm(it["lines"][0].split()[0]); cands = [w for w in WORDS if norm(w["w"]) == first]
    if not cands: continue
    t = min(cands, key=lambda w: abs(w["start"] - it["start"]))["start"]
    sync.append((it["id"], round(it["start"] - t, 2)))
mx = max(sync, key=lambda s: abs(s[1]))
add(abs(mx[1]) <= 0.4, "every item starts within 0.4 s of its first spoken word", f"worst {mx[0]} at {mx[1]:+.2f} s; " + ", ".join(f"{a} {b:+.2f}" for a, b in sync if abs(b) > 0.2))

# ---- write CHECKS.md ----
L = ["# CHECKS - BETHLEHEM_ANIMATIC_v1.mp4", "", "Generated by `animatic/check_animatic.py` from `_remotion/public/bethlehem/animatic_data.json` (the same data the comp renders) + ffprobe on the film. $0.", ""]
npass = sum(r[0] == "PASS" for r in res); nfail = sum(r[0] == "FAIL" for r in res)
L += [f"**{npass} PASS, {nfail} FAIL**", "", "| Result | Check | Detail |", "|---|---|---|"]
for s, n, d in res: L.append(f"| {s} | {n} | {d.replace('|','/')} |")
L += ["", "## Clip length vs on-screen time", "", "| Panel | Still | Clip | Clip s | On screen s | Spare s |", "|---|---|---|---|---|---|"]
for c in cl: L.append("| " + " | ".join(map(str, c)) + " |")
L += ["", "## Text items (start-end, seconds)", "", "| Item | Page | Start | End | Dur | Words | s/word | Text |", "|---|---|---|---|---|---|---|---|"]
for it in its:
    dur = (F(it["end"]) - F(it["start"])) / 30; nw = sum(len(l.split()) for l in it["lines"])
    L.append(f"| {it['id']} | {it['page']} | {it['start']:.2f} | {it['end']:.2f} | {dur:.2f} | {nw} | {dur/nw:.2f} | {' / '.join(it['lines'])} |")
L += ["", "## Transitions at their real frames", ""]
for p in D["pages"]:
    L.append(f"- Page {p['n']} {p['name']}: {p['trans'].upper()} starts {p['start']:.2f} s = frame {F(p['start'])}, {p['tf']} frames" + (" (sacred)" if p["sacred"] else ""))
open(A / "CHECKS.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(f"{s}  {n}  {d[:150]}" for s, n, d in res))
sys.exit(1 if nfail else 0)
