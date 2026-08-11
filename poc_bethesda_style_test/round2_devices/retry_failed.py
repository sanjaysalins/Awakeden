"""THROWAWAY POC retry — re-render the 4 stills that hit the nsfw false-positive."""
from __future__ import annotations
import re, subprocess, urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
OUT_DIR = Path(__file__).resolve().parent / "stills"
GUARDRAIL = (
    ", absolutely no legible text, no legible lettering, no readable words or "
    "numerals anywhere in the image -- any writing-like marks must read as "
    "abstract ink texture or blank/illegible surface only, no visible text or "
    "captions, no modern objects or clothing, reverent and dignified tone, "
    "ancient Near-Eastern or period-appropriate setting only, fully and modestly "
    "clothed, no gore, no nsfw"
)

RETRIES = [
    {
        "stem": "sounding_line_03", "model": "nano_banana_pro",
        "prompt": (
            "Detailed 19th-century scientific cross-section engraving, cutaway diagram style, "
            "muted mineral ink-wash palette of slate blue-grey and faded sienna, fine technical "
            "linework, aged parchment ground, restrained and scholarly like a naturalist's survey "
            "plate. A close cutaway view of an entirely empty rock-cut tomb chamber: the round "
            "stone rolled aside from the entrance, soft light spilling into the bare chamber from "
            "outside, a single plain white burial cloth folded neatly on an empty stone shelf. "
            "Nothing else in the chamber, no person present, quiet and resolved."
            + GUARDRAIL
        ),
    },
    {
        "stem": "registration_pull_03", "model": "nano_banana_pro",
        "prompt": (
            "Illuminated manuscript page illustration layered beneath a translucent vellum "
            "overlay sheet, aged vellum ground, fine ink linework with muted gold and umber wash, "
            "restrained devotional palette, like a printmaker's registration proof. An extreme "
            "close-up on one small still-life ink diagram: a scatter of small rounded bone gaming "
            "lots beside a folded garment, drawn on the lower vellum layer. On the upper "
            "translucent vellum sheet above it, a near-identical scatter of small rounded dice is "
            "drawn, precisely aligned over the first, with a thin fine cross-mark glowing at the "
            "single point where the two drawings overlap exactly. No people, objects only."
            + GUARDRAIL
        ),
    },
    {
        "stem": "one_take_scroll_01", "model": "nano_banana_pro",
        "prompt": (
            "Ancient scroll illustration, aged papyrus-toned ground, fine sepia ink linework, "
            "restrained scholarly palette, like a photographed museum scroll fragment. A long "
            "horizontal ancient scroll partially unrolled, its surface covered in dense abstract "
            "vertical texture suggesting columns of ancient script but with no legible letterforms "
            "at all -- pure abstract ink texture only. Along the scroll's bottom margin runs a "
            "thin continuous ink frieze drawing, in the simple flat style of an ancient carved "
            "relief: a small two-wheeled cart pulled by a single ox, one seated figure in modest "
            "ankle-length robes, ancient Near-Eastern dress, ornamental and stylised, ruins-relief "
            "in feeling, ancient art history museum plate."
            + GUARDRAIL
        ),
    },
    {
        "stem": "one_take_scroll_02", "model": "nano_banana_pro",
        "prompt": (
            "Ancient scroll illustration, aged papyrus-toned ground, fine sepia ink linework, "
            "restrained scholarly palette, like a photographed museum scroll fragment. A close "
            "view of the scroll's bottom-margin frieze drawing, in the simple flat style of an "
            "ancient carved relief: a small two-wheeled cart at rest, one seated figure in modest "
            "ankle-length robes gesturing outward, a second standing figure in matching modest "
            "robes a short distance away on the roadside, both figures small, stylised and "
            "ornamental, ancient art history museum plate, no anatomical detail. Above the frieze, "
            "the scroll's script-texture columns are abstract ink marks only, no legible "
            "letterforms, dense and even."
            + GUARDRAIL
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
