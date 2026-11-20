"""$0 VIEWER-FIT page (hub, 2026-11-20): sorts every ready-to-post film by the owner's YouTube Studio lesson
(winners = 40-65 s shorts, a big human moment near Jesus, a paradox/question title).
Length is measured (ffprobe). 'Human moment' and 'title type' are hand calls, listed in CALLS below.
Writes _roadmap\\pipelines\\_VIEWER_FIT.html. Changes nothing else.
  .venv\\Scripts\\python.exe _roadmap\\pipelines\\viewer_fit_page.py"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import release_state as rs  # noqa: E402

e = html.escape
SAME = "Same story as 2 other shorts. Pick one."
# slug -> (human moment near Jesus?, title is paradox/question?, short note)
CALLS = {
    "today-in-paradise": (1, 1, ""), "woman-behold-thy-son": (1, 1, ""), "it-is-finished": (1, 1, ""),
    "father-into-thy-hands": (1, 1, ""), "ps22-03-forsaken-cry": (1, 1, ""), "he-was-asleep-in-the-storm": (1, 1, ""),
    "sign-of-jonah": (1, 1, ""), "the-empty-tomb": (1, 1, ""), "women-first-witnesses": (1, 1, ""),
    "ps22-02-mockers-words": (1, 1, "Also drop the '| Bible' tag from the title."),
    "mary-and-martha-did-he-care": (1, 1, ""),
    "second-fire-he-fed-him-first": (1, 0, "Title 'The Second Fire' is flat. Needs a paradox title."),
    "bronze-serpent-01-look-and-live": (0, 1, SAME),
    "bronze-serpent-02-the-thing-that-killed-them": (0, 1, SAME),
    "moses-and-the-snake-on-a-pole": (0, 1, SAME),
    "bronze-serpent-03-son-of-man-lifted-up": (0, 1, ""),
    "ps22-04-declared-to-brethren": (0, 1, ""), "ps22-05-he-hath-done-this": (0, 1, ""),
    "ps22-06-ends-of-the-earth": (0, 1, ""), "ps22-07-body-foretold": (0, 1, ""),
    "seed-of-woman-01-first-gospel-in-the-curse": (0, 1, ""), "seed-of-woman-02-her-seed": (0, 1, ""),
    "seed-of-woman-03-heel-vs-head": (0, 0, "Title reads like a verse tag."),
    "seed-of-woman-04-serpent-crusher-promised": (0, 1, ""),
    "rahab-and-the-scarlet-cord": (0, 1, ""), "aaron-and-the-two-goats": (0, 1, ""),
}


KEEP_AS_IS = {"ps22-02-mockers-words", "mary-and-martha-did-he-care", "second-fire-he-fed-him-first"}


def url(p):
    return "file:///" + str(Path(p).resolve()).replace("\\", "/")


def secs(v):
    try:
        return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)],
                                    capture_output=True, text=True, timeout=30).stdout.strip())
    except Exception:
        return None


def yt_title(d, fallback):
    f = next(iter(sorted((d / "publish").glob("youtube*.md"))), None) if d else None
    if f:
        m = re.search(r"(?im)^##\s*TITLE\s*\n+(.+)", f.read_text(encoding="utf-8"))
        if m:
            return m.group(1).strip()
    return fallback


def tick(ok, yes, no):
    return f'<span class="{"ok" if ok else "bad"}">{"&#10004;" if ok else "&#10008;"} {e(yes if ok else no)}</span>'


def card(r):
    s = r["s"]
    img = (f'<a href="{e(url(r["thumb"]))}"><img src="{e(url(r["thumb"]))}" alt=""></a>'
           if r["thumb"] and Path(r["thumb"]).exists() else '<div class="noimg">no poster</div>')
    ln = "?" if r["sec"] is None else (f'{r["sec"]:.0f} s' if r["sec"] < 120 else f'{r["sec"] / 60:.0f} min')
    if s.kind == "long":
        checks = f"<p>{ln}</p>"
    else:
        checks = "<p>" + "<br>".join([
            tick(r["len_ok"], f"{ln} (good length)", f"{ln} (aim 40-65 s)"),
            tick(r["human"], "human moment near Jesus", "no human moment near Jesus"),
            tick(r["ttl"], "paradox / question title", "flat title")]) + "</p>"
    note = f'<p class="note">{e(r["note"])}</p>' if r.get("note") else ""
    watch = f'<a href="{e(url(s.video))}">Watch</a>' if s.video and Path(s.video).exists() else '<span class="bad">video missing</span>'
    return f'<div class="card">{img}<div class="body"><h3>{e(r["title"])}</h3>{checks}{note}<p>{watch}</p></div></div>'


def main():
    states, _, _ = rs.gather()
    box = {"post": [], "trim": [], "later": [], "long": []}
    for s, _ in rs.to_post(states):
        d = s.source_dir
        r = dict(s=s, sec=secs(s.video) if s.video else None, title=yt_title(d, s.title or s.slug),
                 thumb=(d / "publish" / "thumbs" / ("thumb_16x9.jpg" if s.kind == "long" else "thumb_1x1.jpg")) if d else None)
        if s.kind == "long":
            box["long"].append(r)
            continue
        r["human"], r["ttl"], r["note"] = CALLS.get(s.slug, (0, 0, "Not judged yet."))
        r["len_ok"] = r["sec"] is not None and 40 <= r["sec"] <= 65
        if s.slug in KEEP_AS_IS:  # owner 2026-11-20: locked films stay as they are, post as-is
            r["note"] = "Owner: keep as is (locked). Post as-is."
            box["post"].append(r)
        elif not r["human"]:
            box["later"].append(r)
        elif r["len_ok"] and r["ttl"]:
            box["post"].append(r)
        else:
            box["trim"].append(r)

    def section(key, head, sub):
        items = sorted(box[key], key=lambda r: r["sec"] or 0)
        return (f'<h2>{head} <span class="cnt">({len(items)})</span></h2><p class="sub">{sub}</p>'
                f'<section class="grp">{"".join(map(card, items))}</section>')

    total = sum(map(len, box.values()))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Viewer Fit</title>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fbf7ee;--ink:#1f1f1f;--soft:#5b5b5b;--card:#fff;--line:#e3dccb;--acc:#2f5fa7;--ok:#1e7a3c;--bad:#c0392b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;--acc:#7aa7ef;--ok:#6fd08c;--bad:#ff8a80}}}}
:root[data-theme="dark"]{{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;--acc:#7aa7ef;--ok:#6fd08c;--bad:#ff8a80}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:20px/1.6 "Atkinson Hyperlegible",Verdana,sans-serif;letter-spacing:.02em;margin:0 auto;padding:20px 16px 60px;max-width:1000px}}
h1{{font-size:34px;margin:0 0 4px}}h2{{font-size:26px;margin:28px 0 0}}h3{{font-size:20px;margin:0 0 4px}}
.sub{{color:var(--soft);margin:2px 0 10px}}.cnt{{color:var(--soft);font-weight:400}}
.grp{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.card{{display:flex;gap:12px;background:var(--card);border:2px solid var(--line);border-radius:12px;padding:10px}}
.card img,.noimg{{width:110px;height:110px;object-fit:cover;border-radius:8px;flex:none;background:var(--line)}}
.noimg{{display:flex;align-items:center;justify-content:center;color:var(--soft);font-size:15px}}
.body{{min-width:0;font-size:17px}}.body p{{margin:0 0 4px}}.note{{font-weight:700}}
.ok{{color:var(--ok)}}.bad{{color:var(--bad);font-weight:700}}a{{color:var(--acc);font-weight:700}}
.pick{{background:var(--card);border:3px solid var(--acc);border-radius:12px;padding:12px 16px}}
</style></head><body>
<h1>Viewer fit: {total} ready films</h1>
<p class="sub">Your YouTube data: winners are short (40-65 s), a big human moment near Jesus, a paradox or question title.</p>
<div class="pick"><b>My pick:</b> post box 1 first. Then trim box 2. Post box 3 slowly, to test.</div>
{section("post", "1. Post first", "Fits all 3.")}
{section("trim", "2. Trim first", "Good story, but too long (or a flat title). Trim = cut a line or two of words, re-cut, fresh check. $0.")}
{section("later", "3. Post later, test slowly", "Good films, but an Old Testament idea, not a human moment near Jesus. Your data says these do less well.")}
{section("long", "4. Long films", "Your data is about shorts. These are a separate test.")}
<p class="sub">Length is measured. 'Human moment' and 'title' are my own calls, not yet checked by a panel.</p>
</body></html>"""
    out = Path(__file__).with_name("_VIEWER_FIT.html")
    out.write_text(page, encoding="utf-8")
    print({k: len(v) for k, v in box.items()}, "->", out)


if __name__ == "__main__":
    main()
