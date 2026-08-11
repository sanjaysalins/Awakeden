"""THROWAWAY POC retry -- re-render the 4 stills that hit the nsfw false-positive."""
from __future__ import annotations
import re, subprocess, urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
OUT_DIR = Path(__file__).resolve().parent / "stills"
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

RETRIES = [
    {
        "stem": "same_fire_raw", "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A small campfire in a ring of plain stones, a "
            "few glowing embers, two or three sticks of wood, simple and "
            "calm, flat even daylight with no strong shadows, a neutral "
            "reference study. Plain aged paper background, nothing else in "
            "frame, centered, clean simple linework." + GUARDRAIL
        ),
    },
    {
        "stem": "earlier_page_01", "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". An open journal page on aged cream paper, "
            "faint ruled lines, a small hand-drawn margin sketch of two "
            "plain cloth bundles stacked one above the other, warm ink "
            "linework, quiet and orderly, otherwise blank." + GUARDRAIL
        ),
    },
    {
        "stem": "token_02", "model": "nano_banana_pro",
        "prompt": (
            TOKEN_STYLE + ". A close view of one plain mudbrick doorway at "
            "night: a dry, matte, dark red painted mark drawn across the "
            "lintel and both doorposts in three deliberate brush strokes, "
            "flat and dry, not wet, not dripping. The doorway itself a "
            "plain dark rectangle, no figures visible." + GUARDRAIL
        ),
    },
    {
        "stem": "blemish_hunt_raw", "model": "nano_banana_pro",
        "prompt": (
            SKETCH_STYLE + ". A single young sheep standing calmly in "
            "profile, full body visible, a simple gentle naturalist study, "
            "clean plain linework, plain aged paper background, soft even "
            "lighting, centered, nothing else in frame." + GUARDRAIL
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

for item in RETRIES:
    print(f"[{item['model']}] {item['stem']} - retry")
    proc = subprocess.run(
        [HF_CLI, "generate", "create", item["model"], "--prompt", item["prompt"],
         "--aspect_ratio", "9:16", "--wait"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
    )
    if proc.returncode != 0:
        print(f"  FAILED: {proc.stderr.strip()[-500:]}")
        continue
    m = _URL_RE.search(proc.stdout)
    if not m:
        print(f"  NO URL: {proc.stdout.strip()[-500:]}")
        continue
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    (OUT_DIR / f"{item['stem']}.png").write_bytes(data)
    print(f"  -> {item['stem']}.png ({len(data):,} bytes)")
