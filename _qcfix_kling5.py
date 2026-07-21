"""Kling 3.0 pass on the 5 stubborn clip-QC-fix clips that remain in already-
inked episodes (isaiah53/psalm22/bronze) after 2 failed Seedance attempts each.
The 7 EW01 clips from the original 12 are DROPPED here (episode archived to
oil-painting legacy, see longform/EW01_Two_Goats/v1/_archived_oil_baroque/).

Uses the SAME proven frozen-tableau + reframed-camera prompts already written
for these 5 slugs (round-2 retry prompts in _qcfix_state/fix_jobs.json) — only
the ANIMATION MODEL changes, per the project's own locked bake-off finding
(Seedance invents motion on action/multi-figure panels; Kling holds them
frozen). kling3_0, mode=pro, duration=5s (the project's standard Kling
invocation, matches shorts' HF-pro convention and longform/_style_poc's
kling3_0 config). Renders into the SAME _qcfix_test/ dirs as the Seedance
attempts (new file, doesn't clobber the failed Seedance renders — useful for
comparison during QC).
"""
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

STATE = ROOT / "_qcfix_state"
JOBS = {j["slug"]: j for j in json.loads((STATE / "fix_jobs.json").read_text(encoding="utf-8"))}

SLUGS = [
    "nail_through_hand",
    "lots_dice_closeup",
    "07_make_a_fiery_serpent_set_it_on_a_pole",
    "15_hezekiah_breaks_the_brazen_serpent",
    "two_thieves_foreground",
]

EP = {"isaiah53": "01_Isaiah_53", "psalm22": "02_Psalm_22", "bronze": "04_The_Bronze_Serpent"}


def test_dir(job) -> Path:
    return Path(job["out"]).parent / "_qcfix_test"


def src_still(job) -> Path:
    """The dry (drip-removed) still if this job had a Gemini edit, else the original."""
    if job.get("edit"):
        return test_dir(job) / f"{job['slug']}_dry.png"
    return Path(job["still"])


def roll(job) -> bool:
    src = src_still(job)
    if not src.exists():
        print(f"[roll] SKIP {job['slug']}: source still missing ({src})")
        return False
    out = test_dir(job) / f"{job['slug']}_kling.mp4"
    cmd = [str(config.HF_CLI_PATH), "generate", "create", "kling3_0",
           "--start-image", str(src), "--prompt", job["prompt"],
           "--duration", "5", "--aspect_ratio", job["aspect"],
           "--mode", "pro", "--sound", "off", "--wait"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=900)
    blob = (r.stdout or "") + "\n" + (r.stderr or "")
    m = re.search(r"https://\S+?\.mp4", r.stdout or "", re.IGNORECASE)
    if "nsfw" in blob.lower() or r.returncode != 0 or not m:
        print(f"[roll] FAIL {job['slug']} ({r.returncode}): {blob[-300:]}")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(m.group(0), headers={"User-Agent": "JesusInTheBible/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        out.write_bytes(resp.read())
    try:
        cost.record_hf(EP[job["lane"]], "long", "clip", "kling3_0",
                       note=f"{job['slug']} (qcfix Kling pass)")
    except Exception as e:
        print(f"       [cost] ledger row failed (non-fatal): {e}")
    print(f"[roll] ok  {job['slug']} -> {out}")
    return True


def main():
    ok = fail = 0
    for s in SLUGS:
        j = JOBS[s]
        (ok, fail) = (ok + 1, fail) if roll(j) else (ok, fail + 1)
    print(f"\n[done] {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
