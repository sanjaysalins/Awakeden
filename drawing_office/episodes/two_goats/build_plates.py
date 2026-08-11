"""Drawing Office POC -- Two Goats, "the_undivided" device.
3 paid plates per commission.json's plate_bill. P3 chains P2 as an --image
reference (palette/mood continuity) rather than an independent unguided
generation, per commission.json's risk_reconciliation note.
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

PLATES = [
    {
        "id": "P1", "stem": "veil",
        "subject": (
            "A heavy woven curtain hanging across a wide stone doorway, seen "
            "from an outer courtyard: a cherubim-figured pattern faintly "
            "worked into the weave, rich blue, purple and scarlet threads "
            "through fine linen, warm oil-lamp light catching the near "
            "threshold and the curtain's near folds, deep unlit shadow "
            "beyond the curtain into the inner sanctuary. No figures "
            "present. Full-height vertical composition, the curtain filling "
            "the frame."
        ),
        "refs": [],
    },
    {
        "id": "P2", "stem": "two_goats",
        "subject": (
            "Two ordinary domestic goats standing together at one moment of "
            "division, full bodies visible: on the left, one goat stands "
            "calm and entirely still beside a low stone altar; on the "
            "right, the other goat has begun turning its body away, "
            "oriented toward open ground and a wide horizon. A priest's two "
            "hands rest gently on both animals at once, one hand on each, "
            "connecting them across the center of the frame. Behind on the "
            "left, a suggestion of a shadowed sanctuary interior and a "
            "glimpse of a woven curtain; behind on the right, a suggestion "
            "of open wilderness ground and sky. One continuous, "
            "unified composition, not two separate scenes."
        ),
        "refs": [],
    },
    {
        "id": "P3", "stem": "christ",
        "subject": (
            "Christ bearing a great unseen weight upon His shoulders, head "
            "bowed low, gaunt and sorrowful, a marred and suffering visage, "
            "standing alone, full figure, robed simply. The sky and ground "
            "behind Him shift gently from a deep shadowed blue-grey on one "
            "side of the frame to a warm dust-gold on the other side, "
            "echoing a threshold being crossed within one figure. Reverent, "
            "still, dignified, not idealized or heroic in build -- worn and "
            "human."
        ),
        "refs": ["two_goats.png"],  # palette/mood continuity, not alignment
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
        rp = PLATES_DIR / r
        if rp.exists():
            ref_flags += ["--image", str(rp)]

    print(f"  [nano_banana_pro] {plate['id']} {plate['stem']}  refs={plate['refs']}")
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
    results = []
    for plate in PLATES:
        results.append(generate_one(plate))
    (HERE / "plates_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
