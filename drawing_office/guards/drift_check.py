"""Vision guard: did the rendered still actually stay in illustration mode, or
did the image model drift into a photograph of a real physical object/scene?

Encodes failure mode #1 from this week's POC work: prompts using words like
"photograph", "museum artifact", "under glass", "display case" reliably
pulled the image model OUT of illustration mode into full photoreal/
photographed-prop renders — one case even baked an actual legible English
museum placard into the image. `prompt_lint.py` catches the PROMPT before
spend; this catches the RENDERED IMAGE after spend, in case the model drifted
anyway (or the banned lexicon slipped in through a different channel, e.g. an
attached reference).
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # drawing_office/guards -> JesusInTheBible
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from drawing_office.guards._vision_common import vision_call

_ROLE = (
    "You are an independent visual-STYLE auditor for an illustrated Bible-story "
    "pipeline. Every still in this project MUST read as a drawn or painted "
    "illustration -- never a photograph of a real physical object, prop, or "
    "scene. This project has previously shipped prompts (words like "
    "'photograph', 'museum artifact', 'under glass', 'display case') that "
    "reliably pulled the image model OUT of illustration mode into full "
    "photoreal/photographed-prop renders -- one case even baked a real legible "
    "English museum placard into the image. Your ONE job is to catch that "
    "drift before the image ships.\n\n"
    "Answer exactly one question: does this image read as a DRAWN/PAINTED "
    "ILLUSTRATION (ink linework, watercolor/gouache/oil paint, visible "
    "brushwork or penwork, an illustrative rendering style -- any genuinely "
    "hand-crafted-looking medium), or as a PHOTOGRAPH of a real physical "
    "object or scene (photographic lighting and lens characteristics, real-"
    "world material/skin/fabric texture, a studio or museum-style prop shot)?\n\n"
    "Return ONLY a JSON object (optionally inside a ```json fence):\n"
    "{\n"
    '  "verdict": "illustration" | "photograph" | "ambiguous",\n'
    '  "note": "<one or two sentences on what you see that drove the verdict>"\n'
    "}\n"
)


def check_illustration_not_photograph(png_bytes: bytes, label: str = "") -> dict:
    """Ask the vision model whether `png_bytes` reads as a drawn/painted
    illustration or a photograph. Returns:
        {"passed": bool, "verdict": "illustration"|"photograph"|"ambiguous", "note": str}
    FAIL-CLOSED: passed is True ONLY on a clear "illustration" verdict —
    "photograph", "ambiguous", AND any vision-call failure/error all count as
    passed=False (mirrors visual_render.verify_image's fail-closed NEEDS-EYE
    pattern for API-unavailable cases; an audit we could not run, or could not
    get a clear answer from, must never pass)."""
    user_text = (
        f"IMAGE LABEL: {label or '(none given)'}\n\n"
        "Look at the attached image and answer the illustration-vs-photograph "
        "question above."
    )
    try:
        data = vision_call(
            _ROLE, user_text, png_bytes,
            label=f"drift-check:{label or 'unlabeled'}",
        )
    except Exception as e:
        return {
            "passed": False,
            "verdict": "ambiguous",
            "note": f"AUDIT_UNAVAILABLE -- vision call failed, fail-closed: {e}",
        }

    verdict = str(data.get("verdict", "ambiguous")).strip().lower()
    if verdict not in ("illustration", "photograph", "ambiguous"):
        verdict = "ambiguous"
    return {
        "passed": verdict == "illustration",
        "verdict": verdict,
        "note": str(data.get("note", "")),
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        _REPO_ROOT / "poc_bethesda_style_test" / "round3_devices" / "stills" / "sightline_01.png"
    )
    print(f"drift_check smoke test on: {target}")
    if not target.exists():
        print(f"[SKIP] file not found: {target}")
    else:
        result = check_illustration_not_photograph(target.read_bytes(), label=target.stem)
        print(result)
