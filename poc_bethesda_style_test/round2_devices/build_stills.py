"""THROWAWAY POC — NOT part of the production pipeline.

Generates 3 stills x 5 structural-device concepts (Fable's round 2 brief) —
"The Closed File", "The Sounding Line", "The Registration Pull",
"The Double-Entry Page", "The One-Take Scroll" — each matched to a real
locked narration. Same mechanics as poc_bethesda_style_test/build_stills.py.
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
OUT_DIR = Path(__file__).resolve().parent / "stills"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# No legible text anywhere -- this project's own locked rule (T1): the Word/text
# is conveyed by gesture or abstract mark, never AI-rendered lettering. Real
# captions/entries get added afterward by code (Scribed Ink), never by the model.
GUARDRAIL = (
    ", absolutely no legible text, no legible lettering, no readable words or "
    "numerals anywhere in the image -- any writing-like marks must read as "
    "abstract ink texture or blank/illegible surface only, no visible text or "
    "captions, no modern objects or clothing, reverent and dignified tone, "
    "ancient Near-Eastern or period-appropriate setting only, no gore, no nsfw"
)

STILLS = [
    # ---------------- 1: THE CLOSED FILE (Matt 16:13-17) ----------------
    {
        "concept": "closed_file", "label": "The Closed File", "id": "01",
        "beat": "Hook — the drawer, rank after rank of closed cards",
        "model": "nano_banana_pro",
        "prompt": (
            "Antiquarian museum archive illustration, ink and muted wash on aged card stock, "
            "warm low lamplight, meticulous cross-hatched linework, restrained scholarly palette "
            "of sepia, slate and faded ochre, like a 19th-century accession-catalogue engraving. "
            "A wide view into an open wooden card-catalogue drawer, dozens of tabbed index cards "
            "standing upright in tight ranks, each card aged and closed shut, a small hand-drawn "
            "portrait bust silhouette faintly visible on the edge of each tab, dust motes in the "
            "lamplight. Dense, orderly, slightly oppressive rows of finished, filed things."
            + GUARDRAIL
        ),
    },
    {
        "concept": "closed_file", "label": "The Closed File", "id": "02",
        "beat": "The one loose card, unfiled, on the desk",
        "model": "nano_banana_pro",
        "prompt": (
            "Antiquarian museum archive illustration, ink and muted wash on aged card stock, "
            "warm low lamplight, meticulous cross-hatched linework, restrained scholarly palette "
            "of sepia, slate and faded ochre, like a 19th-century accession-catalogue engraving. "
            "A close view of a wooden desk blotter beside the open card drawer: one single index "
            "card lies flat and alone on the desk, apart from the filed ranks behind it, its lower "
            "portion blank and unfiled. A small unfinished ink portrait study of a calm bearded "
            "man's face occupies the card's upper half, rendered with only a few confident lines, "
            "not fully resolved. A dip pen and open inkwell rest beside it."
            + GUARDRAIL
        ),
    },
    {
        "concept": "closed_file", "label": "The Closed File", "id": "03",
        "beat": "Landing — the portrait turns, meets your eyes",
        "model": "nano_banana_pro",
        "prompt": (
            "Antiquarian museum archive illustration, ink and muted wash on aged card stock, "
            "warm low lamplight, meticulous cross-hatched linework, restrained scholarly palette "
            "of sepia, slate and faded ochre, like a 19th-century accession-catalogue engraving. "
            "An extreme close-up on a single index card: a simple, dignified ink line-drawn "
            "portrait of a calm bearded man's face, three-quarter turned toward the viewer, eyes "
            "meeting the viewer directly, both eyes level and calm not staring, warm lamplight "
            "catching one side of the drawn face. The card's lower portion is bare aged paper, "
            "no other cards visible, deep soft shadow surrounding the single card."
            + GUARDRAIL
        ),
    },

    # ---------------- 2: THE SOUNDING LINE (Jonah 1:17 / Matt 12:40) ----------------
    {
        "concept": "sounding_line", "label": "The Sounding Line", "id": "01",
        "beat": "Hook — the cutaway, ship to the depths",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed 19th-century scientific cross-section engraving, cutaway diagram style, "
            "muted mineral ink-wash palette of slate blue-grey and faded sienna, fine technical "
            "linework, aged parchment ground, restrained and scholarly like a naturalist's survey "
            "plate. A tall vertical cross-section: a small wooden sailing ship cut away at the "
            "waterline near the top of the frame, layered dark water descending beneath it in "
            "horizontal bands growing darker with depth, a single ruled fathom-line with small "
            "tick marks descending through the water column. Restrained, measured, scientific."
            + GUARDRAIL
        ),
    },
    {
        "concept": "sounding_line", "label": "The Sounding Line", "id": "02",
        "beat": "The datum line — belly and tomb at the same depth",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed 19th-century scientific cross-section engraving, cutaway diagram style, "
            "muted mineral ink-wash palette of slate blue-grey and faded sienna, fine technical "
            "linework, aged parchment ground, restrained and scholarly like a naturalist's survey "
            "plate. A wide cross-section at depth: on one side, a great fish shown in anatomical "
            "cutaway with a small robed man curled peacefully inside its belly cavity; on the other "
            "side of the same plate, a rock-cut tomb chamber cutaway at the identical measured "
            "depth, a shrouded form on a stone ledge within. One horizontal ruled datum line with "
            "fathom tick marks connects the fish cutaway to the tomb cutaway across the plate."
            + GUARDRAIL
        ),
    },
    {
        "concept": "sounding_line", "label": "The Sounding Line", "id": "03",
        "beat": "Landing — the tomb cutaway, empty and lit",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed 19th-century scientific cross-section engraving, cutaway diagram style, "
            "muted mineral ink-wash palette of slate blue-grey and faded sienna, fine technical "
            "linework, aged parchment ground, restrained and scholarly like a naturalist's survey "
            "plate. A close cutaway view of a rock-cut tomb chamber: the round stone rolled aside "
            "from the entrance, soft light spilling into the chamber from outside, an empty folded "
            "linen shroud resting undisturbed on the stone ledge within, no figure present. Quiet, "
            "resolved, the same restrained cross-section technical style as the rest of the plate."
            + GUARDRAIL
        ),
    },

    # ---------------- 3: THE REGISTRATION PULL (Psalm 22) ----------------
    {
        "concept": "registration_pull", "label": "The Registration Pull", "id": "01",
        "beat": "The psalm leaf — David's own margin vignettes",
        "model": "nano_banana_pro",
        "prompt": (
            "Illuminated manuscript page illustration, aged vellum ground, fine ink linework with "
            "muted gold and umber wash, restrained devotional palette, like a medieval psalter "
            "leaf. A single manuscript page bordered by three small soft-edged margin vignettes "
            "fading into the page's edges: pierced open hands, a cluster of mocking robed figures "
            "gesturing, a folded garment beside a scatter of small carved lots. The page's central "
            "area is bare aged vellum with no legible script, only faint horizontal ruling lines "
            "where text would sit. Quiet, ancient, devotional."
            + GUARDRAIL
        ),
    },
    {
        "concept": "registration_pull", "label": "The Registration Pull", "id": "02",
        "beat": "The vellum overlay settles, registration marks click in",
        "model": "nano_banana_pro",
        "prompt": (
            "Illuminated manuscript page illustration layered beneath a translucent vellum "
            "overlay sheet, aged vellum ground, fine ink linework with muted gold and umber wash, "
            "restrained devotional palette. A manuscript page seen through a slightly offset "
            "translucent vellum sheet lying over it: the vellum carries its own faint ink vignette "
            "of a crucified figure's pierced hand and a small mocking-crowd sketch, positioned so "
            "they nearly overlap the psalm page's own vignettes beneath. Two small fine cross-mark "
            "registration symbols are visible at the upper corners where the layers align, thin "
            "and precise, like a printmaker's proof sheet."
            + GUARDRAIL
        ),
    },
    {
        "concept": "registration_pull", "label": "The Registration Pull", "id": "03",
        "beat": "Close on one match point — the lots, aligned",
        "model": "nano_banana_pro",
        "prompt": (
            "Illuminated manuscript page illustration layered beneath a translucent vellum "
            "overlay sheet, aged vellum ground, fine ink linework with muted gold and umber wash, "
            "restrained devotional palette, like a printmaker's registration proof. An extreme "
            "close-up on one single match point: a small ink vignette of scattered carved lots and "
            "a folded garment on the lower vellum layer, with a near-identical vignette of Roman "
            "soldiers' dice on the upper translucent vellum sheet, the two vignettes precisely "
            "aligned one over the other, a small fine cross-mark registration symbol glowing "
            "faintly at the exact point of overlap."
            + GUARDRAIL
        ),
    },

    # ---------------- 4: THE DOUBLE-ENTRY PAGE (Isaiah 53:5) ----------------
    {
        "concept": "double_entry", "label": "The Double-Entry Page", "id": "01",
        "beat": "The empty ledger, two ruled columns",
        "model": "nano_banana_pro",
        "prompt": (
            "Scribe's ledger page illustration, aged cream paper, fine hand-ruled ink lines, "
            "restrained sepia and rubric-red palette, like an old accounting book's opening page. "
            "A wide view of a ruled ledger spread divided into two columns by one strong vertical "
            "center rule, each column further divided by faint horizontal ruling lines. The page "
            "is almost entirely bare and unfilled -- no legible entries yet, only the empty ruled "
            "grid itself, quiet and expectant, warm aged paper texture, gentle raking light "
            "crossing the page."
            + GUARDRAIL
        ),
    },
    {
        "concept": "double_entry", "label": "The Double-Entry Page", "id": "02",
        "beat": "Entries and vignettes arrive, transfer lines cross the gutter",
        "model": "nano_banana_pro",
        "prompt": (
            "Scribe's ledger page illustration, aged cream paper, fine hand-ruled ink lines, "
            "restrained sepia and rubric-red palette, like an old accounting book mid-use. A ruled "
            "two-column ledger page, each column now holding several small soft-edged ink "
            "vignettes in its ruled rows -- one column's vignettes suggest wounds and a crown of "
            "thorns, the facing column's vignettes suggest ordinary anonymous figures bowed under "
            "unseen weight. Two or three fine curved red ink lines cross the center gutter, each "
            "connecting one vignette on the left to one vignette on the right."
            + GUARDRAIL
        ),
    },
    {
        "concept": "double_entry", "label": "The Double-Entry Page", "id": "03",
        "beat": "Landing — the ruling resolves into a cross",
        "model": "nano_banana_pro",
        "prompt": (
            "Scribe's ledger page illustration, aged cream paper, fine hand-ruled ink lines, "
            "restrained sepia and rubric-red palette, like an old accounting book's closing page. "
            "A wide view of a completed ruled ledger page: the strong vertical center rule and a "
            "strong horizontal rule near the bottom of the page intersect, and several fine red "
            "ink transfer lines from both columns all converge and terminate at that intersection, "
            "so the ruled lines and the red lines together visually resolve into the clear shape "
            "of a plain cross. A double rule is drawn beneath, like a closed account. Quiet, "
            "resolved, still."
            + GUARDRAIL
        ),
    },

    # ---------------- 5: THE ONE-TAKE SCROLL (Acts 8) ----------------
    {
        "concept": "one_take_scroll", "label": "The One-Take Scroll", "id": "01",
        "beat": "Hook — the scroll unrolling, the frieze below",
        "model": "nano_banana_pro",
        "prompt": (
            "Ancient scroll illustration, aged papyrus-toned ground, fine sepia ink linework, "
            "restrained scholarly palette, like a photographed museum scroll fragment. A long "
            "horizontal ancient scroll partially unrolled, its surface covered in dense abstract "
            "vertical texture suggesting columns of ancient script but with no legible letterforms "
            "at all -- pure abstract ink texture only. Along the scroll's bottom margin runs a "
            "thin continuous ink frieze: a small two-wheeled chariot with two robed figures, drawn "
            "in a simple ancient frieze style, mid-journey along a dusty road."
            + GUARDRAIL
        ),
    },
    {
        "concept": "one_take_scroll", "label": "The One-Take Scroll", "id": "02",
        "beat": "The halt — Philip enters the frieze",
        "model": "nano_banana_pro",
        "prompt": (
            "Ancient scroll illustration, aged papyrus-toned ground, fine sepia ink linework, "
            "restrained scholarly palette, like a photographed museum scroll fragment. A close "
            "view of the scroll's bottom-margin frieze: the small chariot has come to a halt, one "
            "seated robed figure inside it gesturing outward as if mid-question, a second robed "
            "figure approaching on foot from the roadside, mid-stride, about to meet the chariot. "
            "Above the frieze, the scroll's script-texture columns are abstract ink marks only, "
            "no legible letterforms, dense and even."
            + GUARDRAIL
        ),
    },
    {
        "concept": "one_take_scroll", "label": "The One-Take Scroll", "id": "03",
        "beat": "Landing — the scroll runs past its own text into image",
        "model": "nano_banana_pro",
        "prompt": (
            "Ancient scroll illustration transitioning into painted image, aged papyrus-toned "
            "ground on the left dissolving into a soft painted devotional scene on the right, fine "
            "sepia ink linework giving way to gentle wash colour, restrained and reverent. The "
            "left portion of the frame still carries the scroll's abstract script-texture columns "
            "(no legible letters), which thin out and dissolve into open aged parchment; from that "
            "dissolve, a simple soft-edged image emerges on the right side of the frame: a plain "
            "wooden cross silhouette against a pale open sky, distant and still."
            + GUARDRAIL
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
CREDITS_TO_USD = 0.05  # user-corrected rate (5000cr = $250)


def generate_one(item: dict) -> dict:
    stem = f"{item['concept']}_{item['id']}"
    png_path = OUT_DIR / f"{stem}.png"
    result = {**item, "stem": stem, "ok": False, "error": None}
    if png_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {stem}.png already exists")
        return result

    print(f"  [{item['model']}] {stem} - {item['beat']}")
    try:
        proc = subprocess.run(
            [HF_CLI, "generate", "create", item["model"],
             "--prompt", item["prompt"],
             "--aspect_ratio", "9:16",
             "--wait"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=600,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"hf CLI exit {proc.returncode}: {proc.stderr.strip()[-400:]}")
        match = _URL_RE.search(proc.stdout)
        if not match:
            raise RuntimeError(f"no image URL in stdout: {proc.stdout.strip()[-400:]}")
        url = match.group(0)
        req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            png_path.write_bytes(resp.read())
        print(f"        -> {png_path.name} ({png_path.stat().st_size:,} bytes)")
        result["ok"] = True
    except Exception as e:
        print(f"        FAILED: {e}")
        result["error"] = str(e)
    return result


def build_gallery(results: list[dict]) -> None:
    concepts = {}
    for r in results:
        concepts.setdefault(r["concept"], {"label": r["label"], "items": []})
        concepts[r["concept"]]["items"].append(r)

    total_credits = sum(2 for r in results if r["ok"] and not r.get("skipped"))  # all nano_banana_pro
    total_usd = round(total_credits * CREDITS_TO_USD, 2)

    cards = []
    for key, c in concepts.items():
        items_html = ""
        for it in c["items"]:
            if it["ok"]:
                img = f'<img src="stills/{it["stem"]}.png" alt="{it["beat"]}" loading="lazy">'
            else:
                img = f'<div class="fail">FAILED<br>{it.get("error","")[:200]}</div>'
            items_html += f'''
            <figure>
              {img}
              <figcaption><b>{it["id"]}</b> — {it["beat"]}</figcaption>
            </figure>'''
        cards.append(f'''
        <section>
          <h2>{c["label"]}</h2>
          <div class="row">{items_html}</div>
        </section>''')

    html = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Round 2 devices — 5 concepts, 3 stills each</title>
<style>
  body {{ background:#141210; color:#EDE7D9; font-family: Georgia, serif; margin:0; padding:40px 24px 80px; }}
  h1 {{ font-size: 26px; font-weight: 400; }}
  .meta {{ color:#B3AB9B; font-family: ui-monospace, monospace; font-size: 13px; margin-bottom: 40px; }}
  section {{ margin-bottom: 48px; border-top: 1px solid #3A342B; padding-top: 24px; }}
  h2 {{ color:#D97C5C; font-weight:400; font-size:20px; margin-bottom:16px; }}
  .row {{ display:flex; gap:16px; flex-wrap:wrap; }}
  figure {{ margin:0; width: 280px; }}
  img {{ width:100%; display:block; border-radius:3px; background:#000; }}
  .fail {{ width:280px; height:498px; background:#2a1414; color:#e08; display:flex; align-items:center; justify-content:center; text-align:center; padding:12px; font-family:monospace; font-size:11px; border-radius:3px; }}
  figcaption {{ font-size:13px; color:#B3AB9B; margin-top:8px; }}
  figcaption b {{ color:#EDE7D9; }}
</style></head><body>
<h1>Round 2 devices — 5 concepts, 3 stills each</h1>
<div class="meta">Fable's structural-device brief &middot; throwaway POC, not in production pipeline &middot; spend this run: ~{total_credits} credits (~${total_usd})</div>
{"".join(cards)}
</body></html>'''
    gallery_path = Path(__file__).resolve().parent / "index.html"
    gallery_path.write_text(html, encoding="utf-8")
    print(f"\nGallery: {gallery_path}")
    print(f"Spend this run: ~{total_credits} credits (~${total_usd})")


if __name__ == "__main__":
    results = [generate_one(item) for item in STILLS]
    (Path(__file__).resolve().parent / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    build_gallery(results)
