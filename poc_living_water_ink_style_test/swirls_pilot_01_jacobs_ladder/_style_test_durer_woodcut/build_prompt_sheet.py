"""Builds _PROMPT_SHEET.html — every still + animation prompt + required refs
for the "book" plan (2 full-woodcut hero bookends + 8 hybrid interior pages),
so the user can generate the stills externally (Nano Banana Pro / Gemini
Flash image) and animate them, then hand the finished clips back for
assembly.

Reuses REAL locked content everywhere — the hybrid still prompts come from
render_hybrid_all.py's build_prompt() (same function used to render the
actual test stills), the hybrid animation prompts come straight from
swirls_page.assemble_animation_prompt() (the same function the base pilot
uses), and the hero prompts are copied verbatim from render_hero_open.py /
render_test.py. Nothing here is retyped by hand.

Run:
  .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\swirls_pilot_01_jacobs_ladder\\_style_test_durer_woodcut\\build_prompt_sheet.py
"""
from __future__ import annotations

import html
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PILOT_DIR = HERE.parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, str(PILOT_DIR))
sys.path.insert(0, str(PILOT_DIR.parent / "test_the_cross"))
import render_jacobs_ladder as jl  # noqa: E402
from swirls_page import assemble_animation_prompt  # noqa: E402

# loaded by explicit path -- both this dir and test_the_cross/ have a
# same-named render_test.py, so sys.path-based import is ambiguous here.
hy = load("hy_hybrid_all", HERE / "render_hybrid_all.py")
hero_open = load("hy_hero_open", HERE / "render_hero_open.py")
hero_close = load("hy_hero_close", HERE / "render_test.py")

OUT = HERE / "_PROMPT_SHEET.html"

PAGE_IDS = ["f01", "f02", "f03", "f04", "f05", "f06", "f07", "f08"]


def e(s: str) -> str:
    return html.escape(s)


def ref_thumbs(refs) -> str:
    if not refs:
        return '<div class="noref">no reference images — this page establishes Jacob\'s look</div>'
    items = []
    for r in refs:
        fname = Path(r.path).name
        items.append(
            f'<div class="ref"><img src="../refs/{e(fname)}"><div class="refname">{e(fname)}</div>'
            f'<div class="refdesc">{e(r.subject)}</div></div>'
        )
    return '<div class="refs">' + "".join(items) + '</div>'


_ta_counter = [0]


def ta_block(title: str, text: str, rows: int = 8) -> str:
    _ta_counter[0] += 1
    tid = f"ta{_ta_counter[0]}"
    return (
        f'<div class="section-title">{e(title)}'
        f'<button class="copybtn" onclick="copyTa(\'{tid}\', this)">Copy</button></div>'
        f'<textarea id="{tid}" readonly rows="{rows}">{e(text)}</textarea>'
    )


def card(label: str, title: str, still_prompt: str, refs_html: str, anim_prompt: str,
         note: str = "") -> str:
    note_html = f'<div class="note">{e(note)}</div>' if note else ""
    return f"""
<div class="card">
  <div class="cardhead"><span class="label">{e(label)}</span><span class="title">{e(title)}</span></div>
  {note_html}
  {ta_block("Still prompt (Nano Banana Pro / Gemini image)", still_prompt)}
  <div class="section-title">Reference images to attach</div>
  {refs_html}
  {ta_block("Animation prompt (for whichever video model you use)", anim_prompt)}
</div>"""


REF_SHEET_STYLE = (
    "Delicate hand-drawn ink linework and soft watercolor wash on aged cream paper with "
    "visible grain, fine quick cross-hatching, in the style of a found piece of animation "
    "development art — a plain reference-sheet study, NOT a scene: no background setting, no "
    "other figures or objects, no title, no frame number, no handwritten notes, no text or "
    "labels of any kind. Not photorealistic, not anime, no polished graphic design, no clean "
    "comic-book inking."
)


def ref_gen_card(label: str, title: str, prompt: str) -> str:
    return f"""
<div class="card">
  <div class="cardhead"><span class="label">{e(label)}</span><span class="title">{e(title)}</span></div>
  {ta_block("Reference-sheet prompt (generate this FIRST, before any still)", prompt, rows=6)}
</div>"""


