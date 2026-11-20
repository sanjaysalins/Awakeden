"""$0 POSTING page (hub): one simple dyslexia-friendly page of every finished film not yet on YouTube.
Reads pipeline.release_state (same data as _UPLOAD_TRACKER.html) + the two lane films (T12, T13) not yet in the manifest.
Writes _roadmap\\pipelines\\_POSTING.html. Never uploads; after posting, the owner pastes the URL into the shown command.
  .venv\\Scripts\\python.exe _roadmap\\pipelines\\posting_page.py"""
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import release_state as rs  # noqa: E402

e = html.escape
PY = r".venv\Scripts\python.exe"


def url(p):
    return "file:///" + str(Path(p).resolve()).replace("\\", "/")


def secs(v):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        return float(out)
    except Exception:
        return None


def length(v):
    s = secs(v)
    return "?" if s is None else (f"{s:.0f} s" if s < 120 else f"{s / 60:.0f} min")


def card(title, kind, video, poster, pack, slug, note=""):
    img = f'<img src="{e(url(poster))}" alt="">' if poster and Path(poster).exists() else '<div class="noimg">no poster</div>'
    links = [f'<a href="{e(url(video))}">Watch the video</a>'] if video and Path(video).exists() else ['<span class="bad">video file missing</span>']
    links.append(f'<a href="{e(url(pack))}">Open the publish pack (title, text, captions)</a>' if pack and Path(pack).exists()
                 else '<span class="bad">publish pack not built yet</span>')
    cmd = f"{PY} upload_tracker.py --set {slug} youtube PASTE-URL-HERE" if slug else ""
    after = (f'<div class="after"><b>After you post:</b> paste the YouTube link into this line and run it:'
             f'<code>{e(cmd)}</code><button onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent)">Copy</button></div>'
             if cmd else "")
    return (f'<div class="card">{img}<div class="body"><h3>{e(title)}</h3><p class="meta">{e(kind)} · {length(video) if video else "?"}</p>'
            + (f'<p class="note">{e(note)}</p>' if note else "") + "<p>" + "<br>".join(links) + "</p>" + after + "</div></div>")


def main():
    states, _, _ = rs.gather()
    todo = [s for s, _ in rs.to_post(states)]
    groups = {}
    for s in todo:
        groups.setdefault(s.cluster or s.parent or s.slug, []).append(s)
    def newest(g):
        return max((Path(s.video).stat().st_mtime for s in g if s.video and Path(s.video).exists()), default=0)
    order = sorted(groups.values(), key=newest, reverse=True)
    blocks = []
    for g in order:
        g.sort(key=lambda s: (s.kind != "long", s.cluster_order or 0, s.slug))
        cards = []
        for s in g:
            d = s.source_dir
            th = d / "publish" / "thumbs" / ("thumb_16x9.jpg" if s.kind == "long" else "thumb_1x1.jpg") if d else None
            cards.append(card(s.title or s.slug, "Long film" if s.kind == "long" else "Short", s.video, th,
                              d / "publish" / "PUBLISH_INDEX.html" if d else None, s.slug))
        lead = g[0].title if g[0].kind == "long" else f"A set of {len(g)} shorts, starting with “{g[0].title}”"
        head = f'<h2>{e(lead)} <span class="cnt">({len(g)} films: post together)</span></h2>' if len(g) > 1 else ""
        blocks.append(f'<section class="grp">{head}{"".join(cards)}</section>')
    c5 = ROOT / "batches" / "cluster_05_prophecy"  # both packs built + red-teamed 2026-11-18/19 (not in the manifest yet)
    new = [card("Jesus Walks on Water. Job Said Only God Does. (Job 9 -> Mark 6)", "Short, comic style",
                c5 / "job_sea_short/visual/job_sea_final.mp4", c5 / "job_sea_short/publish/thumbs/thumb_1x1.jpg",
                c5 / "job_sea_short/publish/PUBLISH_INDEX.html", None,
                "Ready to post today (release 2026-11-20; rights checked by owner). After you post, tell me the link."),
           card("Can One Man Heal and Forgive? (Isaiah 6 -> Mark 2)", "Short, comic style",
                c5 / "can_one_man_short/visual/can_one_man_final.mp4", c5 / "can_one_man_short/publish/thumbs/thumb_1x1.jpg",
                c5 / "can_one_man_short/publish/PUBLISH_INDEX.html", None,
                "Ready to post today (release 2026-11-20). After you post, tell me the link.")]
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Films To Post</title>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fbf7ee;--ink:#1f1f1f;--soft:#5b5b5b;--card:#fff;--line:#e3dccb;--acc:#2f5fa7;--bad:#c0392b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;--acc:#7aa7ef;--bad:#ff8a80}}}}
:root[data-theme="dark"]{{--bg:#1b1a17;--ink:#f1eee6;--soft:#b9b4a8;--card:#26241f;--line:#3a372f;--acc:#7aa7ef;--bad:#ff8a80}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font:20px/1.6 "Atkinson Hyperlegible",Verdana,sans-serif;letter-spacing:.02em;margin:0 auto;padding:20px 16px 60px;max-width:1000px}}
h1{{font-size:34px;margin:0 0 4px}}h2{{font-size:25px;margin:0 0 10px}}h3{{font-size:22px;margin:0 0 2px}}
.sub{{color:var(--soft)}}.cnt{{color:var(--soft);font-size:18px;font-weight:400}}
.grp{{border:2px solid var(--line);border-radius:14px;padding:14px;margin:0 0 20px;background:var(--bg)}}
.card{{display:flex;gap:16px;background:var(--card);border:2px solid var(--line);border-radius:12px;padding:12px;margin:0 0 10px}}
.card img,.noimg{{width:200px;height:200px;object-fit:cover;border-radius:8px;flex:none;background:var(--line)}}
.noimg{{display:flex;align-items:center;justify-content:center;color:var(--soft);font-size:16px}}
.body{{min-width:0}}.meta{{color:var(--soft);margin:0 0 6px}}.note{{margin:0 0 6px;font-weight:700}}
a{{color:var(--acc);font-weight:700}}.bad{{color:var(--bad);font-weight:700}}
.after{{font-size:16px;margin-top:6px}}code{{display:block;background:var(--line);padding:6px 8px;border-radius:6px;word-break:break-all;margin:4px 0}}
button{{font:inherit;font-size:16px;padding:4px 14px;border-radius:8px;border:2px solid var(--acc);background:var(--card);color:var(--acc);cursor:pointer}}
@media (max-width:640px){{.card{{flex-direction:column}}.card img,.noimg{{width:100%;height:auto;aspect-ratio:1}}body{{font-size:19px}}}}
</style></head><body>
<h1>Films to post</h1>
<p class="sub">{len(todo)} finished films are not on YouTube yet, plus 2 new ones. Post from the top down. Films in one box go together.</p>
<h2>Post today</h2><section class="grp">{"".join(new)}</section>
<h2>Ready to post now</h2>
{"".join(blocks)}
</body></html>"""
    out = Path(__file__).with_name("_POSTING.html")
    out.write_text(page, encoding="utf-8")
    print(f"{len(todo)} films ready + 2 new -> {out}")


if __name__ == "__main__":
    main()
