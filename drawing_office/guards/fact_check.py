"""Vision guard: does a rendered still actually match its registry card's
`accuracy_spec` lines (explicit, Scripture-cited physical facts)?

Encodes failure mode #3 from this week's POC work: one still was supposed to
show a young "lamb without blemish" (Exodus 12:5) and instead rendered a
mature horned ram. Nothing caught it until a human looked. This guard asks
the vision model a real, specific, checkable question per spec line — not a
vague "does this look right" — so a spec like that, run against an image of a
ram when a lamb was specified, would plausibly get flagged.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # drawing_office/guards -> JesusInTheBible
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from drawing_office.guards._vision_common import vision_call

_ROLE = (
    "You are an independent Bible-ACCURACY auditor for an illustrated Bible-"
    "story pipeline. Each rendered still is supposed to match a set of "
    "explicit, Scripture-cited accuracy specs (an exact species, age, count, "
    "or physical detail named in the KJV text). This kind of check has "
    "already caught a real miss on this project: a spec calling for a young "
    "'lamb without blemish' (Exodus 12:5) was rendered as a mature HORNED RAM, "
    "and nothing caught it until a human looked. Your ONE job is to check the "
    "rendered image against EACH spec below as its OWN explicit, checkable "
    "question -- do not wave a spec through because the image looks broadly "
    "plausible; check the SPECIFIC stated detail (species, age/maturity, "
    "count, posture, presence/absence of horns, material, colour, etc).\n\n"
    "For EACH numbered spec, decide PASS or FAIL against what is ACTUALLY "
    "visible in the image, and if FAIL, state exactly what you see instead of "
    "what was specified.\n\n"
    "Return ONLY a JSON object (optionally inside a ```json fence):\n"
    "{\n"
    '  "results": [\n'
    '    {"spec": "<the spec number or a short quote of it>", "passed": true|false, '
    '"issue": "<empty string if passed; otherwise what you actually see vs what '
    'was specified>"},\n'
    "    ...\n"
    "  ],\n"
    '  "note": "<one or two sentences overall>"\n'
    "}\n"
    "Include exactly ONE result object per numbered spec below, in order — do "
    "not skip any, do not merge any."
)


def check_accuracy_specs(png_bytes: bytes, accuracy_specs: list[str]) -> dict:
    """Ask the vision model to verify `png_bytes` against each line of
    `accuracy_specs` as an explicit yes/no question. Returns:
        {"passed": bool, "failures": [{"spec": str, "issue": str}], "note": str}
    FAIL-CLOSED: passed=False if ANY spec fails, if the vision call errors, or
    if the reply is malformed (missing/non-list "results") — a check we
    couldn't run or couldn't parse must never silently pass."""
    if not accuracy_specs:
        return {"passed": True, "failures": [], "note": "no accuracy_specs given -- nothing to check"}

    spec_lines = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(accuracy_specs))
    user_text = (
        "ACCURACY SPECS TO CHECK (one explicit yes/no question per line):\n"
        f"{spec_lines}\n\n"
        "Look at the attached image and check it against every spec above."
    )
    try:
        data = vision_call(_ROLE, user_text, png_bytes, label="fact-check")
    except Exception as e:
        return {
            "passed": False,
            "failures": [
                {"spec": s, "issue": f"AUDIT_UNAVAILABLE -- vision call failed, fail-closed: {e}"}
                for s in accuracy_specs
            ],
            "note": f"AUDIT_UNAVAILABLE -- vision call failed, fail-closed: {e}",
        }

    results = data.get("results")
    failures: list[dict] = []
    if isinstance(results, list) and results:
        for r in results:
            if not isinstance(r, dict) or not r.get("passed", False):
                spec = r.get("spec", "?") if isinstance(r, dict) else "?"
                issue = r.get("issue", "") if isinstance(r, dict) else "malformed result entry"
                failures.append({"spec": str(spec), "issue": str(issue)})
    else:
        # Malformed/empty response shape -- fail closed rather than silently pass.
        failures.append({
            "spec": "(all)",
            "issue": "AUDIT_MALFORMED -- vision reply did not contain a usable results list, fail-closed",
        })

    return {
        "passed": len(failures) == 0,
        "failures": failures,
        "note": str(data.get("note", "")),
    }


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        _REPO_ROOT / "poc_bethesda_style_test" / "round3_devices" / "stills" / "sightline_01.png"
    )
    specs = [
        "The scene shows a crowd of people standing beneath a large tree, viewed from behind.",
        "There is a city gate with arched doorways visible in the background.",
    ]
    print(f"fact_check smoke test on: {target}")
    if not target.exists():
        print(f"[SKIP] file not found: {target}")
    else:
        result = check_accuracy_specs(target.read_bytes(), specs)
        print(result)
