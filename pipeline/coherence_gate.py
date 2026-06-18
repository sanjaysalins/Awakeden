"""IMG-COHERENT vision gate (step 2) — the body-plausibility judgement.

The deterministic scaffolding lives in `pipeline/coherence.py` (sidecar + fail-closed
is_verified). THIS module is the LOOK: a single BLIND vision pass that flags a CLEAR F1-F5
defect and DEFAULTS TO PASS, recording the verdict through coherence.record_verdict.

Canonical fail classes (the live, calibrated gate — see v2/SPEC.md §5 INV-23):
  F1 modern/anachronism · F2 frame/border/split-screen · F3 broken face/grotesque expression ·
  F4 impossible anatomy (floating head/limb, through-object, giant head) · F5 dominant garbled text.
Suffering-Christ traits (gaunt/sorrowful/upward-gaze, upright crucifixion, background scrolls) PASS.

This default-PASS posture REPLACED an earlier over-strict C1-C7 "when unsure FAIL" design after
calibration showed it over-rejected good Baroque art (precision 0.08 -> 0.50). The k-vote,
hash-pooled `coherence.aggregate` ensemble is the BULK re-audit / determinism tool, not this look.
"""
from __future__ import annotations
import json
from pathlib import Path

from pipeline import coherence

# Shared JSON contract — keep in lockstep with the Workflow's inline schema.
# Canonical fail classes are F1-F5 (the LIVE default-pass gate); the old C1-C7 body sub-axis is
# retired (it belonged to the over-strict design the calibration replaced).
COHERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "f1_modern_ok": {"type": "boolean"},
        "f2_frame_ok": {"type": "boolean"},
        "f3_face_ok": {"type": "boolean"},
        "f4_anatomy_ok": {"type": "boolean"},
        "f5_text_ok": {"type": "boolean"},
        "worst_region": {"type": "string",
                         "description": "the single worst defect region, or NONE"},
        "passed": {"type": "boolean"},
        "fail_reasons": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["f1_modern_ok", "f2_frame_ok", "f3_face_ok", "f4_anatomy_ok", "f5_text_ok",
                 "worst_region", "passed", "fail_reasons"],
}

ROLE = (
    "You are a quality auditor for devotional Baroque oil paintings. Flag a still as NOT FIT FOR "
    "USE ONLY for a CLEAR, OBVIOUS defect — a glaring AI-render failure a viewer would notice at "
    "a glance. You are NOT judging art taste or theology. You do NOT get the scene description "
    "(blind). DEFAULT TO PASS: when in doubt, PASS. Only fail on an unmistakable defect below.\n\n"
    "These suffering-Christ traits are INTENTIONAL and must PASS (do NOT fail them):\n"
    "  - a gaunt, sunken, hollow-eyed, sorrowful, weeping, or anguished face; eyes gazing UP or "
    "half-closed in agony (Man of Sorrows — this is the point, not a defect);\n"
    "  - an upright crucifixion with feet resting on a ledge/suppedaneum and arms along the beam "
    "(standard crucifixion iconography — NOT 'standing instead of hanging');\n"
    "  - a scroll/parchment/book carrying script or even garbled lettering IN a scene (writing is "
    "handled elsewhere; a background scroll is NOT a bad still);\n"
    "  - dark/dramatic chiaroscuro, shadow-dissolved background figures, blood, wounds, dirt.\n\n"
    "FAIL (passed:false) ONLY for one of these CLEAR defects:\n"
    "F1 MODERN/ANACHRONISM: an obviously modern or out-of-period object, garment, hairstyle, "
    "flag/banner, or item in an ancient scene; a glossy modern photo-portrait look.\n"
    "F2 FRAME/BORDER: a painted picture-frame, wooden border, canvas edge, triptych side-panel, "
    "or split-screen around the image (it must be full-bleed).\n"
    "F3 BROKEN FACE: a clearly melted/warped/asymmetric face, two faces merged, eyes that are "
    "plainly malformed (not merely looking up/away), or a grotesque/leering/unsettling SMILE on "
    "a reverent subject.\n"
    "F4 IMPOSSIBLE ANATOMY: a detached/FLOATING head or limb, a limb passing THROUGH a solid "
    "object, a giant-head/tiny-body proportion, an extra/missing limb, or an obviously malformed "
    "hand (wrong finger count on a prominent hand).\n"
    "F5 DOMINANT GARBLED TEXT: large gibberish lettering that DOMINATES the image as its subject "
    "(not a small background scroll).\n\n"
    "FIRST adversarially LOCALIZE the single worst region; if it is not a CLEAR F1-F5 defect, "
    "PASS. Return ONLY the JSON."
)


