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

  1b. FAIL-CLOSED ship gate (gate_dir / worklist) — the piece-level authority on shippability.
     A piece is GREEN only if EVERY production still has a PASS audit sidecar. A MISSING sidecar
     is BLOCKED (unaudited), a FAIL/SKIPPED sidecar is BLOCKED. It never passes by default — the
     opposite of the old pipeline behaviour that PASSED a still when the (now-dead) vision API
     could not be reached. That fail-OPEN is why 84 bad stills shipped with 0 audit sidecars.
     Wiring (the required batch-Agent step):
        a) render a piece's stills (through render_grounded, not a bespoke script)
        b)  --worklist <dir>   -> the batch of stills needing audit + the checklist
        c) spawn a vision Agent that READS each PNG, applies the checklist, and records a
           verdict per still:  --record <png> --verdict PASS|FAIL --flags "..."
        d)  --gate <dir>       -> exits 0 only when every still is PASS; a renderer/skill must
           refuse to call a piece "done" (animate/assemble) until this is 0.

  2. check_comic_spec(spec) -> deterministic ($0) template-variety gate on a motion-comic spec:
     fails an all-'full' slideshow, requires a mix of the layout library, no two adjacent beats
     sharing a template, 'full' only on hero beats.  This is the gate that WOULD have caught the
     13/13-'full' plan that shipped.

  # content audit brief for one still:
  .venv\\Scripts\\python.exe -m render_lint.verify --image <png> --stage still --subject "..."
  # FAIL-CLOSED ship gate for a whole piece's stills (exit 1 until every still is PASS):
  .venv\\Scripts\\python.exe -m render_lint.verify --gate <visual_dir>
  # the batch a vision Agent must audit to turn the gate green:
  .venv\\Scripts\\python.exe -m render_lint.verify --worklist <visual_dir>
  # record one still's eyeball verdict:
  .venv\\Scripts\\python.exe -m render_lint.verify --record <png> --verdict PASS|FAIL --flags "note; note"
  # template-variety gate on a comic spec:
  .venv\\Scripts\\python.exe -m render_lint.verify --spec <mocomic.spec.json>
