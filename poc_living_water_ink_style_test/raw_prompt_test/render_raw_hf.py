"""THROWAWAY POC — NOT part of the production pipeline.

Same as render_raw.py, but via the Higgsfield CLI (nano_banana_pro) instead
of calling google.genai directly. Sends the master prompt file VERBATIM
(no editing, no splitting, no adaptation).

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\raw_prompt_test\\render_raw_hf.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
MD_PATH = Path(r"C:\Users\sanjay\Downloads\NBP Master Prompt — Living Water.md")
OUT_PATH = Path(__file__).resolve().parent / "raw_prompt_9x16_hf.png"
MODEL = "nano_banana_pro"

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

if __name__ == "__main__":
    prompt = MD_PATH.read_text(encoding="utf-8")
    print(f"Prompt length: {len(prompt):,} chars (verbatim from {MD_PATH.name})")

    proc = subprocess.run(
        [HF_CLI, "generate", "create", MODEL,
         "--prompt", prompt,
         "--aspect_ratio", "9:16",
         "--wait"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=600,
    )
    if proc.returncode != 0:
        raise SystemExit(f"hf CLI exit {proc.returncode}: {proc.stderr.strip()[-800:]}\nstdout: {proc.stdout.strip()[-800:]}")
    match = _URL_RE.search(proc.stdout)
    if not match:
        raise SystemExit(f"no image URL in stdout: {proc.stdout.strip()[-800:]}")
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        OUT_PATH.write_bytes(resp.read())
    print(f"-> {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")