def build_user(scene=None) -> str:
    # Blind by default (no subject_block) to preserve the default-PASS, no-prior posture.
    return ("Audit the attached painting for a CLEAR F1-F5 defect (default to PASS). "
            "Localize the worst region first, then fill the schema. Be specific in fail_reasons "
            "(which F#, which figure, what you actually see).")


def verdict_to_sidecar_args(data: dict) -> dict:
    """Map a vision verdict dict -> coherence.record_verdict kwargs (F1-F5)."""
    passes = {
        "f1": data.get("f1_modern_ok"), "f2": data.get("f2_frame_ok"),
        "f3": data.get("f3_face_ok"), "f4": data.get("f4_anatomy_ok"),
        "f5": data.get("f5_text_ok"), "worst_region": data.get("worst_region"),
    }
    return {"audited": True, "passed": bool(data.get("passed")),
            "passes": passes, "fail_reasons": data.get("fail_reasons") or []}


def audit_still(png_path: Path, scene=None, log=print) -> dict:
    """Run the vision look on one still and record its coherence sidecar. Returns the verdict.
    On an Anthropic usage cap, records audited=False (UNVERIFIED) — never a fake pass."""
    from pipeline import config, text_engine
    png_path = Path(png_path)
    png_bytes = png_path.read_bytes()
    try:
        if config.agent_mode():
            from pipeline import agent_bridge
            text = agent_bridge.call_vision(
                role=ROLE, user=build_user(scene), image_bytes=png_bytes, media="image/png",
                model=config.MODEL, label=f"coherence:{png_path.name}")
            data = text_engine._extract_json(text)
        else:
            import base64
            client = text_engine._client()
            resp = client.messages.create(
                model=config.MODEL, max_tokens=1500, thinking={"type": "adaptive"}, system=ROLE,
                messages=[{"role": "user", "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                  "data": base64.b64encode(png_bytes).decode("ascii")}},
                    {"type": "text", "text": build_user(scene)}]}])
            data = text_engine._extract_json("".join(b.text for b in resp.content if b.type == "text"))
    except Exception as e:  # noqa
        if any(s in str(e).lower() for s in ("usage limit", "usage limits", "regain access")):
            coherence.record_verdict(png_path, audited=False, passed=False,
                                     note="audit skipped (Anthropic usage cap)")
            log(f"      ! coherence SKIPPED (usage cap) — {png_path.name}")
            return {"audited": False, "passed": False}
        raise
    coherence.record_verdict(png_path, **verdict_to_sidecar_args(data))
    log(f"      coherence {'PASS' if data.get('passed') else 'FAIL'} — {png_path.name}"
        + ("" if data.get("passed") else f"  ({'; '.join(data.get('fail_reasons') or [])})"))
    return data


if __name__ == "__main__":
    import sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: python -m pipeline.coherence_gate <short folder|png> ...")
        raise SystemExit(2)
    targets: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            targets += sorted((p / "visual" / "nbp").glob("*.png"))
        elif p.suffix == ".png":
            targets.append(p)
    for png in targets:
        audit_still(png)
    print(f"\naudited {len(targets)} still(s).")
