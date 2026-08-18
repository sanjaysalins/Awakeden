"""THROWAWAY POC — NOT part of the production pipeline.

Renders Fable's 4-still full-storyline set (same storyboard-page pattern as
the working F14 test) via Higgsfield's nano_banana_pro. 9:16 by default.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\full_story_4stills\\render.py
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
ASPECT = "16:9"
MODEL = "nano_banana_pro"

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def render_one(item: dict) -> dict:
    stem = f"{item['seq']}_{item['label'].lower().replace(' ', '_')}_{ASPECT.replace(':', 'x')}"
    out_path = HERE / f"{stem}.png"
    result = {**item, "stem": stem, "ok": False, "error": None}
    if out_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {stem}.png already exists")
        return result

    print(f"  [{MODEL}] {stem} - {item['frame_no']}")
    proc = subprocess.run(
        [HF_CLI, "generate", "create", MODEL,
         "--prompt", item["prompt"],
         "--aspect_ratio", ASPECT,
         "--wait"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=600,
    )
    if proc.returncode != 0:
        result["error"] = f"hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-400:]}"
        print(f"        FAILED: {result['error']}")
        return result
    match = _URL_RE.search(proc.stdout)
    if not match:
        result["error"] = f"no image URL in stdout: {proc.stdout.strip()[-400:]}"
        print(f"        FAILED: {result['error']}")
        return result
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")
    result["ok"] = True
    return result


if __name__ == "__main__":
    items = json.loads((HERE / "_prompts.json").read_text(encoding="utf-8"))
    results = [render_one(item) for item in items]
    (HERE / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for r in results if r["ok"] and not r.get("skipped"))
    print(f"\nRendered {ok} new image(s), {sum(1 for r in results if r.get('skipped'))} skipped.")
