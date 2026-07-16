"""inked_audit.py — Phase 0 of the inked-style migration.

The EW04 POC proved the inked graphic-novel style works, but three accuracy
defects slipped through and were caught ONLY by a human reading the frames:

  - the bronze-serpent pole rendered as a CADUCEUS (snake coiled round the staff),
  - the crucifixion rendered with DAGGER-shaped nails / empty un-pierced hands,
  - a snakebite victim with a literal SNAKE drawn on his neck like a tattoo.

The existing Vision audit (`visual_render.verify_image`) missed all three: it was
hardcoded to judge "Baroque oil painting" tone and had no concept of these
ICONOGRAPHY traps. Phase 0 fixes both halves:

  1. `config.VISUAL_STYLE` now selects the audit's style rubric (inked vs baroque)
     — see config.STYLE_AUDIT_RUBRIC. (done in visual_render._vision_call)
  2. THIS module adds the known-failure-motif checks: each trap pins the CORRECT
     iconography against the WRONG one the model tends to draw, so the auditor is
     told exactly what to look for.

It audits a BARE image (no Scene object needed) so it can run on the EW04 POC
frames today and, in Phase 1, be wired into the production render/animate path.

CLI (proof / ad-hoc):
    .venv\\Scripts\\python.exe -m pipeline.inked_audit <image.png> \\
        --should "the bronze serpent lifted on a pole" --traps caduceus
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import config


# Known iconography traps. Each: what the CORRECT image shows vs the WRONG thing
# the model tends to substitute. Keyed so a scene/object can opt in by name.
# `bad` is the failure the auditor must FAIL on; `good` is the pass condition.
ICONOGRAPHY_TRAPS: dict[str, dict[str, str]] = {
    "caduceus": {
        "subject": "bronze serpent standard (Numbers 21:8)",
        "good": "a SINGLE serpent set ON TOP of / mounted at the summit of a tall, "
                "straight, BARE wooden pole, raised and lifted high like a banner; "
                "the lower shaft is plain bare wood.",
        "bad": "a serpent that SPIRALS, COILS, WINDS or WRAPS AROUND the staff "
               "(a caduceus / the Rod of Asclepius / a medical or pharmacy symbol). "
               "ANY snake twined around the pole is a HARD FAIL.",
    },
    "nails": {
        "subject": "crucifixion nails",
        "good": "iron nails driven THROUGH the hands and THROUGH the feet, each "
                "seen as a small FLAT DARK ROUND nail-head flush against the pierced "
                "flesh with a little blood at the wound.",
        "bad": "DAGGERS, blades, spikes or rods with CROSSGUARDS / handles sticking "
               "out; metal studs decorating the ENDS of the beams; or hands that are "
               "NOT actually pierced (resting on / gripping the wood). Any protruding "
               "blade-like hardware or un-pierced hand is a HARD FAIL.",
    },
    "body_snake": {
        "subject": "snakebite victim",
        "good": "a real BITE WOUND on bare skin — small puncture marks, redness, "
                "bruised swelling.",
        "bad": "a literal SNAKE drawn ON the body/neck (a snake tattoo, or a small "
               "serpent attached to or crawling on the skin). A snake-as-marking on "
               "a person is a HARD FAIL.",
    },
    "roped_wrists": {
        "subject": "crucified wrists",
        "good": "wrists/hands NAILED to the wood (a pierce wound).",
        "bad": "wrists merely BOUND WITH ROPE or cord instead of nailed. Roped-not-"
               "nailed wrists on a crucifixion is a HARD FAIL.",
    },
    "cross_in_water": {
        "subject": "the cross",
        "good": "an UPRIGHT cross.",
        "bad": "a cross whose reflection/orientation reads as an UPSIDE-DOWN / "
               "inverted cross. An inverted-reading cross is a HARD FAIL.",
    },
}


def _trap_block(trap_keys: list[str]) -> str:
    if not trap_keys:
        return ""
    lines = ["\nKNOWN ICONOGRAPHY TRAPS — check each explicitly; any one wrong = passed:false:"]
    for k in trap_keys:
        t = ICONOGRAPHY_TRAPS.get(k)
        if not t:
            raise SystemExit(f"[inked_audit] unknown trap '{k}'. Known: {sorted(ICONOGRAPHY_TRAPS)}")
        lines.append(
            f"  - {t['subject']}:\n"
            f"      CORRECT: {t['good']}\n"
            f"      WRONG (FAIL): {t['bad']}"
        )
    return "\n".join(lines) + "\n"


def build_audit_prompt(should_show: str, trap_keys: list[str], style: str | None = None) -> str:
    """Compose the auditor system prompt: inked style fidelity + the named traps."""
    style = (style or config.VISUAL_STYLE).strip().lower()
    style_rubric = config.STYLE_AUDIT_RUBRIC.get(style, config.STYLE_AUDIT_RUBRIC["graphic_novel"])
    medium = config.STYLE_MEDIUM_PHRASE.get(style, config.STYLE_MEDIUM_PHRASE["graphic_novel"])
    return (
        "You are an INDEPENDENT visual content + iconography auditor for a reverent "
        "Bible-faithful illustration. Audit the attached image against the spec "
        "below. Be strict: a plausible-but-wrong image is a FAIL.\n\n"
        f"WHAT THE IMAGE SHOULD SHOW: {should_show}\n"
        + _trap_block(trap_keys)
        + "\nALSO APPLY:\n"
        + style_rubric
        + "Return ONLY a JSON object (optionally in a ```json fence):\n"
        '{\n'
        '  "passed": true | false,\n'
        '  "issues": [{"claim": "<what was required>", "actual": "<what you see>"}],\n'
        '  "trap_hits": ["<trap key that failed>", ...]\n'
        "}\n"
        f"Pass ONLY when the subject is correct, every iconography trap is on the "
        f"CORRECT side, and the image reads as a {medium}."
    )


def audit_image(image_path: Path, should_show: str, trap_keys: list[str],
                style: str | None = None) -> dict:
    """Run the inked auditor on one image via the local-CLI vision bridge
    (agent_bridge.call_vision) — no metered Anthropic API."""
    from pipeline import agent_bridge, text_engine
    png_bytes = Path(image_path).read_bytes()
    role = build_audit_prompt(should_show, trap_keys, style)
    text = agent_bridge.call_vision(
        role=role, user=f"Audit the attached image: {image_path}",
        image_bytes=png_bytes, media="image/png", model=config.MODEL,
        label=f"inked-audit:{Path(image_path).name}",
    )
    return text_engine._extract_json(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--should", required=True, help="what the image should show")
    ap.add_argument("--traps", default="", help="comma-separated trap keys")
    ap.add_argument("--style", default=None, help="override VISUAL_STYLE (graphic_novel|baroque)")
    ap.add_argument("--print-prompt", action="store_true",
                    help="just print the composed audit prompt (no vision call)")
    a = ap.parse_args()
    traps = [t.strip() for t in a.traps.split(",") if t.strip()]
    if a.print_prompt:
        print(build_audit_prompt(a.should, traps, a.style))
        return
    result = audit_image(Path(a.image), a.should, traps, a.style)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("passed") else 1)


if __name__ == "__main__":
    main()
