"""THROWAWAY POC retry — re-render the 2 stills that missed on the first pass."""
from __future__ import annotations
import re, subprocess, urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
OUT_DIR = Path(__file__).resolve().parent / "stills"
GUARDRAIL = (
    ", no visible text or lettering, no modern objects or clothing, "
    "reverent and dignified tone, ancient Near-Eastern setting only, no gore, no nsfw"
)

RETRIES = [
    {
        "stem": "far_corner_03", "model": "nano_banana_pro",
        "prompt": (
            "Detailed archaeological reconstruction illustration, cutaway survey plate style, "
            "muted mineral ink-wash palette of ochre, slate grey and faded sienna, fine technical "
            "linework, aged parchment ground, cartographic precision, seen from directly overhead, "
            "restrained and scholarly like a 19th-century excavation report plate, small distant "
            "schematic figures throughout, no anatomical detail. "
            "An overhead architectural plan view of the far corner of a stone colonnaded porch: two "
            "small, distant, fully-clothed schematic figures in modest ankle-length first-century "
            "robes - one figure reclining on a thin mat, one figure standing upright beside him. Both "
            "figures rendered as tiny simplified survey-plate icons, no facial or bodily detail, "
            "entirely covered by loose robes. In the far distance at the edge of frame, a sliver of a "
            "rectangular pool is visible, still and untouched. A single fine red survey-line runs from "
            "off-frame into this corner, ending at the standing figure's feet - the only mark of color "
            "in an otherwise muted palette. Still, resolved, quiet, purely diagrammatic and modest."
            + GUARDRAIL
        ),
    },
    {
        "stem": "take_up_thy_bed_01", "model": "seedream_v5_pro",
        "prompt": (
            "Extreme macro studio product photography of a single object, shot on a pure seamless "
            "black backdrop with nothing else visible in frame - no architecture, no room, no "
            "landscape, no pool, no horizon, only pure black void surrounding the object. Dramatic "
            "hard raking light from one side, like a museum relic documentary film still, shallow "
            "depth of field, extreme material realism. "
            "The object: a thin ancient woven reed sleeping mat filling most of the frame, its close-up "
            "texture in sharp macro focus. The weave shows decades of wear and frayed fibers, and a "
            "faint but unmistakable body-shaped darkened impression is pressed permanently into the "
            "surface where a person has lain for a very long time. Severe, intimate, museum-relic "
            "authority - absolutely nothing in frame but the mat and the black void around it."
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
