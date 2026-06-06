"""Generate PRODUCTION_TRACKER.html + PRODUCTION_PLAN.md — the comprehensive plan & state.

Built FROM data/series.json (the greenlit source of truth — 76 episodes / 10 series) so
nothing is silently dropped. Red-team-revised (2026-06-06):
- Funnel: shorts = snack/hook; long-forms = the deep researched meal that SUPPORTS them.
- Long TIERING (not 1:1): Tier-1 series-anchor long (1/series) backs the long tail;
  Tier-2 flagship dedicated longs only for rich texts; Tier-3 = short backed by the anchor.
- Every short shows its supporting long AND whether that long EXISTS (mp3+) or is a placeholder.
- series.json guardrails + brand carried per series; theme per episode.
- Status from on-disk scan (cut = assembled POC, not 'approved'); upload = GDrive posting tracker.
- Off-catalog existing work + not-yet-greenlit channel flagships listed separately, clearly tagged.
Stages: planned->narration->mp3->stills->clips->cut(POC)->captioned->uploaded(COMPLETE)."""
import html, json, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHORTS_ROOT = Path("C:/Users/sanjay/PycharmProjects/PythonProject1/jesus/narration")
LONG_ROOT = ROOT / "longform"
SERIES_JSON = json.loads((ROOT / "data" / "series.json").read_text(encoding="utf-8"))["series"]

STAGES = ["planned", "narration", "mp3", "stills", "clips", "cut", "captioned", "uploaded"]
STAGE_LABEL = {"planned": "Planned", "narration": "Narration", "mp3": "MP3 ready",
               "stills": "Stills", "clips": "Clips", "cut": "Cut (POC)", "captioned": "Captioned",
               "uploaded": "COMPLETE"}
STAGE_COLOR = {"planned": "#5b5446", "narration": "#3b6ea5", "mp3": "#2e8b8b", "stills": "#7d5ba6",
               "clips": "#c2772e", "cut": "#caa24a", "captioned": "#7bb661", "uploaded": "#46c463"}
SI = {s: i for i, s in enumerate(STAGES)}
# Cost derived from CLAUDE.md's own model: ~$23/short (Kling ~$11 + images ~$5 + Opus ~$5-6
# + audio ~$0.5); a clean long ~$30 (Isaiah pilot was ~$48 WITH redos). Captions/thumbnails are
# ~$0 tooling but cost TIME. These are metered-$ only, exclude human-gate/review time.
COST_SHORT, COST_LONG = 23, 35
REMAIN_FACTOR = {"planned": 1.0, "narration": 0.95, "mp3": 0.80, "stills": 0.45, "clips": 0.15,
                 "cut": 0.0, "captioned": 0.0, "uploaded": 0.0}
MULTIDIM = 1.5   # series.json is 1:1, but production ships ~N dims/episode (Bread=3) → real short load
CONTINGENCY = 1.3  # retries / re-renders / gate failures (common per STATE.md)

# ---- TIER-2 flagship longs: rich texts that get a dedicated deep-dive (ref -> long) ----
# id, title, ref, stage, folders, note. A short whose primary_ref is here is backed by it.
FLAGSHIPS = [
    ("isa53", "Isaiah 53 — The Suffering Servant", "Isaiah 53:5", "captioned", ["01_Isaiah"], "READY TO POST"),
    ("ps22", "Psalm 22 — The Song From the Cross", "Psalm 22:16", "mp3", ["02_Psalm"], "ACTIVE — next: scene plan"),
    ("ps22b", "Psalm 22 (cross-word)", "Matthew 27:46", "mp3", ["02_Psalm"], "same long as Ps 22 flagship"),
    ("passover", "The Passover Lamb", "John 1:29", "planned", [], "BATCH"),
    ("serpent", "The Bronze Serpent", "John 3:14", "planned", [], "BATCH"),
    ("itfin", "It Is Finished — tetelestai", "John 19:30", "planned", [], "BATCH (shared w/ last-week)"),
    ("well", "The Woman at the Well", "John 4:14", "planned", [], ""),
    ("lazarus", "Lazarus — Resurrection & the Life", "John 11:25", "planned", [], "backs Lazarus + I AM Resurrection"),
    ("emptytomb", "The Empty Tomb — He Is Risen", "Matthew 28:6", "planned", [], "flagship resurrection deep-dive"),
    ("seed", "The Seed of the Woman", "Genesis 3:15", "planned", [], "the first gospel"),
    ("greatiam", "The Great I AM", "Exodus 3:14", "planned", [], "burning bush -> Jn 8:58"),
    ("jonah", "The Sign of Jonah", "Jonah 1:17", "planned", [], "death & resurrection sign"),
]
FLAG_BY_REF = {f[2]: f for f in FLAGSHIPS}

