#!/usr/bin/env python
"""VERIFY layer of the render-quality loop (Phase 2) — catch CONTENT / DOCTRINE / LAYOUT
defects that the pre-flight prompt linter (lint.py) cannot see, because they only appear in
the RENDERED pixels or in the assembled comic PLAN.

Two gates:

  1. content_brief(image, stage, subject, context) -> a structured checklist the reviewer
     (in-chat Agent, since the Anthropic key is dead) applies BY EYE to the rendered still/clip.
     The checklist is built from the llm/regex rules in rules.json for that stage PLUS the
     always-on doctrine/period checks. Record the verdict with write_audit().  This is the gate
     that WOULD have caught the roped fists, the church, the dominoes, the cube-stud nails.

  2. check_comic_spec(spec) -> deterministic ($0) template-variety gate on a motion-comic spec:
     fails an all-'full' slideshow, requires a mix of the layout library, no two adjacent beats
     sharing a template, 'full' only on hero beats.  This is the gate that WOULD have caught the
     13/13-'full' plan that shipped.

  # content audit brief for one still:
  .venv\\Scripts\\python.exe -m render_lint.verify --image <png> --stage still --subject "..."
  # template-variety gate on a comic spec:
  .venv\\Scripts\\python.exe -m render_lint.verify --spec <mocomic.spec.json>
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "rules.json"

# ---- subject taxonomy for the scene-variety gate ----
# every scene in a plan is tagged with exactly one subject_type
CHRIST_TYPES = {"christ_hero", "christ_detail", "christ_risen"}   # Christ IS the dominant subject
CONTEXT_TYPES = {"context_scene", "ot_echo", "human_us", "symbolic"}  # the depth layers
SUBJECT_TYPES = CHRIST_TYPES | CONTEXT_TYPES

# templates that are legitimately single-bleed "hero" layouts
HERO_TEMPLATES = {"full"}
# the full layout vocabulary (keep in sync with comic_engine.TEMPLATES)
ALL_TEMPLATES = {"full", "two_v", "split_v", "stack_h", "big_inset", "triptych_v",
                 "strip_h3", "quad", "hero_frac3", "hero_frac4", "hero_band3"}


def load_rules() -> list[dict]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))["rules"]


# ---------------- gate 1: per-image content / doctrine brief ----------------
# always-on checks (independent of any single rule) — the doctrine + period floor
_ALWAYS = [
    "HANDS: if crucified, are BOTH hands OPEN/flat with a pierced wound in the palm? (NO clenched fist, NO rope binding the wrist)",
    "NAILS: any nail shows as a WOUND/pierced hole, never a proud cube/stud/bolt standing out of the palm",
    "ANACHRONISM: no church, steeple, dome-with-cross, cathedral, or cross-topped building anywhere",
    "LOTS: any gambling pieces are carved animal knucklebones in the dust, NOT dice / dominoes / pip-tiles",
    "PROPS: no free-standing burning candle outdoors, no modern/medieval object",
    "FACE: is this the SAME Christ as the passion panels? (not younger/prettier/idealised on the glory/risen shots)",
    "PERIOD: faces, dress, architecture read ancient Near-Eastern 1st-century — never modern/European/medieval",
    "REVERENCE: God/the Father is never depicted as a figure; tone is holy, not horror or NSFW",
    "TEXT: no gibberish letters / speech bubbles / legible writing baked into the art",
]


def content_brief(stage: str, subject: str, context: str = "") -> dict:
    """Return the checklist to apply by eye to the rendered image."""
    rules = load_rules()
    rule_checks = []
    for r in rules:
        if r.get("check") == "structural":
            continue
        if r.get("stage", "both") not in (stage, "both"):
            continue
        rule_checks.append(f"[{r['severity']}] {r['id']}: {r['message'][:110]}")
    return {"stage": stage, "subject": subject, "context": context,
            "always": _ALWAYS, "rule_checks": rule_checks}


def report_brief(stage: str, subject: str, context: str = "") -> None:
    b = content_brief(stage, subject, context)
    print(f"\n=== CONTENT AUDIT BRIEF ({stage}) ===")
    if context:
        print(f"context: {context}")
    print(f"subject: {subject[:160]}")
    print("\n-- always-on doctrine/period checks --")
    for c in b["always"]:
        print(f"  [ ] {c}")
    print("\n-- rule-derived checks --")
    for c in b["rule_checks"]:
        print(f"  [ ] {c}")
    print("\nApply BY EYE (Read the PNG). Then write_audit() with pass/fail + notes.")


def write_audit(image: Path, verdict: str, flags: list[str], reviewer: str = "in-chat-agent") -> Path:
    """Persist the eyeball verdict beside the image as <stem>.audit.json."""
    image = Path(image)
    side = image.with_suffix(".audit.json")
    side.write_text(json.dumps({
        "image": image.name, "verdict": verdict.upper(),   # PASS | FAIL
        "flags": flags, "reviewer": reviewer, "stage": "content",
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return side


def audit_status(image: Path) -> str | None:
    side = Path(image).with_suffix(".audit.json")
    if side.exists():
        return json.loads(side.read_text(encoding="utf-8")).get("verdict")
    return None


# ---------------- gate 2: comic template-variety (deterministic) ----------------
def check_comic_spec(spec: dict) -> dict:
    """Deterministic template-variety gate. Returns {passed, findings[], stats}."""
    beats = spec.get("beats", spec.get("plan", {}).get("beats", []))
    tpls = [b.get("tpl", "full") for b in beats]
    n = len(tpls)
    findings = []
    distinct = set(tpls)
    full_ct = sum(1 for t in tpls if t in HERO_TEMPLATES)
    grid_ct = n - full_ct

    if n == 0:
        return {"passed": False, "findings": ["spec has no beats"], "stats": {}}
    if grid_ct == 0:
        findings.append(f"BLOCK all {n} beats are '{'/'.join(HERO_TEMPLATES)}' — a slideshow, not a comic; use the template library")
    if len(distinct) < 5:
        findings.append(f"BLOCK only {len(distinct)} distinct templates ({sorted(distinct)}); need >= 5 for a viral/epic comic-page rhythm")
    if full_ct > round(n * 0.4):
        findings.append(f"WARN 'full' on {full_ct}/{n} beats (> ~40%); reserve full for true hero singles")
    for i in range(1, n):
        if tpls[i] == tpls[i - 1] and tpls[i] not in HERO_TEMPLATES:
            findings.append(f"WARN beats {i-1}&{i} share template '{tpls[i]}' (adjacent repeat)")
    unknown = distinct - ALL_TEMPLATES
    if unknown:
        findings.append(f"BLOCK unknown templates {sorted(unknown)} (not in the engine library)")

    passed = not any(f.startswith("BLOCK") for f in findings)
    stats = {"beats": n, "distinct_templates": sorted(distinct),
             "full": full_ct, "grid_or_fracture": grid_ct}
    return {"passed": passed, "findings": findings, "stats": stats}


# ---------------- gate 3: scene SUBJECT variety (deterministic) ----------------
def _scenes_of(plan: dict) -> list[dict]:
    for path in (("scenes",), ("plan", "scenes"), ("final_plan", "scenes")):
        node = plan
        for k in path:
            node = node.get(k, {}) if isinstance(node, dict) else {}
        if isinstance(node, list) and node:
            return node
    return []


def check_scene_subjects(plan: dict) -> dict:
    """Deterministic subject-variety gate — stops a plan that is mostly 'Christ in a pose'.

    Every scene must carry a subject_type (see SUBJECT_TYPES). FAILS (BLOCK) when Christ-centric
    stills dominate (> 60%), when the OT-echo/prophecy layer is missing, or when the context/human
    depth layers are too thin. This is the gate that WOULD have caught the 9/12-Christ-pose plan.
    """
    scenes = _scenes_of(plan)
    n = len(scenes)
    if n == 0:
        return {"passed": False, "findings": ["BLOCK plan has no scenes"], "stats": {}}

    types = [s.get("subject_type", "") for s in scenes]
    unknown = [t for t in types if t not in SUBJECT_TYPES]
    counts = {t: types.count(t) for t in SUBJECT_TYPES}
    christ = sum(counts[t] for t in CHRIST_TYPES)
    non_christ = n - christ
    christ_pct = round(100 * christ / n)

    # longest run of consecutive christ_* scenes
    run = maxrun = 0
    for t in types:
        run = run + 1 if t in CHRIST_TYPES else 0
        maxrun = max(maxrun, run)

    findings = []
    if unknown:
        findings.append(f"BLOCK {len(unknown)} scene(s) missing/invalid subject_type {unknown}; tag each with one of {sorted(SUBJECT_TYPES)}")
    if christ_pct > 60:
        findings.append(f"BLOCK Christ-centric stills are {christ}/{n} ({christ_pct}%) — over the 60% cap; this is 'Jesus in various poses'. Replace pose beats with context_scene / ot_echo / human_us / symbolic stills")
    if non_christ < round(n * 0.4):
        findings.append(f"BLOCK only {non_christ}/{n} context/depth stills (< 40%); the plan does not do justice to the narration's layers")
    if counts["ot_echo"] < 1:
        findings.append("BLOCK no ot_echo scene — the OT prophecy/type layer (e.g. Psalm 22:18 'they cast lots upon my vesture') is missing; every piece traces its thread through Scripture")
    if counts["human_us"] < 1:
        findings.append("WARN no human_us scene — the conviction ('the sin was ours too') has no visual stand-in for the viewer")
    if counts["context_scene"] < 2:
        findings.append(f"WARN only {counts['context_scene']} context_scene still(s); show more of the surrounding event (crowd, executioners, robe)")
    if maxrun > 2:
        findings.append(f"WARN {maxrun} consecutive Christ-centric scenes — break the pose-after-pose run with a context/echo/human beat")

    passed = not any(f.startswith("BLOCK") for f in findings)
    stats = {"scenes": n, "christ_centric": christ, "christ_pct": christ_pct,
             "non_christ": non_christ, "max_consecutive_christ": maxrun,
             "by_type": {t: c for t, c in counts.items() if c}}
    return {"passed": passed, "findings": findings, "stats": stats}


def report_plan(plan_path: Path) -> None:
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    r = check_scene_subjects(plan)
    print(f"\n=== SCENE-SUBJECT VARIETY GATE ({Path(plan_path).name}) ===")
    print(f"stats: {r['stats']}")
    print(f"verdict: {'PASS' if r['passed'] else 'FAIL'}")
    for f in r["findings"]:
        print(f"  - {f}")
    if not r["findings"]:
        print("  clean — rich subject variety, not pose-heavy")


def report_spec(spec_path: Path) -> None:
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    r = check_comic_spec(spec)
    print(f"\n=== TEMPLATE-VARIETY GATE ({Path(spec_path).name}) ===")
    print(f"stats: {r['stats']}")
    print(f"verdict: {'PASS' if r['passed'] else 'FAIL'}")
    for f in r["findings"]:
        print(f"  - {f}")
    if not r["findings"]:
        print("  clean — good template variety")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image"); ap.add_argument("--stage", default="still")
    ap.add_argument("--subject", default=""); ap.add_argument("--context", default="")
    ap.add_argument("--spec")
    ap.add_argument("--plan", help="scene plan JSON -> subject-variety gate")
    a = ap.parse_args()
    if a.plan:
        report_plan(Path(a.plan))
    elif a.spec:
        report_spec(Path(a.spec))
    elif a.image or a.subject:
        report_brief(a.stage, a.subject, a.context)
    else:
        ap.error("pass --plan (subject gate) / --spec (template gate) / --image (content brief)")


if __name__ == "__main__":
    main()