"""
from __future__ import annotations
import argparse, json, re, sys
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
# always-on checks (independent of any single rule) — the doctrine + period floor.
# Every entry is a defect CLASS actually observed in the 2026-07-04 corpus red-team (84 flawed
# stills). Phrased so a vision reviewer answers each with a clear yes/no on the pixels.
_ALWAYS = [
    "NAILS-THROUGH: every crucifixion nail passes THROUGH the hand/foot into the wood — never lying flat ACROSS the palm, gripped in the fingers, or floating on TOP of the beam",
    "WOUND-IS-A-HOLE: each nail wound is a torn pierced HOLE (risen = a round healed scar), never a flat disc / communion-wafer / patch / stud / button / thin slash / X-stitch on the skin",
    "HANDS-OPEN: if crucified, BOTH hands are OPEN/flat, no clenched fist, no rope binding the wrist; count fingers — exactly five per hand, no sixth digit, no fused mitten",
    "ONE-FIXING-METHOD: the SAME body is fixed one way — either nailed OR roped, never nailed on one hand and rope-lashed on the other wrist/feet",
    "LAMP-NOT-CANDLE: any light source is a low clay oil lamp (flame at a pinched side spout), NOT a wax candle, a candle-in-a-bowl, a glass-chimney hurricane/kerosene lantern, or a carriage lantern",
    "SKYLINE: no church / steeple / cross-topped building / Byzantine or golden ONION dome (Dome of the Rock) / minaret / pointed-Gothic arch / leaded diamond-lattice glass / medieval castellated battlement / Greek-Parthenon colonnade+pediment anywhere in the scene",
    "TEXT-FREE: no legible or semi-legible writing baked in — no pseudo-Hebrew / pseudo-Latin gibberish on scrolls, coins, a titulus/sign, or building walls; surfaces read as blank or illegible marks",
    "NO-LOGO: no modern brand / pop-culture emblem embossed on any prop — coins carry a worn ancient head (Tyrian-shekel), NEVER a Batman bat-wing, star, or corporate mark",
    "NO-MODERN-OBJECT: no closed modern shoe/loafer (feet wear open leather sandals), sports/athletic tape, wristwatch, eyeglasses, bench-vise/screw-clamp, telegraph/utility pole or strung wire",
    "LOTS-AND-BONES: gambling lots + any scattered 'bones' are carved knucklebone astragali / realistic bones — NEVER dice, dominoes, pip-tiles, or cartoon double-knobbed dog-treat bones",
    "STRIPPED-VICTIM: a crucified figure (Christ or a thief) is stripped to a loincloth — no ornate embroidered robe, gold-trim cuffs, or jewellery on the body",
    "ONE-CHRIST: there is exactly ONE Christ figure and He is the subject — NO second Christ-lookalike (white robe, long hair, beard) standing among the mourner / 'us' / crowd figures",
    "NO-CLONED-FACES: a crowd is distinct people (vary age/build/hair/features) — not the same face repeated, and no faceless void/blob figure at a focal point",
    "HOUSE-STYLE: rendered in THIS project's inked graphic-novel line art — NOT anime/cel-shade, ukiyo-e / Hokusai wave, watercolour, photoreal, or soft painterly Baroque; it must match its sibling stills, not read as a different artist",
    "CROSS-CONTINUITY: within a piece the crucified Christ is consistent — crown of thorns PRESENT on every cross frame (never crowned in one cut and bare-headed in the next); the central cross is NOT empty during beats where He hangs (lots / mocking / darkness)",
    "FACE-CONSISTENT: this is the SAME Christ as the passion panels (not younger/prettier/idealised on the glory/risen shots)",
    "PERIOD: faces, dress, architecture read ancient Near-Eastern 1st-century — never modern/European/medieval; David is an ancient Hebrew, not a medieval-European peasant",
    "REVERENCE: God/the Father is never depicted as a figure; tone is holy, not horror or NSFW",
    "ANATOMY: no extra/duplicated limb, no praying-hands pressed to the chest on a figure whose arms are nailed outstretched, no disembodied hand/arm",
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


# ---------------- gate 1b: FAIL-CLOSED piece-level ship gate ----------------
# Skip non-production PNGs: refs, char/world anchors, probes, bake-offs, work/preview dirs,
# and any underscored helper (contact sheets, filmstrips). Only true story stills are gated.
_SKIP_TOKENS = ("ref", "anchor", "probe", "bakeoff", "reface", "byteplus", "mocomic",
                "compare", "contact", "filmstrip", "preview", "audit", "review", "work",
                "_v3", "_fx", "_kin", "_mc", "_cap", "seg")


def is_production_png(p: Path) -> bool:
    """True for a story still that MUST pass the content gate; False for refs/helpers."""
    name = p.name.lower()
    if not name.endswith(".png") or name.startswith("_"):
        return False
    parts = str(p).replace("\\", "/").lower().split("/")
    # any parent dir that is a helper/work area disqualifies it
    if any(any(tok in seg for tok in _SKIP_TOKENS) for seg in parts[:-1]):
        return False
    return not any(tok in name for tok in _SKIP_TOKENS)


def _sidecar_verdict(png: Path) -> str | None:
    """Read the audit verdict, accepting BOTH sidecar schemas:
      - render_lint : <stem>.audit.json      with {"verdict": "PASS"|"FAIL"}
      - pipeline    : <stem>.png.audit.json   with {"passed": true|false}  (ImageAudit)
    A corrupt sidecar, or one with neither field, is treated as FAIL (fail-closed) —
    so a pipeline NEEDS-EYE audit (passed=false, written when the vision API is down)
    correctly blocks the gate instead of slipping through."""
    for side in (png.with_suffix(".audit.json"), png.with_name(png.name + ".audit.json")):
        if side.exists():
            try:
                d = json.loads(side.read_text(encoding="utf-8"))
            except Exception:
                return "FAIL"
            v = (d.get("verdict") or "").upper()
            if v:
                return v
            if "passed" in d:                       # pipeline ImageAudit schema
                return "PASS" if d.get("passed") is True else "FAIL"
            return "FAIL"                            # neither field -> untrusted
    return None


def gate_dir(folder) -> dict:
    """FAIL-CLOSED ship gate for one piece's stills.

    GREEN only if EVERY production PNG in `folder` (top level) has a PASS audit sidecar.
    A missing sidecar counts as UNAUDITED (blocked); anything that is not literally PASS
    (FAIL / SKIPPED / corrupt) counts as blocked. An empty folder is NOT green.
    This is the single authority a renderer/skill must consult before animate/assemble.
    """
    folder = Path(folder)
    pngs = sorted(p for p in folder.glob("*.png") if is_production_png(p))
    passed, failed, unaudited = [], [], []
    for p in pngs:
        v = _sidecar_verdict(p)
        if v == "PASS":
            passed.append(p.name)
        elif v is None:
            unaudited.append(p.name)
        else:
            failed.append(p.name)
    green = bool(pngs) and not failed and not unaudited
    return {"green": green, "dir": str(folder), "total": len(pngs),
            "pass": passed, "fail": failed, "unaudited": unaudited}


def worklist(folder, stage: str = "still") -> dict:
    """The batch a vision Agent must audit before gate_dir() can go green:
    every production still lacking a PASS sidecar, plus the checklist to apply to each."""
    g = gate_dir(folder)
    brief = content_brief(stage, subject="<per-still>")
    return {"dir": g["dir"], "todo": g["unaudited"] + g["fail"],
            "already_pass": g["pass"], "checklist": brief["always"] + brief["rule_checks"]}


def report_gate(folder) -> int:
    g = gate_dir(folder)
    print(f"\n=== STILL SHIP GATE (FAIL-CLOSED) - {g['dir']} ===")
    print(f"stills: {g['total']}  |  PASS {len(g['pass'])}  FAIL {len(g['fail'])}  UNAUDITED {len(g['unaudited'])}")
    for n in g["fail"]:
        print(f"  X FAIL      {n}")
    for n in g["unaudited"]:
        print(f"  ? UNAUDITED {n}  (blocked until a vision Agent records a verdict)")
    print(f"\nGATE: {'GREEN - every still PASSED, clear to animate/assemble' if g['green'] else 'BLOCKED - not shippable'}")
    if not g["green"]:
        print("  run  --worklist <dir>  to get the audit batch + checklist.")
    return 0 if g["green"] else 1


def report_worklist(folder, stage: str = "still") -> None:
    w = worklist(folder, stage)
    print(f"\n=== AUDIT WORKLIST - {w['dir']} ===")
    print(f"{len(w['todo'])} still(s) need a vision-Agent verdict "
          f"({len(w['already_pass'])} already PASS):")
    for n in w["todo"]:
        print(f"  [ ] {n}")
    print("\n-- checklist to apply BY EYE to EACH still (Read the PNG) --")
    for c in w["checklist"]:
        print(f"  [ ] {c}")
    print("\nRecord each with:  --record <png> --verdict PASS|FAIL --flags \"note; note\"")


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
    try:  # rules/checklist carry unicode (arrows, dashes); don't die on a cp1252 console
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--image"); ap.add_argument("--stage", default="still")
    ap.add_argument("--subject", default=""); ap.add_argument("--context", default="")
    ap.add_argument("--spec")
    ap.add_argument("--plan", help="scene plan JSON -> subject-variety gate")
    ap.add_argument("--gate", help="stills folder -> FAIL-CLOSED ship gate (exit 1 until all PASS)")
    ap.add_argument("--worklist", help="stills folder -> the audit batch + checklist")
    ap.add_argument("--record", help="a PNG -> write its <stem>.audit.json verdict")
    ap.add_argument("--verdict", choices=["PASS", "FAIL", "pass", "fail"], help="with --record")
    ap.add_argument("--flags", default="", help="with --record: '; '-separated defect notes")
    a = ap.parse_args()
    if a.gate:
        sys.exit(report_gate(Path(a.gate)))
    elif a.worklist:
        report_worklist(Path(a.worklist), a.stage)
    elif a.record:
        if not a.verdict:
            ap.error("--record requires --verdict PASS|FAIL")
        flags = [f.strip() for f in a.flags.split(";") if f.strip()]
        side = write_audit(Path(a.record), a.verdict, flags)
        print(f"recorded {a.verdict.upper()} -> {side}")
    elif a.plan:
        report_plan(Path(a.plan))
    elif a.spec:
        report_spec(Path(a.spec))
    elif a.image or a.subject:
        report_brief(a.stage, a.subject, a.context)
    else:
        ap.error("pass --gate/--worklist/--record (ship gate) / --plan / --spec / --image")


if __name__ == "__main__":
    main()
