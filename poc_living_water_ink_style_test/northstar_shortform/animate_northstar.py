"""North-star pattern-lock — animate all 8 shots x 2 aspect ratios.

HF CLI ONLY. Tiering matches the project's locked living-sketchbook split:
Kling for genuine designed/cued motion (a held gaze-then-hold, a spoken line,
real locomotion); veo3_1_lite for atmospheric holds / multi-figure "hold
still" crowd shots. Subtle-localized-motion recipe (camera + baked text
frozen) matches the validated 2026-08-18 Round 6 bake-off, not the unrelated
gallery-tour shorts convention.

Run: .venv\\Scripts\\python.exe animate_northstar.py --shots 1,4 --ratios 9:16,16:9
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import urllib.request
from pathlib import Path

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
_URL_RE = re.compile(r"https://\S+?\.(?:mp4|mov|webm)", re.IGNORECASE)

FROZEN = ("The camera does not move. The top row of the page — the title, the frame "
          "number, and all three small panels with everything drawn inside them — is "
          "a completely static, unchanging picture for the entire clip: not one new "
          "mark, line, color, or letter ever appears anywhere in that row, and nothing "
          "already there ever fades, moves, or changes. Motion happens ONLY inside the "
          "one large lower illustration. No new elements, no invented content, no new "
          "text anywhere on the page.")
NO_MOUTH = ("His lips stay closed and completely still — he is not speaking and his "
            "mouth does not move at all.")

SHOTS = [
    {"n": 1, "label": "wide_the_ask", "model": "veo3_1_lite",
     "motion": "The woman continues her final steps along the path toward the well, "
               "her waterpot swaying gently with her stride; Jesus remains still, "
               "seated, watching her approach. " + FROZEN},
    {"n": 2, "label": "medium_2shot_living_water", "model": "veo3_1_lite",
     "motion": "Only inside the large lower illustration: the single thread of blue "
               "ink drifts and curls very slowly upward from the well's mouth, like "
               "wet ink spreading on paper — it stays thin and stays entirely within "
               "the lower illustration, never reaching up into the panel row above; "
               "Jesus's open hand settles slightly; the woman's expression softens by "
               "a fraction. " + FROZEN},
    {"n": 3, "label": "2shot_breaking_to_singles", "model": "veo3_1_lite",
     "motion": "The small blue watercolor bloom between the two figures pulses very "
               "faintly, spreading a hair further into the paper; both figures hold "
               "their positions, eyes locked. " + FROZEN},
    {"n": 4, "label": "closeup_jesus_five_husbands", "model": "veo3_1_lite",
     "motion": "Jesus's eyes blink once — closing briefly and then opening again fully "
               "— ending with his eyes wide open, steady, and gazing directly at the "
               "viewer, calm and direct. " + NO_MOUTH + " After the single blink "
               "completes with his eyes open, everything holds perfectly still: eyes "
               "open, expression calm, for the rest of the clip. The soft blue threads "
               "near him drift very slightly. " + FROZEN},
    {"n": 5, "label": "compressed_2shot_spirit_truth", "model": "veo3_1_lite",
     "motion": "The pale mountain wash in the background breathes very faintly; the "
               "two figures remain settled and still, the conversation calm. " + FROZEN},
    {"n": 6, "label": "held_single_jesus_i_am_he", "model": "veo3_1_lite",
     "motion": "Jesus's expression stays calm, warm, and completely still throughout "
               "— " + NO_MOUTH + " Only his eyes hold a steady, direct, unwavering "
               "gaze at the viewer, unchanged for the whole clip. The single thin "
               "current of blue-and-gold ink drawn in the still lengthens only "
               "slightly and drifts very slowly outward, like wet ink easing along the "
               "paper — it stays a thin calligraphic line at all times and never "
               "grows into a wide flow, flood, or river; its size at the end of the "
               "clip is barely larger than in the very first frame. " + FROZEN},
    {"n": 7, "label": "wide_moving_she_runs", "model": "kling3_0",
     "motion": "The woman runs down the path in one continuous motion, her robes and "
               "head covering streaming behind her with her stride. Her arms and hands "
               "are empty and swing freely and naturally with her running stride — she "
               "carries nothing in either hand. The waterpot stays exactly where the "
               "still shows it, alone on the well's edge behind her, the whole clip "
               "through. The blue-gold ink threads already trailing from the well in "
               "the still drift a little further along the path with her, staying thin, "
               "delicate calligraphic threads at all times — they never widen into a "
               "broad river, flood, or wash of color; their width and size at the end "
               "of the clip stay close to what they were in the very first frame, only "
               "their length grows slightly. " + FROZEN},
    {"n": 8, "label": "wide_landing_town_arrives", "model": "veo3_1_lite",
     "motion": "The crowd of townspeople continues walking forward at an even, "
               "unhurried pace; Jesus's open arms hold their welcoming gesture; the "
               "diffused blue-and-gold ink threads drift very slowly through the air "
               "of the scene. " + FROZEN},
]


def render_one(shot: dict, ratio: str) -> dict:
    ratio_dir = HERE / ratio.replace(":", "x")
    stem = f"shot{shot['n']:02d}_{shot['label']}"
    src_png = ratio_dir / f"{stem}.png"
    out_path = ratio_dir / f"{stem}.mp4"
    result = {"shot": shot["n"], "label": shot["label"], "ratio": ratio,
              "model": shot["model"], "stem": stem, "ok": False, "error": None, "skipped": False}
    if not src_png.exists():
        result["error"] = f"missing source still: {src_png}"
        print(f"  [skip] {result['error']}")
        return result
    if out_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {ratio}/{stem}.mp4 already exists")
        return result

    cmd = [HF_CLI, "generate", "create", shot["model"], "--prompt", shot["motion"],
           "--start-image", str(src_png), "--aspect_ratio", ratio]
    if shot["model"] == "kling3_0":
        cmd += ["--mode", "pro", "--duration", "5", "--sound", "off"]
    else:  # veo3_1_lite
        cmd += ["--duration", "4"]
    cmd += ["--wait"]

    print(f"  [{shot['model']}] {ratio}/{stem}")
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=900)
    if proc.returncode != 0:
        result["error"] = f"hf CLI exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[-500:]}"
        print(f"        FAILED: {result['error']}")
        return result
    match = _URL_RE.search(proc.stdout)
    if not match:
        result["error"] = f"no video URL in stdout: {proc.stdout.strip()[-500:]}"
        print(f"        FAILED: {result['error']}")
        return result
    url = match.group(0)
    req = urllib.request.Request(url, headers={"User-Agent": "JesusInTheBible-POC/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        out_path.write_bytes(resp.read())
    print(f"        -> {ratio_dir.name}/{out_path.name} ({out_path.stat().st_size:,} bytes)")
    result["ok"] = True
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", default="1,2,3,4,5,6,7,8")
    ap.add_argument("--ratios", default="9:16,16:9")
    args = ap.parse_args()

    wanted = {int(x) for x in args.shots.split(",")}
    ratios = args.ratios.split(",")
    shots = [s for s in SHOTS if s["n"] in wanted]

    results_path = HERE / "animate_results.json"
    results = json.loads(results_path.read_text(encoding="utf-8")) if results_path.exists() else []

    for shot in shots:
        for ratio in ratios:
            r = render_one(shot, ratio)
            results.append(r)
            results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    n_ok = sum(1 for r in results if r["ok"])
    n_fail = sum(1 for r in results if not r["ok"])
    print(f"\nDone. {n_ok} ok, {n_fail} failed. See {results_path}")