def build_ref_gen_cards() -> str:
    jacob_build = jl._JACOB_BUILD
    parts = [
        ref_gen_card(
            "REF — JACOB (full figure)", "jacob_ref.png",
            f"A single reference illustration of one Biblical-era young man, full figure, "
            f"standing in a simple relaxed three-quarter pose against a plain, softly textured "
            f"cream paper background. He is {jacob_build}. He holds nothing in his hands, "
            f"arms resting naturally at his sides. {REF_SHEET_STYLE}"
        ),
        ref_gen_card(
            "REF — JACOB (face close-up)", "jacob_face_ref.png",
            f"A close-up reference illustration of one Biblical-era young man's face and head "
            f"only, three-quarter angle, against a plain, softly textured cream paper "
            f"background — no body below the shoulders. He is {jacob_build}. Focus on his face, "
            f"hair, and the exact faint shadow of his sparse young beard. {REF_SHEET_STYLE}"
        ),
        ref_gen_card(
            "REF — THE STONE", "stone_ref.png",
            "A single reference illustration of one rough, uncut field stone — a tan-brown "
            "boulder with a naturally flattened top, the same single stone that will recur on "
            "every page — sitting alone against a plain, softly textured cream paper "
            f"background. {REF_SHEET_STYLE}"
        ),
        ref_gen_card(
            "REF — THE STAFF", "staff_ref.png",
            "A single reference illustration of one plain straight wooden traveler's staff, "
            "with no hook, crook, or knob at either end, resting diagonally against a plain, "
            f"softly textured cream paper background. {REF_SHEET_STYLE}"
        ),
        ref_gen_card(
            "REF — THE LADDER", "ladder_ref.png",
            "A single reference illustration of one great ladder of plain weathered wood — two "
            "straight rails and flat rungs — shown as a close study of its lowest section "
            "standing on bare ground, against a plain, softly textured cream paper background. "
            f"{REF_SHEET_STYLE}"
        ),
        ref_gen_card(
            "REF — THE PLACE", "bethel_ref.png",
            "A single reference illustration of bare, stony, red-brown hill country — low "
            "rolling hills on the horizon, sparse dry grass and small stones scattered across "
            "open ground, no meadow, no hedges, no trees, no figures. A location/terrain "
            f"study. {REF_SHEET_STYLE}"
        ),
    ]
    return "\n".join(parts)


