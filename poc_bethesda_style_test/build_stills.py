"""THROWAWAY POC — NOT part of the production pipeline.

Generates 3 stills x 4 fresh creative concepts (Fable's brief) for the
Bethesda short ("29 The Race He Could Never Win", John 5), via the same
Higgsfield CLI invocation pattern the real pipeline uses
(pipeline/visual_render.py HFProvider.generate), but standalone — does not
import or touch any production pipeline code or config.

Run: .venv\\Scripts\\python.exe poc_bethesda_style_test\\build_stills.py
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

GUARDRAIL = (
    ", no visible text or lettering, no modern objects or clothing, "
    "reverent and dignified tone, ancient Near-Eastern setting only, no gore, no nsfw"
)

CREDITS_TO_USD = 0.15  # anchored: nano_banana_2 2cr ~= $0.30 (pipeline/cost.py)

STILLS = [
    # ---------------- CONCEPT 1: THE FAR CORNER (overhead survey plate) ----------------
    {
        "concept": "far_corner", "label": "The Far Corner", "id": "01",
        "beat": "Hook — the whole complex, overhead",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed archaeological reconstruction illustration, cutaway survey plate style, "
            "muted mineral ink-wash palette of ochre, slate grey and faded sienna, fine technical "
            "linework, aged parchment ground, cartographic precision, seen from directly overhead, "
            "restrained and scholarly like a 19th-century excavation report plate. "
            "An overhead cutaway view of the entire Pool of Bethesda complex: a rectangular pool at "
            "the center ringed by five covered stone colonnaded porches, each packed with dozens of "
            "tiny huddled figures - the sick, the blind, the lame - lying on mats, all oriented toward "
            "the water. Fine architectural linework renders the columns and stonework in precise "
            "archaeological detail. A faint hand-drawn survey grid overlay, the pool at the exact "
            "center a dark still rectangle. Dense with tiny figures, muted and scholarly."
            + GUARDRAIL
        ),
    },
    {
        "concept": "far_corner", "label": "The Far Corner", "id": "02",
        "beat": "Track to the far corner — the measured distance",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed archaeological reconstruction illustration, cutaway survey plate style, "
            "muted mineral ink-wash palette of ochre, slate grey and faded sienna, fine technical "
            "linework, aged parchment ground, cartographic precision, seen from directly overhead, "
            "restrained and scholarly like a 19th-century excavation report plate. "
            "An overhead view tracking along the length of one covered stone porch of the Bethesda "
            "complex: rows of huddled sick figures on mats grow sparser toward the far end, ending at "
            "one man lying utterly alone in the farthest corner, physically separated from the crowd "
            "by open bare stone floor. A thin hand-drawn survey line with small tick marks measures "
            "the distance from the crowd to the lone man, with a small hand-lettered '38' beside it. "
            "Isolated, quiet, the empty stone floor between the crowd and the one man is the subject."
            + GUARDRAIL
        ),
    },
    {
        "concept": "far_corner", "label": "The Far Corner", "id": "03",
        "beat": "Landing — the red path, pulled back",
        "model": "nano_banana_pro",
        "prompt": (
            "Detailed archaeological reconstruction illustration, cutaway survey plate style, "
            "muted mineral ink-wash palette of ochre, slate grey and faded sienna, fine technical "
            "linework, aged parchment ground, cartographic precision, seen from directly overhead, "
            "restrained and scholarly like a 19th-century excavation report plate. "
            "A close overhead view of two tiny figures at the far corner of a stone colonnaded porch: "
            "one man lying on a thin mat, another man standing calmly beside him, unhurried, in plain "
            "first-century robed dress. In the far distance at the edge of frame, a sliver of a "
            "crowded rectangular pool is visible, its water untouched and still. A single fine red "
            "survey-line runs from off-frame into this corner, ending at the standing man's feet - "
            "the only mark of color in an otherwise muted palette. Still, resolved, quiet."
            + GUARDRAIL
        ),
    },

    # ---------------- CONCEPT 2: HIS SKY (first-person POV, painterly) ----------------
    {
        "concept": "his_sky", "label": "His Sky", "id": "01",
        "beat": "Hook — the ceiling, feet crossing",
        "model": "nano_banana_pro",
        "prompt": (
            "First-person point-of-view painting, looking upward, painterly realism with warm "
            "candlelight and rippling water-reflected light, soft atmospheric depth, ancient stone "
            "architecture, reverent and intimate, cinematic framing, no visible narrator body. "
            "Looking straight up from ground level at a weathered ancient stone colonnade ceiling, "
            "ribbed stone arches, warm rippling water-light reflections dancing across the stone from "
            "an unseen pool below. At the very bottom edge of frame, several pairs of sandaled feet "
            "are caught mid-stride, blurred with motion, crossing close past the viewer. Trapped, "
            "patient, warm light against cold stone, the passage of time implied by the blur of feet."
            + GUARDRAIL
        ),
    },
    {
        "concept": "his_sky", "label": "His Sky", "id": "02",
        "beat": "The shadow arrives — no face",
        "model": "nano_banana_pro",
        "prompt": (
            "First-person point-of-view painting, looking upward, painterly realism with warm "
            "candlelight and rippling water-reflected light, soft atmospheric depth, ancient stone "
            "architecture, reverent and intimate, cinematic framing, no visible narrator body. "
            "A first-person view looking up at a tall stone colonnade archway, backlit by bright "
            "daylight; a single robed man's silhouette leans into frame from the side, his shape dark "
            "against the bright light beyond, his face entirely lost in shadow and backlight, one "
            "hand-shape visible at his side. His shadow falls directly down over the viewer's "
            "position. Quiet arrival, no face, only presence, warm bright light behind a dark "
            "reverent silhouette."
            + GUARDRAIL
        ),
    },
    {
        "concept": "his_sky", "label": "His Sky", "id": "03",
        "beat": "Landing — standing upright, the world below",
        "model": "nano_banana_pro",
        "prompt": (
            "First-person point-of-view painting, looking downward from standing height, painterly "
            "realism with warm daylight, soft atmospheric depth, ancient stone architecture, reverent "
            "and intimate, cinematic framing, no visible narrator face. "
            "A first-person view from standing eye-level height, looking down at one's own hands "
            "rolling a thin woven mat into a bundle. Below and beyond, a pool complex with covered "
            "stone colonnades is visible at a distance, small, a churning crowd of the sick still "
            "gathered at the water's edge. The horizon is level, one's own sandaled feet visible at "
            "the bottom of frame, standing upright for the first time. Quiet triumph, warm daylight."
            + GUARDRAIL
        ),
    },

    # ---------------- CONCEPT 3: THE BLUR (long-exposure photographic) ----------------
    {
        "concept": "the_blur", "label": "The Blur", "id": "01",
        "beat": "Hook — one sharp man, a river of ghosts",
        "model": "seedream_v5_pro",
        "prompt": (
            "Long-exposure night photography aesthetic rendered as a single frame, real motion-blur "
            "streaks (not a stylized painting), one subject in tack-sharp focus while everything else "
            "is a smeared trail of light and movement, muted warm-cool palette, ancient Near-Eastern "
            "setting, cinematic and restrained. "
            "A stone porch corner: one gaunt man lies utterly sharp and still on a thin mat in the "
            "lower third of frame, while behind him a river of translucent, elongated motion-blur "
            "silhouettes streams diagonally across the frame toward an unseen glowing pool off to the "
            "side - dozens of blurred ghostly figures in constant motion, none of them resolved, all "
            "moving in one direction. Photographic long-exposure realism, warm glow at the frame edge, "
            "cold stone, the stillness of the one sharp figure the entire point of the image."
            + GUARDRAIL
        ),
    },
    {
        "concept": "the_blur", "label": "The Blur", "id": "02",
        "beat": "Jesus resolves out of the blur",
        "model": "seedream_v5_pro",
        "prompt": (
            "Long-exposure night photography aesthetic rendered as a single frame, real motion-blur "
            "streaks (not a stylized painting), one subject in tack-sharp focus while everything else "
            "is a smeared trail of light and movement, muted warm-cool palette, ancient Near-Eastern "
            "setting, cinematic and restrained. "
            "The same stone porch corner: a gaunt man lies sharp and still on a thin mat as before, "
            "and a second figure is caught mid-resolution, materializing out of the blurred river of "
            "moving ghosts - his lower body still slightly translucent and smeared, his upper body and "
            "standing posture already tack-sharp, standing at the feet of the lying man. Blurred "
            "motion-trails of the crowd continue streaming past in the background. The moment of "
            "arrival, sharpness overtaking blur, a quiet miracle rendered as photographic focus."
            + GUARDRAIL
        ),
    },
    {
        "concept": "the_blur", "label": "The Blur", "id": "03",
        "beat": "Landing — empty porch, one sharp mat",
        "model": "seedream_v5_pro",
        "prompt": (
            "Long-exposure night photography aesthetic rendered as a single frame, real photographic "
            "realism, tack-sharp and still, muted warm-cool palette, ancient Near-Eastern setting, "
            "cinematic and restrained. "
            "The same stone porch corner, now empty of any blur or crowd motion - the streaking "
            "ghost-trails have faded away entirely, leaving only a plain, sharply focused, tack-still "
            "image: an abandoned thin woven mat lying flat on bare stone, slightly rumpled where a "
            "body recently lay. In the distance, a pool's surface is calm and glassy, its faint light "
            "no longer needed. Stillness after motion, resolution, quiet and empty, warm fading light."
            + GUARDRAIL
        ),
    },

    # ---------------- CONCEPT 4: TAKE UP THY BED (macro artifact / void) ----------------
    {
        "concept": "take_up_thy_bed", "label": "Take Up Thy Bed", "id": "01",
        "beat": "Hook — macro on the mat, the body's imprint",
        "model": "seedream_v5_pro",
        "prompt": (
            "Museum artifact macro photography, dramatic raking side-light against pure black void, "
            "extreme material realism, shallow depth of field, restrained and reverent, like a "
            "dark-field relic documentary film still, no people visible. "
            "An extreme macro photograph of a thin ancient woven reed sleeping mat, lit by a single "
            "hard raking light source from one side against a pure black void background. The weave "
            "shows decades of wear, frayed fibers, a faint but unmistakable body-shaped darkened "
            "impression pressed permanently into the surface where a person has lain for a very long "
            "time. Severe, intimate, museum-relic authority, the black void giving the object total "
            "focus."
            + GUARDRAIL
        ),
    },
    {
        "concept": "take_up_thy_bed", "label": "Take Up Thy Bed", "id": "02",
        "beat": "The worn edge — 38 years of dragging toward the water",
        "model": "seedream_v5_pro",
        "prompt": (
            "Museum artifact macro photography, dramatic raking side-light against pure black void, "
            "extreme material realism, shallow depth of field, restrained and reverent, like a "
            "dark-field relic documentary film still, no people visible. "
            "An extreme macro photograph of the frayed, worn corner edge of an ancient woven reed "
            "mat, lit by hard raking side-light against pure black void. The fibers on this one edge "
            "are visibly thinner and more worn than the rest of the mat, clear evidence of being "
            "dragged repeatedly across stone in one direction over many years. Forensic, quiet, a "
            "single detail telling a long story of struggle."
            + GUARDRAIL
        ),
    },
    {
        "concept": "take_up_thy_bed", "label": "Take Up Thy Bed", "id": "03",
        "beat": "Landing — the mat stands, the pool untouched",
        "model": "seedream_v5_pro",
        "prompt": (
            "Museum artifact macro photography, dramatic raking side-light against pure black void, "
            "extreme material realism, shallow depth of field, restrained and reverent, like a "
            "dark-field relic documentary film still, no people visible. "
            "An ancient woven reed mat, rolled into a tight upright bundle, standing unaided on its "
            "end in a pure black void, lit by hard raking side-light. Beside it, in the far negative "
            "space of the frame, the faint circular outline of a still, dark, untouched pool of water "
            "is barely visible in the blackness. Quiet triumph, an object transformed, restrained and "
            "reverent, almost nothing else in frame."
            + GUARDRAIL
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


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

    total_credits = sum(
        (2 if r["model"] == "nano_banana_pro" else 3)
        for r in results if r["ok"] and not r.get("skipped")
    )
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
<title>Bethesda style test — 4 concepts</title>
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
<h1>Bethesda style test — 4 concepts, 3 stills each</h1>
<div class="meta">Source: "29 The Race He Could Never Win" (John 5) &middot; throwaway POC, not in production pipeline &middot; spend this run: ~{total_credits} credits (~${total_usd})</div>
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
