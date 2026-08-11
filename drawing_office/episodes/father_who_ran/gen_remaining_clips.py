"""The remaining 11 of 13 clips. Slots 5 and 7 (the test gate) already done
and confirmed real motion by eye. Same discipline: subject moves, camera
holds still. Every prompt names a concrete state-change, never a camera verb.
"""
from __future__ import annotations
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PLATES = HERE / "plates"
CROPS = HERE / "crops"
THIRD_LINE = HERE.parents[2] / "poc_bethesda_style_test" / "round3_devices" / "stills"
CLIPS = HERE / "clips"

STYLE_TAIL = (
    " Hand-drawn ink and watercolor illustration style, muted earth tones, "
    "no text, no modern elements, reverent tone."
)

JOBS = [
    {
        "name": "slot1_walk", "model": "seedance1_5", "duration": "8",
        "start_image": THIRD_LINE / "third_line_01.png",
        "prompt": (
            "Camera holds still, no camera movement. The lone ragged figure "
            "trudges forward along the road, legs alternating in a real "
            "walking stride, his torn hem swaying with each step, small "
            "puffs of dust rising at his heels, head down." + STYLE_TAIL
        ),
    },
    {
        "name": "slot2_run_flash", "model": "kling3_0", "mode": "pro", "duration": "5",
        "start_image": CROPS / "run_flash_waist_up.png",
        "prompt": (
            "Camera holds still, no camera movement. The older robed man "
            "surges forward a full running stride toward the viewer, his "
            "robe snapping and billowing behind him, his staff swinging "
            "with the motion, dust bursting up from his feet." + STYLE_TAIL
        ),
    },
    {
        "name": "slot3_watching", "model": "seedance1_5", "duration": "8",
        "start_image": PLATES / "father_watching.png",
        "prompt": (
            "Camera holds still, no camera movement. The old man's robe and "
            "hair stir and lift gently in a real gust of wind, and his head "
            "slowly turns further to one side, gazing intently down the "
            "empty road." + STYLE_TAIL
        ),
    },
    {
        "name": "slot4_feet_pound", "model": "kling3_0", "mode": "pro", "duration": "7",
        "start_image": PLATES / "running_feet.png",
        "prompt": (
            "Camera holds still, no camera movement. The sandaled feet "
            "strike the ground repeatedly in a running stride, the robe "
            "hem hitching and swinging with each footfall, fresh dust "
            "exploding outward from every impact on the dirt road."
            + STYLE_TAIL
        ),
    },
    {
        "name": "slot6_great_way_off", "model": "seedance1_5", "duration": "8",
        "start_image": PLATES / "great_way_off.png",
        "prompt": (
            "Camera holds still, no camera movement. The tiny distant "
            "ragged figure on the road keeps walking forward, visibly "
            "advancing further along the winding road across the shot; "
            "heat shimmer wavers over the distant ground; a small bird "
            "crosses the sky high above." + STYLE_TAIL
        ),
    },
    {
        "name": "slot8_arrival", "model": "kling3_0", "mode": "pro", "duration": "5",
        "start_image": THIRD_LINE / "third_line_03.png",
        "prompt": (
            "Camera holds still, no camera movement. The older man's arms "
            "visibly tighten around the younger man, pulling him closer; "
            "the younger man's face presses further into his shoulder; "
            "both robes settle and shift with the motion; dust that was in "
            "the air drifts and slowly falls to the ground." + STYLE_TAIL
        ),
    },
    {
        "name": "slot9_fists_unclench", "model": "kling3_0", "mode": "pro", "duration": "6",
        "start_image": CROPS / "fists_on_back.png",
        "prompt": (
            "Camera holds still, no camera movement. The clenched fist "
            "pressed against the older man's back slowly opens, fingers "
            "spreading out, then closing again to grip the fabric of his "
            "robe. A small, real, deliberate hand motion." + STYLE_TAIL
        ),
    },
    {
        "name": "slot10_open_hand", "model": "kling3_0", "mode": "pro", "duration": "5",
        "start_image": CROPS / "open_hand.png",
        "prompt": (
            "Camera holds still, no camera movement. The reaching open "
            "hand spreads its fingers further and strains toward the "
            "viewer, the sleeve whipping with the motion, dust streaming "
            "past in the wind of the movement." + STYLE_TAIL
        ),
    },
    {
        "name": "slot11_watcher_becomes_runner", "model": "kling3_0", "mode": "pro", "duration": "5",
        "start_image": CROPS / "watcher_turn.png",
        "prompt": (
            "Camera holds still, no camera movement. The old man's hand "
            "drops from shading his eyes, his robe swirls as his whole "
            "body turns, and he launches forward into the first running "
            "stride, one continuous motion from stillness into a sprint."
            + STYLE_TAIL
        ),
    },
    {
        "name": "slot12_christ_walking", "model": "kling3_0", "mode": "pro", "duration": "6",
        "start_image": PLATES / "christ_road.png",
        "prompt": (
            "Camera holds still, no camera movement. Christ walks forward "
            "at a steady, unhurried, deliberate pace toward the viewer, "
            "his arms slowly beginning to open wider at his sides, warm "
            "golden light gently growing brighter behind him. Calm, "
            "reverent, dignified motion -- no rushing, no distortion."
            + STYLE_TAIL
        ),
    },
    {
        "name": "slot13_landing", "model": "seedance1_5", "duration": "8",
        "start_image": CROPS / "christ_close.png",
        "prompt": (
            "Camera holds still, no camera movement. Christ continues "
            "walking forward slowly and steadily, his robe stirring "
            "gently in the breeze, the warm golden light behind him "
            "slowly breathing and deepening. Calm, reverent, continuous "
            "motion, no rushing." + STYLE_TAIL
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
            cmd += ["--mode", job.get("mode", "pro"), "--sound", "off"]
        else:
            cmd += ["--generate_audio", "false"]
        cmd += ["--wait"]
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=900)
        if proc.returncode != 0:
            print(f"  FAILED: {proc.stderr.strip()[-800:]}")
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
