"""Build a single-page reference of every SKILL (panel_animator/ device
library + the core engine) and every STYLE (the 35-variant identity bake-off,
`_style_identity_bakeoff/style_manifest.json`) built for the living-sketchbook
series so far. $0, no API calls, no LLM -- just formats what already exists.

Styles come straight from style_manifest.json (35 entries) with their real
thumbnail from `_style_identity_bakeoff/stills/<id>.png`. Skills are the
verbatim one-line descriptions from this project's own skill registry
(.claude/skills/*), grouped by what kind of thing they act on.

Re-run any time style_manifest.json changes -- the SKILLS list below is
static (it mirrors the skill registry, which isn't machine-readable from
here) and needs a manual edit if a new panel_animator skill ships.

  .venv\\Scripts\\python.exe poc_living_sketchbook/_build_skills_styles_reference.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BAKEOFF = HERE / "_style_identity_bakeoff"
MANIFEST = BAKEOFF / "style_manifest.json"
OUT = HERE / "_SKILLS_AND_STYLES.html"

STATUS_ORDER = {"production_approved": 0, "caution": 1, "rejected": 2}
STATUS_LABEL = {"production_approved": "production approved", "caution": "caution", "rejected": "rejected"}

# ---------------------------------------------------------------- skills ----
# (name, slash-command, one-line description, category) -- descriptions are
# the verbatim summaries from this repo's own skill registry.
SKILLS = [
    # --- core engine ---
    ("Living Sketchbook", "/living-sketchbook",
     "The Awakeden SKETCH-REENACTMENT engine: tell a Bible story as 10-14 animated "
     "editorial-sketch spreads on aged paper, fast-paced, every spread genuinely moving, "
     "every episode landing on Jesus.", "Core engine"),

    # --- paper & light devices (act on the page, not the drawing) ---
    ("Tide-Mark", "/tide-mark",
     "A damp tide-line stain across the bottom band of a frame that rises and falls over "
     "time via a single height_frac parameter.", "Paper & light"),
    ("Wash-Creep", "/wash-creep",
     "A dark blue-grey watercolour wash advances or retreats along a fibrous, feathered "
     "front, the way ink spreads or dries back on damp cold-press paper.", "Paper & light"),
    ("Damp Cockle", "/damp-cockle",
     "A spatially-varying paper warp (low-frequency displacement + raking-light shading) "
     "so the sheet reads as damp, waving, buckling paper rather than a rigid computer wobble.", "Paper & light"),
    ("Set-Off", "/set-off",
     "A faint, mirrored, absorbed impression of an earlier hand-scribed verse card bleeding "
     "through onto the blank upper page of a landing spread.", "Paper & light"),
    ("Still-Water Mirror", "/still-water-mirror",
     "A deterministic reflection for calm-water stills -- mirrors a narrow band above the "
     "horizon and ripples it, fail-closed against reflecting a standing figure.", "Paper & light"),
    ("Blue-Line", "/blue-line",
     "A spread opens as pale non-photo-blue underdrawing, then the ink arrives once along a "
     "hand-wobbled diagonal front and the page is finished for good.", "Paper & light"),
    ("Raking Light", "/raking-light",
     "A broad, slow directional grazing sweep that catches paper tooth and deepens "
     "torn-edge shadow, flaring the gold-leaf strip once as it crosses it.", "Paper & light"),
    ("Held Breath", "/held-breath",
     "Reads a narration's real silences into an energy(t) envelope that every other "
     "paper-layer device multiplies its own amplitude by.", "Paper & light"),
    ("Candle-Only", "/candle-only",
     "A radial light budget (warm gain inside a moving radius, cold-dark falloff outside "
     "it) anchored to a drawn light source already in the art.", "Paper & light"),

    # --- reveal, camera & transition devices ---
    ("Page Transitions (Torn-Out Page)", "/page-transitions",
     "The Keeper grabs, lifts, and rips a page out of the book on camera, revealing the "
     "next page already waiting beneath.", "Reveal & camera"),
    ("Lift-Away", "/lift-away",
     "A calm page-turn transition (Round 9 build) for moving between spreads without a hard cut.", "Reveal & camera"),
    ("Insert-Page Camera", "(programmatic -- panel_animator/insert_page_camera.py)",
     "A deterministic $0 reading-order pan/push/pull camera over ONE static baked-lettering "
     "insert page -- never generative motion, which would garble baked text.", "Reveal & camera"),
    ("Grid Choreography", "/grid-choreography",
     "A virtual page camera over a live multi-panel grid -- racks focus toward whichever "
     "panel currently holds attention, dimming the other three.", "Reveal & camera"),
    ("Parallax Panel", "/parallax-panel",
     "A 2.5D parallax-depth clip from a single rendered still -- the nearest salient "
     "subject drifts at a different rate than the base plate for real depth.", "Reveal & camera"),
    ("Line-Boil", "/line-boil",
     "A subtle, smooth per-frame wobble of micro translate/rotate so a clip reads as "
     "hand-inked frame-by-frame animation instead of a computer-locked render.", "Reveal & camera"),
    ("Ink Transition", "/ink-transition",
     "A hand-bleed or brush-wipe transition between two clips/stills using an organic "
     "noise-field reveal edge, not a generic crossfade or hard cut.", "Reveal & camera"),

    # --- lettering & data devices ---
    ("Marginalia", "/marginalia",
     "A real, chosen, hand-lettered field-note caption + a wobbled leader line pointing at "
     "a detail already in an already-rendered still.", "Lettering & data"),
    ("Typography Panel", "/typography-panel",
     "An in-world kinetic-type comic-grid panel -- torn ink caption band, punchy spring "
     "pop-in, optional honest ticking-counter.", "Lettering & data"),
    ("Infographic Panel", "/infographic-panel",
     "A genuine two-still comic diptych (torn ink gutter, hand-drawn brush arrow, punchy "
     "reveals) showing a cause/effect or before/after relationship.", "Lettering & data"),
    ("Measuring Reed", "/measuring-reed",
     "A hand-ruled measured span draws itself across the page whenever Scripture states an "
     "actual physical magnitude verbatim.", "Lettering & data"),
    ("Tally", "/tally",
     "An exact-count device for scripture-stated counts that can't be trusted to the "
     "generative page, only to code.", "Lettering & data"),

    # --- marginalia / hand devices ---
    ("Keeper's Hand", "/keeper-hand",
     "One authored energy number (0 calm .. 1 panic) drives a human hand's jitter/heave/"
     "lean/pressure writing into the sketchbook margin.", "Hand & margin"),
    ("Margin Study", "/margin-study",
     "1-3 quick graphite pencil studies swept-reveal from a diagonal front, derived only "
     "from the spread's own already-rendered art.", "Hand & margin"),
    ("Annotator's Circle", "/annotators-circle",
     "A hand-drawn ink ellipse that draws itself, in two passes, around ONE word the "
     "instant the narrator speaks it.", "Hand & margin"),
    ("Bleeding Word", "/bleeding-word",
     "One drop lands on a Keeper-hand word's own ink and blooms -- radial wet darkening + "
     "edge dissolve + descending trails.", "Hand & margin"),
    ("Elder Leaf", "/elder-leaf",
     "The episode's Old-Testament echo arriving as a visibly OLDER leaf (foxed, deckled, "
     "linen-taped) carrying the OT verse in an elder register of Scribed Ink.", "Hand & margin"),
    ("Frottage", "/frottage",
     "An object still (coin, seal, inscription) emerges as a graphite rubbing under "
     "diagonal strokes that accumulate in real hand order.", "Hand & margin"),
    ("Papermaker's Mark", "/papermakers-mark",
     "A wire-form watermark pressed into the paper, invisible at rest, appearing only while "
     "raking-light's sweep crosses it.", "Hand & margin"),
    ("Ribbon Marker", "/ribbon-marker",
     "A narrow rubric-red ribbon that slips down and settles across the landing spread's "
     "margin lane, then holds byte-identical stillness.", "Hand & margin"),

    # --- impact & polish ---
    ("Impact Burst", "/impact-burst",
     "A hand-drawn ink impact burst (jagged star + speed lines) composited onto a clip at "
     "an exact SFX-hit timestamp.", "Impact & polish"),
    ("Print Grade", "/print-grade",
     "A halftone + print-texture grade pass (dot screen, CMYK misregistration, film grain) "
     "-- the difference between a nice illustration and a printed comic.", "Impact & polish"),

    # --- sound ---
    ("Scriptorium Foley", "/scriptorium-foley",
     "Gives each paper/lettering device's known schedule a matching diegetic sound from "
     "the sound library, ambience-level, sidechain-ducked.", "Sound"),

    # --- QC ---
    ("Margin Sentinel", "(QC tool, not a slash skill)",
     "Watches every pixel that was blank paper margin in frame 0 of a raw animated clip and "
     "flags anything that grows in and never leaves.", "QC"),
]

CSS = """
  body { background:#16181d; color:#e8e4d8; font-family:Georgia, serif; line-height:1.5; padding:28px 18px 100px; }
  .wrap { max-width:1500px; margin:0 auto; }
  h1 { color:#e9c877; font-size:1.9rem; margin-bottom:6px; }
  h2 { color:#e9c877; font-size:1.3rem; margin:44px 0 6px; border-bottom:1px solid #333; padding-bottom:8px; }
  h3.cat { color:#c9b98a; font-size:1.02rem; margin:26px 0 10px; text-transform:uppercase; letter-spacing:.04em; }
  .sub { color:#9aa0ad; margin-bottom:10px; font-size:14px; max-width:100ch; }
  .bar { background:#1e2129; border:1px solid #333; border-radius:8px; padding:10px 16px; margin:14px 0 8px; font-size:14px; }
  .bar b { color:#e9c877; }
  .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }
  .skillgrid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:12px; }
  .card { background:#1e2129; border-radius:8px; overflow:hidden; border:2px solid #333; }
  .card.production_approved { border-color:#3a4a3a; }
  .card.caution { border-color:#8a7a2a; }
  .card.rejected { border-color:#6a2a2a; }
  .card img { width:100%; display:block; background:#000; aspect-ratio:16/9; object-fit:cover; }
  .cap { padding:10px 12px; font-size:.82rem; color:#c9c4b6; }
  .cap b { color:#e8e4d8; display:block; font-size:.9rem; }
  .tags { margin:6px 0; }
  .tag { display:inline-block; background:#2a2d36; color:#9aa0ad; font-size:.68rem; padding:2px 6px; border-radius:3px; margin:2px 3px 0 0; }
  .status { display:inline-block; font-size:.7rem; padding:2px 7px; border-radius:4px; margin-top:6px; }
  .status.production_approved { background:#2a3a2a; color:#9fd39f; }
  .status.caution { background:#3a3320; color:#e9c877; }
  .status.rejected { background:#3a2a2a; color:#d99f9f; }
  .skillcard { background:#1e2129; border:1px solid #333; border-radius:8px; padding:12px 14px; }
  .skillcard b { color:#e9c877; }
  .skillcard .cmd { color:#7fa8c9; font-size:.78rem; display:block; margin:2px 0 6px; }
  .skillcard p { color:#c9c4b6; font-size:.85rem; margin:0; }
"""


def style_cards():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = sorted(manifest.values(), key=lambda e: (STATUS_ORDER.get(e["status"], 9), e["id"]))
    counts = {"production_approved": 0, "caution": 0, "rejected": 0}
    cards = []
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        img = BAKEOFF / "stills" / f"{e['id']}.png"
        img_tag = f'<img src="_style_identity_bakeoff/stills/{e["id"]}.png" loading="lazy">' if img.exists() else ""
        tags = "".join(f'<span class="tag">{t}</span>' for t in e.get("beat_signal", []))
        note = e["scores"].get("moses", {}).get("note", "")
        gold_flag = " ⚠️ gold-leaf conflict" if e.get("gold_leaf_conflict") else ""
        clean_name = e["name"].split(" ⚠")[0]
        cards.append(f"""<div class="card {e['status']}">{img_tag}
  <div class="cap"><b>{clean_name}</b>{e['id']} &middot; {e['family']}{gold_flag}
  <div class="tags">{tags}</div>
  {note}
  <div><span class="status {e['status']}">{STATUS_LABEL[e['status']]}</span></div></div></div>""")
    return cards, counts, len(entries)


def skill_cards():
    by_cat = {}
    for name, cmd, desc, cat in SKILLS:
        by_cat.setdefault(cat, []).append((name, cmd, desc))
    blocks = []
    for cat, items in by_cat.items():
        cards = "".join(
            f'<div class="skillcard"><b>{name}</b><span class="cmd">{cmd}</span><p>{desc}</p></div>'
            for name, cmd, desc in items
        )
        blocks.append(f'<h3 class="cat">{cat}</h3><div class="skillgrid">{cards}</div>')
    return "".join(blocks), sum(len(v) for v in by_cat.values())


def build():
    s_cards, s_counts, s_total = style_cards()
    skill_html, skill_total = skill_cards()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Living-Sketchbook — skills &amp; styles reference</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>LIVING-SKETCHBOOK — everything built so far</h1>
<div class="sub">A reference catalogue, not a narrative piece: every panel_animator device skill
(the "paper-layer" engines built across the round 5/6/7/8/9 design sessions) and every rendering
style from the 35-variant identity bake-off (Moses/Jesus identity-locked, scored for
"handmade/alive"). Skills are used selectively, one or two per episode, deliberately picked for
the beat they serve — not stacked everywhere just because they exist.</div>

<h2>Styles — {s_total} rendering-technique variants</h2>
<div class="bar"><b>{s_counts.get('production_approved',0)}</b> production approved &nbsp;·&nbsp;
<b>{s_counts.get('caution',0)}</b> caution (weak on portrait / unreliable) &nbsp;·&nbsp;
<b>{s_counts.get('rejected',0)}</b> rejected</div>
<div class="grid">
{chr(10).join(s_cards)}
</div>

<h2>Skills — {skill_total} panel-animator devices + the core engine</h2>
{skill_html}

</div>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"[ok] {s_total} styles + {skill_total} skills -> {OUT}")


if __name__ == "__main__":
    build()
