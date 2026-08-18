"""THROWAWAY POC — NOT part of the production pipeline.

Image-to-video bake-off: one whole ink-storyboard-page still, animated across
several Higgsfield i2v models, to see which handles this complex multi-panel
composition best (frozen text, subtle localized motion, no hallucination).

Run: .venv\\Scripts\\python.exe poc_living_water_ink_style_test\\bakeoff\\run_bakeoff.py
"""
from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
SRC_IMAGE = HERE.parent / "raw_prompt_test" / "user_prompt_16x9_directgemini_newkey.png"
OUT_DIR = HERE / "clips"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "The camera is completely locked, frozen, no zoom, no pan, no camera movement at all. "
    "This is a hand-drawn ink-and-watercolor storyboard page on aged paper coming subtly "
    "alive, like a living illustration, not a video pan. All handwritten text, titles, "
    "frame numbers, and labels stay perfectly still, sharp, and unchanged the entire time - "
    "never morph, warp, or melt the lettering. The paper itself stays still. "
    "Only small, localized, restrained motion: the blue and gold ink swirls drift and curl "
    "gently, like wet ink spreading slowly across paper. In the large lower scene, the "
    "seated man's open hand moves in a small, slow, calm gesture as he speaks, and the "
    "standing woman's robe sways very slightly; both blink softly. In the top-right small "
    "panel, the running woman's stride continues forward slightly, her jar and robe in "
    "gentle motion. In the top-left small panel, the man's portrait breathes softly, a slow "
    "blink, the faint halo lines drift almost imperceptibly. The town panel stays almost "
    "entirely still, just a hint of atmospheric haze. Nothing new appears, no extra figures, "
    "no invented objects, the composition and every character's identity stay exactly as "
    "drawn."
)

# Already submitted (debugging the --json response shape) — reuse instead of
# re-spending on a duplicate job.
ALREADY_SUBMITTED = {
    "veo3_1_lite": "7c129375-fc5e-49df-80d0-7587d0a82504",
}

# (job_type, extra hf CLI params)
MODELS = [
    ("kling3_0", ["--mode", "pro", "--duration", "5", "--sound", "off"]),
    ("kling3_0_turbo", ["--duration", "5"]),
    ("seedance1_5", ["--resolution", "720p", "--duration", "4", "--generate_audio", "false"]),
    ("seedance_2_5", ["--duration", "4", "--mode", "omni_reference"]),
    ("veo3_1_lite", ["--duration", "4"]),
    ("veo3_1", ["--duration", "4"]),
    ("wan2_7", ["--duration", "5"]),
]


def submit(model: str, extra: list[str]) -> dict:
    args = [HF_CLI, "generate", "create", model,
            "--prompt", PROMPT,
            "--image", str(SRC_IMAGE),
            "--aspect_ratio", "16:9",
            "--json"] + extra
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    if proc.returncode != 0:
        return {"model": model, "ok": False, "error": (proc.stderr or proc.stdout).strip()[-500:]}
    try:
        data = json.loads(proc.stdout)
        job_id = data[0] if isinstance(data, list) else data.get("id")
    except Exception as e:
        return {"model": model, "ok": False, "error": f"parse error: {e}: {proc.stdout[-300:]}"}
    return {"model": model, "ok": True, "id": job_id}


def poll_all(jobs: list[dict], timeout_s: int = 900) -> list[dict]:
    """Round-robin poll every pending job so they finish in wall-clock
    parallel instead of one-at-a-time serial waits."""
    pending = [j for j in jobs if j.get("ok")]
    done = [j for j in jobs if not j.get("ok")]
    start = time.time()
    while pending and time.time() - start < timeout_s:
        still_pending = []
        for job in pending:
            proc = subprocess.run([HF_CLI, "generate", "get", job["id"], "--json"],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
            try:
                data = json.loads(proc.stdout)
            except Exception:
                still_pending.append(job)
                continue
            status = data.get("status")
            if status == "completed":
                job["ok"] = True
                job["result_url"] = data.get("result_url")
                done.append(job)
                print(f"  {job['model']}: completed")
            elif status == "failed":
                job["ok"] = False
                job["error"] = "job failed"
                done.append(job)
                print(f"  {job['model']}: FAILED")
            else:
                still_pending.append(job)
        pending = still_pending
        if pending:
            time.sleep(10)
    for job in pending:
        job["ok"] = False
        job["error"] = "timeout"
        done.append(job)
    return done


def download(job: dict) -> dict:
    if not job.get("ok") or not job.get("result_url"):
        return job
    out_path = OUT_DIR / f"{job['model']}.mp4"
    try:
        req = urllib.request.Request(job["result_url"], headers={"User-Agent": "JesusInTheBible-POC/1.0"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            out_path.write_bytes(resp.read())
        job["path"] = str(out_path)
        job["bytes"] = out_path.stat().st_size
    except Exception as e:
        job["ok"] = False
        job["error"] = f"download failed: {e}"
    return job


if __name__ == "__main__":
    print(f"Source: {SRC_IMAGE}")
    print("Submitting jobs (skipping models already downloaded)...")
    jobs = []
    for m, extra in MODELS:
        if (OUT_DIR / f"{m}.mp4").exists():
            print(f"  {m}: already downloaded, skipping")
            continue
        if m in ALREADY_SUBMITTED:
            jobs.append({"model": m, "ok": True, "id": ALREADY_SUBMITTED[m]})
        else:
            jobs.append(submit(m, extra))
    for j in jobs:
        print(f"  {j['model']}: {'submitted ' + j.get('id', '') if j['ok'] else 'FAILED: ' + j.get('error', '')}")

    print("\nPolling until all complete (round-robin)...")
    results = poll_all(jobs)
    print("\nDownloading completed clips...")
    results = [download(r) for r in results]
    for r in results:
        status = "OK" if r["ok"] else f"FAILED: {r.get('error')}"
        print(f"  {r['model']}: {status}")

    (HERE / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for r in results if r["ok"])
    print(f"\n{ok}/{len(results)} succeeded.")
