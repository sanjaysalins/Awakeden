"""Retry N2 (nsfw false-positive, reworded) and N3 (transient 503, same wording)."""
from __future__ import annotations
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from pipeline.medium_anchors import SKETCH, build_prompt  # noqa: E402

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PLATES_DIR = HERE / "plates"
REF = HERE.parent.parent.parent / "poc_bethesda_style_test" / "round3_devices" / "stills" / "third_line_02.png"

RETRIES = [
    {
        "stem": "son_rehearsing",
        "subject": (
            "A close view of a young man's shoulders and head from behind and "
            "to the side, dusty and travel-worn, wearing a torn patched olive "
            "tunic, walking along a road with his head bowed low, deep in "
            "silent thought, eyes cast down toward the ground. Dusty road "
            "behind him, warm late light. No frontal facial close-up."
        ),
    },
    {
        "stem": "running_feet",
        "subject": (
            "An extreme low-angle close view of a man's sandaled feet and "
            "the hem of a brown robe, caught mid-stride on a dusty road, "
            "dust puffing up at the point of contact, the hem hitched up "
            "and swinging. No face visible, ground-level framing only."
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)

if __name__ == "__main__":
    for item in RETRIES:
        out_path = PLATES_DIR / f"{item['stem']}.png"
        if out_path.exists():
            print(f"[skip] {out_path.name}")
            continue
        prompt = build_prompt(SKETCH, item["subject"])
        print(f"[nano_banana_pro] {item['stem']} - retry")
        proc = subprocess.run(
            [HF_CLI, "generate", "create", "nano_banana_pro", "--prompt", prompt,
             "--aspect_ratio", "9:16", "--image", str(REF), "--wait"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
        )
        if proc.returncode != 0:
            print(f"  FAILED: {proc.stderr.strip()[-500:]}")
            continue
        m = _URL_RE.search(proc.stdout)
        if not m:
            print(f"  NO URL: {proc.stdout.strip()[-500:]}")
            continue
        req = urllib.request.Request(m.group(0), headers={"User-Agent": "DrawingOffice-POC/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        print(f"  -> {out_path.name} ({len(data):,} bytes)")
