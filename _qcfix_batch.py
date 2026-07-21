"""Clip-QC fix batch runner (consumes scratchpad fix_jobs.json; see _QCFIX_PLAN.md).

Two phases, run separately so every Gemini-edited still gets an EYE CHECK before
any roll money is spent on it:
  --edits  : run the Gemini still edits only -> <clips_dir>/_qcfix_test/<slug>_dry.png
  --rolls  : run the seedance re-rolls -> <clips_dir>/_qcfix_test/<slug>.mp4
             (edit jobs roll FROM the _dry.png; roll-only jobs from the original still;
              jobs whose _dry.png is missing or rejected are SKIPPED with a warning)
  --only a,b,c : limit to these slugs (retry lane)
Nothing overwrites an original clip or still; promotion happens after QC.
"""
import argparse
import base64
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import config
from pipeline import cost

JOBS_PATH = Path(r"C:\Users\sanjay\AppData\Local\Temp\claude"
                 r"\C--Users-sanjay-PycharmProjects-JesusInTheBible"
                 r"\82909425-6283-4f57-b9e1-43a682530658\scratchpad\fix_jobs.json")

EP = {"isaiah53": "01_Isaiah_53", "psalm22": "02_Psalm_22",
      "bronze": "04_The_Bronze_Serpent", "two_goats": "EW01_Two_Goats"}


def test_dir(job) -> Path:
    return Path(job["out"]).parent / "_qcfix_test"


def dry_png(job) -> Path:
    return test_dir(job) / f"{job['slug']}_dry.png"


def run_edit(client, genai_types, job) -> bool:
    still = Path(job["still"])
    keep = "; ".join(job["edit"]["keep_list"])
    prompt = (f"{job['edit']['instruction']} Everything else must stay pixel-identical "
              f"to the original — especially keep unchanged: {keep}. Same composition, "
              f"framing, faces, line work, colors, and style.")
    up = client.files.upload(file=str(still), config=genai_types.UploadFileConfig(
        display_name=still.name, mime_type="image/png"))
    resp = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[{"parts": [{"fileData": {"mimeType": "image/png", "fileUri": up.uri}},
                             {"text": prompt}]}],
        config={"responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": job.get("aspect", "16:9")}})
    for p in resp.candidates[0].content.parts:
        if hasattr(p, "inline_data") and p.inline_data and p.inline_data.data:
            data = p.inline_data.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            out = dry_png(job)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            cost.record_nbp(EP[job["lane"]], "long", "still-edit", 1,
                            note=f"{job['slug']} drip-removal (qcfix batch)")
            print(f"[edit] ok  {job['slug']} -> {out}")
            return True
    print(f"[edit] FAIL {job['slug']}: no image bytes")
    return False


def run_roll(job) -> bool:
    src = dry_png(job) if job.get("edit") else Path(job["still"])
    if job.get("edit") and not src.exists():
        print(f"[roll] SKIP {job['slug']}: edited still missing ({src})")
        return False
    out = test_dir(job) / f"{job['slug']}.mp4"
    cmd = [str(config.HF_CLI_PATH), "generate", "create", job["model"],
           "--start-image", str(src), "--prompt", job["prompt"],
           "--duration", job["duration"], "--aspect_ratio", job["aspect"], "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if "nsfw" in blob.lower() or r.returncode != 0 or not m:
        print(f"[roll] FAIL {job['slug']} ({r.returncode}): {blob[-250:]}")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        out.write_bytes(resp.read())
    cost.record_hf(EP[job["lane"]], "long", "clip", job["model"],
                   note=f"{job['slug']} (qcfix batch)")
    print(f"[roll] ok  {job['slug']} -> {out}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edits", action="store_true")
    ap.add_argument("--rolls", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    jobs = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    if a.only:
        keep = {s.strip() for s in a.only.split(",")}
        jobs = [j for j in jobs if j["slug"] in keep]
    ok = fail = 0
    if a.edits:
        from google import genai
        from google.genai import types as genai_types
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        for j in jobs:
            if j.get("edit"):
                (ok, fail) = (ok + 1, fail) if run_edit(client, genai_types, j) else (ok, fail + 1)
    if a.rolls:
        for j in jobs:
            (ok, fail) = (ok + 1, fail) if run_roll(j) else (ok, fail + 1)
    print(f"\n[done] {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
