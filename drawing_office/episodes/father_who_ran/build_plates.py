"""Drawing Office -- The Father Who Ran. 5 new supporting plates, chained
against the proven third_line_02/03 stills as character-consistency refs
(same father: grey hair, brown robe, staff; same son: patched olive tunic).
"""
from __future__ import annotations
import json
import re
import subprocess
import urllib.request
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from pipeline.medium_anchors import SKETCH, build_prompt  # noqa: E402

HF_CLI = r"C:\Users\sanjay\bin\hf.exe"
HERE = Path(__file__).resolve().parent
PLATES_DIR = HERE / "plates"
PLATES_DIR.mkdir(exist_ok=True)

SOURCE_STILLS = Path(r"C:\Users\sanjay\PycharmProjects\JesusInTheBible\poc_bethesda_style_test\round3_devices\stills")
REF_FATHER_SON = SOURCE_STILLS / "third_line_02.png"  # the run -- best ref for both figures
REF_EMBRACE = SOURCE_STILLS / "third_line_03.png"

PLATES = [
    {
        "id": "N1", "stem": "father_watching",
        "subject": (
            "An old bearded man with grey hair, wearing a simple brown robe, "
            "stands alone on a flat rooftop terrace at the edge of a modest "
            "house, one hand raised to shade his eyes, gazing down a long "
            "empty dusty road stretching into the distance. Late warm "
            "afternoon light, his robe stirred by a light wind. Full figure, "
            "seen from behind and slightly to the side."
        ),
        "refs": [REF_FATHER_SON],
    },
    {
        "id": "N2", "stem": "son_rehearsing",
        "subject": (
            "A close view of a young man's shoulders and head, filthy and "
            "gaunt, wearing a torn patched olive tunic, walking with his "
            "head down, mouth slightly open as if quietly rehearsing "
            "words to himself, eyes downcast. Dusty road behind him, warm "
            "late light."
        ),
        "refs": [REF_FATHER_SON],
    },
    {
        "id": "N3", "stem": "running_feet",
        "subject": (
            "An extreme low-angle close view of a man's sandaled feet and "
            "the hem of a brown robe, caught mid-stride on a dusty road, "
            "dust puffing up at the point of contact, the hem hitched up "
            "and swinging. No face visible, ground-level framing only."
        ),
        "refs": [REF_FATHER_SON],
    },
    {
        "id": "N4", "stem": "great_way_off",
        "subject": (
            "A vast, wide view of an empty dusty road stretching from the "
            "foreground into a hazy distant horizon, dry hills on either "
            "side. Far in the distance, one small ragged figure in a torn "
            "olive tunic walks alone along the road, tiny against the "
            "landscape. Warm late-afternoon light, heat haze over the "
            "road."
        ),
        "refs": [REF_FATHER_SON],
    },
    {
        "id": "N5", "stem": "christ_road",
        "subject": (
            "Christ walking steadily along a dusty road toward the "
            "viewer, arms beginning to open slightly at his sides, warm "
            "golden dawn light growing behind him, simple robe, gaunt and "
            "dignified, reverent bearing, full figure, road and dry hills "
            "around him."
        ),
        "refs": [],
    },
]

_URL_RE = re.compile(r"https://\S+?\.(?:png|jpg|jpeg|webp)", re.IGNORECASE)


def generate_one(plate: dict) -> dict:
    out_path = PLATES_DIR / f"{plate['stem']}.png"
    result = {**plate, "ok": False, "error": None}
    if out_path.exists():
        result["ok"] = True
        result["skipped"] = True
        print(f"  [skip] {plate['stem']}.png already exists")
        return result

    prompt = build_prompt(SKETCH, plate["subject"])
    ref_flags = []
    for r in plate["refs"]:
        if Path(r).exists():
            ref_flags += ["--image", str(r)]

    print(f"  [nano_banana_pro] {plate['id']} {plate['stem']}  refs={[Path(r).name for r in plate['refs']]}")
    try:
        proc = subprocess.run(
            [HF_CLI, "generate", "create", "nano_banana_pro",
             "--prompt", prompt, "--aspect_ratio", "9:16", *ref_flags, "--wait"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"hf CLI exit {proc.returncode}: {proc.stderr.strip()[-400:]}")
        m = _URL_RE.search(proc.stdout)
        if not m:
            raise RuntimeError(f"no image URL: {proc.stdout.strip()[-400:]}")
        req = urllib.request.Request(m.group(0), headers={"User-Agent": "DrawingOffice-POC/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            out_path.write_bytes(resp.read())
        print(f"        -> {out_path.name} ({out_path.stat().st_size:,} bytes)")
        result["ok"] = True
    except Exception as e:
        print(f"        FAILED: {e}")
        result["error"] = str(e)
    return result


if __name__ == "__main__":
    results = [generate_one(p) for p in PLATES]
    (HERE / "plates_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
