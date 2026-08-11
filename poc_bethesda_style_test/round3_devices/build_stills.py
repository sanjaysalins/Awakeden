"""THROWAWAY POC -- NOT part of the production pipeline.

Round 3: 6 structural-device concepts. Two of them (The Same Fire, The
Blemish Hunt) are explicitly pitched as "one AI plate + code does the rest"
-- this script actually proves that: 1 generation each, then real PIL
post-processing (relight / crop-zoom) produces the other 2 "stills", never
a second AI generation hoping to match the first.
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageDraw

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
OUT_DIR = Path(__file__).resolve().parent / "stills"
OUT_DIR.mkdir(parents=True, exist_ok=True)

GUARDRAIL = (
    ", absolutely no legible text, no legible lettering, no readable words or "
    "numerals anywhere in the image, no modern objects or clothing, reverent "
    "and dignified tone, ancient Near-Eastern or period-appropriate setting "
    "only, no gore, no nsfw, fully and modestly clothed"
)
SKETCH_STYLE = (
    "Hand-drawn editorial sketch illustration, ink linework with muted "
    "watercolor wash on aged sketchbook paper, journal-style, restrained "
    "earth and sepia palette, warm and painterly, not photographic, not a "
    "photograph, drawn and inked by hand"
)
TOKEN_STYLE = (
    "Flat hand-drawn ink-wash illustration on aged paper, editorial sketch "
    "style, restrained muted night palette of deep blue-grey and warm ochre "
    "pale wash reserve for light, paper tooth visible, not photographic, not "
    "a photograph, drawn and inked by hand"
)

# AI generations only -- text/lettering for these beats is added by CODE in
# real production (Scribed Ink / keeper-hand), never by the image model.
AI_STILLS = [
    # ---------------- 1: THE SAME FIRE (John 21) -- 1 gen, 2 code regrades ----------------
    {
        "concept": "same_fire", "label": "The Same Fire", "id": "raw",
        "beat": "AI plate — neutral study, meant to be relit",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A small charcoal fire glowing in a simple stone "
            "fire-ring, a few embers and sticks of wood, rendered under flat, "
            "even, neutral daylight with no strong directional shadows -- a "
            "calm neutral study meant to be relit later. Plain aged paper "
            "background, nothing else in frame, centered, clean simple "
            "linework." + GUARDRAIL
        ),
    },

    # ---------------- 2: THE EARLIER PAGE (1 Cor 5:7) ----------------
    {
        "concept": "earlier_page", "label": "The Earlier Page", "id": "01",
        "beat": "The current spread — the assumed order",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". An open handwritten journal page, aged cream "
            "paper, faint ruled lines, a small hand-drawn margin sketch of "
            "two simple bundle icons stacked one above the other suggesting "
            "an ordered list, warm ink linework, quiet and orderly."
            + GUARDRAIL
        ),
    },
    {
        "concept": "earlier_page", "label": "The Earlier Page", "id": "02",
        "beat": "The earlier leaf — already recorded, dated before",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A single much older aged parchment leaf, foxed "
            "and yellowed at the edges, its ink faded to pale brown, held "
            "slightly apart from a newer page beside it, a small sketched "
            "icon of a simple lamb resting near the top of the old leaf, "
            "deckled edges, linen-tape corner repair, warm restrained sepia "
            "and faint gold-leaf accents." + GUARDRAIL
        ),
    },
    {
        "concept": "earlier_page", "label": "The Earlier Page", "id": "03",
        "beat": "The page turns — the corrected sequence",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". An open book spread seen from slightly above, "
            "one page caught mid-turn, the gutter and real page thickness "
            "clearly visible, warm raking light crossing the pages, a small "
            "sketched lamb icon near the top of one page and a simple "
            "checklist icon below it, aged paper texture throughout."
            + GUARDRAIL
        ),
    },

    # ---------------- 3: THE SIGHTLINE (Zacchaeus, Luke 19) ----------------
    {
        "concept": "sightline", "label": "The Sightline", "id": "01",
        "beat": "Hook — the crowd, the tree, the vertical axis",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ", tall vertical composition. A full-height street "
            "scene in an ancient town: a dusty road and a dense crowd of "
            "robed figures shown only as backs of heads and shoulders along "
            "the bottom of the frame, a tall sycamore tree trunk rising "
            "through the center of the frame, its branches spreading near "
            "the top. No visible faces in the crowd." + GUARDRAIL
        ),
    },
    {
        "concept": "sightline", "label": "The Sightline", "id": "02",
        "beat": "Up the trunk — one small figure in the branch",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A close view partway up a thick sycamore tree "
            "trunk and its lower branches, one small robed figure perched "
            "carefully on a branch, seen from a middle distance, looking "
            "down and outward, face only lightly suggested. Dappled leaf "
            "shadow, warm daylight." + GUARDRAIL
        ),
    },
    {
        "concept": "sightline", "label": "The Sightline", "id": "03",
        "beat": "Landing — the two lines meet",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A view looking up from street level into "
            "sycamore branches: a small robed figure sits in the branch "
            "above, looking down; far below at the base of the trunk, "
            "another robed figure stands looking directly up, one hand "
            "slightly raised. Warm daylight, dappled leaf shadow, both "
            "figures small and clear, no faces in close detail."
            + GUARDRAIL
        ),
    },

    # ---------------- 4: THE TOKEN (Exodus 12) ----------------
    {
        "concept": "token", "label": "The Token", "id": "01",
        "beat": "Hook — the street, every doorway dark",
        "model": "nano_banana_pro",
        "prompt": (
            TOKEN_STYLE + ". A long straight street of an ancient mudbrick "
            "town at night, a row of plain doorways receding into the "
            "distance, each doorway a simple dark rectangle in a plain "
            "wall, no figures visible, one pale wash of light low on the "
            "horizon." + GUARDRAIL
        ),
    },
    {
        "concept": "token", "label": "The Token", "id": "02",
        "beat": "The mark blooms on the lintel",
        "model": "nano_banana_pro",
        "prompt": (
            TOKEN_STYLE + ". A close view of one plain mudbrick doorway at "
            "night: a dark red ink mark drawn across the lintel and both "
            "doorposts in three deliberate strokes, the ink slightly bled "
            "at the edges, the doorway itself a plain dark rectangle, no "
            "figures visible." + GUARDRAIL
        ),
    },
    {
        "concept": "token", "label": "The Token", "id": "03",
        "beat": "Landing — the judgment pass",
        "model": "nano_banana_pro",
        "prompt": (
            TOKEN_STYLE + ". Two plain doorways side by side at night: the "
            "left doorway grand and finely built but entirely dark and "
            "unmarked, the right doorway small and plain but marked with a "
            "dark red stroke across its lintel and glowing with a warm pale "
            "wash of light spilling from within. No figures visible."
            + GUARDRAIL
        ),
    },

    # ---------------- 5: THE BLEMISH HUNT (Exodus 12:5-6) -- 1 gen, 2 code crops ----------------
    {
        "concept": "blemish_hunt", "label": "The Blemish Hunt", "id": "raw",
        "beat": "AI plate — the whole lamb, meant to be studied",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A single young lamb standing calmly in profile, "
            "full body visible, rendered as a careful naturalist study, "
            "clean simple linework, plain aged paper background, soft even "
            "lighting, centered composition, nothing else in frame."
            + GUARDRAIL
        ),
    },

    # ---------------- 6: THE THIRD LINE (the prodigal, Luke 15:20) ----------------
    {
        "concept": "third_line", "label": "The Third Line", "id": "01",
        "beat": "The rehearsal — alone on the road",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A dusty road scene, a lone ragged robed figure "
            "walking alone in the distance, small in frame, the road "
            "stretching ahead toward a distant home, warm late-afternoon "
            "light, quiet and solitary mood." + GUARDRAIL
        ),
    },
    {
        "concept": "third_line", "label": "The Third Line", "id": "02",
        "beat": "The run — interrupted mid-approach",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A wide view of a dusty road: an older robed "
            "figure running toward a smaller ragged figure in the middle "
            "distance, both figures caught mid-motion, arms outstretched, "
            "warm golden late-afternoon light, dust caught in the air near "
            "their feet, emotional and warm." + GUARDRAIL
        ),
    },
    {
        "concept": "third_line", "label": "The Third Line", "id": "03",
        "beat": "Landing — the embrace, the line unfinished",
        "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A close view of two robed figures embracing, "
            "an older figure with arms wrapped around a smaller ragged "
            "figure who is bowed with his face hidden against the older "
            "man's shoulder, warm golden light, tender and quiet mood, no "
            "visible faces in close detail." + GUARDRAIL
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)
CREDITS_TO_USD = 0.05


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


# --------------------------------------------------------------------------
# CODE-ONLY derivations -- the actual point of this round's two pitches.
# --------------------------------------------------------------------------
def _radial_vignette(img: Image.Image, cx_frac, cy_frac, inner_frac, outer_frac, dark_to=0.15):
    """Multiplicative radial mask: 1.0 near (cx,cy), fading to dark_to at outer_frac."""
    w, h = img.size
    cx, cy = w * cx_frac, h * cy_frac
    max_r = (w ** 2 + h ** 2) ** 0.5 / 2
    inner, outer = inner_frac * max_r, outer_frac * max_r
    mask = Image.new("L", (w, h), 0)
    dr = mask.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= inner:
                v = 255
            elif d >= outer:
                v = int(255 * dark_to)
            else:
                t = (d - inner) / max(1e-6, outer - inner)
                v = int(255 * (1 - t * (1 - dark_to)))
            dr[x, y] = v
            if x + 1 < w:
                dr[x + 1, y] = v
            if y + 1 < h:
                dr[x, y + 1] = v
            if x + 1 < w and y + 1 < h:
                dr[x + 1, y + 1] = v
    return mask


def relight_fire(raw_path: Path, night_out: Path, dawn_out: Path) -> None:
    """The Same Fire's whole thesis: ONE plate, TWO code-only lightings.
    No second generation, no alignment risk -- literally the same pixels."""
    base = Image.open(raw_path).convert("RGB")
    w, h = base.size

    # NIGHT: cool, desaturated, tight radial light held close around the fire
    # (candle-only device logic) -- fear closes the light down.
    night = ImageEnhance.Color(base).enhance(0.55)
    night = ImageEnhance.Brightness(night).enhance(0.62)
    night = ImageEnhance.Contrast(night).enhance(1.08)
    r, g, b = night.split()
    b = ImageEnhance.Brightness(b).enhance(1.18)
    r = ImageEnhance.Brightness(r).enhance(0.92)
    night = Image.merge("RGB", (r, g, b))
    mask = _radial_vignette(base, 0.5, 0.62, inner_frac=0.10, outer_frac=0.42, dark_to=0.22)
    dark = ImageEnhance.Brightness(night).enhance(0.35)
    night = Image.composite(night, dark, mask)
    night.save(night_out)
    print(f"  [ok] {night_out.name} (code regrade -- night, candle-only)")

    # DAWN: warm, brighter, light radius wide open -- grace arrives, opens up.
    dawn = ImageEnhance.Color(base).enhance(1.12)
    dawn = ImageEnhance.Brightness(dawn).enhance(1.15)
    dawn = ImageEnhance.Contrast(dawn).enhance(1.05)
    r, g, b = dawn.split()
    r = ImageEnhance.Brightness(r).enhance(1.16)
    g = ImageEnhance.Brightness(g).enhance(1.05)
    b = ImageEnhance.Brightness(b).enhance(0.88)
    dawn = Image.merge("RGB", (r, g, b))
    mask2 = _radial_vignette(base, 0.5, 0.62, inner_frac=0.35, outer_frac=0.95, dark_to=0.72)
    soft_dark = ImageEnhance.Brightness(dawn).enhance(0.8)
    dawn = Image.composite(dawn, soft_dark, mask2)
    dawn.save(dawn_out)
    print(f"  [ok] {dawn_out.name} (code regrade -- dawn, wide open)")


def crop_study(raw_path: Path, out_path: Path, box_frac: tuple, label: str) -> None:
    """The Blemish Hunt's whole thesis: ONE plate, magnified crops derived by
    code, never a second generation of 'the same lamb'."""
    img = Image.open(raw_path).convert("RGB")
    w, h = img.size
    x0, y0, x1, y1 = box_frac
    crop = img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    crop = crop.resize((w, h), Image.LANCZOS)
    crop.save(out_path)
    print(f"  [ok] {out_path.name} (code crop-zoom -- {label})")


def build_gallery(results: list[dict], derived: list[dict]) -> None:
    concepts = {}
    for r in results:
        concepts.setdefault(r["concept"], {"label": r["label"], "items": []})
        concepts[r["concept"]]["items"].append({**r, "kind": "ai"})
    for d in derived:
        concepts.setdefault(d["concept"], {"label": d["label"], "items": []})
        concepts[d["concept"]]["items"].append({**d, "kind": "code"})

    total_credits = sum(2 for r in results if r["ok"] and not r.get("skipped"))
    total_usd = round(total_credits * CREDITS_TO_USD, 2)

    cards = []
    for key, c in concepts.items():
        items_html = ""
        for it in c["items"]:
            badge = "AI generation" if it["kind"] == "ai" else "code-derived, $0"
            if it.get("ok", True):
                img = f'<img src="stills/{it["stem"]}.png" alt="{it["beat"]}" loading="lazy">'
            else:
                img = f'<div class="fail">FAILED<br>{it.get("error","")[:200]}</div>'
            items_html += f'''
            <figure>
              {img}
              <figcaption><b>{it["id"]}</b> — {it["beat"]}<br><span class="badge">{badge}</span></figcaption>
            </figure>'''
        cards.append(f'''
        <section>
          <h2>{c["label"]}</h2>
          <div class="row">{items_html}</div>
        </section>''')

    html = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Round 3 devices — 6 concepts</title>
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
  .badge {{ font-family: ui-monospace, monospace; font-size:10.5px; color:#7FA095; }}
</style></head><body>
<h1>Round 3 devices — 6 concepts</h1>
<div class="meta">Fable's round-3 brief &middot; throwaway POC, not in production pipeline &middot; AI spend this run: ~{total_credits} credits (~${total_usd}) &middot; Same Fire + Blemish Hunt include real $0 code-derived views, not extra generations</div>
{"".join(cards)}
</body></html>'''
    gallery_path = Path(__file__).resolve().parent / "index.html"
    gallery_path.write_text(html, encoding="utf-8")
    print(f"\nGallery: {gallery_path}")
    print(f"AI spend this run: ~{total_credits} credits (~${total_usd})")


if __name__ == "__main__":
    results = [generate_one(item) for item in AI_STILLS]
    (Path(__file__).resolve().parent / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    derived = []
    fire_raw = OUT_DIR / "same_fire_raw.png"
    if fire_raw.exists():
        relight_fire(fire_raw, OUT_DIR / "same_fire_night.png", OUT_DIR / "same_fire_dawn.png")
        derived += [
            {"concept": "same_fire", "label": "The Same Fire", "id": "night",
             "beat": "Code regrade — the denial, cold and closed", "stem": "same_fire_night"},
            {"concept": "same_fire", "label": "The Same Fire", "id": "dawn",
             "beat": "Code regrade — the same fire, warm and open", "stem": "same_fire_dawn"},
        ]

    lamb_raw = OUT_DIR / "blemish_hunt_raw.png"
    if lamb_raw.exists():
        crop_study(lamb_raw, OUT_DIR / "blemish_hunt_flank.png", (0.20, 0.30, 0.75, 0.75), "day 12, the flank")
        crop_study(lamb_raw, OUT_DIR / "blemish_hunt_eye.png", (0.32, 0.28, 0.58, 0.50), "day 14, the eye")
        derived += [
            {"concept": "blemish_hunt", "label": "The Blemish Hunt", "id": "flank",
             "beat": "Code crop-zoom — day 12, the flank", "stem": "blemish_hunt_flank"},
            {"concept": "blemish_hunt", "label": "The Blemish Hunt", "id": "eye",
             "beat": "Code crop-zoom — day 14, the eye, without blemish", "stem": "blemish_hunt_eye"},
        ]

    build_gallery(results, derived)