# ---- STATUS OVERLAY: (series_id, primary_ref) -> (stage, [folder prefixes], takes note) ----
ST = {
    ("i-am", "John 6:35"): ("cut", ["34", "35", "36"], "3 shipped dims: #34 Hunger · #35 Manna · #36 No Wise Cast Out"),
    ("i-am", "John 8:12"): ("mp3", ["06", "31"], "#06 · #31 Light You Can Stand In"),
    ("i-am", "John 10:9"): ("cut", ["32", "07"], "#32 Door Was a Body (CUT) · #07 (mp3)"),
    ("i-am", "John 10:11"): ("cut", ["33"], "#33 Shepherd In The Gap"),
    ("jesus-in-ot", "Isaiah 53:5"): ("mp3", ["30", "21", "25"], "3 dims: #30 Smitten · #21 Pronouns · #25 Gaza Road"),
    ("jesus-in-ot", "Psalm 22:16"): ("mp3", ["04"], "#04 psalms 22 part 2"),
    ("jesus-in-ot", "Jonah 1:17"): ("narration", ["23"], "#23 The Prepared Belly (no mp3)"),
    ("questions-jesus-asked", "Matthew 16:15"): ("mp3", ["Who Do You Say", "27", "24", "19"], "#WhoDoYouSay · #27 · #24 · #19 (mp3)"),
    ("questions-jesus-asked", "Matthew 8:26"): ("cut", ["02", "28", "20"], "#02 (CUT v3) · #28 · #20 (mp3)"),
    ("questions-jesus-asked", "John 5:6"): ("cut", ["18", "29", "26", "22"], "#18 He Never Said Yes (CUT) · +3 mp3"),
    ("questions-jesus-asked", "John 21:17"): ("cut", ["16"], "#16 The Fire Jesus Built"),
    ("encounters", "John 4:14"): ("cut", ["08"], "#08 The Well That Never Runs Dry"),
    ("encounters", "John 21:17"): ("cut", ["16"], "cross-filed w/ QJA #16 (Peter restored)"),
    ("miracles-signs", "Mark 4:39"): ("mp3", ["20"], "#20 He Was Asleep in the Storm (cross-filed)"),
    ("last-week", "John 19:30"): ("planned", [], "cross-filed w/ words-from-cross"),
}

# ---- OFF-CATALOG existing work (real folders not in series.json) ----
OFFCAT = [
    ("The Prodigal Son — the kiss that cut off the bargain", "Luke 15:20", "cut", ["12"],
     "#12 (CUT) · +mp3 #09 Father Who Ran, #10 Line Never Said, #11 Confession — multi-dim. NOT a greenlit series.json episode (parables backlog)."),
    ("He Said It Under the Lamps", "John 8?", "narration", ["05"], "#05 incomplete (no mp3) — orphan."),
]

# ---- BACKLOG: channel flagships NOT yet greenlit — a proposed 'core-gospel' bucket ----
# (title, ref, kind, proposed_series) — the funnel applies: flagship longs anchor clusters of shorts.
BACKLOG = [
    # --- flagship deep-dive LONGS (the meat) ---
    ("Resurrection Morning — the whole account", "Matthew 28 / John 20", "long", "core-resurrection"),
    ("The Incarnation — the Word made flesh", "John 1:1-14 / Luke 2", "long", "core-incarnation"),
    ("The Sermon on the Mount", "Matthew 5-7", "long", "core-teaching"),
    ("The Last Supper — communion instituted", "Luke 22:19", "long", "core-passion"),
    ("The Transfiguration", "Matthew 17:2", "long", "core-glory"),
    ("The Great Commission & the Ascension", "Matthew 28:19 / Acts 1:9", "long", "core-sending"),
    ("Pentecost — the Spirit poured out", "Acts 2", "long", "core-sending"),
    ("Abraham & Isaac (the Akedah)", "Genesis 22", "long", "types-shadows?"),
    # --- shorts (the snacks), each would draw on a flagship above ---
    ("For God so loved the world", "John 3:16", "short", "core-incarnation"),
    ("Ye must be born again", "John 3:3", "short", "core-incarnation"),
    ("The Lord's Prayer", "Matthew 6:9", "short", "core-teaching"),
    ("The Beatitudes — blessed are", "Matthew 5:3", "short", "core-teaching"),
    ("Salt and light", "Matthew 5:13-16", "short", "core-teaching"),
    ("The Good Samaritan", "Luke 10:33", "short", "core-parables"),
    ("The Parable of the Sower", "Matthew 13:3", "short", "core-parables"),
    ("The Lost Sheep / Lost Coin", "Luke 15:4-10", "short", "core-parables"),
    ("The Mustard Seed", "Matthew 13:31", "short", "core-parables"),
    ("The Baptism of Jesus", "Matthew 3:16", "short", "core-incarnation"),
    ("This is my body / my blood", "Luke 22:19-20", "short", "core-passion"),
    ("He is risen — the angel's word", "Matthew 28:6", "short", "core-resurrection"),
    ("Go ye therefore", "Matthew 28:19", "short", "core-sending"),
]

