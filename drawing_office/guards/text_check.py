"""Vision guard: is there ANY legible text, word, or numeral visible anywhere
in a rendered still?

This project's own standing rule (see CLAUDE.md "sketchbook-controlled-text-
overlay" / marginalia skill): text is composited by code AFTERWARD, never AI-
rendered — an image model told "no lettering" in the prompt still reliably
produces garbled or even accidentally legible lettering (signage, scrolls,
placards, inscriptions, book pages). This guard is the after-the-fact catch.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # drawing_office/guards -> JesusInTheBible
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from drawing_office.guards._vision_common import vision_call

_ROLE = (
    "You are an independent visual-content auditor for an illustrated Bible-"
    "story pipeline. This project's standing rule: NO text, words, letters, or "
    "numerals may be rendered by the image model -- every caption and verse "
    "card is composited by code AFTERWARD, as a separate overlay layer. An "
    "image model asked to 'not include text' still reliably generates garbled "
    "or even accidentally legible lettering (signage, labels, book pages, "
    "placards, carved inscriptions). Your ONE job is to catch ANY legible "
    "text anywhere in the frame before the image ships.\n\n"
    "Scan the ENTIRE image -- including small background details, signage, "
    "scrolls, book/journal pages, carved inscriptions, banners, clothing, and "
    "any object with markings -- for anything a human could read as a letter, "
    "word, or numeral, in ANY language or script, whether fully legible or "
    "only partially/nearly legible.\n\n"
    "Return ONLY a JSON object (optionally inside a ```json fence):\n"
    "{\n"
    '  "legible_text_found": ["<what you see + a short location note, e.g. '
    '\'faint cursive writing, upper-left margin\'>", ...],\n'
    '  "note": "<one or two sentences>"\n'
    "}\n"
    "Return an empty list only if you find NOTHING readable anywhere. When in "
    "doubt about whether marks are legible text vs abstract texture/scribble, "
    "ERR ON THE SIDE OF FLAGGING IT."
)


def check_no_legible_text(png_bytes: bytes) -> dict:
    """Ask the vision model whether ANY legible text/words/numerals are
    visible anywhere in `png_bytes`. Returns:
        {"passed": bool, "legible_text_found": [...], "note": str}
    FAIL-CLOSED: passed=False if any text is flagged OR the vision call itself
    fails/errors (never silently pass on an API failure)."""
    user_text = "Look at the attached image and scan it for any legible text per the rule above."
    try:
        data = vision_call(_ROLE, user_text, png_bytes, label="text-check")
    except Exception as e:
        return {
            "passed": False,
            "legible_text_found": [],
            "note": f"AUDIT_UNAVAILABLE -- vision call failed, fail-closed: {e}",
        }

    found = data.get("legible_text_found", [])
    if not isinstance(found, list):
        found = [str(found)] if found else []
    return {
        "passed": len(found) == 0,
        "legible_text_found": found,
        "note": str(data.get("note", "")),
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        _REPO_ROOT / "poc_bethesda_style_test" / "round3_devices" / "stills" / "sightline_01.png"
    )
    print(f"text_check smoke test on: {target}")
    if not target.exists():
        print(f"[SKIP] file not found: {target}")
    else:
        result = check_no_legible_text(target.read_bytes())
        print(result)