def main() -> None:
    cards = []

    # ---- Reference images (generate these FIRST) ---------------------------
    ref_gen_cards = build_ref_gen_cards()

    # ---- Hero bookends -----------------------------------------------------
    open_refs_html = ref_thumbs_from_paths(hero_open.REF_IMAGES, [
        "Jacob, full figure — face, hair, beard, dress, build",
        "Jacob's staff — plain straight wooden pole, no crook",
        "The place — bare stony hill country, low hills, no meadow",
    ])
    open_anim = (
        "Stationary camera, locked wide static shot, no pan, no zoom. Jacob continues his "
        "slow, weary walk forward along the ground, one heavy step after another at the same "
        "tired, even pace for the whole clip, his head staying low, his staff swinging gently "
        "with his stride; his mantle stirs faintly in the evening wind; the dusk light stays "
        "exactly as warm and dim as it already is, unchanged for the whole clip; the distant "
        "tents stay exactly as drawn; no new figure, mark, or text appears anywhere on the "
        "frame at any point."
    )
    cards.append(card(
        "HERO — OPEN", "F01 opening bookend, full woodcut (no panels)",
        hero_open.PROMPT, open_refs_html, open_anim,
        note="Book opens here, wordless. Mirrors the closing hero below — same framing, opposite light/posture."
    ))

    close_refs_html = ref_thumbs_from_paths(hero_close.REF_IMAGES, [
        "Jacob, full figure — face, hair, beard, dress, build",
        "Jacob's staff — plain straight wooden pole, no crook",
        "The place — bare stony hill country, low hills, no meadow",
    ])
    close_anim = (
        "Stationary camera, locked wide static shot, no pan, no zoom. Jacob stands still, "
        "facing the dawn horizon, only his mantle and the hem of his robe stirring gently in "
        "the morning wind; his staff stays upright and still in his hand; the dawn light stays "
        "exactly as it already is, unchanged for the whole clip; no new figure, mark, or text "
        "appears anywhere on the frame at any point."
    )
    cards.append(card(
        "HERO — CLOSE", "F08 closing bookend, full woodcut (no panels)",
        hero_close.PROMPT, close_refs_html, close_anim,
        note="Book closes here, wordless. Already rendered once as f08_durer_woodcut_test.png."
    ))

    # ---- Hybrid interior pages ----------------------------------------------
    for pid in PAGE_IDS:
        spec = jl.PAGES[pid]
        still_prompt = hy.build_prompt(spec)
        anim_prompt = assemble_animation_prompt(spec)
        refs_html = ref_thumbs(spec.refs)
        cards.append(card(
            pid.upper(), f'"{spec.caption_lines[0]}"', still_prompt, refs_html, anim_prompt,
        ))

    body = "\n".join(cards)
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Ladder — Book Plan Prompt Sheet</title>
<style>
  :root {{ --bg:#14131a; --card:#1e1c26; --ink:#ece7f5; --muted:#928da3; --accent:#8fb4e3; --gold:#d7b45a; --good:#8fd18f; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:40px 24px 100px; background:var(--bg); color:var(--ink); font-family:Georgia,'Iowan Old Style',serif; }}
  header {{ max-width:1000px; margin:0 auto 32px; text-align:center; }}
  header h1 {{ font-size:1.8rem; margin:0 0 8px; }}
  header p {{ color:var(--muted); margin:4px 0; font-size:.95rem; max-width:800px; margin-left:auto; margin-right:auto; line-height:1.5; }}
  h2.section-heading {{ max-width:1000px; margin:44px auto 18px; color:var(--gold); font-size:1.2rem; letter-spacing:.03em; border-bottom:1px solid #33303e; padding-bottom:8px; }}
  .card {{ max-width:1000px; margin:0 auto 28px; background:var(--card); border:1px solid #33303e; border-radius:10px; padding:20px 24px; }}
  .cardhead {{ display:flex; align-items:center; gap:12px; margin-bottom:6px; }}
  .label {{ display:inline-block; background:var(--gold); color:#14131a; font-weight:bold; font-size:.75rem; letter-spacing:.06em; padding:3px 10px; border-radius:4px; }}
  .title {{ font-size:1.1rem; font-weight:bold; }}
  .note {{ color:var(--accent); font-size:.85rem; margin-bottom:10px; font-style:italic; }}
  .section-title {{ display:flex; align-items:center; justify-content:space-between; font-size:.75rem; letter-spacing:.06em; text-transform:uppercase; color:var(--gold); margin:14px 0 6px; }}
  .copybtn {{ font-family:Georgia,serif; font-size:.72rem; letter-spacing:normal; text-transform:none; background:#2c2938; color:var(--accent); border:1px solid #3a3648; border-radius:5px; padding:3px 10px; cursor:pointer; }}
  .copybtn:hover {{ background:#3a3648; }}
  .copybtn.copied {{ background:var(--good); color:#14131a; border-color:var(--good); }}
  textarea {{ width:100%; background:#100f15; color:var(--ink); border:1px solid #3a3648; border-radius:6px; padding:10px; font-family:Georgia,serif; font-size:.88rem; line-height:1.5; resize:vertical; }}
  .refs {{ display:flex; gap:14px; flex-wrap:wrap; }}
  .ref {{ width:120px; text-align:center; font-size:.72rem; color:var(--muted); }}
  .ref img {{ width:100%; border-radius:5px; border:1px solid #3a3648; background:#fff; margin-bottom:4px; }}
  .refname {{ color:var(--ink); font-weight:bold; word-break:break-all; }}
  .refdesc {{ margin-top:2px; }}
  .noref {{ color:var(--muted); font-size:.85rem; font-style:italic; }}
</style>
</head>
<body>
<header>
  <h1>The Ladder — Book Plan Prompt Sheet</h1>
  <p>Everything needed for a fresh project: reference-sheet prompts first, then every still +
  animation prompt for the "book" plan (2 full-woodcut hero bookends, open/close, wordless + 8
  hybrid interior pages — woodcut-cinematic panels, locked ink-wash main scene). Generate the 6
  reference images first, then use them as image references for every still below. Generate
  stills, animate them with whatever tool, then hand the finished clips back for assembly.</p>
</header>

<h2 class="section-heading">Step 0 — Reference images (generate these first)</h2>
{ref_gen_cards}

<h2 class="section-heading">Step 1 — Hero bookends + hybrid interior pages</h2>
{body}

<script>
function copyTa(id, btn) {{
  var ta = document.getElementById(id);
  ta.select();
  ta.setSelectionRange(0, 999999);
  navigator.clipboard.writeText(ta.value).then(function() {{
    var orig = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {{ btn.textContent = orig; btn.classList.remove('copied'); }}, 1500);
  }}).catch(function() {{
    document.execCommand('copy');
  }});
}}
</script>
</body>
</html>
"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(f"-> {OUT}")


def ref_thumbs_from_paths(paths, descs) -> str:
    items = []
    for p, d in zip(paths, descs):
        fname = Path(p).name
        items.append(
            f'<div class="ref"><img src="../refs/{e(fname)}"><div class="refname">{e(fname)}</div>'
            f'<div class="refdesc">{e(d)}</div></div>'
        )
    return '<div class="refs">' + "".join(items) + '</div>'


if __name__ == "__main__":
    main()