# ===================== build model =====================
LONGS, SHORTS = [], []
for s in SERIES_JSON:
    sid = s["id"]
    # Tier-1 series anchor long
    LONGS.append(dict(id=f"anchor_{sid}", series=sid, tier=1, title=f"{s['name']} (series deep-dive)",
                      ref=s.get("hook_pattern", ""), stage="planned", folders=[],
                      note="SERIES ANCHOR — backs the shorts that have no dedicated flagship", kind="long"))
    # shorts = the series' greenlit episodes
    for e in s["episodes"]:
        ref = e.get("primary_ref", "")
        stage, folders, takes = ST.get((sid, ref), ("planned", [], ""))
        flag = FLAG_BY_REF.get(ref)
        support = flag[0] if flag else f"anchor_{sid}"
        SHORTS.append(dict(series=sid, title=e["title"], ref=ref, theme=e.get("theme", ""),
                           support=support, stage=stage, folders=folders, takes=takes, kind="short"))
# Tier-2 flagship longs (dedupe ps22/ps22b share a film)
seen_flag = set()
for fid, ftitle, fref, fstage, ffolders, fnote in FLAGSHIPS:
    if fid in ("ps22b",):   # alias of ps22, don't list twice
        continue
    # find which series this flagship lives in (by the episode ref)
    fser = next((s["id"] for s in SERIES_JSON for e in s["episodes"] if e.get("primary_ref") == fref), "jesus-in-ot")
    LONGS.append(dict(id=fid, series=fser, tier=2, title=ftitle, ref=fref, stage=fstage,
                      folders=ffolders, note=("FLAGSHIP · " + fnote) if fnote else "FLAGSHIP", kind="long"))
LONG_BY_ID = {l["id"]: l for l in LONGS}
# ps22b alias resolves to ps22
LONG_BY_ID["ps22b"] = LONG_BY_ID.get("ps22")
SER_META = {s["id"]: s for s in SERIES_JSON}

# ===================== assets =====================
def furl(p): return "file:///" + urllib.parse.quote(str(p).replace("\\", "/"), safe="/:")
def match_folder(root, hint):
    for d in root.iterdir():
        if d.is_dir() and (d.name == hint or d.name.startswith(hint + " ") or d.name.startswith(hint + "_")):
            return d
    return None
def assets_for(entry):
    root = LONG_ROOT if entry["kind"] == "long" else SHORTS_ROOT
    links = []
    for hint in entry.get("folders", []):
        folder = match_folder(root, hint)
        if not folder:
            continue
        vdirs = sorted([p for p in folder.glob("v*") if p.is_dir()]) or [folder]
        v = max(vdirs, key=lambda x: (bool(list(x.glob("assembly/viral_cut.mp4")) or list(x.glob("visual_16x9/*16x9.mp4"))), (x / "narration.mp3").exists()))
        def add(ic, lb, p):
            if p and p.exists(): links.append((ic, lb, furl(p)))
        add("📄", "script", v / "narration.md"); add("🔊", "mp3", v / "narration.mp3")
        if entry["kind"] == "short":
            add("🎞", "cut", v / "assembly" / "viral_cut.mp4")
            add("🎬", "reel", v / "assembly" / "all_takes_reel.mp4")
            add("🖼", "stills", next(iter(v.glob("visual/*/index.html")), None))
        else:
            films = [p for p in v.glob("visual_16x9/*16x9.mp4") if "bak" not in p.name and "captioned" not in p.name]
            if films: add("🎬", "film", films[0])
            add("💬", "captioned", next(iter(v.glob("visual_16x9/*captioned.mp4")), None))
            add("🖼", "gallery", v / "visual_16x9" / "index.html")
    seen, out = set(), []
    for ic, lb, u in links:
        if lb not in seen: seen.add(lb); out.append((ic, lb, u))
    return out

