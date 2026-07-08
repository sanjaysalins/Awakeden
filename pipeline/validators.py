"""Deterministic validators for the validation engine (see VALIDATION_ENGINE_PLAN.md).

These are PURE-CODE checks that run every change ($0, no LLM) and lock in the fixes
from the 2026-06-14 session of misses:
  - CLIP-VIRAL          : a Kling cut-plan must use the viral crop-cut sequence, NOT a slow zoom.
  - CLIP-IMAGE-GROUNDED : a cut-plan must not inject the scene's rich subject_block nouns
                          (blood / lamplight / first-light / pen) that made Kling hallucinate.
  - prompt_has_criteria : verify_image's audit prompt must still carry the period/tone + text + anatomy checks.
  - rules_integrity     : data/rules.json is well-formed and its memories/fixtures exist.

Vision-based rules (IMG-*, CLIP-FROZEN, CLIP-NOMORPH) are NOT unit-tested here (non-deterministic);
they are exercised by the on-demand vision calibration runner (validate_fixtures.py).
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "data" / "rules.json"
MEMORY_DIR = Path(r"C:\Users\sanjay\.claude\projects\C--Users-sanjay-PycharmProjects-JesusInTheBible\memory")


# ---------------------------------------------------------------- rules registry

def load_rules() -> list[dict]:
    data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    return data["rules"]


# ---------------------------------------------------------------- cut-plan shape

# Signatures of the OLD rich-text / hallucination-seeding cut-plan prompt. These are
# UNIQUE to the original build_cutplan (which injected the subject_block + a flame line);
# they are NOT present in the clean v2 camera-only plan, nor in the harmless boilerplate
# ("Scene contains: the scene is a painted tableau ... nothing moves") that image_to_kling
# appends to EVERY clip — so we must not flag a bare "Scene contains:".
_RICHTEXT_MARKERS = ("micro-motion", "flame stirs", "oil painting video clip",
                     "classical devotional oil painting realism")
# Phrases that prove the prompt forbids invented content (the anti-hallucination clause).
_FROZEN_MARKERS = ("nothing inside the painting", "frozen", "only the camera",
                   "fixed photograph", "static")
# A single-slow-zoom (the over-correction regression) reads like this.
_SLOWZOOM_MARKERS = ("one single", "single, very slow", "single slow", "slowly zooms in")


def _beats(kling_json: dict) -> list[dict]:
    return kling_json.get("beats", []) or []


def cutplan_viral(kling_json: dict) -> tuple[bool, str]:
    """CLIP-VIRAL: must be a crop-cut sequence (>=6 beats), not a 1-2 beat slow zoom."""
    beats = _beats(kling_json)
    prompt = (kling_json.get("prompt") or "").lower()
    if any(m in prompt for m in _SLOWZOOM_MARKERS) and len(beats) <= 3:
        return False, f"slow-zoom cut-plan ({len(beats)} beats, single push-in) — not a viral crop-cut edit"
    if len(beats) < 6:
        return False, f"only {len(beats)} beats — viral edit needs >=6 crop-cuts (full->mid->close->macro->return)"
    # at least a few distinct framings present in the beat descriptions
    descs = " ".join((b.get("description") or "").lower() for b in beats)
    framings = sum(1 for w in ("full", "mid", "close", "macro", "insert", "detail") if w in descs)
    if framings < 3:
        return False, f"beats lack framing variety (only {framings} framing words) — reads as a static hold"
    return True, f"viral crop-cut sequence ({len(beats)} beats, {framings} framings)"


def gate_cutplan(kling_json: dict, manifest: dict | None = None) -> tuple[bool, list[str]]:
    """Submit-gate: a cut-plan may only be used if it is BOTH viral (crop-cuts) AND
    image-grounded (no rich-text injection). When a locked element manifest is supplied
    (Visual v3, INV-25), the plan must ALSO be manifest-grounded — every beat targets a
    verified element, no invented writing surface. Deterministic, $0, fail-closed. Wire this
    in wherever a .kling.json is authored, BEFORE it reaches Kling."""
    problems: list[str] = []
    ok_v, r_v = cutplan_viral(kling_json)
    if not ok_v:
        problems.append(f"CLIP-VIRAL: {r_v}")
    ok_g, r_g = cutplan_image_grounded(kling_json)
    if not ok_g:
        problems.append(f"CLIP-IMAGE-GROUNDED: {r_g}")
    if manifest is not None:
        ok_m, r_m = cutplan_manifest_grounded(kling_json, manifest)
        if not ok_m:
            problems += [f"CLIP-MANIFEST-GROUNDED: {p}" for p in r_m]
    return (not problems), problems


# Generic full-frame / structural beat words that map to the whole composition (the "full"
# element), not to a specific cropped element.
_FRAMING_WORDS = {"full", "wide", "whole", "entire", "composition", "frame", "back",
                  "return", "establishing", "overview", "tableau", "scene"}


def _manifest_vocab(manifest: dict) -> tuple[set, set]:
    """The legal target vocabulary = VERIFIED element ids + label keywords + ambient words."""
    ids, words = set(), set()
    for e in manifest.get("elements", []):
        if not e.get("verified"):           # only verified elements are legal crop targets
            continue
        if e.get("id"):
            ids.add(e["id"].lower())
        words.update(re.findall(r"[a-z]{4,}", (e.get("label") or "").lower()))
    for amb in manifest.get("ambient_layer", []):
        words.update(re.findall(r"[a-z]{4,}", str(amb).lower()))
    return ids, words


def cutplan_manifest_grounded(kling_json: dict, manifest: dict) -> tuple[bool, list[str]]:
    """CLIP-MANIFEST-GROUNDED (INV-25): every cut beat must target a VERIFIED manifest
    element (by id or a label keyword) or be a generic full-frame beat. A beat that names a
    writing surface (titulus/inscription/sign/scroll) absent from the manifest is the
    invented-garbled-text seed (the 2026-06-18 bake-off 'BINTX' titulus) -> fail. Deterministic."""
    if not manifest or not manifest.get("elements"):
        return False, ["no manifest / no elements to ground against"]
    ids, words = _manifest_vocab(manifest)
    if not (ids or words):
        return False, ["manifest has no VERIFIED elements — nothing the edit may target"]
    allowed = ids | words | _FRAMING_WORDS
    problems: list[str] = []
    for i, b in enumerate(_beats(kling_json)):
        desc = (b.get("description") or "").lower()
        bad_writing = [t for t in _WRITING_SUBJECT
                       if t in desc and t not in words and t not in ids]
        if bad_writing:
            problems.append(f"beat {i}: targets writing surface '{bad_writing[0]}' "
                            "not in the manifest (invented-text seed)")
            continue
        toks = set(re.findall(r"[a-z]{3,}", desc))
        if not (toks & allowed):
            problems.append(f"beat {i}: '{desc[:48]}' targets no verified manifest element")
    return (not problems), problems


def cutplan_image_grounded(kling_json: dict) -> tuple[bool, str]:
    """CLIP-IMAGE-GROUNDED: prompt must NOT inject rich scene-text nouns, and MUST carry
    the anti-invention clause. This is the deterministic discriminator between the old
    text-seeded plan (hallucinated blood/lava/writing) and the clean camera-only plan."""
    prompt = (kling_json.get("prompt") or "").lower()
    hits = [m for m in _RICHTEXT_MARKERS if m in prompt]
    if hits:
        return False, f"prompt injects rich scene text ({', '.join(hits)}) — seeds Kling hallucination"
    if not any(m in prompt for m in _FROZEN_MARKERS):
        return False, "prompt lacks the anti-invention clause (frozen / only the camera / nothing moves)"
    return True, "camera-only, image-grounded (no rich-text injection, anti-invention clause present)"


# ---------------------------------------------------------------- never animate writing

# A scene whose SUBJECT is a writing surface: generative animation (Kling) morphs the
# letters into hallucinated garbled text (the recurring #02/#03/#04/#06 scroll defect).
_WRITING_SUBJECT = ("scroll", "titulus", "codex", "inscription", "placard", "parchment",
                    "manuscript", "stone tablet", "tablet of", "sign reading",
                    "sign that reads", "lettering", "engraved words", "the words of the",
                    "verse on", "written law", "open book", "scribe writing", "writing hand")
# Phrases that prove the text was deliberately designed UN-readable (safe to animate / hold).
_ILLEGIBLE_OK = ("illegible", "no legible", "unreadable", "no readable", "abstract mark",
                 "indistinct mark", "blurred mark", "suggested marks", "non-letterforms")


# Negated writing mentions ("no titulus", "without a scroll", "no lettering of any kind")
# are an EXCLUSION, not a writing subject — strip them before scanning so an explicit
# "no scroll present" does not false-flag the scene. (Found by the v2 Isaiah-53 build.)
_NEG_WRITING_RE = re.compile(
    r"\b(?:no|without|free of|not any|never|nor)\b[\w\s,]{0,30}?\b("
    + "|".join(re.escape(t) for t in _WRITING_SUBJECT) + r")\b")


def never_animate_writing(scene: dict) -> tuple[bool, str]:
    """NEVER-ANIMATE-WRITING (INV-17): a scene whose subject is a writing surface
    (scroll/titulus/codex/sign/inscription) must NOT go to generative animation — Kling
    morphs the letters into garbled text. Hold it as a still, give it a deterministic
    ffmpeg push-in, or exclude it from the cut. Returns ok=True when the scene is SAFE to
    animate. Scan subject_block/title/mood; explicitly-illegible OR explicitly-excluded passes."""
    text = " ".join(str(scene.get(k, "")) for k in ("subject_block", "title", "mood_block")).lower()
    scrubbed = _NEG_WRITING_RE.sub(" ", text)   # drop "no scroll / no titulus" exclusions
    hits = [t for t in _WRITING_SUBJECT if t in scrubbed]
    if not hits:
        return True, "no writing surface in subject — safe to animate"
    if any(s in text for s in _ILLEGIBLE_OK):
        return True, f"writing surface ({hits[0]}) explicitly designed illegible — safe"
    return False, (f"writing subject ({', '.join(hits)}) with intended legible text — do NOT "
                   "animate (hold as still / ffmpeg push-in / exclude from the cut)")


# ---------------------------------------------------------------- narrative-presence gate

_NARRATIVE_FACTS_PATH = ROOT / "data" / "narrative_facts.json"
_PRESENCE_WINDOW = 75   # chars after a character name to look for a presence/perception verb


def load_narrative_facts() -> list[dict]:
    if not _NARRATIVE_FACTS_PATH.exists():
        return []
    return json.loads(_NARRATIVE_FACTS_PATH.read_text(encoding="utf-8")).get("not_present", [])


def narrative_presence(spoken_text: str) -> tuple[bool, list[str]]:
    """NARRATIVE-PRESENCE (hard gate, defect class 'invented-narrative-detail', INV-4).
    FAIL the SPOKEN text when it asserts a known-absent Bible character watching/seeing/
    standing-at an event the record places them away from (e.g. 'Peter watched the
    scourging' — the disciples fled, Matt 26:56). Deterministic + fail-closed; ZERO false
    positives — only the curated data/narrative_facts.json pairings can fail (a true claim
    like 'John watched it at the cross' never trips, John not being listed). Pass ONLY the
    spoken text (not DEPTH notes, which may discuss these as negative examples)."""
    text = (spoken_text or "").lower()
    fails: list[str] = []
    for fact in load_narrative_facts():
        events = fact.get("event_words", [])
        if not any(ev in text for ev in events):
            continue                      # the event isn't in view — nothing to flag
        verbs = fact.get("presence_verbs", [])
        for alias in fact.get("aliases", []):
            pos = text.find(alias)
            hit = False
            while pos >= 0:
                window = text[pos: pos + len(alias) + _PRESENCE_WINDOW]
                if any(v in window for v in verbs):
                    hit = True
                    break
                pos = text.find(alias, pos + len(alias))
            if hit:
                fails.append(
                    f"NARRATIVE-PRESENCE: '{alias.title()}' asserted as watching/present at the "
                    f"event (near '{events[0]}*') — {fact.get('disproof', '')}")
                break                     # one fail per character is enough
    return (not fails), fails


# ---------------------------------------------------------------- prompt criteria guard

def prompt_has_criteria() -> tuple[bool, str]:
    """The verify_image audit prompt must still contain the period/tone, text, and anatomy
    checks. Guards against accidental removal (the period/tone check was added 2026-06-14).
    The role text lives in pipeline/visual_render.py; the period/tone check moved into the
    per-style config.STYLE_AUDIT_RUBRIC when the prompt was de-hardcoded from Baroque, so
    EVERY style rubric is checked (a new style must not ship without it)."""
    import config as _cfg  # root config, same import as visual_render

    src = (ROOT / "pipeline" / "visual_render.py").read_text(encoding="utf-8").lower()
    required = {
        "nsfw": "nsfw",
        "modern faces": "modern",
        "anatomy": "finger",
        "banned tokens": "banned",
    }
    missing = [name for name, needle in required.items() if needle not in src]
    rubrics = getattr(_cfg, "STYLE_AUDIT_RUBRIC", {})
    if not rubrics:
        missing.append("STYLE_AUDIT_RUBRIC (missing/empty)")
    for style_name, rubric in rubrics.items():
        low = rubric.lower()
        for name, needle in (("period authenticity", "period authenticity"),
                             ("horror tone", "horror")):
            if needle not in low:
                missing.append(f"{name} ({style_name} rubric)")
    if missing:
        return False, f"verify_image prompt missing checks: {', '.join(missing)}"
    return True, "verify_image carries period/tone + text + anatomy checks (all style rubrics)"


# ---------------------------------------------------------------- banned tokens

def banned_tokens(text: str) -> list[str]:
    """Return any banned visible-token strings present in text (reuses config list)."""
    from . import config as _cfg  # noqa
    toks = getattr(_cfg, "VISUAL_BANNED_TOKENS", set())
    low = (text or "").lower()
    return sorted(t for t in toks if t.lower() in low)


# ---------------------------------------------------------------- registry integrity

def rules_integrity() -> tuple[bool, list[str]]:
    """Every rule well-formed; validator + memory present; referenced fixtures exist in the
    manifest; referenced memory files exist on disk."""
    problems: list[str] = []
    rules = load_rules()
    ids = set()
    man_path = ROOT / "pipeline" / "validation_fixtures" / "manifest.json"
    manifest = {}
    if man_path.exists():
        manifest = json.loads(man_path.read_text(encoding="utf-8")).get("fixtures", {})
    for r in rules:
        rid = r.get("id", "<no-id>")
        if rid in ids:
            problems.append(f"{rid}: duplicate id")
        ids.add(rid)
        for key in ("id", "scope", "title", "description", "severity", "check", "validator", "memory"):
            if not r.get(key):
                problems.append(f"{rid}: missing/empty '{key}'")
        if r.get("scope") not in ("still", "clip", "cut", "text", "audio"):
            problems.append(f"{rid}: bad scope '{r.get('scope')}'")
        if r.get("severity") not in ("fail", "warn"):
            problems.append(f"{rid}: bad severity '{r.get('severity')}'")
        if r.get("check") not in ("deterministic", "vision"):
            problems.append(f"{rid}: bad check '{r.get('check')}'")
        mem = r.get("memory", "")
        if mem and not (MEMORY_DIR / f"{mem}.md").exists():
            problems.append(f"{rid}: memory '{mem}.md' not found")
        for fx in r.get("fixtures", []):
            if manifest and fx not in manifest:
                problems.append(f"{rid}: fixture '{fx}' not in manifest")
    return (not problems), problems
