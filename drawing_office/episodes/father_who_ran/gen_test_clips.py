"""Test gate: the 2 hardest clips first, per Fable's own recommendation.
Slot 7 (Kling, the hero run -- two figures, real action) and slot 5
(Seedance, the son rehearsing -- calm single figure, face-identity risk)."""
from __future__ import annotations
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
THIRD_LINE = HERE.parents[2] / "poc_bethesda_style_test" / "round3_devices" / "stills"
CLIPS = HERE / "clips"
CLIPS.mkdir(exist_ok=True)

STYLE_TAIL = (
    " Hand-drawn ink and watercolor illustration style, muted earth tones, "
    "no text, no modern elements, reverent tone."
)

JOBS = [
    {
        "name": "slot7_the_run", "model": "kling3_0", "mode": "pro", "duration": "5",
        "start_image": THIRD_LINE / "third_line_02.png",
        "prompt": (
            "Camera holds still, no camera movement. The older robed man "
            "with grey hair continues running forward down the dusty road "
            "toward the smaller ragged figure ahead of him, his robe "
            "streaming and snapping behind him, staff swinging, dust "
            "rolling up from his sandals with each stride, his arms already "
            "reaching forward. The gap between the two figures visibly "
            "closes as he runs -- he gets noticeably nearer across the "
            "shot. The smaller figure's arms lift higher in response."
            + STYLE_TAIL
        ),
    },
    {
        "name": "slot5_rehearsing", "model": "seedance1_5", "duration": "8",
        "start_image": PLATES / "son_rehearsing.png",
        "prompt": (
            "Camera holds still, no camera movement. The young man walks "
            "forward slowly along the road, head bowed, his lips moving "
            "silently as if quietly rehearsing words to himself, small "
            "gestures of his downcast eyes, his shoulders shifting gently "
            "with each slow step. Dust drifts faintly at his feet."
            + STYLE_TAIL
        ),
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

if __name__ == "__main__":
    for job in JOBS:
        out_mp4 = CLIPS / f"{job['name']}.mp4"
        if out_mp4.exists():
            print(f"[skip] {out_mp4.name}")
            continue
        print(f"[{job['model']}] {job['name']} ...")
        cmd = [HF_CLI, "generate", "create", job["model"],
               "--start-image", str(job["start_image"]),
               "--prompt", job["prompt"],
               "--aspect_ratio", "9:16", "--duration", job["duration"]]
        if job["model"] == "kling3_0":
            cmd += ["--mode", job["mode"], "--sound", "off"]
        else:
            cmd += ["--generate_audio", "false"]
        cmd += ["--wait"]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=900)
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