# ===================== metrics =====================
all_e = LONGS + SHORTS
n_long, n_short = len(LONGS), len(SHORTS)
n_started = sum(1 for e in all_e if e["stage"] != "planned")
n_mp3 = sum(1 for e in all_e if SI[e["stage"]] >= SI["mp3"])
n_cut = sum(1 for e in all_e if SI[e["stage"]] >= SI["cut"])
n_complete = sum(1 for e in all_e if e["stage"] == "uploaded")
# shorts whose supporting long is NOT yet at mp3+ (the honest "awaiting their long" number)
awaiting = [s for s in SHORTS if SI[LONG_BY_ID.get(s["support"], {"stage": "planned"})["stage"]] < SI["mp3"]]
# honest cost RANGE (panel: the flat $1940 was a toy). low = base metered; high = ×multidim ×contingency.
_short_remain = sum(COST_SHORT * REMAIN_FACTOR[s["stage"]] for s in SHORTS)
_long_remain = sum(COST_LONG * REMAIN_FACTOR[l["stage"]] for l in LONGS)
cost_low = round((_short_remain + _long_remain) / 50) * 50
cost_high = round((_short_remain * MULTIDIM + _long_remain) * CONTINGENCY / 50) * 50

# ===================== render html =====================
def badge(st): return f'<span class="badge" style="background:{STAGE_COLOR[st]}">{STAGE_LABEL[st]}</span>'
def bar(st): return '<span class="bar">' + "".join(f'<span class="seg" style="background:{STAGE_COLOR[s] if (i<=SI[st] and st!="planned") else "#2a2418"}"></span>' for i, s in enumerate(STAGES)) + '</span>'
def alinks(e):
    a = assets_for(e)
    return "".join(f'<a class="al" href="{u}" target="_blank">{ic} {lb}</a>' for ic, lb, u in a) or '<span class="noasset">—</span>'

sections = []
for s in SERIES_JSON:
    sid = s["id"]
    longs = sorted([l for l in LONGS if l["series"] == sid], key=lambda e: (e["tier"], -SI[e["stage"]]))
    shorts = sorted([sh for sh in SHORTS if sh["series"] == sid], key=lambda e: (-SI[e["stage"]], e["title"]))
    rows = ""
    for l in longs:
        tier = "⚓ anchor" if l["tier"] == 1 else "★ flagship"
        backs = sum(1 for sh in SHORTS if sh["support"] == l["id"]) + (sum(1 for sh in SHORTS if sh["support"] == "ps22b") if l["id"] == "ps22" else 0)
        note = f'<span class="enote">{html.escape(l["note"])}</span>' if l["note"] else ""
        rows += f'<tr class="row" data-stage="{l["stage"]}" data-kind="long"><td class="kind">🎬 {tier}</td><td class="ttl"><b>{html.escape(l["title"])}</b><span class="ref">{html.escape(l["ref"])}</span>{note}<span class="supn">backs {backs} short(s)</span></td><td class="st">{badge(l["stage"])}</td><td class="pg">{bar(l["stage"])}</td><td class="as">{alinks(l)}</td></tr>'
    for sh in shorts:
        sl = LONG_BY_ID.get(sh["support"])
        if sl and SI[sl["stage"]] >= SI["mp3"]:
            backed = f'<span class="backed">⤷ backed by: {html.escape(sl["title"])} {badge(sl["stage"])}</span>'
        elif sl:
            backed = f'<span class="retro">⤷ long not built yet: {html.escape(sl["title"])} (retrofit)</span>'
        else:
            backed = '<span class="needlong">⚠ NEEDS a supporting long</span>'
        theme = f'<span class="theme">{html.escape(sh["theme"])}</span>' if sh.get("theme") else ""
        takes = f'<span class="enote">{html.escape(sh["takes"])}</span>' if sh.get("takes") else ""
        rows += f'<tr class="row" data-stage="{sh["stage"]}" data-kind="short"><td class="kind">📱 short</td><td class="ttl"><b>{html.escape(sh["title"])}</b><span class="ref">{html.escape(sh["ref"])}</span>{theme}{takes}<br>{backed}</td><td class="st">{badge(sh["stage"])}</td><td class="pg">{bar(sh["stage"])}</td><td class="as">{alinks(sh)}</td></tr>'
    donecut = sum(1 for e in longs + shorts if SI[e["stage"]] >= SI["cut"])
    g = html.escape(s.get("guardrails", "")); cta = html.escape(s.get("cta_pattern", ""))
    sections.append(f'<section class="series"><h2>{html.escape(s["name"])} <span class="sid">{sid} · {html.escape(s.get("brand",""))}</span><span class="scount">{len(longs)} long · {len(shorts)} short · {donecut} cut+</span></h2><p class="sblurb">{html.escape(s.get("concept",""))}</p><p class="guard">⚖ guardrail: {g}<br>CTA: {cta}</p><table>{rows}</table></section>')

# off-catalog + backlog
off_rows = ""
for title, ref, stage, folders, note in OFFCAT:
    e = dict(kind="short", folders=folders, stage=stage)
    off_rows += f'<tr class="row" data-stage="{stage}" data-kind="short"><td class="kind">📱 off-cat</td><td class="ttl"><b>{html.escape(title)}</b><span class="ref">{html.escape(ref)}</span><span class="enote">{html.escape(note)}</span></td><td class="st">{badge(stage)}</td><td class="pg">{bar(stage)}</td><td class="as">{alinks(e)}</td></tr>'
