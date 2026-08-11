"""THROWAWAY EPISODE BUILD -- the 2 paid animated inserts (the only real motion
in the whole piece). Camera holds still; only the water/crowd and the rising
man move."""
from __future__ import annotations
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
INSERTS = HERE / "inserts"

JOBS = [
    {
        "name": "insert_a_water_stirs",
        "start_image": INSERTS / "insert_a_source.png",
        "prompt": (
            "Camera holds perfectly still, locked overhead viewpoint, no camera movement at all. "
            "The still rectangular pool of water at the center of frame suddenly disturbs -- "
            "concentric ripples spread out across the water's surface from the center. At the same "
            "moment, the small robed figures sitting on mats at the pool's edges abruptly rise and "
            "surge toward the water in a sudden rush, robes billowing with motion, several figures "
            "reaching the water's edge first, jostling. The stone architecture, the columns, and the "
            "camera framing remain completely static throughout -- only the water and the moving "
            "figures change. Ancient archaeological survey-plate illustration style, muted ink-wash "
            "palette, no text, no modern elements, reverent tone."
        ),
    },
    {
        "name": "insert_b_man_rises",
        "start_image": INSERTS / "insert_b_source.png",
        "prompt": (
            "Camera holds perfectly still, locked overhead viewpoint, no camera movement at all. "
            "The reclining robed figure lying on the woven mat slowly sits up and rises smoothly to "
            "standing in one continuous motion. As he rises, the woven mat beneath him lifts and "
            "rolls itself up in his grip, its shadow swinging upright with him. The standing robed "
            "figure beside him remains completely still and unmoving throughout, watching calmly. "
            "The stone architecture, the distant pool, and the camera framing remain completely "
            "static -- only the rising man and his mat move. Ancient archaeological survey-plate "
            "illustration style, muted ink-wash palette, no text, no modern elements, reverent tone."
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
             "--aspect_ratio", "9:16",
             "--duration", "5",
             "--mode", "pro",
             "--sound", "off",
             "--wait"],
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
        req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible-POC/1.0"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
        out_mp4.write_bytes(data)
        print(f"  -> {out_mp4.name} ({len(data):,} bytes)")
