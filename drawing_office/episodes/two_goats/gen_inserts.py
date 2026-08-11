"""Drawing Office POC -- Two Goats paid inserts (the only real motion)."""
from __future__ import annotations
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "primitives"))
from crop_study import camera_crop  # noqa: E402
from PIL import Image

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
INSERTS = HERE / "inserts"
INSERTS.mkdir(exist_ok=True)

# Insert A source: crop tight on the right (warm/departing) goat + open ground.
goats = Image.open(PLATES / "two_goats.png")
crop_a = camera_crop(goats, cx_frac=0.72, cy_frac=0.55, zoom=1.6)
crop_a.save(INSERTS / "insert_a_source.png")
print(f"[ok] insert_a_source.png {crop_a.size}")

JOBS = [
    {
        "name": "insert_a_goat_departs",
        "start_image": INSERTS / "insert_a_source.png",
        "prompt": (
            "Camera holds perfectly still, no camera movement at all. The "
            "goat turns its body fully away from the viewer and walks "
            "steadily forward into the open ground and distant hills "
            "beyond, moving away and growing smaller, dust lifting softly "
            "at its hooves. The landscape and the camera framing remain "
            "completely static -- only the goat moves, receding into the "
            "distance. Hand-drawn ink and watercolor illustration style, "
            "muted earth tones, no text, no modern elements, reverent tone."
        ),
    },
    {
        "name": "insert_b_veil_tears",
        "start_image": PLATES / "veil.png",
        "prompt": (
            "Camera holds perfectly still, no camera movement at all. The "
            "heavy woven curtain tears suddenly from top to bottom in one "
            "continuous rip down its center, the two halves pulling apart "
            "and swinging slightly outward, bright light spilling through "
            "the widening gap between them. The stone archway, the oil "
            "lamp, and the camera framing remain completely static -- only "
            "the curtain tears and the light grows. Hand-drawn ink and "
            "watercolor illustration style, muted earth tones, no text, no "
            "modern elements, reverent tone."
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

if __name__ == "__main__":
    for job in JOBS:
        out_mp4 = INSERTS / f"{job['name']}.mp4"
        if out_mp4.exists():
            print(f"[skip] {out_mp4.name} already exists")
            continue
        print(f"[kling3_0 pro] {job['name']} ...")
        proc = subprocess.run(
            [HF_CLI, "generate", "create", "kling3_0",
             "--start-image", str(job["start_image"]),
             "--prompt", job["prompt"],
             "--aspect_ratio", "9:16", "--duration", "5",
             "--mode", "pro", "--sound", "off", "--wait"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
        )
        if proc.returncode != 0:
            print(f"  FAILED: {proc.stderr.strip()[-800:]}")
            print(f"  stdout tail: {proc.stdout.strip()[-800:]}")
            continue
        m = _URL_RE.search(proc.stdout)
        if not m:
            print(f"  NO VIDEO URL: {proc.stdout.strip()[-800:]}")
            continue
        req = urllib.request.Request(m.group(0), headers={"User-Agent": "DrawingOffice-POC/1.0"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
        out_mp4.write_bytes(data)
        print(f"  -> {out_mp4.name} ({len(data):,} bytes)")
