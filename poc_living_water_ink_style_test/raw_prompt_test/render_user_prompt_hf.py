"""THROWAWAY POC — NOT part of the production pipeline.

Runs the user's exact prompt, verbatim, via Higgsfield's nano_banana_pro
(NBP) model. No editing of the prompt text.

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\raw_prompt_test\\render_user_prompt_hf.py
"""
from __future__ import annotations

import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
ASPECT = "16:9"
OUT_PATH = Path(__file__).resolve().parent / f"user_prompt_{ASPECT.replace(':', 'x')}_hf.png"
MODEL = "nano_banana_pro"

PROMPT = '''Create a piece of conceptual storyboard art on aged textured paper for a sequence titled "Living Water / Jesus & Woman."

The page should look like rough but beautiful animation development art, drawn in expressive black ink with muted watercolor washes. Use a hand-drawn storyboard aesthetic with visible sketch lines, brush textures, rough edges, handwritten notes, and a vintage paper base.

The page layout should include:

a title at the top left: "SEQ: Living Water / Jesus & Woman"
frame number text "F14" at the top right
a top row of three storyboard panels
a large full-scene illustration filling the lower half of the page
small annotation sketches and handwritten notes integrated naturally

Top storyboard panels:

A close-up portrait of Jesus facing left, stylized and ink-drawn, with a subtle abstract aura/halo. Label the panel "1". Under it, handwrite: "F14: THE LIVING WATER".
A sketch of a distant hill-town or Samaritan city, labeled "2".
A sketch of the Samaritan woman moving away quickly with her water jar, looking back over her shoulder, labeled "3". To the side, include the handwritten note: "NOTE: Swirls of Life".

In the large lower illustration, show Jesus seated on a large stone beside a stone well, gesturing calmly toward the Samaritan woman. She stands opposite him with curiosity, holding a small pot from which blue and gold life-like swirling forms subtly emerge. She wears stylized robes and a head covering. The background shows a rolling desert landscape with scattered olive trees and open space.

At the bottom left, include a small distant drawing of six or seven disciples walking along a path, with the handwritten note: "DISCIPLES ARRIVING".

Repeat the note "NOTE: Swirls of Life" near the woman\u2019s pot.

The art style should remain rough, expressive, and exploratory \u2014 more like animation concept art than finished illustration.

Color palette: black ink, blue, ochre, muted green, brown, and touches of soft gold wash.

Avoid photorealism, polished graphic design, clean comic-book inking, and overly neat layout. The page should feel handmade, thoughtful, and alive.'''

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

if __name__ == "__main__":
    print(f"Prompt length: {len(PROMPT):,} chars (verbatim, user-supplied)")
    proc = subprocess.run(
        [HF_CLI, "generate", "create", MODEL,
         "--prompt", PROMPT,
         "--aspect_ratio", ASPECT,
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
