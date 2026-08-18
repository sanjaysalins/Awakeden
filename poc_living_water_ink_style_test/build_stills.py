"""THROWAWAY POC — NOT part of the production pipeline.

Style-feasibility test: can NBP (Gemini 3 Pro Image Preview) hit the
hand-drawn ink-animation look described in
`C:\\Users\\sanjay\\Downloads\\NBP Master Prompt — Living Water.md`
(John 4:4-42, Jesus and the Samaritan woman)?

5 self-contained stills (Fable-authored prompts, no reference images, no
continuity between calls — each prompt restates the full character design)
spanning the story's blue "Swirls of Life" progression: almost-none ->
first restrained trace -> penetrating density -> one delicate swirl ->
diffused through the whole community.

Standalone — does NOT import pipeline/config, mirrors the google.genai call
pattern in pipeline/visual_render.py's NBPProvider but independent of it.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\build_stills.py
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "stills"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Sibling project's .env holds GEMINI_API_KEY (same source config.py uses).
SIBLING_ENV = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\.env")
if SIBLING_ENV.exists():
    load_dotenv(SIBLING_ENV, override=False)
load_dotenv(HERE.parent / ".env", override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-3-pro-image-preview"
ASPECT_RATIO = "9:16"
USD_PER_IMG = 0.50

STILLS = [
    # Filled in from Fable's output — see _prompts.json (written once Fable returns).
]


def _load_stills() -> list[dict]:
    if STILLS:
        return STILLS
    prompts_path = HERE / "_prompts.json"
    if not prompts_path.exists():
        raise SystemExit(f"No prompts: fill STILLS in this file or write {prompts_path}")
    return json.loads(prompts_path.read_text(encoding="utf-8"))


def generate_one(client, genai_types, item: dict) -> dict:
    stem = f"seq{item['seq']}_{item['label'].lower().replace(' ', '_')}"
    png_path = OUT_DIR / f"{stem}.png"
    result = {**item, "stem": stem, "ok": False, "error": None, "skipped": False}
    if png_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {stem}.png already exists")
        return result

    print(f"  [nbp] {stem} - {item['beat']}")
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=[{"parts": [{"text": item["prompt"]}]}],
            config={
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": ASPECT_RATIO},
            },
        )
        candidates = getattr(resp, "candidates", None) or []
        if not candidates:
            raise RuntimeError("NBP returned no candidates")
        cand_parts = candidates[0].content.parts if candidates[0].content else []
        image_bytes = None
        for p in cand_parts:
            if getattr(p, "inline_data", None) and p.inline_data.data:
                image_bytes = p.inline_data.data
                break
        if not image_bytes:
            finish = getattr(candidates[0], "finish_reason", "?")
            raise RuntimeError(f"no image bytes (finish_reason={finish})")
        png_path.write_bytes(image_bytes)
        print(f"        -> {png_path.name} ({png_path.stat().st_size:,} bytes)")
        result["ok"] = True
    except Exception as e:
        print(f"        FAILED: {e}")
        result["error"] = str(e)
    return result


def build_gallery(results: list[dict]) -> None:
    rendered = sum(1 for r in results if r["ok"] and not r["skipped"])
    total_usd = round(rendered * USD_PER_IMG, 2)

    cards = []
    for r in results:
        if r["ok"]:
            img = f'<img src="stills/{r["stem"]}.png" alt="{r["beat"]}" loading="lazy">'
        else:
            img = f'<div class="fail">FAILED<br>{(r.get("error") or "")[:300]}</div>'
        cards.append(f'''
        <figure>
          {img}
          <figcaption><b>SEQ {r["seq"]} — {r["label"]}</b><br>{r["beat"]}</figcaption>
        </figure>''')

    html = f'''<!doctype html><html><head><meta charset="utf-8">
<title>Living Water — ink-animation style test (NBP)</title>
<style>
  body {{ background:#141210; color:#EDE7D9; font-family: Georgia, serif; margin:0; padding:40px 24px 80px; }}
  h1 {{ font-size: 24px; font-weight: 400; }}
  .meta {{ color:#B3AB9B; font-family: ui-monospace, monospace; font-size: 13px; margin-bottom: 32px; }}
  .row {{ display:flex; gap:20px; flex-wrap:wrap; }}
  figure {{ margin:0; width: 300px; }}
  img {{ width:100%; display:block; border-radius:3px; background:#000; }}
  .fail {{ width:300px; height:534px; background:#2a1414; color:#e08; display:flex; align-items:center; justify-content:center; text-align:center; padding:12px; font-family:monospace; font-size:11px; border-radius:3px; }}
  figcaption {{ font-size:13px; color:#B3AB9B; margin-top:8px; line-height:1.4; }}
  figcaption b {{ color:#EDE7D9; }}
</style></head><body>
<h1>Living Water — ink-animation style test</h1>
<div class="meta">Source: John 4:4-42, "NBP Master Prompt — Living Water.md" &middot; provider: NBP (gemini-3-pro-image-preview) &middot; throwaway POC, not in production pipeline &middot; spend this run: {rendered} image(s) (~${total_usd})</div>
<div class="row">{"".join(cards)}</div>
</body></html>'''
    gallery_path = HERE / "index.html"
    gallery_path.write_text(html, encoding="utf-8")
    print(f"\nGallery: {gallery_path}")
    print(f"Spend this run: {rendered} image(s) (~${total_usd})")


if __name__ == "__main__":
    if not GEMINI_API_KEY:
        raise SystemExit(f"GEMINI_API_KEY not set (checked {SIBLING_ENV} and repo .env)")
    from google import genai
    from google.genai import types as genai_types

    client = genai.Client(api_key=GEMINI_API_KEY)
    items = _load_stills()
    results = [generate_one(client, genai_types, item) for item in items]
    (HERE / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    build_gallery(results)