back_rows = "".join(f'<tr class="row" data-stage="planned" data-kind="{k}"><td class="kind">{"🎬 long" if k=="long" else "📱 short"}</td><td class="ttl"><b>{html.escape(t)}</b><span class="ref">{html.escape(r)}</span><span class="enote">candidate · proposed bucket: {html.escape(ps)}</span></td><td class="st">{badge("planned")}</td><td class="pg">{bar("planned")}</td><td class="as">—</td></tr>' for t, r, k, ps in BACKLOG)
sections.append(f'<section class="series"><h2>Off-catalog existing work <span class="sid">not in series.json</span></h2><p class="sblurb">Real folders on disk that aren\'t a greenlit series.json episode.</p><table>{off_rows}</table></section>')
sections.append(f'<section class="series"><h2>Backlog — channel flagships to consider <span class="sid">candidates</span></h2><p class="sblurb">Core gospel topics a "Jesus in the Bible" channel arguably needs — NOT yet greenlit. Decide whether to add.</p><table>{back_rows}</table></section>')

legend = "".join(f'<span class="lg"><span class="dot" style="background:{STAGE_COLOR[s]}"></span>{STAGE_LABEL[s]}</span>' for s in STAGES)
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gospel Shorts + Long-Form — Production Plan &amp; State</title><style>
:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#14110d;color:#e9e0cf;font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
header{{padding:22px 26px;border-bottom:1px solid #332b20;background:#181410}}h1{{margin:0 0 4px;font-size:22px}}.tag{{color:#9c8e74;font-size:13px;max-width:1000px}}
.cards{{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0 4px}}.c{{background:#1d1810;border:1px solid #332b20;border-radius:10px;padding:10px 16px;min-width:108px}}.c b{{display:block;font-size:25px;color:#e7c98a}}.c span{{font-size:12px;color:#9c8e74}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;padding:12px 26px;border-bottom:1px solid #332b20;background:#16120d;font-size:12px;position:sticky;top:0;z-index:5}}.lg{{display:flex;align-items:center;gap:6px;color:#cdbf9f}}.dot{{width:11px;height:11px;border-radius:3px}}
.filters{{padding:10px 26px;display:flex;gap:8px;flex-wrap:wrap;border-bottom:1px solid #332b20}}.filters button{{background:#2a2318;color:#e9e0cf;border:1px solid #4a3f2c;border-radius:6px;padding:5px 11px;cursor:pointer;font-size:12px}}.filters button.on{{background:#6b5836;border-color:#8a724a}}
main{{padding:8px 26px 60px;max-width:1200px}}.series{{margin:26px 0}}h2{{font-size:18px;margin:0 0 2px;border-bottom:1px solid #2a2418;padding-bottom:6px}}
.sid{{font-size:11px;color:#80745c;font-weight:400;background:#221c13;padding:2px 7px;border-radius:20px;margin-left:6px}}.scount{{float:right;font-size:12px;color:#9c8e74;font-weight:400}}
.sblurb{{color:#9c8e74;font-size:13px;margin:4px 0 4px}}.guard{{color:#9d8a6f;font-size:11.5px;margin:0 0 10px;font-style:italic}}
table{{width:100%;border-collapse:collapse}}tr.row{{border-bottom:1px solid #221c13}}td{{padding:9px 8px;vertical-align:top}}
.kind{{white-space:nowrap;color:#b9a888;font-size:12px;width:92px}}.ttl b{{color:#ece3d0}}.ref{{color:#80745c;font-size:12px;margin-left:8px}}
.theme{{display:block;color:#8a93a0;font-size:11.5px;margin-top:2px}}.enote{{color:#c79a5a;font-size:11.5px;margin-left:0;font-style:italic}}.supn{{display:block;color:#6f8a9d;font-size:11px;margin-top:2px}}
.backed{{color:#8a9d7a;font-size:11.5px}}.retro{{color:#d6a24a;font-size:11.5px;font-weight:600}}.needlong{{color:#d96a6a;font-size:11.5px;font-weight:700}}
.st{{width:108px}}.badge{{font-size:11px;padding:3px 9px;border-radius:20px;color:#16120d;font-weight:600;white-space:nowrap}}
.pg{{width:160px;white-space:nowrap}}.bar{{display:inline-flex;gap:2px}}.seg{{width:15px;height:9px;border-radius:2px}}
.as{{width:220px}}.al{{display:inline-block;background:#23301f;color:#bfe0a8;border:1px solid #3c5a2c;border-radius:6px;padding:2px 7px;margin:2px 3px 0 0;font-size:11px;text-decoration:none}}.al:hover{{background:#33491f}}.noasset{{color:#5b5446}}
</style></head><body>
<header><h1>Gospel Shorts + Long-Form — Production Plan &amp; State</h1>
<div class="tag">Built from <b>data/series.json</b> (the greenlit catalog). Funnel: shorts = snack/hook · long-forms = the deep researched meal that supports them.
<b>Long tiering:</b> ⚓ one series-anchor long backs the tail · ★ flagship dedicated longs for rich texts · the rest are shorts backed by their anchor.
Green pills open completed assets. <b>cut = assembled POC</b> (not yet approved/uploaded). Scanned 2026-06-06; upload status = GDrive posting tracker.</div>
<div class="cards">
<div class="c"><b>{n_long+n_short}</b><span>topics<br>({n_long} long · {n_short} short)</span></div>
<div class="c"><b>{n_started}</b><span>started</span></div>
<div class="c"><b>{n_cut}</b><span>cut+ (POC)</span></div>
<div class="c"><b>{n_complete}</b><span>COMPLETE<br>(uploaded)</span></div>
<div class="c"><b>{len(awaiting)}</b><span>shorts awaiting<br>their long (mp3+)</span></div>
<div class="c"><b>~${cost_low}-{cost_high}</b><span>metered $ to cut all<br>(×multidim ×retries)</span></div>
</div>
<div class="tag" style="margin-top:10px"><b>Gated pipeline (done-definitions):</b> narration → <b>PANEL review</b> → mp3 (audio gate) → stills (image gate) → clips (clip gate) → cut POC → <b>QA watch</b> → captioned → <b>upload kit</b> (title/desc/hashtags/thumbnail ×4 platforms) → uploaded.
&nbsp; <b>Master plan</b> = this doc; <b>sub-plans</b> = BATCH_PLAN.md (batching) + PRODUCER_ORCHESTRATOR_PLAN.md (red-teamed: don't build yet).</div>
</header>
<div class="legend">{legend}</div>
<div class="filters">
<button class="on" data-f="all" onclick="filt('all',this)">All</button>
<button data-f="long" onclick="filt('long',this)">🎬 Long-form</button>
<button data-f="short" onclick="filt('short',this)">📱 Shorts</button>
<button data-f="planned" onclick="filt('planned',this)">Not started</button>
<button data-f="cut" onclick="filt('cut',this)">Cut+ (review)</button>
</div>
<main>{''.join(sections)}</main>
<script>function filt(f,btn){{document.querySelectorAll('.filters button').forEach(b=>b.classList.remove('on'));btn.classList.add('on');document.querySelectorAll('tr.row').forEach(r=>{{let show=true;if(f==='long'||f==='short')show=r.dataset.kind===f;else if(f==='planned')show=r.dataset.stage==='planned';else if(f==='cut')show=['cut','captioned','uploaded'].includes(r.dataset.stage);r.style.display=show?'':'none';}});document.querySelectorAll('.series').forEach(s=>{{s.style.display=[...s.querySelectorAll('tr.row')].some(r=>r.style.display!=='none')?'':'none';}});}}</script>
</body></html>"""
(ROOT / "PRODUCTION_TRACKER.html").write_text(doc, encoding="utf-8")

# ===================== markdown plan (for the AI panel) =====================
md = [f"# Gospel Shorts + Long-Form — Comprehensive Production Plan & State\n",
      "Built from `data/series.json` (10 greenlit series / 76 episodes). Red-team + 5-CLI panel reviewed 2026-06-06; this is the revised master plan.\n",
      "## 1. Strategy (the funnel — honest version)\n"
      "- **Shorts = snack/hook** (60s viral entry); **long-forms = the deep, researched meal** that supports them.\n"
      "- **Long TIERING (a dedicated long per short is NOT the goal — the panel showed that's ~$2k+ of compilations nobody clicks):**\n"
      "  - **★ Flagship long** — a real, dedicated deep-dive for a RICH text (Isaiah 53, Psalm 22, Passover, Serpent…). This genuinely 'backs' its short(s). ~12 of these.\n"
      "  - **Standalone short** — most shorts stand on their own (self-contained gospel hit); they are NOT 'distilled from' a long.\n"
      "  - **⚓ Series-anchor long = OPTIONAL overview/playlist hub, a catalog placeholder — NOT a per-short research meal.** Build only if a series earns it. (Panel fix: stop pretending all 76 are 'backed'.)\n"
      "- **Write-long-first applies to FLAGSHIP texts only** (Isaiah 53, Psalm 22 prove it). Existing standalone shorts are kept as-is; they don't need a retrofit unless a flagship is later built on that text.\n"
      "- **Reuse:** batch audio, then a stills REUSE AUDIT — bounded to same-format (16:9≠9:16) thread-NEUTRAL plates (topical-fit gate). Honest expectation ~15-25%, strong ONLY in the cross/types cluster. Tooling (long-form reuse audit) is NOT built yet — a prerequisite, not an assumption.\n",
      f"## 2. State\n- {n_long} longs + {n_short} catalog shorts. Started {n_started}. Cut+ (POC) {n_cut}. **COMPLETE (uploaded) {n_complete}.**\n"
      f"- Shorts whose flagship/anchor long isn't built yet: {len(awaiting)} (mostly fine — they're standalone).\n"
      f"- **Multi-dimension:** series.json is 1:1, but production ships ~N faithful dims/episode (I AM Bread = 3 shipped). Real short folders > 76; cost scaled by ~{MULTIDIM}×.\n",
      "## 3. PROOF-FIRST priority (panel: don't build inventory before proving the publish loop)\n"
      "1. **PUBLISH Isaiah 53 NOW** — it's captioned/ready. Build its upload kit (title/desc/hashtags/thumbnail), post to YT (+TT/FB/IG), link the short cuts to it. Prove the whole loop end-to-end ONCE.\n"
      "2. **Finish Psalm 22 long end-to-end** (scene plan → stills → clips → assemble → caption → publish) — the SECOND template; confirms the episode-generic drivers work on episode 2.\n"
      "3. **Audit the 9 existing cut POCs** (keep / re-cut / retire) and publish the keepers with kits — turn POCs into COMPLETE before making more.\n"
      "4. **THEN the passion BATCH** (words-from-cross + types-shadows flagships + their shorts) — only after the template + publish loop is proven and a reuse-audit tool exists.\n"
      "5. Roll out remaining series by brand (SLK first), measured against analytics from steps 1-3.\n",
      "## 4. Gated pipeline & done-definitions (panel: state list ≠ pipeline)\n"
      "`planned → narration → PANEL(enforced) → mp3 → stills → clips → cut(POC) → QA-watch → captioned → upload-kit → uploaded(COMPLETE)`\n"
      "- **narration done** = script locked AFTER in-engine red-team + enforced `independent_review.py` panel (mandatory per CLAUDE.md).\n"
      "- **mp3 done** = audio rendered + human audio-gate approved.\n- **stills/clips done** = image-gate / clip-gate approved (the 3 human gates from cli_pipeline.py).\n"
      "- **cut(POC)** = assembled `viral_cut.mp4` — NOT a release; a POC the engine is still iterating.\n- **QA-watch** = human watches the whole clip (≥6 frames/scene) for morph/anatomy/glitter; re-gen on fail.\n"
      "- **captioned** = veed_io caption burn (the locked last step).\n- **upload-kit** = title/desc/hashtags/thumbnail per platform.\n- **uploaded(COMPLETE)** = live on the platform + logged in the GDrive posting tracker.\n",
      f"## 5. Cost (derived, not the old flat $1940)\n"
      f"- Per CLAUDE.md: **~$23/short** (Kling ~$11 + images ~$5 + Opus ~$5-6 + audio); **~${COST_LONG}/long** clean (Isaiah pilot ~$48 WITH redos).\n"
      f"- **Metered $ to take everything to a CUT: ~${cost_low}-{cost_high}** (low = base; high = ×{MULTIDIM} multi-dim shorts ×{CONTINGENCY} retries). Excludes human-gate/review TIME.\n"
      "- 'To a cut' is NOT the goal — captions are ~$0 tooling but thumbnails + upload kits + the panel/QA passes cost TIME, the real bottleneck.\n"
      "- **Reuse can only lower this AFTER the audit tool exists and the cross/types library is seeded** — don't bank the savings yet.\n",
      "## 6. Distribution (the channel's actual purpose — was missing)\n"
      "- **Platforms:** YouTube (longs + shorts), TikTok, FB, IG Reels — the user's 4-platform tracker.\n"
      "- **Per-clip upload kit:** title · description (with the short→backing-long link) · hashtags · thumbnail · safe-area caption check. Wire to `0 Christianity/PRODUCTION & POSTING TRACKER.md` on GDrive.\n"
      "- **Cross-link:** every short's description points to its flagship long ('full story → deep-dive'); every long pins its shorts.\n"
      "- **Cadence:** decide shorts/week + long/2-weeks AFTER steps 1-2 give real retention data. Brand rollout: SLK → Awakeden → Either.\n",
      "## 7. Cross-series collisions (same verse, two series — resolve, don't double-count)\n"
      "- **John 19:30 'It is finished'** — words-from-cross (primary) ↔ last-week (cross-file, don't rebuild; differentiate by lens: atonement vs chronology).\n"
      "- **Jonah** — jesus-in-ot 'Sign of Jonah' (primary) ↔ types-shadows 'Jonah three days' (cross-file; one asset).\n"
      "- **John 21:17** — QJA 'Do You Love Me' (#16, primary) ↔ encounters 'Peter restored' (same clip; QJA's three-voice vs encounters' anti-psychologising — pick QJA's framing).\n"
      "- **Luke 23:43** — words-from-cross 'Today in paradise' ↔ encounters 'thief on the cross' (one asset, two playlists).\n"
      "- **John 1:29 'Lamb'** — types-shadows 'Passover Lamb' (flagship) ↔ names-titles 'Lamb of God' (title lens; share the flagship long, distinct short hooks).\n"
      "- Headline '76' counts catalog ROWS; **distinct content is ~70** after these cross-files.\n",
      "## 8. Doctrinal pre-flight (per-episode guardrail flags the panel caught)\n"
      "- **Scapegoat (Lev 16 / Heb 9:12)** — Heb warrants the Atonement *sacrifice*; the *scapegoat-sent-away* type has weaker explicit NT warrant. Frame carefully or lead with the sacrifice.\n"
      "- **Markan miracles in a 'Signs' series** — Calming the Storm (Mk 4) / Paralytic (Mk 2) aren't Johannine *sēmeia*; don't force John's frame — let Mark's kingdom/authority reading drive (the series' own guardrail).\n"
      "- **Rich young ruler (Mk 10)** — the text exposes the idol of wealth; encounters' anti-moralism guardrail must still let the text land grace, not flatten it.\n"
      "- **Woman caught in adultery (Jn 8)** — note the textual-variant (pericope adulterae) honestly.\n"
      "- **Pierced / Zech 12:10 + 'My God forsaken'** — keep Father/Son distinction explicit so a 60s short can't be misheard as modalism.\n"
      "- Every narration still passes the enforced panel before lock — this list is the pre-flight, not a replacement.\n",
      "## 9. Single source of truth\n"
      "- **This plan (PRODUCTION_PLAN.md / PRODUCTION_TRACKER.html) is the master.** Regenerated by `_production_tracker.py` from series.json + the on-disk scan.\n"
      "- Sub-plans (binding): `BATCH_PLAN.md` (batched stages), `PRODUCER_ORCHESTRATOR_PLAN.md` (red-teamed → don't build the orchestrator yet; do long-form-generic first — DONE).\n"
      "- **Known limitation:** status is a curated overlay (`ST` dict) + a live asset scan, not a fully-automated register. Auto-discovery from disk is a future improvement.\n"]
for s in SERIES_JSON:
    sid = s["id"]
    md.append(f"\n## {s['name']}  ({sid} · {s.get('brand','')})\n*{s.get('concept','')}*\n> guardrail: {s.get('guardrails','')}\n")
    for l in [x for x in LONGS if x["series"] == sid]:
        md.append(f"- 🎬 **{l['title']}** <{l['ref']}> — _{l['stage']}_ {'(anchor)' if l['tier']==1 else '(flagship)'} {l['note']}")
    for sh in [x for x in SHORTS if x["series"] == sid]:
        sl = LONG_BY_ID.get(sh["support"], {})
        md.append(f"- 📱 {sh['title']} <{sh['ref']}> — _{sh['stage']}_ — backed by: {sl.get('title','?')} ({sl.get('stage','?')})"
                  + (f" — takes: {sh['takes']}" if sh.get('takes') else ""))
md.append("\n## Off-catalog existing work (not greenlit)\n" + "\n".join(f"- {t} <{r}> — {st} — {n}" for t, r, st, fo, n in OFFCAT))
md.append("\n## 10. Backlog — channel flagships to greenlight (proposed 'core gospel' buckets)\n"
          "A 'Jesus in the Bible' channel needs these core topics; NOT yet in series.json. Proposed as new buckets "
          "(core-incarnation / core-teaching / core-parables / core-passion / core-resurrection / core-sending / core-glory):\n"
          + "\n".join(f"- {'🎬 LONG' if k=='long' else '📱 short'}: {t} <{r}>  → bucket: {ps}" for t, r, k, ps in BACKLOG))
(ROOT / "PRODUCTION_PLAN.md").write_text("\n".join(md), encoding="utf-8")

print(f"[done] PRODUCTION_TRACKER.html + PRODUCTION_PLAN.md")
print(f"  {n_long} longs · {n_short} shorts · started {n_started} · cut+ {n_cut} · complete {n_complete}")
print(f"  shorts awaiting long: {len(awaiting)} · est metered to cut ~${cost_low}-{cost_high}")
