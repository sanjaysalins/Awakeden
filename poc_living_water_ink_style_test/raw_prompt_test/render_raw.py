"""THROWAWAY POC — NOT part of the production pipeline.

Sends the master prompt file VERBATIM (no editing, no splitting, no
adaptation) to NBP as a single 9:16 generation. No transformation of the
user's prompt text.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\raw_prompt_test\\render_raw.py
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
MD_PATH = Path(r"C:\Users\sanjay\Downloads\NBP Master Prompt — Living Water.md")
OUT_PATH = HERE / "raw_prompt_9x16.png"

SIBLING_ENV = Path(r"C:\Users\sanjay\PycharmProjects\PythonProject1\.env")
if SIBLING_ENV.exists():
    load_dotenv(SIBLING_ENV, override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-3-pro-image-preview"

if __name__ == "__main__":
    if not GEMINI_API_KEY:
        raise SystemExit(f"GEMINI_API_KEY not set (checked {SIBLING_ENV})")

    prompt = MD_PATH.read_text(encoding="utf-8")
    print(f"Prompt length: {len(prompt):,} chars (verbatim from {MD_PATH.name})")

    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)
    resp = client.models.generate_content(
        model=MODEL,
        contents=[{"parts": [{"text": prompt}]}],
        config={
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "9:16"},
        },
    )
    candidates = getattr(resp, "candidates", None) or []
    if not candidates:
        raise SystemExit("NBP returned no candidates")
    cand_parts = candidates[0].content.parts if candidates[0].content else []
    image_bytes = None
    for p in cand_parts:
        if getattr(p, "inline_data", None) and p.inline_data.data:
            image_bytes = p.inline_data.data
            break
    if not image_bytes:
        finish = getattr(candidates[0], "finish_reason", "?")
        raise SystemExit(f"No image bytes (finish_reason={finish})")

    OUT_PATH.write_bytes(image_bytes)
    print(f"-> {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")
